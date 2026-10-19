"""
A4 OPTIMIZED: DWG-04 MECHANICAL FABRICATION, NOZZLE & MANWAY DETAILS CAD
PACKED-BED ABSORBER (C-101) — 750 mm ID x 4500 mm BED
STUDENT: SOURISH SENAPATI | ROLL NO.: 002310301035 | DATE: 29/09/2026
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
    cad_dim_h, cad_dim_v, cad_dim_leader, cad_balloon, cad_flange,
    cad_hatch_rect, cad_draw_table_a4, W, H, BK, GREY
)

def generate_a4_dwg04(out_pdf, out_png):
    fig, ax = create_a4_canvas()
    draw_a4_border(ax)
    
    # ── 4 Main Mechanical Detail Panels ──────────────────────────────────────
    # Detail 1: Vessel Shell Butt Weld & Liner (Top-Left: X = 0.8 to 10.0, Y = 11.8 to 20.2)
    # Detail 2: Nozzle N1 Shell Penetration & Repad (Top-Center: X = 10.4 to 19.6, Y = 11.8 to 20.2)
    # Detail 3: Access Manway DN450 & Davit Arm (Btm-Left: X = 0.8 to 10.0, Y = 3.4 to 11.4)
    # Detail 4: Lifting Lug & Grounding Boss (Btm-Center: X = 10.4 to 19.6, Y = 3.4 to 11.4)
    # Right Side: Tables & Engineering Notes (X = 20.0 to 28.9, Y = 3.4 to 20.2)
    
    # ─────────────────────────────────────────────────────────────────────────
    # DETAIL 1: VESSEL SHELL BUTT WELD & CORROSION BARRIER LINER
    # ─────────────────────────────────────────────────────────────────────────
    cad_rect(ax, 0.8, 11.8, 9.2, 8.4, lw=0.9, fill=True)
    cad_text(ax, 5.4, 19.8, 'DETAIL 1 — ASME SEC VIII SHELL WELD & LINER', sz=5.5, bold=True)
    cad_text(ax, 5.4, 19.35, 'TYPE 1 BUTT WELD & 3 mm PVDF LINER — SCALE 1:4', sz=4.4, bold=True)
    
    CX_1 = 5.4
    CY_1 = 15.8
    t_cs = 1.4   # Carbon steel 8 mm scaled
    t_ln = 0.5   # PVDF liner 3 mm scaled
    
    # Left Steel Plate (SA-516 Gr 70)
    p_lcs = [(CX_1 - 3.6, CY_1 - t_cs/2), (CX_1 - 0.25, CY_1 - t_cs/2),
             (CX_1 - 0.1, CY_1), (CX_1 - 0.38, CY_1 + t_cs/2),
             (CX_1 - 3.6, CY_1 + t_cs/2)]
    ax.add_patch(Polygon(p_lcs, closed=True, fc='white', ec=BK, lw=1.0))
    cad_hatch_rect(ax, CX_1 - 3.6, CY_1 - t_cs/2, 3.2, t_cs, pitch=0.18, angle=45, lw=0.3)
    
    # Right Steel Plate (SA-516 Gr 70)
    p_rcs = [(CX_1 + 3.6, CY_1 - t_cs/2), (CX_1 + 0.25, CY_1 - t_cs/2),
             (CX_1 + 0.1, CY_1), (CX_1 + 0.38, CY_1 + t_cs/2),
             (CX_1 + 3.6, CY_1 + t_cs/2)]
    ax.add_patch(Polygon(p_rcs, closed=True, fc='white', ec=BK, lw=1.0))
    cad_hatch_rect(ax, CX_1 + 0.42, CY_1 - t_cs/2, 3.18, t_cs, pitch=0.18, angle=45, lw=0.3)
    
    # Weld Seam Metal (Double-V Butt Weld)
    p_wld = [(CX_1 - 0.38, CY_1 + t_cs/2), (CX_1 - 0.1, CY_1),
             (CX_1 - 0.25, CY_1 - t_cs/2), (CX_1 + 0.25, CY_1 - t_cs/2),
             (CX_1 + 0.1, CY_1), (CX_1 + 0.38, CY_1 + t_cs/2)]
    ax.add_patch(Polygon(p_wld, closed=True, fc='white', ec=BK, lw=0.9))
    cad_hatch_rect(ax, CX_1 - 0.35, CY_1 - t_cs/2, 0.70, t_cs, pitch=0.10, angle=-45, lw=0.3)
    
    # PVDF Corrosion Barrier Liner on Wetted Face (Top)
    y_ln_b = CY_1 + t_cs/2
    cad_rect(ax, CX_1 - 3.6, y_ln_b, 7.2, t_ln, lw=1.0, fill=True)
    cad_rect(ax, CX_1 - 0.6, y_ln_b + t_ln - 0.08, 1.2, 0.22, lw=0.8, fill=True) # Cap strip
    cad_text(ax, CX_1, y_ln_b + t_ln + 0.35, 'PVDF CAP STRIP (15 kV SPARK TESTED)', sz=3.6, bold=True)
    
    # Clean Uncluttered Callouts Below Assembly (Zero text over hatching)
    cad_line(ax, CX_1 - 2.2, CY_1 - t_cs/2, CX_1 - 2.2, CY_1 - t_cs/2 - 0.55, lw=0.45)
    cad_circle(ax, CX_1 - 2.2, CY_1 - t_cs/2 + 0.15, 0.05, fill=True)
    cad_text(ax, CX_1 - 2.2, CY_1 - t_cs/2 - 0.80, 'BASE SHELL: SA-516 GR 70\n(t = 8 mm CAD)', sz=3.4, bold=True)
    
    cad_line(ax, CX_1, CY_1 - t_cs/2, CX_1, CY_1 - t_cs/2 - 1.45, lw=0.45)
    cad_circle(ax, CX_1, CY_1 - t_cs/2 + 0.15, 0.05, fill=True)
    cad_text(ax, CX_1, CY_1 - t_cs/2 - 1.75, 'DOUBLE-V FULL-PEN BUTT WELD\n100% RADIOGRAPHY (UW-11, E = 1.0)', sz=3.5, bold=True)
    
    cad_line(ax, CX_1 + 2.2, y_ln_b + t_ln/2, CX_1 + 2.2, CY_1 - t_cs/2 - 0.55, lw=0.45)
    cad_circle(ax, CX_1 + 2.2, y_ln_b + t_ln/2, 0.05, fill=True)
    cad_text(ax, CX_1 + 2.2, CY_1 - t_cs/2 - 0.80, '3.0 mm BONDED PVDF LINER\nCORROSION BARRIER (WET Br2)', sz=3.4, bold=True)
    
    # Left Dimensions (Well inside left margin)
    cad_dim_v(ax, CX_1 - 3.9, CY_1 - t_cs/2, CY_1 + t_cs/2, '8 mm', text_offset=-0.22, sz=4.0)
    cad_dim_v(ax, CX_1 - 3.9, y_ln_b, y_ln_b + t_ln, '3 mm', text_offset=-0.22, sz=4.0)
    
    # ─────────────────────────────────────────────────────────────────────────
    # DETAIL 2: NOZZLE N1 (DN150) PENETRATION & REINFORCING PAD
    # ─────────────────────────────────────────────────────────────────────────
    cad_rect(ax, 10.4, 11.8, 9.2, 8.4, lw=0.9, fill=True)
    cad_text(ax, 15.0, 19.8, 'DETAIL 2 — NOZZLE N1 (DN150) & REPAD', sz=5.5, bold=True)
    cad_text(ax, 15.0, 19.35, 'ASME B16.5 WELD NECK & UG-37 REPAD — 1:10', sz=4.4, bold=True)
    
    CX_2 = 14.8
    CY_2 = 15.4
    
    # Shell wall (Horizontal plate)
    y_sh_b = CY_2 - 2.2
    cad_rect(ax, 11.2, y_sh_b, 7.2, 0.32, lw=1.0, fill=True)
    cad_text(ax, CX_2, y_sh_b - 0.42, 'SHELL WALL (ID 750 mm, t = 8 mm)', sz=3.6, bold=True)
    
    # Reinforcing Pad (Repad OD 340 mm -> 3.0 cm width, Thk 8 mm -> 0.32 cm)
    w_rp = 3.0
    cad_rect(ax, CX_2 - w_rp/2, y_sh_b + 0.32, w_rp, 0.32, lw=0.9, fill=True)
    
    # Telltale Weep Hole & Clean Non-Overflow Leader
    x_wh = CX_2 + 1.1
    y_wh = y_sh_b + 0.48
    cad_circle(ax, x_wh, y_wh, 0.06, fill=True)
    # Leader angled cleanly inside the panel (Knee at 16.5, line to 17.0, text ha='left' terminates at 18.5)
    cad_line(ax, x_wh, y_wh, 16.5, y_sh_b + 1.15, lw=0.45)
    cad_line(ax, 16.5, y_sh_b + 1.15, 16.9, y_sh_b + 1.15, lw=0.45)
    cad_circle(ax, x_wh, y_wh, 0.05, fill=True)
    cad_text(ax, 17.0, y_sh_b + 1.15, '1/8" NPT WEEP HOLE', sz=3.3, bold=True, ha='left')
    
    # Nozzle Neck Pipe (DN150 / 6" Sch 40S: OD 168.3 mm -> 1.5 cm)
    w_nk = 1.5
    h_nk = 3.4
    cad_rect(ax, CX_2 - w_nk/2, y_sh_b, w_nk, h_nk, lw=0.9, fill=True)
    cad_line(ax, CX_2, y_sh_b - 0.3, CX_2, y_sh_b + h_nk + 1.1, lw=0.35, ls='-.')
    
    # Weld Neck Flange (DN150 Class 150 RF: OD 280 mm -> 2.5 cm)
    y_flg = y_sh_b + h_nk
    flg_w = 2.5
    cad_rect(ax, CX_2 - flg_w/2, y_flg, flg_w, 0.45, lw=1.0, fill=True)
    cad_rect(ax, CX_2 - 0.9, y_flg + 0.45, 1.8, 0.08, lw=0.8, fill=True) # Raised face
    
    # Clear Dimensions (Within Panel Bounds 10.4 to 19.6)
    cad_dim_h(ax, CX_2 - flg_w/2, CX_2 + flg_w/2, y_flg + 0.85, 'FLG OD 280 mm', sz=4.0)
    cad_dim_h(ax, CX_2 - w_rp/2, CX_2 + w_rp/2, y_sh_b + 0.95, 'REPAD OD 340 mm', sz=4.0)
    cad_dim_v(ax, CX_2 - flg_w/2 - 0.45, y_sh_b + 0.32, y_flg + 0.45, '250 mm', text_offset=-0.22, sz=4.0)
    
    # Nozzle Identification Balloon
    cad_balloon(ax, CX_2 - 1.8, y_sh_b + 2.0, 'N1', radius=0.32, sz=5.0)
    
    # ─────────────────────────────────────────────────────────────────────────
    # DETAIL 3: ACCESS MANWAY (DN450 / 18") & MECHANICAL DAVIT ARM
    # ─────────────────────────────────────────────────────────────────────────
    cad_rect(ax, 0.8, 3.4, 9.2, 8.0, lw=0.9, fill=True)
    cad_text(ax, 5.4, 11.0, 'DETAIL 3 — ACCESS MANWAY (DN450) & DAVIT', sz=5.5, bold=True)
    cad_text(ax, 5.4, 10.55, 'ASME B16.5 BLIND COVER & HINGED DAVIT — 1:12', sz=4.4, bold=True)
    
    CX_3 = 5.2
    CY_3 = 6.4
    x_sh = 2.6
    
    # Shell wall (Vertical)
    cad_line(ax, x_sh, CY_3 - 2.5, x_sh, CY_3 + 2.5, lw=1.0)
    # Centerline stops BEFORE the callout zone (X = 2.0 to 4.9)
    cad_line(ax, x_sh - 0.4, CY_3, x_sh + 2.4, CY_3, lw=0.35, ls='-.')
    
    # Manway neck (ID 450 mm -> 2.4 cm)
    cad_rect(ax, x_sh, CY_3 - 1.2, 1.3, 2.4, lw=0.9, fill=True)
    # Flange & Blind Cover (OD 635 mm -> 3.4 cm)
    x_mf = x_sh + 1.3
    cad_rect(ax, x_mf, CY_3 - 1.7, 0.28, 3.4, lw=0.9, fill=True) # Flange
    x_bc = x_mf + 0.32
    cad_rect(ax, x_bc, CY_3 - 1.7, 0.28, 3.4, lw=0.9, fill=True) # Blind Cover
    # Stud Bolts
    for by in [CY_3 - 1.4, CY_3 + 1.4]:
        cad_line(ax, x_mf - 0.15, by, x_bc + 0.45, by, lw=0.85)
    
    # Davit Arm (Swinging Hinge Post)
    cad_line(ax, x_sh + 0.18, CY_3 + 1.5, x_sh + 0.18, CY_3 + 2.5, lw=1.1) # Post
    cad_line(ax, x_sh + 0.18, CY_3 + 2.5, x_bc + 0.15, CY_3 + 2.5, lw=1.1) # Arm
    cad_line(ax, x_bc + 0.15, CY_3 + 2.5, x_bc + 0.15, CY_3 + 1.6, lw=0.8) # Hanger
    cad_text(ax, x_sh + 1.6, CY_3 + 2.78, 'MECHANICAL HINGED DAVIT ARM', sz=3.6, bold=True)
    
    # Clean Callouts (Placed neatly to the right of blind cover with leaders)
    tx_m = 5.7
    cad_text(ax, tx_m, CY_3 + 0.65, 'BLIND FLANGE COVER (85 kg)', sz=3.4, bold=True, ha='left')
    cad_line(ax, tx_m - 0.1, CY_3 + 0.65, x_bc + 0.28, CY_3 + 0.65, lw=0.45)
    
    cad_text(ax, tx_m, CY_3 + 0.15, '16x 1-1/8" SA-193 B7 STUDS', sz=3.4, bold=True, ha='left')
    cad_line(ax, tx_m - 0.1, CY_3 + 0.15, x_bc + 0.45, CY_3 + 1.4, lw=0.45)
    
    cad_text(ax, tx_m, CY_3 - 0.35, 'PTFE SPIRAL-WOUND GASKET', sz=3.4, bold=True, ha='left')
    cad_line(ax, tx_m - 0.1, CY_3 - 0.35, x_mf + 0.28, CY_3 - 0.35, lw=0.45)
    
    cad_text(ax, tx_m, CY_3 - 0.85, 'ASME B16.5 CLASS 150 RF', sz=3.4, bold=True, ha='left')
    
    # ID 450 mm Dimension on Left
    cad_dim_v(ax, x_sh - 0.45, CY_3 - 1.2, CY_3 + 1.2, 'ID 450 mm', text_offset=-0.22, sz=4.0)
    
    # ─────────────────────────────────────────────────────────────────────────
    # DETAIL 4: TOP LIFTING LUG & GROUNDING BOSS DETAILS
    # ─────────────────────────────────────────────────────────────────────────
    cad_rect(ax, 10.4, 3.4, 9.2, 8.0, lw=0.9, fill=True)
    cad_text(ax, 15.0, 11.0, 'DETAIL 4 — LIFTING LUG & EARTHING BOSS', sz=5.5, bold=True)
    cad_text(ax, 15.0, 10.55, 'RIGGING PADEYE (5.0 t SWL — PRELIM) & GROUNDING — 1:10', sz=4.4, bold=True)
    
    # Sub-Detail 4A: Top Rigging Padeye (Lifting Lug) on Left
    CX_L = 12.8
    CY_L = 5.8
    cad_arc(ax, CX_L, CY_L - 0.9, 4.0, 1.0, theta1=0, theta2=180, lw=1.0) # Vessel head curve
    cad_rect(ax, CX_L - 0.65, CY_L - 0.4, 1.3, 1.5, lw=0.9, fill=True) # Lug base
    cad_arc(ax, CX_L, CY_L + 1.1, 1.3, 1.3, theta1=0, theta2=180, lw=0.9) # Rounded top
    cad_circle(ax, CX_L, CY_L + 0.8, 0.25, lw=0.8, fill=True) # Shackle pin hole
    cad_circle(ax, CX_L, CY_L + 0.8, 0.42, lw=0.5, ls='--') # Cheek reinforcing doubler
    
    cad_text(ax, CX_L, CY_L + 2.2, 'LIFTING LUG (5.0 t SWL — PRELIM)', sz=3.5, bold=True)
    cad_text(ax, CX_L, CY_L + 1.8, 'SA-516 GR 70 (t = 20 mm)', sz=3.4, bold=True)
    cad_text(ax, CX_L, CY_L - 1.4, 'TOP HEAD WELDED PADEYE', sz=3.4, bold=True)
    
    # Sub-Detail 4B: Earthing / Grounding Boss on Right
    CX_G = 16.6
    CY_G = 6.4
    # Skirt Wall Plate
    cad_rect(ax, CX_G - 0.15, CY_G - 1.0, 0.22, 2.0, lw=0.9, fill=True)
    # Copper Grounding Boss Welded to Skirt
    cad_rect(ax, CX_G + 0.07, CY_G - 0.35, 0.45, 0.70, lw=0.8, fill=True)
    cad_circle(ax, CX_G + 0.30, CY_G, 0.08, fill=True) # M12 tapped hole
    # Grounding Cable Terminal & Symbol
    cad_line(ax, CX_G + 0.30, CY_G, CX_G + 1.1, CY_G, lw=0.8)
    cad_circle(ax, CX_G + 1.1, CY_G, 0.12, fill=True)
    # Earth symbol lines
    cad_line(ax, CX_G + 1.1, CY_G - 0.15, CX_G + 1.1, CY_G - 0.45, lw=0.7)
    cad_line(ax, CX_G + 0.95, CY_G - 0.45, CX_G + 1.25, CY_G - 0.45, lw=0.8)
    cad_line(ax, CX_G + 1.00, CY_G - 0.53, CX_G + 1.20, CY_G - 0.53, lw=0.7)
    cad_line(ax, CX_G + 1.05, CY_G - 0.61, CX_G + 1.15, CY_G - 0.61, lw=0.6)
    
    # Clean Callouts COMPLETELY BELOW the Plate (Zero collision with skirt!)
    cad_text(ax, CX_G + 0.5, CY_G - 1.4, 'VESSEL EARTHING BOSS', sz=3.6, bold=True)
    cad_text(ax, CX_G + 0.5, CY_G - 1.8, 'M12 SS BOLT (<1.0 OHM)', sz=3.4, bold=True)
    cad_text(ax, CX_G + 0.5, CY_G - 2.2, 'WELDED TO SKIRT BASE', sz=3.3, bold=True)
    
    # ═════════════════════════════════════════════════════════════════════════
    # RIGHT SIDE: TABLES & FABRICATION SPECIFICATIONS (X = 20.0 to 28.9)
    # ═════════════════════════════════════════════════════════════════════════
    # Total available width = 28.9 - 20.0 = 8.9 cm EXACTLY
    
    # TABLE 1: MASTER ASME B16.5 NOZZLE SCHEDULE (Width = 8.9 cm)
    T1_X = 20.0
    T1_Y = 11.2
    t1_headers = ['NOZ', 'SERVICE', 'SIZE', 'FLG OD', 'REPAD']
    t1_widths  = [1.0, 3.4, 1.5, 1.5, 1.5]  # Sum = 8.9 cm
    t1_rows = [
        ['N1', 'Feed Gas Inlet',    'DN 150', '280 mm', 'DIA 340 mm'],
        ['N3', 'Water Scrub Inlet', 'DN 80',  '190 mm', 'DIA 190 mm'],
        ['N4', 'Rich Liquor Outlet','DN 80',  '190 mm', 'Integral'],
        ['N5', 'Shell Bottom Drain','DN 40',  '127 mm', 'None'],
        ['N6', 'Treated Gas Vent',  'DN 50',  '152 mm', 'None'],
        ['M1', 'Lower Access Manway','DN 450','635 mm', 'DIA 750 mm'],
        ['M2', 'Upper Access Manway','DN 450','635 mm', 'DIA 750 mm'],
    ]
    cad_draw_table_a4(ax, T1_X, T1_Y, t1_headers, t1_rows, t1_widths, row_h=0.38,
                      title='TABLE 1 — NOZZLE SCHEDULE & REPADS', sz=4.2)
    
    # TABLE 2: WELDING PROCEDURE & NDE TABLE (Width = 8.9 cm)
    T2_X = 20.0
    T2_Y = 7.3
    t2_headers = ['JOINT', 'LOCATION', 'WELD TYPE', 'NDE METHOD']
    t2_widths  = [1.3, 3.2, 2.2, 2.2]  # Sum = 8.9 cm
    t2_rows = [
        ['Cat. A', 'Longitudinal Shell', 'Double-V Butt', '100% Radiography (RT)'],
        ['Cat. B', 'Girth Seams',        'Double-V Butt', '100% Radiography (RT)'],
        ['Cat. C', 'Flange Hubs',        'Full Pen Hub',  '100% Dye Penetrant'],
        ['Cat. D', 'Nozzle Necks',       'Set-Through',   '100% PT + Ultrasonic'],
        ['Repad',  'Reinforcing Pads',   'Continuous',    'Air Leak Test (1.5 bar)'],
        ['Liner',  'PVDF Membrane',      'Thermal Cap',   '15 kV Spark Testing'],
    ]
    cad_draw_table_a4(ax, T2_X, T2_Y, t2_headers, t2_rows, t2_widths, row_h=0.38,
                      title='TABLE 2 — WELDING & NDE SCHEDULE', sz=4.2)
    
    # FABRICATION NOTES (Width = 8.9 cm)
    N_X = 20.0
    N_Y = 3.4
    W_N = 8.9
    H_N = 3.5
    cad_rect(ax, N_X, N_Y, W_N, H_N, lw=0.9, fill=True)
    cad_text(ax, N_X + W_N/2, N_Y + H_N - 0.28, 'PRESSURE VESSEL FABRICATION NOTES', sz=4.8, bold=True)
    cad_line(ax, N_X, N_Y + H_N - 0.52, N_X + W_N, N_Y + H_N - 0.52, lw=0.6)
    
    notes_dwg4 = [
        "1. CODE JURISDICTION: PRELIMINARY DESIGN PER ASME SEC VIII DIV 1.",
        "2. LINING: 3 mm SOLID PVDF TESTED AT 15 kV (NACE SP0188).",
        "3. HYDROSTATIC TEST PRESSURE: AS PER ASME VIII DIV. 1 (CHLORIDE-FREE DM WATER).",
    ]
    for idx, nl in enumerate(notes_dwg4):
        cad_text(ax, N_X + 0.35, N_Y + H_N - 1.05 - idx * 0.65, nl, sz=3.8, ha='left', bold=True)
    
    # Title Block
    draw_a4_title_block(
        ax,
        dwg_title='PACKED-BED ABSORBER (C-101) — MECHANICAL FABRICATION DETAILS CAD',
        dwg_no='PEDD-PBA-04',
        scale='DETAILED 1:4, 1:10 METRIC'
    )
    
    fig.savefig(out_pdf, dpi=300, facecolor='white')
    fig.savefig(out_png, dpi=300, facecolor='white')
    plt.close(fig)
    print(f"SUCCESS: Clean A4 DWG-04 generated at {out_pdf}")

if __name__ == '__main__':
    out_dir = r'd:\GAMES\zercxes\CAD_Engineering_Drawings\Packed_Bed_Absorber_Drawings'
    os.makedirs(out_dir, exist_ok=True)
    p_pdf = os.path.join(out_dir, '04_Packed_Bed_Absorber_Nozzle_Manway_Details_CAD.pdf')
    p_png = os.path.join(out_dir, '04_Packed_Bed_Absorber_Nozzle_Manway_Details_CAD.png')
    generate_a4_dwg04(p_pdf, p_png)
