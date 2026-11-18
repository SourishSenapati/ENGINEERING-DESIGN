"""
DWG-05: 3D ISOMETRIC PLANT INTEGRATION & CONNECTED PIPING LAYOUT
VAPOR-PHASE ETHYLENE OXIDATION MULTI-TUBULAR REACTOR SYSTEM (R-201)
ORTHOGONAL 3D AXONOMETRIC PERSPECTIVE — COMPLETE CLOSED-LOOP PIPING
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
from matplotlib.patches import Rectangle, Circle, Polygon, Arc

from cad_common import (
    create_cad_canvas, draw_sheet_border, draw_title_block,
    cad_line, cad_rect, cad_circle, cad_arc, cad_text, cad_arrow,
    cad_dim_h, cad_dim_v, cad_dim_leader, cad_balloon, cad_flange,
    cad_hatch_rect, cad_draw_table, W, H, BK, GREY
)

def generate_reactor_dwg05(out_pdf, out_png):
    fig, ax = create_cad_canvas()
    draw_sheet_border(ax)

    # ═════════════════════════════════════════════════════════════════════════
    # HEADER BANNER
    # ═════════════════════════════════════════════════════════════════════════
    cad_text(ax, W / 2.0, H - 2.0, '3D AXONOMETRIC ISOMETRIC PLANT INTEGRATION & CONNECTED PIPING LAYOUT', sz=10.5, bold=True)
    cad_text(ax, W / 2.0, H - 2.8, 'VAPOR-PHASE ETHYLENE OXIDATION PACKED BED TUBULAR REACTOR (R-201) — FULL CLOSED-LOOP PIPING TRAIN', sz=7.8, bold=True, color='#0a3d62')
    cad_line(ax, 8.0, H - 3.4, W - 8.0, H - 3.4, lw=1.2, color='#2980b9')

    # ═════════════════════════════════════════════════════════════════════════
    # ISOMETRIC PROJECTION ENGINE (30 DEGREE STANDARD ISO)
    # ═════════════════════════════════════════════════════════════════════════
    IX0, IY0 = 31.0, 10.0
    ANG = np.radians(30)
    cos30 = np.cos(ANG)
    sin30 = np.sin(ANG)
    SC = 1.65

    def to_iso(x, y, z):
        u = IX0 + (x - y) * cos30 * SC
        v = IY0 + (x + y) * sin30 * SC + z * SC * 1.05
        return u, v

    def draw_iso_pipe(pts, color='#111111', lw=1.3, arrow_idx=None, label=None, label_idx=None, label_offset=(0, 0.45)):
        iso_pts = [to_iso(px, py, pz) for px, py, pz in pts]
        for i in range(len(iso_pts) - 1):
            x1, y1 = iso_pts[i]
            x2, y2 = iso_pts[i+1]
            cad_line(ax, x1, y1, x2, y2, lw=lw, color=color, zorder=6)
        if arrow_idx is not None and arrow_idx < len(iso_pts) - 1:
            ax1, ay1 = iso_pts[arrow_idx]
            ax2, ay2 = iso_pts[arrow_idx + 1]
            mx, my = (ax1 + ax2)/2.0, (ay1 + ay2)/2.0
            dx, dy = ax2 - ax1, ay2 - ay1
            L = np.hypot(dx, dy)
            if L > 1e-4:
                ux, uy = dx/L, dy/L
                cad_arrow(ax, mx - ux*0.35, my - uy*0.35, mx + ux*0.35, my + uy*0.35, lw=lw, color=color, head_scale=6)
        if label and label_idx is not None and label_idx < len(iso_pts) - 1:
            lx1, ly1 = iso_pts[label_idx]
            lx2, ly2 = iso_pts[label_idx + 1]
            mlx, mly = (lx1 + lx2)/2.0 + label_offset[0], (ly1 + ly2)/2.0 + label_offset[1]
            cad_text(ax, mlx, mly, label, sz=4.2, bold=True, color=color, bg='white')

    # 1. Reinforced Concrete Foundation Pad in Isometric
    p_fnd = [to_iso(-11.0, -9.0, 0), to_iso(15.0, -9.0, 0), to_iso(15.0, 11.0, 0), to_iso(-11.0, 11.0, 0)]
    ax.add_patch(Polygon(p_fnd, closed=True, fc='#eaedf0', ec=BK, lw=1.1, zorder=2))
    p_fnd_edge1 = [to_iso(-11.0, -9.0, 0), to_iso(15.0, -9.0, 0), to_iso(15.0, -9.0, -0.6), to_iso(-11.0, -9.0, -0.6)]
    ax.add_patch(Polygon(p_fnd_edge1, closed=True, fc='#ced6e0', ec=BK, lw=0.9, zorder=2))
    p_fnd_edge2 = [to_iso(-11.0, -9.0, 0), to_iso(-11.0, 11.0, 0), to_iso(-11.0, 11.0, -0.6), to_iso(-11.0, -9.0, -0.6)]
    ax.add_patch(Polygon(p_fnd_edge2, closed=True, fc='#a4b0be', ec=BK, lw=0.9, zorder=2))

    # Grid Lines on Pad (1m spacing)
    for gx in np.arange(-10.0, 15.0, 2.5):
        p1 = to_iso(gx, -9.0, 0)
        p2 = to_iso(gx, 11.0, 0)
        cad_line(ax, p1[0], p1[1], p2[0], p2[1], lw=0.35, ls=':', color='#747d8c', zorder=2)
    for gy in np.arange(-8.0, 11.0, 2.5):
        p1 = to_iso(-11.0, gy, 0)
        p2 = to_iso(15.0, gy, 0)
        cad_line(ax, p1[0], p1[1], p2[0], p2[1], lw=0.35, ls=':', color='#747d8c', zorder=2)

    # ═════════════════════════════════════════════════════════════════════════
    # EQUIPMENT 1: MULTI-TUBULAR REACTOR R-201 (Center: x = 0, y = 0)
    # ═════════════════════════════════════════════════════════════════════════
    RX, RY = 0.0, 0.0
    R_RAD = 1.6
    Z_SKIRT = 2.2
    Z_TUBE_BOT = Z_SKIRT + 1.2
    Z_TUBE_TOP = Z_TUBE_BOT + 12.0
    Z_HEAD_TOP = Z_TUBE_TOP + 1.8

    # Skirt
    p_skirt_bot = [to_iso(RX + R_RAD*np.cos(t), RY + R_RAD*np.sin(t), 0.0) for t in np.linspace(0, 2*np.pi, 24)]
    ax.add_patch(Polygon(p_skirt_bot, closed=True, fc='#f1f2f6', ec=BK, lw=1.1, zorder=3))
    u_l_sk, v_l_sk0 = to_iso(RX - R_RAD, RY, 0.0)
    _, v_l_sk1 = to_iso(RX - R_RAD, RY, Z_SKIRT)
    u_r_sk, v_r_sk0 = to_iso(RX + R_RAD, RY, 0.0)
    _, v_r_sk1 = to_iso(RX + R_RAD, RY, Z_SKIRT)
    cad_line(ax, u_l_sk, v_l_sk0, u_l_sk, v_l_sk1, lw=1.2, zorder=4)
    cad_line(ax, u_r_sk, v_r_sk0, u_r_sk, v_r_sk1, lw=1.2, zorder=4)

    # Shell Body
    u_l, v_l_b = to_iso(RX - R_RAD, RY, Z_TUBE_BOT)
    _, v_l_t = to_iso(RX - R_RAD, RY, Z_TUBE_TOP)
    u_r, v_r_b = to_iso(RX + R_RAD, RY, Z_TUBE_BOT)
    _, v_r_t = to_iso(RX + R_RAD, RY, Z_TUBE_TOP)
    cad_rect(ax, u_l, v_l_b, u_r - u_l, v_l_t - v_l_b, lw=1.4, fill=True, fc='#f8f9fa', zorder=4)
    cad_line(ax, u_l, v_l_b, u_l, v_l_t, lw=1.4, zorder=5)
    cad_line(ax, u_r, v_r_b, u_r, v_r_t, lw=1.4, zorder=5)

    # Top Head & Bottom Head (2:1 Ellipsoidal)
    u_c_top, v_c_top = to_iso(RX, RY, Z_TUBE_TOP)
    ax.add_patch(Arc((u_c_top, v_c_top), 2*R_RAD*SC*cos30*2, R_RAD*SC*0.7, theta1=0, theta2=360, ec=BK, lw=1.3, zorder=5))
    ax.add_patch(Arc((u_c_top, v_c_top + 1.2), 2*R_RAD*SC*cos30*2, R_RAD*SC*0.7, theta1=0, theta2=180, ec=BK, lw=1.3, zorder=5))
    u_c_bot, v_c_bot = to_iso(RX, RY, Z_TUBE_BOT)
    ax.add_patch(Arc((u_c_bot, v_c_bot), 2*R_RAD*SC*cos30*2, R_RAD*SC*0.7, theta1=180, theta2=360, ec=BK, lw=1.3, zorder=5))

    # Internal Multi-Tubular Calandria Representation
    for ti in np.linspace(-R_RAD + 0.35, R_RAD - 0.35, 7):
        u_t1, v_t1 = to_iso(RX + ti, RY, Z_TUBE_BOT + 0.3)
        u_t2, v_t2 = to_iso(RX + ti, RY, Z_TUBE_TOP - 0.3)
        cad_line(ax, u_t1, v_t1, u_t2, v_t2, lw=0.75, ls='--', color='#2980b9', zorder=5)

    cad_text(ax, u_c_top, v_c_top + 2.4, 'R-201 ETHYLENE OXIDATION REACTOR\n1,000 TUBES x 1.5" SCH 80 (L = 30.81 FT)\nCATALYST WEIGHT: 26,469 LB (Ag / Al2O3)', sz=5.5, bold=True, bg='white')

    # Structural Platforms & Cage Ladders
    for pz in [Z_SKIRT + 1.0, Z_TUBE_BOT + 6.0, Z_TUBE_TOP + 0.5]:
        up_c, vp_c = to_iso(RX, RY, pz)
        cad_line(ax, up_c - 2.8, vp_c, up_c + 2.8, vp_c, lw=0.9, color='#34495e', zorder=5)
        cad_line(ax, up_c - 2.8, vp_c + 0.5, up_c + 2.8, vp_c + 0.5, lw=0.5, color='#34495e', zorder=5)

    # ═════════════════════════════════════════════════════════════════════════
    # EQUIPMENT 2: AIR COMPRESSOR C-201 & MOTOR (x = -8.5, y = -5.0, z = 0.5)
    # ═════════════════════════════════════════════════════════════════════════
    c_u, c_v = to_iso(-8.5, -5.0, 0.8)
    cad_rect(ax, c_u - 1.2, c_v - 0.7, 2.4, 1.4, lw=1.2, fill=True, fc='#ecf0f1', zorder=4)
    cad_circle(ax, c_u + 1.8, c_v, 0.55, lw=1.1, fill=True, fc='#dff9fb')
    cad_text(ax, c_u + 1.8, c_v, 'M', sz=5.5, bold=True)
    cad_line(ax, c_u + 1.2, c_v, c_u + 1.25, c_v, lw=1.2)
    cad_text(ax, c_u - 0.1, c_v, 'C-201\nAIR COMP.', sz=4.8, bold=True)

    # ═════════════════════════════════════════════════════════════════════════
    # EQUIPMENT 3: FEED PREHEATER E-201 (x = -5.5, y = 3.0, z = 2.0)
    # ═════════════════════════════════════════════════════════════════════════
    e_u, e_v = to_iso(-5.5, 3.0, 2.2)
    cad_rect(ax, e_u - 1.6, e_v - 0.7, 3.2, 1.4, lw=1.2, fill=True, fc='#fcf3cf', zorder=4)
    cad_line(ax, e_u - 1.3, e_v + 0.3, e_u + 1.3, e_v + 0.3, lw=0.6, ls='--')
    cad_line(ax, e_u - 1.3, e_v - 0.3, e_u + 1.3, e_v - 0.3, lw=0.6, ls='--')
    cad_text(ax, e_u, e_v + 1.1, 'E-201 PREHEATER\n(260 DEG C FEED)', sz=4.5, bold=True, bg='white')

    # ═════════════════════════════════════════════════════════════════════════
    # EQUIPMENT 4: STEAM DRUM V-201 (x = 5.5, y = 4.5, z = 12.0)
    # ═════════════════════════════════════════════════════════════════════════
    v_u, v_v = to_iso(5.5, 4.5, 12.0)
    cad_rect(ax, v_u - 1.8, v_v - 0.7, 3.6, 1.4, lw=1.2, fill=True, fc='#e8f8f5', zorder=5)
    ax.add_patch(Arc((v_u - 1.8, v_v), 0.8, 1.4, theta1=90, theta2=270, ec=BK, lw=1.2))
    ax.add_patch(Arc((v_u + 1.8, v_v), 0.8, 1.4, theta1=270, theta2=90, ec=BK, lw=1.2))
    cad_text(ax, v_u, v_v + 1.2, 'V-201 STEAM DRUM\n(400 PSIG SAT. STEAM)', sz=4.5, bold=True, bg='white')

    # ═════════════════════════════════════════════════════════════════════════
    # EQUIPMENT 5: COOLANT PUMPS P-201A/B (x = 5.5, y = 4.5, z = 0.6)
    # ═════════════════════════════════════════════════════════════════════════
    p_u1, p_v1 = to_iso(4.5, 4.5, 0.6)
    p_u2, p_v2 = to_iso(6.5, 4.5, 0.6)
    for pu, pv, tag in [(p_u1, p_v1, 'P-201A'), (p_u2, p_v2, 'P-201B')]:
        cad_circle(ax, pu, pv, 0.45, lw=1.0, fill=True, fc='#d4edda')
        cad_text(ax, pu, pv - 0.75, tag, sz=4.0, bold=True)

    # ═════════════════════════════════════════════════════════════════════════
    # EQUIPMENT 6: EFFLUENT COOLER E-202 (x = 8.0, y = -3.5, z = 3.5)
    # ═════════════════════════════════════════════════════════════════════════
    ec_u, ec_v = to_iso(8.0, -3.5, 3.5)
    cad_rect(ax, ec_u - 1.6, ec_v - 0.7, 3.2, 1.4, lw=1.2, fill=True, fc='#fcf3cf', zorder=4)
    cad_text(ax, ec_u, ec_v + 1.1, 'E-202 EFFLUENT COOLER\n(COOLING WATER)', sz=4.5, bold=True, bg='white')

    # ═════════════════════════════════════════════════════════════════════════
    # EQUIPMENT 7: ETHYLENE OXIDE ABSORBER C-201 (x = 12.0, y = 1.0, z = 0.0)
    # ═════════════════════════════════════════════════════════════════════════
    ab_u, ab_v_bot = to_iso(12.0, 1.0, 1.0)
    _, ab_v_top = to_iso(12.0, 1.0, 11.5)
    cad_rect(ax, ab_u - 1.0, ab_v_bot, 2.0, ab_v_top - ab_v_bot, lw=1.3, fill=True, fc='#f1f2f6', zorder=4)
    ax.add_patch(Arc((ab_u, ab_v_top), 2.0, 0.7, theta1=0, theta2=360, ec=BK, lw=1.2, zorder=5))
    ax.add_patch(Arc((ab_u, ab_v_bot), 2.0, 0.7, theta1=180, theta2=360, ec=BK, lw=1.2, zorder=5))
    cad_text(ax, ab_u, ab_v_top + 1.2, 'C-201 EO ABSORBER\n(WATER SCRUBBER)', sz=4.6, bold=True, bg='white')

    # ═════════════════════════════════════════════════════════════════════════
    # FULLY CONNECTED 3D ISOMETRIC PIPING NETWORK (ZERO DISCONNECTIONS!)
    # ═════════════════════════════════════════════════════════════════════════
    # PIPE 1: C2H4 FEED LINE (Line 101)
    pts_c2h4 = [
        (-10.5, -7.0, 4.0),
        (-6.0,  -7.0, 4.0),
        (-6.0,  -2.0, 4.0),
        (-6.0,   1.5, 4.0)
    ]
    draw_iso_pipe(pts_c2h4, color='#c0392b', lw=1.5, arrow_idx=0, label='10"-C2H4-101 (0.9 LBMOL/S @ 25 ATM)', label_idx=0, label_offset=(-0.8, 0.45))

    # PIPE 2: COMPRESSED AIR FEED (Line 102)
    pts_air = [
        (-8.5, -5.0, 1.2),
        (-8.5, -2.0, 1.2),
        (-6.0, -2.0, 1.2),
        (-6.0, -2.0, 3.8)
    ]
    draw_iso_pipe(pts_air, color='#2980b9', lw=1.4, arrow_idx=1, label='12"-AIR-102 (AIR FEED)', label_idx=1, label_offset=(-0.8, 0.35))

    # PIPE 3: MIXED GAS TO PREHEATER E-201 (Line 103)
    pts_mix = [
        (-6.0, 1.5, 4.0),
        (-6.0, 3.0, 4.0),
        (-5.5, 3.0, 2.8)
    ]
    draw_iso_pipe(pts_mix, color='#8e44ad', lw=1.4, arrow_idx=0)

    # PIPE 4: PREHEATED FEED TO REACTOR TOP NOZZLE N1 (Line 104)
    pts_feed = [
        (-5.5, 3.0, 1.8),
        (-5.5, 3.0, 15.5),
        (0.0,  3.0, 15.5),
        (0.0,  0.0, 15.5),
        (0.0,  0.0, Z_HEAD_TOP + 1.2)
    ]
    draw_iso_pipe(pts_feed, color='#d35400', lw=1.6, arrow_idx=2, label='14"-FEED-104 (25 ATM, 260 C)', label_idx=2, label_offset=(0.0, 0.45))

    # PIPE 5: REACTOR DISCHARGE BOTTOM NOZZLE N2 TO EFFLUENT COOLER E-202 (Line 105)
    pts_effluent = [
        (0.0,  0.0,  Z_SKIRT - 0.5),
        (0.0, -3.5,  Z_SKIRT - 0.5),
        (6.5, -3.5,  Z_SKIRT - 0.5),
        (6.5, -3.5,  3.5),
        (7.2, -3.5,  3.5)
    ]
    draw_iso_pipe(pts_effluent, color='#e67e22', lw=1.5, arrow_idx=1, label='14"-EFF-105 (21.0 ATM, 40% CONV)', label_idx=1, label_offset=(0.0, 0.45))

    # PIPE 6: COOLED EFFLUENT TO ABSORBER COLUMN C-201 (Line 106)
    pts_to_abs = [
        (8.8,  -3.5, 3.5),
        (12.0, -3.5, 3.5),
        (12.0,  1.0, 3.5)
    ]
    draw_iso_pipe(pts_to_abs, color='#16a085', lw=1.4, arrow_idx=1, label='12"-GAS-106 TO ABSORBER', label_idx=1, label_offset=(0.0, 0.40))

    # PIPE 7: BFW COOLANT TO REACTOR JACKET (Line 107)
    pts_bfw = [
        (5.5, 4.5, 1.0),
        (1.8, 4.5, 1.0),
        (1.8, 0.0, 1.0),
        (1.6, 0.0, Z_TUBE_BOT + 0.8)
    ]
    draw_iso_pipe(pts_bfw, color='#27ae60', lw=1.3, arrow_idx=1, label='10"-BFW-107 COOLANT INLET', label_idx=1, label_offset=(0.0, 0.35))

    # PIPE 8: THERMOSIPHON STEAM RETURN FROM REACTOR TO DRUM V-201 (Line 108)
    pts_steam = [
        (1.6, 0.0, Z_TUBE_TOP - 0.8),
        (1.8, 0.0, Z_TUBE_TOP - 0.8),
        (1.8, 4.5, Z_TUBE_TOP - 0.8),
        (4.5, 4.5, 12.0)
    ]
    draw_iso_pipe(pts_steam, color='#e74c3c', lw=1.4, arrow_idx=2, label='12"-STM-108 TO STEAM DRUM', label_idx=2, label_offset=(0.0, 0.40))

    # PIPE 9: DOWNCOMER WATER FROM DRUM V-201 TO PUMPS P-201A/B (Line 109)
    pts_downcomer = [
        (5.5, 4.5, 11.3),
        (5.5, 4.5, 1.0)
    ]
    draw_iso_pipe(pts_downcomer, color='#2980b9', lw=1.3, arrow_idx=0, label='8"-BFW-109 DOWNCOMER', label_idx=0, label_offset=(0.8, 0.0))

    # ═════════════════════════════════════════════════════════════════════════
    # RIGHT SIDE PANELS: MECHANICAL DATA TABLE & PIPING LINE SCHEDULE
    # ═════════════════════════════════════════════════════════════════════════
    TX_BASE = 57.0

    # Table 1: Equipment Specification Schedule
    t1_headers = ['TAG', 'EQUIPMENT NAME', 'SIZE / RATING', 'DESIGN DUTY / CAPACITY']
    t1_rows = [
        ['R-201', 'Ethylene Oxidation Tubular Reactor', '84" ID x 38.5 ft OAL, 1000 Tubes', '3240 lbmol/h C2H4, 25 atm, 260 C'],
        ['C-201', 'Centrifugal Air Compressor', 'Multi-stage with Intercooler', '1620 lbmol/h O2 in Air @ 26 bar'],
        ['E-201', 'Mixed Feed Gas Preheater', 'TEMA BEM (Shell & Tube)', 'Heat 88.15 lb/s gas 25 to 260 C'],
        ['V-201', 'Steam Separator Drum', '48" ID x 12.0 ft Horiz. Vessel', '400 psig Sat. Steam (Isothermal)'],
        ['P-201A/B', 'BFW Coolant Circ. Pumps', 'Centrifugal API-610 1+1', '450 gpm @ 50 psi dP'],
        ['E-202', 'Reactor Effluent Cooler', 'TEMA AEL (Shell & Tube)', 'Cool reaction gas 260 to 40 C'],
        ['C-201', 'Ethylene Oxide Absorber', '60" ID x 45 ft Packed Column', '99.5% EO Recovery in Water Wash']
    ]
    t1_widths = [2.2, 7.5, 7.5, 7.5] # 24.7 cm
    cad_draw_table(ax, TX_BASE, 35.0, t1_headers, t1_rows, t1_widths, row_h=0.55,
                   title='TABLE 1 — 3D PLANT EQUIPMENT SPECIFICATION SCHEDULE', title_sz=7.5, sz=4.8)

    # Table 2: Piping Line Schedule
    t2_headers = ['LINE NO.', 'SERVICE DESCRIPTION', 'SIZE / SCH', 'DESIGN P & T', 'MATERIAL']
    t2_rows = [
        ['10"-C2H4-101', 'Pure Ethylene Gas Feed', '10" Sch 80', '25 atm / Amb', 'CS A106-B'],
        ['12"-AIR-102', 'Compressed Air Feed', '12" Sch 80', '26 atm / 120 C', 'CS A106-B'],
        ['14"-FEED-104', 'Mixed Isothermal Reactor Feed', '14" Sch 80', '25 atm / 260 C', '304L SS'],
        ['14"-EFF-105', 'Reactor Reaction Effluent', '14" Sch 80', '21 atm / 260 C', '304L SS'],
        ['12"-GAS-106', 'Cooled Gas to EO Absorber', '12" Sch 80', '20.8 atm / 40 C', 'CS A106-B'],
        ['10"-BFW-107', 'Coolant Circulation Supply', '10" Sch 80', '32 bar / 240 C', 'CS A106-B'],
        ['12"-STM-108', 'Boiling Water/Steam Return', '12" Sch 80', '32 bar / 250 C', 'CS A106-B'],
        ['8"-BFW-109', 'Steam Drum Downcomer to Pump', '8" Sch 80', '32 bar / 250 C', 'CS A106-B']
    ]
    t2_widths = [3.2, 7.0, 3.2, 5.5, 5.8] # 24.7 cm
    cad_draw_table(ax, TX_BASE, 21.0, t2_headers, t2_rows, t2_widths, row_h=0.55,
                   title='TABLE 2 — CLOSED-LOOP 3D ISOMETRIC PIPING LINE SCHEDULE', title_sz=7.5, sz=4.8)

    # General Assembly & Erection Notes
    notes = [
        '1. ALL 3D PIPING IS ROUTED ALONG STRICT ORTHOGONAL AXES WITH ZERO DISCONNECTIONS.',
        '2. PIPING MATERIAL CLASS CS300 (ASME B31.3 PROCESS PIPING CODE). FLANGES ASME B16.5 CL300 RF.',
        '3. REACTOR TUBES (1,000 TUBES, 1.5" SCH 80) ROLLER EXPANDED & SEAL WELDED PER ASME SEC VIII UW-20.',
        '4. ISOTHERMAL BED TEMPERATURE MAINTAINED AT 260 DEG C VIA PRESSURIZED BOILING WATER AT 400 PSIG.',
        '5. ALL HIGH-PRESSURE REACTION PIPING 100% RADIOGRAPHED (RT) AND POST-WELD HEAT TREATED (PWHT).'
    ]
    for idx, nt in enumerate(notes):
        cad_text(ax, TX_BASE + 0.5, 17.5 - idx * 0.55, nt, sz=4.6, bold=False, ha='left')

    # ═════════════════════════════════════════════════════════════════════════
    # INSTITUTIONAL TITLE BLOCK
    # ═════════════════════════════════════════════════════════════════════════
    draw_title_block(
        ax,
        dwg_title='3D ISOMETRIC PLANT INTEGRATION & CONNECTED PIPING LAYOUT',
        dwg_no='DWG-05',
        rev='00',
        sheet_no='05 OF 05',
        scale='PICTORIAL AXONOMETRIC / AS NOTED',
        equip_desc='ETHYLENE OXIDATION MULTI-TUBULAR REACTOR SYSTEM (R-201) — 3D PLANT LAYOUT',
        duty_desc='CLOSED-LOOP PIPING TRAIN | C-201 -> E-201 -> R-201 -> E-202 -> C-201 | BFW COOLANT SYSTEM',
        date='17 / 11 / 2026'
    )

    plt.savefig(out_png, dpi=300)
    plt.savefig(out_pdf)
    plt.close()
    print(f"[SUCCESS] DWG-05 generated: {out_png}")
    print(f"[SUCCESS] DWG-05 generated: {out_pdf}")

if __name__ == '__main__':
    out_dir = r"d:\GAMES\zercxes\CAD_Engineering_Drawings"
    generate_reactor_dwg05(
        os.path.join(out_dir, "05_Ethylene_Oxide_Reactor_3D_Isometric_Plant_Assembly_CAD.pdf"),
        os.path.join(out_dir, "05_Ethylene_Oxide_Reactor_3D_Isometric_Plant_Assembly_CAD.png")
    )
