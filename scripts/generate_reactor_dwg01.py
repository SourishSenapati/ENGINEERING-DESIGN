"""
DWG-01: EQUIPMENT GENERAL ARRANGEMENT & SECTIONAL CAD
VAPOR-PHASE ETHYLENE OXIDATION MULTI-TUBULAR REACTOR (R-201)
1000 TUBES (1.5" SCH 80) x 30.81 FT PACKED BED WITH ERGUN PRESSURE DROP
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

def generate_reactor_dwg01(out_pdf, out_png):
    fig, ax = create_cad_canvas()
    draw_sheet_border(ax)

    # ═════════════════════════════════════════════════════════════════════════
    # VIEW 1: MAIN CUT-OPEN SECTIONAL ELEVATION (Left Half: X = 2.5 to 33.0)
    # ═════════════════════════════════════════════════════════════════════════
    CX = 16.5        # Centerline X
    Y_BASE = 7.5     # Ground / Foundation level
    
    # Vertical coordinates (scale: approx 1 cm = 350 mm)
    Y_SKIRT_BOT = Y_BASE + 0.6
    Y_SKIRT_TOP = Y_BASE + 4.8
    Y_BOT_TS = Y_SKIRT_TOP + 3.0    # Bottom tubesheet Y = 15.3
    TUBE_LEN = 26.5                 # Scaled packed tube length
    Y_TOP_TS = Y_BOT_TS + TUBE_LEN  # Top tubesheet Y = 41.8
    TS_THK = 1.0                    # Tubesheet thickness = 75 mm
    HEAD_H = 4.2                    # Ellipsoidal head depth
    
    R_SHELL_ID = 5.2                # 84" ID = 2,134 mm -> radius = 5.2 cm
    THK_SHELL = 0.25                # 1.0" wall thickness = 25.4 mm
    R_SHELL_OD = R_SHELL_ID + THK_SHELL
    
    # 1. Centerline
    cad_line(ax, CX, Y_BASE - 0.5, CX, Y_TOP_TS + TS_THK + HEAD_H + 4.5, lw=0.45, ls='dashdot', color='#c0392b')
    
    # View Titles
    cad_text(ax, CX, Y_TOP_TS + TS_THK + HEAD_H + 5.2, 'VIEW 1 — DETAILED SECTIONAL ELEVATION (CUT-OPEN VIEW)', sz=9.0, bold=True)
    cad_text(ax, CX, Y_TOP_TS + TS_THK + HEAD_H + 4.2, 'MULTI-TUBULAR PACKED-BED REACTOR (R-201) — 1,000 TUBES x 1.5" SCH 80', sz=7.0, bold=True)
    cad_text(ax, CX, Y_TOP_TS + TS_THK + HEAD_H + 3.4, 'ISOTHERMAL VAPOR-PHASE ETHYLENE OXIDATION WITH AIR @ 25 ATM, 260 DEG C', sz=5.8, bold=True, color='#2c3e50')
    
    # 2. Concrete Foundation & Grout
    cad_rect(ax, CX - 7.5, Y_BASE, 15.0, 0.6, lw=0.9, fill=True, fc='#f1f2f6')
    cad_hatch_rect(ax, CX - 7.5, Y_BASE, 15.0, 0.6, pitch=0.35, angle=45, lw=0.35, color='#7f8c8d')
    cad_line(ax, CX - 8.5, Y_BASE, CX + 8.5, Y_BASE, lw=1.2)
    cad_text(ax, CX - 6.0, Y_BASE + 0.3, 'REINFORCED CONCRETE PAD (GRADE M30)', sz=5.0, bold=True)
    
    # 3. Skirt Support & Base Ring
    # Base ring
    cad_rect(ax, CX - R_SHELL_OD - 0.8, Y_SKIRT_BOT, 2 * (R_SHELL_OD + 0.8), 0.35, lw=1.0, fill=True, fc='#bdc3c7')
    # Cylindrical Skirt
    cad_rect(ax, CX - R_SHELL_OD, Y_SKIRT_BOT + 0.35, 2 * R_SHELL_OD, Y_SKIRT_TOP - (Y_SKIRT_BOT + 0.35), lw=1.0, fill=False)
    # Skirt Access Manway
    cad_circle(ax, CX, (Y_SKIRT_BOT + Y_SKIRT_TOP) / 2.0, 0.9, lw=0.8, fill=True, fc='#ffffff')
    cad_circle(ax, CX, (Y_SKIRT_BOT + Y_SKIRT_TOP) / 2.0, 0.7, lw=0.5, fill=False)
    cad_text(ax, CX, (Y_SKIRT_BOT + Y_SKIRT_TOP) / 2.0, 'SKIRT MANWAY\nDN500 (20")', sz=4.2, bold=True)
    
    # 4. Bottom Dished Head (2:1 Ellipsoidal)
    b_head_path = [
        (MPath.MOVETO, (CX - R_SHELL_ID, Y_BOT_TS)),
        (MPath.CURVE4, (CX - R_SHELL_ID, Y_SKIRT_TOP)),
        (MPath.CURVE4, (CX + R_SHELL_ID, Y_SKIRT_TOP)),
        (MPath.CURVE4, (CX + R_SHELL_ID, Y_BOT_TS))
    ]
    codes, verts = zip(*b_head_path)
    ax.add_patch(PathPatch(MPath(verts, codes), fill=True, facecolor='#ffffff', edgecolor=BK, lw=1.2, zorder=2))
    
    # Bottom Product Nozzle N2 (14" CL300)
    noz_w = 1.4
    noz_h = 2.2
    cad_rect(ax, CX - noz_w / 2.0, Y_SKIRT_TOP - noz_h, noz_w, noz_h, lw=1.0, fill=True, fc='#ffffff', zorder=3)
    cad_flange(ax, CX, Y_SKIRT_TOP - noz_h, orientation='V', length=noz_w * 1.5, thickness=0.25, lw=1.1)
    
    # 5. Top Dished Head (2:1 Ellipsoidal)
    t_head_path = [
        (MPath.MOVETO, (CX - R_SHELL_ID, Y_TOP_TS + TS_THK)),
        (MPath.CURVE4, (CX - R_SHELL_ID, Y_TOP_TS + TS_THK + HEAD_H)),
        (MPath.CURVE4, (CX + R_SHELL_ID, Y_TOP_TS + TS_THK + HEAD_H)),
        (MPath.CURVE4, (CX + R_SHELL_ID, Y_TOP_TS + TS_THK))
    ]
    codes, verts = zip(*t_head_path)
    ax.add_patch(PathPatch(MPath(verts, codes), fill=True, facecolor='#ffffff', edgecolor=BK, lw=1.2, zorder=2))
    
    # Top Feed Inlet Nozzle N1 (14" CL300)
    cad_rect(ax, CX - noz_w / 2.0, Y_TOP_TS + TS_THK + HEAD_H * 0.75, noz_w, noz_h, lw=1.0, fill=True, fc='#ffffff', zorder=3)
    cad_flange(ax, CX, Y_TOP_TS + TS_THK + HEAD_H * 0.75 + noz_h, orientation='V', length=noz_w * 1.5, thickness=0.25, lw=1.1)
    
    # Top Gas Distribution Perforated Baffle Plate
    cad_line(ax, CX - R_SHELL_ID + 0.6, Y_TOP_TS + TS_THK + 1.2, CX + R_SHELL_ID - 0.6, Y_TOP_TS + TS_THK + 1.2, lw=1.0, ls=':')
    cad_text(ax, CX, Y_TOP_TS + TS_THK + 1.6, 'PERFORATED GAS DISTRIBUTOR BAFFLE', sz=4.8, bold=True)
    
    # 6. Tubesheets (Top & Bottom)
    cad_rect(ax, CX - R_SHELL_OD - 0.5, Y_BOT_TS - TS_THK, 2 * (R_SHELL_OD + 0.5), TS_THK, lw=1.2, fill=True, fc='#bdc3c7', zorder=4)
    cad_rect(ax, CX - R_SHELL_OD - 0.5, Y_TOP_TS, 2 * (R_SHELL_OD + 0.5), TS_THK, lw=1.2, fill=True, fc='#bdc3c7', zorder=4)
    
    # Tubesheet Bolting Flanges
    cad_rect(ax, CX - R_SHELL_OD - 0.8, Y_BOT_TS - TS_THK - 0.4, 0.6, TS_THK + 0.8, lw=0.8, fill=True, fc='#7f8c8d')
    cad_rect(ax, CX + R_SHELL_OD + 0.2, Y_BOT_TS - TS_THK - 0.4, 0.6, TS_THK + 0.8, lw=0.8, fill=True, fc='#7f8c8d')
    cad_rect(ax, CX - R_SHELL_OD - 0.8, Y_TOP_TS - 0.4, 0.6, TS_THK + 0.8, lw=0.8, fill=True, fc='#7f8c8d')
    cad_rect(ax, CX + R_SHELL_OD + 0.2, Y_TOP_TS - 0.4, 0.6, TS_THK + 0.8, lw=0.8, fill=True, fc='#7f8c8d')
    
    # 7. Cylindrical Shell Body
    cad_line(ax, CX - R_SHELL_ID, Y_BOT_TS, CX - R_SHELL_ID, Y_TOP_TS, lw=1.3)
    cad_line(ax, CX + R_SHELL_ID, Y_BOT_TS, CX + R_SHELL_ID, Y_TOP_TS, lw=1.3)
    cad_line(ax, CX - R_SHELL_OD, Y_BOT_TS, CX - R_SHELL_OD, Y_TOP_TS, lw=0.7)
    cad_line(ax, CX + R_SHELL_OD, Y_BOT_TS, CX + R_SHELL_OD, Y_TOP_TS, lw=0.7)
    
    # Shell Wall Hatching (Cross section wall)
    cad_rect(ax, CX - R_SHELL_OD, Y_BOT_TS, THK_SHELL, TUBE_LEN, lw=0.6, fill=True, fc='#dcdde1')
    cad_rect(ax, CX + R_SHELL_ID, Y_BOT_TS, THK_SHELL, TUBE_LEN, lw=0.6, fill=True, fc='#dcdde1')
    
    # 8. Transverse Coolant Baffles (Segmental 25% cut)
    baffle_ys = [Y_BOT_TS + 5.0, Y_BOT_TS + 10.5, Y_BOT_TS + 16.0, Y_BOT_TS + 21.5]
    for idx_b, by in enumerate(baffle_ys):
        if idx_b % 2 == 0:
            cad_line(ax, CX - R_SHELL_ID, by, CX + R_SHELL_ID - 2.5, by, lw=1.4, color='#2980b9')
        else:
            cad_line(ax, CX - R_SHELL_ID + 2.5, by, CX + R_SHELL_ID, by, lw=1.4, color='#2980b9')
            
    # 9. Multi-Tube Array (Showing 15 Representative Tubes with Catalyst Packing)
    n_display_tubes = 15
    tube_spacing = (2 * R_SHELL_ID - 1.2) / (n_display_tubes - 1)
    t_width = 0.32
    
    for i in range(n_display_tubes):
        tx = (CX - R_SHELL_ID + 0.6) + i * tube_spacing
        # Draw tube walls
        cad_line(ax, tx - t_width / 2.0, Y_BOT_TS, tx - t_width / 2.0, Y_TOP_TS, lw=0.6, color='#555555')
        cad_line(ax, tx + t_width / 2.0, Y_BOT_TS, tx + t_width / 2.0, Y_TOP_TS, lw=0.6, color='#555555')
        # Catalyst Bed inside Tube
        cad_rect(ax, tx - t_width / 2.0, Y_BOT_TS + 0.3, t_width, TUBE_LEN - 0.6, lw=0.0, fill=True, fc='#f5cd79', zorder=2)
        # Catalyst Pellets (Circles)
        for py in np.linspace(Y_BOT_TS + 1.2, Y_TOP_TS - 1.2, 12):
            cad_circle(ax, tx, py, 0.10, lw=0.35, fill=True, fc='#e67e22', zorder=3)
            
    # Catalyst Retaining Grid (Top) and Wire Mesh Support (Bottom)
    cad_line(ax, CX - R_SHELL_ID + 0.3, Y_TOP_TS - 0.3, CX + R_SHELL_ID - 0.3, Y_TOP_TS - 0.3, lw=1.2, ls=':', color='#2c3e50')
    cad_line(ax, CX - R_SHELL_ID + 0.3, Y_BOT_TS + 0.3, CX + R_SHELL_ID - 0.3, Y_BOT_TS + 0.3, lw=1.2, ls=':', color='#2c3e50')
    
    # 10. Coolant Nozzles on Shell (N3: Inlet @ bottom, N4: Outlet @ top)
    c_noz_w = 1.0
    c_noz_h = 1.2
    # N3: Coolant Inlet (10" CL300)
    cad_rect(ax, CX + R_SHELL_OD, Y_BOT_TS + 2.0, c_noz_h, c_noz_w, lw=0.9, fill=True, fc='#ffffff')
    cad_flange(ax, CX + R_SHELL_OD + c_noz_h, Y_BOT_TS + 2.0 + c_noz_w / 2.0, orientation='H', length=c_noz_w * 1.5, thickness=0.22, lw=1.0)
    
    # N4: Coolant Vapor Outlet (12" CL300)
    cad_rect(ax, CX + R_SHELL_OD, Y_TOP_TS - 3.2, c_noz_h, c_noz_w * 1.2, lw=0.9, fill=True, fc='#ffffff')
    cad_flange(ax, CX + R_SHELL_OD + c_noz_h, Y_TOP_TS - 3.2 + (c_noz_w * 1.2) / 2.0, orientation='H', length=c_noz_w * 1.8, thickness=0.22, lw=1.0)
    
    # 11. Dimensions (All ASME/ANSI formatted with 45-degree ticks)
    # Total O.A. Height
    cad_dim_v(ax, CX - R_SHELL_OD - 3.8, Y_BASE, Y_TOP_TS + TS_THK + HEAD_H * 0.75 + noz_h + 0.25,
              'TOTAL O.A. HEIGHT = 46.50 FT (14,170 MM)', ext=0.45, sz=5.5)
    
    # Packed Tube Length L
    cad_dim_v(ax, CX - R_SHELL_OD - 1.8, Y_BOT_TS, Y_TOP_TS,
              'PACKED TUBE LENGTH L = 30.81 FT (9,390 MM)', ext=0.45, sz=5.5)
    
    # Skirt Height
    cad_dim_v(ax, CX - R_SHELL_OD - 1.8, Y_BASE, Y_SKIRT_TOP,
              'SKIRT H = 8.20 FT (2,500 MM)', ext=0.40, sz=4.8)
    
    # Shell Inside Diameter
    cad_dim_h(ax, CX - R_SHELL_ID, CX + R_SHELL_ID, Y_TOP_TS + TS_THK + 0.6,
              'SHELL ID = 84.00 IN (2,134 MM)', ext=0.40, sz=5.5)
    
    # 12. Component Identification Balloons matching BOM Table
    cad_balloon(ax, CX - 3.0, Y_TOP_TS + TS_THK + HEAD_H + 1.2, '1')    # Feed Nozzle N1
    cad_balloon(ax, CX + 3.0, Y_TOP_TS + TS_THK + 1.6, '2')             # Top Head
    cad_balloon(ax, CX - R_SHELL_OD - 1.2, Y_TOP_TS + 0.5, '3')         # Top Tubesheet
    cad_balloon(ax, CX + R_SHELL_ID + 2.4, Y_TOP_TS - 2.5, '4')         # Coolant Outlet N4
    cad_balloon(ax, CX - 2.0, Y_BOT_TS + 18.0, '5')                     # Catalyst Bed
    cad_balloon(ax, CX + R_SHELL_OD + 0.8, Y_BOT_TS + 13.0, '6')        # Reactor Shell Body
    cad_balloon(ax, CX + 2.0, Y_BOT_TS + 10.5, '7')                     # Coolant Baffle
    cad_balloon(ax, CX + R_SHELL_ID + 2.4, Y_BOT_TS + 2.6, '8')         # Coolant Inlet N3
    cad_balloon(ax, CX - R_SHELL_OD - 1.2, Y_BOT_TS - 0.5, '9')         # Bottom Tubesheet
    cad_balloon(ax, CX - 2.5, Y_BOT_TS - 1.8, '10')                     # Bottom Head
    cad_balloon(ax, CX - 3.0, Y_SKIRT_TOP - 1.2, '11')                  # Product Nozzle N2
    cad_balloon(ax, CX - R_SHELL_OD - 0.8, Y_SKIRT_BOT + 2.2, '12')     # Support Skirt
    cad_balloon(ax, CX - R_SHELL_OD - 1.2, Y_SKIRT_BOT + 0.2, '13')     # Anchor Base Plate
    
    # Leaders pointing from balloons to components
    cad_line(ax, CX - 2.6, Y_TOP_TS + TS_THK + HEAD_H + 1.2, CX - 0.8, Y_TOP_TS + TS_THK + HEAD_H * 0.75 + 1.0, lw=0.45)
    cad_line(ax, CX + 2.6, Y_TOP_TS + TS_THK + 1.6, CX + 1.5, Y_TOP_TS + TS_THK + 2.5, lw=0.45)
    cad_line(ax, CX - R_SHELL_OD - 0.8, Y_TOP_TS + 0.5, CX - R_SHELL_OD, Y_TOP_TS + 0.5, lw=0.45)
    cad_line(ax, CX + R_SHELL_ID + 2.0, Y_TOP_TS - 2.5, CX + R_SHELL_OD + c_noz_h, Y_TOP_TS - 2.5, lw=0.45)
    cad_line(ax, CX - 1.6, Y_BOT_TS + 18.0, CX - 0.5, Y_BOT_TS + 18.0, lw=0.45)
    cad_line(ax, CX + R_SHELL_OD + 0.4, Y_BOT_TS + 13.0, CX + R_SHELL_OD, Y_BOT_TS + 13.0, lw=0.45)
    cad_line(ax, CX + 1.6, Y_BOT_TS + 10.5, CX + 0.5, Y_BOT_TS + 10.5, lw=0.45)
    cad_line(ax, CX + R_SHELL_ID + 2.0, Y_BOT_TS + 2.6, CX + R_SHELL_OD + c_noz_h, Y_BOT_TS + 2.6, lw=0.45)
    cad_line(ax, CX - R_SHELL_OD - 0.8, Y_BOT_TS - 0.5, CX - R_SHELL_OD, Y_BOT_TS - 0.5, lw=0.45)
    cad_line(ax, CX - 2.1, Y_BOT_TS - 1.8, CX - 1.0, Y_BOT_TS - 1.8, lw=0.45)
    cad_line(ax, CX - 2.6, Y_SKIRT_TOP - 1.2, CX - 0.8, Y_SKIRT_TOP - 1.2, lw=0.45)
    cad_line(ax, CX - R_SHELL_OD - 0.4, Y_SKIRT_BOT + 2.2, CX - R_SHELL_OD, Y_SKIRT_BOT + 2.2, lw=0.45)
    cad_line(ax, CX - R_SHELL_OD - 0.8, Y_SKIRT_BOT + 0.2, CX - R_SHELL_OD - 0.4, Y_SKIRT_BOT + 0.2, lw=0.45)

    # ═════════════════════════════════════════════════════════════════════════
    # VIEW 2: SECTION A-A — CALANDRIA TUBESHEET & TUBE LAYOUT (X = 35.0 to 53.0, Y = 32.0 to 53.0)
    # ═════════════════════════════════════════════════════════════════════════
    TS_CX = 43.5
    TS_CY = 43.0
    TS_R = 6.8
    
    cad_text(ax, TS_CX, TS_CY + TS_R + 2.2, 'VIEW 2 — SECTION A-A (TUBESHEET LAYOUT)', sz=8.0, bold=True)
    cad_text(ax, TS_CX, TS_CY + TS_R + 1.3, '1,000 TUBES ON 2.375" (60.3 MM) TRIANGULAR PITCH (30 DEG)', sz=6.0, bold=True, color='#2c3e50')
    
    # Outer Flange Circle
    cad_circle(ax, TS_CX, TS_CY, TS_R + 0.8, lw=1.2, fill=True, fc='#bdc3c7')
    # Bolt Circle
    cad_circle(ax, TS_CX, TS_CY, TS_R + 0.4, lw=0.45, ls='dashdot', ec='#c0392b')
    # Shell Inside Boundary
    cad_circle(ax, TS_CX, TS_CY, TS_R, lw=1.2, fill=True, fc='#ffffff')
    
    # Centerlines
    cad_line(ax, TS_CX - TS_R - 1.2, TS_CY, TS_CX + TS_R + 1.2, TS_CY, lw=0.4, ls='dashdot', color='#c0392b')
    cad_line(ax, TS_CX, TS_CY - TS_R - 1.2, TS_CX, TS_CY + TS_R + 1.2, lw=0.4, ls='dashdot', color='#c0392b')
    
    # Generate 1,000 Tubes on 30 deg Triangular Pitch Pattern
    np.random.seed(101)
    pitch_scaled = 0.42
    h_step = pitch_scaled * np.sqrt(3.0) / 2.0
    
    y_offsets = np.arange(-TS_R + 0.5, TS_R - 0.4, h_step)
    tube_count_actual = 0
    for row_idx, yo in enumerate(y_offsets):
        x_shift = 0.0 if row_idx % 2 == 0 else pitch_scaled / 2.0
        x_offsets = np.arange(-TS_R + 0.5 + x_shift, TS_R - 0.4, pitch_scaled)
        for xo in x_offsets:
            dist = np.sqrt(xo**2 + yo**2)
            if dist < TS_R - 0.35:
                # Tube Outer & Inner Diameter
                cad_circle(ax, TS_CX + xo, TS_CY + yo, 0.15, lw=0.45, fill=True, fc='#dcdde1', zorder=4)
                cad_circle(ax, TS_CX + xo, TS_CY + yo, 0.11, lw=0.35, fill=True, fc='#ffffff', zorder=5)
                tube_count_actual += 1
                
    # Flange Bolt Holes (36 bolts)
    for b_ang in np.linspace(0, 2 * np.pi, 36, endpoint=False):
        bx = TS_CX + (TS_R + 0.4) * np.cos(b_ang)
        by = TS_CY + (TS_R + 0.4) * np.sin(b_ang)
        cad_circle(ax, bx, by, 0.09, lw=0.4, fill=True, fc='#111111', zorder=6)
        
    cad_dim_h(ax, TS_CX - TS_R, TS_CX + TS_R, TS_CY - TS_R - 1.0, 'SHELL ID = 84.00" (2,134 MM)', ext=0.35, sz=5.5)

    # ═════════════════════════════════════════════════════════════════════════
    # VIEW 3: DETAIL B — SINGLE TUBE & CATALYST BED PACKING (X = 35.0 to 53.0, Y = 10.0 to 30.0)
    # ═════════════════════════════════════════════════════════════════════════
    DT_CX = 43.5
    DT_CY = 20.0
    DT_W = 4.8
    DT_H = 15.0
    
    cad_text(ax, DT_CX, DT_CY + DT_H / 2.0 + 1.8, 'VIEW 3 — DETAIL B (TUBE & CATALYST PACKING)', sz=8.0, bold=True)
    cad_text(ax, DT_CX, DT_CY + DT_H / 2.0 + 1.0, '1.5" SCH 80 TUBE (ID=1.500", OD=1.900", TW=0.200") WITH 0.5" SPHERES', sz=6.0, bold=True, color='#2c3e50')
    
    # Tube Outer Wall Hatching
    cad_rect(ax, DT_CX - DT_W / 2.0, DT_CY - DT_H / 2.0, DT_W, DT_H, lw=1.2, fill=True, fc='#bdc3c7')
    # Tube Inner Bore (Packed Space)
    t_id_scaled = DT_W * (1.500 / 1.900)  # ID/OD proportion
    cad_rect(ax, DT_CX - t_id_scaled / 2.0, DT_CY - DT_H / 2.0, t_id_scaled, DT_H, lw=0.8, fill=True, fc='#fff2cc')
    
    # Catalyst Pellets Array inside Tube
    pellet_r = 0.42
    p_ys = np.arange(DT_CY - DT_H / 2.0 + 0.8, DT_CY + DT_H / 2.0 - 0.6, 0.95)
    for p_row, py in enumerate(p_ys):
        if p_row % 2 == 0:
            for px_off in [-1.0, 0.0, 1.0]:
                cad_circle(ax, DT_CX + px_off, py, pellet_r, lw=0.6, fill=True, fc='#e67e22')
        else:
            for px_off in [-0.55, 0.55]:
                cad_circle(ax, DT_CX + px_off, py, pellet_r, lw=0.6, fill=True, fc='#e67e22')
                
    # Lower Wire Mesh Support & Upper Hold-Down Screen
    cad_line(ax, DT_CX - t_id_scaled / 2.0, DT_CY - DT_H / 2.0 + 0.35, DT_CX + t_id_scaled / 2.0, DT_CY - DT_H / 2.0 + 0.35, lw=2.0, ls=':', color='#111111')
    cad_line(ax, DT_CX - t_id_scaled / 2.0, DT_CY + DT_H / 2.0 - 0.35, DT_CX + t_id_scaled / 2.0, DT_CY + DT_H / 2.0 - 0.35, lw=2.0, ls=':', color='#111111')
    
    # Dimensions on Detail B
    cad_dim_h(ax, DT_CX - DT_W / 2.0, DT_CX + DT_W / 2.0, DT_CY + DT_H / 2.0 + 0.5, 'OD = 1.900" (48.26 MM)', ext=0.3, sz=5.0)
    cad_dim_h(ax, DT_CX - t_id_scaled / 2.0, DT_CX + t_id_scaled / 2.0, DT_CY - DT_H / 2.0 - 0.5, 'ID = 1.500" (38.10 MM)', ext=0.3, sz=5.0)
    
    # Detail Callouts
    cad_dim_leader(ax, DT_CX - DT_W / 2.0 + 0.2, DT_CY + 4.0, DT_CX - 3.8, DT_CY + 4.0, DT_CX - 5.0,
                   'SCHEDULE 80 WALL = 0.200" (5.08 MM)', sz=5.0)
    cad_dim_leader(ax, DT_CX, DT_CY - 1.0, DT_CX - 3.8, DT_CY - 1.0, DT_CX - 5.0,
                   '0.50" (12.7 MM) AG/AL2O3 SPHERES (phi = 0.50)', sz=5.0)
    cad_dim_leader(ax, DT_CX + t_id_scaled / 2.0 - 0.2, DT_CY - DT_H / 2.0 + 0.35, DT_CX + 3.8, DT_CY - DT_H / 2.0 + 0.35, DT_CX + 5.0,
                   'SS316 WIRE MESH SUPPORT SCREEN', sz=5.0)

    # ═════════════════════════════════════════════════════════════════════════
    # RIGHT PANEL: TABLES (X = 54.0 to 82.5, Y = 7.0 to 52.0)
    # ═════════════════════════════════════════════════════════════════════════
    # Table 1: Equipment Nozzle Schedule
    n_headers = ['MARK', 'SERVICE / NOZZLE DESCRIPTION', 'NOM. SIZE', 'RATING', 'FACING']
    n_rows = [
        ['N1', 'PROCESS FEED GAS INLET (C2H4 + AIR)', 'DN350 (14")', 'CLASS 300', 'ASME B16.5 RF'],
        ['N2', 'REACTOR PRODUCT EFFLUENT (C2H4O)', 'DN350 (14")', 'CLASS 300', 'ASME B16.5 RF'],
        ['N3', 'COOLANT LIQUID INLET (BFW / DOWTHERM)', 'DN250 (10")', 'CLASS 300', 'ASME B16.5 RF'],
        ['N4', 'COOLANT VAPOR OUTLET (TO STEAM DRUM)', 'DN300 (12")', 'CLASS 300', 'ASME B16.5 RF'],
        ['M1', 'VESSEL INSPECTION MANWAY (TOP DOME)', 'DN500 (20")', 'CLASS 300', 'DAVIT TYPE RF'],
        ['M2', 'VESSEL DISCHARGE MANWAY (BOTTOM)', 'DN500 (20")', 'CLASS 300', 'DAVIT TYPE RF'],
        ['PT1', 'INLET/OUTLET PRESSURE TRANSMITTERS', 'DN50 (2")', 'CLASS 300', 'FLANGED RF'],
        ['TT1', 'MULTIPLEX BED THERMOCOUPLE WELLS', 'DN40 (1.5")', 'CLASS 300', 'FLANGED RF'],
        ['PSV', 'SAFETY RELIEF VALVE (SHELL & TUBE)', 'DN80 (3")', 'CLASS 300', 'FLANGED RF']
    ]
    n_widths = [1.5, 13.5, 3.5, 3.5, 6.0]
    cad_draw_table(ax, 54.0, 40.5, n_headers, n_rows, n_widths, row_h=0.55,
                   title='TABLE 1 — REACTOR NOZZLE SCHEDULE (ASME B16.5 CLASS 300)', title_sz=7.5, sz=5.2)

    # Table 2: Bill of Materials (BOM) & Mechanical MOC
    b_headers = ['ITEM', 'DESCRIPTION / COMPONENT NAME', 'QTY', 'MATERIAL SPECIFICATION (ASME / ASTM)']
    b_rows = [
        ['1', 'PROCESS GAS INLET NOZZLE (N1) FLANGE', '1', 'ASTM A105 FORGED CARBON STEEL, CL300 RF'],
        ['2', 'TOP 2:1 ELLIPSOIDAL DISHED HEAD', '1', 'SA-516 GR 70 KILLED CS (1.00" THK) + CLAD'],
        ['3', 'TOP CALANDRIA TUBESHEET (75 MM THK)', '1', 'SA-266 CL 2 FORGING + EXPLOSION CLAD'],
        ['4', 'COOLANT VAPOR OUTLET NOZZLE (N4)', '1', 'ASTM A106 GR B SEAMLESS PIPE, CL300 RF'],
        ['5', 'CATALYST BED (1,000 TUBES x 30.81 FT)', '26,469 LB', 'SILVER ON LOW S.A. ALUMINA (0.50" SPHERES)'],
        ['6', 'CYLINDRICAL REACTOR SHELL (84.0" ID)', '1', 'SA-516 GR 70 PRESSURE VESSEL STEEL (1.00" THK)'],
        ['7', 'SEGMENTAL COOLANT BAFFLES (25% CUT)', '4', 'ASTM A285 GR C CARBON STEEL (0.375" THK)'],
        ['8', 'COOLANT LIQUID INLET NOZZLE (N3)', '1', 'ASTM A106 GR B SEAMLESS PIPE, CL300 RF'],
        ['9', 'BOTTOM CALANDRIA TUBESHEET (75 MM)', '1', 'SA-266 CL 2 FORGING + EXPLOSION CLAD'],
        ['10', 'BOTTOM 2:1 ELLIPSOIDAL DISHED HEAD', '1', 'SA-516 GR 70 PRESSURE VESSEL STEEL (1.00" THK)'],
        ['11', 'REACTOR PRODUCT OUTLET NOZZLE (N2)', '1', 'ASTM A105 FORGED CARBON STEEL, CL300 RF'],
        ['12', 'CYLINDRICAL VESSEL SUPPORT SKIRT', '1', 'ASTM A36 STRUCTURAL CARBON STEEL (16 MM THK)'],
        ['13', 'HEAVY-DUTY ANCHOR BASE RING & CHAIRS', '16 SETS', 'M36 ANCHOR BOLTS (ASTM A193 B7) WITH DOUBLE NUTS'],
        ['14', 'CATALYST TUBES (1.5" SCH 80 SEAMLESS)', '1,000 PCS', 'SA-214 CONDENSER TUBES / SA-249 TP304']
    ]
    b_widths = [1.5, 12.0, 3.2, 11.3]
    cad_draw_table(ax, 54.0, 24.5, b_headers, b_rows, b_widths, row_h=0.55,
                   title='TABLE 2 — BILL OF MATERIALS (BOM) & MECHANICAL SPECIFICATIONS', title_sz=7.5, sz=5.0)

    # Table 3: Process Operating Parameters & Reaction Kinetics
    p_headers = ['PARAMETER / KINETIC SPECIFICATION', 'DESIGN VALUE (US)', 'DESIGN VALUE (SI)', 'GOVERNING CODE / EQUATION']
    p_rows = [
        ['ETHYLENE FEED RATE (FA0)', '0.900 LB-MOL/S (3,240 LB-MOL/H)', '408.2 MOL/S (1,469.6 KMOL/H)', 'MASS BALANCE BASIS'],
        ['AIR FEED RATE (STOICHIOMETRIC O2)', '3.043 LB-MOL/S (AIR FEED)', '1,380.2 MOL/S', 'THETA_B=0.50, THETA_I=1.881'],
        ['INLET OPERATING PRESSURE (P0)', '25.00 ATM (367.4 PSIA)', '2.533 MPA (25.33 BAR)', 'PLANT BATTERY LIMITS'],
        ['OPERATING TEMPERATURE (ISOTHERMAL)', '260.0 DEG C (500.0 DEG F)', '533.15 K', 'DOWTHERM/BFW JACKET CONTROL'],
        ['SPECIFIC REACTION RATE CONSTANT (k)', '0.0141 LBMOL/(ATM.LB CAT.H)', '8.539E-5 MOL/(BAR.KG.S)', '-rA = k.PA^(1/3).PB^(2/3)'],
        ['TARGET ETHYLENE CONVERSION (X)', '40.0 % CONVERSION', 'X = 0.4000', 'SINGLE PASS REACTION SPEC'],
        ['IDEAL CATALYST WEIGHT (dP = 0)', '24,390.55 LB CAT', '11,063.38 KG CAT', 'ANALYTICAL BASELINE INTEGRAL'],
        ['ACTUAL CATALYST WEIGHT (ERGUN dP)', '26,469.02 LB CAT (+8.52%)', '12,006.16 KG CAT', 'COUPLED RK-45 NUMERICAL ODE'],
        ['TOTAL REACTOR PRESSURE DROP (deltaP)', '4.002 ATM (58.81 PSI, 16.0%)', '0.4055 MPA', 'ERGUN PACKED BED EQUATION'],
        ['EXIT VOLUMETRIC FLOW RATIO (v/v0)', '1.1202 (+12.02% EXPANSION)', '1.1202', 'v/v0 = (1 + eps_A.X) / y']
    ]
    p_widths = [9.5, 7.5, 5.5, 5.5]
    cad_draw_table(ax, 54.0, 9.5, p_headers, p_rows, p_widths, row_h=0.55,
                   title='TABLE 3 — PROCESS DESIGN PARAMETERS & RIGOROUS KINETIC SOLUTION', title_sz=7.5, sz=5.0)

    # ═════════════════════════════════════════════════════════════════════════
    # TITLE BLOCK (Bottom Full Width)
    # ═════════════════════════════════════════════════════════════════════════
    draw_title_block(
        ax,
        dwg_title='EQUIPMENT GENERAL ARRANGEMENT & SECTIONAL CAD',
        dwg_no='DWG-01',
        rev='00',
        sheet_no='01 OF 05',
        scale='1:35 METRIC / US CUSTOMARY',
        equip_desc='ETHYLENE OXIDATION MULTI-TUBULAR REACTOR (R-201) — 1000 TUBES x 1.5" SCH 80',
        duty_desc='FA0 = 0.9 LB-MOL/S | P0 = 25 ATM | T = 260 C | X = 0.40 | CAT W = 26,469 LB | deltaP = 4.00 ATM'
    )

    plt.savefig(out_png, dpi=300)
    plt.savefig(out_pdf)
    plt.close()
    print(f"[SUCCESS] DWG-01 generated: {out_png}")
    print(f"[SUCCESS] DWG-01 generated: {out_pdf}")

if __name__ == '__main__':
    out_dir = r"d:\GAMES\zercxes\CAD_Engineering_Drawings"
    generate_reactor_dwg01(
        os.path.join(out_dir, "01_Ethylene_Oxide_Reactor_General_Arrangement_Elevation_CAD.pdf"),
        os.path.join(out_dir, "01_Ethylene_Oxide_Reactor_General_Arrangement_Elevation_CAD.png")
    )
