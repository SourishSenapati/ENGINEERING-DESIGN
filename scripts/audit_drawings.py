import fitz
import os
import glob

pdf_files = [
    r"d:\GAMES\zercxes\CAD_Engineering_Drawings\Packed_Bed_Absorber_Drawings\01_Packed_Bed_Absorber_General_Arrangement_CAD.pdf",
    r"d:\GAMES\zercxes\CAD_Engineering_Drawings\Packed_Bed_Absorber_Drawings\02_Packed_Bed_Absorber_Internal_Assembly_CAD.pdf",
    r"d:\GAMES\zercxes\CAD_Engineering_Drawings\Packed_Bed_Absorber_Drawings\03_Packed_Bed_Absorber_Packing_Support_Details_CAD.pdf",
    r"d:\GAMES\zercxes\CAD_Engineering_Drawings\Packed_Bed_Absorber_Drawings\04_Packed_Bed_Absorber_Nozzle_Manway_Details_CAD.pdf",
    r"d:\GAMES\zercxes\CAD_Engineering_Drawings\Packed_Bed_Absorber_Drawings\05_Packed_Bed_Absorber_PID_Instrumentation_CAD.pdf",
    r"d:\GAMES\zercxes\CAD_Engineering_Drawings\Packed_Bed_Absorber_Drawings\06_Packed_Bed_Absorber_3D_Isometric_Assembly_CAD.pdf",
]

print("="*80)
print("AUDITING ALL 6 A4 CAD DRAWINGS FOR STRICT COMPLIANCE")
print("="*80)

all_passed = True

for idx, p_pdf in enumerate(pdf_files, 1):
    doc = fitz.open(p_pdf)
    page = doc[0]
    rect = page.rect
    text = page.get_text()
    
    # 1. Dimension Check: ISO A4 Landscape is 841.89 x 595.28 pt
    w_ok = abs(rect.width - 841.89) < 0.5
    h_ok = abs(rect.height - 595.28) < 0.5
    dim_ok = w_ok and h_ok
    
    # 2. Student & Roll No.
    has_student = "SOURISH SENAPATI" in text
    has_roll_no = "ROLL NO." in text
    has_no_exam_roll = "EXAM ROLL" not in text
    has_no_sheet_no = "OF 05" not in text and "SHEET NO" not in text
    
    # 3. Unicode / Glyph Replacement check
    replacement_count = text.count(chr(65533))
    
    # 4. LaTeX syntax check
    latex_leak = any(k in text for k in ['\\frac', '\\rho', '\\Delta', '\\approx', '\\cdot', '$$'])
    
    print(f"\nDWG {idx}: {os.path.basename(p_pdf)}")
    print(f"  - Dimensions: {rect.width:.2f} x {rect.height:.2f} pt -> {'PASS (A4 Landscape)' if dim_ok else 'FAIL'}")
    print(f"  - Student Name (SOURISH SENAPATI): {'PASS' if has_student else 'FAIL'}")
    print(f"  - Roll Label ('ROLL NO.'): {'PASS' if has_roll_no else 'FAIL'}")
    print(f"  - No 'EXAM ROLL': {'PASS' if has_no_exam_roll else 'FAIL'}")
    print(f"  - No Sheet No ('OF 05'): {'PASS' if has_no_sheet_no else 'FAIL'}")
    print(f"  - Replacement Glyphs (U+FFFD): {replacement_count} -> {'PASS' if replacement_count == 0 else 'FAIL'}")
    print(f"  - LaTeX Leaks: {'PASS (None)' if not latex_leak else 'FAIL'}")
    
    if not (dim_ok and has_student and has_roll_no and has_no_exam_roll and has_no_sheet_no and replacement_count == 0 and not latex_leak):
        all_passed = False

print("\n" + "="*80)
if all_passed:
    print("ALL 6 DRAWINGS FULLY COMPLIANT WITH STRICT INDUSTRIAL & ACADEMIC STANDARDS!")
else:
    print("SOME CHECKS FAILED! INVESTIGATION NEEDED.")
print("="*80)
