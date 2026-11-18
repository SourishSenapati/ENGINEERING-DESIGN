# 🛠️ 3rd-Party & Proprietary Tool Developer SDK Guide

> *"There are only two kinds of languages: the ones people complain about and the ones nobody uses."* — Bjarne Stroustrup

The **CAD Native 3D Viewer** platform is architected specifically so that **third-party commercial vendors, in-house engineering teams, and academic researchers** can easily build custom tools, proprietary format decoders, and post-processing visualizers on top of the native 3D engine.

Whether you write in **TypeScript/JavaScript, Python, C++, or Rust (WebAssembly)**, the platform provides direct, unopinionated hooks.

---

## 🏛️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                   CAD NATIVE 3D PLATFORM                    │
├───────────────────────────────┬─────────────────────────────┤
│   CORE KERNELS & LOADERS      │   EXTENSIBILITY LAYER       │
│ • OpenCASCADE WebAssembly     │ • window.CADViewerSDK       │
│ • Three.js WebGL Engine       │ • Plugin Lifecycle Hooks    │
│ • Parasolid / SW Resolvers    │ • Custom Format Parsers     │
│ • glTF / STL / OBJ Loaders    │ • Dynamic Toolbars & Panels │
└───────────────▲───────────────┴──────────────▲──────────────┘
                │                              │
┌───────────────┴───────────────┐ ┌────────────┴──────────────┐
│   PROPRIETARY CAD FORMATS     │ │   3RD-PARTY TOOL PLUGINS  │
│ (Custom Binary Adapters,      │ │ (FEA Stress, CFD Vectors, │
│ In-House Enterprise Streams)  │ │ Tolerance Stack-Up, Cost) │
└───────────────────────────────┘ └───────────────────────────┘
```

---

## 1. Building a 3rd-Party Webview Plugin

Any script or extension can register a plugin via the global `window.CADViewerSDK`:

```javascript
// Register a custom 3rd-party engineering plugin
window.CADViewerSDK.registerPlugin({
  id: "company-tolerance-inspector",
  name: "Tolerance & GD&T Stack-Up Inspector",
  version: "1.0.0",
  author: "Acme Engineering Corp",

  init(api) {
    // 1. Add a custom button to the top command ribbon
    api.addToolbarButton({
      id: "btn-tolerance-check",
      label: "GD&T CHECK",
      iconHtml: "&#9881;",
      tooltip: "Run ASME Y14.5 Geometric Dimensioning Audit",
      onClick: () => {
        api.togglePanel("tolerance-panel");
      }
    });

    // 2. Add an interactive floating tool panel
    api.addFloatingPanel({
      id: "tolerance-panel",
      title: "ASME Y14.5 TOLERANCE AUDIT",
      onRender: (container, api) => {
        container.innerHTML = `
          <div style="font-size: 11px; margin-bottom: 8px;">
            Auditing component fit tolerances and clearance fits.
          </div>
          <button id="btn-run-audit" class="btn full-btn primary">Execute Fit Audit</button>
        `;
        container.querySelector("#btn-run-audit").onclick = () => {
          alert("Tolerance stack-up verified within +/- 0.05 mm!");
        };
      }
    });
  },

  // Called whenever a new model is loaded
  onModelLoaded(modelContext, api) {
    console.log("Model loaded for audit:", modelContext.fileName);
    console.log("Total parts:", modelContext.meshes.length);
  },

  // Called whenever an engineer clicks a part in the 3D viewport
  onSelectionChanged(selectedMesh, api) {
    if (selectedMesh) {
      console.log("Inspecting part:", selectedMesh.name);
    }
  }
});
```

---

## 2. Registering Proprietary & Custom File Formats

If your company or lab has a proprietary file format (e.g., `.mycad`, `.fem`, `.cfdmesh`, `.bin3d`), register a custom parser directly with the engine:

```javascript
window.CADViewerSDK.registerFormatParser(".mycad", async (buffer, fileName, api) => {
  // 1. Decode your proprietary binary data
  const dataView = new DataView(buffer);
  const vertexCount = dataView.getUint32(0, true);

  // 2. Build Three.js geometry from your proprietary stream
  const geometry = new THREE.BufferGeometry();
  // ... populate positions, normals, and indices ...

  // 3. Return mesh(es) for native rendering
  const material = new THREE.MeshStandardMaterial({ color: 0x38bdf8, metalness: 0.8 });
  const mesh = new THREE.Mesh(geometry, material);
  mesh.name = fileName;
  return mesh;
});
```

---

## 3. Vertex Color & Heatmap API (FEA / CFD / Thermal)

To display finite element stress contours (von Mises), CFD velocity vectors, or thermal gradients:

```javascript
// Apply a custom Float32Array RGB colormap to any mesh
// colors: [r0, g0, b0, r1, g1, b1, ..., rn, gn, bn] (values 0.0 to 1.0)
api.applyVertexColors("mesh_0", colorsRGBArray);

// Restore original nominal CAD PBR material
api.resetMeshColors();
```

*A production example of this is built directly into the viewer: see `src/webview/fea-stress-plugin.ts`.*

---

## 4. Python SDK & CLI (`cad_viewer_sdk.py`)

For engineers writing automation scripts, numerical solvers (SciPy, NumPy), or pipeline exporters:

```bash
# Navigate to the Python SDK directory
cd cad-native-viewer/sdk/python

# 1. Print structured model metadata (size, format, companion links)
python cad_viewer_sdk.py "path/to/model.step" --info

# 2. Package into a single zero-dependency HTML file runnable on any device
python cad_viewer_sdk.py "path/to/model.step" --export-html "reactor_report.html"
```

In your own Python scripts:
```python
from cad_viewer_sdk import CADModelMetadata, StandaloneHTMLPackager

# Inspect CAD file and resolve companion assets
meta = CADModelMetadata("R201_Vessel_Pressure_Shell.SLDPRT")
print(meta.to_dict())

# Export standalone 3D report
StandaloneHTMLPackager.generate_html(meta, "pressure_shell_3d.html")
```

---

## 5. Summary of Supported Integrations

| Language / Tool | Integration Path | Use Case |
| :--- | :--- | :--- |
| **TypeScript / JavaScript** | `window.CADViewerSDK` | Interactive UI panels, toolbars, custom WebGL shaders |
| **Python** | `cad_viewer_sdk.py` | Automated CLI batch conversion, Jupyter notebooks, Aspen/CFD pipelines |
| **C / C++ / Rust** | WebAssembly compilation | High-speed B-Rep geometry tessellation, custom physics kernels |
| **Proprietary Binary** | `registerFormatParser()` | In-house enterprise CAD formats, legacy binary models |
