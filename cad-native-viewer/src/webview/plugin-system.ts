import * as THREE from 'three';

export interface CADModelContext {
  fileName: string;
  extension: string;
  fileSize: number;
  meshes: Array<{
    id: string;
    name: string;
    mesh: THREE.Mesh;
    color: THREE.Color;
    triangleCount: number;
    vertexCount: number;
  }>;
  boundingBox: THREE.Box3;
  size: THREE.Vector3;
  center: THREE.Vector3;
}

export interface CADViewerAPI {
  scene: THREE.Scene;
  camera: THREE.PerspectiveCamera;
  renderer: THREE.WebGLRenderer;
  rootGroup: THREE.Group;
  getModelContext: () => CADModelContext | null;
  focusOnMesh: (mesh: THREE.Mesh) => void;
  fitCamera: () => void;
  addMeshToScene: (mesh: THREE.Object3D) => void;
  removeMeshFromScene: (mesh: THREE.Object3D) => void;
  setMeshColor: (meshId: string, colorHex: number) => void;
  applyVertexColors: (meshId: string, colorsRGB: Float32Array) => void;
  resetMeshColors: () => void;
  addToolbarButton: (btn: {
    id: string;
    label: string;
    iconHtml?: string;
    tooltip?: string;
    onClick: (api: CADViewerAPI) => void;
  }) => void;
  addFloatingPanel: (panel: {
    id: string;
    title: string;
    onRender: (container: HTMLElement, api: CADViewerAPI) => void;
  }) => void;
  togglePanel: (panelId: string, force?: boolean) => void;
  postMessageToHost: (type: string, payload?: any) => void;
}

export interface CADViewerPlugin {
  id: string;
  name: string;
  version?: string;
  author?: string;
  description?: string;
  init?: (api: CADViewerAPI) => void;
  onModelLoaded?: (model: CADModelContext, api: CADViewerAPI) => void;
  onSelectionChanged?: (mesh: THREE.Mesh | null, api: CADViewerAPI) => void;
  onFrame?: (deltaTime: number, api: CADViewerAPI) => void;
}

export type CustomFormatParser = (
  buffer: ArrayBuffer,
  fileName: string,
  api: CADViewerAPI
) => Promise<THREE.Object3D | THREE.Object3D[]>;

export class CADPluginManager {
  private plugins: Map<string, CADViewerPlugin> = new Map();
  private formatParsers: Map<string, CustomFormatParser> = new Map();
  private api: CADViewerAPI;

  constructor(api: CADViewerAPI) {
    this.api = api;
  }

  public registerPlugin(plugin: CADViewerPlugin) {
    if (this.plugins.has(plugin.id)) {
      console.warn(`[CADPluginManager] Overwriting plugin with id ${plugin.id}`);
    }
    this.plugins.set(plugin.id, plugin);
    console.log(`[CADPluginManager] Registered plugin "${plugin.name}" (${plugin.id} v${plugin.version || '1.0.0'})`);

    try {
      if (plugin.init) {
        plugin.init(this.api);
      }
    } catch (err) {
      console.error(`[CADPluginManager] Error initializing plugin ${plugin.id}:`, err);
    }
  }

  public registerFormatParser(extension: string, parser: CustomFormatParser) {
    const cleanExt = extension.toLowerCase().startsWith('.') ? extension.toLowerCase() : `.${extension.toLowerCase()}`;
    this.formatParsers.set(cleanExt, parser);
    console.log(`[CADPluginManager] Registered 3rd-party format parser for "${cleanExt}"`);
  }

  public getFormatParser(extension: string): CustomFormatParser | undefined {
    const cleanExt = extension.toLowerCase().startsWith('.') ? extension.toLowerCase() : `.${extension.toLowerCase()}`;
    return this.formatParsers.get(cleanExt);
  }

  public notifyModelLoaded(modelContext: CADModelContext) {
    this.plugins.forEach((plugin) => {
      try {
        if (plugin.onModelLoaded) {
          plugin.onModelLoaded(modelContext, this.api);
        }
      } catch (err) {
        console.error(`[CADPluginManager] Error in plugin ${plugin.id}.onModelLoaded:`, err);
      }
    });
  }

  public notifySelectionChanged(mesh: THREE.Mesh | null) {
    this.plugins.forEach((plugin) => {
      try {
        if (plugin.onSelectionChanged) {
          plugin.onSelectionChanged(mesh, this.api);
        }
      } catch (err) {
        console.error(`[CADPluginManager] Error in plugin ${plugin.id}.onSelectionChanged:`, err);
      }
    });
  }

  public notifyFrame(deltaTime: number) {
    this.plugins.forEach((plugin) => {
      try {
        if (plugin.onFrame) {
          plugin.onFrame(deltaTime, this.api);
        }
      } catch (err) {
        console.error(`[CADPluginManager] Error in plugin ${plugin.id}.onFrame:`, err);
      }
    });
  }

  public getRegisteredPlugins(): CADViewerPlugin[] {
    return Array.from(this.plugins.values());
  }
}
