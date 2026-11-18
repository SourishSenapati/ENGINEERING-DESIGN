"""
A4 OPTIMIZED: DWG-04 ACETALDEHYDE SIEVE TRAY HYDRAULIC DESIGN & INTERNAL ASSEMBLY
ACETALDEHYDE DISTILLATION SYSTEM (C-301) — 12000 kg/h FEED (50 wt% AcH, 60% VAPOUR)
STUDENT: SOURISH SENAPATI | ROLL NO.: 002310301035 | DATE: 17/11/2026
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

def generate_acetaldehyde_dwg04(out_pdf, out_png):
    fig, ax = create_a4_canvas()
    draw_a4_border(ax)
    
    SUB_INFO = 'ACETALDEHYDE DISTILLATION (C-301)  |  12000 kg/h FEED (50 wt% AcH)  |  ID 2.00 m, R=3.89  |  ASME SEC VIII / TEMA'
    draw_a4_title_block(ax, 'SIEVE TRAY HYDRAULIC DESIGN & INTERNAL ASSEMBLY',
                        'JU/ChE/ED/DWG-04', scale='AS NOTED', date='17 / 11 / 2026', sub_info=SUB_INFO)
    
    # ═════════════════════════════════════════════════════════════════════════
    # VIEW A: TOP PLAN VIEW OF SINGLE-PASS SIEVE TRAY (SCALE 1:35)
    # ═════════════════════════════════════════════════════════════════════════
    CX_A, CY_A = 5.2, 13.6
    R_TRAY = 2.75   # Radius representing 1000 mm real -> Scale ~1:36
    
    cad_text(ax, CX_A, CY_A + R_TRAY + 0.85, 'VIEW A: SINGLE-PASS SIEVE TRAY PLAN VIEW', sz=5.5, bold=True)
    cad_text(ax, CX_A, CY_A + R_TRAY + 0.50, 'SCALE 1:35 METRIC (COLUMN ID = 2000 mm)', sz=4.2, bold=True)
    
    # Column Shell Ring
    cad_circle(ax, CX_A, CY_A, R_TRAY + 0.12, lw=0.95, fill=False)
    cad_circle(ax, CX_A, CY_A, R_TRAY, lw=0.65, fill=True)
    # Centerlines
    cad_line(ax, CX_A - R_TRAY - 0.4, CY_A, CX_A + R_TRAY + 0.4, CY_A, lw=0.35, ls='-.')
    cad_line(ax, CX_A, CY_A - R_TRAY - 0.4, CX_A, CY_A + R_TRAY + 0.4, lw=0.35, ls='-.')
    
    # Segmental Downcomers (Left: Downcomer from tray above; Right: Downcomer to tray below)
    # Downcomer chord at width 360 mm real -> 0.99 cm canvas
    DX_IN = CX_A - R_TRAY + 0.95
    DX_OUT = CX_A + R_TRAY - 0.95
    
    # Left Downcomer Inlet Area
    y_chord = np.sqrt(max(0, R_TRAY**2 - (0.95 - R_TRAY)**2))
    cad_line(ax, DX_IN, CY_A - y_chord, DX_IN, CY_A + y_chord, lw=0.85)
    cad_hatch_rect(ax, CX_A - R_TRAY, CY_A - y_chord, DX_IN - (CX_A - R_TRAY), 2*y_chord, pitch=0.15, angle=45, lw=0.25)
    cad_text(ax, CX_A - R_TRAY + 0.45, CY_A, 'DOWNCOMER\nFROM TRAY\nABOVE', sz=3.6, bold=True)
    
    # Right Downcomer Outlet & Weir
    cad_line(ax, DX_OUT, CY_A - y_chord, DX_OUT, CY_A + y_chord, lw=1.1)  # Outlet Weir
    cad_hatch_rect(ax, DX_OUT, CY_A - y_chord, CX_A + R_TRAY - DX_OUT, 2*y_chord, pitch=0.15, angle=-45, lw=0.25)
    cad_text(ax, CX_A + R_TRAY - 0.45, CY_A, 'DOWNCOMER\nTO TRAY\nBELOW', sz=3.6, bold=True)
    
    # Calming Zones (Unperforated margins: 50 mm)
    cad_line(ax, DX_IN + 0.22, CY_A - y_chord + 0.15, DX_IN + 0.22, CY_A + y_chord - 0.15, lw=0.35, ls=':')
    cad_line(ax, DX_OUT - 0.22, CY_A - y_chord + 0.15, DX_OUT - 0.22, CY_A + y_chord - 0.15, lw=0.35, ls=':')
    cad_text(ax, DX_IN + 0.12, CY_A + y_chord - 0.35, 'CALMING\nZONE', sz=3.0, bold=False, ha='left')
    cad_text(ax, DX_OUT - 0.12, CY_A + y_chord - 0.35, 'CALMING\nZONE', sz=3.0, bold=False, ha='right')
    
    # Active Perforated Bubbling Area
    for hx in np.arange(DX_IN + 0.45, DX_OUT - 0.35, 0.32):
        for hy in np.arange(CY_A - y_chord + 0.35, CY_A + y_chord - 0.35, 0.32):
            if (hx - CX_A)**2 + (hy - CY_A)**2 < (R_TRAY - 0.28)**2:
                cad_circle(ax, hx, hy, 0.04, fill=True, fc='#002288', ec=BK, lw=0.2)
                
    # Liquid Crossflow Arrow
    cad_arrow(ax, DX_IN + 0.8, CY_A, DX_OUT - 0.8, CY_A, lw=1.2, color='#008800', head_scale=9)
    cad_text(ax, CX_A, CY_A + 0.40, 'SINGLE-PASS LIQUID CROSSFLOW DIRECTION', sz=4.0, bold=True, color='#008800')
    
    # Dimension Callouts for View A
    cad_dim_h(ax, DX_IN, DX_OUT, CY_A - y_chord - 0.45, 'ACTIVE LENGTH = 1280 mm', sz=3.8)
    cad_dim_v(ax, CX_A - R_TRAY - 0.45, CY_A - y_chord, CY_A + y_chord, 'WEIR LENGTH Lw = 1440 mm', sz=3.6, text_offset=0.2)
    
    # ═════════════════════════════════════════════════════════════════════════
    # VIEW B: SECTIONAL ELEVATION B-B (TRAY HYDRAULIC PHENOMENA)
    # ═════════════════════════════════════════════════════════════════════════
    CX_B, CY_B = 5.2, 6.2
    
    cad_text(ax, CX_B, CY_B + 2.5, 'VIEW B: SECTION B-B — TRAY FROTH HYDRAULICS', sz=5.5, bold=True)
    cad_text(ax, CX_B, CY_B + 2.15, 'DETAIL OF CROSSFLOW FROTH REGIME & DOWNCOMER BACKUP', sz=4.2, bold=True)
    
    # Tray Floor & Tray Spacing (Ts = 500 mm real = 2.0 cm canvas)
    Y_TRAY_N = CY_B - 1.0
    Y_TRAY_N1 = CY_B + 1.0
    cad_line(ax, CX_B - 3.4, Y_TRAY_N, CX_B + 3.4, Y_TRAY_N, lw=0.9)   # Tray N floor
    cad_line(ax, CX_B - 3.4, Y_TRAY_N1, CX_B + 3.4, Y_TRAY_N1, lw=0.9) # Tray N-1 floor
    
    # Downcomer from Tray N-1 (Left)
    cad_line(ax, CX_B - 2.5, Y_TRAY_N1, CX_B - 2.5, Y_TRAY_N + 0.35, lw=0.85)
    cad_dim_v(ax, CX_B - 2.7, Y_TRAY_N, Y_TRAY_N + 0.35, 'h_cl = 38 mm', sz=3.4, text_offset=0.15)
    
    # Outlet Weir on Tray N (Right)
    cad_line(ax, CX_B + 2.3, Y_TRAY_N, CX_B + 2.3, Y_TRAY_N + 0.50, lw=1.1)
    cad_dim_v(ax, CX_B + 2.5, Y_TRAY_N, Y_TRAY_N + 0.50, 'hw = 50 mm', sz=3.4, text_offset=0.15)
    
    # Downcomer to Tray N+1 (Right)
    cad_line(ax, CX_B + 3.0, Y_TRAY_N + 0.50, CX_B + 3.0, Y_TRAY_N - 0.75, lw=0.85)
    
    # Aerated Froth Regime (Wavy profile on Tray N)
    froth_x = np.linspace(CX_B - 2.3, CX_B + 2.2, 40)
    froth_y = Y_TRAY_N + 0.85 + 0.07 * np.sin(froth_x * 7)
    for i in range(len(froth_x) - 1):
        cad_line(ax, froth_x[i], froth_y[i], froth_x[i+1], froth_y[i+1], lw=0.6, ls='--', color='#0066cc')
    cad_text(ax, CX_B, Y_TRAY_N + 1.10, 'AERATED FROTH REGIME (hf = 135 mm)', sz=3.8, bold=True, color='#0066cc')
    
    # Liquid Head over weir (how)
    cad_line(ax, CX_B + 2.1, Y_TRAY_N + 0.65, CX_B + 2.4, Y_TRAY_N + 0.65, lw=0.5, ls=':')
    cad_dim_v(ax, CX_B + 2.8, Y_TRAY_N + 0.50, Y_TRAY_N + 0.65, 'how = 18.5 mm', sz=3.2, text_offset=0.15)
    
    # Perforations and Rising Vapor Jets
    for vx in np.arange(CX_B - 1.9, CX_B + 1.9, 0.48):
        cad_line(ax, vx - 0.05, Y_TRAY_N, vx + 0.05, Y_TRAY_N, lw=1.2, color='#ffffff')
        cad_arrow(ax, vx, Y_TRAY_N - 0.40, vx, Y_TRAY_N + 0.28, lw=0.6, color='#0033aa', head_scale=4)
        
    cad_text(ax, CX_B, Y_TRAY_N - 0.55, 'VAPOR BUBBLING JETS (uv = 1.18 m/s)', sz=3.6, bold=True, color='#0033aa')
    
    # Tray Spacing Dimension
    cad_dim_v(ax, CX_B - 3.6, Y_TRAY_N, Y_TRAY_N1, 'TRAY SPACING Ts = 500 mm', sz=3.8, text_offset=0.2)
    
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
        (PX0 + PITCH_CM * 1.5, PY0 + PITCH_CM * np.sqrt(3)/2),
        (PX0 + PITCH_CM, PY0 + PITCH_CM * np.sqrt(3))
    ]
    
    # Draw connecting pitch triangle
    t_poly = [(PX0, PY0), (PX0 + PITCH_CM, PY0), (PX0 + PITCH_CM/2, PY0 + PITCH_CM * np.sqrt(3)/2)]
    ax.add_patch(Polygon(t_poly, closed=True, fc='#e6f0fa', ec='#0033aa', lw=0.75, ls='--', zorder=3))
    
    for px, py in pts:
        cad_circle(ax, px, py, 0.24, fill=True, fc='white', ec=BK, lw=0.85, zorder=4)
        cad_line(ax, px - 0.32, py, px + 0.32, py, lw=0.35, ls='-.', zorder=5)
        cad_line(ax, px, py - 0.32, px, py + 0.32, lw=0.35, ls='-.', zorder=5)
        
    # Pitch dimensions
    cad_dim_h(ax, PX0, PX0 + PITCH_CM, PY0 - 0.45, 'PITCH p = 15.0 mm', sz=3.8)
    cad_dim_v(ax, PX0 + PITCH_CM + 0.45, PY0, PY0 + PITCH_CM * np.sqrt(3)/2, 'p*sin(60)', sz=3.2, text_offset=0.15)
    
    # Hole diameter callout
    cad_line(ax, PX0, PY0, PX0 - 0.70, PY0 + 0.70, lw=0.55)
    cad_line(ax, PX0 - 0.70, PY0 + 0.70, PX0 - 1.40, PY0 + 0.70, lw=0.55)
    cad_text(ax, PX0 - 1.45, PY0 + 0.75, 'HOLE DIA dh = 5.0 mm\nSA-240 316L DECK (3 mm)', sz=3.6, bold=True, ha='right')
    
    # Pitch geometry notes
    cad_text(ax, RX_BASE + 9.4, 15.10, 'GEOMETRIC RELATIONSHIPS:\n- Equilateral Triangular Pitch (30 deg)\n- Fractional Hole Area Ah / Aa = 10.1 %\n- Ah / Aa = 0.907 * (dh / p)^2 = 0.1008\n- Hole Velocity uh = 11.7 m/s\n- Total Holes: ~12,600 per Sieve Tray', sz=3.6, bold=False, ha='left')
    
    # ═════════════════════════════════════════════════════════════════════════
    # RIGHT HALF: HYDRAULIC DESIGN TABLES
    # ═════════════════════════════════════════════════════════════════════════
    # 1. Tray Geometry Table
    t1_headers = ['PARAMETER', 'VALUE', 'UNIT', 'DESIGN CRITERIA / FORMULA']
    t1_rows = [
        ['Column Inside Diameter (Dc)', '2000 (2.00)', 'mm (m)', 'Uniform cross-section sized for capacity'],
        ['Tray Spacing (Ts)', '500', 'mm', 'Standard access spacing for maintenance'],
        ['Total Column Area (Ac)', '3.142', 'm2', 'Ac = (pi / 4) * Dc^2'],
        ['Downcomer Area (Ad)', '0.345 (11.0%)', 'm2', 'Sized for liquid deaeration and residence'],
        ['Active Bubbling Area (Aa)', '2.452 (78.0%)', 'm2', 'Aa = Ac - 2*Ad (Active crossflow zone)'],
        ['Weir Length (Lw)', '1440 (0.72 Dc)', 'mm', 'Chord length of segmental downcomer'],
        ['Outlet Weir Height (hw)', '50', 'mm', 'Maintains steady froth pool across tray deck'],
        ['Downcomer Clearance (hcl)', '38', 'mm', 'Positive liquid seal below outlet weir'],
        ['Perforation Diameter (dh)', '5.0', 'mm', 'Punched stainless steel circular orifices'],
        ['Perforation Pitch (p)', '15.0', 'mm', 'Equilateral triangular arrangement (30 deg)'],
        ['Total Hole Area (Ah)', '0.247 (10.1%)', 'm2', 'Ah / Aa = 10.08 % open area ratio'],
    ]
    t1_col_w = [4.2, 2.2, 1.4, 5.8]
    cad_draw_table_a4(ax, RX_BASE, 7.85, t1_headers, t1_rows, t1_col_w,
                      row_h=0.33, title='TABLE 1: SIEVE TRAY MECHANICAL GEOMETRY & ACTIVE AREA DETAILS',
                      title_sz=4.6, sz=3.8)
    
    # 2. Hydraulic Performance & Flooding Check Table
    t2_headers = ['HYDRAULIC METRIC', 'RECTIFYING', 'STRIPPING', 'LIMIT / STANDARD']
    t2_rows = [
        ['Max Vapor Flow, V (kg/h)', '29,313', '29,556', 'Overhead & stripping vapor loads'],
        ['Max Liquid Flow, L (kg/h)', '23,313', '35,556', 'Internal reflux & liquid descending'],
        ['Superficial Velocity, uv (m/s)', '1.18', '1.15', 'Operating gas velocity through column'],
        ['Flooding Velocity, uf (m/s)', '1.65', '1.62', 'Fair flooding correlation (Csb = 0.086)'],
        ['Percent Flooding (%)', '71.5 %', '71.0 %', 'Allowable: 65% - 75% max (Stable operation)'],
        ['Dry Tray Drop, hd (Pa)', '245 Pa', '242 Pa', 'Orifice coefficient Co = 0.73'],
        ['Total Tray Drop, ht (Pa)', '580 Pa', '610 Pa', 'Well within 700 Pa allowable tray DP'],
        ['Downcomer Backup, hdc (mm)', '195 mm', '215 mm', '< 50% tray spacing (250 mm design limit)'],
        ['Weeping Velocity, uw (m/s)', '6.2 m/s', '6.0 m/s', 'Operating uh = 11.7 m/s (Zero weeping)'],
        ['Downcomer Residence (s)', '6.2 s', '5.8 s', '> 5.0 s minimum for vapour deaeration'],
    ]
    t2_col_w = [4.2, 2.3, 2.3, 4.8]
    cad_draw_table_a4(ax, RX_BASE, 3.80, t2_headers, t2_rows, t2_col_w,
                      row_h=0.33, title='TABLE 2: HYDRAULIC OPERATING WINDOW & FLOODING VALIDATION',
                      title_sz=4.6, sz=3.8)
    
    # Save Outputs
    fig.savefig(out_pdf, format='pdf', dpi=300)
    fig.savefig(out_png, format='png', dpi=300)
    plt.close(fig)
    print(f"  [OK] DWG-04 generated: {os.path.basename(out_pdf)}")

if __name__ == '__main__':
    out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Acetaldehyde_PropyleneOxide_Distillation_Drawings')
    os.makedirs(out_dir, exist_ok=True)
    generate_acetaldehyde_dwg04(
        os.path.join(out_dir, '04_Acetaldehyde_Sieve_Tray_Assembly_Hydraulic_Details_CAD.pdf'),
        os.path.join(out_dir, '04_Acetaldehyde_Sieve_Tray_Assembly_Hydraulic_Details_CAD.png')
    )
