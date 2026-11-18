"""
DWG-03: MECHANICAL FABRICATION & ASME SECTION VIII DETAILS
VAPOR-PHASE ETHYLENE OXIDATION MULTI-TUBULAR REACTOR (R-201)
ASME SEC VIII DIV 1 (UW-20, UG-32, UG-37) CLOSE-UP ENGINEERING DETAILS:
TUBE-TO-TUBESHEET WELD, 2:1 ELLIPSOIDAL HEAD, SKIRT CHAIR & CATALYST GRID
STUDENT: SOURISH SENAPATI | ROLL: 002310301035 | DATE: 17/11/2026
SUBJECT: CHEMICAL REACTION ENGINEERING - II / PEDD | JADAVPUR UNIVERSITY
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon, Arc, PathPatch
from matplotlib.path import Path as MPath

from cad_common import (
    create_cad_canvas, draw_sheet_border, draw_title_block,
    cad_line, cad_rect, cad_circle, cad_arc, cad_text, cad_arrow,
    cad_dim_h, cad_dim_v, cad_dim_leader, cad_balloon, cad_flange,
    cad_hatch_rect, cad_draw_table, W, H, BK, GREY
)

def generate_reactor_dwg03(out_pdf, out_png):
    fig, ax = create_cad_canvas()
    draw_sheet_border(ax)

    # ═════════════════════════════════════════════════════════════════════════
    # HEADER BANNER
    # ═════════════════════════════════════════════════════════════════════════
    cad_text(ax, W / 2.0, H - 2.0, 'TRIPLE-EFFECT / MULTI-STAGE MECHANICAL FABRICATION & PRESSURE VESSEL DETAILS', sz=10.5, bold=True)
    cad_text(ax, W / 2.0, H - 2.8, 'VAPOR-PHASE ETHYLENE OXIDATION MULTI-TUBULAR REACTOR (R-201) — ASME SECTION VIII DIV 1 CODE DETAILS', sz=7.8, bold=True, color='#0a3d62')
    cad_line(ax, 8.0, H - 3.4, W - 8.0, H - 3.4, lw=1.2, color='#2980b9')

    # ═════════════════════════════════════════════════════════════════════════
    # DETAIL A: TUBE-TO-TUBESHEET JOINT (Top-Left: X = 4.0 to 38.0, Y = 32.0 to 52.0)
    # ═════════════════════════════════════════════════════════════════════════
    ax1_cx, ax1_cy = 19.0, 42.0
    cad_text(ax, ax1_cx, 51.5, 'DETAIL A — TUBE-TO-TUBESHEET JOINT (ASME SEC VIII DIV 1 UW-20)', sz=8.5, bold=True)
    cad_text(ax, ax1_cx, 50.3, 'ROLLER EXPANDED WITH DOUBLE SERRATION GROOVES & STRENGTH SEAL FILLET WELD', sz=6.5, bold=True, color='#2c3e50')

    # Tubesheet block (75 mm thick = 6.0 cm scaled, width = 18.0 cm)
    ts_w, ts_h = 16.0, 6.0
    cad_rect(ax, ax1_cx - ts_w / 2.0, ax1_cy - ts_h / 2.0, ts_w, ts_h, lw=1.2, fill=True, fc='#dcdde1')
    cad_hatch_rect(ax, ax1_cx - ts_w / 2.0, ax1_cy - ts_h / 2.0, ts_w, ts_h, pitch=0.45, angle=45, lw=0.35, color='#7f8c8d')
    
    # Explosion clad layer on top of tubesheet (6 mm clad = 0.5 cm scaled)
    cad_rect(ax, ax1_cx - ts_w / 2.0, ax1_cy + ts_h / 2.0 - 0.5, ts_w, 0.5, lw=0.8, fill=True, fc='#bdc3c7')
    
    # Tube Hole in Tubesheet (OD = 48.26 mm -> 3.8 cm scaled, ID = 38.10 mm -> 3.0 cm scaled)
    t_od_sc = 3.8
    t_id_sc = 3.0
    cad_rect(ax, ax1_cx - t_od_sc / 2.0, ax1_cy - ts_h / 2.0 - 4.0, t_od_sc, ts_h + 4.0 + 0.3, lw=0.0, fill=True, fc='#ffffff')
    
    # Schedule 80 Tube Walls passing through hole
    wall_sc = (t_od_sc - t_id_sc) / 2.0
    # Left tube wall
    cad_rect(ax, ax1_cx - t_od_sc / 2.0, ax1_cy - ts_h / 2.0 - 4.0, wall_sc, ts_h + 4.3, lw=1.0, fill=True, fc='#bdc3c7')
    cad_hatch_rect(ax, ax1_cx - t_od_sc / 2.0, ax1_cy - ts_h / 2.0 - 4.0, wall_sc, ts_h + 4.3, pitch=0.25, angle=-45, lw=0.3)
    # Right tube wall
    cad_rect(ax, ax1_cx + t_id_sc / 2.0, ax1_cy - ts_h / 2.0 - 4.0, wall_sc, ts_h + 4.3, lw=1.0, fill=True, fc='#bdc3c7')
    cad_hatch_rect(ax, ax1_cx + t_id_sc / 2.0, ax1_cy - ts_h / 2.0 - 4.0, wall_sc, ts_h + 4.3, pitch=0.25, angle=-45, lw=0.3)
    
    # Tube Centerline
    cad_line(ax, ax1_cx, ax1_cy - ts_h / 2.0 - 4.5, ax1_cx, ax1_cy + ts_h / 2.0 + 2.0, lw=0.45, ls='dashdot', color='#c0392b')
    
    # Double Serration Grooves in Tubesheet Hole (0.4 mm D x 3.0 mm W)
    g_h = 0.4
    g_w = 0.25
    # Groove 1 (Lower)
    cad_rect(ax, ax1_cx - t_od_sc / 2.0 - g_w, ax1_cy - 0.8 - g_h / 2.0, g_w, g_h, lw=0.8, fill=True, fc='#111111')
    cad_rect(ax, ax1_cx + t_od_sc / 2.0, ax1_cy - 0.8 - g_h / 2.0, g_w, g_h, lw=0.8, fill=True, fc='#111111')
    # Groove 2 (Upper)
    cad_rect(ax, ax1_cx - t_od_sc / 2.0 - g_w, ax1_cy + 0.8 - g_h / 2.0, g_w, g_h, lw=0.8, fill=True, fc='#111111')
    cad_rect(ax, ax1_cx + t_od_sc / 2.0, ax1_cy + 0.8 - g_h / 2.0, g_w, g_h, lw=0.8, fill=True, fc='#111111')
    
    # Strength Seal Fillet Weld (TIG) at Tube Projection (Triangular fillets)
    weld_sz = 0.45
    p_w1 = [(ax1_cx - t_od_sc / 2.0, ax1_cy + ts_h / 2.0),
            (ax1_cx - t_od_sc / 2.0 - weld_sz, ax1_cy + ts_h / 2.0),
            (ax1_cx - t_od_sc / 2.0, ax1_cy + ts_h / 2.0 + 0.3)]
    ax.add_patch(Polygon(p_w1, closed=True, fc='#111111', ec=BK, lw=0.8))
    
    p_w2 = [(ax1_cx + t_od_sc / 2.0, ax1_cy + ts_h / 2.0),
            (ax1_cx + t_od_sc / 2.0 + weld_sz, ax1_cy + ts_h / 2.0),
            (ax1_cx + t_od_sc / 2.0, ax1_cy + ts_h / 2.0 + 0.3)]
    ax.add_patch(Polygon(p_w2, closed=True, fc='#111111', ec=BK, lw=0.8))

    # Detail A Callouts & Leaders
    cad_dim_leader(ax, ax1_cx - t_od_sc / 2.0 - weld_sz / 2.0, ax1_cy + ts_h / 2.0 + 0.15,
                   ax1_cx - 4.5, ax1_cy + ts_h / 2.0 + 1.8, ax1_cx - 7.5,
                   'FULL PENETRATION STRENGTH SEAL WELD (TIG)', sz=5.5)
    
    cad_dim_leader(ax, ax1_cx - t_od_sc / 2.0 - g_w / 2.0, ax1_cy + 0.8,
                   ax1_cx - 4.5, ax1_cy + 0.8, ax1_cx - 7.5,
                   'DOUBLE SERRATION GROOVES (0.4 MM D x 3 MM W)\nFOR HIGH PRESSURE TIGHTNESS (25 ATM)', sz=5.0)
    
    cad_dim_leader(ax, ax1_cx + ts_w / 2.0 - 2.0, ax1_cy,
                   ax1_cx + 5.5, ax1_cy + 1.2, ax1_cx + 7.5,
                   '75 MM THK TUBESHEET (SA-266 CL 2)\n+ 6 MM EXPLOSION BONDED CLAD', sz=5.2)
    
    cad_dim_leader(ax, ax1_cx + t_od_sc / 2.0 - wall_sc / 2.0, ax1_cy - 2.5,
                   ax1_cx + 5.5, ax1_cy - 2.5, ax1_cx + 7.5,
                   '1.5" SCH 80 SEAMLESS TUBE (SA-214)\nOD = 48.26 MM, ID = 38.10 MM, TW = 5.08 MM', sz=5.2)

    # ═════════════════════════════════════════════════════════════════════════
    # DETAIL B: 2:1 ELLIPSOIDAL DISHED HEAD FORMING GEOMETRY (Top-Right: X = 46.0 to 80.0, Y = 32.0 to 52.0)
    # ═════════════════════════════════════════════════════════════════════════
    ax2_cx, ax2_cy = 63.0, 41.5
    cad_text(ax, ax2_cx, 51.5, 'DETAIL B — ASME 2:1 ELLIPSOIDAL DISHED HEAD & NOZZLE REINFORCEMENT', sz=8.5, bold=True)
    cad_text(ax, ax2_cx, 50.3, 'STANDARDIZED ASME CODE RATIOS: Rc = 0.90 Do, rk = 0.17 Do, NOZZLE RF PAD PER UG-37', sz=6.5, bold=True, color='#2c3e50')

    # Half Head Elevation Profile
    hd_w = 12.0   # Scaled radius = 6.0 cm (Do = 2,134 mm)
    hd_h = 5.5    # Dish depth = Do / 4 = 533 mm
    
    # Dished Head Arc
    ax.add_patch(Arc((ax2_cx, ax2_cy), hd_w * 2.0, hd_h * 2.0, theta1=0, theta2=180, ec=BK, lw=1.4))
    cad_line(ax, ax2_cx - hd_w, ax2_cy, ax2_cx + hd_w, ax2_cy, lw=0.6, ls='--')
    cad_line(ax, ax2_cx, ax2_cy - 1.0, ax2_cx, ax2_cy + hd_h + 4.5, lw=0.45, ls='dashdot', color='#c0392b')
    
    # Straight flange (2" = 50 mm -> 0.8 cm scaled)
    cad_line(ax, ax2_cx - hd_w, ax2_cy, ax2_cx - hd_w, ax2_cy - 0.8, lw=1.4)
    cad_line(ax, ax2_cx + hd_w, ax2_cy, ax2_cx + hd_w, ax2_cy - 0.8, lw=1.4)
    
    # Shell to head weld joint (Circumferential Category B seam)
    cad_line(ax, ax2_cx - hd_w - 0.4, ax2_cy - 0.8, ax2_cx - hd_w + 0.4, ax2_cy - 0.8, lw=0.8, ls=':')
    cad_line(ax, ax2_cx + hd_w - 0.4, ax2_cy - 0.8, ax2_cx + hd_w + 0.4, ax2_cy - 0.8, lw=0.8, ls=':')
    
    # 14" Nozzle Neck N1 welded at apex
    noz_w_d = 2.4
    noz_h_d = 3.2
    cad_rect(ax, ax2_cx - noz_w_d / 2.0, ax2_cy + hd_h - 0.3, noz_w_d, noz_h_d, lw=1.1, fill=True, fc='#ffffff')
    cad_flange(ax, ax2_cx, ax2_cy + hd_h - 0.3 + noz_h_d, orientation='V', length=noz_w_d * 1.5, thickness=0.35, lw=1.2)
    
    # ASME UG-37 Reinforcing Pad (Donut plate surrounding nozzle)
    rf_w = 4.8
    rf_thk = 0.35
    cad_rect(ax, ax2_cx - rf_w / 2.0, ax2_cy + hd_h - 0.5, rf_w, rf_thk, lw=0.9, fill=True, fc='#dcdde1')
    cad_circle(ax, ax2_cx + 1.8, ax2_cy + hd_h - 0.5 + rf_thk / 2.0, 0.08, fill=True, fc='#111111')
    
    # Dimensions on Detail B
    cad_dim_h(ax, ax2_cx - hd_w, ax2_cx + hd_w, ax2_cy - 1.4, 'OUTSIDE DIAMETER Do = 86.00" (2,184 MM)', ext=0.4, sz=5.5)
    cad_dim_v(ax, ax2_cx + hd_w + 1.2, ax2_cy, ax2_cy + hd_h, 'DISH DEPTH h = Do/4 = 21.50" (546 MM)', ext=0.4, sz=5.2)
    
    # Geometry Leaders
    cad_dim_leader(ax, ax2_cx - hd_w + 1.0, ax2_cy + 1.2,
                   ax2_cx - hd_w - 2.5, ax2_cy + 3.0, ax2_cx - hd_w - 4.5,
                   'KNUCKLE RADIUS rk = 0.17 Do = 14.62" (371 MM)\n(PREVENTS STRESS CONCENTRATION)', sz=5.0)
    
    cad_dim_leader(ax, ax2_cx + 2.5, ax2_cy + hd_h * 0.7,
                   ax2_cx + 5.5, ax2_cy + hd_h * 0.7 + 1.5, ax2_cx + 8.5,
                   'DISH CROWN RADIUS Rc = 0.90 Do = 77.40" (1,966 MM)\nSA-516 GR 70 KILLED CS (1.00" THK)', sz=5.0)
    
    cad_dim_leader(ax, ax2_cx + 1.8, ax2_cy + hd_h - 0.5 + rf_thk / 2.0,
                   ax2_cx + 4.5, ax2_cy + hd_h + 1.2, ax2_cx + 7.5,
                   'REINFORCING PAD PER ASME UG-37 (1.00" THK)\nWITH 1/8" NPT TELLTALE WEEP HOLE', sz=5.0)

    # ═════════════════════════════════════════════════════════════════════════
    # DETAIL C: VESSEL SKIRT SUPPORT & ANCHOR BOLT CHAIR (Bottom-Left: X = 4.0 to 38.0, Y = 7.0 to 28.0)
    # ═════════════════════════════════════════════════════════════════════════
    ax3_cx, ax3_cy = 19.0, 16.5
    cad_text(ax, ax3_cx, 28.5, 'DETAIL C — VESSEL SKIRT SUPPORT & ANCHOR BOLT CHAIR DETAIL', sz=8.5, bold=True)
    cad_text(ax, ax3_cx, 27.3, 'FABRICATED STEEL ANCHOR CHAIR ON REINFORCED CONCRETE FOUNDATION SLAB', sz=6.5, bold=True, color='#2c3e50')

    # Foundation Concrete (Grade M30)
    fnd_w, fnd_h = 18.0, 2.5
    fnd_top = ax3_cy - 4.5
    cad_rect(ax, ax3_cx - fnd_w / 2.0, fnd_top - fnd_h, fnd_w, fnd_h, lw=1.2, fill=True, fc='#f1f2f6')
    cad_hatch_rect(ax, ax3_cx - fnd_w / 2.0, fnd_top - fnd_h, fnd_w, fnd_h, pitch=0.45, angle=45, lw=0.35, color='#7f8c8d')
    cad_line(ax, ax3_cx - fnd_w / 2.0 - 1.0, fnd_top, ax3_cx + fnd_w / 2.0 + 1.0, fnd_top, lw=1.2)
    cad_text(ax, ax3_cx - 5.5, fnd_top - fnd_h / 2.0, 'FOUNDATION CONCRETE (GRADE M30)', sz=5.0, bold=True)
    
    # Non-Shrink Grout Layer (50 mm = 0.6 cm scaled)
    grout_h = 0.6
    cad_rect(ax, ax3_cx - fnd_w / 2.0 + 1.0, fnd_top, fnd_w - 2.0, grout_h, lw=0.8, fill=True, fc='#dcdde1')
    cad_hatch_rect(ax, ax3_cx - fnd_w / 2.0 + 1.0, fnd_top, fnd_w - 2.0, grout_h, pitch=0.25, angle=-45, lw=0.25)
    cad_text(ax, ax3_cx + 4.5, fnd_top + grout_h / 2.0, 'NON-SHRINK GROUT (50 MM)', sz=4.5, bold=True)
    
    # Base Ring (30 mm thk = 0.5 cm scaled, width = 6.0 cm)
    br_top = fnd_top + grout_h
    cad_rect(ax, ax3_cx - 3.5, br_top, 7.0, 0.5, lw=1.0, fill=True, fc='#bdc3c7')
    
    # Skirt Shell Wall (16 mm thk = 0.35 cm scaled)
    skirt_x = ax3_cx + 1.5
    skirt_thk = 0.35
    skirt_h_d = 8.5
    cad_rect(ax, skirt_x, br_top + 0.5, skirt_thk, skirt_h_d, lw=1.1, fill=True, fc='#bdc3c7')
    cad_text(ax, skirt_x + 1.8, br_top + 5.0, 'SKIRT SHELL (16 MM THK)\nSA-36 CARBON STEEL', sz=5.0, bold=True)
    
    # Anchor Chair Gusset Plates (16 mm thk)
    cad_line(ax, ax3_cx - 2.5, br_top + 0.5, ax3_cx - 2.5, br_top + 4.5, lw=1.2)
    cad_line(ax, ax3_cx - 2.5, br_top + 4.5, skirt_x, br_top + 6.0, lw=1.2)
    cad_line(ax, skirt_x, br_top + 6.0, skirt_x, br_top + 0.5, lw=1.2)
    
    # Top Bearing Plate of Chair (30 mm thk)
    cad_rect(ax, ax3_cx - 3.2, br_top + 4.5, 3.5, 0.6, lw=1.0, fill=True, fc='#7f8c8d')
    
    # Heavy-Duty M36 Anchor Bolt (Embedded into concrete)
    bolt_x = ax3_cx - 1.5
    cad_rect(ax, bolt_x - 0.25, fnd_top - 2.2, 0.5, 7.8, lw=0.9, fill=True, fc='#ffffff', zorder=4)
    # Double nuts & washer
    cad_rect(ax, bolt_x - 0.55, br_top + 5.1, 1.1, 0.5, lw=0.8, fill=True, fc='#bdc3c7', zorder=5)
    cad_rect(ax, bolt_x - 0.55, br_top + 5.6, 1.1, 0.5, lw=0.8, fill=True, fc='#bdc3c7', zorder=5)
    cad_circle(ax, bolt_x, br_top + 6.4, 0.22, lw=0.6, fill=False, zorder=5)
    
    # Detail C Callouts
    cad_dim_leader(ax, bolt_x, br_top + 5.85,
                   ax3_cx - 4.5, br_top + 6.5, ax3_cx - 7.5,
                   'M36 ANCHOR BOLT (ASTM A193 B7)\nWITH DOUBLE HEAVY HEX NUTS', sz=5.2)
    
    cad_dim_leader(ax, ax3_cx - 2.0, br_top + 2.5,
                   ax3_cx - 5.5, br_top + 2.5, ax3_cx - 7.5,
                   'CHAIR GUSSET PLATE (16 MM THK SA-36)', sz=5.0)

    # ═════════════════════════════════════════════════════════════════════════
    # DETAIL D: CATALYST RETAINING GRID & LOWER SUPPORT SCREEN (Bottom-Right: X = 46.0 to 80.0, Y = 7.0 to 28.0)
    # ═════════════════════════════════════════════════════════════════════════
    ax4_cx, ax4_cy = 63.0, 16.5
    cad_text(ax, ax4_cx, 28.5, 'DETAIL D — CATALYST SUPPORT GRID & RETAINING MESH DETAIL', sz=8.5, bold=True)
    cad_text(ax, ax4_cx, 27.3, 'SS316 MULTI-LAYER WIRE MESH WITH LOWER PERFORATED SUPPORT GRID & HOLD-DOWN BARS', sz=6.5, bold=True, color='#2c3e50')

    # Reactor Shell Wall at Bottom
    grid_w = 14.0
    sw_x = ax4_cx + grid_w / 2.0
    cad_rect(ax, sw_x, ax4_cy - 5.0, 0.6, 10.0, lw=1.2, fill=True, fc='#bdc3c7')
    cad_text(ax, sw_x + 0.8, ax4_cy + 2.5, 'VESSEL SHELL\n(SA-516 GR 70)', sz=5.0, bold=True)
    
    # Support Ring / Cleat welded to shell
    cad_rect(ax, sw_x - 1.2, ax4_cy - 2.5, 1.2, 0.8, lw=1.0, fill=True, fc='#7f8c8d')
    cad_line(ax, sw_x - 1.2, ax4_cy - 1.7, sw_x, ax4_cy - 1.7, lw=0.6)
    
    # Lower Perforated Support Grid (25 mm x 50 mm flat bars on 50 mm pitch)
    cad_rect(ax, ax4_cx - grid_w / 2.0, ax4_cy - 2.5, grid_w - 1.2, 0.8, lw=1.1, fill=True, fc='#dcdde1')
    for px_b in np.linspace(ax4_cx - grid_w / 2.0 + 0.8, sw_x - 1.8, 8):
        cad_line(ax, px_b, ax4_cy - 2.5, px_b, ax4_cy - 1.7, lw=0.8)
    cad_text(ax, ax4_cx - 2.0, ax4_cy - 3.2, 'LOWER SUPPORT GRID BARS (25 x 50 MM ON 50 MM PITCH)', sz=4.8, bold=True)
    
    # Knitted Wire Mesh Catalyst Support Screen (SS316 / Monel 400, 20 Mesh)
    cad_rect(ax, ax4_cx - grid_w / 2.0, ax4_cy - 1.7, grid_w - 1.2, 1.8, lw=1.1, fill=True, fc='#fff2cc')
    cad_hatch_rect(ax, ax4_cx - grid_w / 2.0, ax4_cy - 1.7, grid_w - 1.2, 1.8, pitch=0.25, angle=45, lw=0.3, color='#b94a48')
    cad_hatch_rect(ax, ax4_cx - grid_w / 2.0, ax4_cy - 1.7, grid_w - 1.2, 1.8, pitch=0.25, angle=-45, lw=0.3, color='#b94a48')
    cad_text(ax, ax4_cx - 1.0, ax4_cy - 0.8, 'KNITTED WIRE MESH PAD (SS316L / MONEL 400)\n20 MESH (0.8 MM WIRE) — 99.9% RETENTION', sz=5.2, bold=True, bg='white')
    
    # Top Hold-Down Flat Bar & Clamp Ring
    cad_rect(ax, ax4_cx - grid_w / 2.0, ax4_cy + 0.1, grid_w - 1.2, 0.5, lw=1.0, fill=True, fc='#bdc3c7')
    cad_text(ax, ax4_cx - 2.0, ax4_cy + 0.9, 'TOP HOLD-DOWN FLAT BARS (20 x 3 MM)', sz=4.8, bold=True)
    
    # J-Bolt Clamp & Retaining Latch
    cad_rect(ax, sw_x - 1.5, ax4_cy - 2.7, 0.35, 3.6, lw=0.8, fill=True, fc='#111111')
    cad_circle(ax, sw_x - 1.32, ax4_cy + 1.1, 0.22, lw=0.6, fill=True, fc='#ffffff')
    cad_text(ax, sw_x - 1.8, ax4_cy + 1.6, 'J-BOLT CLAMP', sz=4.2, bold=True, ha='right')
    
    # Catalyst Pellets resting on mesh screen
    for cx_s in np.linspace(ax4_cx - grid_w / 2.0 + 0.8, sw_x - 2.0, 11):
        cad_circle(ax, cx_s, ax4_cy + 1.1, 0.42, lw=0.5, fill=True, fc='#e67e22')
    for cx_s in np.linspace(ax4_cx - grid_w / 2.0 + 1.2, sw_x - 2.4, 10):
        cad_circle(ax, cx_s, ax4_cy + 1.9, 0.42, lw=0.5, fill=True, fc='#e67e22')
    cad_text(ax, ax4_cx - 1.0, ax4_cy + 2.8, '0.50" (12.7 MM) AG/AL2O3 CATALYST BED (phi = 0.50)', sz=5.0, bold=True, color='#c0392b')

    # ═════════════════════════════════════════════════════════════════════════
    # TITLE BLOCK (Bottom Full Width)
    # ═════════════════════════════════════════════════════════════════════════
    draw_title_block(
        ax,
        dwg_title='MECHANICAL FABRICATION & ASME SECTION VIII DETAILS',
        dwg_no='DWG-03',
        rev='00',
        sheet_no='03 OF 05',
        scale='CLOSE-UP DETAILS / PROPORTIONED',
        equip_desc='ETHYLENE OXIDATION MULTI-TUBULAR REACTOR (R-201) — ASME SEC VIII DIV 1 CODE DETAILS',
        duty_desc='UW-20 TUBE-TO-TUBESHEET WELD | 2:1 ELLIPSOIDAL HEAD UG-32 | SKIRT CHAIR | CATALYST GRID'
    )

    plt.savefig(out_png, dpi=300)
    plt.savefig(out_pdf)
    plt.close()
    print(f"[SUCCESS] DWG-03 generated: {out_png}")
    print(f"[SUCCESS] DWG-03 generated: {out_pdf}")

if __name__ == '__main__':
    out_dir = r"d:\GAMES\zercxes\CAD_Engineering_Drawings"
    generate_reactor_dwg03(
        os.path.join(out_dir, "03_Ethylene_Oxide_Reactor_Mechanical_Fabrication_Details_CAD.pdf"),
        os.path.join(out_dir, "03_Ethylene_Oxide_Reactor_Mechanical_Fabrication_Details_CAD.png")
    )
