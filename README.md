# Chemical & Process Equipment Engineering Designs & CAD Blueprints

[![License: Dual MIT / CC BY 4.0](https://img.shields.io/badge/License-MIT%20%7C%20CC%20BY%204.0-blue.svg)](LICENSE)
[![Standards: ASME Sec VIII Div 1](https://img.shields.io/badge/Standards-ASME%20Sec%20VIII%20Div%201-red.svg)](https://www.asme.org)
[![Flanges: ASME B16.5](https://img.shields.io/badge/Flanges-ASME%20B16.5%20Class%20150-orange.svg)](https://www.asme.org)
[![Instrumentation: ISA-5.1](https://img.shields.io/badge/P%26ID-ISA--5.1-green.svg)](https://www.isa.org)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Drawing Format: ISO A4 / A1](https://img.shields.io/badge/Format-ISO%20A4%20%7C%20ISO%20A1-purple.svg)](#drawing-formats--standards)

Industrial-grade chemical process equipment designs, mechanical blueprints, P&ID instrumentation diagrams, and parametric CAD generation engines.

All drawings are designed in strict compliance with **ASME Boiler and Pressure Vessel Code (BPVC) Section VIII Division 1**, **ASME B16.5 Flanges**, **ISA-5.1 Instrumentation Standards**, and **TEMA Standards**, authored by **Sourish Senapati** (Department of Chemical Engineering, Jadavpur University).

---

## Table of Contents
- [Project Overview](#project-overview)
- [Repository Structure](#repository-structure)
- [Equipment Designs](#equipment-designs)
  - [1. Packed-Bed Absorber Column (C-101)](#1-packed-bed-absorber-column-c-101)
  - [2. Multi-Effect Caustic Soda Evaporator Plant](#2-multi-effect-caustic-soda-evaporator-plant)
- [Parametric CAD Engine & Generation](#parametric-cad-engine--generation)
  - [Prerequisites & Installation](#prerequisites--installation)
  - [Building All Absorber Blueprints](#building-all-absorber-blueprints)
  - [Automated Compliance Auditing](#automated-compliance-auditing)
- [Drawing Formats & Standards](#drawing-formats--standards)
- [Licensing & Intellectual Property](#licensing--intellectual-property)
- [Author & Academic Credits](#author--academic-credits)

---

## Project Overview

This repository hosts comprehensive design deliverables for major chemical process plant equipment:
1. **Packed-Bed Absorption Column (C-101)**: Designed for bromine gas recovery ($0.25\ \text{m}^3/\text{s}$ gas feed containing $2.0\ \text{mol}\%\ \text{Br}_2$, absorbed into $17.25\ \text{kg/s}$ process water).
2. **Triple-Effect Evaporator System**: Industrial-scale multiple-effect evaporator for caustic soda ($\text{NaOH}$) concentration featuring forward-feed calandrias, flash chambers, vapor separators, and barometric condensers.

Each equipment package contains complete engineering documentation ranging from process flowsheets and piping & instrumentation diagrams (P&ID) to mechanical fabrication details, internal assembly sections, and isometric cutaway visualizations.

---

## Repository Structure

```
ENGINEERING-DESIGN/
├── Packed_Bed_Absorber_Drawings/       # Core A4 report-optimized drawings (PDF + PNG)
│   ├── 01_Packed_Bed_Absorber_General_Arrangement_CAD.pdf / .png
│   ├── 02_Packed_Bed_Absorber_Internal_Assembly_CAD.pdf / .png
│   ├── 03_Packed_Bed_Absorber_Packing_Support_Details_CAD.pdf / .png
│   ├── 04_Packed_Bed_Absorber_Nozzle_Manway_Details_CAD.pdf / .png
│   ├── 05_Packed_Bed_Absorber_PID_Instrumentation_CAD.pdf / .png
│   ├── 06_Packed_Bed_Absorber_3D_Isometric_Assembly_CAD.pdf / .png
│   └── A1_Large_Format/               # Large-scale plotter blueprints (A1 format)
│       ├── 01_Packed_Bed_Absorber_General_Arrangement_CAD.pdf / .png
│       ├── 02_Packed_Bed_Absorber_Internal_Assembly_CAD.pdf / .png
│       ├── 03_Packed_Bed_Absorber_Packing_Support_Details_CAD.pdf / .png
│       ├── 04_Packed_Bed_Absorber_Nozzle_Manway_Details_CAD.pdf / .png
│       └── 05_Packed_Bed_Absorber_PID_Instrumentation_CAD.pdf / .png
├── Previous_Triple_Effect_Evaporator/  # Triple-Effect Evaporator package (PDF + PNG)
│   ├── 01_Triple_Effect_NaOH_PFD.pdf / .png
│   ├── 02_Triple_Effect_Evaporator_Component_CAD.pdf / .png
│   ├── 03_Triple_Effect_Plant_GA_Structural_Elevation_CAD.pdf / .png
│   ├── 04_Triple_Effect_Detailed_PID_CAD.pdf / .png
│   └── 05_Triple_Effect_Mechanical_Fabrication_Details_CAD.pdf / .png
├── scripts/                            # Parametric CAD generation & audit engine
│   ├── __init__.py
│   ├── audit_drawings.py              # Automated ISO dimension & font compliance audit
│   ├── cad_common.py                  # A1 plotting geometry primitives & title blocks
│   ├── cad_common_a4.py               # A4 landscape plotting primitives & tables
│   ├── generate_a4_dwg01.py to 06.py  # A4 blueprint generators (Sheets 01 - 06)
│   └── generate_dwg01.py to 05.py     # A1 blueprint generators (Sheets 01 - 05)
├── build_all_absorber_drawings.py      # Master build script for all blueprints
├── requirements.txt                    # Python dependencies
├── LICENSE                             # Dual license (MIT + CC BY 4.0)
└── README.md                           # Documentation & engineering basis
```

---

## Equipment Designs

### 1. Packed-Bed Absorber Column (C-101)

#### Design Basis & Specifications
| Parameter | Value | Standard / Note |
|:---|:---|:---|
| **Equipment Tag** | C-101 | Packed Gas Absorber Column |
| **Service** | Bromine Recovery ($\text{Br}_2$ in Air) | Corrosive gas scrubbing |
| **Gas Feed Rate** | $0.25\ \text{m}^3/\text{s}$ ($900\ \text{m}^3/\text{h}$) | Normal operating conditions |
| **Solvent Feed Rate** | $17.25\ \text{kg/s}$ Water | Counter-current flow |
| **Inlet Gas Composition** | $2.0\ \text{mol}\%\ \text{Br}_2$ in air | Toxic / corrosive duty |
| **Target Absorption** | $> 95\%\ \text{Br}_2$ recovery | Environmental emission compliance |
| **Column Internal Diameter** | $750\ \text{mm}$ (ID) | Calculated based on flooding velocity |
| **Packed Height** | $4500\ \text{mm}$ total | Structured / random ceramic Intalox saddles |
| **Bed Segmentation** | 2 Beds ($2250\ \text{mm}$ each) | Mid-column redistributor installed |
| **Total Vessel Height** | $8350\ \text{mm}$ (Tangent-to-Tangent) | Skirt height $2000\ \text{mm}$ |
| **Shell Material** | 316L Stainless Steel | PV Code allowable stress $115\ \text{MPa}$ |
| **Design Pressure / Temp** | $0.35\ \text{MPa(g)}$ / $65^\circ\text{C}$ | Full vacuum rated for shutdown |
| **Corrosion Allowance** | $3.0\ \text{mm}$ | Heavy halogen service |
| **Head Geometry** | $2:1$ Ellipsoidal Heads | ASME BPVC Sec VIII Div 1 |

#### Drawing Catalog
- **Sheet 01: General Arrangement & Vessel Elevation (GA)**
  - Full elevation drawing with centerline geometry, nozzle elevation schedules, skirt base ring, anchor bolts, and foundation loading table.
- **Sheet 02: Internal Assembly & Packed Bed Sections**
  - Sectional elevation showing trough-type liquid distributor, spray nozzles, re-distributor pan, bed limiters, and packing support plates.
- **Sheet 03: Packing Support Plate & Hold-Down Grid Details**
  - Structural bar grid layout, perforated corrugated gas injection slots ($> 85\%$ free area to prevent premature flooding), hold-down grid clamp details.
- **Sheet 04: Nozzle Details, Flanges & Manway Assembly**
  - ASME B16.5 Class 150 Raised Face (RF) nozzle details, reinforcement pad dimensions, weld profiles (ASME Sec VIII UW-16), and $450\ \text{mm}$ swing-bolt manways (M1, M2).
- **Sheet 05: Piping & Instrumentation Diagram (P&ID)**
  - Complete ISA-5.1 instrument loops: feed gas differential pressure transmitters (PDIT-101), solvent flow control loop (FCV-102), liquid level controllers (LIC-103), vent gas halogen gas analyzer (AT-104), and high-integrity emergency relief interlocks.
- **Sheet 06: 3D Isometric View & Cutaway Assembly**
  - Isometric spatial representation displaying internal packing beds, external ladders, platform cages, nozzle orientation, and structural skirt support.

---

### 2. Multi-Effect Caustic Soda Evaporator Plant

#### Design Basis & Specifications
| Parameter | Value | Standard / Note |
|:---|:---|:---|
| **Service** | Caustic Soda ($\text{NaOH}$) Concentration | Tri-effect concentration train |
| **Feed Flowrate** | Industrial brine / dilute caustic solution | Multi-stage forward/backward feed |
| **Evaporator Type** | Vertical Long-Tube Falling/Rising Film Calandria | High heat transfer coefficient |
| **Heat Exchanger Standard**| TEMA Class R (Refinery / Heavy Chemical) | Removable tube bundle, floating head |
| **Condenser System** | Multi-jet Barometric Condenser | Vacuum maintenance system |
| **Materials of Construction** | Nickel 200 / Monel 400 contact parts | High temperature caustic embrittlement protection |

#### Drawing Catalog
- **Drawing 01: Process Flow Diagram (PFD)**
  - Mass and energy balances, stream tables, thermal vapor recompression loops, steam economy optimization.
- **Drawing 02: Component CAD & Calandria Tube-Sheet Layout**
  - Mechanical details of shell, tube bundle layout, triangular pitch spacing, impingement baffles, and tube-to-tubesheet expanded joints.
- **Drawing 03: Plant GA & Structural Elevation**
  - Multi-tier structural steel elevation showing evaporator staging, condenser tower, inter-stage pumps, vapor ducting, and maintenance clearance.
- **Drawing 04: Detailed P&ID**
  - Level, vacuum, temperature, and product density cascade control loops, safety relief valves (PSV), and automated steam throttling.
- **Drawing 05: Mechanical Fabrication Details**
  - Flange dimensions, shell joint weld preparations, expansion joints, vapor-liquid separator mesh pads, and dished head pressings.

---

## Parametric CAD Engine & Generation

Unlike conventional static CAD exports, all blueprints in this repository are **parametrically computed and rendered** via custom Python CAD engines.

### Key Features of the CAD Engine
- **Millimeter-Accurate Vector Canvas**: Built on top of `matplotlib` and `numpy` using true physical coordinate systems (ISO A4: $297 \times 210\ \text{mm}$; ISO A1: $841 \times 594\ \text{mm}$).
- **Zero Glyph Glitches**: Engineered typography utilizing standard CAD font vectors, eliminating character encoding errors ($\text{U+FFFD}$).
- **Collision-Free Text Layout**: Dynamic text placement algorithms that prevent label overlaps even in dense technical tables and dimensional callouts.
- **Standard Title Blocks (ISO 7200)**: Formatted title blocks containing drawing title, equipment specifications, drawing number, scale, date, and academic metadata.

### Prerequisites & Installation
Ensure you have Python 3.10+ installed:
```bash
# Clone the repository
git clone https://github.com/SourishSenapati/ENGINEERING-DESIGN.git
cd ENGINEERING-DESIGN

# Install required dependencies
py -m pip install -r requirements.txt
```

### Building All Absorber Blueprints
To regenerate all 6 A4 print sheets and 5 A1 large plotter drawings simultaneously:
```bash
py build_all_absorber_drawings.py
```
This produces both vector `.pdf` files (for sharp printing and scaling) and high-resolution `.png` renders (at 300 DPI for quick previews).

### Automated Compliance Auditing
Run the built-in drawing verification suite to guarantee drawing compliance:
```bash
py scripts/audit_drawings.py
```
The audit script inspects:
- Exact ISO A4 Landscape dimensions ($841.89 \times 595.28\ \text{pt}$)
- Title block metadata accuracy
- Absence of Unicode character substitution glitches
- Absence of unparsed raw LaTeX formatting leaks

---

## Drawing Formats & Standards

All drawings in this repository conform to the following international and industrial standards:
- **ASME BPVC Section VIII, Division 1**: Rules for Construction of Pressure Vessels
- **ASME B16.5**: Pipe Flanges and Flanged Fittings (NPS 1/2 through NPS 24)
- **ISA-5.1**: Instrumentation Symbols and Identification
- **TEMA**: Tubular Exchanger Manufacturers Association (Class R)
- **ISO 128 / ISO 5457 / ISO 7200**: Technical product documentation, drawing sheet sizes, layouts, and title blocks

---

## Licensing & Intellectual Property

This repository utilizes a dual-licensing structure to address both software and engineering design rights:

1. **Source Code & CAD Generation Scripts**:
   Licensed under the **[MIT License](LICENSE)**. You are free to inspect, run, modify, distribute, and integrate the Python CAD generation scripts into personal or commercial applications.

2. **Engineering Designs, CAD Blueprints, Flowsheets & Technical Documentation**:
   Licensed under the **[Creative Commons Attribution 4.0 International License (CC BY 4.0)](LICENSE)**. You are free to share, copy, adapt, and build upon the mechanical drawings, P&IDs, PFDs, and equipment specifications, provided appropriate credit is given to the author.

---

## Author & Academic Credits

- **Author**: Sourish Senapati
- **Department**: Department of Chemical Engineering
- **Institution**: Jadavpur University, Kolkata, India
- **Course**: B.E. Chemical Engineering — *Process Equipment Design & Drawing*
- **GitHub**: [@SourishSenapati](https://github.com/SourishSenapati)
