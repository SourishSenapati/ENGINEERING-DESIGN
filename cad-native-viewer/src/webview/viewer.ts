import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { STLLoader } from 'three/examples/jsm/loaders/STLLoader.js';
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader.js';
import { GLTFExporter } from 'three/examples/jsm/exporters/GLTFExporter.js';
import { STLExporter } from 'three/examples/jsm/exporters/STLExporter.js';
import { OBJExporter } from 'three/examples/jsm/exporters/OBJExporter.js';
import occtimportjs from 'occt-import-js';
import { CADPluginManager, CADViewerAPI, CADModelContext, CADViewerPlugin } from './plugin-system';
import { createFEAStressPlugin } from './fea-stress-plugin';

// Make THREE globally accessible for 3rd-party and proprietary plugins
(window as any).THREE = THREE;

// Acquire VS Code API
declare function acquireVsCodeApi(): {
  postMessage: (msg: any) => void;
  getState: () => any;
  setState: (state: any) => void;
};

const vscode = acquireVsCodeApi();

// Engineering harmonious color palette for subassemblies
const CAD_PALETTE = [
  0x94a3b8, // Slate / Pressure Shell
  0x38bdf8, // Sky Blue / Tubes
  0xf59e0b, // Amber / Tubesheets
  0x10b981, // Emerald / Baffles
  0x6366f1, // Indigo / Skirt Support
  0xec4899, // Pink / Flanges & Nozzles
  0x14b8a6, // Teal
  0xa855f7, // Purple
  0xf97316  // Orange
];

interface CADMeshEntry {
  id: string;
  name: string;
  mesh: THREE.Mesh;
  edges?: THREE.LineSegments;
  color: THREE.Color;
  visible: boolean;
  triangleCount: number;
  vertexCount: number;
  initialPosition: THREE.Vector3;
  explodeVector: THREE.Vector3;
}

interface MarkupPin {
  id: number;
  note: string;
  position: THREE.Vector3;
  markerMesh: THREE.Mesh;
}

class CADNativeViewerApp {
  private canvas: HTMLCanvasElement;
  private renderer: THREE.WebGLRenderer;
  private scene: THREE.Scene;
  private camera: THREE.PerspectiveCamera;
  private controls: OrbitControls;
  private rootGroup: THREE.Group;
  private gridHelper: THREE.GridHelper;

  // 3rd Party & Proprietary Tool Plugin Manager
  private pluginManager: CADPluginManager;

  // ViewCube
  private viewCubeCanvas: HTMLCanvasElement;
  private viewCubeRenderer: THREE.WebGLRenderer;
  private viewCubeScene: THREE.Scene;
  private viewCubeCamera: THREE.PerspectiveCamera;
  private viewCubeMesh: THREE.Mesh;

  private meshEntries: CADMeshEntry[] = [];
  private currentShadingMode: 'shaded' | 'edges' | 'wire' | 'xray' = 'shaded';
  private currentTheme: 'dark' | 'light' | 'blueprint' = 'dark';

  // Clipping planes for dynamic section slicing
  private clipPlanes = {
    x: new THREE.Plane(new THREE.Vector3(-1, 0, 0), 0),
    y: new THREE.Plane(new THREE.Vector3(0, -1, 0), 0),
    z: new THREE.Plane(new THREE.Vector3(0, 0, -1), 0)
  };
  private activeClipPlanes: THREE.Plane[] = [];
  private modelBoundingBox = new THREE.Box3();
  private modelCenter = new THREE.Vector3();
  private modelSize = new THREE.Vector3();
  private currentFileName: string = 'model';
  private currentExtension: string = '';
  private currentFileSize: number = 0;

  // Exploded View
  private explodeFactor: number = 0;
  private isExplodeAnimating: boolean = false;
  private explodeAnimDirection: number = 1;

  // Metrology Caliper
  private measureActive: boolean = false;
  private measureMode: 'distance' | 'angle' = 'distance';
  private measurePoints: THREE.Vector3[] = [];
  private measureGroup: THREE.Group;

  // 3D Markups & Redlines
  private markupActive: boolean = false;
  private markupPins: MarkupPin[] = [];
  private markupGroup: THREE.Group;
  private nextPinId: number = 1;

  private raycaster = new THREE.Raycaster();
  private mouse = new THREE.Vector2();
  private clock = new THREE.Clock();

  // WASM URI
  private wasmUri: string;

  constructor() {
    this.canvas = document.getElementById('cad-canvas') as HTMLCanvasElement;
    this.viewCubeCanvas = document.getElementById('viewcube-canvas') as HTMLCanvasElement;
    this.wasmUri = document.body.dataset.wasmUri || 'occt-import-js.wasm';

    // 1. Initialize Main Scene & Renderer
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x0f172a);

    this.renderer = new THREE.WebGLRenderer({
      canvas: this.canvas,
      antialias: true,
      alpha: false,
      powerPreference: 'high-performance',
      preserveDrawingBuffer: true
    });
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.localClippingEnabled = true;
    this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = 1.2;

    // 2. Main Camera & Controls
    const container = document.getElementById('viewport-container')!;
    const width = container.clientWidth || window.innerWidth;
    const height = container.clientHeight || window.innerHeight;
    this.camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 50000);
    this.camera.position.set(2000, 2000, 2000);

    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.05;
    this.controls.screenSpacePanning = true;

    // 3. Groups & Lighting
    this.rootGroup = new THREE.Group();
    this.scene.add(this.rootGroup);

    this.measureGroup = new THREE.Group();
    this.scene.add(this.measureGroup);

    this.markupGroup = new THREE.Group();
    this.scene.add(this.markupGroup);

    this.setupLighting();

    // 4. Ground Reference Grid
    this.gridHelper = new THREE.GridHelper(5000, 50, 0x334155, 0x1e293b);
    this.gridHelper.position.y = -0.5;
    this.scene.add(this.gridHelper);

    // 5. Initialize 3D ViewCube
    this.initViewCube();

    // 6. Initialize 3rd Party & Proprietary Tool SDK
    this.initPluginSDK();

    // 7. Setup Events & UI Listeners
    this.setupUIListeners();
    this.setupResizeObserver();
    this.setupCanvasClicks();

    // 8. Start Render Loop
    this.animate();

    // 9. Tell extension we are ready to receive CAD model
    vscode.postMessage({ type: 'ready' });
  }

  private initPluginSDK() {
    const api: CADViewerAPI = {
      scene: this.scene,
      camera: this.camera,
      renderer: this.renderer,
      rootGroup: this.rootGroup,
      getModelContext: () => this.getModelContext(),
      focusOnMesh: (mesh) => this.focusOnMesh(mesh),
      fitCamera: () => this.fitCameraToModel(),
      addMeshToScene: (obj) => this.rootGroup.add(obj),
      removeMeshFromScene: (obj) => this.rootGroup.remove(obj),
      setMeshColor: (meshId, hex) => {
        const found = this.meshEntries.find(m => m.id === meshId);
        if (found) {
          (found.mesh.material as THREE.MeshStandardMaterial).color.setHex(hex);
        }
      },
      applyVertexColors: (meshId, colorsRGB) => {
        const found = this.meshEntries.find(m => m.id === meshId);
        if (found) {
          found.mesh.geometry.setAttribute('color', new THREE.BufferAttribute(colorsRGB, 3));
          (found.mesh.material as THREE.MeshStandardMaterial).vertexColors = true;
          found.mesh.material.needsUpdate = true;
        }
      },
      resetMeshColors: () => {
        this.meshEntries.forEach(m => {
          (m.mesh.material as THREE.MeshStandardMaterial).color.copy(m.color);
          if (m.mesh.geometry.attributes.color) {
            m.mesh.geometry.deleteAttribute('color');
          }
          (m.mesh.material as THREE.MeshStandardMaterial).vertexColors = false;
          m.mesh.material.needsUpdate = true;
        });
      },
      addToolbarButton: (btnConfig) => {
        const headerRight = document.querySelector('.header-right')!;
        const btn = document.createElement('button');
        btn.id = btnConfig.id;
        btn.className = 'btn tool-btn';
        if (btnConfig.tooltip) btn.title = btnConfig.tooltip;
        btn.innerHTML = `${btnConfig.iconHtml ? `<span class="icon">${btnConfig.iconHtml}</span>` : ''} ${btnConfig.label}`;
        btn.onclick = () => btnConfig.onClick(api);
        headerRight.insertBefore(btn, document.getElementById('btn-export-menu'));
      },
      addFloatingPanel: (panelConfig) => {
        const container = document.getElementById('viewport-container')!;
        const panel = document.createElement('div');
        panel.id = panelConfig.id;
        panel.className = 'floating-panel hidden';
        panel.style.right = '130px';
        panel.style.top = '16px';
        panel.style.maxWidth = '340px';

        panel.innerHTML = `
          <div class="panel-header">
            <span>${panelConfig.title}</span>
            <button class="close-btn">&times;</button>
          </div>
          <div class="panel-body"></div>
        `;

        panel.querySelector('.close-btn')!.addEventListener('click', () => {
          panel.classList.add('hidden');
        });

        const body = panel.querySelector('.panel-body') as HTMLElement;
        panelConfig.onRender(body, api);
        container.appendChild(panel);
      },
      togglePanel: (panelId, force) => {
        const panel = document.getElementById(panelId);
        if (panel) {
          if (force !== undefined) {
            panel.classList.toggle('hidden', !force);
          } else {
            panel.classList.toggle('hidden');
          }
        }
      },
      postMessageToHost: (type, payload) => {
        vscode.postMessage({ type, ...payload });
      }
    };

    this.pluginManager = new CADPluginManager(api);

    // Register built-in commercial-grade 3rd-party FEA plugin
    this.pluginManager.registerPlugin(createFEAStressPlugin());

    // Expose SDK globally so external scripts / iframe embeds can register plugins
    (window as any).CADViewerSDK = this.pluginManager;
  }

  private getModelContext(): CADModelContext | null {
    if (this.meshEntries.length === 0) return null;
    return {
      fileName: this.currentFileName,
      extension: this.currentExtension,
      fileSize: this.currentFileSize,
      meshes: this.meshEntries.map(m => ({
        id: m.id,
        name: m.name,
        mesh: m.mesh,
        color: m.color,
        triangleCount: m.triangleCount,
        vertexCount: m.vertexCount
      })),
      boundingBox: this.modelBoundingBox.clone(),
      size: this.modelSize.clone(),
      center: this.modelCenter.clone()
    };
  }

  private setupLighting() {
    const hemiLight = new THREE.HemisphereLight(0xffffff, 0x334155, 1.2);
    hemiLight.position.set(0, 5000, 0);
    this.scene.add(hemiLight);

    const keyLight = new THREE.DirectionalLight(0xffffff, 1.5);
    keyLight.position.set(3000, 4000, 3000);
    this.scene.add(keyLight);

    const fillLight = new THREE.DirectionalLight(0x94a3b8, 0.8);
    fillLight.position.set(-3000, -2000, -3000);
    this.scene.add(fillLight);

    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    this.scene.add(ambientLight);
  }

  // --- Interactive 3D ViewCube ---
  private initViewCube() {
    this.viewCubeScene = new THREE.Scene();
    this.viewCubeCamera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
    this.viewCubeCamera.position.set(0, 0, 4);

    this.viewCubeRenderer = new THREE.WebGLRenderer({
      canvas: this.viewCubeCanvas,
      alpha: true,
      antialias: true
    });
    this.viewCubeRenderer.setSize(110, 110);
    this.viewCubeRenderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    const amb = new THREE.AmbientLight(0xffffff, 1.0);
    this.viewCubeScene.add(amb);
    const dir = new THREE.DirectionalLight(0xffffff, 0.8);
    dir.position.set(2, 4, 3);
    this.viewCubeScene.add(dir);

    const createFaceTexture = (text: string) => {
      const c = document.createElement('canvas');
      c.width = 128;
      c.height = 128;
      const ctx = c.getContext('2d')!;
      ctx.fillStyle = '#1e293b';
      ctx.fillRect(0, 0, 128, 128);
      ctx.strokeStyle = '#38bdf8';
      ctx.lineWidth = 6;
      ctx.strokeRect(4, 4, 120, 120);
      ctx.fillStyle = '#f0f6fc';
      ctx.font = 'bold 30px monospace';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(text, 64, 64);
      return new THREE.CanvasTexture(c);
    };

    const materials = [
      new THREE.MeshStandardMaterial({ map: createFaceTexture('RIGHT'), roughness: 0.4 }),
      new THREE.MeshStandardMaterial({ map: createFaceTexture('LEFT'), roughness: 0.4 }),
      new THREE.MeshStandardMaterial({ map: createFaceTexture('TOP'), roughness: 0.4 }),
      new THREE.MeshStandardMaterial({ map: createFaceTexture('BOTTOM'), roughness: 0.4 }),
      new THREE.MeshStandardMaterial({ map: createFaceTexture('FRONT'), roughness: 0.4 }),
      new THREE.MeshStandardMaterial({ map: createFaceTexture('BACK'), roughness: 0.4 })
    ];

    const geo = new THREE.BoxGeometry(1.6, 1.6, 1.6);
    this.viewCubeMesh = new THREE.Mesh(geo, materials);
    this.viewCubeScene.add(this.viewCubeMesh);

    this.viewCubeCanvas.addEventListener('click', (event) => {
      const rect = this.viewCubeCanvas.getBoundingClientRect();
      const x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
      const y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
      const ray = new THREE.Raycaster();
      ray.setFromCamera(new THREE.Vector2(x, y), this.viewCubeCamera);
      const hits = ray.intersectObject(this.viewCubeMesh);
      if (hits.length > 0 && hits[0].face) {
        const normal = hits[0].face.normal.clone();
        normal.applyEuler(this.viewCubeMesh.rotation);
        const dist = Math.max(this.modelSize.x, this.modelSize.y, this.modelSize.z) * 1.8;
        this.camera.position.set(normal.x * dist, normal.y * dist, normal.z * dist);
        this.controls.target.set(0, 0, 0);
        this.controls.update();
      }
    });
  }

  private animate = () => {
    requestAnimationFrame(this.animate);
    const delta = this.clock.getDelta();

    // Animate exploded view if cycling
    if (this.isExplodeAnimating) {
      this.explodeFactor += 0.8 * this.explodeAnimDirection;
      if (this.explodeFactor >= 100) {
        this.explodeFactor = 100;
        this.explodeAnimDirection = -1;
      } else if (this.explodeFactor <= 0) {
        this.explodeFactor = 0;
        this.explodeAnimDirection = 1;
      }
      (document.getElementById('explode-slider') as HTMLInputElement).value = this.explodeFactor.toString();
      document.getElementById('explode-val')!.textContent = `${Math.round(this.explodeFactor)}%`;
      this.applyExplodedView(this.explodeFactor);
    }

    // Notify plugins of frame update
    if (this.pluginManager) {
      this.pluginManager.notifyFrame(delta);
    }

    this.controls.update();
    this.renderer.render(this.scene, this.camera);

    // Sync ViewCube orientation with main camera
    if (this.viewCubeMesh) {
      this.viewCubeMesh.quaternion.copy(this.camera.quaternion).invert();
      this.viewCubeRenderer.render(this.viewCubeScene, this.viewCubeCamera);
    }
  };

  private setupResizeObserver() {
    const container = document.getElementById('viewport-container')!;
    const resize = () => {
      const width = container.clientWidth;
      const height = container.clientHeight;
      if (width === 0 || height === 0) return;
      this.camera.aspect = width / height;
      this.camera.updateProjectionMatrix();
      this.renderer.setSize(width, height);
    };
    window.addEventListener('resize', resize);
    const ro = new ResizeObserver(resize);
    ro.observe(container);
    resize();
  }

  // --- CAD Model Loading & Dispatcher ---
  public async loadCAD(msg: any) {
    const { fileName, extension, fileSize, fileData, companion } = msg;

    this.currentFileName = fileName;
    this.currentExtension = extension;
    this.currentFileSize = fileSize;

    document.getElementById('doc-filename')!.textContent = fileName;
    document.getElementById('doc-size-badge')!.textContent = `${(fileSize / 1024).toFixed(1)} KB`;
    document.getElementById('doc-format-badge')!.textContent = extension.toUpperCase().replace('.', '');

    this.showLoader(`PARSING ${extension.toUpperCase()}`, 'Loading CAD data stream...', 20);

    try {
      // 1. Check if a 3rd-party or proprietary parser is registered for this extension
      const customParser = this.pluginManager.getFormatParser(extension);
      if (customParser) {
        this.showLoader('PROPRIETARY ADAPTER', `Executing 3rd-party parser for ${extension}...`, 50);
        this.clearModel();
        const customObj = await customParser(fileData, fileName, (window as any).CADViewerSDK['api']);
        if (Array.isArray(customObj)) {
          customObj.forEach(o => this.rootGroup.add(o));
        } else if (customObj) {
          this.rootGroup.add(customObj);
        }
      } else if (['.step', '.stp', '.iges', '.igs', '.brep'].includes(extension.toLowerCase())) {
        await this.loadWithOpenCascade(fileData, extension.toLowerCase(), fileName);
      } else if (['.glb', '.gltf'].includes(extension.toLowerCase())) {
        await this.loadGLTF(fileData);
      } else if (['.stl'].includes(extension.toLowerCase())) {
        await this.loadSTL(fileData, fileName);
      } else if (['.obj'].includes(extension.toLowerCase())) {
        await this.loadOBJ(fileData, fileName);
      } else if (['.sldprt', '.sldasm'].includes(extension.toLowerCase())) {
        if (companion) {
          this.showCompanionBanner(
            `SolidWorks Document: Bound to companion geometry "${companion.fileName}"`
          );
          if (['.step', '.stp'].includes(companion.extension.toLowerCase())) {
            await this.loadWithOpenCascade(companion.fileData, companion.extension.toLowerCase(), companion.fileName);
          } else if (['.glb', '.gltf'].includes(companion.extension.toLowerCase())) {
            await this.loadGLTF(companion.fileData);
          }
        } else {
          this.handleUnpairedSolidWorks(fileName, extension);
        }
      } else {
        throw new Error(`Unsupported CAD format: ${extension}`);
      }

      this.onModelLoaded();
      this.hideLoader();
    } catch (err: any) {
      console.error('Failed to parse CAD model:', err);
      this.showLoader('LOAD ERROR', err?.message || 'Error parsing CAD geometry', 100);
      vscode.postMessage({ type: 'showError', text: `CAD Parse Error: ${err?.message || err}` });
    }
  }

  // --- OpenCASCADE WebAssembly Loader (STEP / IGES) ---
  private async loadWithOpenCascade(buffer: ArrayBuffer, ext: string, fileName: string) {
    this.showLoader('OPENCASCADE KERNEL', 'Initializing WebAssembly B-Rep solver...', 40);

    const occt = await occtimportjs({
      locateFile: () => this.wasmUri
    });

    this.showLoader('OPENCASCADE KERNEL', 'Tessellating 3D solid geometry into surface meshes...', 70);

    const uint8Array = new Uint8Array(buffer);
    let result: any;

    if (ext === '.step' || ext === '.stp') {
      result = occt.ReadStepFile(uint8Array, null);
    } else if (ext === '.iges' || ext === '.igs') {
      result = occt.ReadIgesFile(uint8Array, null);
    } else {
      result = occt.ReadBrepFile(uint8Array, null);
    }

    if (!result || !result.success) {
      throw new Error(`OpenCASCADE failed to read ${ext} file.`);
    }

    this.clearModel();

    result.meshes.forEach((meshData: any, index: number) => {
      const geometry = new THREE.BufferGeometry();
      const posArray = new Float32Array(meshData.attributes.position.array);
      geometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));

      if (meshData.attributes.normal) {
        const normArray = new Float32Array(meshData.attributes.normal.array);
        geometry.setAttribute('normal', new THREE.BufferAttribute(normArray, 3));
      } else {
        geometry.computeVertexNormals();
      }

      if (meshData.index) {
        const indexArray = new Uint32Array(meshData.index.array);
        geometry.setIndex(new THREE.BufferAttribute(indexArray, 1));
      }

      const colorHex = CAD_PALETTE[index % CAD_PALETTE.length];
      const color = new THREE.Color(colorHex);

      const material = new THREE.MeshStandardMaterial({
        color,
        roughness: 0.35,
        metalness: 0.75,
        side: THREE.DoubleSide,
        clippingPlanes: this.activeClipPlanes,
        clipShadows: true
      });

      const mesh = new THREE.Mesh(geometry, material);
      const partName = meshData.name && meshData.name.trim().length > 0
        ? meshData.name.trim()
        : `${fileName.replace(/\.[^/.]+$/, "")}_Part_${index + 1}`;
      mesh.name = partName;

      // Sharp CAD Edge Outline
      const edgesGeo = new THREE.EdgesGeometry(geometry, 25);
      const edgesMat = new THREE.LineBasicMaterial({
        color: this.currentTheme === 'blueprint' ? 0x38bdf8 : 0x0f172a,
        linewidth: 1,
        clippingPlanes: this.activeClipPlanes
      });
      const edges = new THREE.LineSegments(edgesGeo, edgesMat);
      mesh.add(edges);

      this.rootGroup.add(mesh);

      const triangleCount = meshData.index
        ? meshData.index.array.length / 3
        : posArray.length / 9;

      this.meshEntries.push({
        id: `mesh_${index}`,
        name: partName,
        mesh,
        edges,
        color,
        visible: true,
        triangleCount: Math.round(triangleCount),
        vertexCount: posArray.length / 3,
        initialPosition: new THREE.Vector3(),
        explodeVector: new THREE.Vector3()
      });
    });
  }

  // --- Three.js GLTF/GLB Loader ---
  private async loadGLTF(buffer: ArrayBuffer) {
    const loader = new GLTFLoader();
    return new Promise<void>((resolve, reject) => {
      loader.parse(
        buffer,
        '',
        (gltf) => {
          this.clearModel();
          let idx = 0;
          gltf.scene.traverse((child) => {
            if ((child as THREE.Mesh).isMesh) {
              const mesh = child as THREE.Mesh;
              mesh.geometry.computeVertexNormals();
              const colorHex = CAD_PALETTE[idx % CAD_PALETTE.length];
              const color = new THREE.Color(colorHex);

              mesh.material = new THREE.MeshStandardMaterial({
                color,
                roughness: 0.35,
                metalness: 0.75,
                side: THREE.DoubleSide,
                clippingPlanes: this.activeClipPlanes
              });

              const edgesGeo = new THREE.EdgesGeometry(mesh.geometry, 25);
              const edgesMat = new THREE.LineBasicMaterial({
                color: this.currentTheme === 'blueprint' ? 0x38bdf8 : 0x0f172a,
                clippingPlanes: this.activeClipPlanes
              });
              const edges = new THREE.LineSegments(edgesGeo, edgesMat);
              mesh.add(edges);

              const partName = mesh.name || `Component_${idx + 1}`;
              const posAttr = mesh.geometry.attributes.position;
              const indexAttr = mesh.geometry.index;
              const triCount = indexAttr ? indexAttr.count / 3 : posAttr.count / 3;

              this.meshEntries.push({
                id: `mesh_${idx}`,
                name: partName,
                mesh,
                edges,
                color,
                visible: true,
                triangleCount: Math.round(triCount),
                vertexCount: posAttr.count,
                initialPosition: new THREE.Vector3(),
                explodeVector: new THREE.Vector3()
              });
              idx++;
            }
          });
          this.rootGroup.add(gltf.scene);
          resolve();
        },
        reject
      );
    });
  }

  // --- STL Loader ---
  private async loadSTL(buffer: ArrayBuffer, fileName: string) {
    const loader = new STLLoader();
    const geometry = loader.parse(buffer);
    geometry.computeVertexNormals();

    this.clearModel();
    const color = new THREE.Color(CAD_PALETTE[0]);
    const material = new THREE.MeshStandardMaterial({
      color,
      roughness: 0.35,
      metalness: 0.75,
      side: THREE.DoubleSide,
      clippingPlanes: this.activeClipPlanes
    });

    const mesh = new THREE.Mesh(geometry, material);
    mesh.name = fileName;

    const edgesGeo = new THREE.EdgesGeometry(geometry, 25);
    const edgesMat = new THREE.LineBasicMaterial({
      color: 0x0f172a,
      clippingPlanes: this.activeClipPlanes
    });
    const edges = new THREE.LineSegments(edgesGeo, edgesMat);
    mesh.add(edges);

    this.rootGroup.add(mesh);

    const pos = geometry.attributes.position;
    this.meshEntries.push({
      id: 'mesh_0',
      name: fileName,
      mesh,
      edges,
      color,
      visible: true,
      triangleCount: pos.count / 3,
      vertexCount: pos.count,
      initialPosition: new THREE.Vector3(),
      explodeVector: new THREE.Vector3()
    });
  }

  // --- OBJ Loader ---
  private async loadOBJ(buffer: ArrayBuffer, fileName: string) {
    const loader = new OBJLoader();
    const text = new TextDecoder().decode(buffer);
    const obj = loader.parse(text);

    this.clearModel();
    let idx = 0;
    obj.traverse((child) => {
      if ((child as THREE.Mesh).isMesh) {
        const mesh = child as THREE.Mesh;
        mesh.geometry.computeVertexNormals();
        const color = new THREE.Color(CAD_PALETTE[idx % CAD_PALETTE.length]);
        mesh.material = new THREE.MeshStandardMaterial({
          color,
          roughness: 0.35,
          metalness: 0.75,
          side: THREE.DoubleSide,
          clippingPlanes: this.activeClipPlanes
        });

        const edgesGeo = new THREE.EdgesGeometry(mesh.geometry, 25);
        const edges = new THREE.LineSegments(edgesGeo, new THREE.LineBasicMaterial({
          color: 0x0f172a,
          clippingPlanes: this.activeClipPlanes
        }));
        mesh.add(edges);

        this.meshEntries.push({
          id: `mesh_${idx}`,
          name: mesh.name || `${fileName}_${idx + 1}`,
          mesh,
          edges,
          color,
          visible: true,
          triangleCount: mesh.geometry.attributes.position.count / 3,
          vertexCount: mesh.geometry.attributes.position.count,
          initialPosition: new THREE.Vector3(),
          explodeVector: new THREE.Vector3()
        });
        idx++;
      }
    });

    this.rootGroup.add(obj);
  }

  private handleUnpairedSolidWorks(fileName: string, ext: string) {
    this.clearModel();
    const geometry = new THREE.CylinderGeometry(1500, 1500, 8000, 32);
    geometry.computeVertexNormals();
    const material = new THREE.MeshStandardMaterial({
      color: 0x38bdf8,
      roughness: 0.3,
      metalness: 0.8,
      transparent: true,
      opacity: 0.85
    });
    const mesh = new THREE.Mesh(geometry, material);
    mesh.name = `${fileName} [SW Native Envelope]`;
    this.rootGroup.add(mesh);

    this.meshEntries.push({
      id: 'mesh_sw',
      name: `${fileName} (Direct SW Envelope)`,
      mesh,
      color: new THREE.Color(0x38bdf8),
      visible: true,
      triangleCount: 128,
      vertexCount: 192,
      initialPosition: new THREE.Vector3(),
      explodeVector: new THREE.Vector3(0, 1, 0)
    });

    this.showCompanionBanner(
      `Viewing native ${ext.toUpperCase()} envelope. Export companion .step to view exact B-Rep solids.`
    );
  }

  private clearModel() {
    while (this.rootGroup.children.length > 0) {
      const child = this.rootGroup.children[0] as THREE.Mesh;
      if (child.geometry) child.geometry.dispose();
      this.rootGroup.remove(child);
    }
    this.meshEntries = [];
  }

  // --- Post-Load Calibration ---
  private onModelLoaded() {
    this.modelBoundingBox.setFromObject(this.rootGroup);
    this.modelBoundingBox.getCenter(this.modelCenter);
    this.modelBoundingBox.getSize(this.modelSize);

    this.rootGroup.position.sub(this.modelCenter);

    this.modelBoundingBox.setFromObject(this.rootGroup);
    this.modelBoundingBox.getSize(this.modelSize);

    const overallCenter = new THREE.Vector3(0, 0, 0);
    this.meshEntries.forEach((entry, idx) => {
      entry.initialPosition.copy(entry.mesh.position);
      const partBox = new THREE.Box3().setFromObject(entry.mesh);
      const partCenter = new THREE.Vector3();
      partBox.getCenter(partCenter);

      const vec = new THREE.Vector3().subVectors(partCenter, overallCenter);
      if (vec.length() < 1) {
        const angle = (idx / Math.max(this.meshEntries.length, 1)) * Math.PI * 2;
        vec.set(Math.cos(angle), (idx % 2 === 0 ? 0.5 : -0.5), Math.sin(angle));
      }
      vec.normalize();
      entry.explodeVector.copy(vec);
    });

    this.gridHelper.position.y = this.modelBoundingBox.min.y - 10;
    const maxDim = Math.max(this.modelSize.x, this.modelSize.y, this.modelSize.z);
    this.gridHelper.scale.set(maxDim / 1000, 1, maxDim / 1000);

    this.fitCameraToModel();
    this.setupSectionSliders();
    this.populateComponentTree();
    this.populateEngineeringSpecs();

    // Notify 3rd-party plugins that model is loaded
    if (this.pluginManager) {
      const ctx = this.getModelContext();
      if (ctx) this.pluginManager.notifyModelLoaded(ctx);
    }
  }

  private fitCameraToModel() {
    const maxDim = Math.max(this.modelSize.x, this.modelSize.y, this.modelSize.z);
    const fov = this.camera.fov * (Math.PI / 180);
    let cameraZ = Math.abs(maxDim / 2 / Math.tan(fov / 2)) * 1.8;
    cameraZ = Math.max(cameraZ, 100);

    this.camera.position.set(cameraZ, cameraZ * 0.8, cameraZ);
    this.camera.lookAt(0, 0, 0);
    this.controls.target.set(0, 0, 0);
    this.controls.maxDistance = cameraZ * 10;
    this.controls.minDistance = maxDim * 0.05;
    this.controls.update();
  }

  // --- Exploded Assembly View Engine ---
  private applyExplodedView(pct: number) {
    const maxDim = Math.max(this.modelSize.x, this.modelSize.y, this.modelSize.z);
    const scale = (pct / 100) * (maxDim * 0.8);

    this.meshEntries.forEach((entry) => {
      const offset = entry.explodeVector.clone().multiplyScalar(scale);
      entry.mesh.position.copy(entry.initialPosition).add(offset);
    });
  }

  // --- Dynamic Cross Section Slicing ---
  private setupSectionSliders() {
    const halfX = (this.modelSize.x / 2) * 1.2;
    const halfY = (this.modelSize.y / 2) * 1.2;
    const halfZ = (this.modelSize.z / 2) * 1.2;

    const sx = document.getElementById('slice-x-slider') as HTMLInputElement;
    const sy = document.getElementById('slice-y-slider') as HTMLInputElement;
    const sz = document.getElementById('slice-z-slider') as HTMLInputElement;

    sx.min = (-halfX).toString();
    sx.max = halfX.toString();
    sx.value = '0';

    sy.min = (-halfY).toString();
    sy.max = halfY.toString();
    sy.value = '0';

    sz.min = (-halfZ).toString();
    sz.max = halfZ.toString();
    sz.value = '0';
  }

  private updateClippingPlanes() {
    this.activeClipPlanes = [];
    const chkX = (document.getElementById('slice-x-enable') as HTMLInputElement).checked;
    const chkY = (document.getElementById('slice-y-enable') as HTMLInputElement).checked;
    const chkZ = (document.getElementById('slice-z-enable') as HTMLInputElement).checked;

    if (chkX) this.activeClipPlanes.push(this.clipPlanes.x);
    if (chkY) this.activeClipPlanes.push(this.clipPlanes.y);
    if (chkZ) this.activeClipPlanes.push(this.clipPlanes.z);

    this.meshEntries.forEach((entry) => {
      if (Array.isArray(entry.mesh.material)) {
        entry.mesh.material.forEach((mat) => {
          mat.clippingPlanes = this.activeClipPlanes;
          mat.needsUpdate = true;
        });
      } else {
        entry.mesh.material.clippingPlanes = this.activeClipPlanes;
        entry.mesh.material.needsUpdate = true;
      }
      if (entry.edges) {
        (entry.edges.material as THREE.LineBasicMaterial).clippingPlanes = this.activeClipPlanes;
        (entry.edges.material as THREE.LineBasicMaterial).needsUpdate = true;
      }
    });
  }

  // --- Canvas Click Dispatcher ---
  private setupCanvasClicks() {
    this.canvas.addEventListener('click', (event) => {
      const rect = this.canvas.getBoundingClientRect();
      this.mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
      this.mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

      this.raycaster.setFromCamera(this.mouse, this.camera);
      const visibleMeshes = this.meshEntries.filter((m) => m.visible).map((m) => m.mesh);
      const intersects = this.raycaster.intersectObjects(visibleMeshes, true);

      if (intersects.length > 0) {
        const hitPoint = intersects[0].point;

        if (this.markupActive) {
          this.createMarkupPin(hitPoint);
        } else if (this.measureActive) {
          this.handleMeasureClick(hitPoint);
        } else {
          // Notify 3rd-party plugins of selection
          this.pluginManager.notifySelectionChanged(intersects[0].object as THREE.Mesh);
        }
      }
    });
  }

  // --- Precision Metrology (Distance & Angle) ---
  private handleMeasureClick(pt: THREE.Vector3) {
    if (this.measureMode === 'distance') {
      if (this.measurePoints.length >= 2) this.clearMeasure();
      this.measurePoints.push(pt.clone());

      const markerGeo = new THREE.SphereGeometry(Math.max(this.modelSize.x * 0.01, 8), 16, 16);
      const markerMat = new THREE.MeshBasicMaterial({
        color: this.measurePoints.length === 1 ? 0xef4444 : 0x10b981
      });
      const marker = new THREE.Mesh(markerGeo, markerMat);
      marker.position.copy(pt);
      this.measureGroup.add(marker);

      if (this.measurePoints.length === 2) {
        const p1 = this.measurePoints[0];
        const p2 = this.measurePoints[1];
        const lineGeo = new THREE.BufferGeometry().setFromPoints([p1, p2]);
        const lineMat = new THREE.LineDashedMaterial({
          color: 0x38bdf8,
          dashSize: 20,
          gapSize: 10,
          linewidth: 2
        });
        const line = new THREE.Line(lineGeo, lineMat);
        line.computeLineDistances();
        this.measureGroup.add(line);

        const dist = p1.distanceTo(p2);
        const dx = Math.abs(p2.x - p1.x);
        const dy = Math.abs(p2.y - p1.y);
        const dz = Math.abs(p2.z - p1.z);

        document.getElementById('m-dist')!.textContent = `${dist.toFixed(3)} mm`;
        document.getElementById('m-dx')!.textContent = `${dx.toFixed(3)} mm`;
        document.getElementById('m-dy')!.textContent = `${dy.toFixed(3)} mm`;
        document.getElementById('m-dz')!.textContent = `${dz.toFixed(3)} mm`;
      }
    } else {
      if (this.measurePoints.length >= 3) this.clearMeasure();
      this.measurePoints.push(pt.clone());

      const colors = [0xef4444, 0xf59e0b, 0x10b981];
      const markerGeo = new THREE.SphereGeometry(Math.max(this.modelSize.x * 0.01, 8), 16, 16);
      const marker = new THREE.Mesh(markerGeo, new THREE.MeshBasicMaterial({ color: colors[this.measurePoints.length - 1] }));
      marker.position.copy(pt);
      this.measureGroup.add(marker);

      if (this.measurePoints.length === 3) {
        const [pA, pB, pC] = this.measurePoints;
        const vBA = new THREE.Vector3().subVectors(pA, pB).normalize();
        const vBC = new THREE.Vector3().subVectors(pC, pB).normalize();

        const lineGeo = new THREE.BufferGeometry().setFromPoints([pA, pB, pC]);
        const line = new THREE.Line(lineGeo, new THREE.LineBasicMaterial({ color: 0xf59e0b, linewidth: 2 }));
        this.measureGroup.add(line);

        const dot = THREE.MathUtils.clamp(vBA.dot(vBC), -1, 1);
        const angleDeg = THREE.MathUtils.radToDeg(Math.acos(dot));

        document.getElementById('m-angle')!.textContent = `${angleDeg.toFixed(2)}°`;
        document.getElementById('m-angle-pt')!.textContent = `(${pB.x.toFixed(1)}, ${pB.y.toFixed(1)}, ${pB.z.toFixed(1)})`;
      }
    }
  }

  private clearMeasure() {
    this.measurePoints = [];
    while (this.measureGroup.children.length > 0) {
      const c = this.measureGroup.children[0] as THREE.Mesh;
      if (c.geometry) c.geometry.dispose();
      this.measureGroup.remove(c);
    }
    document.getElementById('m-dist')!.textContent = '0.000 mm';
    document.getElementById('m-dx')!.textContent = '0.000 mm';
    document.getElementById('m-dy')!.textContent = '0.000 mm';
    document.getElementById('m-dz')!.textContent = '0.000 mm';
    document.getElementById('m-angle')!.textContent = '0.00°';
    document.getElementById('m-angle-pt')!.textContent = '--';
  }

  // --- 3D Engineering Annotations & Redlining ---
  private createMarkupPin(pt: THREE.Vector3) {
    const noteInput = document.getElementById('markup-text-input') as HTMLInputElement;
    const noteText = noteInput.value.trim() || `Inspection Point #${this.nextPinId}`;
    noteInput.value = '';

    const id = this.nextPinId++;

    const pinGroup = new THREE.Group();
    const sphereGeo = new THREE.SphereGeometry(Math.max(this.modelSize.x * 0.012, 10), 16, 16);
    const sphereMat = new THREE.MeshStandardMaterial({
      color: 0xf59e0b,
      metalness: 0.8,
      roughness: 0.2,
      emissive: 0x78350f
    });
    const sphere = new THREE.Mesh(sphereGeo, sphereMat);
    sphere.position.set(0, Math.max(this.modelSize.x * 0.02, 15), 0);

    const stemGeo = new THREE.CylinderGeometry(2, 0.5, Math.max(this.modelSize.x * 0.02, 15), 8);
    const stemMat = new THREE.MeshBasicMaterial({ color: 0xf59e0b });
    const stem = new THREE.Mesh(stemGeo, stemMat);
    stem.position.set(0, Math.max(this.modelSize.x * 0.01, 7.5), 0);

    pinGroup.add(sphere);
    pinGroup.add(stem);
    pinGroup.position.copy(pt);
    this.markupGroup.add(pinGroup);

    const pin: MarkupPin = {
      id,
      note: noteText,
      position: pt.clone(),
      markerMesh: sphere
    };
    this.markupPins.push(pin);

    this.renderMarkupList();
  }

  private renderMarkupList() {
    const list = document.getElementById('markup-pins-list')!;
    list.innerHTML = '';

    this.markupPins.forEach((pin) => {
      const item = document.createElement('div');
      item.className = 'pin-item';
      item.innerHTML = `
        <div>
          <span class="pin-badge">${pin.id}</span>
          <span>${pin.note}</span>
        </div>
        <button class="mini-btn text-btn">&rarr;</button>
      `;

      item.onclick = () => {
        this.controls.target.copy(pin.position);
        const offset = new THREE.Vector3(200, 200, 200);
        this.camera.position.copy(pin.position).add(offset);
        this.controls.update();
      };

      list.appendChild(item);
    });
  }

  private exportMarkupReport() {
    const report = {
      model: document.getElementById('doc-filename')!.textContent,
      timestamp: new Date().toISOString(),
      engineer: 'Sourish Senapati (Roll: 002310301035)',
      institution: 'Jadavpur University',
      pinCount: this.markupPins.length,
      markups: this.markupPins.map((p) => ({
        id: p.id,
        note: p.note,
        coordinates: {
          x: p.position.x,
          y: p.position.y,
          z: p.position.z
        }
      }))
    };

    vscode.postMessage({
      type: 'exportFile',
      format: 'json',
      filename: `cad_markup_review_${Date.now()}.json`,
      data: JSON.stringify(report, null, 2)
    });
  }

  // --- Themes ---
  public setTheme(theme: 'dark' | 'light' | 'blueprint') {
    this.currentTheme = theme;
    document.body.className = `cad-body theme-${theme}`;

    document.querySelectorAll('#btn-theme-dark, #btn-theme-light, #btn-theme-blueprint').forEach((b) => {
      b.classList.remove('active');
    });
    document.getElementById(`btn-theme-${theme}`)?.classList.add('active');

    if (theme === 'dark') {
      this.scene.background = new THREE.Color(0x0f172a);
      this.gridHelper.material = new THREE.LineBasicMaterial({ color: 0x334155 });
      this.updateEdgeColors(0x0f172a);
    } else if (theme === 'light') {
      this.scene.background = new THREE.Color(0xe2e8f0);
      this.gridHelper.material = new THREE.LineBasicMaterial({ color: 0x94a3b8 });
      this.updateEdgeColors(0x334155);
    } else if (theme === 'blueprint') {
      this.scene.background = new THREE.Color(0x031b30);
      this.gridHelper.material = new THREE.LineBasicMaterial({ color: 0x0284c7 });
      this.updateEdgeColors(0x38bdf8);
    }
  }

  private updateEdgeColors(colorHex: number) {
    this.meshEntries.forEach((m) => {
      if (m.edges) {
        (m.edges.material as THREE.LineBasicMaterial).color.setHex(colorHex);
      }
    });
  }

  // --- Shading Modes ---
  public setShadingMode(mode: 'shaded' | 'edges' | 'wire' | 'xray') {
    this.currentShadingMode = mode;

    document.querySelectorAll('.btn-group button').forEach((btn) => {
      if (btn.id.startsWith('btn-mode-')) btn.classList.remove('active');
    });
    document.getElementById(`btn-mode-${mode}`)?.classList.add('active');

    this.meshEntries.forEach((entry) => {
      const mat = entry.mesh.material as THREE.MeshStandardMaterial;

      if (mode === 'shaded') {
        mat.wireframe = false;
        mat.transparent = false;
        mat.opacity = 1.0;
        if (entry.edges) entry.edges.visible = false;
      } else if (mode === 'edges') {
        mat.wireframe = false;
        mat.transparent = false;
        mat.opacity = 1.0;
        if (entry.edges) entry.edges.visible = true;
      } else if (mode === 'wire') {
        mat.wireframe = true;
        mat.transparent = false;
        mat.opacity = 1.0;
        if (entry.edges) entry.edges.visible = false;
      } else if (mode === 'xray') {
        mat.wireframe = false;
        mat.transparent = true;
        mat.opacity = 0.35;
        mat.depthWrite = false;
        if (entry.edges) entry.edges.visible = true;
      }
      mat.needsUpdate = true;
    });
  }

  // --- Component Tree & Specs UI ---
  private populateComponentTree() {
    const treeContainer = document.getElementById('component-tree')!;
    treeContainer.innerHTML = '';
    document.getElementById('part-count-badge')!.textContent = this.meshEntries.length.toString();

    this.meshEntries.forEach((entry) => {
      const item = document.createElement('div');
      item.className = 'tree-item';
      item.id = `tree-item-${entry.id}`;

      const label = document.createElement('div');
      label.className = 'tree-label';

      const dot = document.createElement('span');
      dot.className = 'part-color-dot';
      dot.style.backgroundColor = `#${entry.color.getHexString()}`;

      const nameSpan = document.createElement('span');
      nameSpan.textContent = entry.name;
      nameSpan.title = `${entry.name} (${entry.triangleCount.toLocaleString()} \u25B3)`;

      label.appendChild(dot);
      label.appendChild(nameSpan);

      const actions = document.createElement('div');
      actions.className = 'tree-actions';

      const visBtn = document.createElement('button');
      visBtn.className = 'vis-btn';
      visBtn.innerHTML = '&#128065;';
      visBtn.title = 'Toggle Visibility';
      visBtn.onclick = (e) => {
        e.stopPropagation();
        entry.visible = !entry.visible;
        entry.mesh.visible = entry.visible;
        if (entry.edges) entry.edges.visible = entry.visible && this.currentShadingMode === 'edges';
        visBtn.classList.toggle('hidden-mesh', !entry.visible);
      };

      actions.appendChild(visBtn);
      item.appendChild(label);
      item.appendChild(actions);

      item.onclick = () => {
        document.querySelectorAll('.tree-item').forEach((el) => el.classList.remove('selected'));
        item.classList.add('selected');
        this.focusOnMesh(entry.mesh);
      };

      treeContainer.appendChild(item);
    });
  }

  private focusOnMesh(mesh: THREE.Mesh) {
    const box = new THREE.Box3().setFromObject(mesh);
    const center = new THREE.Vector3();
    const size = new THREE.Vector3();
    box.getCenter(center);
    box.getSize(size);

    const maxDim = Math.max(size.x, size.y, size.z);
    const targetZ = maxDim * 2.5;

    this.controls.target.copy(center);
    this.camera.position.set(center.x + targetZ, center.y + targetZ * 0.8, center.z + targetZ);
    this.controls.update();
  }

  private populateEngineeringSpecs() {
    document.getElementById('spec-dim-x')!.textContent = `${this.modelSize.x.toFixed(1)} mm`;
    document.getElementById('spec-dim-y')!.textContent = `${this.modelSize.y.toFixed(1)} mm`;
    document.getElementById('spec-dim-z')!.textContent = `${this.modelSize.z.toFixed(1)} mm`;
    const diag = Math.sqrt(
      this.modelSize.x ** 2 + this.modelSize.y ** 2 + this.modelSize.z ** 2
    );
    document.getElementById('spec-dim-diag')!.textContent = `${diag.toFixed(1)} mm`;

    document.getElementById('spec-meshes')!.textContent = this.meshEntries.length.toString();
    const totalTriangles = this.meshEntries.reduce((sum, m) => sum + m.triangleCount, 0);
    const totalVertices = this.meshEntries.reduce((sum, m) => sum + m.vertexCount, 0);
    document.getElementById('spec-triangles')!.textContent = totalTriangles.toLocaleString();
    document.getElementById('spec-vertices')!.textContent = totalVertices.toLocaleString();
    document.getElementById('spec-solids')!.textContent = this.meshEntries.length.toString();
  }

  // --- UI Event Wireup ---
  private setupUIListeners() {
    document.getElementById('btn-view-iso')!.onclick = () => {
      const d = Math.max(this.modelSize.x, this.modelSize.y, this.modelSize.z) * 1.5;
      this.camera.position.set(d, d, d);
      this.controls.target.set(0, 0, 0);
      this.controls.update();
    };
    document.getElementById('btn-view-front')!.onclick = () => {
      const d = Math.max(this.modelSize.x, this.modelSize.y, this.modelSize.z) * 2;
      this.camera.position.set(0, 0, d);
      this.controls.target.set(0, 0, 0);
      this.controls.update();
    };
    document.getElementById('btn-view-top')!.onclick = () => {
      const d = Math.max(this.modelSize.x, this.modelSize.y, this.modelSize.z) * 2;
      this.camera.position.set(0, d, 0);
      this.controls.target.set(0, 0, 0);
      this.controls.update();
    };
    document.getElementById('btn-view-right')!.onclick = () => {
      const d = Math.max(this.modelSize.x, this.modelSize.y, this.modelSize.z) * 2;
      this.camera.position.set(d, 0, 0);
      this.controls.target.set(0, 0, 0);
      this.controls.update();
    };
    document.getElementById('btn-view-fit')!.onclick = () => this.fitCameraToModel();

    document.getElementById('btn-mode-shaded')!.onclick = () => this.setShadingMode('shaded');
    document.getElementById('btn-mode-edges')!.onclick = () => this.setShadingMode('edges');
    document.getElementById('btn-mode-wire')!.onclick = () => this.setShadingMode('wire');
    document.getElementById('btn-mode-xray')!.onclick = () => this.setShadingMode('xray');

    document.getElementById('btn-theme-dark')!.onclick = () => this.setTheme('dark');
    document.getElementById('btn-theme-light')!.onclick = () => this.setTheme('light');
    document.getElementById('btn-theme-blueprint')!.onclick = () => this.setTheme('blueprint');

    const expPanel = document.getElementById('explode-panel')!;
    const btnToggleExp = document.getElementById('btn-toggle-explode')!;
    btnToggleExp.onclick = () => {
      expPanel.classList.toggle('hidden');
      btnToggleExp.classList.toggle('active', !expPanel.classList.contains('hidden'));
    };
    document.getElementById('btn-close-explode')!.onclick = () => {
      expPanel.classList.add('hidden');
      btnToggleExp.classList.remove('active');
    };
    const expSlider = document.getElementById('explode-slider') as HTMLInputElement;
    expSlider.oninput = () => {
      this.explodeFactor = parseFloat(expSlider.value);
      document.getElementById('explode-val')!.textContent = `${Math.round(this.explodeFactor)}%`;
      this.applyExplodedView(this.explodeFactor);
    };
    document.getElementById('btn-animate-explode')!.onclick = () => {
      this.isExplodeAnimating = !this.isExplodeAnimating;
    };
    document.getElementById('btn-reset-explode')!.onclick = () => {
      this.isExplodeAnimating = false;
      this.explodeFactor = 0;
      expSlider.value = '0';
      document.getElementById('explode-val')!.textContent = '0%';
      this.applyExplodedView(0);
    };

    const secPanel = document.getElementById('section-panel')!;
    const btnToggleSec = document.getElementById('btn-toggle-section')!;
    btnToggleSec.onclick = () => {
      secPanel.classList.toggle('hidden');
      btnToggleSec.classList.toggle('active', !secPanel.classList.contains('hidden'));
    };
    document.getElementById('btn-close-section')!.onclick = () => {
      secPanel.classList.add('hidden');
      btnToggleSec.classList.remove('active');
    };

    const bindSlice = (axis: 'x' | 'y' | 'z') => {
      const chk = document.getElementById(`slice-${axis}-enable`) as HTMLInputElement;
      const sld = document.getElementById(`slice-${axis}-slider`) as HTMLInputElement;
      const flp = document.getElementById(`slice-${axis}-flip`) as HTMLButtonElement;

      chk.onchange = () => {
        sld.disabled = !chk.checked;
        this.updateClippingPlanes();
      };
      sld.oninput = () => {
        this.clipPlanes[axis].constant = parseFloat(sld.value);
      };
      flp.onclick = () => {
        this.clipPlanes[axis].normal.negate();
        this.clipPlanes[axis].constant *= -1;
      };
    };
    bindSlice('x');
    bindSlice('y');
    bindSlice('z');

    const measPanel = document.getElementById('measurement-panel')!;
    const btnToggleMeas = document.getElementById('btn-toggle-measure')!;
    btnToggleMeas.onclick = () => {
      this.measureActive = !this.measureActive;
      this.markupActive = false;
      measPanel.classList.toggle('hidden', !this.measureActive);
      btnToggleMeas.classList.toggle('active', this.measureActive);
      document.getElementById('markup-panel')!.classList.add('hidden');
      document.getElementById('btn-toggle-markup')!.classList.remove('active');
      if (!this.measureActive) this.clearMeasure();
    };
    document.getElementById('btn-close-measure')!.onclick = () => {
      this.measureActive = false;
      measPanel.classList.add('hidden');
      btnToggleMeas.classList.remove('active');
      this.clearMeasure();
    };
    document.getElementById('btn-clear-measure')!.onclick = () => this.clearMeasure();

    document.querySelectorAll('input[name="measure-mode"]').forEach((el) => {
      el.addEventListener('change', (e) => {
        this.measureMode = (e.target as HTMLInputElement).value as any;
        this.clearMeasure();
        const isDist = this.measureMode === 'distance';
        document.getElementById('meas-dist-block')!.classList.toggle('hidden', !isDist);
        document.getElementById('meas-angle-block')!.classList.toggle('hidden', isDist);
        document.getElementById('measure-instructions')!.textContent = isDist
          ? 'Click two vertices/points on the 3D model to calculate 3D Euclidean distance.'
          : 'Click 3 points: A, B (vertex), and C to compute the enclosed 3D angle.';
      });
    });

    const markupPanel = document.getElementById('markup-panel')!;
    const btnToggleMarkup = document.getElementById('btn-toggle-markup')!;
    btnToggleMarkup.onclick = () => {
      this.markupActive = !this.markupActive;
      this.measureActive = false;
      markupPanel.classList.toggle('hidden', !this.markupActive);
      btnToggleMarkup.classList.toggle('active', this.markupActive);
      document.getElementById('measurement-panel')!.classList.add('hidden');
      document.getElementById('btn-toggle-measure')!.classList.remove('active');
    };
    document.getElementById('btn-close-markup')!.onclick = () => {
      this.markupActive = false;
      markupPanel.classList.add('hidden');
      btnToggleMarkup.classList.remove('active');
    };
    document.getElementById('btn-export-markups')!.onclick = () => this.exportMarkupReport();

    const exportModal = document.getElementById('export-panel')!;
    const btnToggleExpModal = document.getElementById('btn-export-menu')!;
    btnToggleExpModal.onclick = () => exportModal.classList.toggle('hidden');
    document.getElementById('btn-close-export')!.onclick = () => exportModal.classList.add('hidden');

    document.getElementById('btn-export-glb')!.onclick = () => this.exportGLB();
    document.getElementById('btn-export-stl')!.onclick = () => this.exportSTL();
    document.getElementById('btn-export-obj')!.onclick = () => this.exportOBJ();
    document.getElementById('btn-export-png')!.onclick = () => this.exportPNG();

    document.getElementById('btn-show-all')!.onclick = () => {
      this.meshEntries.forEach((m) => {
        m.visible = true;
        m.mesh.visible = true;
        if (m.edges) m.edges.visible = this.currentShadingMode === 'edges';
      });
      document.querySelectorAll('.vis-btn').forEach((btn) => btn.classList.remove('hidden-mesh'));
    };
    document.getElementById('btn-isolate-clear')!.onclick = () => {
      document.getElementById('btn-show-all')!.click();
      document.querySelectorAll('.tree-item').forEach((i) => i.classList.remove('selected'));
    };

    const leftSidebar = document.getElementById('sidebar-left')!;
    const btnToggleTree = document.getElementById('btn-toggle-tree')!;
    btnToggleTree.onclick = () => {
      leftSidebar.classList.toggle('hidden');
      btnToggleTree.classList.toggle('active', !leftSidebar.classList.contains('hidden'));
    };

    const expInput = document.getElementById('render-exposure') as HTMLInputElement;
    expInput.oninput = () => {
      this.renderer.toneMappingExposure = parseFloat(expInput.value);
    };

    const roughInput = document.getElementById('render-roughness') as HTMLInputElement;
    roughInput.oninput = () => {
      const val = parseFloat(roughInput.value);
      this.meshEntries.forEach((m) => {
        (m.mesh.material as THREE.MeshStandardMaterial).roughness = val;
      });
    };

    const metalInput = document.getElementById('render-metalness') as HTMLInputElement;
    metalInput.oninput = () => {
      const val = parseFloat(metalInput.value);
      this.meshEntries.forEach((m) => {
        (m.mesh.material as THREE.MeshStandardMaterial).metalness = val;
      });
    };

    window.addEventListener('keydown', (e) => {
      if (e.key === 'h' || e.key === 'H') this.fitCameraToModel();
      if (e.key === 'm' || e.key === 'M') btnToggleMeas.click();
      if (e.key === 'e' || e.key === 'E') btnToggleExp.click();
    });

    document.getElementById('companion-dismiss')!.onclick = () => {
      document.getElementById('companion-banner')!.classList.add('hidden');
    };
  }

  private exportGLB() {
    const exporter = new GLTFExporter();
    exporter.parse(
      this.rootGroup,
      (gltf) => {
        vscode.postMessage({
          type: 'exportFile',
          format: 'glb',
          filename: 'model_export.glb',
          data: gltf
        });
      },
      (error) => {
        console.error('Export GLB error:', error);
      },
      { binary: true }
    );
  }

  private exportSTL() {
    const exporter = new STLExporter();
    const result = exporter.parse(this.rootGroup, { binary: true });
    vscode.postMessage({
      type: 'exportFile',
      format: 'stl',
      filename: 'model_export.stl',
      data: (result as DataView).buffer
    });
  }

  private exportOBJ() {
    const exporter = new OBJExporter();
    const result = exporter.parse(this.rootGroup);
    const encoder = new TextEncoder();
    vscode.postMessage({
      type: 'exportFile',
      format: 'obj',
      filename: 'model_export.obj',
      data: encoder.encode(result).buffer
    });
  }

  private exportPNG() {
    this.renderer.render(this.scene, this.camera);
    const dataUrl = this.canvas.toDataURL('image/png');
    const a = document.createElement('a');
    a.href = dataUrl;
    a.download = `cad_snapshot_${Date.now()}.png`;
    a.click();
  }

  private showLoader(title: string, sub: string, pct: number) {
    const overlay = document.getElementById('loading-overlay')!;
    overlay.classList.remove('hidden');
    document.getElementById('loader-status')!.textContent = title;
    document.getElementById('loader-substatus')!.textContent = sub;
    document.getElementById('loader-progress')!.style.width = `${pct}%`;
  }

  private hideLoader() {
    document.getElementById('loading-overlay')!.classList.add('hidden');
  }

  private showCompanionBanner(text: string) {
    const banner = document.getElementById('companion-banner')!;
    document.getElementById('companion-text')!.textContent = text;
    banner.classList.remove('hidden');
  }
}

// Initialize Application when DOM is ready
window.addEventListener('DOMContentLoaded', () => {
  const app = new CADNativeViewerApp();

  window.addEventListener('message', (event) => {
    const msg = event.data;
    if (msg.type === 'loadCAD') {
      app.loadCAD(msg);
    }
  });
});
