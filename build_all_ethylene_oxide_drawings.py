r"""
MASTER BUILD SCRIPT: ETHYLENE OXIDE PACKED-BED TUBULAR REACTOR (R-201) CAD BLUEPRINTS
Generates all 5 Full CAD Blueprints (PDF + 300 DPI PNG):
  DWG-01: Equipment General Arrangement & Sectional Elevation CAD
  DWG-02: Process Piping & Instrumentation Diagram (P&ID) with ISA-5.1 Loops
  DWG-03: Mechanical Fabrication & ASME Section VIII Division 1 Code Details
  DWG-04: Rigorous Chemical Reaction Kinetics & Hydraulic Performance Curves
  DWG-05: 3D Isometric Plant Integration & Connected Piping Layout
Deploys to:
  - D:\GAMES\zercxes\CAD_Engineering_Drawings\Ethylene_Oxide_Reactor_Drawings
  - D:\Downloads\pedd
  - C:\Users\SOURISH SENAPATI\Downloads\pedd
  - C:\Users\SOURISH SENAPATI\Downloads
  - D:\Downloads
  - Brain Artifacts directory
"""

import sys
import os
import shutil
import time

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), 'scripts')
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from generate_reactor_dwg01 import generate_reactor_dwg01
from generate_reactor_dwg02 import generate_reactor_dwg02
from generate_reactor_dwg03 import generate_reactor_dwg03
from generate_reactor_dwg04 import generate_reactor_dwg04
from generate_reactor_dwg05 import generate_reactor_dwg05
from solve_ethylene_oxide_reactor import solve_reactor

def main():
    print("=" * 80)
    print("BUILDING ETHYLENE OXIDE TUBULAR REACTOR CAD BLUEPRINTS (TRIPLE EFFECT QUALITY)")
    print("=" * 80)
    t0 = time.time()

    root_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(root_dir, 'Ethylene_Oxide_Reactor_Drawings')
    os.makedirs(out_dir, exist_ok=True)

    # 1. Run numerical solver
    print("\n--- PHASE 1: SOLVING COUPLED ERGUN ODE & KINETICS ---")
    res = solve_reactor()

    # 2. Generate all 5 CAD drawings
    print("\n--- PHASE 2: GENERATING FULL CAD ENGINEERING BLUEPRINTS (5 SHEETS) ---")
    dwgs = [
        ('01_Ethylene_Oxide_Reactor_General_Arrangement_Elevation_CAD', generate_reactor_dwg01),
        ('02_Ethylene_Oxide_Reactor_Process_PID_Instrumentation_CAD', generate_reactor_dwg02),
        ('03_Ethylene_Oxide_Reactor_Mechanical_Fabrication_Details_CAD', generate_reactor_dwg03),
        ('04_Ethylene_Oxide_Reactor_Kinetic_Hydraulic_Performance_Curves_CAD', generate_reactor_dwg04),
        ('05_Ethylene_Oxide_Reactor_3D_Isometric_Plant_Assembly_CAD', generate_reactor_dwg05),
    ]

    all_generated_files = []

    for name, gen_fn in dwgs:
        pdf_path = os.path.join(out_dir, f"{name}.pdf")
        png_path = os.path.join(out_dir, f"{name}.png")
        print(f"Generating {name}...")
        gen_fn(pdf_path, png_path)
        all_generated_files.extend([pdf_path, png_path])

    # 3. Clean and Prepare Target Deployment Directories
    pedd_dirs = [
        r"D:\user\SOURISH SENAPATI\Downloads\pedd",
        r"D:\Downloads\pedd",
        r"C:\Users\SOURISH SENAPATI\Downloads\pedd",
    ]

    print("\n--- PHASE 3: CLEARING PEDD FOLDERS & DEPLOYING THE BEST BLUEPRINTS ---")
    for pdir in pedd_dirs:
        try:
            if os.path.exists(pdir):
                for item in os.listdir(pdir):
                    item_path = os.path.join(pdir, item)
                    if os.path.isfile(item_path) or os.path.islink(item_path):
                        os.unlink(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                print(f"[CLEARED] Emptied folder: {pdir}")
            else:
                os.makedirs(pdir, exist_ok=True)
                print(f"[CREATED] Created folder: {pdir}")
            
            # Copy only the 5 definitive reactor blueprints (PDF + PNG)
            for src_file in all_generated_files:
                fname = os.path.basename(src_file)
                dst_file = os.path.join(pdir, fname)
                shutil.copy2(src_file, dst_file)
            print(f"[DEPLOYED] Copied {len(all_generated_files)} clean blueprints to: {pdir}")
        except Exception as e:
            print(f"[ERROR] Failed in {pdir}: {e}")

    # Also deploy to root downloads and brain artifacts for accessibility
    extra_dirs = [
        r"C:\Users\SOURISH SENAPATI\Downloads",
        r"D:\Downloads",
        r"C:\Users\SOURISH SENAPATI\.gemini\antigravity\brain\ccfd5b92-7eb1-499b-94b8-0f0185a2992f",
    ]
    for edir in extra_dirs:
        try:
            os.makedirs(edir, exist_ok=True)
            for src_file in all_generated_files:
                shutil.copy2(src_file, os.path.join(edir, os.path.basename(src_file)))
        except Exception as e:
            pass

    elapsed = time.time() - t0
    print(f"\nBUILD COMPLETE in {elapsed:.2f} seconds.")
    print(f"Reactor drawings stored in: {out_dir}")

if __name__ == '__main__':
    main()
