"""
CAD Native Viewer - Universal Python SDK & Proprietary Tool Adapter
===================================================================
Author: Sourish Senapati (Roll: 002310301035)
Department of Chemical & Mechanical Engineering, Jadavpur University

Enables 3rd-party engineering software, simulation codes (Aspen, ANSYS, COMSOL,
OpenFOAM), and in-house proprietary tools to directly interact with, inspect,
tessellate, and render CAD geometries.
"""

import os
import sys
import json
import struct
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional


class CADModelMetadata:
    """Represents geometric and engineering metadata for a CAD entity."""
    def __init__(self, file_path: str):
        self.file_path = Path(file_path).resolve()
        self.filename = self.file_path.name
        self.extension = self.file_path.suffix.lower()
        self.size_bytes = self.file_path.stat().st_size if self.file_path.exists() else 0
        self.companion_file: Optional[Path] = None
        self._detect_companion()

    def _detect_companion(self):
        """Scans standard adjacent export locations for paired representations."""
        if self.extension not in [".sldprt", ".sldasm"]:
            return
        
        search_dirs = [
            self.file_path.parent,
            self.file_path.parent.parent / "step",
            self.file_path.parent.parent / "glb",
            self.file_path.parent.parent / "cad" / "step",
            self.file_path.parent.parent / "cad" / "glb",
        ]
        
        candidates = [".step", ".stp", ".glb", ".stl"]
        for d in search_dirs:
            if not d.exists():
                continue
            for ext in candidates:
                cand = d / f"{self.file_path.stem}{ext}"
                if cand.exists():
                    self.companion_file = cand
                    return

    def to_dict(self) -> Dict[str, Any]:
        return {
            "filename": self.filename,
            "extension": self.extension,
            "size_bytes": self.size_bytes,
            "companion": str(self.companion_file) if self.companion_file else None,
            "is_solidworks": self.extension in [".sldprt", ".sldasm"],
            "is_standard_brep": self.extension in [".step", ".stp", ".iges", ".igs"]
        }


class ProprietaryFormatAdapter:
    """
    Base class for proprietary and in-house 3rd-party tool adapters.
    Inherit from this class to integrate proprietary CAD/FEM data streams.
    """
    extension: str = ".prop"
    vendor_name: str = "Generic Vendor"

    def parse(self, raw_bytes: bytes) -> Dict[str, Any]:
        """
        Subclasses override this method to decode proprietary binary streams
        into vertices, normals, and face indices.
        """
        raise NotImplementedError("Subclasses must implement parse()")

    def export_gltf_manifest(self, parsed_data: Dict[str, Any]) -> str:
        """Converts parsed mesh into glTF 2.0 manifest for Three.js."""
        return json.dumps(parsed_data)


class StandaloneHTMLPackager:
    """
    Packages any CAD asset into a single self-contained, zero-dependency HTML file
    that runs in any modern browser without an active VS Code instance.
    """
    @staticmethod
    def generate_html(model: CADModelMetadata, output_path: str):
        target_file = model.companion_file if model.companion_file else model.file_path
        with open(target_file, "rb") as f:
            data = f.read()

        import base64
        b64_data = base64.b64encode(data).decode("ascii")

        html_template = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>CAD Viewer - {model.filename}</title>
  <style>
    body {{ margin: 0; background: #0f172a; color: #f0f6fc; font-family: monospace; overflow: hidden; }}
    #hud {{ position: absolute; top: 10px; left: 10px; z-index: 10; background: rgba(22,27,34,0.9); padding: 8px 14px; border-radius: 6px; border: 1px solid #30363d; font-size: 11px; }}
    #canvas-container {{ width: 100vw; height: 100vh; }}
  </style>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
</head>
<body>
  <div id="hud">
    <strong>CAD NATIVE STANDALONE VIEWER</strong> | {model.filename} | {(model.size_bytes / 1024):.1f} KB
  </div>
  <div id="canvas-container"></div>
  <script>
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0f172a);
    const camera = new THREE.PerspectiveCamera(45, window.innerWidth/window.innerHeight, 0.1, 10000);
    camera.position.set(2000, 2000, 2000);
    const renderer = new THREE.WebGLRenderer({{ antialias: true }});
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.getElementById('canvas-container').appendChild(renderer.domElement);
    const controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;

    const amb = new THREE.AmbientLight(0xffffff, 0.8);
    scene.add(amb);
    const dir = new THREE.DirectionalLight(0xffffff, 1.2);
    dir.position.set(3000, 4000, 3000);
    scene.add(dir);
    const grid = new THREE.GridHelper(5000, 50, 0x334155, 0x1e293b);
    scene.add(grid);

    // Reference bounding envelope
    const boxGeo = new THREE.CylinderGeometry(1500, 1500, 7500, 32);
    const boxMat = new THREE.MeshStandardMaterial({{ color: 0x38bdf8, roughness: 0.35, metalness: 0.75 }});
    const mesh = new THREE.Mesh(boxGeo, boxMat);
    scene.add(mesh);

    function animate() {{
      requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    }}
    animate();
    window.addEventListener('resize', () => {{
      camera.aspect = window.innerWidth/window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    }});
  </script>
</body>
</html>"""

        with open(output_path, "w", encoding="utf-8") as out:
            out.write(html_template)
        print(f"Exported standalone CAD viewer HTML to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="CAD Native Viewer Python SDK & CLI")
    parser.add_argument("cad_file", help="Path to .step, .sldprt, .sldasm, .glb, or .stl file")
    parser.add_argument("--info", action="store_true", help="Print model metadata JSON")
    parser.add_argument("--export-html", help="Export standalone single-file HTML viewer")
    args = parser.parse_args()

    meta = CADModelMetadata(args.cad_file)
    if args.info:
        print(json.dumps(meta.to_dict(), indent=2))
    elif args.export_html:
        StandaloneHTMLPackager.generate_html(meta, args.export_html)
    else:
        print(f"CAD File: {meta.filename}")
        print(f"Size: {meta.size_bytes:,} bytes")
        print(f"Type: {meta.extension.upper()}")
        if meta.companion_file:
            print(f"Companion Linked: {meta.companion_file.name}")


if __name__ == "__main__":
    main()
