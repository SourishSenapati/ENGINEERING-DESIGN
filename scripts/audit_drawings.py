import fitz
import os
import glob

base_dir = os.path.dirname(os.path.dirname(__file__))

absorber_pdfs = sorted(glob.glob(os.path.join(base_dir, "Packed_Bed_Absorber_Drawings", "*CAD.pdf")))
distillation_pdfs = sorted(glob.glob(os.path.join(base_dir, "Ethanol_Water_Distillation_Drawings", "*.pdf")))

all_groups = [
    ("PACKED-BED ABSORBER (C-101)", absorber_pdfs),
    ("ETHANOL-WATER DISTILLATION (C-201)", distillation_pdfs)
]

print("=" * 80)
print("AUDITING ALL A4 CAD DRAWINGS ACROSS PACKAGES FOR STRICT COMPLIANCE")
print("=" * 80)

total_passed = True

for group_name, pdf_list in all_groups:
    print(f"\n>>> PACKAGE: {group_name} ({len(pdf_list)} DRAWINGS) <<<")
    for idx, p_pdf in enumerate(pdf_list, 1):
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
        
        is_dwg_ok = dim_ok and has_student and has_roll_no and has_no_exam_roll and has_no_sheet_no and replacement_count == 0 and not latex_leak
        
        status_tag = "PASS" if is_dwg_ok else "FAIL"
        print(f"  [{status_tag}] DWG {idx:02d}: {os.path.basename(p_pdf)}")
        if not is_dwg_ok:
            total_passed = False
            print(f"       - Dimensions: {rect.width:.2f} x {rect.height:.2f} pt -> {'PASS' if dim_ok else 'FAIL'}")
            print(f"       - Student Name (SOURISH SENAPATI): {'PASS' if has_student else 'FAIL'}")
            print(f"       - Roll Label ('ROLL NO.'): {'PASS' if has_roll_no else 'FAIL'}")
            print(f"       - No 'EXAM ROLL': {'PASS' if has_no_exam_roll else 'FAIL'}")
            print(f"       - No Sheet No ('OF 05'): {'PASS' if has_no_sheet_no else 'FAIL'}")
            print(f"       - Replacement Glyphs (U+FFFD): {replacement_count}")
            print(f"       - LaTeX Leaks: {latex_leak}")

print("\n" + "=" * 80)
if total_passed:
    print("ALL DRAWINGS FULLY COMPLIANT WITH STRICT INDUSTRIAL & ACADEMIC STANDARDS!")
else:
    print("SOME CHECKS FAILED! INVESTIGATION NEEDED.")
print("=" * 80)
