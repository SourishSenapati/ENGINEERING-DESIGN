import * as THREE from 'three';
import { CADViewerPlugin, CADViewerAPI, CADModelContext } from './plugin-system';

export function createFEAStressPlugin(): CADViewerPlugin {
  let isFEAActive = false;
  let currentYieldLimit = 250; // MPa
  let currentModel: CADModelContext | null = null;
  let originalMaterials: Map<string, THREE.Material | THREE.Material[]> = new Map();

  // Rainbow / Jet colormap helper: val in [0, 1]
  const getJetColor = (t: number) => {
    const clampT = Math.max(0, Math.min(1, t));
    const r = Math.max(0, Math.min(1, 1.5 - Math.abs(clampT * 4 - 3)));
    const g = Math.max(0, Math.min(1, 1.5 - Math.abs(clampT * 4 - 2)));
    const b = Math.max(0, Math.min(1, 1.5 - Math.abs(clampT * 4 - 1)));
    return { r, g, b };
  };

  return {
    id: 'fea-stress-contour-visualizer',
    name: 'FEA Von Mises Stress & Thermal Visualizer',
    version: '1.2.0',
    author: 'Sourish Senapati (Jadavpur University)',
    description: '3rd-party finite element stress contour and thermal gradient inspection tool.',

    init(api: CADViewerAPI) {
      // 1. Add Toolbar Button
      api.addToolbarButton({
        id: 'btn-fea-stress',
        label: 'FEA STRESS',
        iconHtml: '&#9874;',
        tooltip: 'Finite Element Von Mises Stress Contour Analyzer',
        onClick: () => {
          api.togglePanel('fea-stress-panel');
        }
      });

      // 2. Add Floating Panel
      api.addFloatingPanel({
        id: 'fea-stress-panel',
        title: 'FEA VON MISES STRESS CONTOUR (3RD PARTY TOOL)',
        onRender: (container: HTMLElement) => {
          container.innerHTML = `
            <div style="font-size: 11px; color: var(--text-muted); margin-bottom: 8px;">
              Third-Party Extension Plugin built via <code>CADViewerSDK</code>. Visualizes simulated ASME Sec VIII Div 1 mechanical stress tensors.
            </div>
            
            <div class="slider-control" style="margin-bottom: 10px;">
              <div class="flex-between">
                <span>Allowable Yield Limit (&sigma;<sub>y</sub>):</span>
                <strong id="fea-yield-val">${currentYieldLimit} MPa</strong>
              </div>
              <input type="range" id="fea-yield-slider" min="100" max="450" value="${currentYieldLimit}" style="width: 100%;">
            </div>

            <div class="flex-between" style="font-family: var(--font-mono); font-size: 10px; margin-bottom: 8px;">
              <span style="color: #38bdf8;">0 MPa (Safe)</span>
              <span style="color: #10b981;">150 MPa</span>
              <span style="color: #f59e0b;">250 MPa</span>
              <span style="color: #ef4444;">&gt;350 MPa (Yield)</span>
            </div>

            <!-- Colormap Bar -->
            <div style="width: 100%; height: 8px; border-radius: 4px; background: linear-gradient(90deg, #38bdf8, #10b981, #f59e0b, #ef4444); margin-bottom: 12px; border: 1px solid var(--border-color);"></div>

            <div class="flex-row gap-2">
              <button id="btn-apply-fea" class="btn full-btn primary">Compute & Map Stress</button>
              <button id="btn-reset-fea" class="btn full-btn">Restore Nominal CAD</button>
            </div>
          `;

          const slider = container.querySelector('#fea-yield-slider') as HTMLInputElement;
          const yieldVal = container.querySelector('#fea-yield-val') as HTMLElement;
          slider.oninput = () => {
            currentYieldLimit = parseFloat(slider.value);
            yieldVal.textContent = `${currentYieldLimit} MPa`;
            if (isFEAActive) applyFEAContour(api);
          };

          const applyBtn = container.querySelector('#btn-apply-fea') as HTMLButtonElement;
          applyBtn.onclick = () => {
            isFEAActive = true;
            applyFEAContour(api);
          };

          const resetBtn = container.querySelector('#btn-reset-fea') as HTMLButtonElement;
          resetBtn.onclick = () => {
            isFEAActive = false;
            restoreMaterials();
          };
        }
      });
    },

    onModelLoaded(model: CADModelContext) {
      currentModel = model;
      originalMaterials.clear();
      model.meshes.forEach((m) => {
        originalMaterials.set(m.id, m.mesh.material);
      });
    }
  };

  function applyFEAContour(api: CADViewerAPI) {
    if (!currentModel) return;

    currentModel.meshes.forEach((mEntry) => {
      const mesh = mEntry.mesh;
      const geometry = mesh.geometry;
      const posAttr = geometry.attributes.position;
      if (!posAttr) return;

      const vertexCount = posAttr.count;
      const colors = new Float32Array(vertexCount * 3);

      // Simulate radial and elevation pressure vessel stress: sigma = P*R/t + axial bending
      for (let i = 0; i < vertexCount; i++) {
        const y = posAttr.getY(i);
        const x = posAttr.getX(i);
        const z = posAttr.getZ(i);

        const r = Math.sqrt(x * x + z * z);
        const heightNorm = (y + 4000) / 8000;

        // Simulated stress field: highest near nozzles and tubesheet junction
        let stress = 120 + 80 * Math.sin(heightNorm * Math.PI * 3) + (r > 1200 ? 90 : 20);
        stress = Math.max(10, Math.min(420, stress));

        const normStress = stress / currentYieldLimit;
        const { r: cr, g: cg, b: cb } = getJetColor(normStress);

        colors[i * 3] = cr;
        colors[i * 3 + 1] = cg;
        colors[i * 3 + 2] = cb;
      }

      geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

      // Use a vertex-colored material
      const feaMat = new THREE.MeshStandardMaterial({
        vertexColors: true,
        roughness: 0.4,
        metalness: 0.5,
        side: THREE.DoubleSide
      });
      mesh.material = feaMat;
    });
  }

  function restoreMaterials() {
    if (!currentModel) return;
    currentModel.meshes.forEach((mEntry) => {
      const orig = originalMaterials.get(mEntry.id);
      if (orig) {
        mEntry.mesh.material = orig;
      }
      if (mEntry.mesh.geometry.attributes.color) {
        mEntry.mesh.geometry.deleteAttribute('color');
      }
    });
  }
}
