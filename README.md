# Chemical & Process Equipment Engineering Designs & CAD Blueprints

[![License: Educational Non-Commercial Only](https://img.shields.io/badge/License-Educational%20Only%20(CC%20BY--NC%204.0)-red.svg)](LICENSE)
[![Standards: ASME Sec VIII Div 1](https://img.shields.io/badge/Standards-ASME%20Sec%20VIII%20Div%201-red.svg)](https://www.asme.org)
[![Flanges: ASME B16.5](https://img.shields.io/badge/Flanges-ASME%20B16.5%20Class%20150-orange.svg)](https://www.asme.org)
[![Instrumentation: ISA-5.1](https://img.shields.io/badge/P%26ID-ISA--5.1-green.svg)](https://www.isa.org)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Drawing Format: ISO A4 / A1](https://img.shields.io/badge/Format-ISO%20A4%20%7C%20ISO%20A1-purple.svg)](#drawing-formats--standards)

Industrial-grade chemical process equipment designs, mechanical blueprints, P&ID instrumentation diagrams, and parametric CAD generation engines.

All drawings are designed in strict compliance with **ASME Boiler and Pressure Vessel Code (BPVC) Section VIII Division 1**, **ASME B16.5 Flanges**, **ISA-5.1 Instrumentation Standards**, and **TEMA Standards**, authored by **Sourish Senapati** (Department of Chemical Engineering, Jadavpur University).

> **License Notice**: This repository is strictly for **Non-Commercial Educational & Academic Use Only with Mandatory Attribution** to **Sourish Senapati**. Commercial use is strictly prohibited. See [LICENSE](LICENSE) for full details.

---

## Table of Contents

- [Project Portfolios](#project-portfolios)
  - [1. Packed-Bed Bromine Absorber – Mass Transfer and Process Safety Design](#1-packed-bed-bromine-absorber--mass-transfer-and-process-safety-design)
  - [2. Triple-Effect NaOH Evaporation Plant – Process Design and Equipment CAD](#2-triple-effect-naoh-evaporation-plant--process-design-and-equipment-cad)
  - [3. Ethanol–Water Recovery – Distillation Process Design and Equipment Sizing](#3-ethanolwater-recovery--distillation-process-design-and-equipment-sizing)
  - [4. Acetaldehyde–Propylene Oxide Distillation – McCabe–Thiele Design & Blueprints](#4-acetaldehyde-propylene-oxide-distillation--mccabe-thiele-design--blueprints)
  - [5. Ethylene Oxide Packed-Bed Tubular Reactor – Coupled Ergun Hydraulics & Kinetics](#5-ethylene-oxide-packed-bed-tubular-reactor--coupled-ergun-hydraulics--kinetics)
- [Repository Structure](#repository-structure)
- [Parametric CAD Engine & Generation](#parametric-cad-engine--generation)
  - [Prerequisites & Installation](#prerequisites--installation)
  - [Building Blueprint Packages](#building-blueprint-packages)
  - [Automated Compliance Auditing](#automated-compliance-auditing)
- [Drawing Formats & Standards](#drawing-formats--standards)
- [Licensing & Intellectual Property](#licensing--intellectual-property)
- [Author & Academic Credits](#author--academic-credits)

---

## Project Portfolios

### 1. Packed-Bed Bromine Absorber – Mass Transfer and Process Safety Design

- **Duration**: 29 Sep, 2026 – 13 Oct, 2026
- **Team Size**: 1
- **Mentor**: Prof. A. Bhawal
- **Key Skills / Technologies**: Mass Transfer, Gas Absorption, Process Equipment Design, Packed Column Design, Process Flow Diagram (PFD), Piping and Instrumentation Diagram (P&ID), Process Safety, Instrumentation and Control, SolidWorks, AutoCAD
- **Repository Location**: [`Packed_Bed_Absorber_Drawings/`](Packed_Bed_Absorber_Drawings/)

#### Description
Developed a preliminary packed-bed bromine scrubber design for a gas stream containing $2\ \text{mol}\%\ \text{bromine}$ at $0.25\ \text{m}^3/\text{s}$. Sized a $750\ \text{mm}$ internal-diameter, $9.63\ \text{m}$ high absorber with a $4.5\ \text{m}$ bed of $25\ \text{mm}$ ceramic Raschig rings and a water flow of $17.25\ \text{kg/s}$, targeting $90\%\ \text{bromine}$ removal.

Prepared process documentation and mechanical CAD detailing for the distributor, demister, packing support, nozzles and manways. Incorporated liquid-to-gas ratio control, bed differential-pressure alarms/interlocks, level control, emissions-monitoring concepts and pressure-relief provisions. Applied mass-transfer fundamentals, preliminary equipment-design methods and process-safety principles.

#### Drawing Catalog
- **DWG 01**: General Arrangement & Vessel Elevation (Nozzle schedules, design parameters, support skirt, foundation details)
- **DWG 02**: Internal Assembly & Packed Bed Sections (Liquid distributor, redistributor, packing hold-down and support plates)
- **DWG 03**: Packing Support Plate & Hold-Down Grid Details (Structural bar grids, slot geometry, gas injection openings)
- **DWG 04**: Nozzle Details, Flanges & Manway Assembly (ANSI/ASME B16.5 Class 150 RF, reinforcing pads, weld details)
- **DWG 05**: Piping & Instrumentation Diagram (P&ID) with ISA-5.1 tag numbers and control loops
- **DWG 06**: 3D Isometric View & Cutaway Assembly (Visual spatial perspective and structural layout)
*(Also available in A1 Large Plotter Format under `Packed_Bed_Absorber_Drawings/A1_Large_Format/`)*

---

### 2. Triple-Effect NaOH Evaporation Plant – Process Design and Equipment CAD

- **Duration**: 01 Sep, 2026 – 29 Sep, 2026
- **Team Size**: 1
- **Mentor**: Prof. RJC
- **Key Skills / Technologies**: Chemical Process Design, Material and Energy Balances, Heat Transfer, Triple-Effect Evaporation, Process Flow Diagram (PFD), Piping and Instrumentation Diagram (P&ID), Equipment Design, Process Control, AutoCAD, SolidWorks
- **Repository Location**: [`Previous_Triple_Effect_Evaporator/`](Previous_Triple_Effect_Evaporator/)

#### Description
Designed a preliminary forward-feed triple-effect evaporator for concentrating $400\ \text{tonnes/day}$ of $15\ \text{wt}\%\ \text{NaOH}$ feed into $5,000\ \text{kg/h}$ of $50\ \text{wt}\%\ \text{product}$. Completed material and energy balances, estimating a total evaporation rate of $11,666.7\ \text{kg/h}$, a total heat duty of $8.805\ \text{MW}$ and a heat-transfer area of $68.3\ \text{m}^2$ per effect.

Developed a process flow diagram, detailed P&ID, plant general arrangement and equipment/fabrication drawings. Documented pumps, calandrias, condenser, steam and vacuum systems, DCS cascade-control concepts and preliminary ASME/TEMA-oriented equipment-design considerations. The project applies heat-transfer, process-design and equipment-integration principles to an industrial-scale chemical process.

#### Drawing Catalog
- **Drawing 01**: Process Flow Diagram (PFD) with Mass & Energy Balances
- **Drawing 02**: Component CAD & Calandria Tube-Sheet Layout (TEMA standards, tube pitch, baffle cuts)
- **Drawing 03**: Plant GA & Structural Elevation (Multi-level structural framing, access platforms, pipe racks)
- **Drawing 04**: Detailed P&ID with instrumentation, safety relief valves, vacuum loops, level controls
- **Drawing 05**: Mechanical Fabrication Details (Flanges, expansion joints, mist eliminators, dished heads)

---

### 3. Ethanol–Water Recovery – Distillation Process Design and Equipment Sizing

- **Duration**: 04 Aug, 2026 – 01 Sep, 2026
- **Team Size**: 1
- **Key Skills / Technologies**: Separation Processes, Distillation, Vapour-Liquid Equilibrium, Wilson Thermodynamic Model, Material Balances, McCabe-Thiele Method, Process Equipment Design, Equipment Sizing, Process Flow Diagrams, AutoCAD
- **Repository Location**: [`Ethanol_Water_Distillation_Drawings/`](Ethanol_Water_Distillation_Drawings/)

#### Description
Developed a preliminary ethanol-water separation process for a $700\ \text{kmol/h}$ feed containing $7\ \text{mol}\%\ \text{ethanol}$. Performed material balances, vapour-liquid equilibrium analysis using the Wilson model, and McCabe-Thiele distillation-stage calculations.

Selected a preliminary reflux ratio of $3.0$ and a column internal diameter of approximately $1.20\ \text{m}$. Developed a process flow diagram covering the feed tank, pump, distillation column, reboiler, condenser and reflux drum. Documented the design basis, preliminary equipment sizing and assumptions for process-engineering review.

#### Drawing Catalog
- **DWG 01**: Process Flow Diagram (PFD) & Heat-Mass Balances (T-101, P-101, E-101, C-201, E-102, V-101, P-102, E-103, E-104 with 8 stream tables, 100.000% mass balance closure)
- **DWG 02**: VLE Analysis (Wilson Model) & McCabe-Thiele Stages (Azeotrope pinch point, $R=3.0$ ROL, $q=1.0$ feed line, 14 trays + reboiler = 15 theoretical stages, Murphree efficiency $65\%$, 24 actual sieve trays)
- **DWG 03**: Distillation Column General Arrangement & Elevation (Dual-view sectional elevation and exterior elevation with platform cages and ASME B16.5 nozzle schedule)
- **DWG 04**: Sieve Tray Hydraulic Design & Internal Assembly (Top plan view, crossflow froth section, $5\ \text{mm}$ hole on $15.0\ \text{mm}$ triangular pitch, $10.1\%$ hole area, $68.3\%$ flooding check)
- **DWG 05**: Piping & Instrumentation Diagram (P&ID) with ISA-5.1 Loops (Split-range pressure, Tray 6 rectifying reflux cascade, sump level, column DP interlock, safety relief)
- **DWG 06**: Reboiler & Condenser Details & 3D Isometric Assembly (Vertical thermosiphon reboiler TEMA BEM, condenser TEMA AEL, 3D spatial isometric plant assembly)

---

### 4. Acetaldehyde–Propylene Oxide Distillation – McCabe–Thiele Design & Blueprints

- **Duration**: 17 Nov, 2026
- **Team Size**: 1
- **Key Skills / Technologies**: Separation Processes, Binary Distillation, Vapour-Liquid Equilibrium (VLE), McCabe–Thiele Graphical Method, Tangent Pinch Analysis, Minimum Reflux Ratio, Column Hydraulics, Sieve Tray Design, PFD, P&ID (ISA-5.1), Heat Exchangers (TEMA BEM/AEL), ASME Section VIII Div 1
- **Repository Location**: [`Acetaldehyde_PropyleneOxide_Distillation_Drawings/`](Acetaldehyde_PropyleneOxide_Distillation_Drawings/)

#### Description
Engineered a complete industrial-grade binary distillation column design separating an equimolar mass feed of $12,000\ \text{kg/h}$ ($50\ \text{wt}\%\ \text{Acetaldehyde}$, $50\ \text{wt}\%\ \text{Propylene Oxide}$, $60\%\ \text{vapour feed}$, $q = 0.40$) into a high-purity distillate containing $97\ \text{wt}\%\ \text{Acetaldehyde}$ ($6,000\ \text{kg/h}$) and a stripped bottoms stream containing $97\ \text{wt}\%\ \text{Propylene Oxide}$ ($6,000\ \text{kg/h}$, $3\ \text{wt}\%\ \text{Acetaldehyde}$).

Conducted rigorous material balances ($100.000\%$ closure), VLE equilibrium curve and tangent pinch analysis ($(x_P, y_P) = (0.49152, 0.62013)$), minimum reflux evaluation ($R_{\min} = 2.7754$), and operating lines determination at $R = 1.4 R_{\min} = 3.8855$ ($m_R = 0.79531$, $m_S = 1.20176$). Stepped all 25 theoretical stages (12 rectifying trays, feed stage at Stage 13, 12 stripping trays + 1 partial reboiler). Sized a $2.00\ \text{m}$ internal-diameter column with 24 actual sieve trays, thermosiphon reboiler ($Q_R = 3,912.45\ \text{kW}$), and overhead total condenser ($Q_C = 4,733.92\ \text{kW}$).

#### Drawing Catalog
- **DWG 01**: Process Flow Diagram (PFD) & Heat-Mass Balances (T-301, P-301, E-301, C-301, E-302, E-303, V-301, P-302, E-304, E-305 with 10 stream tables, 100.000% mass balance closure)
- **DWG 02**: VLE Analysis & McCabe-Thiele Theoretical Stages (Tangent pinch point, $R=3.8855$ ROL, $q=0.40$ feed line, 24 trays + reboiler = 25 theoretical stages, composition profiles)
- **DWG 03**: Distillation Column General Arrangement & Elevation (Dual-view sectional elevation and exterior elevation with platform cages and ASME B16.5 Class 150 RF nozzle schedule)
- **DWG 04**: Sieve Tray Hydraulic Design & Internal Assembly (Top plan view, crossflow froth section, $5\ \text{mm}$ hole on $15.0\ \text{mm}$ triangular pitch, $10.1\%$ hole area, $71.5\%$ flooding check)
- **DWG 05**: Piping & Instrumentation Diagram (P&ID) with ISA-5.1 Loops (Split-range pressure, Tray 18 sensitive temp cascade, column DP flooding interlock, sump level, safety relief)
- **DWG 06**: Reboiler & Condenser Details & 3D Isometric Assembly (Vertical thermosiphon reboiler TEMA BEM, condenser TEMA AEL, 3D spatial isometric plant assembly)

### 5. Ethylene Oxide Packed-Bed Tubular Reactor – Coupled Ergun Hydraulics & Kinetics

- **Duration**: Nov, 2026
- **Team Size**: 1
- **Author**: Sourish Senapati (Exam Roll No: `002310301035`)
- **Key Skills / Technologies**: Chemical Reaction Engineering, Heterogeneous Catalysis, Ergun Equation Coupled ODE Modeling, Packed-Bed Tubular Reactor (PBR) Design, Runge-Kutta Numerical Integration, Thermal Utilities (Dowtherm A), ASME Section VIII Div 1, ISA-5.1 Instrumentation, SolidWorks 2025 SP1.2, STEP AP214, WebGL Three.js PBR, AutoCAD / ezdxf A1 CAD
- **Repository Location**: [`Ethylene_Oxide_Reactor_Drawings/`](Ethylene_Oxide_Reactor_Drawings/)

#### Description
Rigorous chemical reaction engineering design, hydraulic modeling, native SolidWorks 2025 3D CAD modeling, and plant integration for a multi-tubular fixed-bed catalytic reactor (R-201) converting ethylene to ethylene oxide over an $\text{Ag}/\alpha\text{-Al}_2\text{O}_3$ catalyst ($D_p = 1/2\text{ in}$, $\rho_c = 140\text{ lb/ft}^3$, $\phi = 0.50$) at $260^\circ\text{C}$ and $25\text{ atm}$ inlet pressure.

Solved the non-linear coupled differential system for reaction conversion $dX/dW$ and Ergun momentum loss $dy/dW$ ($y = P/P_0$) with non-equimolar expansion ($\epsilon = -0.14286$). Determined exact catalyst mass $W = 26,469.02\text{ lb cat}$ ($12,006.16\text{ kg}$, an $8.52\%$ penalty over the zero-$\Delta P$ ideal baseline of $24,390.55\text{ lb}$), exit pressure $P_{\text{exit}} = 20.998\text{ atm}$ ($\Delta P = 4.002\text{ atm} = 58.81\text{ psi}$), and net volumetric expansion $v/v_0 = 1.1202$. Sized $1,021$ Schedule 80 tubes ($1.5\text{-in}$ nominal, $D_i = 1.500\text{ in}$, $D_o = 1.900\text{ in}$) packed to $30.0\text{ ft}$ stock length inside an $84.0\text{-in}$ ($2.134\text{ m}$) ID pressure shell ($t_s = 1.125\text{ in}$ SA-516 Gr 70) cooled by circulating Dowtherm A ($420\text{ gpm}$).

#### Drawing Catalog & Turnkey Deliverables
- **DWG 01**: Equipment General Arrangement & Sectional Elevation CAD (`JU-CHE-PEDD-R201-DWG-01`)
- **DWG 02**: Process Piping & Instrumentation Diagram (P&ID) with ISA-5.1 Loops (`JU-CHE-PEDD-R201-DWG-02`)
- **DWG 03**: Mechanical Fabrication & ASME Section VIII Division 1 Code Details (`JU-CHE-PEDD-R201-DWG-03`)
- **DWG 04**: Rigorous Reaction Kinetics & Hydraulic Performance Curves (`JU-CHE-PEDD-R201-DWG-04`)
- **DWG 05**: 3D Isometric Plant Integration & Connected Piping Layout (`JU-CHE-PEDD-R201-DWG-05`)
- **Native SolidWorks 2025 CAD**: 6x `.SLDPRT` parametric parts + master `.SLDASM` assembly under `cad/sldprt/` and `cad/sldasm/`.
- **Standard STEP AP214 Exchange**: Master model `R201_Ethylene_Oxide_Reactor_Assembly.step` ($307\text{ KB}$, $4,138$ entities) + component STEPs under `cad/step/`.
- **Interactive 3D WebGL Orbit Viewer**: Three.js dynamic Z-plane slicing and PBR inspector in `cad/viewer/index.html` + multi-material PBR GLB models under `cad/glb/`.
- **Standard A1 Vector DXF Drawings**: Fully layered engineering drawings under `cad/dxf/`.
- **10-Point Integration Audit**: 100% passed (zero disconnected lines, zero mock pipes) verified in `mechanical/plant_integration_audit_report.md`.

---

## Repository Structure

```
CAD_Engineering_Drawings/
├── Ethylene_Oxide_Reactor_Drawings/      # Complete Turnkey Reactor Package (Toor Dal Standard)
│   ├── README.md                        # Master engineering treatise & documentation index
│   ├── 01..05 Drawings (PDF + PNG)      # Official 5-sheet vector drawing package
│   ├── aspen/                           # Aspen Plus / HYSYS simulation reports & stream tables
│   ├── cad/
│   │   ├── dxf/                         # 2D Vector DXFs (Elevation, Tubesheet, P&ID)
│   │   ├── glb/                         # PBR GLB 3D models (Full exterior & internal cutaway)
│   │   ├── pdf/ & png/                  # Drawing prints and 300 DPI high-res renders
│   │   ├── sldasm/                      # Native SolidWorks 2025 Master Assembly (.SLDASM)
│   │   ├── sldprt/                      # 6x Native SolidWorks Parametric Parts (.SLDPRT)
│   │   ├── step/                        # Standard ISO 10303-21 STEP AP214 B-Rep models
│   │   └── viewer/                      # Standalone Three.js 3D WebGL Orbit Viewer
│   ├── mechanical/                      # ASME Section VIII Div 1 calculations & audit reports
│   ├── piping_instrumentation/          # Master equipment, line lists, valves, instruments
│   └── scripts/                         # SolidWorks COM, PBR GLB, DXF & audit generators
├── Acetaldehyde_PropyleneOxide_Distillation_Drawings/ # Acetaldehyde-PO Distillation package (PDF + PNG)
│   ├── 01_Acetaldehyde_Distillation_Process_Flow_Diagram_PFD.pdf / .png
│   ├── 02_Acetaldehyde_VLE_McCabe_Thiele_Distillation_CAD.pdf / .png
│   ├── 03_Acetaldehyde_Column_General_Arrangement_Elevation_CAD.pdf / .png
│   ├── 04_Acetaldehyde_Sieve_Tray_Assembly_Hydraulic_Details_CAD.pdf / .png
│   ├── 05_Acetaldehyde_Column_PID_Instrumentation_CAD.pdf / .png
│   └── 06_Acetaldehyde_Distillation_Reboiler_Condenser_3D_Isometric_CAD.pdf / .png
├── Ethanol_Water_Distillation_Drawings/  # Ethanol-Water Distillation package (PDF + PNG)
│   ├── 01_Ethanol_Distillation_Process_Flow_Diagram_PFD.pdf / .png
│   ├── 02_Ethanol_VLE_McCabe_Thiele_Distillation_CAD.pdf / .png
│   ├── 03_Ethanol_Column_General_Arrangement_Elevation_CAD.pdf / .png
│   ├── 04_Ethanol_Sieve_Tray_Assembly_Hydraulic_Details_CAD.pdf / .png
│   ├── 05_Ethanol_Column_PID_Instrumentation_CAD.pdf / .png
│   └── 06_Ethanol_Distillation_Reboiler_Condenser_3D_Isometric_CAD.pdf / .png
├── Packed_Bed_Absorber_Drawings/         # Packed-Bed Absorber package (A4 Format)
│   ├── 01_Packed_Bed_Absorber_General_Arrangement_CAD.pdf / .png
│   ├── 02_Packed_Bed_Absorber_Internal_Assembly_CAD.pdf / .png
│   ├── 03_Packed_Bed_Absorber_Packing_Support_Details_CAD.pdf / .png
│   ├── 04_Packed_Bed_Absorber_Nozzle_Manway_Details_CAD.pdf / .png
│   ├── 05_Packed_Bed_Absorber_PID_Instrumentation_CAD.pdf / .png
│   ├── 06_Packed_Bed_Absorber_3D_Isometric_Assembly_CAD.pdf / .png
│   └── A1_Large_Format/                 # Absorber large plotter blueprints (A1 Format)
├── Previous_Triple_Effect_Evaporator/    # Triple-Effect Evaporator package (PDF + PNG)
│   ├── 01_Triple_Effect_NaOH_PFD.pdf / .png
│   ├── 02_Triple_Effect_Evaporator_Component_CAD.pdf / .png
│   ├── 03_Triple_Effect_Plant_GA_Structural_Elevation.pdf / .png
│   ├── 04_Triple_Effect_Detailed_PID_CAD.pdf / .png
│   └── 05_Triple_Effect_Mechanical_Fabrication_Details.pdf / .png
├── VIRTUAL-PLANT/                        # ROS2 / Gazebo Digital Twin & Refinery CAD Drawings
├── scripts/                              # Parametric CAD generation & numerical ODE solvers
│   ├── __init__.py
│   ├── cad_common.py                    # Universal CAD drafting primitives & ASME title blocks
│   ├── cad_common_a4.py                 # A4 landscape plotting primitives
│   ├── solve_ethylene_oxide_reactor.py  # Coupled Ergun ODE numerical solver (RK-45)
│   ├── parametric_study_nt.py           # Schedule 80 tube count parametric study
│   ├── generate_reactor_dwg01.py to 05.py # Ethylene Oxide Reactor blueprint generators
│   ├── generate_acetaldehyde_dwg01.py to 06.py # Acetaldehyde Distillation blueprint generators
│   ├── generate_ethanol_dwg01.py to 06.py # Ethanol Distillation blueprint generators
│   ├── generate_a4_dwg01.py to 06.py    # Absorber A4 blueprint generators
│   └── generate_dwg01.py to 05.py       # Absorber A1 blueprint generators
├── build_all_ethylene_oxide_drawings.py  # Master build & deploy script for Reactor blueprints
├── build_all_absorber_drawings.py        # Master build script for Absorber blueprints
├── build_all_distillation_drawings.py    # Master build script for Distillation blueprints
├── build_all_acetaldehyde_drawings.py    # Master build script for Acetaldehyde blueprints
├── requirements.txt                      # Python dependencies (matplotlib, numpy, scipy, PyMuPDF)
├── LICENSE                               # Educational & Academic License (CC BY-NC 4.0)
└── README.md                             # Documentation & engineering basis
```

---

## Parametric CAD Engine & Generation

### Prerequisites & Installation
Ensure you have Python 3.10+ installed:
```bash
# Clone the repository
git clone https://github.com/SourishSenapati/ENGINEERING-DESIGN.git
cd ENGINEERING-DESIGN

# Install required dependencies
py -m pip install -r requirements.txt
```

### Building Blueprint Packages

- **Build Ethylene Oxide Reactor Blueprints (5 Sheets)**:
  ```bash
  py build_all_ethylene_oxide_drawings.py
  ```

- **Build Acetaldehyde–Propylene Oxide Distillation Blueprints (6 Sheets)**:
  ```bash
  py build_all_acetaldehyde_drawings.py
  ```

- **Build Ethanol Distillation Blueprints (6 Sheets)**:
  ```bash
  py build_all_distillation_drawings.py
  ```

- **Build Packed-Bed Absorber Blueprints (A4 + A1 Formats)**:
  ```bash
  py build_all_absorber_drawings.py
  ```

### Automated Compliance Auditing
Run the verification test suite to check all 18 A4 drawings across all three equipment packages:
```bash
py scripts/audit_drawings.py
```
Checks verified:
- Exact ISO A4 Landscape dimensions ($841.89 \times 595.28\ \text{pt}$)
- Title block metadata accuracy (`SOURISH SENAPATI`, `ROLL NO. 002310301035`)
- Absence of Unicode character substitution glitches (`U+FFFD`)
- Absence of unparsed raw LaTeX formatting leaks

---

## 🛠️ Universal CAD Native 3D Viewer (`cad-native-viewer`)

This repository includes **`cad-native-viewer`**, a high-precision VS Code, Cursor, Windsurf, VSCodium, and WSL extension that allows direct, native 3D viewing of CAD files just like PDFs and Markdown previews:

- **Supported CAD Formats**: `.step`, `.stp`, `.sldprt`, `.sldasm`, `.iges`, `.igs`, `.brep`, `.glb`, `.gltf`, `.stl`, `.obj`.
- **Pure WebAssembly Engine**: Powered by OpenCASCADE WebAssembly (`occt-import-js`), requiring **zero** external software or C++ compilers. Operates 100% offline on Windows, Linux, and macOS.
- **Interactive Toolset**:
  - Full 3D Orbit, Pan, Zoom, and Fit-to-Screen controls.
  - Dynamic 3-Axis Cross-Section Slicing (X, Y, Z sliders with normal flipping).
  - Precision Measurement Caliper (3D Euclidean distance $D = \sqrt{\Delta X^2 + \Delta Y^2 + \Delta Z^2}$).
  - Shading Presets: PBR Metallic Shaded, Sharp CAD Edges, Technical Wireframe, and Ghosted X-Ray.
  - Multi-body Component Tree with part visibility toggles and focus.
  - Direct export to binary GLB, STL, OBJ, and Ultra-HD PNG snapshots.
- **Package Location**: [`cad-native-viewer/`](cad-native-viewer/)

To install locally:
```bash
code --install-extension cad-native-viewer/cad-native-viewer-1.0.0.vsix
```

---

## 🌐 Virtual Plant Twin & Game-Engine Plant Simulator

For the full interactive 3D WebGL plant simulation environment, real-time chemical process telemetry, ROS 2 automation nodes, and Gazebo ODE physical twins, visit the companion repository:

👉 **[SourishSenapati/VIRTUAL-PLANT](https://github.com/SourishSenapati/VIRTUAL-PLANT)**

Features in `VIRTUAL-PLANT`:
- **React 19 + Three.js Industrial Plant Simulator**: First-person and orbit camera walkthroughs, animated catalyst tube cutaways, and procedural acoustic sound synthesis.
- **Gazebo ODE Physics World**: Multi-body rigid-body dynamics for a 100,000 BPD petroleum refinery and chemical processing complex.
- **ROS 2 Humble / Iron Middleware**: Real-time mass balance controllers, dynamic cut-point optimizers, and Safety Instrumented Systems (SIS).

---

## Drawing Formats & Standards

All drawings in this repository conform to the following international and industrial standards:
- **ASME BPVC Section VIII, Division 1**: Rules for Construction of Pressure Vessels
- **ASME B16.5**: Pipe Flanges and Flanged Fittings (Class 150 Raised Face)
- **ISA-5.1**: Instrumentation Symbols and Identification
- **TEMA**: Tubular Exchanger Manufacturers Association (Class R, Types BEM and AEL)
- **ISO 128 / ISO 5457 / ISO 7200**: Technical product documentation, drawing sheet sizes, layouts, and title blocks

---

## Licensing & Intellectual Property

This repository is licensed strictly for **Non-Commercial Educational & Academic Use Only with Mandatory Attribution**:

1. **Educational & Academic Use Only**:
   Free of charge strictly for classroom instruction, university coursework, academic research, and personal learning. Any commercial use, industrial exploitation, or inclusion in proprietary commercial tools is **strictly prohibited** without explicit, prior written consent from the author.

2. **Mandatory Attribution / Credit**:
   Any use, reference, lecture, presentation, or derivative work **must prominently credit Sourish Senapati** (Department of Chemical Engineering, Jadavpur University) and link back to this repository:
   `https://github.com/SourishSenapati/ENGINEERING-DESIGN`

- **CAD Blueprints, Flowsheets & Documentation**: Licensed under **[CC BY-NC 4.0 (Creative Commons Attribution-NonCommercial 4.0 International)](LICENSE)**.
- **Source Code & Parametric CAD Scripts**: Licensed under the **[Educational Non-Commercial Source License](LICENSE)**.

See the complete **[LICENSE](LICENSE)** file for full terms, conditions, and citation formats.

---

## Author & Academic Credits

- **Author**: Sourish Senapati
- **Department**: Department of Chemical Engineering
- **Institution**: Jadavpur University, Kolkata, India
- **Course**: B.E. Chemical Engineering — *Process Equipment Design & Drawing*
- **Mentors**:
  - Prof. A. Bhawal (Packed-Bed Absorber Design)
  - Prof. RJC (Triple-Effect Evaporator Design)
- **GitHub**: [@SourishSenapati](https://github.com/SourishSenapati)
