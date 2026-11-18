"""
A4 OPTIMIZED: DWG-06 ACETALDEHYDE DISTILLATION REBOILER, CONDENSER & 3D ISOMETRIC ASSEMBLY
ACETALDEHYDE DISTILLATION SYSTEM (C-301) — 12000 kg/h FEED (50 wt% AcH, 60% VAPOUR)
STUDENT: SOURISH SENAPATI | ROLL NO.: 002310301035 | DATE: 17/11/2026
SUBJECT: PROCESS EQUIPMENT DESIGN & DRAWING | JADAVPUR UNIVERSITY
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon, Arc, Ellipse
from cad_common_a4 import (
    create_a4_canvas, draw_a4_border, draw_a4_title_block,
    cad_line, cad_rect, cad_circle, cad_arc, cad_text, cad_arrow,
    cad_dim_h, cad_dim_v, cad_balloon, cad_flange,
    cad_hatch_rect, cad_draw_table_a4, W, H, BK, GREY
)

def generate_acetaldehyde_dwg06(out_pdf, out_png):
    fig, ax = create_a4_canvas()
    draw_a4_border(ax)
    
    # ── Institutional Title Block ──
    SUB_INFO = 'ACETALDEHYDE DISTILLATION (C-301)  |  12000 kg/h FEED (50 wt% AcH)  |  ID 2.00 m, R=3.89  |  ASME SEC VIII / TEMA'
    draw_a4_title_block(
        ax,
        dwg_title='REBOILER & CONDENSER DETAILS & 3D ISOMETRIC ASSEMBLY',
        dwg_no='JU/ChE/ED/DWG-06',
        scale='AS NOTED / PICTORIAL',
        date='17 / 11 / 2026',
        sub_info=SUB_INFO
    )
    
    # ── Drawing Header Banner ──
    cad_text(ax, W/2, H - 1.25, 'HEAT EXCHANGER FABRICATION DETAILS & 3D ISOMETRIC PLANT ASSEMBLY', sz=6.6, bold=True)
    cad_text(ax, W/2, H - 1.62, 'THERMOSIPHON REBOILER (TEMA BEM) | CONDENSER (TEMA AEL) | CONNECTED 3D CLOSED-LOOP PIPING', sz=4.8, bold=False)
    
    # ═════════════════════════════════════════════════════════════════════════
    # VIEW 1: VERTICAL THERMOSIPHON REBOILER E-302 (TEMA BEM) - TOP LEFT
    # Box: X = 0.8 to 10.4, Y = 11.4 to 18.9 (Height = 7.5 cm)
    # ═════════════════════════════════════════════════════════════════════════
    cad_rect(ax, 0.8, 11.4, 9.6, 7.5, lw=0.9, fill=True)
    RX1, RY1 = 5.6, 15.0
    cad_text(ax, 5.6, 18.60, 'VIEW 1: VERTICAL THERMOSIPHON REBOILER E-302 (TEMA BEM)', sz=5.0, bold=True)
    cad_text(ax, 5.6, 18.25, 'HEAT DUTY: 3912.45 kW | SHELL: 800 mm ID x 3000 mm TUBE L', sz=3.8, bold=True)
    
    # Shell Dimensions: 1.15 cm wide x 3.6 cm tall
    SW1, SH1 = 1.15, 3.40
    cad_rect(ax, RX1 - SW1/2, RY1 - SH1/2, SW1, SH1, lw=0.85, fill=True)
    # Tubesheets Top & Bottom
    cad_rect(ax, RX1 - SW1/2 - 0.14, RY1 + SH1/2, SW1 + 0.28, 0.12, lw=0.75, fill=True)
    cad_rect(ax, RX1 - SW1/2 - 0.14, RY1 - SH1/2 - 0.12, SW1 + 0.28, 0.12, lw=0.75, fill=True)
    # Channel Heads (Bonnet Type B)
    cad_arc(ax, RX1, RY1 + SH1/2 + 0.12, SW1, 0.50, theta1=0, theta2=180, lw=0.85)
    cad_arc(ax, RX1, RY1 - SH1/2 - 0.12, SW1, 0.50, theta1=180, theta2=360, lw=0.85)
    
    # Tube bundle vertical lines (schematic)
    for tx in np.linspace(RX1 - SW1/2 + 0.18, RX1 + SW1/2 - 0.18, 6):
        cad_line(ax, tx, RY1 - SH1/2, tx, RY1 + SH1/2, lw=0.35, ls='--')
        
    # Segmental Baffles (25% cut)
    for idx, by in enumerate(np.linspace(RY1 - SH1/2 + 0.55, RY1 + SH1/2 - 0.55, 5)):
        if idx % 2 == 0:
            cad_line(ax, RX1 - SW1/2, by, RX1 + SW1/2 - 0.28, by, lw=0.6)
        else:
            cad_line(ax, RX1 - SW1/2 + 0.28, by, RX1 + SW1/2, by, lw=0.6)
            
    # Steam Inlet Nozzle (Shell side top left) & Impingement Plate
    cad_rect(ax, RX1 - SW1/2 - 0.40, RY1 + SH1/2 - 0.55, 0.40, 0.20, lw=0.65, fill=True)
    cad_flange(ax, RX1 - SW1/2 - 0.40, RY1 + SH1/2 - 0.45, orientation='H', length=0.36)
    cad_line(ax, RX1 - SW1/2 + 0.12, RY1 + SH1/2 - 0.60, RX1 - SW1/2 + 0.12, RY1 + SH1/2 - 0.30, lw=0.80) # Impingement
    cad_text(ax, RX1 - SW1/2 - 0.48, RY1 + SH1/2 - 0.45, 'STEAM IN (DN200)\n1.5 bar(g)', sz=3.0, bold=True, ha='right')
    
    # Condensate Drain Nozzle (Shell side bottom left)
    cad_rect(ax, RX1 - SW1/2 - 0.40, RY1 - SH1/2 + 0.35, 0.40, 0.16, lw=0.65, fill=True)
    cad_flange(ax, RX1 - SW1/2 - 0.40, RY1 - SH1/2 + 0.43, orientation='H', length=0.30)
    cad_text(ax, RX1 - SW1/2 - 0.48, RY1 - SH1/2 + 0.43, 'CONDENSATE OUT\nDN80 TO TRAP', sz=3.0, bold=True, ha='right')
    
    # Sump Liquid Feed Nozzle (Bottom channel bonnet, connected to C-301 N5)
    cad_rect(ax, RX1 - 0.14, RY1 - SH1/2 - 0.48, 0.28, 0.36, lw=0.65, fill=True)
    cad_flange(ax, RX1, RY1 - SH1/2 - 0.48, orientation='V', length=0.44)
    cad_text(ax, RX1, RY1 - SH1/2 - 0.68, 'LIQUID IN (DN250)\nFROM COLUMN SUMP N5', sz=3.1, bold=True)
    
    # Vapor Return Nozzle (Top channel bonnet, connected to C-301 N4)
    cad_rect(ax, RX1 - 0.18, RY1 + SH1/2 + 0.12, 0.36, 0.36, lw=0.65, fill=True)
    cad_flange(ax, RX1, RY1 + SH1/2 + 0.48, orientation='V', length=0.52)
    cad_text(ax, RX1, RY1 + SH1/2 + 0.70, 'VAPOR OUT (DN400)\nTO COLUMN N4', sz=3.1, bold=True)
    
    # Mounting Support Lugs on Shell
    cad_line(ax, RX1 + SW1/2, RY1, RX1 + SW1/2 + 0.30, RY1 - 0.25, lw=0.8)
    cad_line(ax, RX1 + SW1/2, RY1 - 0.25, RX1 + SW1/2 + 0.30, RY1 - 0.25, lw=0.8)
    cad_text(ax, RX1 + SW1/2 + 0.38, RY1 - 0.12, 'SUPPORT LUG\n(4 PLACES)', sz=2.8, bold=False, ha='left')
    
    # Dimension Callouts for Reboiler
    cad_dim_v(ax, RX1 + SW1/2 + 1.8, RY1 - SH1/2, RY1 + SH1/2, '3000 TUBE L', sz=3.4, text_offset=0.20)
    cad_dim_h(ax, RX1 - SW1/2, RX1 + SW1/2, RY1 + SH1/2 + 0.95, 'ID 800', sz=3.4)

    # ═════════════════════════════════════════════════════════════════════════
    # VIEW 2: HORIZONTAL OVERHEAD CONDENSER E-303 (TEMA AEL) - BOTTOM LEFT
    # Box: X = 0.8 to 10.4, Y = 3.4 to 11.1 (Height = 7.7 cm)
    # ═════════════════════════════════════════════════════════════════════════
    cad_rect(ax, 0.8, 3.4, 9.6, 7.7, lw=0.9, fill=True)
    CX2, CY2 = 5.5, 7.10
    cad_text(ax, 5.6, 10.80, 'VIEW 2: HORIZONTAL CONDENSER E-303 (TEMA AEL)', sz=5.0, bold=True)
    cad_text(ax, 5.6, 10.45, 'HEAT DUTY: 4733.92 kW (CHW) | SHELL: 1000 mm ID x 4500 mm L', sz=3.8, bold=True)
    
    # Shell Dimensions: 4.5 cm long x 1.25 cm diameter
    CSW, CSH = 4.40, 1.20
    cad_rect(ax, CX2 - CSW/2, CY2 - CSH/2, CSW, CSH, lw=0.85, fill=True)
    # Tubesheets Left & Right
    cad_rect(ax, CX2 - CSW/2 - 0.14, CY2 - CSH/2 - 0.14, 0.14, CSH + 0.28, lw=0.75, fill=True)
    cad_rect(ax, CX2 + CSW/2, CY2 - CSH/2 - 0.14, 0.14, CSH + 0.28, lw=0.75, fill=True)
    # Channel Head (Left: Type A with pass partition)
    cad_rect(ax, CX2 - CSW/2 - 0.75, CY2 - CSH/2, 0.61, CSH, lw=0.85, fill=True)
    cad_line(ax, CX2 - CSW/2 - 0.75, CY2, CX2 - CSW/2 - 0.14, CY2, lw=0.80) # Pass partition
    # Bonnet Head (Right: Type L)
    cad_arc(ax, CX2 + CSW/2 + 0.14, CY2, 0.55, CSH, theta1=270, theta2=90, lw=0.85)
    
    # Tube bundle horizontal lines (schematic 2-pass)
    for ty in [CY2 - 0.42, CY2 - 0.20, CY2 + 0.20, CY2 + 0.42]:
        cad_line(ax, CX2 - CSW/2, ty, CX2 + CSW/2, ty, lw=0.35, ls='--')
        
    # Vapor Inlet Dome Nozzle (Top of shell, connected to Column N1)
    cad_rect(ax, CX2 - 0.65, CY2 + CSH/2, 0.45, 0.38, lw=0.65, fill=True)
    cad_flange(ax, CX2 - 0.425, CY2 + CSH/2 + 0.38, orientation='V', length=0.55)
    cad_text(ax, CX2 - 0.425, CY2 + CSH/2 + 0.60, 'VAPOR IN (DN350)\nFROM COLUMN TOP N1', sz=3.1, bold=True)
    
    # Impingement Baffle below vapor inlet
    cad_line(ax, CX2 - 0.75, CY2 + CSH/2 - 0.15, CX2 - 0.10, CY2 + CSH/2 - 0.15, lw=0.8)
    
    # Condensate Drain Nozzle (Bottom of shell, connected to Reflux Drum V-301)
    cad_rect(ax, CX2 + 0.75, CY2 - CSH/2 - 0.38, 0.26, 0.38, lw=0.65, fill=True)
    cad_flange(ax, CX2 + 0.88, CY2 - CSH/2 - 0.38, orientation='V', length=0.38)
    cad_text(ax, CX2 + 0.88, CY2 - CSH/2 - 0.60, 'CONDENSATE OUT (DN150)\nTO REFLUX DRUM V-301', sz=3.1, bold=True)
    
    # Cooling water inlet & outlet on channel head
    cad_text(ax, CX2 - CSW/2 - 0.85, CY2 - 0.32, 'CW IN (DN200)\n7.0 C', sz=3.0, bold=True, ha='right')
    cad_text(ax, CX2 - CSW/2 - 0.85, CY2 + 0.32, 'CW OUT (DN200)\n12.0 C', sz=3.0, bold=True, ha='right')
    
    # Saddle Supports (Left: Fixed, Right: Sliding)
    sad_w, sad_h = 0.35, 0.40
    for sx, stype in [(CX2 - 1.25, 'FIXED'), (CX2 + 1.25, 'SLIDING')]:
        cad_rect(ax, sx - sad_w/2, CY2 - CSH/2 - sad_h, sad_w, sad_h, lw=0.65, fill=True, fc='#EAEAEA')
        cad_line(ax, sx - sad_w/2 - 0.15, CY2 - CSH/2 - sad_h, sx + sad_w/2 + 0.15, CY2 - CSH/2 - sad_h, lw=0.9)
        cad_text(ax, sx, CY2 - CSH/2 - sad_h/2, stype[:3], sz=2.5, bold=True)
        
    # Dimension Callouts for Condenser
    cad_dim_h(ax, CX2 - CSW/2, CX2 + CSW/2, CY2 - CSH/2 - 0.85, '4500 TUBE LENGTH', sz=3.4)

    # ═════════════════════════════════════════════════════════════════════════
    # VIEW 3: 3D ISOMETRIC PLANT INTEGRATION & CONNECTED PIPING LAYOUT
    # Box: X = 10.7 to 19.5, Y = 3.4 to 18.9 (Width = 8.8 cm, Height = 15.5 cm)
    # ═════════════════════════════════════════════════════════════════════════
    cad_rect(ax, 10.7, 3.4, 8.8, 15.5, lw=0.9, fill=True)
    cad_text(ax, 15.1, 18.60, 'VIEW 3: 3D ISOMETRIC CONNECTED PLANT ASSEMBLY', sz=4.8, bold=True)
    cad_text(ax, 15.1, 18.25, 'AXONOMETRIC PERSPECTIVE — COMPLETE CLOSED-LOOP PIPING', sz=3.7, bold=True)
    
    IX0, IY0 = 13.8, 5.0
    ANG = np.radians(30)
    cos30 = np.cos(ANG)
    sin30 = np.sin(ANG)
    
    def to_iso(x, y, z):
        u = IX0 + (x - y) * cos30 * 0.58
        v = IY0 + (x + y) * sin30 * 0.58 + z * 0.62
        return u, v
    
    # 1. Reinforced Concrete Foundation Pad in Isometric
    p_fnd = [to_iso(-2.2, -2.0, 0), to_iso(4.2, -2.0, 0), to_iso(4.2, 3.5, 0), to_iso(-2.2, 3.5, 0)]
    ax.add_patch(Polygon(p_fnd, closed=True, fc='#f0f0f0', ec=BK, lw=0.8, zorder=2))
    
    # 2. Distillation Column C-301 in Isometric (Center at x=0, y=0)
    COL_R = 0.80
    u_c, v_c_bot = to_iso(0, 0, 0.5)
    _, v_c_top = to_iso(0, 0, 14.5)
    
    # Skirt and Column Outline
    cad_circle(ax, to_iso(0, 0, 0)[0], to_iso(0, 0, 0)[1], COL_R * 0.60, lw=0.85)
    cad_line(ax, u_c - COL_R, v_c_bot, u_c - COL_R, v_c_top, lw=1.1, zorder=4)
    cad_line(ax, u_c + COL_R, v_c_bot, u_c + COL_R, v_c_top, lw=1.1, zorder=4)
    ax.add_patch(Arc((u_c, v_c_top), 2*COL_R, COL_R * 0.6, theta1=0, theta2=360, ec=BK, lw=1.1, zorder=5))
    ax.add_patch(Arc((u_c, v_c_bot), 2*COL_R, COL_R * 0.6, theta1=180, theta2=360, ec=BK, lw=1.1, zorder=4))
    
    # Internal Trays indication
    for zi in np.linspace(2.2, 12.5, 12):
        ui, vi = to_iso(0, 0, zi)
        cad_line(ax, ui - COL_R*0.75, vi, ui + COL_R*0.75, vi, lw=0.40, color='#0044aa', zorder=3)
    cad_text(ax, u_c, v_c_top + 0.70, 'C-301 COLUMN\n(ID 2000 mm)', sz=3.8, bold=True)
    
    # Structural Platforms & Handrails
    for pl_z in [3.8, 8.5, 13.0]:
        up, vp = to_iso(0, 0, pl_z)
        cad_line(ax, up - 1.25, vp, up + 1.25, vp, lw=0.75, color='#444444', zorder=4)
        cad_line(ax, up - 1.25, vp + 0.35, up + 1.25, vp + 0.35, lw=0.45, color='#444444', zorder=4)
        
    # 3. Thermosiphon Reboiler E-302 in Isometric (at x= -1.8, y= 0.6)
    ur, vr_bot = to_iso(-1.8, 0.6, 1.0)
    _, vr_top = to_iso(-1.8, 0.6, 4.4)
    cad_rect(ax, ur - 0.32, vr_bot, 0.64, vr_top - vr_bot, lw=0.85, fill=True, fc='#FAF8F0', zorder=5)
    cad_text(ax, ur, vr_bot - 0.40, 'E-302 REBOILER\n(3912 kW)', sz=3.2, bold=True)
    
    # 4. Elevated Overhead Condenser E-303 (at x= 2.5, y= -0.6, z= 12.8)
    uc, vc = to_iso(2.6, -0.6, 12.8)
    cad_rect(ax, uc - 0.85, vc - 0.28, 1.70, 0.56, lw=0.85, fill=True, fc='#FAF8F0', zorder=5)
    cad_text(ax, uc, vc + 0.50, 'E-303 CONDENSER\n(4734 kW)', sz=3.2, bold=True)
    
    # 5. Reflux Drum V-301 (at x= 2.6, y= -0.6, z= 8.8)
    uv, vv = to_iso(2.6, -0.6, 8.8)
    cad_rect(ax, uv - 0.55, vv - 0.25, 1.10, 0.50, lw=0.85, fill=True, fc='#F0F8FF', zorder=5)
    cad_text(ax, uv, vv - 0.38, 'V-301 REFLUX DRUM', sz=3.0, bold=True)
    
    # 6. Reflux Pumps P-302A/B on Ground (at x= 2.2, y= 0.2, z= 0.6)
    upmp, vpmp = to_iso(2.2, 0.2, 0.6)
    cad_circle(ax, upmp, vpmp, 0.22, lw=0.75, fill=True, fc='#E0FFE0', zorder=5)
    cad_text(ax, upmp + 0.70, vpmp, 'P-302A/B', sz=3.0, bold=True)
    
    # ── FULLY CONNECTED 3D ISOMETRIC PIPING RUNS (STRICT ORTHOGONAL AXES — ZERO DISCONNECTIONS!) ──
    # Helper to draw a polyline in isometric space
    def draw_iso_pipe(pts, color, lw=1.2, arrow_idx=None, label=None, label_idx=None, label_offset=(0, 0.25)):
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
                cad_arrow(ax, mx - ux*0.18, my - uy*0.18, mx + ux*0.18, my + uy*0.18, lw=lw, color=color, head_scale=4.5)
        if label and label_idx is not None and label_idx < len(iso_pts) - 1:
            lx1, ly1 = iso_pts[label_idx]
            lx2, ly2 = iso_pts[label_idx + 1]
            mlx, mly = (lx1 + lx2)/2.0 + label_offset[0], (ly1 + ly2)/2.0 + label_offset[1]
            cad_text(ax, mlx, mly, label, sz=2.8, bold=True, color=color, bg='white')

    # A. Sump Liquid to Reboiler (Line L-305: Column Sump N5 -> Reboiler E-302 Bottom Channel)
    # Column N5: (x=-COL_R, y=0, z=0.8) -> (-1.8, 0, 0.8) -> (-1.8, 0.6, 0.8) -> into Reboiler bottom channel (-1.8, 0.6, 1.0)
    pts_l305 = [
        (-COL_R, 0.0, 0.8),
        (-1.8,   0.0, 0.8),
        (-1.8,   0.6, 0.8),
        (-1.8,   0.6, 1.0)
    ]
    draw_iso_pipe(pts_l305, color='#b71540', lw=1.3, arrow_idx=0, label='L-305 (DN250)', label_idx=0, label_offset=(0, 0.22))

    # B. Vapor Return to Column (Line L-306: Reboiler E-302 Top Channel -> Column N4)
    # Reboiler top channel: (-1.8, 0.6, 4.4) -> (-1.8, 0.0, 4.4) -> (-COL_R, 0.0, 4.4) into column N4
    pts_l306 = [
        (-1.8,   0.6, 4.4),
        (-1.8,   0.0, 4.4),
        (-COL_R, 0.0, 4.4)
    ]
    draw_iso_pipe(pts_l306, color='#b71540', lw=1.4, arrow_idx=1, label='L-306 (DN400)', label_idx=1, label_offset=(0, 0.25))

    # C. Overhead Vapor Line (Line L-301: Column Top N1 -> Condenser E-303 Top Shell Dome)
    # Column top nozzle N1: (0, 0, 14.8) -> vertical rise to (0, 0, 16.0) -> east to (2.6, 0, 16.0) -> north to (2.6, -0.6, 16.0) -> drop into Condenser (2.6, -0.6, 13.2)
    pts_l301 = [
        (0.0,  0.0, 14.8),
        (0.0,  0.0, 15.9),
        (2.6,  0.0, 15.9),
        (2.6, -0.6, 15.9),
        (2.6, -0.6, 13.1)
    ]
    draw_iso_pipe(pts_l301, color='#0c2461', lw=1.4, arrow_idx=2, label='L-301 (DN350)', label_idx=2, label_offset=(0.2, 0.25))

    # D. Condensate Drain Line (Line L-302: Condenser E-303 Bottom Drain -> Reflux Drum V-301)
    # Condenser drain: (2.6, -0.6, 12.5) -> drop vertically into Reflux Drum top (2.6, -0.6, 9.1)
    pts_l302 = [
        (2.6, -0.6, 12.5),
        (2.6, -0.6,  9.1)
    ]
    draw_iso_pipe(pts_l302, color='#079992', lw=1.2, arrow_idx=0, label='L-302 (DN150)', label_idx=0, label_offset=(0.55, 0.0))

    # E. Drum to Pump Suction (Reflux Drum V-301 Bottom Drain -> Pump P-302A/B)
    # Drum bottom: (2.6, -0.6, 8.5) -> drop vertically to (2.6, -0.6, 0.6) -> turn east to (2.6, 0.2, 0.6) -> into pump (2.2, 0.2, 0.6)
    pts_drum_pmp = [
        (2.6, -0.6, 8.5),
        (2.6, -0.6, 0.6),
        (2.6,  0.2, 0.6),
        (2.35, 0.2, 0.6)
    ]
    draw_iso_pipe(pts_drum_pmp, color='#079992', lw=1.1, arrow_idx=1)

    # F. Reflux Return Line (Line L-303: Pump Discharge -> Column Top Tray N2)
    # Pump discharge: (2.05, 0.2, 0.6) -> rise vertically to (2.05, 0.2, 13.0) -> turn west to (COL_R, 0.2, 13.0) -> into column (COL_R, 0.0, 13.0)
    pts_l303 = [
        (2.05,  0.2,  0.6),
        (2.05,  0.2, 13.0),
        (COL_R, 0.2, 13.0),
        (COL_R, 0.0, 13.0)
    ]
    draw_iso_pipe(pts_l303, color='#079992', lw=1.2, arrow_idx=1, label='L-303 (DN150) REFLUX', label_idx=1, label_offset=(0.75, 0.0))

    # G. Distillate Product Take-Off (Line L-304: Branch from L-303 to Storage)
    pts_l304 = [
        (2.05, 0.2, 2.5),
        (3.8,  0.2, 2.5),
        (3.8, -1.5, 2.5)
    ]
    draw_iso_pipe(pts_l304, color='#38ada9', lw=1.1, arrow_idx=1, label='L-304 DISTILLATE', label_idx=1, label_offset=(0, 0.22))

    # H. Bottoms Product Draw (Line L-307: Column Bottom Sump N6 -> Battery Limit)
    pts_l307 = [
        (0.0,  0.0,  0.5),
        (0.0,  0.0, -0.2),
        (0.0, -1.8, -0.2),
        (3.5, -1.8, -0.2)
    ]
    draw_iso_pipe(pts_l307, color='#e58e26', lw=1.2, arrow_idx=2, label='L-307 (DN100) BOTTOMS', label_idx=2, label_offset=(0, 0.22))

    # ═════════════════════════════════════════════════════════════════════════
    # RIGHT SIDE: HEAT EXCHANGER TABLES & PIPING SCHEDULE (X = 19.8 to 28.9, W = 9.1 cm)
    # ═════════════════════════════════════════════════════════════════════════
    TX_BASE = 19.8
    
    # TABLE 1: Heat Exchanger Thermal & Mechanical Data Table
    t1_headers = ['SPECIFICATION', 'REBOILER (E-302)', 'CONDENSER (E-303)']
    t1_rows = [
        ['TEMA Classification', 'BEM (Fixed Tubesheet)', 'AEL (Removable Bundle)'],
        ['Heat Duty', '3912.45 kW (3.91 MW)', '4733.92 kW (4.73 MW)'],
        ['Heat Transfer Area', '165.0 m2', '245.0 m2'],
        ['Shell Diameter (ID)', '800 mm', '1000 mm'],
        ['Tube Length', '3000 mm (Vertical)', '4500 mm (Horizontal)'],
        ['Tube OD x Thickness', '25.4 mm (1") x 2.1 mm', '19.05 mm (3/4") x 1.65 mm'],
        ['Tube Pitch & Layout', '31.75 mm Triangular (30 deg)', '25.4 mm Triangular (30 deg)'],
        ['Tube Count / Passes', '280 Tubes / 1 Pass', '420 Tubes / 2 Passes'],
        ['Shell / Tube Material', 'SA-516 Gr 70 / 304L SS', 'SA-516 Gr 70 / 304L SS'],
        ['Design Press. (Shell/Tube)', '0.50 / 0.35 MPa(g)', '0.35 / 0.60 MPa(g)'],
        ['Design Temp. (Shell/Tube)', '160 C / 120 C', '110 C / 65 C'],
    ]
    t1_col_w = [3.5, 2.8, 2.8] # sum = 9.1 cm
    cad_draw_table_a4(ax, TX_BASE, 11.20, t1_headers, t1_rows, t1_col_w,
                      row_h=0.33, title='TABLE 1: HEAT EXCHANGER TEMA MECHANICAL & THERMAL DATA',
                      title_sz=4.3, sz=3.6)
    
    # TABLE 2: Connected Piping Line Schedule
    t2_headers = ['LINE NO', 'SIZE / RATING', 'FROM -> TO', 'SERVICE']
    t2_rows = [
        ['L-301', '14" DN350 CL150', 'C-301 (N1) -> E-303', 'Overhead Vapour'],
        ['L-302', '6" DN150 CL150',  'E-303 -> V-301',     'Condensed Reflux'],
        ['L-303', '6" DN150 CL150',  'P-302 -> C-301 (N2)', 'Liquid Reflux Return'],
        ['L-304', '4" DN100 CL150',  'P-302 -> Storage',   'Distillate Product D'],
        ['L-305', '10" DN250 CL150', 'C-301 (N5) -> E-302', 'Bottoms Liquid Draw'],
        ['L-306', '16" DN400 CL150', 'E-302 -> C-301 (N4)', 'Reboiler Vapour Return'],
        ['L-307', '4" DN100 CL150',  'C-301 (N6) -> E-305', 'Bottoms Product W'],
    ]
    t2_col_w = [1.8, 2.3, 2.6, 2.4] # sum = 9.1 cm
    cad_draw_table_a4(ax, TX_BASE, 6.70, t2_headers, t2_rows, t2_col_w,
                      row_h=0.33, title='TABLE 2: CLOSED-LOOP CONNECTED PIPING SCHEDULE',
                      title_sz=4.3, sz=3.6)
    
    # ASSEMBLY & PIPING ERECTION NOTES BOX
    N_X = 19.8
    N_Y = 3.4
    W_N = 9.1
    H_N = 2.85
    cad_rect(ax, N_X, N_Y, W_N, H_N, lw=0.9, fill=True)
    cad_text(ax, N_X + W_N/2, N_Y + H_N - 0.26, 'PIPING INTEGRATION & ERECTION ENGINEERING NOTES', sz=4.2, bold=True)
    cad_line(ax, N_X, N_Y + H_N - 0.48, N_X + W_N, N_Y + H_N - 0.48, lw=0.6)
    
    pnotes = [
        "1. THERMOSIPHON LOOP: REBOILER E-302 RUNS VIA NATURAL DENSITY CIRCULATION.",
        "   LIQUID DRAW L-305 AND VAPOR RETURN L-306 SLOPED >= 1:50; NO POCKETS.",
        "2. CONDENSER ELEVATION: E-303 MOUNTED ON STRUCTURAL STEEL (EL +12.8 m)",
        "   TO PROVIDE GRAVITY DRAINAGE L-302 INTO REFLUX DRUM V-301.",
        "3. EXPANSION: ALL PIPING DESIGNED PER ASME B31.3 WITH 3D EXPANSION LOOPS.",
        "4. HYDROTEST: COMPLETE LOOP HYDROTESTED AT 1.5x DESIGN PRESSURE (0.525 MPa).",
    ]
    for idx, nl in enumerate(pnotes):
        cad_text(ax, N_X + 0.22, N_Y + H_N - 0.76 - idx * 0.34, nl, sz=3.1, ha='left')
    
    fig.savefig(out_pdf, dpi=300, facecolor='white')
    fig.savefig(out_png, dpi=300, facecolor='white')
    plt.close(fig)
    print(f"SUCCESS: Clean A4 DWG-06 generated at {out_pdf}")

if __name__ == '__main__':
    out_dir = r"d:\GAMES\zercxes\CAD_Engineering_Drawings\Acetaldehyde_PropyleneOxide_Distillation_Drawings"
    os.makedirs(out_dir, exist_ok=True)
    pdf = os.path.join(out_dir, "06_Acetaldehyde_Distillation_Reboiler_Condenser_3D_Isometric_CAD.pdf")
    png = os.path.join(out_dir, "06_Acetaldehyde_Distillation_Reboiler_Condenser_3D_Isometric_CAD.png")
    generate_acetaldehyde_dwg06(pdf, png)
