import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';

export function activate(context: vscode.ExtensionContext) {
  const provider = new CADNativeEditorProvider(context);
  context.subscriptions.push(
    vscode.window.registerCustomEditorProvider(
      'cad.nativeViewer',
      provider,
      {
        webviewOptions: {
          retainContextWhenHidden: true
        },
        supportsMultipleEditorsPerDocument: true
      }
    )
  );

  // Register commands
  context.subscriptions.push(
    vscode.commands.registerCommand('cadNativeViewer.openWithCADViewer', async (uri?: vscode.Uri) => {
      const targetUri = uri || vscode.window.activeTextEditor?.document.uri;
      if (targetUri) {
        await vscode.commands.executeCommand('vscode.openWith', targetUri, 'cad.nativeViewer');
      }
    }),
    vscode.commands.registerCommand('cadNativeViewer.resetView', () => {
      vscode.window.showInformationMessage('Use FIT button in CAD viewer ribbon to reset view.');
    })
  );
}

export function deactivate() {}

class CADNativeEditorProvider implements vscode.CustomReadonlyEditorProvider {
  constructor(private readonly context: vscode.ExtensionContext) {}

  public async openCustomDocument(
    uri: vscode.Uri,
    _openContext: vscode.CustomDocumentOpenContext,
    _token: vscode.CancellationToken
  ): Promise<vscode.CustomDocument> {
    return { uri, dispose: () => {} };
  }

  public async resolveCustomEditor(
    document: vscode.CustomDocument,
    webviewPanel: vscode.WebviewPanel,
    _token: vscode.CancellationToken
  ): Promise<void> {
    const webview = webviewPanel.webview;
    const documentDir = path.dirname(document.uri.fsPath);

    webview.options = {
      enableScripts: true,
      localResourceRoots: [
        this.context.extensionUri,
        vscode.Uri.file(documentDir),
        vscode.Uri.file(path.resolve(documentDir, '..'))
      ]
    };

    webview.html = this.getHtmlForWebview(webviewPanel, document.uri);

    const messageListener = webview.onDidReceiveMessage(async (message) => {
      switch (message.type) {
        case 'ready': {
          await this.sendFileData(webviewPanel, document.uri);
          break;
        }
        case 'showInfo': {
          vscode.window.showInformationMessage(message.text);
          break;
        }
        case 'showError': {
          vscode.window.showErrorMessage(message.text);
          break;
        }
        case 'exportFile': {
          try {
            const defaultUri = vscode.Uri.file(
              path.join(documentDir, message.filename || 'exported_cad_model.glb')
            );
            const saveUri = await vscode.window.showSaveDialog({
              defaultUri,
              filters: {
                '3D Models & Documents': [message.format || 'glb']
              }
            });
            if (saveUri) {
              const buffer = typeof message.data === 'string'
                ? Buffer.from(message.data, 'utf-8')
                : Buffer.from(message.data);
              await vscode.workspace.fs.writeFile(saveUri, buffer);
              vscode.window.showInformationMessage(`Exported successfully to ${path.basename(saveUri.fsPath)}`);
            }
          } catch (err: any) {
            vscode.window.showErrorMessage(`Export failed: ${err?.message || err}`);
          }
          break;
        }
      }
    });

    webviewPanel.onDidDispose(() => {
      messageListener.dispose();
    });
  }

  private async sendFileData(webviewPanel: vscode.WebviewPanel, uri: vscode.Uri) {
    const filePath = uri.fsPath;
    const fileName = path.basename(filePath);
    const ext = path.extname(filePath).toLowerCase();
    const documentDir = path.dirname(filePath);
    const baseName = path.basename(filePath, ext);

    try {
      const fileBytes = await vscode.workspace.fs.readFile(uri);
      const companion = await this.resolveCompanion(documentDir, baseName, ext);

      webviewPanel.webview.postMessage({
        type: 'loadCAD',
        fileName,
        extension: ext,
        fileSize: fileBytes.byteLength,
        fileData: fileBytes.buffer,
        companion
      });
    } catch (err: any) {
      webviewPanel.webview.postMessage({
        type: 'error',
        message: `Failed to read file ${fileName}: ${err.message}`
      });
    }
  }

  private async resolveCompanion(documentDir: string, baseName: string, ext: string) {
    if (ext !== '.sldprt' && ext !== '.sldasm') {
      return null;
    }

    const searchDirs = [
      documentDir,
      path.resolve(documentDir, '..', 'step'),
      path.resolve(documentDir, '..', 'glb'),
      path.resolve(documentDir, '..', 'export'),
      path.resolve(documentDir, '..', 'cad', 'step'),
      path.resolve(documentDir, '..', 'cad', 'glb')
    ];

    const extensionsToLookFor = ['.step', '.stp', '.glb', '.gltf', '.stl', '.obj'];

    for (const dir of searchDirs) {
      if (!fs.existsSync(dir)) continue;

      for (const targetExt of extensionsToLookFor) {
        const candidate = path.join(dir, `${baseName}${targetExt}`);
        if (fs.existsSync(candidate)) {
          const compBytes = await vscode.workspace.fs.readFile(vscode.Uri.file(candidate));
          return {
            fileName: path.basename(candidate),
            extension: targetExt,
            fileSize: compBytes.byteLength,
            fileData: compBytes.buffer,
            relativePath: path.relative(documentDir, candidate)
          };
        }
      }

      if (ext === '.sldasm') {
        const files = fs.readdirSync(dir);
        const stepAssembly = files.find(f => f.toLowerCase().endsWith('.step') || f.toLowerCase().endsWith('.stp'));
        if (stepAssembly) {
          const candidate = path.join(dir, stepAssembly);
          const compBytes = await vscode.workspace.fs.readFile(vscode.Uri.file(candidate));
          return {
            fileName: path.basename(candidate),
            extension: path.extname(candidate).toLowerCase(),
            fileSize: compBytes.byteLength,
            fileData: compBytes.buffer,
            relativePath: path.relative(documentDir, candidate)
          };
        }
      }
    }

    return null;
  }

  private getHtmlForWebview(webviewPanel: vscode.WebviewPanel, uri: vscode.Uri): string {
    const webview = webviewPanel.webview;
    const mediaUri = vscode.Uri.joinPath(this.context.extensionUri, 'media');
    const distUri = vscode.Uri.joinPath(this.context.extensionUri, 'dist');

    const scriptUri = webview.asWebviewUri(vscode.Uri.joinPath(distUri, 'webview.js'));
    const styleUri = webview.asWebviewUri(vscode.Uri.joinPath(mediaUri, 'viewer.css'));
    const wasmUri = webview.asWebviewUri(vscode.Uri.joinPath(mediaUri, 'occt-import-js.wasm'));

    const nonce = getNonce();
    const fileName = path.basename(uri.fsPath);

    return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="Content-Security-Policy" content="
    default-src 'none';
    img-src ${webview.cspSource} data: blob:;
    style-src ${webview.cspSource} 'unsafe-inline';
    script-src 'nonce-${nonce}' ${webview.cspSource} 'wasm-unsafe-eval' 'unsafe-eval';
    connect-src ${webview.cspSource} blob: data:;
  ">
  <title>CAD Native 3D Viewer - ${escapeHtml(fileName)}</title>
  <link rel="stylesheet" href="${styleUri}">
</head>
<body class="cad-body" data-wasm-uri="${wasmUri}">
  <!-- Top Command Ribbon -->
  <header class="cad-header">
    <div class="header-left">
      <div class="logo-badge">
        <svg class="cube-icon" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
          <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
          <line x1="12" y1="22.08" x2="12" y2="12"></line>
        </svg>
        <span class="app-title">CAD 3D NATIVE</span>
      </div>
      <div class="file-info-chip">
        <span id="doc-filename" class="chip-name">${escapeHtml(fileName)}</span>
        <span id="doc-format-badge" class="chip-badge">DETECTING...</span>
        <span id="doc-size-badge" class="chip-size">-- KB</span>
      </div>
    </div>

    <!-- Center View & Shading Controls -->
    <div class="header-center">
      <div class="btn-group" role="group">
        <button id="btn-view-iso" class="btn" title="Isometric Projection">ISO</button>
        <button id="btn-view-front" class="btn" title="Front Elevation">FRONT</button>
        <button id="btn-view-top" class="btn" title="Top Plan">TOP</button>
        <button id="btn-view-right" class="btn" title="Right Profile">RIGHT</button>
        <button id="btn-view-fit" class="btn" title="Zoom Fit All (Home)">FIT</button>
      </div>

      <div class="divider"></div>

      <!-- Shading Mode Group -->
      <div class="btn-group" role="group">
        <button id="btn-mode-shaded" class="btn active" title="Shaded Realistic PBR">SHADED</button>
        <button id="btn-mode-edges" class="btn" title="Shaded with Sharp CAD Edges">EDGES</button>
        <button id="btn-mode-wire" class="btn" title="Technical Wireframe">WIRE</button>
        <button id="btn-mode-xray" class="btn" title="X-Ray Ghosted">X-RAY</button>
      </div>

      <div class="divider"></div>

      <!-- Theme Switcher -->
      <div class="btn-group" role="group">
        <button id="btn-theme-dark" class="btn active" title="Industrial Dark Theme">DARK</button>
        <button id="btn-theme-light" class="btn" title="Studio Light Theme">LIGHT</button>
        <button id="btn-theme-blueprint" class="btn" title="Technical Blueprint Theme">BLUEPRINT</button>
      </div>
    </div>

    <!-- Right Engineering Toolset -->
    <div class="header-right">
      <button id="btn-toggle-explode" class="btn tool-btn" title="Exploded Assembly View">
        <span class="icon">&#128165;</span> EXPLODE
      </button>
      <button id="btn-toggle-section" class="btn tool-btn" title="Toggle 3-Axis Cross-Section Slicing">
        <span class="icon">&#9986;</span> SLICE
      </button>
      <button id="btn-toggle-measure" class="btn tool-btn" title="Precision Metrology Caliper">
        <span class="icon">&#128207;</span> MEASURE
      </button>
      <button id="btn-toggle-markup" class="btn tool-btn" title="3D Engineering Redlines & Review Pins">
        <span class="icon">&#128204;</span> MARKUP
      </button>
      <button id="btn-toggle-tree" class="btn tool-btn active" title="Component Hierarchy Tree">
        <span class="icon">&#9776;</span> TREE
      </button>
      <button id="btn-export-menu" class="btn tool-btn primary" title="Export Model / Snapshot">
        <span class="icon">&#128190;</span> EXPORT
      </button>
    </div>
  </header>

  <!-- Main Viewport Area -->
  <div class="cad-main">
    <!-- Left Sidebar: Component Tree & Materials -->
    <aside id="sidebar-left" class="sidebar sidebar-left">
      <div class="sidebar-header">
        <span class="sidebar-title">MODEL COMPONENTS</span>
        <span id="part-count-badge" class="count-pill">0</span>
      </div>
      <div class="sidebar-actions">
        <button id="btn-show-all" class="text-btn">Show All</button>
        <button id="btn-isolate-clear" class="text-btn">Clear Isolate</button>
      </div>
      <div id="component-tree" class="tree-container">
        <!-- Dynamically generated part tree nodes -->
      </div>
      
      <!-- Engineering Title Block Attribution -->
      <div class="plant-meta-card">
        <div class="meta-row"><span class="meta-label">DISCIPLINE:</span> <span class="meta-val">Chemical & Mechanical Engineering</span></div>
        <div class="meta-row"><span class="meta-label">INSTITUTION:</span> <span class="meta-val">Jadavpur University</span></div>
        <div class="meta-row"><span class="meta-label">DESIGNER:</span> <span class="meta-val highlight">Sourish Senapati</span></div>
        <div class="meta-row"><span class="meta-label">ROLL NO:</span> <span class="meta-val">002310301035</span></div>
        <div class="meta-row"><span class="meta-label">ASME CODE:</span> <span class="meta-val">Sec VIII Div 1 (2024 ED)</span></div>
      </div>
    </aside>

    <!-- Canvas Container -->
    <div id="viewport-container" class="viewport-container">
      <canvas id="cad-canvas"></canvas>

      <!-- Interactive 3D Orientation ViewCube -->
      <div id="viewcube-container" class="viewcube-container" title="Click faces, edges or corners to rotate view">
        <canvas id="viewcube-canvas" width="110" height="110"></canvas>
      </div>

      <!-- Exploded View Floating Panel -->
      <div id="explode-panel" class="floating-panel hidden">
        <div class="panel-header">
          <span>EXPLODED ASSEMBLY DISASSEMBLY</span>
          <button id="btn-close-explode" class="close-btn">&times;</button>
        </div>
        <div class="panel-body">
          <div class="slider-control">
            <div class="flex-between">
              <span>Separation Distance:</span>
              <strong id="explode-val">0%</strong>
            </div>
            <input type="range" id="explode-slider" min="0" max="100" value="0">
          </div>
          <div class="flex-row gap-2 mt-2">
            <button id="btn-animate-explode" class="btn full-btn">Play / Pause Cycle</button>
            <button id="btn-reset-explode" class="btn full-btn">Collapse</button>
          </div>
        </div>
      </div>

      <!-- Dynamic Section Slicing Floating Panel -->
      <div id="section-panel" class="floating-panel hidden">
        <div class="panel-header">
          <span>CROSS-SECTION SLICING (DYNAMIC CUTAWAY)</span>
          <button id="btn-close-section" class="close-btn">&times;</button>
        </div>
        <div class="panel-body">
          <div class="slice-control">
            <label><input type="checkbox" id="slice-x-enable"> Cut X-Plane</label>
            <input type="range" id="slice-x-slider" min="-100" max="100" value="0" disabled>
            <button id="slice-x-flip" class="mini-btn" title="Invert Normal">Flip</button>
          </div>
          <div class="slice-control">
            <label><input type="checkbox" id="slice-y-enable"> Cut Y-Plane (Elevation)</label>
            <input type="range" id="slice-y-slider" min="-100" max="100" value="0" disabled>
            <button id="slice-y-flip" class="mini-btn" title="Invert Normal">Flip</button>
          </div>
          <div class="slice-control">
            <label><input type="checkbox" id="slice-z-enable"> Cut Z-Plane</label>
            <input type="range" id="slice-z-slider" min="-100" max="100" value="0" disabled>
            <button id="slice-z-flip" class="mini-btn" title="Invert Normal">Flip</button>
          </div>
          <div class="slice-options">
            <label><input type="checkbox" id="slice-show-caps" checked> Solid Cross-Section Cap Filling</label>
          </div>
        </div>
      </div>

      <!-- Precision Metrology & Caliper Panel -->
      <div id="measurement-panel" class="floating-panel hidden">
        <div class="panel-header">
          <span>PRECISION METROLOGY CALIPER</span>
          <button id="btn-close-measure" class="close-btn">&times;</button>
        </div>
        <div class="panel-body">
          <div class="measure-type-selector">
            <label><input type="radio" name="measure-mode" value="distance" checked> 2-Pt Distance</label>
            <label><input type="radio" name="measure-mode" value="angle"> 3-Pt Angle</label>
          </div>
          <p id="measure-instructions" class="instruction-text">Click two vertices/points on the 3D model to calculate 3D Euclidean distance.</p>
          <div class="measure-results">
            <div id="meas-dist-block">
              <div class="res-row"><span>Distance (D):</span> <strong id="m-dist">0.000 mm</strong></div>
              <div class="res-row"><span>&Delta;X:</span> <span id="m-dx">0.000 mm</span></div>
              <div class="res-row"><span>&Delta;Y:</span> <span id="m-dy">0.000 mm</span></div>
              <div class="res-row"><span>&Delta;Z:</span> <span id="m-dz">0.000 mm</span></div>
            </div>
            <div id="meas-angle-block" class="hidden">
              <div class="res-row"><span>Enclosed Angle (&theta;):</span> <strong id="m-angle">0.00&deg;</strong></div>
              <div class="res-row"><span>Vertex Point B:</span> <span id="m-angle-pt">--</span></div>
            </div>
          </div>
          <button id="btn-clear-measure" class="btn full-btn">Reset Points</button>
        </div>
      </div>

      <!-- 3D Engineering Markup & Review Panel -->
      <div id="markup-panel" class="floating-panel hidden">
        <div class="panel-header">
          <span>3D ENGINEERING REVIEW & MARKUPS</span>
          <button id="btn-close-markup" class="close-btn">&times;</button>
        </div>
        <div class="panel-body">
          <p class="instruction-text">Click on any 3D model surface to drop an inspection pin.</p>
          <div class="markup-input-row">
            <input type="text" id="markup-text-input" placeholder="Enter engineering comment / note..." class="text-input">
            <button id="btn-add-pin-prompt" class="mini-btn primary-mini">Drop Pin</button>
          </div>
          <div id="markup-pins-list" class="pins-list">
            <!-- Dynamic pins list -->
          </div>
          <button id="btn-export-markups" class="btn full-btn mt-2">Export Review Report (.json)</button>
        </div>
      </div>

      <!-- Export Floating Modal -->
      <div id="export-panel" class="floating-panel hidden">
        <div class="panel-header">
          <span>EXPORT CAD GEOMETRY & SNAPSHOT</span>
          <button id="btn-close-export" class="close-btn">&times;</button>
        </div>
        <div class="panel-body">
          <button id="btn-export-glb" class="btn full-btn mb-2">Export to GLB (Binary GLTF)</button>
          <button id="btn-export-stl" class="btn full-btn mb-2">Export to STL (3D Printing)</button>
          <button id="btn-export-obj" class="btn full-btn mb-2">Export to Wavefront OBJ</button>
          <button id="btn-export-png" class="btn full-btn">Save Ultra-HD Snapshot (PNG)</button>
        </div>
      </div>

      <!-- HUD Loading & Parsing Overlay -->
      <div id="loading-overlay" class="loading-overlay">
        <div class="loader-box">
          <div class="cad-spinner"></div>
          <h3 id="loader-status" class="loader-title">PARSING CAD GEOMETRY</h3>
          <p id="loader-substatus" class="loader-sub">Loading OpenCASCADE WebAssembly CAD kernel...</p>
          <div class="progress-bar-wrap">
            <div id="loader-progress" class="progress-bar-fill"></div>
          </div>
        </div>
      </div>

      <!-- Companion Notification Bar -->
      <div id="companion-banner" class="companion-banner hidden">
        <span class="icon">&#9432;</span>
        <span id="companion-text">Companion 3D representation loaded.</span>
        <button id="companion-dismiss" class="mini-btn">&times;</button>
      </div>
    </div>

    <!-- Right Sidebar: Physical & Geometric Properties -->
    <aside id="sidebar-right" class="sidebar sidebar-right">
      <div class="sidebar-header">
        <span class="sidebar-title">ENGINEERING SPECS</span>
      </div>
      <div class="specs-group">
        <div class="spec-title">BOUNDING ENVELOPE</div>
        <div class="spec-row"><span>Length (X):</span> <strong id="spec-dim-x">-- mm</strong></div>
        <div class="spec-row"><span>Height (Y):</span> <strong id="spec-dim-y">-- mm</strong></div>
        <div class="spec-row"><span>Width (Z):</span> <strong id="spec-dim-z">-- mm</strong></div>
        <div class="spec-row"><span>Diagonal:</span> <strong id="spec-dim-diag">-- mm</strong></div>
      </div>

      <div class="specs-group">
        <div class="spec-title">TOPOLOGY STATS</div>
        <div class="spec-row"><span>Bodies / Meshes:</span> <strong id="spec-meshes">--</strong></div>
        <div class="spec-row"><span>Total Triangles:</span> <strong id="spec-triangles">--</strong></div>
        <div class="spec-row"><span>Total Vertices:</span> <strong id="spec-vertices">--</strong></div>
        <div class="spec-row"><span>B-Rep Solids:</span> <strong id="spec-solids">--</strong></div>
      </div>

      <div class="specs-group">
        <div class="spec-title">LIGHTING & RENDERING</div>
        <div class="slider-control">
          <span>Exposure:</span>
          <input type="range" id="render-exposure" min="0.2" max="3.0" step="0.1" value="1.2">
        </div>
        <div class="slider-control">
          <span>Roughness:</span>
          <input type="range" id="render-roughness" min="0.05" max="1.0" step="0.05" value="0.35">
        </div>
        <div class="slider-control">
          <span>Metalness:</span>
          <input type="range" id="render-metalness" min="0.0" max="1.0" step="0.05" value="0.75">
        </div>
      </div>

      <div class="specs-group">
        <div class="spec-title">NAVIGATION SHORTCUTS</div>
        <div class="shortcuts-list">
          <div><kbd>Left Click + Drag</kbd> Rotate / Orbit</div>
          <div><kbd>Right Click + Drag</kbd> Pan View</div>
          <div><kbd>Scroll Wheel</kbd> Zoom In / Out</div>
          <div><kbd>Double Click</kbd> Focus on Part</div>
          <div><kbd>H</kbd> Fit to Screen</div>
          <div><kbd>M</kbd> Toggle Caliper</div>
          <div><kbd>E</kbd> Toggle Explode</div>
        </div>
      </div>
    </aside>
  </div>

  <script nonce="${nonce}" src="${scriptUri}"></script>
</body>
</html>`;
  }
}

function getNonce(): string {
  let text = '';
  const possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  for (let i = 0; i < 32; i++) {
    text += possible.charAt(Math.floor(Math.random() * possible.length));
  }
  return text;
}

function escapeHtml(text: string): string {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
