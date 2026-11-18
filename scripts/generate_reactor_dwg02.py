"""
DWG-02: DETAILED PROCESS PIPING & INSTRUMENTATION DIAGRAM (P&ID)
VAPOR-PHASE ETHYLENE OXIDATION MULTI-TUBULAR REACTOR PLANT (R-201)
COMPLETE CLOSED-LOOP PIPING, STOICHIOMETRIC AIR RATIO CONTROL,
SHELL ISOTHERMAL STEAM GENERATION LOOP & RECOVERY TRAIN
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

def cad_valve_pid(ax, cx, cy, orientation='H', size=0.45, vtype='GATE', zorder=5):
    s = size / 2.0
    if orientation == 'H':
        p1 = [(cx - s, cy + s / 1.5), (cx, cy), (cx - s, cy - s / 1.5)]
        p2 = [(cx + s, cy + s / 1.5), (cx, cy), (cx + s, cy - s / 1.5)]
        ax.add_patch(Polygon(p1, closed=True, fc='#ffffff', ec=BK, lw=0.8, zorder=zorder))
        ax.add_patch(Polygon(p2, closed=True, fc='#ffffff', ec=BK, lw=0.8, zorder=zorder))
        if vtype == 'CONTROL':
            cad_line(ax, cx, cy, cx, cy + s * 1.3, lw=0.8, zorder=zorder)
            ax.add_patch(Arc((cx, cy + s * 1.8), s * 1.6, s * 1.0, theta1=0, theta2=180, ec=BK, lw=0.9, zorder=zorder))
            cad_line(ax, cx - s * 0.8, cy + s * 1.8, cx + s * 0.8, cy + s * 1.8, lw=0.9, zorder=zorder)
        elif vtype == 'CHECK':
            ax.add_patch(Circle((cx, cy), s * 0.4, fc='#111111', ec=BK, lw=0.5, zorder=zorder+1))
        elif vtype == 'PSV':
            cad_line(ax, cx, cy, cx, cy + s * 1.2, lw=0.8, zorder=zorder)
            cad_rect(ax, cx - s * 0.4, cy + s * 1.2, s * 0.8, s * 0.8, lw=0.8, fill=True, fc='#ffffff', zorder=zorder)
    else:
        p1 = [(cx - s / 1.5, cy - s), (cx, cy), (cx + s / 1.5, cy - s)]
        p2 = [(cx - s / 1.5, cy + s), (cx, cy), (cx + s / 1.5, cy + s)]
        ax.add_patch(Polygon(p1, closed=True, fc='#ffffff', ec=BK, lw=0.8, zorder=zorder))
        ax.add_patch(Polygon(p2, closed=True, fc='#ffffff', ec=BK, lw=0.8, zorder=zorder))
        if vtype == 'CONTROL':
            cad_line(ax, cx, cy, cx + s * 1.3, cy, lw=0.8, zorder=zorder)
            ax.add_patch(Arc((cx + s * 1.8, cy), s * 1.0, s * 1.6, theta1=270, theta2=90, ec=BK, lw=0.9, zorder=zorder))
            cad_line(ax, cx + s * 1.8, cy - s * 0.8, cx + s * 1.8, cy + s * 0.8, lw=0.9, zorder=zorder)

def cad_bubble_pid(ax, cx, cy, line1, line2, r=0.55, loc='DCS', sz=5.2):
    ax.add_patch(Circle((cx, cy), r, fc='#ffffff', ec=BK, lw=0.9, zorder=6))
    if loc == 'DCS':
        cad_line(ax, cx - r, cy, cx + r, cy, lw=0.6, ls='-', zorder=7)
    cad_text(ax, cx, cy + 0.16, line1, sz=sz, bold=True, zorder=8)
    cad_text(ax, cx, cy - 0.18, line2, sz=max(3.8, sz - 0.5), bold=True, zorder=8)

def generate_reactor_dwg02(out_pdf, out_png):
    fig, ax = create_cad_canvas()
    draw_sheet_border(ax)

    # ═════════════════════════════════════════════════════════════════════════
    # HEADER BANNER
    # ═════════════════════════════════════════════════════════════════════════
    cad_text(ax, W / 2.0, H - 2.0, 'TRIPLE-EFFECT / MULTI-STAGE PROCESS PIPING & INSTRUMENTATION DIAGRAM (P&ID)', sz=10.5, bold=True)
    cad_text(ax, W / 2.0, H - 2.8, 'VAPOR-PHASE ETHYLENE OXIDATION TUBULAR REACTOR (R-201) — FULL CLOSED-LOOP INSTRUMENTATION & INTERLOCKS', sz=7.8, bold=True, color='#0a3d62')
    cad_line(ax, 8.0, H - 3.4, W - 8.0, H - 3.4, lw=1.2, color='#2980b9')

    # ═════════════════════════════════════════════════════════════════════════
    # EQUIPMENT LAYOUT (Optimized spacing across X = 2.0 to 62.0)
    # ═════════════════════════════════════════════════════════════════════════
    # 1. Air Compressor C-201 (Bottom Left: X = 5.5, Y = 14.5)
    # 2. Feed Preheater E-201 (X = 15.5, Y = 36.0)
    # 3. Static Mixer M-201 (X = 21.5, Y = 46.0)
    # 4. Reactor R-201 (X = 32.0, Center Y = 30.0)
    # 5. Steam Drum V-201 (X = 45.0, Y = 43.0)
    # 6. Coolant Pumps P-201A/B (X = 45.0, Y = 13.0)
    # 7. Effluent Cooler E-202 (X = 47.0, Y = 24.0)
    # 8. Absorber C-201 (X = 57.5, Y = 28.0)
    # 9. Right Panel Tables: X = 63.5 to 82.5

    # EQUIPMENT 1: AIR COMPRESSOR C-201
    cx_c, cy_c = 5.5, 14.5
    cad_rect(ax, cx_c - 1.4, cy_c - 1.1, 2.8, 2.2, lw=1.2, fill=True, fc='#f1f2f6')
    poly_c = [(cx_c - 1.1, cy_c - 0.9), (cx_c - 1.1, cy_c + 0.9), (cx_c + 0.9, cy_c + 0.5), (cx_c + 0.9, cy_c - 0.5)]
    ax.add_patch(Polygon(poly_c, closed=True, fc='#ffffff', ec=BK, lw=1.2, zorder=3))
    cad_text(ax, cx_c - 0.1, cy_c, 'C-201\nAIR COMP.', sz=5.2, bold=True)
    cad_circle(ax, cx_c + 1.8, cy_c, 0.55, lw=1.0, fill=True, fc='#ffffff')
    cad_text(ax, cx_c + 1.8, cy_c, 'M', sz=6.0, bold=True)
    cad_line(ax, cx_c + 0.9, cy_c, cx_c + 1.25, cy_c, lw=1.0)
    
    # Air Inlet Filter F-101
    cad_rect(ax, cx_c - 3.5, cy_c - 0.6, 1.1, 1.2, lw=1.0, fill=True, fc='#ffffff')
    cad_hatch_rect(ax, cx_c - 3.5, cy_c - 0.6, 1.1, 1.2, pitch=0.2, lw=0.3)
    cad_text(ax, cx_c - 2.9, cy_c + 1.0, 'F-101\nFILTER', sz=4.5, bold=True)
    cad_line(ax, cx_c - 2.4, cy_c, cx_c - 1.1, cy_c, lw=1.2)
    cad_arrow(ax, cx_c - 1.8, cy_c, cx_c - 1.3, cy_c, lw=1.2)

    # EQUIPMENT 2: FEED PREHEATER E-201
    ex, ey = 15.5, 36.0
    ew, eh = 4.2, 2.4
    cad_rect(ax, ex - ew / 2.0, ey - eh / 2.0, ew, eh, lw=1.2, fill=True, fc='#ffffff')
    cad_line(ax, ex - ew / 2.0 + 0.4, ey + 0.5, ex + ew / 2.0 - 0.4, ey + 0.5, lw=0.6)
    cad_line(ax, ex - ew / 2.0 + 0.4, ey, ex + ew / 2.0 - 0.4, ey, lw=0.6)
    cad_line(ax, ex - ew / 2.0 + 0.4, ey - 0.5, ex + ew / 2.0 - 0.4, ey - 0.5, lw=0.6)
    cad_text(ax, ex, ey + eh / 2.0 + 0.7, 'E-201\nFEED PREHEATER', sz=5.2, bold=True)

    # EQUIPMENT 3: STATIC IN-LINE MIXER M-201
    mx, my = 21.5, 46.0
    cad_rect(ax, mx - 1.1, my - 0.5, 2.2, 1.0, lw=1.0, fill=True, fc='#fff2cc')
    cad_line(ax, mx - 0.9, my - 0.4, mx + 0.9, my + 0.4, lw=0.6, ls='--')
    cad_line(ax, mx - 0.9, my + 0.4, mx + 0.9, my - 0.4, lw=0.6, ls='--')
    cad_text(ax, mx, my + 0.9, 'M-201\nSTATIC MIXER', sz=4.8, bold=True)

    # EQUIPMENT 4: MULTI-TUBULAR REACTOR R-201
    rx, ry = 32.0, 30.0
    rw, rh = 6.8, 23.0
    r_r = rw / 2.0
    
    cad_rect(ax, rx - r_r, ry - rh / 2.0, rw, rh, lw=1.5, fill=True, fc='#ffffff')
    ax.add_patch(Arc((rx, ry + rh / 2.0), rw, 3.2, theta1=0, theta2=180, ec=BK, lw=1.5, fc='#ffffff'))
    ax.add_patch(Arc((rx, ry - rh / 2.0), rw, 3.2, theta1=180, theta2=360, ec=BK, lw=1.5, fc='#ffffff'))
    
    cad_rect(ax, rx - r_r - 0.4, ry + rh / 2.0 - 1.2, rw + 0.8, 0.8, lw=1.0, fill=True, fc='#bdc3c7')
    cad_rect(ax, rx - r_r - 0.4, ry - rh / 2.0 + 0.4, rw + 0.8, 0.8, lw=1.0, fill=True, fc='#bdc3c7')
    
    for tx in np.linspace(rx - r_r + 0.7, rx + r_r - 0.7, 9):
        cad_line(ax, tx, ry - rh / 2.0 + 1.2, tx, ry + rh / 2.0 - 1.2, lw=0.6, color='#555555')
        cad_rect(ax, tx - 0.12, ry - rh / 2.0 + 1.4, 0.24, rh - 2.8, lw=0.0, fill=True, fc='#f5cd79')
        
    cad_line(ax, rx - r_r, ry + 4.8, rx + r_r - 1.8, ry + 4.8, lw=1.2, color='#2980b9')
    cad_line(ax, rx - r_r + 1.8, ry, rx + r_r, ry, lw=1.2, color='#2980b9')
    cad_line(ax, rx - r_r, ry - 4.8, rx + r_r - 1.8, ry - 4.8, lw=1.2, color='#2980b9')
    
    cad_text(ax, rx, ry, 'R-201\nETHYLENE OXIDATION\nPACKED BED REACTOR\n1,000 TUBES x 1.5" SCH 80\nAg / Al2O3 CATALYST\n(W = 26,469 LB)',
             sz=5.6, bold=True, bg='white')

    # EQUIPMENT 5: STEAM SEPARATOR DRUM V-201
    vx, vy = 45.0, 43.0
    vw, vh = 4.8, 2.5
    cad_rect(ax, vx - vw / 2.0, vy - vh / 2.0, vw, vh, lw=1.2, fill=True, fc='#ffffff')
    ax.add_patch(Arc((vx - vw / 2.0, vy), 1.5, vh, theta1=90, theta2=270, ec=BK, lw=1.2))
    ax.add_patch(Arc((vx + vw / 2.0, vy), 1.5, vh, theta1=270, theta2=90, ec=BK, lw=1.2))
    cad_line(ax, vx - vw / 2.0, vy - 0.2, vx + vw / 2.0, vy - 0.2, lw=0.6, ls='--')
    cad_text(ax, vx, vy + 0.5, 'V-201\nSTEAM DRUM (400 PSIG)', sz=4.8, bold=True)

    # EQUIPMENT 6: COOLANT CIRCULATION PUMPS P-201A/B
    px1, py1 = 43.5, 12.5
    px2, py2 = 47.0, 12.5
    for px, py, tag in [(px1, py1, 'P-201A'), (px2, py2, 'P-201B')]:
        cad_circle(ax, px, py, 0.70, lw=1.1, fill=True, fc='#ffffff')
        poly_p = [(px - 0.45, py - 0.35), (px + 0.55, py), (px - 0.45, py + 0.35)]
        ax.add_patch(Polygon(poly_p, closed=True, fc='#111111', ec=BK, lw=0.6))
        cad_text(ax, px, py - 1.1, f'{tag}\nCOOLANT', sz=4.5, bold=True)

    # EQUIPMENT 7: EFFLUENT COOLER E-202
    cx2, cy2 = 47.0, 23.5
    cw2, ch2 = 4.0, 2.2
    cad_rect(ax, cx2 - cw2 / 2.0, cy2 - ch2 / 2.0, cw2, ch2, lw=1.2, fill=True, fc='#ffffff')
    cad_line(ax, cx2 - cw2 / 2.0 + 0.3, cy2 + 0.4, cx2 + cw2 / 2.0 - 0.3, cy2 + 0.4, lw=0.6)
    cad_line(ax, cx2 - cw2 / 2.0 + 0.3, cy2, cx2 + cw2 / 2.0 - 0.3, cy2, lw=0.6)
    cad_line(ax, cx2 - cw2 / 2.0 + 0.3, cy2 - 0.4, cx2 + cw2 / 2.0 - 0.3, cy2 - 0.4, lw=0.6)
    cad_text(ax, cx2, cy2 + ch2 / 2.0 + 0.6, 'E-202\nEFFLUENT COOLER', sz=4.8, bold=True)

    # EQUIPMENT 8: ETHYLENE OXIDE ABSORBER COLUMN C-201
    ab_x, ab_y = 57.5, 27.5
    ab_w, ab_h = 3.8, 20.0
    cad_rect(ax, ab_x - ab_w / 2.0, ab_y - ab_h / 2.0, ab_w, ab_h, lw=1.3, fill=True, fc='#ffffff')
    ax.add_patch(Arc((ab_x, ab_y + ab_h / 2.0), ab_w, 2.2, theta1=0, theta2=180, ec=BK, lw=1.3))
    ax.add_patch(Arc((ab_x, ab_y - ab_h / 2.0), ab_w, 2.2, theta1=180, theta2=360, ec=BK, lw=1.3))
    cad_rect(ax, ab_x - ab_w / 2.0 + 0.3, ab_y + 1.8, ab_w - 0.6, 4.5, lw=0.6, fill=True, fc='#dcdde1')
    cad_hatch_rect(ax, ab_x - ab_w / 2.0 + 0.3, ab_y + 1.8, ab_w - 0.6, 4.5, pitch=0.35, lw=0.3)
    cad_rect(ax, ab_x - ab_w / 2.0 + 0.3, ab_y - 5.5, ab_w - 0.6, 4.5, lw=0.6, fill=True, fc='#dcdde1')
    cad_hatch_rect(ax, ab_x - ab_w / 2.0 + 0.3, ab_y - 5.5, ab_w - 0.6, 4.5, pitch=0.35, lw=0.3)
    cad_text(ax, ab_x, ab_y - 0.4, 'C-201\nETHYLENE OXIDE\nABSORBER\nWATER WASH', sz=5.0, bold=True, bg='white')

    # ═════════════════════════════════════════════════════════════════════════
    # CLOSED-LOOP CONTINUOUS PIPING
    # ═════════════════════════════════════════════════════════════════════════
    # LINE 1: ETHYLENE FEED LINE
    cad_line(ax, 2.0, 46.0, mx - 1.1, 46.0, lw=1.4)
    cad_arrow(ax, 3.8, 46.0, 4.8, 46.0, lw=1.4)
    cad_arrow(ax, 13.5, 46.0, 14.5, 46.0, lw=1.4)
    cad_text(ax, 3.2, 46.6, '10"-EO-101-CS300\nC2H4 FEED (0.9 LBMOL/S @ 25 ATM)', sz=4.5, bold=True)
    
    cad_valve_pid(ax, 5.5, 46.0, orientation='H', size=0.50, vtype='CONTROL')
    cad_text(ax, 5.5, 47.2, 'ESDV-101', sz=4.2, bold=True)
    cad_valve_pid(ax, 11.5, 46.0, orientation='H', size=0.50, vtype='CONTROL')
    cad_text(ax, 11.5, 47.2, 'FCV-101', sz=4.2, bold=True)
    
    cad_line(ax, 8.0, 46.0, 8.0, 48.8, lw=0.5, ls='--')
    cad_bubble_pid(ax, 8.0, 48.8, 'PT', '101')
    cad_line(ax, 9.5, 46.0, 9.5, 48.8, lw=0.5, ls='--')
    cad_bubble_pid(ax, 9.5, 48.8, 'TT', '101')
    cad_line(ax, 11.5, 46.0 + 0.50 * 1.8, 11.5, 51.5, lw=0.5, ls='--')
    cad_bubble_pid(ax, 11.5, 51.5, 'FIC', '101')
    cad_line(ax, 11.5, 49.0, 13.0, 49.0, lw=0.5, ls='--')
    cad_bubble_pid(ax, 13.0, 49.0, 'FT', '101')
    cad_line(ax, 13.0, 46.0, 13.0, 49.0 - 0.55, lw=0.5, ls='--')

    # LINE 2: AIR FEED LINE
    cad_line(ax, cx_c + 0.9, cy_c, 9.5, cy_c, lw=1.4)
    cad_line(ax, 9.5, cy_c, 9.5, 25.0, lw=1.4)
    cad_arrow(ax, 9.5, 18.0, 9.5, 19.5, lw=1.4)
    cad_text(ax, 10.2, 19.0, '12"-AIR-102-CS300 (0.45 LBMOL/S O2)', sz=4.5, bold=True, rotation=90)
    
    cad_valve_pid(ax, 9.5, 23.0, orientation='V', size=0.50, vtype='CONTROL')
    cad_text(ax, 10.7, 23.0, 'FCV-102', sz=4.2, bold=True)
    
    cad_line(ax, 9.5 + 0.50 * 1.8, 23.0, 13.0, 23.0, lw=0.5, ls='--')
    cad_bubble_pid(ax, 13.0, 23.0, 'FFIC', '102')
    cad_line(ax, 13.0, 23.0 + 0.55, 13.0, 49.0 - 0.55, lw=0.5, ls='--')
    cad_text(ax, 13.7, 32.0, 'STOICHIOMETRIC RATIO = 0.50 O2/C2H4\n(AIR FLOW CASCADE)', sz=4.2, bold=True, color='#c0392b', rotation=90)
    
    cad_line(ax, 9.5, 25.0, mx, 25.0, lw=1.4)
    cad_line(ax, mx, 25.0, mx, my - 0.5, lw=1.4)
    cad_arrow(ax, mx, 34.0, mx, 36.0, lw=1.4)

    # LINE 3: MIXED FEED THROUGH E-201 INTO REACTOR
    cad_line(ax, mx + 1.1, my, 25.5, my, lw=1.4)
    cad_line(ax, 25.5, my, 25.5, ey, lw=1.4)
    cad_line(ax, 25.5, ey, ex + ew / 2.0, ey, lw=1.4)
    cad_arrow(ax, 21.0, ey, ex + ew / 2.0, ey, lw=1.4)
    
    cad_line(ax, ex, ey + eh / 2.0 + 1.8, ex, ey + eh / 2.0, lw=0.9)
    cad_valve_pid(ax, ex, ey + eh / 2.0 + 1.0, orientation='V', size=0.45, vtype='CONTROL')
    cad_text(ax, ex - 1.1, ey + eh / 2.0 + 1.0, 'TCV-201', sz=4.0, bold=True)
    cad_bubble_pid(ax, ex - 1.8, ey + eh / 2.0 + 1.0, 'TIC', '201')
    cad_line(ax, ex - 1.8 + 0.55, ey + eh / 2.0 + 1.0, ex - 0.45, ey + eh / 2.0 + 1.0, lw=0.5, ls='--')
    cad_text(ax, ex, ey + eh / 2.0 + 2.1, 'M.P. STEAM (15 BAR)', sz=4.2, bold=True)
    
    cad_line(ax, ex - ew / 2.0, ey, 13.5, ey, lw=1.4)
    cad_line(ax, 13.5, ey, 13.5, 49.5, lw=1.4)
    cad_line(ax, 13.5, 49.5, rx, 49.5, lw=1.4)
    cad_line(ax, rx, 49.5, rx, ry + rh / 2.0 + 1.6, lw=1.4)
    cad_arrow(ax, 23.0, 49.5, 25.0, 49.5, lw=1.4)
    cad_text(ax, 22.0, 50.2, '14"-FEED-103-CS300 | 25 ATM, 260 DEG C (ISOTHERMAL FEED)', sz=4.8, bold=True)

    # LINE 4: REACTOR SHELL COOLANT ISOTHERMAL LOOP
    cad_line(ax, px1, py1 + 0.70, px1, 15.0, lw=1.2)
    cad_line(ax, px2, py2 + 0.70, px2, 15.0, lw=1.2)
    cad_line(ax, px1, 15.0, px2, 15.0, lw=1.2)
    cad_line(ax, 45.0, 15.0, 45.0, ry - 8.5, lw=1.4)
    cad_line(ax, 45.0, ry - 8.5, rx + r_r, ry - 8.5, lw=1.4)
    cad_arrow(ax, 41.0, ry - 8.5, 39.0, ry - 8.5, lw=1.4)
    cad_valve_pid(ax, 41.0, ry - 8.5, orientation='H', size=0.45, vtype='CHECK')
    cad_text(ax, 41.0, ry - 7.7, '10"-BFW-104-CS300\nCOOLANT INLET', sz=4.2, bold=True)
    
    cad_line(ax, rx + r_r, ry + 8.5, 41.0, ry + 8.5, lw=1.4)
    cad_line(ax, 41.0, ry + 8.5, 41.0, vy, lw=1.4)
    cad_line(ax, 41.0, vy, vx - vw / 2.0, vy, lw=1.4)
    cad_arrow(ax, 41.0, 40.0, 41.0, 41.5, lw=1.4)
    cad_text(ax, 40.0, 35.0, '12"-STM-105-CS300\nBOILING MIXTURE (260 C)', sz=4.2, bold=True, rotation=90)
    
    cad_line(ax, vx, vy - vh / 2.0, vx, 9.5, lw=1.4)
    cad_line(ax, vx, 9.5, px1, 9.5, lw=1.2)
    cad_line(ax, px1, 9.5, px1, py1 - 0.70, lw=1.2)
    cad_line(ax, vx, 9.5, px2, 9.5, lw=1.2)
    cad_line(ax, px2, 9.5, px2, py2 - 0.70, lw=1.2)
    cad_arrow(ax, vx, 11.5, vx, 10.5, lw=1.2)
    cad_text(ax, vx + 0.8, 11.0, 'LIQUID RECIRC.', sz=4.0, bold=True)
    
    # BFW Makeup into Steam Drum
    cad_line(ax, vx + vw / 2.0, vy - 0.2, vx + vw / 2.0 + 2.5, vy - 0.2, lw=1.0)
    cad_valve_pid(ax, vx + vw / 2.0 + 1.2, vy - 0.2, orientation='H', size=0.45, vtype='CONTROL')
    cad_text(ax, vx + vw / 2.0 + 1.2, vy + 0.5, 'LCV-201', sz=4.0, bold=True)
    cad_text(ax, vx + vw / 2.0 + 2.7, vy - 0.2, 'BFW MAKEUP', sz=4.2, bold=True)
    cad_bubble_pid(ax, vx, vy + 1.8, 'LIC', '201')
    cad_line(ax, vx + 0.55, vy + 1.8, vx + vw / 2.0 + 1.2, vy + 1.8, lw=0.5, ls='--')
    cad_line(ax, vx + vw / 2.0 + 1.2, vy + 1.8, vx + vw / 2.0 + 1.2, vy + 0.5 + 0.45, lw=0.5, ls='--')
    
    # Export Steam from Steam Drum Top
    cad_line(ax, vx, vy + vh / 2.0, vx, vy + vh / 2.0 + 3.2, lw=1.2)
    cad_valve_pid(ax, vx, vy + vh / 2.0 + 1.8, orientation='V', size=0.45, vtype='CONTROL')
    cad_text(ax, vx + 1.1, vy + vh / 2.0 + 1.8, 'PCV-201', sz=4.0, bold=True)
    cad_bubble_pid(ax, vx - 1.5, vy + vh / 2.0 + 1.8, 'PIC', '201')
    cad_line(ax, vx - 1.5 + 0.55, vy + vh / 2.0 + 1.8, vx - 0.45, vy + vh / 2.0 + 1.8, lw=0.5, ls='--')
    cad_arrow(ax, vx, vy + vh / 2.0 + 2.6, vx, vy + vh / 2.0 + 3.1, lw=1.2)
    cad_text(ax, vx, vy + vh / 2.0 + 3.8, '400 PSIG SAT. STEAM TO PLANT HEADER\nHEAT OF RXN RECOVERY (-105 KJ/MOL)', sz=4.5, bold=True, color='#27ae60')

    # LINE 5: REACTOR EFFLUENT LINE
    cad_line(ax, rx, ry - rh / 2.0 - 1.6, rx, 9.5, lw=1.4)
    cad_line(ax, rx, 9.5, 38.0, 9.5, lw=1.4)
    cad_line(ax, 38.0, 9.5, 38.0, cy2, lw=1.4)
    cad_line(ax, 38.0, cy2, cx2 - cw2 / 2.0, cy2, lw=1.4)
    cad_arrow(ax, 38.0, 15.0, 38.0, 17.0, lw=1.4)
    cad_text(ax, 34.0, 10.3, '14"-EP-106-CS300 | 21 ATM, 260 DEG C (X = 0.40)', sz=4.8, bold=True)
    
    # Differential Pressure Transmitter PDIT-201
    cad_line(ax, rx - r_r - 0.4, ry + 9.0, rx - r_r - 2.2, ry + 9.0, lw=0.5, ls='--')
    cad_line(ax, rx - r_r - 0.4, ry - 9.0, rx - r_r - 2.2, ry - 9.0, lw=0.5, ls='--')
    cad_line(ax, rx - r_r - 2.2, ry - 9.0, rx - r_r - 2.2, ry + 9.0, lw=0.5, ls='--')
    cad_bubble_pid(ax, rx - r_r - 2.2, ry, 'PDIT', '201')
    cad_text(ax, rx - r_r - 2.2, ry - 1.1, 'deltaP = 4.00 ATM\n(58.8 PSI)', sz=4.0, bold=True, color='#c0392b')
    
    cad_line(ax, rx - r_r - 0.4, ry + 4.5, rx - r_r - 1.3, ry + 4.5, lw=0.5, ls='--')
    cad_bubble_pid(ax, rx - r_r - 1.3, ry + 4.5, 'TI', '201A', sz=4.5)
    cad_line(ax, rx - r_r - 0.4, ry - 4.5, rx - r_r - 1.3, ry - 4.5, lw=0.5, ls='--')
    cad_bubble_pid(ax, rx - r_r - 1.3, ry - 4.5, 'TI', '201D', sz=4.5)

    # LINE 6: COOLED EFFLUENT TO ABSORBER C-201
    cad_line(ax, cx2 + cw2 / 2.0, cy2, ab_x - ab_w / 2.0, cy2, lw=1.4)
    cad_arrow(ax, cx2 + cw2 / 2.0 + 1.0, cy2, cx2 + cw2 / 2.0 + 1.8, cy2, lw=1.4)
    cad_text(ax, cx2 + cw2 / 2.0 + 1.2, cy2 + 0.5, '14"-EP-107-CS300\nCOOLED GAS (35 C)', sz=4.2, bold=True)
    
    cad_line(ax, cx2, cy2 - ch2 / 2.0, cx2, cy2 - ch2 / 2.0 - 2.2, lw=1.0)
    cad_text(ax, cx2, cy2 - ch2 / 2.0 - 2.5, 'C.W. IN (25 C)', sz=4.2, bold=True)
    cad_line(ax, cx2, cy2 + ch2 / 2.0, cx2, cy2 + ch2 / 2.0 + 2.2, lw=1.0)
    cad_text(ax, cx2, cy2 + ch2 / 2.0 + 2.5, 'C.W. OUT (35 C)', sz=4.2, bold=True)

    # LINE 7: ABSORBER OVERHEAD & BOTTOM PRODUCT
    cad_line(ax, ab_x, ab_y + ab_h / 2.0 + 1.1, ab_x, ab_y + ab_h / 2.0 + 4.0, lw=1.2)
    cad_arrow(ax, ab_x, ab_y + ab_h / 2.0 + 2.8, ab_x, ab_y + ab_h / 2.0 + 3.6, lw=1.2)
    cad_text(ax, ab_x, ab_y + ab_h / 2.0 + 4.5, 'OFF-GAS RECYCLE & N2 PURGE\n(TO CO2 REMOVAL & C2H4 RECYCLE)', sz=4.5, bold=True, color='#2980b9')
    
    cad_line(ax, ab_x - ab_w / 2.0 - 2.2, ab_y + ab_h / 2.0 - 1.5, ab_x - ab_w / 2.0, ab_y + ab_h / 2.0 - 1.5, lw=1.0)
    cad_arrow(ax, ab_x - ab_w / 2.0 - 1.2, ab_y + ab_h / 2.0 - 1.5, ab_x - ab_w / 2.0 - 0.4, ab_y + ab_h / 2.0 - 1.5, lw=1.0)
    cad_text(ax, ab_x - ab_w / 2.0 - 2.4, ab_y + ab_h / 2.0 - 1.5, 'SCRUB WATER', sz=4.0, bold=True, ha='right')

    cad_line(ax, ab_x, ab_y - ab_h / 2.0 - 1.1, ab_x, ab_y - ab_h / 2.0 - 3.5, lw=1.2)
    cad_line(ax, ab_x, ab_y - ab_h / 2.0 - 3.5, ab_x + 3.5, ab_y - ab_h / 2.0 - 3.5, lw=1.2)
    cad_arrow(ax, ab_x + 2.0, ab_y - ab_h / 2.0 - 3.5, ab_x + 3.2, ab_y - ab_h / 2.0 - 3.5, lw=1.2)
    cad_text(ax, ab_x + 3.7, ab_y - ab_h / 2.0 - 3.5, 'CRUDE EO AQUEOUS SOLUTION\nTO EO STRIPPER / GLYCOL PLANT', sz=4.5, bold=True, color='#27ae60')

    # ═════════════════════════════════════════════════════════════════════════
    # P&ID TABLES (Far Right: X = 63.5 to 82.5, Width = 19.0 cm)
    # ═════════════════════════════════════════════════════════════════════════
    tbl_x0 = 63.5
    pid_headers = ['TAG', 'EQUIPMENT / UNIT', 'CAPACITY / DUTY', 'DESIGN CODE']
    pid_rows = [
        ['R-201', 'ETHYLENE OXIDATION PBR', '1,000 TUBES x 1.5" SCH 80', 'ASME SEC VIII DIV 1'],
        ['C-201', 'AIR FEED COMPRESSOR', '3.043 LBMOL/S AIR @ 25 ATM', 'API 617 / ASME PTC 10'],
        ['E-201', 'FEED PREHEATER', 'PREHEAT TO 260 C (M.P. STEAM)', 'TEMA CLASS R / ASME VIII'],
        ['M-201', 'STATIC GAS MIXER', 'HOMOGENEOUS C2H4/AIR BLENDING', 'ASME B31.3 PIPING'],
        ['V-201', 'COOLANT STEAM DRUM', '400 PSIG SAT. STEAM SEPARATION', 'ASME SEC VIII DIV 1'],
        ['P-201A/B', 'COOLANT PUMPS (1D+1S)', '150 M3/H BOILING WATER JACKET', 'API 610 CENTRIFUGAL'],
        ['E-202', 'EFFLUENT COOLER', 'COOL FROM 260 C TO 35 C', 'TEMA CLASS R / ASME VIII'],
        ['C-201', 'EO WATER ABSORBER', '700 MM ID x 12 M PACKED HEIGHT', 'ASME SEC VIII DIV 1']
    ]
    pid_widths = [1.5, 6.2, 6.8, 4.5]
    cad_draw_table(ax, tbl_x0, 36.0, pid_headers, pid_rows, pid_widths, row_h=0.55,
                   title='TABLE 1 — P&ID EQUIPMENT SCHEDULE', title_sz=7.2, sz=4.6)

    loop_headers = ['LOOP TAG', 'CONTROLLED VARIABLE', 'FINAL CONTROL ELEMENT', 'SAFETY ACTION / PHILOSOPHY']
    loop_rows = [
        ['FFIC-102', 'O2/C2H4 RATIO', 'AIR VALVE FCV-102', 'STRICT 0.50 RATIO CASCADE; PREVENTS FLAMMABLE MIXTURE'],
        ['FIC-101', 'ETHYLENE FEED', 'ETHYLENE FCV-101', 'MAINTAINS DESIGN 0.900 LBMOL/S (3,240 LBMOL/H)'],
        ['TIC-201', 'PREHEAT TEMP', 'STEAM VALVE TCV-201', 'CONTROLS EXACT 260.0 DEG C ISOTHERMAL FEED INLET'],
        ['PIC-201', 'JACKET PRESSURE', 'STEAM VALVE PCV-201', 'HOLDS 400 PSIG BOILING WATER TO REMOVE HEAT OF RXN'],
        ['LIC-201', 'STEAM DRUM LVL', 'BFW VALVE LCV-201', 'PREVENTS BOILER TUBE DRYOUT VIA CONTINUOUS BFW MAKEUP'],
        ['PDIT-201', 'BED PRESSURE DROP', 'DCS HIGH-DP ALARM', 'MONITORS ERGUN dP (4.00 ATM NORMAL; ALARM @ 5.0 ATM)'],
        ['ESDV-101', 'EMERGENCY TRIP', 'FAIL-CLOSE BALL VALVE', 'TRIPS ON HIGH BED TEMP (>280 C) OR LOW COOLANT FLOW']
    ]
    loop_widths = [1.8, 4.8, 4.6, 7.8]
    cad_draw_table(ax, tbl_x0, 16.5, loop_headers, loop_rows, loop_widths, row_h=0.55,
                   title='TABLE 2 — INSTRUMENTATION & INTERLOCKS', title_sz=7.2, sz=4.4)

    # ═════════════════════════════════════════════════════════════════════════
    # TITLE BLOCK (Bottom Full Width)
    # ═════════════════════════════════════════════════════════════════════════
    draw_title_block(
        ax,
        dwg_title='DETAILED PROCESS PIPING & INSTRUMENTATION DIAGRAM (P&ID)',
        dwg_no='DWG-02',
        rev='00',
        sheet_no='02 OF 05',
        scale='PIPING & INSTRUMENT SCHEMATIC / N.T.S.',
        equip_desc='ETHYLENE OXIDATION MULTI-TUBULAR REACTOR SYSTEM (R-201 & AUXILIARIES)',
        duty_desc='CLOSED PIPING LOOP | RATIO CONTROL FFIC-102 | STEAM GENERATION V-201 | ERGUN dP MONITORING'
    )

    plt.savefig(out_png, dpi=300)
    plt.savefig(out_pdf)
    plt.close()
    print(f"[SUCCESS] DWG-02 generated: {out_png}")
    print(f"[SUCCESS] DWG-02 generated: {out_pdf}")

if __name__ == '__main__':
    out_dir = r"d:\GAMES\zercxes\CAD_Engineering_Drawings"
    generate_reactor_dwg02(
        os.path.join(out_dir, "02_Ethylene_Oxide_Reactor_Process_PID_Instrumentation_CAD.pdf"),
        os.path.join(out_dir, "02_Ethylene_Oxide_Reactor_Process_PID_Instrumentation_CAD.png")
    )
