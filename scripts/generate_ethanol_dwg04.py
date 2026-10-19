"""
A4 OPTIMIZED: DWG-04 SIEVE TRAY HYDRAULIC DESIGN & INTERNAL ASSEMBLY
ETHANOL DISTILLATION SYSTEM (C-201) — 700 kmol/h FEED (7 mol% EtOH)
STUDENT: SOURISH SENAPATI | ROLL: 002310301035 | DATE: 01/09/2026
SUBJECT: PROCESS EQUIPMENT DESIGN & DRAWING | JADAVPUR UNIVERSITY
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon, Arc
from cad_common_a4 import (
    create_a4_canvas, draw_a4_border, draw_a4_title_block,
    cad_line, cad_rect, cad_circle, cad_arc, cad_text, cad_arrow,
    cad_dim_h, cad_dim_v, cad_balloon, cad_hatch_rect,
    cad_draw_table_a4, W, H, BK, GREY
)

def generate_ethanol_dwg04(out_pdf, out_png):
    fig, ax = create_a4_canvas()
    draw_a4_border(ax)
    
    SUB_INFO = 'ETHANOL DISTILLATION (C-201)  |  700 kmol/h FEED (7 mol% EtOH)  |  ID 1.20 m, R=3.0  |  ASME SEC VIII / TEMA'
    draw_a4_title_block(ax, 'SIEVE TRAY HYDRAULIC DESIGN & INTERNAL ASSEMBLY',
                        'JU/ChE/ED/DWG-04', scale='AS NOTED', date='01 / 09 / 2026', sub_info=SUB_INFO)
    
    # ═════════════════════════════════════════════════════════════════════════
    # VIEW A: TOP PLAN VIEW OF SINGLE-PASS SIEVE TRAY (SCALE 1:20)
    # ═════════════════════════════════════════════════════════════════════════
    CX_A, CY_A = 5.2, 13.6
    R_TRAY = 2.4   # Radius representing 600 mm real -> Scale 1:25 (1 cm = 250 mm)
    
    cad_text(ax, CX_A, CY_A + R_TRAY + 0.85, 'VIEW A: SINGLE-PASS SIEVE TRAY PLAN VIEW', sz=5.5, bold=True)
    cad_text(ax, CX_A, CY_A + R_TRAY + 0.50, 'SCALE 1:25 METRIC (COLUMN ID = 1200 mm)', sz=4.2, bold=True)
    
    # Column Shell Ring
    cad_circle(ax, CX_A, CY_A, R_TRAY + 0.12, lw=0.95, fill=False)
    cad_circle(ax, CX_A, CY_A, R_TRAY, lw=0.65, fill=True)
    # Centerlines
    cad_line(ax, CX_A - R_TRAY - 0.4, CY_A, CX_A + R_TRAY + 0.4, CY_A, lw=0.35, ls='-.')
    cad_line(ax, CX_A, CY_A - R_TRAY - 0.4, CX_A, CY_A + R_TRAY + 0.4, lw=0.35, ls='-.')
    
    # Segmental Downcomers (Left: Downcomer from tray above; Right: Downcomer to tray below)
    # Downcomer chord at X = R_TRAY - 0.75 (Chord width 180 mm real)
    DX_IN = CX_A - R_TRAY + 0.72
    DX_OUT = CX_A + R_TRAY - 0.72
    
    # Left Downcomer Inlet Area
    y_chord = np.sqrt(max(0, R_TRAY**2 - (0.72 - R_TRAY)**2))
    cad_line(ax, DX_IN, CY_A - y_chord, DX_IN, CY_A + y_chord, lw=0.85)
    cad_hatch_rect(ax, CX_A - R_TRAY, CY_A - y_chord, DX_IN - (CX_A - R_TRAY), 2*y_chord, pitch=0.15, angle=45, lw=0.25)
    cad_text(ax, CX_A - R_TRAY + 0.35, CY_A, 'DOWNCOMER\nFROM TRAY\nABOVE', sz=3.6, bold=True)
    
    # Right Downcomer Outlet & Weir
    cad_line(ax, DX_OUT, CY_A - y_chord, DX_OUT, CY_A + y_chord, lw=1.1)  # Outlet Weir
    cad_hatch_rect(ax, DX_OUT, CY_A - y_chord, CX_A + R_TRAY - DX_OUT, 2*y_chord, pitch=0.15, angle=-45, lw=0.25)
    cad_text(ax, CX_A + R_TRAY - 0.35, CY_A, 'DOWNCOMER\nTO TRAY\nBELOW', sz=3.6, bold=True)
    
    # Calming Zones (Unperforated margins: 0.20 cm = 50 mm)
    cad_line(ax, DX_IN + 0.22, CY_A - y_chord + 0.15, DX_IN + 0.22, CY_A + y_chord - 0.15, lw=0.35, ls=':')
    cad_line(ax, DX_OUT - 0.22, CY_A - y_chord + 0.15, DX_OUT - 0.22, CY_A + y_chord - 0.15, lw=0.35, ls=':')
    cad_text(ax, DX_IN + 0.12, CY_A + y_chord - 0.3, 'CALMING\nZONE', sz=3.0, bold=False, ha='left')
    cad_text(ax, DX_OUT - 0.12, CY_A + y_chord - 0.3, 'CALMING\nZONE', sz=3.0, bold=False, ha='right')
    
    # Active Perforated Bubbling Area
    # Draw representative array of holes
    for hx in np.arange(DX_IN + 0.40, DX_OUT - 0.30, 0.28):
        for hy in np.arange(CY_A - y_chord + 0.35, CY_A + y_chord - 0.35, 0.28):
            if (hx - CX_A)**2 + (hy - CY_A)**2 < (R_TRAY - 0.25)**2:
                cad_circle(ax, hx, hy, 0.04, fill=True, fc='#002288', ec=BK, lw=0.2)
                
    # Liquid Crossflow Arrow
    cad_arrow(ax, DX_IN + 0.6, CY_A, DX_OUT - 0.6, CY_A, lw=1.2, color='#008800', head_scale=9)
    cad_text(ax, CX_A, CY_A + 0.35, 'SINGLE-PASS LIQUID CROSSFLOW DIRECTION', sz=4.0, bold=True, color='#008800')
    
    # Dimension Callouts for View A
    cad_dim_h(ax, DX_IN, DX_OUT, CY_A - y_chord - 0.45, 'ACTIVE LENGTH = 840 mm', sz=3.8)
    cad_dim_v(ax, CX_A - R_TRAY - 0.4, CY_A - y_chord, CY_A + y_chord, 'WEIR LENGTH Lw = 840 mm', sz=3.6, text_offset=0.2)
    
    # ═════════════════════════════════════════════════════════════════════════
    # VIEW B: SECTIONAL ELEVATION B-B (TRAY HYDRAULIC PHENOMENA)
    # ═════════════════════════════════════════════════════════════════════════
    CX_B, CY_B = 5.2, 6.2
    
    cad_text(ax, CX_B, CY_B + 2.5, 'VIEW B: SECTION B-B — TRAY FROTH HYDRAULICS', sz=5.5, bold=True)
    cad_text(ax, CX_B, CY_B + 2.15, 'DETAIL OF CROSSFLOW FROTH REGIME & DOWNCOMER BACKUP', sz=4.2, bold=True)
    
    # Tray Floor & Tray Spacing (Ts = 450 mm real = 1.8 cm canvas)
    Y_TRAY_N = CY_B - 0.9
    Y_TRAY_N1 = CY_B + 0.9
    cad_line(ax, CX_B - 3.2, Y_TRAY_N, CX_B + 3.2, Y_TRAY_N, lw=0.9)   # Tray N floor
    cad_line(ax, CX_B - 3.2, Y_TRAY_N1, CX_B + 3.2, Y_TRAY_N1, lw=0.9) # Tray N-1 floor
    
    # Downcomer from Tray N-1 (Left)
    cad_line(ax, CX_B - 2.4, Y_TRAY_N1, CX_B - 2.4, Y_TRAY_N + 0.30, lw=0.85)
    cad_dim_v(ax, CX_B - 2.6, Y_TRAY_N, Y_TRAY_N + 0.30, 'h_cl = 35 mm', sz=3.4, text_offset=0.15)
    
    # Outlet Weir on Tray N (Right)
    cad_line(ax, CX_B + 2.2, Y_TRAY_N, CX_B + 2.2, Y_TRAY_N + 0.45, lw=1.1)
    cad_dim_v(ax, CX_B + 2.4, Y_TRAY_N, Y_TRAY_N + 0.45, 'hw = 50 mm', sz=3.4, text_offset=0.15)
    
    # Downcomer to Tray N+1 (Right)
    cad_line(ax, CX_B + 2.9, Y_TRAY_N + 0.45, CX_B + 2.9, Y_TRAY_N - 0.70, lw=0.85)
    
    # Aerated Froth Regime (Wavy profile on Tray N)
    froth_x = np.linspace(CX_B - 2.2, CX_B + 2.1, 40)
    froth_y = Y_TRAY_N + 0.75 + 0.06 * np.sin(froth_x * 8)
    for i in range(len(froth_x) - 1):
        cad_line(ax, froth_x[i], froth_y[i], froth_x[i+1], froth_y[i+1], lw=0.6, ls='--', color='#0066cc')
    cad_text(ax, CX_B, Y_TRAY_N + 0.95, 'AERATED FROTH REGIME (hf = 185 mm)', sz=3.8, bold=True, color='#0066cc')
    
    # Liquid Head over weir (how)
    cad_line(ax, CX_B + 2.0, Y_TRAY_N + 0.58, CX_B + 2.3, Y_TRAY_N + 0.58, lw=0.5, ls=':')
    cad_dim_v(ax, CX_B + 2.7, Y_TRAY_N + 0.45, Y_TRAY_N + 0.58, 'how = 14 mm', sz=3.2, text_offset=0.15)
    
    # Perforations and Rising Vapor Jets
    for vx in np.arange(CX_B - 1.8, CX_B + 1.8, 0.45):
        cad_line(ax, vx - 0.05, Y_TRAY_N, vx + 0.05, Y_TRAY_N, lw=1.2, color='#ffffff')
        cad_arrow(ax, vx, Y_TRAY_N - 0.35, vx, Y_TRAY_N + 0.25, lw=0.6, color='#0033aa', head_scale=4)
        
    cad_text(ax, CX_B, Y_TRAY_N - 0.45, 'VAPOR BUBBLING JETS (uv = 1.12 m/s)', sz=3.6, bold=True, color='#0033aa')
    
    # Tray Spacing Dimension
    cad_dim_v(ax, CX_B - 3.4, Y_TRAY_N, Y_TRAY_N1, 'TRAY SPACING Ts = 450 mm', sz=3.8, text_offset=0.2)
    
    # ═════════════════════════════════════════════════════════════════════════
    # VIEW C: PERFORATION GEOMETRY & HOLE PITCH DETAIL (TOP RIGHT)
    # ═════════════════════════════════════════════════════════════════════════
    RX_BASE = 14.8
    
    cad_rect(ax, RX_BASE, 12.2, 13.6, 4.4, lw=0.80, fill=True)
    cad_text(ax, RX_BASE + 6.8, 16.25, 'VIEW C: PERFORATION PATTERN & EQUILATERAL TRIANGULAR PITCH', sz=4.8, bold=True)
    
    # Draw triangular pattern schematic
    PX0, PY0 = RX_BASE + 3.2, 13.8
    PITCH_CM = 1.6
    
    pts = [
        (PX0, PY0),
        (PX0 + PITCH_CM, PY0),
        (PX0 + PITCH_CM/2, PY0 + PITCH_CM * np.sqrt(3)/2),
        (PX0 + 1.5*PITCH_CM, PY0 + PITCH_CM * np.sqrt(3)/2),
        (PX0 + PITCH_CM, PY0 + PITCH_CM * np.sqrt(3)),
        (PX0, PY0 + PITCH_CM * np.sqrt(3)),
    ]
    # Triangle grid lines
    cad_line(ax, pts[0][0], pts[0][1], pts[1][0], pts[1][1], lw=0.4, ls=':', color='#888888')
    cad_line(ax, pts[0][0], pts[0][1], pts[2][0], pts[2][1], lw=0.4, ls=':', color='#888888')
    cad_line(ax, pts[1][0], pts[1][1], pts[2][0], pts[2][1], lw=0.4, ls=':', color='#888888')
    cad_line(ax, pts[2][0], pts[2][1], pts[3][0], pts[3][1], lw=0.4, ls=':', color='#888888')
    cad_line(ax, pts[1][0], pts[1][1], pts[3][0], pts[3][1], lw=0.4, ls=':', color='#888888')
    
    # Hole Circles (5.0 mm dia)
    for p in pts:
        cad_circle(ax, p[0], p[1], 0.28, lw=0.8, fill=True, fc='#e6f2ff')
        cad_line(ax, p[0] - 0.35, p[1], p[0] + 0.35, p[1], lw=0.3, ls='-.')
        cad_line(ax, p[0], p[1] - 0.35, p[0], p[1] + 0.35, lw=0.3, ls='-.')
        
    cad_dim_h(ax, pts[0][0], pts[1][0], PY0 - 0.40, 'PITCH p = 12.5 mm', sz=3.8)
    cad_text(ax, pts[2][0] + 0.8, pts[2][1] + 0.5, 'HOLE DIA dh = 5.0 mm\n(BURR-FREE PUNCHED)', sz=3.8, bold=True)
    
    # Explanatory Callouts
    spec_txt = (
        'PERFORATION SPECIFICATIONS:\n'
        '- Hole Diameter (dh): 5.0 mm (3/16") punched 304L SS sheet\n'
        '- Pitch (p): 12.5 mm Equilateral Triangular (30 deg orientation)\n'
        '- Hole-to-Active Area Ratio (Ah/Aa): 10.2 %\n'
        '- Sheet Thickness: 2.5 mm (12 B.W.G.)\n'
        '- Fabrication: Precision CNC gang-punched, smooth deburred top'
    )
    cad_text(ax, RX_BASE + 7.2, 13.9, spec_txt, sz=3.6, bold=False, ha='left')
    
    # ═════════════════════════════════════════════════════════════════════════
    # RIGHT HALF: HYDRAULIC DESIGN & PRESSURE DROP TABLES
    # ═════════════════════════════════════════════════════════════════════════
    # 1. Tray Geometry Table
    t1_headers = ['GEOMETRIC PARAMETER', 'SYMBOL', 'VALUE', 'UNIT']
    t1_rows = [
        ['Column Internal Diameter', 'Dc', '1200', 'mm'],
        ['Total Tower Cross-Section Area', 'At', '1.131', 'm2'],
        ['Downcomer Area (Inlet / Outlet)', 'Ad', '0.124 (11.0 %)', 'm2'],
        ['Net Free Area (At - Ad)', 'An', '1.007', 'm2'],
        ['Active Bubbling Area', 'Aa', '0.883 (78.1 %)', 'm2'],
        ['Total Perforation Hole Area', 'Ah', '0.090 (10.2 % Aa)', 'm2'],
        ['Weir Length (Segmental Chord)', 'Lw', '840', 'mm'],
        ['Weir Height', 'hw', '50.0', 'mm'],
        ['Downcomer Clearance Height', 'hcl', '35.0', 'mm'],
        ['Tray Spacing', 'Ts', '450', 'mm'],
    ]
    t1_col_w = [4.8, 1.8, 4.4, 2.6]
    cad_draw_table_a4(ax, RX_BASE, 7.80, t1_headers, t1_rows, t1_col_w,
                      row_h=0.32, title='TABLE 1: SIEVE TRAY GEOMETRY & PHYSICAL DIMENSIONS',
                      title_sz=4.6, sz=3.8)
    
    # 2. Hydraulic Performance & Pressure Drop Summary Table
    t2_headers = ['HYDRAULIC METRIC', 'CALCULATED', 'ALLOWABLE', 'STATUS / CHECK']
    t2_rows = [
        ['Operating Vapor Velocity (uv)', '1.12 m/s', '1.64 m/s (uf)', 'PASS (68.3 % Flooding)'],
        ['Dry Tray Pressure Drop (hd)', '28.4 mm liq', '< 40.0 mm', 'PASS (Orifice drop)'],
        ['Liquid Height Over Weir (how)', '14.2 mm liq', '> 10.0 mm', 'PASS (Francis Formula)'],
        ['Residual Surface Tension Drop (hr)', '9.8 mm liq', '5 - 15 mm', 'PASS (Aeration drop)'],
        ['Total Tray Pressure Drop (ht)', '62.4 mm (540 Pa)', '< 75 mm (650 Pa)', 'PASS (Optimal range)'],
        ['Downcomer Head Loss (hdc)', '8.6 mm liq', '< 25.0 mm', 'PASS (Sub-weir flow)'],
        ['Clear Downcomer Backup (hdc_tot)', '165 mm liq', '< 225 mm (50 % Ts)', 'PASS (Zero choke flood)'],
        ['Fractional Entrainment (psi)', '0.021 kg/kg', '< 0.050 kg/kg', 'PASS (Low entrainment)'],
    ]
    t2_col_w = [4.8, 2.8, 3.2, 2.8]
    cad_draw_table_a4(ax, RX_BASE, 4.40, t2_headers, t2_rows, t2_col_w,
                      row_h=0.32, title='TABLE 2: HYDRAULIC VALIDATION & PRESSURE DROP BREAKDOWN',
                      title_sz=4.6, sz=3.8)
    
    # Save Outputs
    fig.savefig(out_pdf, format='pdf', dpi=300)
    fig.savefig(out_png, format='png', dpi=300)
    plt.close(fig)
    print(f"  [OK] DWG-04 generated: {os.path.basename(out_pdf)}")

if __name__ == '__main__':
    out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Ethanol_Water_Distillation_Drawings')
    os.makedirs(out_dir, exist_ok=True)
    generate_ethanol_dwg04(
        os.path.join(out_dir, '04_Ethanol_Sieve_Tray_Assembly_Hydraulic_Details_CAD.pdf'),
        os.path.join(out_dir, '04_Ethanol_Sieve_Tray_Assembly_Hydraulic_Details_CAD.png')
    )
