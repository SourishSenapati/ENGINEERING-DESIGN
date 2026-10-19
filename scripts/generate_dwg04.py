"""
DWG-04: MECHANICAL FABRICATION, NOZZLE & MANWAY DETAILS CAD
PACKED-BED ABSORBER (C-101) — 750 MM ID x 4500 MM RASCHIG RING BED
STUDENT: SOURISH SENAPATI | ROLL: 002310301035 | DATE: 29/09/2026
SUBJECT: PROCESS EQUIPMENT DESIGN & DRAWING | JADAVPUR UNIVERSITY
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon, Arc
from cad_common import (
    create_cad_canvas, draw_sheet_border, draw_title_block,
    cad_line, cad_rect, cad_circle, cad_arc, cad_text, cad_arrow,
    cad_dim_h, cad_dim_v, cad_dim_leader, cad_balloon, cad_flange,
    cad_hatch_rect, cad_draw_table, W, H, BK, GREY
)

def generate_dwg04():
    fig, ax = create_cad_canvas()
    draw_sheet_border(ax)
    
    # ═════════════════════════════════════════════════════════════════════════
    # SHEET LAYOUT: 4 MECHANICAL FABRICATION & COMPONENT CAD DETAILS
    # Detail 1: Vessel Shell Butt Weld & Liner (Top-Left: X = 2.5 to 26.5, Y = 28.5 to 52.0)
    # Detail 2: Nozzle N1 Shell Penetration & Repad (Top-Right: X = 28.0 to 52.0, Y = 28.5 to 52.0)
    # Detail 3: Access Manway DN450 & Davit Arm (Btm-Left: X = 2.5 to 26.5, Y = 7.2 to 27.0)
    # Detail 4: Lifting Lug & Grounding Boss Details (Btm-Right: X = 28.0 to 52.0, Y = 7.2 to 27.0)
    # Right Panel: Master ASME B16.5 Nozzle Table & WPS (X = 53.5 to 81.5, Y = 7.2 to 52.0)
    # ═════════════════════════════════════════════════════════════════════════
    
    # ─────────────────────────────────────────────────────────────────────────
    # DETAIL 1: VESSEL SHELL BUTT WELD & CORROSION BARRIER LINER
    # ─────────────────────────────────────────────────────────────────────────
    D1_X, D1_Y, D1_W, D1_H = 2.5, 29.0, 24.5, 23.5
    cad_rect(ax, D1_X, D1_Y, D1_W, D1_H, lw=1.2, fill=True)
    cad_text(ax, D1_X + D1_W/2, D1_Y + D1_H - 0.7,
             'DETAIL 1 — ASME SEC VIII DIV 1 SHELL BUTT WELD & LINER', sz=7.8, bold=True)
    cad_text(ax, D1_X + D1_W/2, D1_Y + D1_H - 1.4,
             'TYPE 1 FULL-PENETRATION DOUBLE-WELDED JOINT & PVDF BARRIER (SCALE 1:2 METRIC)', sz=5.5, bold=True)
    
    CX_D1 = D1_X + 12.25
    CY_D1 = D1_Y + 12.0
    
    # Plate thickness: Carbon steel t = 8 mm -> drawn 3.2 cm for 1:2 scale clarity
    # Liner thickness: PVDF t = 3 mm -> drawn 1.2 cm
    t_cs = 3.2
    t_liner = 1.2
    
    # Left Steel Plate (SA-516 Gr 70)
    p_left_cs = [
        (CX_D1 - 9.0, CY_D1 - t_cs/2), (CX_D1 - 0.6, CY_D1 - t_cs/2),
        (CX_D1 - 0.2, CY_D1), (CX_D1 - 0.9, CY_D1 + t_cs/2),
        (CX_D1 - 9.0, CY_D1 + t_cs/2)
    ]
    ax.add_patch(Polygon(p_left_cs, closed=True, fc='white', ec=BK, lw=1.2))
    cad_hatch_rect(ax, CX_D1 - 9.0, CY_D1 - t_cs/2, 8.0, t_cs, pitch=0.35, angle=45, lw=0.4)
    
    # Right Steel Plate (SA-516 Gr 70)
    p_right_cs = [
        (CX_D1 + 9.0, CY_D1 - t_cs/2), (CX_D1 + 0.6, CY_D1 - t_cs/2),
        (CX_D1 + 0.2, CY_D1), (CX_D1 + 0.9, CY_D1 + t_cs/2),
        (CX_D1 + 9.0, CY_D1 + t_cs/2)
    ]
    ax.add_patch(Polygon(p_right_cs, closed=True, fc='white', ec=BK, lw=1.2))
    cad_hatch_rect(ax, CX_D1 + 1.0, CY_D1 - t_cs/2, 8.0, t_cs, pitch=0.35, angle=45, lw=0.4)
    
    # Weld Seam Metal (Double-V / Root + Fill Passes)
    p_weld = [
        (CX_D1 - 0.9, CY_D1 + t_cs/2), (CX_D1 - 0.2, CY_D1),
        (CX_D1 - 0.6, CY_D1 - t_cs/2), (CX_D1 + 0.6, CY_D1 - t_cs/2),
        (CX_D1 + 0.2, CY_D1), (CX_D1 + 0.9, CY_D1 + t_cs/2)
    ]
    ax.add_patch(Polygon(p_weld, closed=True, fc='white', ec=BK, lw=1.1))
    cad_hatch_rect(ax, CX_D1 - 0.8, CY_D1 - t_cs/2, 1.6, t_cs, pitch=0.15, angle=-45, lw=0.4)
    # Weld Caps (Top and Bottom reinforcement <= 1.5 mm)
    cad_arc(ax, CX_D1, CY_D1 + t_cs/2, 2.0, 0.45, theta1=0, theta2=180, lw=1.0)
    cad_arc(ax, CX_D1, CY_D1 - t_cs/2, 1.6, 0.40, theta1=180, theta2=360, lw=1.0)
    
    # Corrosion Barrier Liner (Solid PVDF / Titanium Clad on Process Wetted Face: Top)
    y_liner_btm = CY_D1 + t_cs/2
    y_liner_top = y_liner_btm + t_liner
    cad_rect(ax, CX_D1 - 9.0, y_liner_btm, 18.0, t_liner, lw=1.2, fill=True)
    cad_hatch_rect(ax, CX_D1 - 9.0, y_liner_btm, 18.0, t_liner, pitch=0.20, angle=0, lw=0.35, color=GREY)
    # Thermo-welded PVDF Cap Strip over weld seam
    cad_rect(ax, CX_D1 - 1.2, y_liner_top - 0.2, 2.4, 0.55, lw=1.0, fill=True)
    cad_text(ax, CX_D1, y_liner_top + 0.9, 'THERMO-WELDED PVDF CAP STRIP\n(SPARK TESTED AT 15 kV)', sz=4.8, bold=True)
    
    # Annotations & Leaders
    cad_text(ax, CX_D1 - 5.0, CY_D1, 'BASE METAL:\nSA-516 GR. 70\n(t = 8 mm CAD)', sz=5.0, bold=True, bg='white')
    cad_text(ax, CX_D1 + 5.0, CY_D1, 'WELD SPECIFICATION:\nASME SEC IX WPS-01\nGTAW ROOT + SMAW FILL', sz=5.0, bold=True, bg='white')
    cad_text(ax, CX_D1 - 5.0, y_liner_btm + t_liner/2, 'CORROSION BARRIER: 3.0 mm SOLID PVDF LINING', sz=4.8, bold=True, bg='white')
    
    # Joint Geometry Callouts
    cad_dim_v(ax, CX_D1 - 9.5, CY_D1 - t_cs/2, CY_D1 + t_cs/2, '8 mm', text_offset=-0.40)
    cad_dim_v(ax, CX_D1 - 9.5, y_liner_btm, y_liner_top, '3 mm', text_offset=-0.40)
    cad_dim_h(ax, CX_D1 - 0.2, CX_D1 + 0.2, CY_D1 - t_cs/2 - 1.2, 'ROOT GAP 2 mm')
    
    cad_text(ax, CX_D1, CY_D1 - t_cs/2 - 2.5,
             'JOINT CATEGORY A & B: 100% RADIOGRAPHIC EXAMINATION (RT-1, UW-11)\n'
             'JOINT EFFICIENCY E = 1.00 | ZERO AIR GAPS / 100% BONDED LINER', sz=5.0, bold=True)
    
    # ─────────────────────────────────────────────────────────────────────────
    # DETAIL 2: NOZZLE N1 (DN150) SHELL PENETRATION & REINFORCING PAD
    # ─────────────────────────────────────────────────────────────────────────
    D2_X, D2_Y, D2_W, D2_H = 27.5, 29.0, 24.5, 23.5
    cad_rect(ax, D2_X, D2_Y, D2_W, D2_H, lw=1.2, fill=True)
    cad_text(ax, D2_X + D2_W/2, D2_Y + D2_H - 0.7,
             'DETAIL 2 — NOZZLE N1 (DN150) PENETRATION & REINFORCING PAD', sz=7.8, bold=True)
    cad_text(ax, D2_X + D2_W/2, D2_Y + D2_H - 1.4,
             'ASME B16.5 WELD NECK FLANGE & ASME UG-37 REPAD (SCALE 1:5 METRIC)', sz=5.5, bold=True)
    
    CX_D2 = D2_X + 13.0
    CY_D2 = D2_Y + 11.5
    
    # Vessel Shell Wall (Curved / Horizontal Section)
    y_sh_btm = CY_D2 - 4.5
    y_sh_top = y_sh_btm + 0.8  # Shell thickness
    cad_rect(ax, D2_X + 1.5, y_sh_btm, D2_W - 3.0, 0.8, lw=1.2, fill=True)
    cad_hatch_rect(ax, D2_X + 1.5, y_sh_btm, D2_W - 3.0, 0.8, pitch=0.25, lw=0.35)
    cad_text(ax, D2_X + 4.5, y_sh_btm - 0.6, 'VESSEL SHELL (ID 750 mm, t = 8 mm)', sz=4.8, bold=True)
    
    # Reinforcing Pad (Repad: OD 340 mm -> Width 6.8 cm, Thickness 8 mm -> 0.8 cm)
    w_repad = 6.8
    cad_rect(ax, CX_D2 - w_repad/2, y_sh_top, w_repad, 0.8, lw=1.1, fill=True)
    cad_hatch_rect(ax, CX_D2 - w_repad/2, y_sh_top, w_repad, 0.8, pitch=0.25, angle=-45, lw=0.35)
    # Repad outer fillet welds
    cad_line(ax, CX_D2 - w_repad/2, y_sh_top + 0.8, CX_D2 - w_repad/2 - 0.6, y_sh_top, lw=1.0)
    cad_line(ax, CX_D2 + w_repad/2, y_sh_top + 0.8, CX_D2 + w_repad/2 + 0.6, y_sh_top, lw=1.0)
    
    # Telltale Weep Hole (1/8" NPT) in Repad
    cad_circle(ax, CX_D2 + 2.2, y_sh_top + 0.4, 0.15, fill=True)
    cad_dim_leader(ax, CX_D2 + 2.2, y_sh_top + 0.4, CX_D2 + 3.5, y_sh_top + 1.8, CX_D2 + 6.0,
                   '1/8" NPT TELLTALE HOLE\n(PNEUMATIC LEAK TEST & WEEP)', sz=4.5)
    
    # Nozzle Neck Pipe (DN150 / 6" Sch 40S: OD 168.3 mm, ID 154.1 mm)
    w_neck_od = 3.4  # Scaled OD
    w_neck_id = 3.0  # Scaled ID
    h_neck = 7.5
    # Neck Outer Walls
    cad_line(ax, CX_D2 - w_neck_od/2, y_sh_btm - 0.5, CX_D2 - w_neck_od/2, y_sh_top + h_neck, lw=1.2)
    cad_line(ax, CX_D2 + w_neck_od/2, y_sh_btm - 0.5, CX_D2 + w_neck_od/2, y_sh_top + h_neck, lw=1.2)
    # Neck Inner Walls
    cad_line(ax, CX_D2 - w_neck_id/2, y_sh_btm - 0.5, CX_D2 - w_neck_id/2, y_sh_top + h_neck, lw=0.8)
    cad_line(ax, CX_D2 + w_neck_id/2, y_sh_btm - 0.5, CX_D2 + w_neck_id/2, y_sh_top + h_neck, lw=0.8)
    cad_hatch_rect(ax, CX_D2 - w_neck_od/2, y_sh_btm, (w_neck_od - w_neck_id)/2, h_neck + 0.8, pitch=0.20, lw=0.35)
    cad_hatch_rect(ax, CX_D2 + w_neck_id/2, y_sh_btm, (w_neck_od - w_neck_id)/2, h_neck + 0.8, pitch=0.20, lw=0.35)
    cad_line(ax, CX_D2, y_sh_btm - 1.2, CX_D2, y_sh_top + h_neck + 2.5, lw=0.4, ls='-.')
    
    # Full Penetration Welds between Neck, Shell and Repad
    cad_line(ax, CX_D2 - w_neck_od/2, y_sh_top + 0.8, CX_D2 - w_neck_od/2 - 0.6, y_sh_top + 0.8, lw=1.0)
    cad_line(ax, CX_D2 + w_neck_od/2, y_sh_top + 0.8, CX_D2 + w_neck_od/2 + 0.6, y_sh_top + 0.8, lw=1.0)
    
    # ASME B16.5 Weld Neck Flange (DN150 Class 150 RF)
    y_flg = y_sh_top + h_neck
    flg_od = 5.6  # 280 mm OD
    flg_thk = 1.0 # 25.4 mm thk
    # Hub taper
    cad_line(ax, CX_D2 - w_neck_od/2, y_flg - 1.5, CX_D2 - flg_od/2 + 0.5, y_flg, lw=1.0)
    cad_line(ax, CX_D2 + w_neck_od/2, y_flg - 1.5, CX_D2 + flg_od/2 - 0.5, y_flg, lw=1.0)
    # Flange ring
    cad_rect(ax, CX_D2 - flg_od/2, y_flg, flg_od, flg_thk, lw=1.2, fill=True)
    # Raised Face (RF: 2 mm high, OD 216 mm -> 4.3 cm)
    rf_w = 4.3
    cad_rect(ax, CX_D2 - rf_w/2, y_flg + flg_thk, rf_w, 0.15, lw=1.0, fill=True)
    # Bolt holes (8x 22 mm holes on BC 241.3 mm)
    for bh_side in [-1, 1]:
        bh_x = CX_D2 + bh_side * 2.4
        cad_line(ax, bh_x, y_flg, bh_x, y_flg + flg_thk, lw=0.6, ls='--')
        cad_line(ax, bh_x, y_flg - 0.2, bh_x, y_flg + flg_thk + 0.2, lw=0.4, ls='-.')
    
    # Dimensions on Nozzle Detail
    cad_dim_h(ax, CX_D2 - flg_od/2, CX_D2 + flg_od/2, y_flg + flg_thk + 1.2, 'FLANGE OD 280 mm (CL 150 RF)')
    cad_dim_h(ax, CX_D2 - w_neck_od/2, CX_D2 + w_neck_od/2, y_flg - 2.2, 'NECK DN150 (OD 168.3 mm)')
    cad_dim_h(ax, CX_D2 - w_repad/2, CX_D2 + w_repad/2, y_sh_top + 2.2, 'REPAD OD 340 mm (UG-37)')
    cad_dim_v(ax, CX_D2 - flg_od/2 - 0.8, y_sh_top, y_flg + flg_thk, 'PROJECTION 250 mm', text_offset=-0.45)
    
    # ─────────────────────────────────────────────────────────────────────────
    # DETAIL 3: VESSEL ACCESS MANWAY (DN450 / 18") & MECHANICAL DAVIT ARM
    # ─────────────────────────────────────────────────────────────────────────
    D3_X, D3_Y, D3_W, D3_H = 2.5, 7.2, 24.5, 21.0
    cad_rect(ax, D3_X, D3_Y, D3_W, D3_H, lw=1.2, fill=True)
    cad_text(ax, D3_X + D3_W/2, D3_Y + D3_H - 0.7,
             'DETAIL 3 — VESSEL ACCESS MANWAY (DN450) & DAVIT ARM', sz=7.8, bold=True)
    cad_text(ax, D3_X + D3_W/2, D3_Y + D3_H - 1.4,
             'ASME B16.5 CLASS 150 BLIND COVER, SPIRAL GASKET & HINGED DAVIT (SCALE 1:6)', sz=5.5, bold=True)
    
    CX_D3 = D3_X + 11.5
    CY_D3 = D3_Y + 11.0
    
    # Vessel Shell Wall (Vertical)
    x_mw_sh = CX_D3 - 5.5
    cad_line(ax, x_mw_sh, CY_D3 - 8.0, x_mw_sh, CY_D3 + 8.0, lw=1.2)
    cad_line(ax, x_mw_sh - 0.35, CY_D3 - 8.0, x_mw_sh - 0.35, CY_D3 + 8.0, lw=0.6)
    cad_hatch_rect(ax, x_mw_sh - 0.35, CY_D3 - 8.0, 0.35, 16.0, pitch=0.20, lw=0.35)
    cad_line(ax, x_mw_sh - 1.5, CY_D3, x_mw_sh + 12.0, CY_D3, lw=0.4, ls='-.') # Centerline
    
    # Manway Neck (ID 450 mm -> 5.4 cm, Length 250 mm -> 3.0 cm)
    mw_id = 5.4
    mw_od = 6.0
    mw_len = 3.2
    cad_rect(ax, x_mw_sh, CY_D3 - mw_od/2, mw_len, (mw_od - mw_id)/2, lw=1.1, fill=True)
    cad_rect(ax, x_mw_sh, CY_D3 + mw_id/2, mw_len, (mw_od - mw_id)/2, lw=1.1, fill=True)
    cad_hatch_rect(ax, x_mw_sh, CY_D3 - mw_od/2, mw_len, (mw_od - mw_id)/2, pitch=0.20, lw=0.35)
    cad_hatch_rect(ax, x_mw_sh, CY_D3 + mw_id/2, mw_len, (mw_od - mw_id)/2, pitch=0.20, lw=0.35)
    
    # Manway Hub Flange (DN450 Class 150 RF: OD 635 mm -> 7.6 cm, Thk 40 mm -> 0.65 cm)
    x_flg1 = x_mw_sh + mw_len
    mw_flg_od = 7.6
    mw_flg_t = 0.65
    cad_rect(ax, x_flg1, CY_D3 - mw_flg_od/2, mw_flg_t, mw_flg_od, lw=1.2, fill=True)
    
    # Spiral Wound Gasket (PTFE filler + 316L rings)
    x_gask = x_flg1 + mw_flg_t
    cad_rect(ax, x_gask, CY_D3 - mw_id/2, 0.12, mw_id, lw=0.8, fill=True)
    
    # Blind Flange Cover (OD 635 mm, Thk 40 mm)
    x_blind = x_gask + 0.12
    cad_rect(ax, x_blind, CY_D3 - mw_flg_od/2, mw_flg_t, mw_flg_od, lw=1.2, fill=True)
    
    # Stud Bolts & Nuts (16x 1-1/8" Studs on BC 577.9 mm)
    for bolt_y in [CY_D3 - mw_flg_od/2 + 0.45, CY_D3 + mw_flg_od/2 - 0.45]:
        cad_line(ax, x_flg1 - 0.4, bolt_y, x_blind + mw_flg_t + 0.4, bolt_y, lw=1.1)
        cad_rect(ax, x_flg1 - 0.35, bolt_y - 0.22, 0.35, 0.44, lw=0.8, fill=True) # Inner nut
        cad_rect(ax, x_blind + mw_flg_t, bolt_y - 0.22, 0.35, 0.44, lw=0.8, fill=True) # Outer nut
    
    # Mechanical Davit Arm Assembly
    # Shell Mounting Bracket & Pivot Socket
    cad_rect(ax, x_mw_sh, CY_D3 + mw_flg_od/2 + 0.8, 0.8, 1.6, lw=1.0, fill=True)
    # Vertical Pivot Post
    cad_line(ax, x_mw_sh + 0.4, CY_D3 + mw_flg_od/2 + 0.5, x_mw_sh + 0.4, CY_D3 + mw_flg_od/2 + 4.2, lw=1.4)
    # Horizontal Swinging Boom Arm
    cad_line(ax, x_mw_sh + 0.4, CY_D3 + mw_flg_od/2 + 4.0, x_blind + mw_flg_t/2, CY_D3 + mw_flg_od/2 + 4.0, lw=1.4)
    # Diagonal Brace
    cad_line(ax, x_mw_sh + 0.4, CY_D3 + mw_flg_od/2 + 2.4, x_mw_sh + 2.5, CY_D3 + mw_flg_od/2 + 4.0, lw=1.0)
    # Eyebolt / Hanger Rod connecting boom to blind cover center
    cad_line(ax, x_blind + mw_flg_t/2, CY_D3 + mw_flg_od/2 + 4.0, x_blind + mw_flg_t/2, CY_D3 + mw_flg_od/2 + 0.5, lw=1.0)
    cad_circle(ax, x_blind + mw_flg_t/2, CY_D3 + mw_flg_od/2 + 0.5, 0.18, lw=0.9, fill=True)
    
    cad_text(ax, x_mw_sh + 2.5, CY_D3 + mw_flg_od/2 + 4.6, 'SWINGING MECHANICAL DAVIT ARM\n(ALLOWS SINGLE-OPERATOR BLIND REMOVAL)', sz=4.8, bold=True)
    cad_text(ax, x_blind + 2.5, CY_D3, 'BLIND COVER (85 kg)\n16X 1-1/8" STUDS\nSPIRAL WOUND PTFE GASKET', sz=4.8, ha='left', bold=True)
    
    # Dimensions on Manway Detail
    cad_dim_v(ax, x_mw_sh - 0.8, CY_D3 - mw_id/2, CY_D3 + mw_id/2, 'ID 450 mm', text_offset=-0.45)
    cad_dim_v(ax, x_blind + mw_flg_t + 1.2, CY_D3 - mw_flg_od/2, CY_D3 + mw_flg_od/2, 'FLANGE OD 635 mm', text_offset=0.45)
    cad_dim_h(ax, x_mw_sh, x_flg1, CY_D3 - mw_flg_od/2 - 1.2, 'PROJECTION 250 mm')
    
    # ─────────────────────────────────────────────────────────────────────────
    # DETAIL 4: TOP HEAD LIFTING LUG & GROUNDING BOSS DETAILS
    # ─────────────────────────────────────────────────────────────────────────
    D4_X, D4_Y, D4_W, D4_H = 27.5, 7.2, 24.5, 21.0
    cad_rect(ax, D4_X, D4_Y, D4_W, D4_H, lw=1.2, fill=True)
    cad_text(ax, D4_X + D4_W/2, D4_Y + D4_H - 0.7,
             'DETAIL 4 — TOP LIFTING LUG & EARTHING BOSS DETAILS', sz=7.8, bold=True)
    cad_text(ax, D4_X + D4_W/2, D4_Y + D4_H - 1.4,
             'RIGGING PADEYE (5.0 t SWL) & GROUNDING TERMINATION (SCALE 1:5 METRIC)', sz=5.5, bold=True)
    
    # Sub-Detail 4A: Top Lifting Lug
    CX_LUG = D4_X + 8.5
    CY_LUG = D4_Y + 11.5
    
    # Curved Top Head Knuckle Plate
    cad_arc(ax, CX_LUG, CY_LUG - 4.5, 12.0, 3.5, theta1=0, theta2=180, lw=1.2)
    cad_arc(ax, CX_LUG, CY_LUG - 4.5, 12.0, 3.0, theta1=0, theta2=180, lw=0.8)
    cad_text(ax, CX_LUG, CY_LUG - 3.8, 'TOP DISHED HEAD (t = 8 mm)', sz=4.5, bold=True)
    
    # Padeye Plate Body (SA-516 Gr 70: 20 mm plate)
    p_lug = [
        (CX_LUG - 2.4, CY_LUG - 2.8), (CX_LUG - 2.2, CY_LUG + 2.5),
        (CX_LUG - 1.2, CY_LUG + 4.2), (CX_LUG + 1.2, CY_LUG + 4.2),
        (CX_LUG + 2.2, CY_LUG + 2.5), (CX_LUG + 2.4, CY_LUG - 2.8)
    ]
    ax.add_patch(Polygon(p_lug, closed=True, fc='white', ec=BK, lw=1.2))
    cad_hatch_rect(ax, CX_LUG - 2.4, CY_LUG - 2.8, 4.8, 7.0, pitch=0.30, lw=0.35)
    
    # Shackle Pin Hole (Ø55 mm) & Cheek Doubler Reinforcing Rings (10 mm thk)
    cad_circle(ax, CX_LUG, CY_LUG + 2.5, 1.4, lw=1.0, fill=True) # Cheek plate OD
    cad_circle(ax, CX_LUG, CY_LUG + 2.5, 0.75, lw=1.2, fill=True) # Shackle hole Ø55
    cad_line(ax, CX_LUG - 1.8, CY_LUG + 2.5, CX_LUG + 1.8, CY_LUG + 2.5, lw=0.4, ls='-.')
    cad_line(ax, CX_LUG, CY_LUG + 0.8, CX_LUG, CY_LUG + 4.5, lw=0.4, ls='-.')
    
    # Weld to Head (Full-penetration bevel + fillet weld)
    cad_line(ax, CX_LUG - 2.8, CY_LUG - 2.8, CX_LUG - 2.4, CY_LUG - 2.8, lw=1.2)
    cad_line(ax, CX_LUG + 2.4, CY_LUG - 2.8, CX_LUG + 2.8, CY_LUG - 2.8, lw=1.2)
    
    cad_text(ax, CX_LUG, CY_LUG + 5.2, 'HEAVY-DUTY LIFTING LUG (2X AT 0° & 180°)\nRATED SAFE WORKING LOAD: 5.0 TONNES\n(>3X COLUMN EMPTY TARE WEIGHT)', sz=4.8, bold=True)
    cad_dim_h(ax, CX_LUG - 2.4, CX_LUG + 2.4, CY_LUG - 1.8, '20 mm PLT')
    
    # Sub-Detail 4B: Earthing / Grounding Boss Detail
    CX_GRD = D4_X + 18.5
    CY_GRD = D4_Y + 11.5
    cad_rect(ax, CX_GRD - 2.8, CY_GRD - 3.5, 5.6, 7.5, lw=1.0, fill=True)
    cad_text(ax, CX_GRD, CY_GRD + 3.2, 'GROUNDING BOSS DETAIL', sz=5.5, bold=True)
    
    # Skirt Plate
    cad_rect(ax, CX_GRD - 2.4, CY_GRD - 2.5, 0.6, 5.0, lw=1.1, fill=True)
    cad_text(ax, CX_GRD - 2.1, CY_GRD, 'SKIRT', sz=4.2, rotation=90, bold=True)
    # Copper-Clad Grounding Pad (50x50x10 mm)
    cad_rect(ax, CX_GRD - 1.8, CY_GRD - 0.8, 1.2, 1.6, lw=1.0, fill=True)
    # Tapped Hole M12
    cad_circle(ax, CX_GRD - 1.2, CY_GRD, 0.30, lw=0.9, fill=True)
    cad_circle(ax, CX_GRD - 1.2, CY_GRD, 0.15, fill=True)
    # Grounding Cable & Lug
    cad_line(ax, CX_GRD - 1.2, CY_GRD, CX_GRD + 1.8, CY_GRD, lw=1.2)
    cad_circle(ax, CX_GRD + 1.8, CY_GRD, 0.40, fill=True, fc=BK)
    cad_text(ax, CX_GRD + 0.2, CY_GRD - 1.8, 'M12 SS STUD & WASHER\nCOPPER CABLE TO GRID\nRESISTANCE < 1.0 OHM', sz=4.4, bold=True)
    
    # ═════════════════════════════════════════════════════════════════════════
    # RIGHT PANEL: MASTER ASME B16.5 NOZZLE TABLE & FABRICATION SCHEDULE
    # ═════════════════════════════════════════════════════════════════════════
    
    # MASTER ASME B16.5 NOZZLE SCHEDULE TABLE
    T1_X = 53.5
    T1_Y = 32.5
    t1_headers = ['TAG', 'SERVICE / DESCRIPTION', 'SIZE', 'RATING', 'FLG OD', 'BOLTS', 'REPAD']
    t1_widths  = [1.6, 10.4, 3.2, 2.8, 3.0, 3.8, 3.2]
    t1_rows = [
        ['N1', 'Feed Gas Inlet Mixture',     'DN 150 (6")', 'CL 150', '280 mm', '8x M20x110', 'Ø340 mm'],
        ['N2', 'Gas Sampling Connection',    'DN 40 (1.5")','CL 150', '127 mm', '4x M14x75',  'None'],
        ['N3', 'Scrubbing Water Feed Inlet', 'DN 80 (3")',  'CL 150', '190 mm', '4x M16x90',  'Ø190 mm'],
        ['N4', 'Rich Liquor Sump Outlet',    'DN 80 (3")',  'CL 150', '190 mm', '4x M16x90',  'Integral'],
        ['N5', 'Column Shell Bottom Drain',  'DN 40 (1.5")','CL 150', '127 mm', '4x M14x75',  'None'],
        ['N6', 'Treated Overhead Gas Vent',  'DN 50 (2")',  'CL 150', '152 mm', '4x M16x85',  'None'],
        ['N7', 'Bed Differential Press (Lo)','DN 50 (2")',  'CL 150', '152 mm', '4x M16x85',  'None'],
        ['N8', 'Bed Differential Press (Hi)','DN 50 (2")',  'CL 150', '152 mm', '4x M16x85',  'None'],
        ['N9', 'Gas Inlet Thermowell (TI)',  'DN 40 (1.5")','CL 150', '127 mm', '4x M14x75',  'None'],
        ['N10','Liquid Level Instrument Taps','DN 50 (2")',  'CL 150', '152 mm', '4x M16x85',  'None'],
        ['N11','Demister Flush Spray Line',  'DN 40 (1.5")','CL 150', '127 mm', '4x M14x75',  'None'],
        ['M1', 'Lower Packing Access Manway','DN 450 (18")','CL 150', '635 mm', '16x 1-1/8"', 'Ø750 mm'],
        ['M2', 'Upper Distributor Manway',  'DN 450 (18")','CL 150', '635 mm', '16x 1-1/8"', 'Ø750 mm'],
    ]
    cad_draw_table(ax, T1_X, T1_Y, t1_headers, t1_rows, t1_widths, row_h=0.48,
                   title='TABLE 1 — MASTER ASME B16.5 NOZZLE & REINFORCEMENT SCHEDULE', sz=5.0)
    
    # TABLE 2: WELDING PROCEDURE SPECIFICATION (WPS) & NDE REQUIREMENTS
    T2_X = 53.5
    T2_Y = 19.5
    t2_headers = ['JOINT CAT.', 'SERVICE / LOCATION', 'WELD TYPE', 'PROCESS', 'NDE / INSPECTION']
    t2_widths  = [2.5, 8.5, 5.0, 5.0, 7.0]
    t2_rows = [
        ['Cat. A', 'Longitudinal Shell Seams', 'Double-V Butt', 'GTAW + SMAW', '100% Radiography (RT-1)'],
        ['Cat. B', 'Circumferential Girth Seams','Double-V Butt', 'GTAW + SMAW', '100% Radiography (RT-1)'],
        ['Cat. C', 'Flange-to-Neck Welds',     'Full Pen Hub',  'GTAW + SMAW', '100% Dye Penetrant (PT)'],
        ['Cat. D', 'Nozzle-to-Shell Welds',    'Full Penetration','GTAW + SMAW','100% PT + Ultrasonic (UT)'],
        ['Repad',  'Reinforcing Pad Fillet',   'Continuous Fillet','SMAW E7018', 'Air Leak Test (1.5 bar)'],
        ['Liner',  'PVDF Corrosion Barrier',   'Hot Gas Thermo', 'Thermoplastic', 'Spark Test 15 kV (NACE)'],
    ]
    cad_draw_table(ax, T2_X, T2_Y, t2_headers, t2_rows, t2_widths, row_h=0.48,
                   title='TABLE 2 — WELDING PROCEDURE (ASME SEC IX) & NDE REQUIREMENTS', sz=5.0)
    
    # FABRICATION NOTES & CODE COMPLIANCE
    N4_X = 53.5
    N4_Y = 7.2
    cad_rect(ax, N4_X, N4_Y, 28.0, 11.8, lw=1.2, fill=True)
    cad_text(ax, N4_X + 14.0, N4_Y + 11.3, 'PRESSURE VESSEL FABRICATION & TESTING SPECIFICATIONS', sz=6.8, bold=True)
    
    notes_dwg4 = [
        "1. ASME CODE JURISDICTION & DESIGN MARGINS:",
        "   - FABRICATED IN STRICT ACCORDANCE WITH ASME SECTION VIII DIVISION 1 (2023 EDITION).",
        "   - MAXIMUM ALLOWABLE WORKING PRESSURE (MAWP): 150 kPa (g) + FULL VACUUM CONTINGENCY.",
        "   - MINIMUM DESIGN METAL TEMPERATURE (MDMT): -10 °C AT DESIGN PRESSURE.",
        "2. CORROSION LINING CONTINUITY & SPARK TESTING:",
        "   - ALL PROCESS WETTED INTERIOR SURFACES SHALL BE LINED WITH 3.0 mm BONDED PVDF / PTFE.",
        "   - LINER CONTINUITY TESTED OVER 100% OF SURFACE USING HIGH-VOLTAGE SPARK TESTER AT 15 kV.",
        "   - ZERO POROSITY, BLISTERS OR AIR GAPS ALLOWED BETWEEN STEEL SHELL AND FLUOROPOLYMER LINER.",
        "3. PRESSURE TESTING & POST-WELD HEAT TREATMENT (PWHT):",
        "   - HYDROSTATIC TEST CONDUCTED AT 1.5x MAWP PRIOR TO FLUOROPOLYMER LINING INSTALLATION.",
        "   - TEST WATER: CHLORIDE-FREE DEMINERALIZED WATER (< 25 ppm Cl-), TEMPERATURE >= 20 °C.",
    ]
    for n_idx, n_line in enumerate(notes_dwg4):
        bold_flag = ("1." in n_line or "2." in n_line or "3." in n_line)
        cad_text(ax, N4_X + 0.40, N4_Y + 10.6 - n_idx * 0.72, n_line, sz=4.6, ha='left', bold=bold_flag)
    
    # ── Title Block ─────────────────────────────────────────────────────────
    draw_title_block(
        ax,
        dwg_title='PACKED-BED ABSORBER (C-101) — MECHANICAL FABRICATION, NOZZLE & MANWAY DETAILS CAD',
        dwg_no='PEDD-PBA-04',
        rev='00',
        sheet_no='04 OF 05',
        scale='DETAILED VIEWS 1:2, 1:5, 1:6 METRIC',
        equip_desc='PRESSURE VESSEL FABRICATION DETAILS — WELDS, REPAD, MANWAY & RIGGING',
        duty_desc='ASME SEC VIII DIV 1 | SA-516 GR 70 + PVDF LINER | ASME B16.5 CL 150 RF'
    )
    
    # ── Save Outputs ────────────────────────────────────────────────────────
    OUT_DIR = r'd:\GAMES\zercxes\CAD_Engineering_Drawings'
    pdf_path = os.path.join(OUT_DIR, '04_Packed_Bed_Absorber_Nozzle_Manway_Details_CAD.pdf')
    png_path = os.path.join(OUT_DIR, '04_Packed_Bed_Absorber_Nozzle_Manway_Details_CAD.png')
    
    fig.savefig(pdf_path, dpi=300, bbox_inches='tight', facecolor='white')
    fig.savefig(png_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"SUCCESS: DWG-04 generated at {pdf_path} and {png_path}")

if __name__ == '__main__':
    generate_dwg04()
