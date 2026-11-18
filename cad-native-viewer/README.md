# CAD Native 3D Viewer

A universal 3D CAD viewer extension for VS Code, Cursor, Windsurf, VSCodium, and WSL environments.

## Supported Formats
- Standard CAD: `.step`, `.stp`, `.iges`, `.igs`, `.brep` (powered by offline OpenCASCADE WebAssembly)
- SolidWorks files: `.sldprt`, `.sldasm` (automated companion resolution and native envelope parsing)
- Polygonal / PBR: `.glb`, `.gltf`, `.stl`, `.obj`

## Key Capabilities
- Interactive 3D Orbit, Pan, Zoom, and Fit-to-Screen controls.
- Dynamic 3-Axis Cross-Section Slicing (X, Y, Z cutaways with interactive sliders).
- Precision Measurement Caliper for 3D Euclidean distances and coordinate deltas.
- Shading presets: Realistic PBR, Sharp CAD Edge Outlines, Technical Wireframe, and Ghosted X-Ray.
- Multi-body Component Tree with individual part visibility toggles and focus.
- One-click export to GLB, STL, OBJ, and high-resolution PNG snapshots.

## Installation

### Method 1: Local VSIX Installation
In PowerShell, Bash, or terminal:
```bash
code --install-extension cad-native-viewer-1.0.0.vsix
```
Or for Cursor / VS Code Insiders / WSL:
```bash
cursor --install-extension cad-native-viewer-1.0.0.vsix
code-insiders --install-extension cad-native-viewer-1.0.0.vsix
```

### Method 2: GitHub Clone & Local Build
```bash
git clone https://github.com/sourish-senapati/cad-native-viewer.git
cd cad-native-viewer
npm install
npm run build
npm run package
```

## Attribution
- Lead Designer & Engineer: Sourish Senapati (Roll: 002310301035)
- Department: Chemical & Mechanical Engineering, Jadavpur University
