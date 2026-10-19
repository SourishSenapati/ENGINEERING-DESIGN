"""
MASTER BUILD SCRIPT: PACKED-BED ABSORBER (C-101) BLUEPRINTS
Generates both:
  1. A4 Format (Readable on standard A4 paper / report submission with zero text overlap)
  2. A1 Large Plotter Format (Full large-scale blueprints)
"""

import sys
import os
import time

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), 'scripts')
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from generate_a4_dwg01 import generate_a4_dwg01
from generate_a4_dwg02 import generate_a4_dwg02
from generate_a4_dwg03 import generate_a4_dwg03
from generate_a4_dwg04 import generate_a4_dwg04
from generate_a4_dwg05 import generate_a4_dwg05
from generate_a4_dwg06 import generate_a4_dwg06

from generate_dwg01 import generate_dwg01
from generate_dwg02 import generate_dwg02
from generate_dwg03 import generate_dwg03
from generate_dwg04 import generate_dwg04
from generate_dwg05 import generate_dwg05

def main():
    print("================================================================================")
    print("BUILDING PACKED-BED ABSORBER CAD BLUEPRINTS (A4 OPTIMIZED + A1 LARGE FORMAT)")
    print("================================================================================")
    t0 = time.time()
    
    out_a4 = os.path.join(os.path.dirname(__file__), 'Packed_Bed_Absorber_Drawings')
    out_a1 = os.path.join(out_a4, 'A1_Large_Format')
    os.makedirs(out_a4, exist_ok=True)
    os.makedirs(out_a1, exist_ok=True)
    
    print("\n--- PHASE 1: GENERATING A4 PRINT-OPTIMIZED SHEETS (ALL 6 SHEETS) ---")
    generate_a4_dwg01(os.path.join(out_a4, '01_Packed_Bed_Absorber_General_Arrangement_CAD.pdf'),
                      os.path.join(out_a4, '01_Packed_Bed_Absorber_General_Arrangement_CAD.png'))
    generate_a4_dwg02(os.path.join(out_a4, '02_Packed_Bed_Absorber_Internal_Assembly_CAD.pdf'),
                      os.path.join(out_a4, '02_Packed_Bed_Absorber_Internal_Assembly_CAD.png'))
    generate_a4_dwg03(os.path.join(out_a4, '03_Packed_Bed_Absorber_Packing_Support_Details_CAD.pdf'),
                      os.path.join(out_a4, '03_Packed_Bed_Absorber_Packing_Support_Details_CAD.png'))
    generate_a4_dwg04(os.path.join(out_a4, '04_Packed_Bed_Absorber_Nozzle_Manway_Details_CAD.pdf'),
                      os.path.join(out_a4, '04_Packed_Bed_Absorber_Nozzle_Manway_Details_CAD.png'))
    generate_a4_dwg05(os.path.join(out_a4, '05_Packed_Bed_Absorber_PID_Instrumentation_CAD.pdf'),
                      os.path.join(out_a4, '05_Packed_Bed_Absorber_PID_Instrumentation_CAD.png'))
    generate_a4_dwg06(os.path.join(out_a4, '06_Packed_Bed_Absorber_3D_Isometric_Assembly_CAD.pdf'),
                      os.path.join(out_a4, '06_Packed_Bed_Absorber_3D_Isometric_Assembly_CAD.png'))
    
    elapsed = time.time() - t0
    print(f"\nBUILD COMPLETE in {elapsed:.2f} seconds.")
    print(f"A4 Drawings location: {out_a4}")
    print(f"A1 Drawings location: {out_a1}")

if __name__ == '__main__':
    main()
