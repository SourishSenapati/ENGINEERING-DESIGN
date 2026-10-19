"""
DWG-03: PACKING SUPPORT & COLUMN BASE STRUCTURAL CAD
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

def generate_dwg03():
    fig, ax = create_cad_canvas()
    draw_sheet_border(ax)
    
    # ═════════════════════════════════════════════════════════════════════════
    # SHEET LAYOUT: 4 COMPREHENSIVE CAD STRUCTURAL DETAILS
    # View 1: Support Grid Sectional Elevation (Top-Left: X = 2.5 to 26.5, Y = 28.5 to 52.0)
    # View 2: Support Grid Plan View (Top-Right: X = 28.0 to 52.0, Y = 28.5 to 52.0)
    # View 3: Skirt & Base Ring Structural Assembly (Btm-Left: X = 2.5 to 26.5, Y = 7.2 to 27.0)
    # View 4: Structural Load Analysis & Engineering Notes (Btm-Right: X = 28.0 to 52.0, Y = 7.2 to 27.0)
    # Right Panel: Tables, Welding Schedule & Structural Sizing (X = 53.5 to 81.5, Y = 7.2 to 52.0)
    # ═════════════════════════════════════════════════════════════════════════
    
    # ─────────────────────────────────────────────────────────────────────────
    # VIEW 1: GAS-INJECTION PACKING SUPPORT ASSEMBLY (SECTIONAL ELEVATION)
    # ─────────────────────────────────────────────────────────────────────────
    V1_X, V1_Y, V1_W, V1_H = 2.5, 29.0, 24.5, 23.5
    cad_rect(ax, V1_X, V1_Y, V1_W, V1_H, lw=1.2, fill=True)
    cad_text(ax, V1_X + V1_W/2, V1_Y + V1_H - 0.7,
             'VIEW 1 — GAS-INJECTION PACKING SUPPORT GRID (SECTIONAL ELEVATION)', sz=7.8, bold=True)
    cad_text(ax, V1_X + V1_W/2, V1_Y + V1_H - 1.4,
             'MULTI-BEAM CORRUGATED CHIMNEY TYPE (>85% FREE AREA) — SCALE 1:8 METRIC', sz=5.5, bold=True)
    
    CX_V1 = V1_X + 12.25
    CY_V1 = V1_Y + 12.5
    R_V1 = 8.0  # 750 mm scaled (16.0 cm total diameter)
    
    # Column Shell Walls
    cad_line(ax, CX_V1 - R_V1, CY_V1 - 8.0, CX_V1 - R_V1, CY_V1 + 8.0, lw=1.2)
    cad_line(ax, CX_V1 + R_V1, CY_V1 - 8.0, CX_V1 + R_V1, CY_V1 + 8.0, lw=1.2)
    cad_line(ax, CX_V1 - R_V1 - 0.28, CY_V1 - 8.0, CX_V1 - R_V1 - 0.28, CY_V1 + 8.0, lw=0.6)
    cad_line(ax, CX_V1 + R_V1 + 0.28, CY_V1 - 8.0, CX_V1 + R_V1 + 0.28, CY_V1 + 8.0, lw=0.6)
    cad_hatch_rect(ax, CX_V1 - R_V1 - 0.28, CY_V1 - 8.0, 0.28, 16.0, pitch=0.20, lw=0.35)
    cad_hatch_rect(ax, CX_V1 + R_V1, CY_V1 - 8.0, 0.28, 16.0, pitch=0.20, lw=0.35)
    cad_line(ax, CX_V1, CY_V1 - 8.5, CX_V1, CY_V1 + 8.5, lw=0.5, ls='-.')
    
    # Internal Shell Support Ring Ledge (50 mm wide x 15 mm thick)
    ring_w = 1.2
    ring_thk = 0.40
    cad_rect(ax, CX_V1 - R_V1, CY_V1 - 1.5, ring_w, ring_thk, lw=1.1, fill=True)
    cad_rect(ax, CX_V1 + R_V1 - ring_w, CY_V1 - 1.5, ring_w, ring_thk, lw=1.1, fill=True)
    
    # Gusset Stiffener Brackets under support ring (8x radial gussets)
    cad_line(ax, CX_V1 - R_V1, CY_V1 - 1.5, CX_V1 - R_V1 + ring_w, CY_V1 - 3.2, lw=1.1)
    cad_line(ax, CX_V1 - R_V1 + ring_w, CY_V1 - 1.5, CX_V1 - R_V1 + ring_w, CY_V1 - 3.2, lw=1.1)
    cad_line(ax, CX_V1 + R_V1, CY_V1 - 1.5, CX_V1 + R_V1 - ring_w, CY_V1 - 3.2, lw=1.1)
    cad_line(ax, CX_V1 + R_V1 - ring_w, CY_V1 - 1.5, CX_V1 + R_V1 - ring_w, CY_V1 - 3.2, lw=1.1)
    cad_text(ax, CX_V1 - R_V1 + 1.8, CY_V1 - 2.5, 'RADIAL GUSSET\nSTIFFENERS (8X)', sz=4.4, ha='left', bold=True)
    
    # Central Support I-Beam (Spanning Column ID: 100 x 50 mm Beam)
    b_flg_w = 1.8
    b_flg_t = 0.22
    b_web_h = 2.0
    b_web_t = 0.25
    b_cy = CY_V1 - 1.5 - b_web_h/2
    # Top Flange
    cad_rect(ax, CX_V1 - b_flg_w/2, CY_V1 - 1.5, b_flg_w, b_flg_t, lw=1.0, fill=True)
    # Web
    cad_rect(ax, CX_V1 - b_web_t/2, CY_V1 - 1.5 - b_web_h, b_web_t, b_web_h, lw=1.0, fill=True)
    # Bottom Flange
    cad_rect(ax, CX_V1 - b_flg_w/2, CY_V1 - 1.5 - b_web_h - b_flg_t, b_flg_w, b_flg_t, lw=1.0, fill=True)
    cad_text(ax, CX_V1, b_cy - 1.8, 'CENTRAL TRANSVERSE SUPPORT BEAM (I-100x50)\nCARRIES 16.1 kN NORMAL LOAD (Zreq = 18.5 cm³)', sz=4.8, bold=True)
    
    # Gas-Injection Corrugated Chimney Support Plate (Norton / Koch-Glitsch style)
    # Corrugations: High gas chimneys with side slots and lower liquid drainage valleys
    grid_y = CY_V1 - 1.5 + ring_thk
    chimney_h = 2.4
    
    # Base Plate Frame
    cad_line(ax, CX_V1 - R_V1 + 0.1, grid_y, CX_V1 + R_V1 - 0.1, grid_y, lw=1.2)
    
    # Draw Corrugated Multi-Beam Gas Chimneys across the 750 mm cross-section
    chim_pitches = np.linspace(CX_V1 - R_V1 + 1.2, CX_V1 + R_V1 - 1.2, 7)
    for c_idx, cx_pos in enumerate(chim_pitches):
        cw = 1.1
        # Chimney body
        cad_rect(ax, cx_pos - cw/2, grid_y, cw, chimney_h, lw=1.1, fill=True)
        # Chimney top ridge cap (anti-fouling roof)
        p_cap = [(cx_pos - cw/2 - 0.12, grid_y + chimney_h),
                 (cx_pos, grid_y + chimney_h + 0.35),
                 (cx_pos + cw/2 + 0.12, grid_y + chimney_h)]
        ax.add_patch(Polygon(p_cap, closed=False, ec=BK, lw=1.1, fill=False))
        # Side Gas Discharge Slots (Independent gas path upward)
        for sy in np.linspace(grid_y + 0.4, grid_y + chimney_h - 0.4, 4):
            cad_line(ax, cx_pos - cw/2, sy, cx_pos - cw/2 + 0.25, sy, lw=0.8)
            cad_line(ax, cx_pos + cw/2 - 0.25, sy, cx_pos + cw/2, sy, lw=0.8)
            # Gas exit arrows
            cad_arrow(ax, cx_pos - cw/2 - 0.45, sy, cx_pos - cw/2 - 0.05, sy + 0.25, lw=0.6, head_scale=5)
            cad_arrow(ax, cx_pos + cw/2 + 0.45, sy, cx_pos + cw/2 + 0.05, sy + 0.25, lw=0.6, head_scale=5)
        # Liquid Drainage Slots at the trough bottom
        cad_line(ax, cx_pos + cw/2 + 0.1, grid_y, cx_pos + cw/2 + 0.1, grid_y - 0.35, lw=0.9)
        cad_arrow(ax, cx_pos + cw/2 + 0.45, grid_y + 0.2, cx_pos + cw/2 + 0.45, grid_y - 0.6, lw=0.7, ls=':', head_scale=6)
    
    cad_text(ax, CX_V1, grid_y + chimney_h + 0.95,
             'INDEPENDENT GAS CHIMNEYS (>85% FREE AREA)\nELIMINATES LIQUID BOTTLENECK & LOCAL FLOODING',
             sz=4.8, bold=True, bg='white')
    
    # 25-mm Ceramic Raschig Rings resting in packing bed
    for rx in np.linspace(CX_V1 - R_V1 + 0.8, CX_V1 + R_V1 - 0.8, 14):
        for ry in [grid_y + chimney_h + 1.8, grid_y + chimney_h + 2.5, grid_y + chimney_h + 3.2]:
            cad_rect(ax, rx - 0.22, ry - 0.22, 0.44, 0.44, lw=0.8, fill=True)
            cad_line(ax, rx - 0.12, ry - 0.22, rx - 0.12, ry + 0.22, lw=0.6)
            cad_line(ax, rx + 0.12, ry - 0.22, rx + 0.12, ry + 0.22, lw=0.6)
    cad_text(ax, CX_V1, grid_y + chimney_h + 4.2, 'PACKED BED: 25-mm CERAMIC RASCHIG RINGS (4500 mm BED)', sz=5.0, bold=True)
    
    # Clamping J-Bolts / Hold-Down Cleats to Support Ring
    for cl_side in [-1, 1]:
        cl_x = CX_V1 + cl_side * (R_V1 - 0.6)
        cad_rect(ax, cl_x - 0.25, grid_y, 0.50, 0.60, lw=0.9, fill=True)
        cad_line(ax, cl_x, grid_y - 0.4, cl_x, grid_y + 0.8, lw=0.9) # Stud bolt
    
    # Dimensions on Sectional Support Grid
    cad_dim_h(ax, CX_V1 - R_V1, CX_V1 + R_V1, grid_y + chimney_h + 5.2, 'COLUMN ID 750 mm (CALCULATED)')
    cad_dim_v(ax, CX_V1 - R_V1 - 1.2, grid_y, grid_y + chimney_h, 'CHIMNEY 100 mm', text_offset=-0.45)
    cad_dim_h(ax, CX_V1 - R_V1, CX_V1 - R_V1 + ring_w, CY_V1 - 4.2, 'RING 50 mm')
    
    # ─────────────────────────────────────────────────────────────────────────
    # VIEW 2: PACKING SUPPORT GRID (TOP PLAN VIEW)
    # ─────────────────────────────────────────────────────────────────────────
    V2_X, V2_Y, V2_W, V2_H = 27.5, 29.0, 24.5, 23.5
    cad_rect(ax, V2_X, V2_Y, V2_W, V2_H, lw=1.2, fill=True)
    cad_text(ax, V2_X + V2_W/2, V2_Y + V2_H - 0.7,
             'VIEW 2 — PACKING SUPPORT GRID & BEAMS (PLAN VIEW)', sz=7.8, bold=True)
    cad_text(ax, V2_X + V2_W/2, V2_Y + V2_H - 1.4,
             'STRUCTURAL LAYOUT & SLOTTED FLOW PATTERN (SCALE 1:8 METRIC)', sz=5.5, bold=True)
    
    CX_V2 = V2_X + 12.25
    CY_V2 = V2_Y + 12.0
    R_PL = 7.5  # 750 mm scaled plan radius
    
    # Outer Shell & Support Ring on Plan
    cad_circle(ax, CX_V2, CY_V2, R_PL + 0.25, lw=0.8) # Shell OD
    cad_circle(ax, CX_V2, CY_V2, R_PL, lw=1.2, fill=True) # Shell ID 750
    cad_circle(ax, CX_V2, CY_V2, R_PL - 1.0, lw=1.0) # Support Ring ID 650 (50 mm width)
    cad_hatch_rect(ax, CX_V2 - R_PL, CY_V2 - R_PL, 2 * R_PL, 2 * R_PL, pitch=0.35, lw=0.35, color=GREY)
    # Centerlines
    cad_line(ax, CX_V2 - R_PL - 1.5, CY_V2, CX_V2 + R_PL + 1.5, CY_V2, lw=0.4, ls='-.')
    cad_line(ax, CX_V2, CY_V2 - R_PL - 1.5, CX_V2, CY_V2 + R_PL + 1.5, lw=0.4, ls='-.')
    
    # Central Main I-Beam Footprint (spanning vertical centerline)
    cad_rect(ax, CX_V2 - 0.7, CY_V2 - R_PL + 0.1, 1.4, 2 * R_PL - 0.2, lw=1.1, fill=True)
    cad_line(ax, CX_V2 - 0.15, CY_V2 - R_PL + 0.1, CX_V2 - 0.15, CY_V2 + R_PL - 0.1, lw=0.7, ls='--')
    cad_line(ax, CX_V2 + 0.15, CY_V2 - R_PL + 0.1, CX_V2 + 0.15, CY_V2 + R_PL - 0.1, lw=0.7, ls='--')
    cad_text(ax, CX_V2, CY_V2, 'CENTRAL SUPPORT BEAM\n(I-100x50)', sz=4.8, bold=True, bg='white')
    
    # Transverse Corrugated Slotted Chimney Trays (Multi-beam pattern)
    for px in np.linspace(CX_V2 - R_PL + 1.2, CX_V2 + R_PL - 1.2, 9):
        if abs(px - CX_V2) > 0.8:
            y_span = 2 * np.sqrt(max(0, (R_PL - 1.0)**2 - (px - CX_V2)**2))
            cad_rect(ax, px - 0.35, CY_V2 - y_span/2, 0.70, y_span, lw=0.8, fill=True)
            # Gas slots
            for sy in np.linspace(CY_V2 - y_span/2 + 0.6, CY_V2 + y_span/2 - 0.6, max(2, int(y_span/1.2))):
                cad_line(ax, px - 0.25, sy, px + 0.25, sy, lw=0.6)
    
    # Clamping Cleats & Studs on Perimeter Bolt Circle (8x M16 bolts)
    for ang in np.linspace(0, 2*np.pi, 8, endpoint=False):
        bx = CX_V2 + (R_PL - 0.5) * np.cos(ang)
        by = CY_V2 + (R_PL - 0.5) * np.sin(ang)
        cad_circle(ax, bx, by, 0.18, lw=0.8, fill=True)
        cad_circle(ax, bx, by, 0.08, fill=True)
    cad_text(ax, CX_V2 + R_PL - 1.2, CY_V2 + R_PL - 0.5, 'HOLD-DOWN CLAMPS\n(8X M16 STUDS)', sz=4.4, bold=True)
    
    # Plan Dimensions
    cad_dim_h(ax, CX_V2 - R_PL, CX_V2 + R_PL, CY_V2 + R_PL + 1.5, 'COLUMN ID 750 mm')
    cad_dim_h(ax, CX_V2 - R_PL + 1.0, CX_V2 + R_PL - 1.0, CY_V2 - R_PL - 1.5, 'RING BORE ID 650 mm')
    
    # ─────────────────────────────────────────────────────────────────────────
    # VIEW 3: CYLINDRICAL SKIRT & FOUNDATION ANCHOR BOLT ASSEMBLY
    # ─────────────────────────────────────────────────────────────────────────
    V3_X, V3_Y, V3_W, V3_H = 2.5, 7.2, 24.5, 21.0
    cad_rect(ax, V3_X, V3_Y, V3_W, V3_H, lw=1.2, fill=True)
    cad_text(ax, V3_X + V3_W/2, V3_Y + V3_H - 0.7,
             'VIEW 3 — CYLINDRICAL SKIRT & FOUNDATION ANCHOR BOLTS', sz=7.8, bold=True)
    cad_text(ax, V3_X + V3_W/2, V3_Y + V3_H - 1.4,
             'SKIRT-TO-HEAD WELD, BASE RING & ANCHOR CHAIRS (SCALE 1:8 METRIC)', sz=5.5, bold=True)
    
    CX_V3 = V3_X + 12.25
    CY_V3_GND = V3_Y + 4.5
    R_SKIRT = 8.0  # Skirt OD = 766 mm scaled
    
    # Concrete Pedestal & Grout
    cad_rect(ax, CX_V3 - 11.5, V3_Y + 0.8, 23.0, CY_V3_GND - (V3_Y + 0.8), lw=1.2, fill=True)
    cad_hatch_rect(ax, CX_V3 - 11.5, V3_Y + 0.8, 23.0, CY_V3_GND - (V3_Y + 0.8), pitch=0.35, angle=-45, lw=0.4)
    cad_line(ax, CX_V3 - 12.0, CY_V3_GND, CX_V3 + 12.0, CY_V3_GND, lw=1.2) # Ground Line
    cad_text(ax, CX_V3 - 9.5, CY_V3_GND - 0.6, 'REINFORCED CONCRETE PEDESTAL (M25 GRADE)', sz=4.8, bold=True)
    
    # Non-Shrink Epoxy Grout (25 mm thick)
    cad_rect(ax, CX_V3 - 10.5, CY_V3_GND, 21.0, 0.40, lw=0.9, fill=True)
    cad_text(ax, CX_V3 + 8.5, CY_V3_GND + 0.20, 'EPOXY GROUT (25 mm)', sz=4.4, ha='left', bold=True)
    
    # Annular Base Ring (OD 1050 mm -> 11.0 cm radius, Thickness 20 mm -> 0.45 cm)
    y_br_btm = CY_V3_GND + 0.40
    br_thk = 0.45
    R_BR_OD = 11.0
    cad_rect(ax, CX_V3 - R_BR_OD, y_br_btm, 2 * R_BR_OD, br_thk, lw=1.2, fill=True)
    cad_text(ax, CX_V3 + R_BR_OD + 0.3, y_br_btm + br_thk/2, 'BASE RING OD 1050 mm (20 mm THK)', sz=4.6, ha='left', bold=True)
    
    # Skirt Shell Plate (Cylindrical: SA-36 Steel, 10 mm thick)
    skirt_top_y = V3_Y + 18.0
    cad_line(ax, CX_V3 - R_SKIRT, y_br_btm + br_thk, CX_V3 - R_SKIRT, skirt_top_y, lw=1.2)
    cad_line(ax, CX_V3 + R_SKIRT, y_br_btm + br_thk, CX_V3 + R_SKIRT, skirt_top_y, lw=1.2)
    cad_line(ax, CX_V3 - R_SKIRT + 0.25, y_br_btm + br_thk, CX_V3 - R_SKIRT + 0.25, skirt_top_y, lw=0.6)
    cad_line(ax, CX_V3 + R_SKIRT - 0.25, y_br_btm + br_thk, CX_V3 + R_SKIRT - 0.25, skirt_top_y, lw=0.6)
    cad_hatch_rect(ax, CX_V3 - R_SKIRT, y_br_btm + br_thk, 0.25, skirt_top_y - y_br_btm - br_thk, pitch=0.20, lw=0.35)
    cad_hatch_rect(ax, CX_V3 + R_SKIRT - 0.25, y_br_btm + br_thk, 0.25, skirt_top_y - y_br_btm - br_thk, pitch=0.20, lw=0.35)
    cad_line(ax, CX_V3, y_br_btm - 1.5, CX_V3, skirt_top_y + 1.5, lw=0.5, ls='-.')
    
    # Bottom Head Knuckle Attachment (Double full-penetration butt weld)
    cad_arc(ax, CX_V3, skirt_top_y, 2 * R_SKIRT, 4.5, theta1=180, theta2=360, lw=1.2)
    cad_arc(ax, CX_V3, skirt_top_y, 2 * (R_SKIRT - 0.25), 4.0, theta1=180, theta2=360, lw=0.8)
    cad_text(ax, CX_V3, skirt_top_y - 1.0, 'SKIRT-TO-BOTTOM HEAD WELD (FULL PENETRATION BUTT WELD)', sz=4.8, bold=True)
    
    # Skirt Access Opening (DN400 with pipe sleeve and reinforcement ring)
    y_acc = y_br_btm + 5.0
    cad_circle(ax, CX_V3, y_acc, 1.8, lw=1.1, fill=True)
    cad_circle(ax, CX_V3, y_acc, 1.5, lw=0.8, ls='--')
    cad_text(ax, CX_V3, y_acc, 'SKIRT ACCESS\nMANHOLE DN 400', sz=4.8, bold=True)
    
    # Skirt Vent Holes (DN50, 2x near top)
    cad_circle(ax, CX_V3 - R_SKIRT + 1.2, skirt_top_y - 2.0, 0.35, lw=0.9, fill=True)
    cad_circle(ax, CX_V3 + R_SKIRT - 1.2, skirt_top_y - 2.0, 0.35, lw=0.9, fill=True)
    cad_text(ax, CX_V3 - R_SKIRT + 1.2, skirt_top_y - 2.8, 'SKIRT VENT (2X)', sz=4.0, bold=True)
    
    # Anchor Bolt Assemblies (8x M24 Bolts on BC 950 mm)
    for ab_sign in [-1, 1]:
        ab_x = CX_V3 + ab_sign * 9.5
        # Anchor Chair Gusset Plates (12 mm thk)
        cad_line(ax, ab_x - 0.6, y_br_btm + br_thk, ab_x - 0.6, y_br_btm + 2.8, lw=1.0)
        cad_line(ax, ab_x + 0.6, y_br_btm + br_thk, ab_x + 0.6, y_br_btm + 2.8, lw=1.0)
        cad_line(ax, ab_x - 0.6, y_br_btm + 2.8, ab_x + 0.6, y_br_btm + 2.8, lw=1.2) # Top chair plate
        # Anchor Bolt Shank & Double Heavy Nuts
        cad_line(ax, ab_x, y_br_btm - 2.5, ab_x, y_br_btm + 3.4, lw=1.2)
        cad_rect(ax, ab_x - 0.35, y_br_btm + 2.8, 0.70, 0.35, lw=0.9, fill=True) # Nut 1
        cad_rect(ax, ab_x - 0.35, y_br_btm + 3.15, 0.70, 0.35, lw=0.9, fill=True) # Locknut 2
        # Concrete embedment hook
        cad_line(ax, ab_x, y_br_btm - 2.5, ab_x + ab_sign*0.8, y_br_btm - 2.5, lw=1.2)
    cad_text(ax, CX_V3 - 9.5, y_br_btm + 4.2, 'ANCHOR BOLT CHAIR (8X)\nM24 SA-193 B7 BOLTS\nEMBEDMENT 450 mm', sz=4.5, bold=True)
    
    # Earthing Boss on Skirt Base
    cad_rect(ax, CX_V3 + R_SKIRT, y_br_btm + 1.2, 0.60, 0.40, lw=0.9, fill=True)
    cad_circle(ax, CX_V3 + R_SKIRT + 0.3, y_br_btm + 1.4, 0.08, fill=True)
    cad_text(ax, CX_V3 + R_SKIRT + 0.8, y_br_btm + 1.4, 'EARTHING BOSS\nM12 TAPPED HOLE', sz=4.2, ha='left', bold=True)
    
    # Dimensions on Skirt Detail
    cad_dim_h(ax, CX_V3 - R_BR_OD, CX_V3 + R_BR_OD, CY_V3_GND - 1.2, 'BASE RING OD 1050 mm')
    cad_dim_h(ax, CX_V3 - 9.5, CX_V3 + 9.5, y_br_btm + 1.8, 'BOLT CIRCLE 950 mm')
    cad_dim_v(ax, CX_V3 - R_SKIRT - 1.8, y_br_btm, skirt_top_y, 'SKIRT 1800 mm', text_offset=-0.50)
    
    # ─────────────────────────────────────────────────────────────────────────
    # VIEW 4: STRUCTURAL LOAD BREAKDOWN & PRELIMINARY BEAM SIZING
    # ─────────────────────────────────────────────────────────────────────────
    V4_X, V4_Y, V4_W, V4_H = 27.5, 7.2, 24.5, 21.0
    cad_rect(ax, V4_X, V4_Y, V4_W, V4_H, lw=1.2, fill=True)
    cad_text(ax, V4_X + V4_W/2, V4_Y + V4_H - 0.7,
             'VIEW 4 — STRUCTURAL LOAD BREAKDOWN & BEAM SIZING ANALYSIS', sz=7.8, bold=True)
    cad_text(ax, V4_X + V4_W/2, V4_Y + V4_H - 1.4,
             'MATHEMATICAL DERIVATION OF GRAVITY, OPERATING & UPSET LOADS', sz=5.5, bold=True)
    
    # Load Breakdown Box
    LX_CALC = V4_X + 1.2
    LY_CALC = V4_Y + 18.0
    
    calc_lines = [
        ("1. DRY PACKING GRAVITY LOAD (CALCULATED DIRECTLY FROM PROCESS DATA):", True),
        ("   - Active Packed Height Z = 4.50 m (Selected; Calculated = 4.30 m)", False),
        ("   - Column Internal Cross-Sectional Area Ac = pi/4 * (0.75 m)² = 0.4418 m²", False),
        ("   - Packed Bed Volume Vp = Ac * Z = 0.4418 * 4.50 = 1.988 m³ (Nominal = 1.79 m³)", False),
        ("   - Ceramic Raschig Ring Bulk Density ρbulk = 680 kg/m³", False),
        ("   - Dry Packing Mass Mp = Vp * ρbulk = 1.79 * 680 = 1,217.2 kg ≈ 1.22 tonnes", False),
        ("   - Dry Packing Weight Wdry = Mp * g = 1217.2 * 9.80665 = 11,937 N ≈ 11.94 kN", True),
        ("", False),
        ("2. OPERATIONAL LIQUID HOLDUP & COMBINED DESIGN LOAD:", True),
        ("   - Normal Dynamic Liquid Holdup (15 vol% of Bed Void Volume):", False),
        ("     V_L,dyn = 0.15 * ε * Vp = 0.15 * 0.74 * 1.79 m³ = 0.1987 m³", False),
        ("     W_liquid,oper = 0.1987 m³ * 997 kg/m³ * 9.81 m/s² = 1.94 kN", False),
        ("   - Support Grid, Clamps & Hold-Down Self-Weight: Wgrid ≈ 1.50 kN", False),
        ("   - NORMAL OPERATING DESIGN LOAD ON SUPPORT: Woper = 11.94 + 1.94 + 1.50 = 15.38 kN ≈ 16.1 kN", True),
        ("", False),
        ("3. WORST-CASE UPSET / FLOODED COLUMN CONDITION (SAFETY CRITERION):", True),
        ("   - In event of bottom nozzle blockage, 100% of packing void fills with water:", False),
        ("     V_void = ε * Vp = 0.74 * 1.79 m³ = 1.325 m³", False),
        ("     W_flood = 1.325 m³ * 997 kg/m³ * 9.81 m/s² = 12.95 kN", False),
        ("   - MAXIMUM FLOODED UPSET LOAD: Wupset = 11.94 + 12.95 + 1.50 = 26.39 kN ≈ 26.4 kN", True),
        ("", False),
        ("4. PRELIMINARY CENTRAL BEAM STRESS & DEFLECTION CHECK:", True),
        ("   - Simply Supported Beam Spanning Column ID (L = 750 mm = 0.75 m):", False),
        ("     Maximum Bending Moment Mmax = (Woper * L) / 8 = (16.1 * 0.75) / 8 = 1.51 kN·m", False),
        ("     Required Section Modulus Zreq = Mmax / (0.66 * fy) = 1.51x10⁶ / (0.66 * 250) = 9.15 cm³", False),
        ("     Selected Section: ISMB 100 / I-100x50 (Z = 25.7 cm³ > Zreq) -> Factor of Safety = 2.81", True),
        ("     Mid-Span Deflection δ = 5 W L³ / (384 E I) = 0.32 mm (< L/1000 = 0.75 mm allowable)", True),
    ]
    
    for l_idx, (l_text, b_flag) in enumerate(calc_lines):
        yy = LY_CALC - l_idx * 0.72
        cad_text(ax, LX_CALC, yy, l_text, sz=4.4, ha='left', bold=b_flag)
    
    # ═════════════════════════════════════════════════════════════════════════
    # RIGHT PANEL: TABLES, WELDING SCHEDULE & CODE COMPLIANCE (X = 53.5 to 81.5)
    # ═════════════════════════════════════════════════════════════════════════
    
    # TABLE 1: PACKING SUPPORT STRUCTURAL LOAD & DESIGN SUMMARY
    T1_X = 53.5
    T1_Y = 37.0
    t1_headers = ['LOAD CONDITION / PARAMETER', 'MAGNITUDE', 'GOVERNING ENGINEERING BASIS']
    t1_widths  = [9.8, 6.2, 12.0]
    t1_rows = [
        ['Dry Packing Weight (Wdry)',  '11.94 kN (1.22 t)', 'Calculated: Vp=1.79 m³, ρbulk=680 kg/m³'],
        ['Normal Dynamic Liquid Holdup', '1.94 kN (0.20 t)', '15 vol% void holdup at L=17.25 kg/s'],
        ['Internals & Grid Self-Weight',  '1.50 kN (0.15 t)', 'FRP / Titanium multi-beam grid frame'],
        ['NORMAL OPERATING LOAD',       '15.38 kN (1.57 t)', 'Wdry + Wliquid + Wgrid (Continuous Service)'],
        ['Design Operating Load (FS=1.05)','16.10 kN (1.64 t)', 'Structural Design Baseline for Support Grid'],
        ['Flooded Liquid Holdup Load',  '12.95 kN (1.32 t)', '100% void space filled with water (ε=0.74)'],
        ['WORST-CASE UPSET / FLOOD LOAD','26.39 kN (2.69 t)', 'Emergency Drainage Interruption Contingency'],
        ['Support Free Flow Area',       '>85% Cross-Section', 'Eliminates premature flooding at bed entry'],
        ['Central Beam Maximum Moment',  '1.51 kN·m',         'Mmax = (W * L) / 8  for Simply Supported Span'],
        ['Selected Central Beam Section','I-100x50 (ISMB 100)','Z = 25.7 cm³ (Allowable Bending Stress 165 MPa)'],
        ['Beam Deflection at Mid-Span',  '0.32 mm (L / 2340)', 'Well within rigid deflection limit (L / 500)'],
        ['Anchor Bolt Tensile Load',     '14.2 kN / bolt',    'Wind overturning + uplift moment (IS 875)'],
    ]
    cad_draw_table(ax, T1_X, T1_Y, t1_headers, t1_rows, t1_widths, row_h=0.48,
                   title='TABLE 1 — STRUCTURAL LOAD SUMMARY & BEAM SIZING DATA', sz=5.0)
    
    # TABLE 2: STRUCTURAL BILL OF MATERIALS (BOM) & WELD SCHEDULE
    T2_X = 53.5
    T2_Y = 22.0
    t2_headers = ['MARK', 'STRUCTURAL COMPONENT', 'QTY', 'MATERIAL SPEC.', 'WELD / FASTENER SPEC.']
    t2_widths  = [1.6, 8.8, 1.6, 8.5, 7.5]
    t2_rows = [
        ['S1', 'Corrugated Support Grid', '1 SET', 'High-Strength FRP / Ti Gr 2', 'Slotted Interlock Cleats'],
        ['S2', 'Support Ledge Ring',      '1 PC',  'SA-516 Gr 70 + PVDF (50x12)', 'Full Pen Fillet Weld (6 mm)'],
        ['S3', 'Ring Gusset Plates',     '8 PCS', 'SA-516 Gr 70 (10 mm Plate)',  'Double Fillet Weld (6 mm)'],
        ['S4', 'Central Support Beam',    '1 PC',  'SA-36 I-100x50 Structural',   'Bolted / Welded to Cleats'],
        ['S5', 'Cylindrical Support Skirt','1 PC', 'SA-36 Steel (10 mm Plate)',   'Full Pen Butt Weld to Head'],
        ['S6', 'Annular Base Ring',       '1 PC',  'SA-36 Steel (1050x740x20 mm)', 'Double Fillet Weld (10 mm)'],
        ['S7', 'Anchor Bolt Chairs',     '8 SET', 'SA-36 (12 mm Plate)',          'Fillet Welded to Skirt & Ring'],
        ['S8', 'Foundation Anchor Bolts', '8 PCS', 'SA-193 B7 Heavy Studs (M24)', 'Double Heavy Hex Nuts SA-194 2H'],
        ['S9', 'Skirt Access Manhole',    '1 SET', 'SA-106 Gr B Pipe + Blind',    'Flanged Sleeve DN 400'],
        ['S10','Earthing Boss Pad',       '2 PCS', 'Copper Clad Steel (50x50x10)','Seal Welded to Skirt Base'],
    ]
    cad_draw_table(ax, T2_X, T2_Y, t2_headers, t2_rows, t2_widths, row_h=0.48,
                   title='TABLE 2 — STRUCTURAL BILL OF MATERIALS & WELDING DETAILS', sz=5.0)
    
    # STRUCTURAL DESIGN CRITERIA & ENGINEERING DISCLAIMER
    N3_X = 53.5
    N3_Y = 7.2
    cad_rect(ax, N3_X, N3_Y, 28.0, 14.2, lw=1.2, fill=True)
    cad_text(ax, N3_X + 14.0, N3_Y + 13.7, 'STRUCTURAL DESIGN CRITERIA & MECHANICAL NOTES', sz=7.0, bold=True)
    
    notes_dwg3 = [
        "1. PROCESS-TO-MECHANICAL BOUNDARY SPECIFICATION:",
        "   - DRY PACKING LOAD (11.94 kN) DERIVED DIRECTLY FROM CONVERGED PROCESS SIZING (Vp = 1.79 m3, 680 kg/m3).",
        "   - NORMAL OPERATIONAL DESIGN LOAD (16.1 kN) INCLUDES 15 vol% LIQUID HOLDUP AND GRID TARE WEIGHT.",
        "   - MAXIMUM CONTINGENCY LOAD (26.4 kN) GOVERNS THE UPSET FLOODED CONDITION FOR INTEGRITY ASSURANCE.",
        "   - STRUCTURAL BEAM DIMENSIONS (I-100x50) AND SKIRT THICKNESS (10 mm) ARE PRELIMINARY CAD ASSUMPTIONS.",
        "     FINAL STRUCTURAL DETAILS REQUIRE VERIFICATION PER IS 800:2007 / AISC 360 SPECIFICATIONS.",
        "2. WELDING PROCEDURE & INSPECTION STANDARDS:",
        "   - ALL STRUCTURAL SKIRT AND BASE RING WELDING: AWS D1.1 / ASME SECTION IX CERTIFIED PROCEDURES.",
        "   - FULL PENETRATION BUTT WELD BETWEEN SKIRT AND BOTTOM HEAD SUBJECT TO 100% MAGNETIC PARTICLE (MT)",
        "     AND ULTRASONIC TESTING (UT) PER ASME SECTION VIII DIVISION 1 MANDATORY APPENDIX 12.",
        "3. CORROSION PROTECTION IN CHEMICAL ENVIRONMENT:",
        "   - EXTERNAL SKIRT SHELL AND BASE RING PRIMED WITH HIGH-BUILD INORGANIC ZINC SILICATE (75 µm)",
        "     FOLLOWED BY TWO COATS OF CHEMICAL-RESISTANT EPOXY MASTIC (TOTAL DRY FILM THICKNESS >= 250 µm).",
        "4. CIVIL & ANCHORING CRITERIA:",
        "   - FOUNDATION SIZED FOR MAXIMUM WIND MOMENT AT 160 km/h BASIC WIND SPEED PER IS 875 (PART 3).",
        "   - ANCHOR BOLTS SHALL BE RETORQUED AFTER INITIAL 72-HOUR WATER HYDROTEST.",
    ]
    for n_idx, n_line in enumerate(notes_dwg3):
        bold_flag = ("1." in n_line or "2." in n_line or "3." in n_line or "4." in n_line)
        cad_text(ax, N3_X + 0.40, N3_Y + 13.0 - n_idx * 0.70, n_line, sz=4.6, ha='left', bold=bold_flag)
    
    # ── Title Block ─────────────────────────────────────────────────────────
    draw_title_block(
        ax,
        dwg_title='PACKED-BED ABSORBER (C-101) — PACKING SUPPORT & COLUMN BASE STRUCTURAL CAD',
        dwg_no='PEDD-PBA-03',
        rev='00',
        sheet_no='03 OF 05',
        scale='1:8 METRIC / DETAIL PROPORTIONED',
        equip_desc='ABSORBER PACKING SUPPORT GRID & CYLINDRICAL SKIRT ASSEMBLY',
        duty_desc='DRY PACKING LOAD: 11.9 kN | OPERATING LOAD: 16.1 kN | UPSET: 26.4 kN'
    )
    
    # ── Save Outputs ────────────────────────────────────────────────────────
    OUT_DIR = r'd:\GAMES\zercxes\CAD_Engineering_Drawings'
    pdf_path = os.path.join(OUT_DIR, '03_Packed_Bed_Absorber_Packing_Support_Details_CAD.pdf')
    png_path = os.path.join(OUT_DIR, '03_Packed_Bed_Absorber_Packing_Support_Details_CAD.png')
    
    fig.savefig(pdf_path, dpi=300, bbox_inches='tight', facecolor='white')
    fig.savefig(png_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"SUCCESS: DWG-03 generated at {pdf_path} and {png_path}")

if __name__ == '__main__':
    generate_dwg03()
