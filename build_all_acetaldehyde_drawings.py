"""
MASTER BUILD SCRIPT: ACETALDEHYDE-PROPYLENE OXIDE DISTILLATION COLUMN (C-301) BLUEPRINTS
Generates all 6 A4 Print-Optimized CAD Blueprints (PDF + 300 DPI PNG):
  DWG-01: Process Flow Diagram (PFD) & Heat-Mass Balances
  DWG-02: VLE Analysis & McCabe-Thiele Stage Stepping (25 Stages)
  DWG-03: Column General Arrangement & Elevation Sectional CAD
  DWG-04: Sieve Tray Hydraulic Design & Internal Assembly
  DWG-05: Piping & Instrumentation Diagram (P&ID) with ISA-5.1 Loops
  DWG-06: Reboiler & Condenser Mechanical Details & 3D Isometric Assembly
"""

import sys
import os
import time

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), 'scripts')
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from generate_acetaldehyde_dwg01 import generate_acetaldehyde_dwg01
from generate_acetaldehyde_dwg02 import generate_acetaldehyde_dwg02
from generate_acetaldehyde_dwg03 import generate_acetaldehyde_dwg03
from generate_acetaldehyde_dwg04 import generate_acetaldehyde_dwg04
from generate_acetaldehyde_dwg05 import generate_acetaldehyde_dwg05
from generate_acetaldehyde_dwg06 import generate_acetaldehyde_dwg06

def main():
    print("=" * 80)
    print("BUILDING ACETALDEHYDE-PROPYLENE OXIDE DISTILLATION CAD BLUEPRINTS (A4 OPTIMIZED)")
    print("=" * 80)
    t0 = time.time()
    
    out_dir = os.path.join(os.path.dirname(__file__), 'Acetaldehyde_PropyleneOxide_Distillation_Drawings')
    os.makedirs(out_dir, exist_ok=True)
    
    print("\n--- PHASE 1: GENERATING A4 PRINT-OPTIMIZED SHEETS (ALL 6 SHEETS) ---")
    generate_acetaldehyde_dwg01(
        os.path.join(out_dir, '01_Acetaldehyde_Distillation_Process_Flow_Diagram_PFD.pdf'),
        os.path.join(out_dir, '01_Acetaldehyde_Distillation_Process_Flow_Diagram_PFD.png')
    )
    generate_acetaldehyde_dwg02(
        os.path.join(out_dir, '02_Acetaldehyde_VLE_McCabe_Thiele_Distillation_CAD.pdf'),
        os.path.join(out_dir, '02_Acetaldehyde_VLE_McCabe_Thiele_Distillation_CAD.png')
    )
    generate_acetaldehyde_dwg03(
        os.path.join(out_dir, '03_Acetaldehyde_Column_General_Arrangement_Elevation_CAD.pdf'),
        os.path.join(out_dir, '03_Acetaldehyde_Column_General_Arrangement_Elevation_CAD.png')
    )
    generate_acetaldehyde_dwg04(
        os.path.join(out_dir, '04_Acetaldehyde_Sieve_Tray_Assembly_Hydraulic_Details_CAD.pdf'),
        os.path.join(out_dir, '04_Acetaldehyde_Sieve_Tray_Assembly_Hydraulic_Details_CAD.png')
    )
    generate_acetaldehyde_dwg05(
        os.path.join(out_dir, '05_Acetaldehyde_Column_PID_Instrumentation_CAD.pdf'),
        os.path.join(out_dir, '05_Acetaldehyde_Column_PID_Instrumentation_CAD.png')
    )
    generate_acetaldehyde_dwg06(
        os.path.join(out_dir, '06_Acetaldehyde_Distillation_Reboiler_Condenser_3D_Isometric_CAD.pdf'),
        os.path.join(out_dir, '06_Acetaldehyde_Distillation_Reboiler_Condenser_3D_Isometric_CAD.png')
    )
    
    elapsed = time.time() - t0
    print(f"\nBUILD COMPLETE in {elapsed:.2f} seconds.")
    print(f"Acetaldehyde Distillation Drawings location: {out_dir}")

if __name__ == '__main__':
    main()
