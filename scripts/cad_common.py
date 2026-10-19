"""
CAD COMMON UTILITIES FOR HIGH-PRECISION ENGINEERING DRAWINGS
Standard: ISO 5457 / ISO 7200 / ASME Y14 Series / ISA-5.1
Subject: PROCESS EQUIPMENT DESIGN & DRAWING
Student: SOURISH SENAPATI | Roll: 002310301035 | Date: 29/09/2026
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle, Circle, Polygon, Arc, Wedge, FancyBboxPatch
import numpy as np

# Canvas Setup: ISO A1 Landscape (84.1 x 59.4 cm)
W, H = 84.1, 59.4
FONT_CAD = 'DejaVu Sans'
BK = '#000000'
GREY = '#444444'

def create_cad_canvas():
    fig = plt.figure(figsize=(W / 2.54, H / 2.54), dpi=300)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor('white')
    return fig, ax

def cad_line(ax, x1, y1, x2, y2, lw=0.9, ls='-', color=BK, zorder=3):
    ax.plot([x1, x2], [y1, y2], color=color, lw=lw, ls=ls, zorder=zorder, solid_capstyle='butt')

def cad_rect(ax, x, y, w, h, lw=0.9, ls='-', fill=False, fc='white', ec=BK, zorder=2):
    fill_color = fc if fill else 'none'
    ax.add_patch(Rectangle((x, y), w, h, fc=fill_color, ec=ec, lw=lw, linestyle=ls, zorder=zorder))

def cad_circle(ax, cx, cy, r, lw=0.9, ls='-', fill=False, fc='white', ec=BK, zorder=2):
    fill_color = fc if fill else 'none'
    ax.add_patch(Circle((cx, cy), r, fc=fill_color, ec=ec, lw=lw, linestyle=ls, zorder=zorder))

def cad_arc(ax, cx, cy, width, height, angle=0.0, theta1=0.0, theta2=360.0, lw=0.9, ls='-', color=BK, zorder=3):
    arc = Arc((cx, cy), width, height, angle=angle, theta1=theta1, theta2=theta2, color=color, lw=lw, linestyle=ls, zorder=zorder)
    ax.add_patch(arc)

def cad_text(ax, x, y, text, sz=7.0, ha='center', va='center', bold=False, zorder=8, bg=None, color=BK, rotation=0):
    weight = 'bold' if bold else 'normal'
    bbox_dict = dict(boxstyle='square,pad=0.15', fc='white', ec='none', alpha=1.0) if bg else None
    ax.text(x, y, str(text), fontsize=sz, ha=ha, va=va, color=color,
            fontweight=weight, fontfamily=FONT_CAD, zorder=zorder, bbox=bbox_dict, rotation=rotation)

def cad_arrow(ax, x1, y1, x2, y2, lw=1.0, ls='-', color=BK, zorder=5, head_scale=10):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw,
                                linestyle=ls, shrinkA=0, shrinkB=0,
                                mutation_scale=head_scale),
                zorder=zorder)

def cad_dim_h(ax, x1, x2, y, label, ext=0.35, sz=6.5, bold=True, bg='white'):
    cad_line(ax, x1, y - ext, x1, y + ext, lw=0.5)
    cad_line(ax, x2, y - ext, x2, y + ext, lw=0.5)
    cad_line(ax, x1, y, x2, y, lw=0.6)
    t = 0.12
    cad_line(ax, x1 - t, y - t, x1 + t, y + t, lw=0.9)
    cad_line(ax, x2 - t, y - t, x2 + t, y + t, lw=0.9)
    cad_text(ax, (x1 + x2)/2, y + 0.22, label, sz=sz, bold=bold, bg=bg)

def cad_dim_v(ax, x, y1, y2, label, ext=0.35, sz=6.5, bold=True, bg='white', text_offset=-0.38):
    cad_line(ax, x - ext, y1, x + ext, y1, lw=0.5)
    cad_line(ax, x - ext, y2, x + ext, y2, lw=0.5)
    cad_line(ax, x, y1, x, y2, lw=0.6)
    t = 0.12
    cad_line(ax, x - t, y1 - t, x + t, y1 + t, lw=0.9)
    cad_line(ax, x - t, y2 - t, x + t, y2 + t, lw=0.9)
    cad_text(ax, x + text_offset, (y1 + y2)/2, label, sz=sz, bold=bold, bg=bg)

def cad_dim_leader(ax, x_target, y_target, x_knee, y_knee, x_end, text, sz=6.0, bold=True):
    cad_line(ax, x_target, y_target, x_knee, y_knee, lw=0.6)
    cad_line(ax, x_knee, y_knee, x_end, y_knee, lw=0.6)
    cad_circle(ax, x_target, y_target, 0.08, fill=True, fc=BK, lw=0.5, zorder=6)
    ha = 'left' if x_end >= x_knee else 'right'
    cad_text(ax, x_end + (0.2 if ha == 'left' else -0.2), y_knee + 0.15, text, sz=sz, ha=ha, bold=bold)

def cad_balloon(ax, cx, cy, mark, radius=0.45, sz=6.5):
    ax.add_patch(Circle((cx, cy), radius, fc='white', ec=BK, lw=0.8, zorder=6))
    cad_text(ax, cx, cy, mark, sz=sz, bold=True)

def cad_flange(ax, x, y, orientation='V', length=0.60, thickness=0.14, lw=1.0):
    d = length / 2
    if orientation == 'V':
        cad_rect(ax, x - d, y, length, thickness, lw=lw, fill=True, zorder=4)
        cad_line(ax, x - d - 0.08, y + thickness/2, x + d + 0.08, y + thickness/2, lw=0.4, ls='-.')
    else:
        cad_rect(ax, x, y - d, thickness, length, lw=lw, fill=True, zorder=4)
        cad_line(ax, x + thickness/2, y - d - 0.08, x + thickness/2, y + d + 0.08, lw=0.4, ls='-.')

def cad_hatch_rect(ax, x, y, w, h, pitch=0.30, lw=0.4, angle=45, color=BK):
    # Hatching inside rectangle
    if angle == 45:
        x_coords = np.arange(x - h, x + w + h, pitch)
        for xc in x_coords:
            x_start = max(x, xc)
            y_start = y + max(0, x - xc)
            x_end = min(x + w, xc + h)
            y_end = y + min(h, x + w - xc)
            if x_start < x_end and y_start < y_end:
                cad_line(ax, x_start, y_start, x_end, y_end, lw=lw, color=color, zorder=2)
    elif angle == -45:
        x_coords = np.arange(x, x + w + 2*h, pitch)
        for xc in x_coords:
            x_start = max(x, xc - h)
            y_start = y + min(h, xc - x)
            x_end = min(x + w, xc)
            y_end = y + max(0, xc - (x + w))
            if x_start < x_end and y_start > y_end:
                cad_line(ax, x_start, y_start, x_end, y_end, lw=lw, color=color, zorder=2)

def cad_valve(ax, cx, cy, orientation='H', size=0.50, valve_type='GATE', act='NONE', zorder=5):
    s = size / 2
    if orientation == 'H':
        p1 = [(cx - s, cy + s/1.5), (cx, cy), (cx - s, cy - s/1.5)]
        p2 = [(cx + s, cy + s/1.5), (cx, cy), (cx + s, cy - s/1.5)]
        ax.add_patch(Polygon(p1, closed=True, fc='white', ec=BK, lw=0.9, zorder=zorder))
        ax.add_patch(Polygon(p2, closed=True, fc='white', ec=BK, lw=0.9, zorder=zorder))
        if valve_type == 'CONTROL':
            cad_line(ax, cx, cy, cx, cy + s*1.4, lw=0.8, zorder=zorder)
            # Diaphragm actuator
            ax.add_patch(Arc((cx, cy + s*1.8), s*1.4, s*0.9, theta1=0, theta2=180, ec=BK, lw=0.9, zorder=zorder))
            cad_line(ax, cx - s*0.7, cy + s*1.8, cx + s*0.7, cy + s*1.8, lw=0.9, zorder=zorder)
            cad_line(ax, cx, cy + s*1.8, cx, cy + s*1.4, lw=0.8, zorder=zorder)
        elif valve_type == 'CHECK':
            cad_line(ax, cx, cy - s/1.5, cx, cy + s/1.5, lw=0.9, zorder=zorder)
        elif valve_type == 'BALL':
            cad_circle(ax, cx, cy, s*0.35, fill=True, fc=BK, lw=0.8, zorder=zorder+1)
        elif valve_type == 'SRV':
            cad_line(ax, cx, cy, cx, cy + s*1.2, lw=0.8, zorder=zorder)
            cad_rect(ax, cx - s*0.4, cy + s*1.2, s*0.8, s*0.8, lw=0.9, fill=True, zorder=zorder)
            cad_line(ax, cx - s*0.4, cy + s*1.2, cx + s*0.4, cy + s*2.0, lw=0.8, zorder=zorder)
    else:
        p1 = [(cx - s/1.5, cy - s), (cx, cy), (cx + s/1.5, cy - s)]
        p2 = [(cx - s/1.5, cy + s), (cx, cy), (cx + s/1.5, cy + s)]
        ax.add_patch(Polygon(p1, closed=True, fc='white', ec=BK, lw=0.9, zorder=zorder))
        ax.add_patch(Polygon(p2, closed=True, fc='white', ec=BK, lw=0.9, zorder=zorder))

def cad_instrument_bubble(ax, cx, cy, tag_line1, tag_line2, r=0.55, loc='FIELD', zorder=6, sz=5.5):
    ax.add_patch(Circle((cx, cy), r, fc='white', ec=BK, lw=0.9, zorder=zorder))
    if loc == 'PANEL':
        cad_line(ax, cx - r, cy, cx + r, cy, lw=0.8, ls='-', zorder=zorder+1)
    elif loc == 'DCS':
        cad_line(ax, cx - r, cy, cx + r, cy, lw=0.8, ls='--', zorder=zorder+1)
    cad_text(ax, cx, cy + 0.16 * (r/0.55), tag_line1, sz=sz, bold=True, zorder=zorder+2)
    cad_text(ax, cx, cy - 0.18 * (r/0.55), tag_line2, sz=max(3.5, sz - 0.4), bold=True, zorder=zorder+2)

def draw_sheet_border(ax):
    # Outer Border
    cad_rect(ax, 0.5, 0.5, W - 1.0, H - 1.0, lw=2.2)
    # Inner Border
    cad_rect(ax, 1.2, 1.2, W - 2.4, H - 2.4, lw=1.2)
    
    # ISO Grid 8x6 (Zones 1-8 horizontal, A-F vertical)
    zones_x, zones_y = 8, 6
    for i in range(1, zones_x):
        gx = 1.2 + i * (W - 2.4) / zones_x
        cad_line(ax, gx, 0.5, gx, 1.2, lw=0.6)
        cad_line(ax, gx, H - 1.2, gx, H - 0.5, lw=0.6)
        cad_text(ax, gx - (W - 2.4)/(2*zones_x), 0.85, str(i), sz=6.5, bold=True)
        cad_text(ax, gx - (W - 2.4)/(2*zones_x), H - 0.85, str(i), sz=6.5, bold=True)
    cad_text(ax, (W - 1.2) - (W - 2.4)/(2*zones_x), 0.85, str(zones_x), sz=6.5, bold=True)
    cad_text(ax, (W - 1.2) - (W - 2.4)/(2*zones_x), H - 0.85, str(zones_x), sz=6.5, bold=True)
    
    zone_letters = ['A', 'B', 'C', 'D', 'E', 'F']
    for j in range(1, zones_y):
        gy = 1.2 + j * (H - 2.4) / zones_y
        cad_line(ax, 0.5, gy, 1.2, gy, lw=0.6)
        cad_line(ax, W - 1.2, gy, W - 0.5, gy, lw=0.6)
        cad_text(ax, 0.85, gy - (H - 2.4)/(2*zones_y), zone_letters[j-1], sz=6.5, bold=True)
        cad_text(ax, W - 0.85, gy - (H - 2.4)/(2*zones_y), zone_letters[j-1], sz=6.5, bold=True)
    cad_text(ax, 0.85, (H - 1.2) - (H - 2.4)/(2*zones_y), zone_letters[zones_y-1], sz=6.5, bold=True)
    cad_text(ax, W - 0.85, (H - 1.2) - (H - 2.4)/(2*zones_y), zone_letters[zones_y-1], sz=6.5, bold=True)

def draw_title_block(ax, dwg_title, dwg_no, rev='00', sheet_no='01 OF 05', scale='1:25 METRIC / PROPORTIONED',
                     equip_desc='PACKED ABSORPTION COLUMN (C-101) — 750 MM ID x 4500 MM BED',
                     duty_desc='0.25 M³/S GAS (2 MOL% Br2) | 90% RECOVERY | WATER: 17.25 KG/S'):
    TB_X = 1.2
    TB_Y = 1.2
    TB_W = W - 2.4
    TB_H = 5.2
    
    cad_rect(ax, TB_X, TB_Y, TB_W, TB_H, lw=1.8, fill=True)
    Y_R1 = TB_Y + 4.10
    Y_R2 = TB_Y + 2.90
    Y_R3 = TB_Y + 1.70
    Y_R4 = TB_Y + 0.50
    
    cad_line(ax, TB_X, Y_R1, TB_X + TB_W, Y_R1, lw=1.2)
    cad_line(ax, TB_X, Y_R2, TB_X + TB_W, Y_R2, lw=0.9)
    cad_line(ax, TB_X, Y_R3, TB_X + TB_W, Y_R3, lw=0.9)
    cad_line(ax, TB_X, Y_R4, TB_X + TB_W, Y_R4, lw=0.9)
    
    col_splits_4 = [0.25, 0.50, 0.75]
    for cs in col_splits_4:
        cad_line(ax, TB_X + TB_W * cs, Y_R4, TB_X + TB_W * cs, Y_R1, lw=0.9)
    col_centers_4 = [0.125, 0.375, 0.625, 0.875]
    
    # Row 1: Header / Institution
    cad_text(ax, TB_X + TB_W / 2, TB_Y + 4.65,
             'JADAVPUR UNIVERSITY  |  CHEMICAL ENGINEERING DEPARTMENT  |  PROCESS EQUIPMENT DESIGN & DRAWING',
             sz=12.5, bold=True)
    
    # Row 2: Drawing Title, Subject, Course, Scale
    r2_h = ['DRAWING TITLE', 'LAB / SUBJECT', 'COURSE / BRANCH', 'SCALE & REVISION']
    r2_v = [dwg_title, 'PROCESS EQUIPMENT DESIGN & DRAWING', 'B.E. CHEMICAL ENGINEERING', f'SCALE: {scale}  |  REV: {rev}']
    for c_idx, (h_txt, v_txt) in enumerate(zip(r2_h, r2_v)):
        cx_pos = TB_X + TB_W * col_centers_4[c_idx]
        cad_text(ax, cx_pos, TB_Y + 3.65, h_txt, sz=6.5, bold=True)
        cad_text(ax, cx_pos, TB_Y + 3.25, v_txt, sz=8.8, bold=True)
    
    # Row 3: Student Details
    r3_h = ['STUDENT NAME', 'EXAM ROLL NUMBER', 'DRAWING / DOCUMENT NO.', 'DATE']
    r3_v = ['SOURISH SENAPATI', '002310301035', f'{dwg_no}  (SHEET {sheet_no})', '29 / 09 / 2026']
    for c_idx, (h_txt, v_txt) in enumerate(zip(r3_h, r3_v)):
        cx_pos = TB_X + TB_W * col_centers_4[c_idx]
        cad_text(ax, cx_pos, TB_Y + 2.45, h_txt, sz=6.5, bold=True)
        cad_text(ax, cx_pos, TB_Y + 2.05, v_txt, sz=9.0, bold=True)
    
    # Row 4: Equipment & Design Summary
    r4_h = ['EQUIPMENT IDENTIFICATION & SERVICE', 'DESIGN BASIS & METALLURGY / LINING', 'PROCESS PERFORMANCE & RECOVERY', 'DESIGN STATUS CLASSIFICATION']
    r4_v = [equip_desc,
            'ASME SEC VIII DIV 1 / SA-516 GR 70 + PVDF LINER / SS316L / CERAMIC',
            duty_desc,
            'CALCULATED: ID 750, Z 4500 | PRELIMINARY CAD: SHELL & NOZZLES']
    for c_idx, (h_txt, v_txt) in enumerate(zip(r4_h, r4_v)):
        cx_pos = TB_X + TB_W * col_centers_4[c_idx]
        cad_text(ax, cx_pos, TB_Y + 1.25, h_txt, sz=6.2, bold=True)
        cad_text(ax, cx_pos, TB_Y + 0.85, v_txt, sz=7.5, bold=True)
    
    # Bottom Note
    cad_text(ax, TB_X + TB_W / 2, TB_Y + 0.25,
             'DIMENSIONS: METRIC (MM / M)  |  FLANGES: ASME B16.5 CLASS 150 RF  |  WELDING: ASME SEC IX  |  THIRD ANGLE PROJECTION',
             sz=7.2, bold=True)
    
    # Third Angle Projection Symbol
    proj_cx = TB_X + 2.5
    proj_cy = TB_Y + TB_H + 0.75
    cad_text(ax, proj_cx, proj_cy + 0.45, 'THIRD ANGLE PROJECTION', sz=5.5, bold=True)
    p_cone = [(proj_cx - 0.7, proj_cy - 0.25), (proj_cx - 0.7, proj_cy + 0.25),
              (proj_cx - 0.2, proj_cy + 0.12), (proj_cx - 0.2, proj_cy - 0.12)]
    ax.add_patch(Polygon(p_cone, closed=True, fc='white', ec=BK, lw=0.8))
    ax.add_patch(Circle((proj_cx + 0.35, proj_cy), 0.25, fc='none', ec=BK, lw=0.8))
    ax.add_patch(Circle((proj_cx + 0.35, proj_cy), 0.12, fc='none', ec=BK, lw=0.8))
    cad_line(ax, proj_cx - 0.85, proj_cy, proj_cx + 0.75, proj_cy, lw=0.5, ls='-.')
    cad_line(ax, proj_cx + 0.35, proj_cy - 0.35, proj_cx + 0.35, proj_cy + 0.35, lw=0.5, ls='-.')

def cad_draw_table(ax, x, y, headers, rows, col_widths, row_h=0.50, title=None, title_sz=7.5, sz=5.5):
    tbl_w = sum(col_widths)
    num_rows = len(rows)
    
    if title:
        cad_text(ax, x + tbl_w/2, y + (num_rows + 1) * row_h + 0.25, title, sz=title_sz, bold=True)
    
    # Header
    cur_x = x
    for h_txt, cw in zip(headers, col_widths):
        cad_rect(ax, cur_x, y + num_rows * row_h, cw, row_h, lw=1.1, fill=True)
        cad_text(ax, cur_x + cw/2, y + num_rows * row_h + row_h/2, h_txt, sz=sz+0.5, bold=True)
        cur_x += cw
        
    # Rows
    for r_idx, row in enumerate(rows):
        cur_x = x
        row_y = y + (num_rows - 1 - r_idx) * row_h
        for val, cw in zip(row, col_widths):
            cad_rect(ax, cur_x, row_y, cw, row_h, lw=0.8, fill=True)
            bold_val = ('N1' in str(val) or 'N2' in str(val) or 'N3' in str(val) or 'N4' in str(val) or
                        'CALCULATED' in str(val) or '0.75' in str(val) or '4500' in str(val) or '11.9' in str(val))
            cad_text(ax, cur_x + cw/2, row_y + row_h/2, str(val), sz=sz, bold=bold_val)
            cur_x += cw
