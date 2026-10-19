"""
A4 OPTIMIZED: DWG-03 PACKING SUPPORT & COLUMN BASE STRUCTURAL CAD
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
    cad_dim_h, cad_dim_v, cad_dim_leader, cad_balloon, cad_flange, cad_hatch_rect,
    cad_draw_table_a4, W, H, BK, GREY
)

def generate_a4_dwg03(out_pdf, out_png):
    fig, ax = create_a4_canvas()
    draw_a4_border(ax)
    
    # ── 4 Main Structural Panels ─────────────────────────────────────────────
    # View 1: Support Grid Sectional Elevation (Top-Left: X = 0.8 to 10.0, Y = 11.8 to 20.2)
    # View 2: Support Grid Plan View (Top-Center: X = 10.4 to 19.6, Y = 11.8 to 20.2)
    # View 3: Skirt & Base Ring Structural Assembly (Btm-Left: X = 0.8 to 10.0, Y = 3.4 to 11.4)
    # View 4: Engineering Connection Details (Btm-Center: X = 10.4 to 19.6, Y = 3.4 to 11.4)
    # Right Side: Tables & Engineering Notes (X = 20.0 to 28.9, Y = 3.4 to 20.2)
    
    # ─────────────────────────────────────────────────────────────────────────
    # VIEW 1: SUPPORT GRID SECTIONAL ELEVATION
    # ─────────────────────────────────────────────────────────────────────────
    cad_rect(ax, 0.8, 11.8, 9.2, 8.4, lw=0.9, fill=True)
    cad_text(ax, 5.4, 19.8, 'VIEW 1 — PACKING SUPPORT GRID (ELEVATION)', sz=5.8, bold=True)
    cad_text(ax, 5.4, 19.35, 'GAS-INJECTION MULTI-BEAM TYPE (>85% FREE AREA) — SCALE 1:20', sz=4.5, bold=True)
    
    CX_1 = 5.4
    CY_1 = 15.35
    R_1 = 3.3   # Scaled 750 mm ID -> 6.6 cm dia
    
    # Shell walls (10 mm carbon steel + 3 mm PVDF liner)
    t_sh = 0.16
    cad_rect(ax, CX_1 - R_1 - t_sh, CY_1 - 2.8, t_sh, 5.6, lw=0.9, fill=True)
    cad_hatch_rect(ax, CX_1 - R_1 - t_sh, CY_1 - 2.8, t_sh, 5.6, pitch=0.12, angle=45, lw=0.25)
    cad_rect(ax, CX_1 + R_1, CY_1 - 2.8, t_sh, 5.6, lw=0.9, fill=True)
    cad_hatch_rect(ax, CX_1 + R_1, CY_1 - 2.8, t_sh, 5.6, pitch=0.12, angle=45, lw=0.25)
    # Vessel Centerline
    cad_line(ax, CX_1, CY_1 - 3.2, CX_1, CY_1 + 3.2, lw=0.35, ls='-.')
    
    # Continuous Support Ledge Ring (50x15 mm flat bar)
    w_led = 0.44
    h_led = 0.16
    y_led = CY_1 - 0.50
    cad_rect(ax, CX_1 - R_1, y_led, w_led, h_led, lw=0.9, fill=True)
    cad_rect(ax, CX_1 + R_1 - w_led, y_led, w_led, h_led, lw=0.9, fill=True)
    
    # Radial Support Gussets (100x50x10 mm)
    p_gus_l = [(CX_1 - R_1, y_led), (CX_1 - R_1 + w_led, y_led), (CX_1 - R_1, y_led - 0.90)]
    ax.add_patch(Polygon(p_gus_l, closed=True, fc='white', ec=BK, lw=0.85))
    p_gus_r = [(CX_1 + R_1, y_led), (CX_1 + R_1 - w_led, y_led), (CX_1 + R_1, y_led - 0.90)]
    ax.add_patch(Polygon(p_gus_r, closed=True, fc='white', ec=BK, lw=0.85))
    cad_dim_leader(ax, CX_1 - R_1 + 0.15, y_led - 0.45, CX_1 - R_1 + 0.65, y_led - 0.65, CX_1 - R_1 + 1.70,
                   '8x GUSSETS (10 mm)', sz=3.4, bold=True)
    
    # Central Support I-Beam (ISMB 100 x 50)
    # Depth = 100 mm -> 0.90 cm, Flange = 50 mm -> 0.45 cm
    y_bm_top = y_led
    y_bm_btm = y_bm_top - 0.90
    # End bearing brackets supporting the beam ends
    cad_rect(ax, CX_1 - R_1, y_bm_btm, 0.45, 0.10, lw=0.8, fill=True)
    cad_rect(ax, CX_1 + R_1 - 0.45, y_bm_btm, 0.45, 0.10, lw=0.8, fill=True)
    # Beam Elevation: Bottom flange, Web, Top flange
    cad_rect(ax, CX_1 - R_1 + 0.15, y_bm_btm, 2 * (R_1 - 0.15), 0.08, lw=0.8, fill=True)
    cad_line(ax, CX_1 - R_1 + 0.15, y_bm_btm + 0.08, CX_1 + R_1 - 0.15, y_bm_btm + 0.08, lw=0.6)
    cad_rect(ax, CX_1 - R_1 + 0.15, y_bm_top - 0.08, 2 * (R_1 - 0.15), 0.08, lw=0.8, fill=True)
    # Web vertical stiffeners at mid-span and quarter points
    for st_x in [CX_1 - 1.5, CX_1, CX_1 + 1.5]:
        cad_line(ax, st_x, y_bm_btm + 0.08, st_x, y_bm_top - 0.08, lw=0.65)
    cad_text(ax, CX_1, y_bm_btm - 0.32, 'CENTRAL STRUCTURAL I-BEAM (ISMB 100 x 50) | SA-36 STEEL', sz=3.6, bold=True)
    
    # Norton / Koch-Glitsch Corrugated Gas-Injection Chimney Plate
    grid_base_y = y_led + h_led
    h_chim = 1.05
    w_chim_b = 0.44
    w_chim_t = 0.36
    
    chim_xs = np.linspace(CX_1 - R_1 + 0.55, CX_1 + R_1 - 0.55, 5)
    for cx_c in chim_xs:
        # Inverted trapezoidal chimney
        p_ch = [
            (cx_c - w_chim_b/2, grid_base_y),
            (cx_c - w_chim_t/2, grid_base_y + h_chim),
            (cx_c + w_chim_t/2, grid_base_y + h_chim),
            (cx_c + w_chim_b/2, grid_base_y)
        ]
        ax.add_patch(Polygon(p_ch, closed=True, fc='white', ec=BK, lw=0.85))
        # Chimney crest cap
        cad_rect(ax, cx_c - w_chim_t/2 - 0.04, grid_base_y + h_chim, w_chim_t + 0.08, 0.06, lw=0.7, fill=True)
        # Lateral gas escape slots on vertical walls
        for sy in [grid_base_y + 0.30, grid_base_y + 0.55, grid_base_y + 0.80]:
            cad_line(ax, cx_c - w_chim_b/2 + 0.03, sy, cx_c - w_chim_t/2 + 0.08, sy, lw=0.6)
            cad_line(ax, cx_c + w_chim_t/2 - 0.08, sy, cx_c + w_chim_b/2 - 0.03, sy, lw=0.6)
        # Gas flow indication arrows (entering through side slots above liquid level)
        cad_arrow(ax, cx_c - 0.38, grid_base_y + 0.40, cx_c - 0.12, grid_base_y + 0.60, lw=0.45, head_scale=3.5)
        cad_arrow(ax, cx_c + 0.38, grid_base_y + 0.40, cx_c + 0.12, grid_base_y + 0.60, lw=0.45, head_scale=3.5)
    
    # Liquid drainage troughs (valleys) between chimneys
    for i in range(len(chim_xs) - 1):
        vx = (chim_xs[i] + chim_xs[i+1]) / 2
        # Liquid drainage orifices
        cad_circle(ax, vx, grid_base_y, 0.04, fill=True, fc=BK)
        cad_arrow(ax, vx, grid_base_y, vx, grid_base_y - 0.35, lw=0.45, head_scale=3.5)
    
    # Clamping bars and J-bolts at edges
    cad_rect(ax, CX_1 - R_1, grid_base_y, 0.30, 0.10, lw=0.8, fill=True)
    cad_rect(ax, CX_1 + R_1 - 0.30, grid_base_y, 0.30, 0.10, lw=0.8, fill=True)
    cad_line(ax, CX_1 - R_1 + 0.15, grid_base_y - 0.20, CX_1 - R_1 + 0.15, grid_base_y + 0.20, lw=0.7)
    cad_line(ax, CX_1 + R_1 - 0.15, grid_base_y - 0.20, CX_1 + R_1 - 0.15, grid_base_y + 0.20, lw=0.7)
    
    # Ceramic Raschig Rings bed above grid
    y_pack_b = grid_base_y + h_chim + 0.06
    for rx in np.linspace(CX_1 - R_1 + 0.35, CX_1 + R_1 - 0.35, 10):
        # Layer 1
        cad_rect(ax, rx - 0.11, y_pack_b + 0.05, 0.22, 0.22, lw=0.6, fill=True)
        cad_line(ax, rx - 0.06, y_pack_b + 0.05, rx - 0.06, y_pack_b + 0.27, lw=0.35)
        cad_line(ax, rx + 0.06, y_pack_b + 0.05, rx + 0.06, y_pack_b + 0.27, lw=0.35)
        # Layer 2
        cad_rect(ax, rx - 0.11, y_pack_b + 0.32, 0.22, 0.22, lw=0.6, fill=True)
        cad_line(ax, rx - 0.06, y_pack_b + 0.32, rx - 0.06, y_pack_b + 0.54, lw=0.35)
        cad_line(ax, rx + 0.06, y_pack_b + 0.32, rx + 0.06, y_pack_b + 0.54, lw=0.35)
    cad_text(ax, CX_1, y_pack_b + 0.72, '25-mm CERAMIC RASCHIG RINGS (PACKED BED Z = 4500 mm)', sz=3.7, bold=True)
    
    # Dimensions & Annotations
    cad_dim_h(ax, CX_1 - R_1, CX_1 + R_1, y_pack_b + 1.15, 'VESSEL ID 750 mm')
    cad_dim_v(ax, CX_1 - R_1 - 0.40, grid_base_y, grid_base_y + h_chim, '120', text_offset=-0.22)
    cad_dim_v(ax, CX_1 + R_1 + 0.35, y_bm_btm, y_bm_top, '100', text_offset=0.22)
    
    # ─────────────────────────────────────────────────────────────────────────
    # VIEW 2: SUPPORT GRID (TOP PLAN VIEW)
    # ─────────────────────────────────────────────────────────────────────────
    cad_rect(ax, 10.4, 11.8, 9.2, 8.4, lw=0.9, fill=True)
    cad_text(ax, 15.0, 19.8, 'VIEW 2 — SUPPORT GRID (TOP PLAN VIEW)', sz=5.8, bold=True)
    cad_text(ax, 15.0, 19.35, 'SEGMENTAL PANELS & STRUCTURAL BEARING — SCALE 1:20', sz=4.5, bold=True)
    
    CX_2 = 15.0
    CY_2 = 15.35
    R_2 = 3.2   # Shell ID 750 mm scaled
    
    # Shell wall (Outer ring & Inner ring)
    cad_circle(ax, CX_2, CY_2, R_2 + 0.14, lw=0.9, fill=True) # Shell OD
    cad_circle(ax, CX_2, CY_2, R_2, lw=1.1, fill=True)        # Shell ID 750
    cad_circle(ax, CX_2, CY_2, R_2 - 0.44, lw=0.75)           # Ledge Ring ID 650
    
    # Centerlines
    cad_line(ax, CX_2 - R_2 - 0.45, CY_2, CX_2 + R_2 + 0.45, CY_2, lw=0.35, ls='-.')
    cad_line(ax, CX_2, CY_2 - R_2 - 0.45, CX_2, CY_2 + R_2 + 0.45, lw=0.35, ls='-.')
    
    # 8 Radial Support Gussets underneath (shown dashed)
    for ang in np.linspace(0, 2*np.pi, 8, endpoint=False):
        gx1 = CX_2 + (R_2 - 0.44) * np.cos(ang)
        gy1 = CY_2 + (R_2 - 0.44) * np.sin(ang)
        gx2 = CX_2 + R_2 * np.cos(ang)
        gy2 = CY_2 + R_2 * np.sin(ang)
        cad_line(ax, gx1, gy1, gx2, gy2, lw=0.55, ls='--')
    
    # Central Support Beam Footprint (ISMB 100 x 50 running vertically)
    bw = 0.45  # Flange width 50 mm
    cad_rect(ax, CX_2 - bw/2, CY_2 - R_2 + 0.05, bw, 2 * R_2 - 0.10, lw=0.9, fill=True)
    # Beam web dashed lines
    cad_line(ax, CX_2 - 0.05, CY_2 - R_2 + 0.05, CX_2 - 0.05, CY_2 + R_2 - 0.05, lw=0.5, ls='--')
    cad_line(ax, CX_2 + 0.05, CY_2 - R_2 + 0.05, CX_2 + 0.05, CY_2 + R_2 - 0.05, lw=0.5, ls='--')
    cad_text(ax, CX_2, CY_2 + 0.55, 'MAIN BEAM\nISMB 100', sz=3.8, bold=True, bg='white')
    
    # Segmental Panel Split Lines (Panels sized to pass through DN 450 manway)
    split_x1 = CX_2 - 1.15
    split_x2 = CX_2 + 1.15
    cad_line(ax, split_x1, CY_2 - np.sqrt(max(0, R_2**2 - 1.15**2)), split_x1, CY_2 + np.sqrt(max(0, R_2**2 - 1.15**2)), lw=0.8, ls=':')
    cad_line(ax, split_x2, CY_2 - np.sqrt(max(0, R_2**2 - 1.15**2)), split_x2, CY_2 + np.sqrt(max(0, R_2**2 - 1.15**2)), lw=0.8, ls=':')
    cad_text(ax, split_x1 - 0.75, CY_2 - 1.85, 'PANEL 1', sz=3.5, bold=True, bg='white')
    cad_text(ax, CX_2, CY_2 - 1.85, 'PANEL 2 (CTR)', sz=3.5, bold=True, bg='white')
    cad_text(ax, split_x2 + 0.75, CY_2 - 1.85, 'PANEL 3', sz=3.5, bold=True, bg='white')
    
    # Corrugated Slotted Chimney Louvers pattern across panels
    for px in np.linspace(CX_2 - R_2 + 0.5, CX_2 + R_2 - 0.5, 7):
        if abs(px - CX_2) > 0.35:
            chord = 2 * np.sqrt(max(0, (R_2 - 0.44)**2 - (px - CX_2)**2))
            cad_rect(ax, px - 0.16, CY_2 - chord/2, 0.32, chord, lw=0.65, fill=True)
            for sy in np.linspace(CY_2 - chord/2 + 0.35, CY_2 + chord/2 - 0.35, 4):
                cad_line(ax, px - 0.12, sy, px + 0.12, sy, lw=0.45)
    
    # 8 Perimeter Hold-Down Clamps with M16 studs
    for ang in np.linspace(np.pi/8, 2*np.pi + np.pi/8, 8, endpoint=False):
        bx = CX_2 + (R_2 - 0.22) * np.cos(ang)
        by = CY_2 + (R_2 - 0.22) * np.sin(ang)
        cad_circle(ax, bx, by, 0.08, fill=True, fc='white', ec=BK, lw=0.7)
        cad_circle(ax, bx, by, 0.03, fill=True, fc=BK)
    cad_text(ax, CX_2 + R_2 - 0.40, CY_2 + R_2 - 0.25, '8x M16 HOLD-DOWN CLAMPS', sz=3.6, bold=True)
    cad_dim_h(ax, CX_2 - R_2, CX_2 + R_2, CY_2 + R_2 + 0.38, 'ID 750 mm')
    
    # ─────────────────────────────────────────────────────────────────────────
    # VIEW 3: CYLINDRICAL SKIRT & FOUNDATION ANCHORAGE
    # ─────────────────────────────────────────────────────────────────────────
    cad_rect(ax, 0.8, 3.4, 9.2, 8.0, lw=0.9, fill=True)
    cad_text(ax, 5.4, 11.0, 'VIEW 3 — CYLINDRICAL SKIRT & BASE RING', sz=5.8, bold=True)
    cad_text(ax, 5.4, 10.55, 'ANCHOR BOLTS & FOUNDATION CHAIRS — SCALE 1:20', sz=4.5, bold=True)
    
    CX_3 = 5.4
    CY_GND_3 = 4.8
    R_SK_3 = 3.3   # Skirt OD 750 mm scaled
    R_BR_3 = 4.6   # Base ring OD 1050 mm scaled
    sk_top_3 = 9.8  # Skirt height 1800 mm scaled
    
    # Concrete Foundation Block (M25 Grade)
    cad_rect(ax, CX_3 - 4.4, 3.5, 8.8, CY_GND_3 - 3.5, lw=0.9, fill=True)
    cad_hatch_rect(ax, CX_3 - 4.4, 3.5, 8.8, CY_GND_3 - 3.5, pitch=0.18, angle=-45, lw=0.25)
    cad_line(ax, CX_3 - 4.5, CY_GND_3, CX_3 + 4.5, CY_GND_3, lw=1.0)
    cad_text(ax, CX_3, 3.75, 'REINFORCED CONCRETE FOUNDATION PIER (M25 GRADE)', sz=3.6, bold=True)
    
    # Non-Shrink Grout Layer (25 mm) with 45° chamfered edge
    cad_rect(ax, CX_3 - R_BR_3 - 0.15, CY_GND_3, 2 * (R_BR_3 + 0.15), 0.15, lw=0.7, fill=True)
    cad_line(ax, CX_3 - R_BR_3 - 0.25, CY_GND_3, CX_3 - R_BR_3 - 0.15, CY_GND_3 + 0.15, lw=0.6)
    cad_line(ax, CX_3 + R_BR_3 + 0.25, CY_GND_3, CX_3 + R_BR_3 + 0.15, CY_GND_3 + 0.15, lw=0.6)
    
    # Annular Base Ring (OD 1050 mm x ID 730 mm x 20 mm plate)
    cad_rect(ax, CX_3 - R_BR_3, CY_GND_3 + 0.15, 2 * R_BR_3, 0.18, lw=0.9, fill=True)
    
    # Cylindrical Skirt Shell (SA-36 Steel, 10 mm wall, 1800 mm height)
    cad_line(ax, CX_3 - R_SK_3, CY_GND_3 + 0.33, CX_3 - R_SK_3, sk_top_3, lw=1.1)
    cad_line(ax, CX_3 + R_SK_3, CY_GND_3 + 0.33, CX_3 + R_SK_3, sk_top_3, lw=1.1)
    cad_line(ax, CX_3 - R_SK_3 + 0.08, CY_GND_3 + 0.33, CX_3 - R_SK_3 + 0.08, sk_top_3, lw=0.45)
    cad_line(ax, CX_3 + R_SK_3 - 0.08, CY_GND_3 + 0.33, CX_3 + R_SK_3 - 0.08, sk_top_3, lw=0.45)
    cad_line(ax, CX_3, CY_GND_3, CX_3, sk_top_3 + 0.6, lw=0.35, ls='-.')
    
    # Bottom Dished Head (2:1 Ellipsoidal) & Weld Junction
    cad_arc(ax, CX_3, sk_top_3, 2 * R_SK_3, 1.4, theta1=180, theta2=360, lw=1.1)
    cad_arc(ax, CX_3, sk_top_3, 2 * (R_SK_3 - 0.08), 1.25, theta1=180, theta2=360, lw=0.55)
    # Weld seam indicator
    cad_circle(ax, CX_3 - R_SK_3, sk_top_3, 0.07, fill=True, fc=BK)
    cad_circle(ax, CX_3 + R_SK_3, sk_top_3, 0.07, fill=True, fc=BK)
    cad_text(ax, CX_3, sk_top_3 - 0.40, 'HEAD-TO-SKIRT FULL PENETRATION BUTT WELD', sz=3.6, bold=True)
    
    # Skirt Access Opening DN 400 (16") with Reinforcing Collar
    y_acc = CY_GND_3 + 2.0
    cad_circle(ax, CX_3, y_acc, 0.70, lw=0.85, fill=True)
    cad_circle(ax, CX_3, y_acc, 0.85, lw=0.55) # Repad collar
    cad_text(ax, CX_3, y_acc, 'SKIRT ACCESS\nDN 400 (16")', sz=3.6, bold=True)
    
    # Two DN 50 (2") Vapor Vent Holes at 180° opposite
    cad_circle(ax, CX_3 - R_SK_3 + 0.25, sk_top_3 - 0.6, 0.10, lw=0.75, fill=True)
    cad_circle(ax, CX_3 + R_SK_3 - 0.25, sk_top_3 - 0.6, 0.10, lw=0.75, fill=True)
    cad_text(ax, CX_3, sk_top_3 - 0.95, '2x DN50 VAPOR VENT HOLES (180 DEG OPPOSITE)', sz=3.4, bold=True)
    
    # Structural Anchor Bolt Chairs (8x M24 SA-193 B7 on 950 mm BC    cad_text(ax, CX_3 + 2.6, CY_GND_3 + 2.8, '8x M24 ANCHOR BOLTS\nON 950 mm BCD', sz=3.5, bold=True, bg='white')
    cad_dim_h(ax, CX_3 - R_BR_3, CX_3 + R_BR_3, CY_GND_3 + 0.60, 'BASE RING OD 1050 mm')
    cad_dim_v(ax, 1.45, CY_GND_3 + 0.33, sk_top_3, 'SKIRT 1800 mm', text_offset=0.0)
    
    # ─────────────────────────────────────────────────────────────────────────
    # VIEW 4: HIGH-MAGNIFICATION STRUCTURAL CONNECTION DETAILS (SCALE 1:5)
    # ─────────────────────────────────────────────────────────────────────────
    cad_rect(ax, 10.4, 3.4, 9.2, 8.0, lw=0.9, fill=True)
    cad_text(ax, 15.0, 11.0, 'VIEW 4 — STRUCTURAL FABRICATION & CONNECTION DETAILS', sz=5.8, bold=True)
    cad_text(ax, 15.0, 10.55, 'DETAIL A: ANCHOR CHAIR | DETAIL B: SUPPORT LEDGE — SCALE 1:5', sz=4.5, bold=True)
    
    # Sub-divider line between Detail A and Detail B
    cad_line(ax, 10.4, 7.2, 19.6, 7.2, lw=0.7)
    
    # ── DETAIL A: ANCHOR BOLT CHAIR & BASE RING CROSS-SECTION (Top Half: Y = 7.2 to 10.4) ──
    cad_text(ax, 15.0, 10.15, 'DETAIL A — ANCHOR BOLT CHAIR & FOUNDATION CONNECTION', sz=4.8, bold=True)
    
    DA_X = 14.8
    DA_Y = 7.55
    
    # Foundation concrete & Grout
    cad_rect(ax, DA_X - 1.8, DA_Y, 3.6, 0.35, lw=0.8, fill=True)
    cad_hatch_rect(ax, DA_X - 1.8, DA_Y, 3.6, 0.35, pitch=0.14, angle=-45, lw=0.25)
    cad_rect(ax, DA_X - 1.8, DA_Y + 0.35, 3.6, 0.20, lw=0.7, fill=True) # 25 mm Grout
    
    # Base Ring plate (20 mm SA-36)
    cad_rect(ax, DA_X - 1.6, DA_Y + 0.55, 3.2, 0.25, lw=0.9, fill=True)
    
    # Skirt Shell Wall (10 mm SA-36) on left
    cad_rect(ax, DA_X - 1.1, DA_Y + 0.80, 0.18, 1.45, lw=0.9, fill=True)
    
    # Chair Vertical Gusset Plate (10 mm)
    p_cgus = [(DA_X - 0.92, DA_Y + 0.80), (DA_X + 0.95, DA_Y + 0.80), (DA_X + 0.95, DA_Y + 1.55), (DA_X - 0.92, DA_Y + 1.55)]
    ax.add_patch(Polygon(p_cgus, closed=True, fc='white', ec=BK, lw=0.85))
    
    # Chair Top Bearing Plate (16 mm SA-36 with clearance hole)
    cad_rect(ax, DA_X - 0.95, DA_Y + 1.55, 2.0, 0.20, lw=0.9, fill=True)
    
    # M24 Anchor Bolt (SA-193 B7) with Spherical Washer & Double Nuts
    bx_da = DA_X + 0.05
    cad_line(ax, bx_da, DA_Y - 0.2, bx_da, DA_Y + 2.25, lw=1.1)
    # Pipe Sleeve (DN50 x 300 mm) in concrete
    cad_rect(ax, bx_da - 0.20, DA_Y, 0.40, 0.35, lw=0.6, ls='--', fill=True)
    # Heavy hex nut + locknut
    cad_rect(ax, bx_da - 0.18, DA_Y + 1.75, 0.36, 0.16, lw=0.75, fill=True)
    cad_rect(ax, bx_da - 0.18, DA_Y + 1.91, 0.36, 0.14, lw=0.75, fill=True)
    
    # Left-Side Callouts (Right-aligned at X = 13.0, leaders to targets)
    cad_text(ax, 13.0, DA_Y + 1.60, 'SKIRT SHELL (10 mm)', sz=3.3, bold=True, ha='right')
    cad_line(ax, 13.1, DA_Y + 1.60, DA_X - 1.1, DA_Y + 1.60, lw=0.5)
    cad_text(ax, 13.0, DA_Y + 0.70, 'BASE RING (20 mm)', sz=3.3, bold=True, ha='right')
    cad_line(ax, 13.1, DA_Y + 0.70, DA_X - 1.6, DA_Y + 0.70, lw=0.5)
    cad_text(ax, 13.0, DA_Y + 0.45, '25 mm GROUT', sz=3.3, bold=True, ha='right')
    cad_line(ax, 13.1, DA_Y + 0.45, DA_X - 1.8, DA_Y + 0.45, lw=0.5)
    
    # Right-Side Callouts (Left-aligned at X = 16.6, leaders to targets)
    cad_text(ax, 16.6, DA_Y + 1.98, 'M24 DBL NUTS + WASHER', sz=3.3, bold=True, ha='left')
    cad_line(ax, 16.5, DA_Y + 1.98, bx_da + 0.18, DA_Y + 1.98, lw=0.5)
    cad_text(ax, 16.6, DA_Y + 1.65, 'TOP CHAIR PLT (16 mm)', sz=3.3, bold=True, ha='left')
    cad_line(ax, 16.5, DA_Y + 1.65, DA_X + 1.05, DA_Y + 1.65, lw=0.5)
    cad_text(ax, 16.6, DA_Y + 1.20, 'GUSSET (10 mm)', sz=3.3, bold=True, ha='left')
    cad_line(ax, 16.5, DA_Y + 1.20, DA_X + 0.95, DA_Y + 1.20, lw=0.5)
    cad_text(ax, 16.6, DA_Y + 0.20, 'DN50 SLEEVE IN CONCRETE', sz=3.3, bold=True, ha='left')
    cad_line(ax, 16.5, DA_Y + 0.20, bx_da + 0.20, DA_Y + 0.20, lw=0.5)
    
    # ── DETAIL B: SUPPORT LEDGE RING & BEAM BEARING DETAIL (Bottom Half: Y = 3.4 to 7.2) ──
    cad_text(ax, 15.0, 6.95, 'DETAIL B — SUPPORT LEDGE RING & BEAM END BEARING', sz=4.8, bold=True)
    
    DB_X = 14.4
    DB_Y = 3.7
    
    # Column Shell Wall (SA-516 Gr 70, 10 mm) + PVDF Liner (3 mm)
    cad_rect(ax, DB_X - 3.4, DB_Y, 0.22, 2.7, lw=1.0, fill=True)
    cad_hatch_rect(ax, DB_X - 3.4, DB_Y, 0.22, 2.7, pitch=0.12, angle=45, lw=0.25)
    cad_rect(ax, DB_X - 3.18, DB_Y, 0.08, 2.7, lw=0.8, fill=True) # PVDF liner
    
    # Support Ledge Ring (50x15 mm flat bar)
    y_led_db = DB_Y + 1.15
    cad_rect(ax, DB_X - 3.10, y_led_db, 1.25, 0.20, lw=0.9, fill=True)
    # Triangular Gusset (100x50x10 mm)
    p_gus_db = [(DB_X - 3.10, y_led_db), (DB_X - 1.85, y_led_db), (DB_X - 3.10, y_led_db - 0.90)]
    ax.add_patch(Polygon(p_gus_db, closed=True, fc='white', ec=BK, lw=0.85))
    
    # Central Beam Bearing Seat Bracket & Slotted Hole for Thermal Expansion
    cad_rect(ax, DB_X - 1.85, y_led_db - 0.65, 0.80, 0.12, lw=0.8, fill=True) # Seat angle
    # Beam ISMB 100 resting on bracket
    cad_rect(ax, DB_X - 1.85, y_led_db - 0.53, 2.8, 0.12, lw=0.8, fill=True) # Bottom flange
    cad_rect(ax, DB_X - 0.5, y_led_db - 0.41, 0.14, 0.66, lw=0.7, fill=True) # Web
    cad_rect(ax, DB_X - 1.85, y_led_db + 0.25, 2.8, 0.12, lw=0.8, fill=True) # Top flange
    
    # Chimney plate bottom flange and clamping clip with J-bolt
    cad_rect(ax, DB_X - 3.00, y_led_db + 0.20, 1.1, 0.10, lw=0.75, fill=True) # Grid flange
    cad_rect(ax, DB_X - 3.00, y_led_db + 0.30, 0.70, 0.08, lw=0.8, fill=True) # Clamp bar
    cad_line(ax, DB_X - 2.65, y_led_db - 0.15, DB_X - 2.65, y_led_db + 0.50, lw=0.75) # J-bolt
    
    # Clean Detail B Callouts (Structured column at X = 15.6, left-aligned)
    cad_text(ax, 15.6, DB_Y + 2.50, '10 mm SHELL + 3 mm PVDF LINER', sz=3.2, bold=True, ha='left')
    cad_line(ax, 15.5, DB_Y + 2.50, DB_X - 3.2, DB_Y + 2.50, lw=0.5)
    
    cad_text(ax, 15.6, DB_Y + 2.05, 'CLAMP BAR & M16 J-BOLT', sz=3.2, bold=True, ha='left')
    cad_line(ax, 15.5, DB_Y + 2.05, DB_X - 2.65, y_led_db + 0.35, lw=0.5)
    
    cad_text(ax, 15.6, DB_Y + 1.55, '50x15 mm LEDGE RING', sz=3.2, bold=True, ha='left')
    cad_line(ax, 15.5, DB_Y + 1.55, DB_X - 2.4, y_led_db + 0.10, lw=0.5)
    
    cad_text(ax, 15.6, DB_Y + 1.15, 'ISMB 100 SUPPORT BEAM', sz=3.3, bold=True, ha='left')
    cad_line(ax, 15.5, DB_Y + 1.15, DB_X + 0.2, y_led_db + 0.31, lw=0.5)
    
    cad_text(ax, 15.6, DB_Y + 0.65, '10 mm RADIAL GUSSET (8 PLACES)', sz=3.2, bold=True, ha='left')
    cad_line(ax, 15.5, DB_Y + 0.65, DB_X - 2.4, y_led_db - 0.45, lw=0.5)
    
    cad_text(ax, 15.6, DB_Y + 0.15, 'SLOTTED HOLE (20x35 mm) / THERMAL SLIDE', sz=3.2, bold=True, ha='left')
    cad_line(ax, 15.5, DB_Y + 0.15, DB_X - 1.4, y_led_db - 0.47, lw=0.5)
    
    # ═════════════════════════════════════════════════════════════════════════
    # RIGHT SIDE: STRUCTURAL SCHEDULES & NOTES (X = 20.0 to 28.9)
    # ═════════════════════════════════════════════════════════════════════════
    
    # TABLE 1: STRUCTURAL DESIGN SCHEDULE & LOAD CRITERIA
    T1_X = 20.0
    T1_Y = 12.0
    t1_headers = ['DESIGN PARAMETER', 'VALUE', 'SPECIFICATION / BASIS']
    t1_widths  = [3.1, 2.3, 3.5]
    t1_rows = [
        ['Operating Grid Load',   '16.08 kN (1.64 t)', 'Dry pack + liq holdup + tare'],
        ['Flooded Upset Load',    '26.39 kN (2.69 t)', '100% void flooded emergency'],
        ['Basic Wind Speed (Vb)', '160 km/h (44.4 m/s)','IS 875 (Part 3) / Cat. 2'],
        ['Wind Base Moment',      '18.52 kN*m',        'Calculated at skirt base ring'],
        ['Seismic Design Zone',   'Zone III (Z = 0.16)','IS 1893 (Part 4) / I = 1.5'],
        ['Central Support Beam',  'ISMB 100 x 50',     'SA-36 Steel (Zx = 25.7 cm3)'],
        ['Max Beam Deflection',   '0.32 mm (<0.75 mm)','delta <= L/1000 allowable'],
        ['Foundation Anchorage',  '8x M24 SA-193 B7',  '950 mm BCD (Tension = 14.8 kN)'],
        ['Skirt Shell & Base Plt','SA-36 (10 & 20 mm)','Max comp. stress 12.4 MPa'],
        ['Foundation Bearing',    '1.85 MPa (<6.25)',  'M25 Concrete (Allowable 6.25)'],
    ]
    cad_draw_table_a4(ax, T1_X, T1_Y, t1_headers, t1_rows, t1_widths, row_h=0.38,
                      title='TABLE 1 — PRELIMINARY STRUCTURAL DESIGN BASIS', sz=3.9)
    
    # TABLE 2: BILL OF MATERIALS (BOM) — STRUCTURAL MEMBERS
    T2_X = 20.0
    T2_Y = 7.4
    t2_headers = ['MARK', 'STRUCTURAL ITEM', 'MATERIAL', 'DIMENSIONS / SECTION', 'QTY']
    t2_widths  = [0.9, 3.1, 2.0, 2.1, 0.8]
    t2_rows = [
        ['S1', 'Gas-Injection Support Grid', 'FRP / Ti Gr 2', '740 mm Dia (Slotted Chimney)','1 SET'],
        ['S2', 'Support Ledge Ring',         'SA-516 Gr 70',  '750 OD x 650 ID x 15 mm',    '1 PC'],
        ['S3', 'Ledge Radial Gussets',       'SA-516 Gr 70',  '100 x 50 x 10 mm Plate',     '8 PCS'],
        ['S4', 'Central Support Beam',       'SA-36 Steel',   'ISMB 100 x 50 (L = 740 mm)',  '1 PC'],
        ['S5', 'Beam Bearing Cleats',        'SA-36 Steel',   'L 75 x 75 x 8 x 100 mm',     '2 PCS'],
        ['S6', 'Cylindrical Skirt Shell',    'SA-36 Steel',   '750 OD x 10 mm x 1800 mm',   '1 PC'],
        ['S7', 'Annular Base Ring',          'SA-36 Steel',   '1050 OD x 730 ID x 20 mm',   '1 PC'],
        ['S8', 'Anchor Chair Gussets & Top', 'SA-36 Steel',   '10 mm Gussets / 16 mm Top',  '8 SETS'],
        ['S9', 'Foundation Anchor Bolts',    'SA-193 B7',     'M24 x 600 mm Studs (Dbl Nut)','8 PCS'],
    ]
    cad_draw_table_a4(ax, T2_X, T2_Y, t2_headers, t2_rows, t2_widths, row_h=0.36,
                      title='TABLE 2 — BILL OF MATERIALS (BOM) — STRUCTURAL', sz=3.9)
    
    # STRUCTURAL NOTES (CONCISE INDUSTRIAL CAD NOTES)
    N_X = 20.0
    N_Y = 3.4
    W_N = 8.9
    H_N = 3.6
    cad_rect(ax, N_X, N_Y, W_N, H_N, lw=0.9, fill=True)
    cad_text(ax, N_X + W_N/2, N_Y + H_N - 0.28, 'PRELIMINARY STRUCTURAL FABRICATION & ERECTION NOTES', sz=4.2, bold=True)
    cad_line(ax, N_X, N_Y + H_N - 0.52, N_X + W_N, N_Y + H_N - 0.52, lw=0.6)
    
    notes_dwg3 = [
        "1. PRELIMINARY BASIS: STRUCTURAL SIZING & LOADS ARE ACADEMIC PRELIMINARY",
        "   VALUES AND REQUIRE FINAL MECHANICAL & STRUCTURAL VERIFICATION.",
        "2. WELDING: PER ASME SEC IX & AWS D1.1. SKIRT-TO-HEAD IS FULL-PENETRATION",
        "   BUTT WELD WITH 100% RADIOGRAPHY (ASME UW-11 CAT B).",
        "3. ANCHORAGE: 8x M24 (SA-193 B7) BOLTS TORQUED TO 450 N*m IN STAR PATTERN.",
        "4. GROUT: 25 mm NON-SHRINK GROUT (MIN COMPRESSIVE STRENGTH 50 MPa AT 28 DAYS).",
        "5. EXPANSION: SLOTTED HOLE (20x35 mm) AT BEAM BEARING PERMITS THERMAL SLIDE.",
        "6. SKIRT VENTS: 2x DN50 VENT HOLES AT 180 DEG PREVENT HAZARDOUS GAS POCKETS.",
    ]
    for idx, nl in enumerate(notes_dwg3):
        cad_text(ax, N_X + 0.25, N_Y + H_N - 0.80 - idx * 0.35, nl, sz=3.4, ha='left', bold=(idx in [0, 1, 2]))
    
    # Title Block
    draw_a4_title_block(
        ax,
        dwg_title='PACKED-BED ABSORBER (C-101) — PACKING SUPPORT & SKIRT BASE CAD',
        dwg_no='PEDD-PBA-03',
        scale='1:20 METRIC'
    )
    
    fig.savefig(out_pdf, dpi=300, facecolor='white')
    fig.savefig(out_png, dpi=300, facecolor='white')
    plt.close(fig)
    print(f"SUCCESS: Revamped A4 DWG-03 generated at {out_pdf}")

if __name__ == '__main__':
    out_dir = r'd:\GAMES\zercxes\CAD_Engineering_Drawings\Packed_Bed_Absorber_Drawings'
    os.makedirs(out_dir, exist_ok=True)
    p_pdf = os.path.join(out_dir, '03_Packed_Bed_Absorber_Packing_Support_Details_CAD.pdf')
    p_png = os.path.join(out_dir, '03_Packed_Bed_Absorber_Packing_Support_Details_CAD.png')
    generate_a4_dwg03(p_pdf, p_png)
