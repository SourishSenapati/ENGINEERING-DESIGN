"""
A4 OPTIMIZED: DWG-06 3D ISOMETRIC ASSEMBLY & EXPLODED INTERNALS CAD
PACKED-BED ABSORBER (C-101) — 750 mm ID x 4500 mm BED
STUDENT: SOURISH SENAPATI | ROLL NO.: 002310301035 | DATE: 29/09/2026
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
    cad_dim_h, cad_dim_v, cad_dim_leader, cad_balloon, cad_flange,
    cad_hatch_rect, cad_draw_table_a4, W, H, BK, GREY
)

def draw_iso_ellipse(ax, cx, cy, rx, ry, fill=True, fc='white', ec=BK, lw=0.8, ls='-', zorder=3):
    ell = Ellipse((cx, cy), rx * 2, ry * 2, fc=fc if fill else 'none', ec=ec, lw=lw, ls=ls, zorder=zorder)
    ax.add_patch(ell)

def draw_iso_cylinder(ax, cx, y_btm, y_top, rx, ry, fill=True, fc='white', ec=BK, lw=0.8, zorder=2):
    # Base ellipse (lower half)
    arc_b = Arc((cx, y_btm), rx * 2, ry * 2, theta1=180, theta2=360, color=ec, lw=lw, zorder=zorder+1)
    ax.add_patch(arc_b)
    # Side walls
    cad_line(ax, cx - rx, y_btm, cx - rx, y_top, lw=lw, color=ec, zorder=zorder+1)
    cad_line(ax, cx + rx, y_btm, cx + rx, y_top, lw=lw, color=ec, zorder=zorder+1)
    # Body fill if requested
    if fill:
        rect = Rectangle((cx - rx, y_btm), rx * 2, y_top - y_btm, fc=fc, ec='none', zorder=zorder)
        ax.add_patch(rect)
    # Top ellipse
    draw_iso_ellipse(ax, cx, y_top, rx, ry, fill=fill, fc=fc, ec=ec, lw=lw, zorder=zorder+2)

def generate_a4_dwg06(out_pdf, out_png):
    fig, ax = create_a4_canvas()
    draw_a4_border(ax)
    
    # ═════════════════════════════════════════════════════════════════════════
    # VIEW 1: 3D CUTAWAY ISOMETRIC GENERAL ARRANGEMENT (X = 0.8 to 11.2)
    # ═════════════════════════════════════════════════════════════════════════
    cad_rect(ax, 0.8, 3.4, 10.4, 16.8, lw=0.9, fill=True)
    cad_text(ax, 6.0, 19.85, 'VIEW 1 — 3D ISOMETRIC CUTAWAY GENERAL ARRANGEMENT', sz=5.5, bold=True)
    cad_text(ax, 6.0, 19.45, 'OVERALL MECHANICAL & CUTAWAY INTERNAL ARCHITECTURE — SCALE 1:35', sz=4.2, bold=True)
    
    CX1 = 5.8
    RX1 = 1.35   # Radius of shell (750 mm ID scaled)
    RY1 = 0.38   # Isometric perspective flattening
    
    # Vertical offset shift (-0.35 cm) to give generous breathing room at the top
    DY = -0.35
    
    # 1. Foundation Pier & Base Ring (Y = 3.6 to 4.7)
    p_pier = [(CX1 - 2.2, 3.6), (CX1 + 2.2, 3.6), (CX1 + 2.2, 3.95 + DY), (CX1 - 2.2, 3.95 + DY)]
    ax.add_patch(Polygon(p_pier, closed=True, fc='#F0F0F0', ec=BK, lw=0.85, zorder=2))
    cad_hatch_rect(ax, CX1 - 2.2, 3.6, 4.4, 0.35, pitch=0.15, angle=-45, lw=0.25)
    cad_text(ax, CX1, 3.75, 'REINFORCED CONCRETE PIER', sz=3.2, bold=True)
    
    # Base Ring (OD 1050 mm)
    draw_iso_cylinder(ax, CX1, 4.0 + DY, 4.15 + DY, 1.85, 0.45, fill=True, fc='white', lw=0.85)
    # Anchor Bolt Chairs
    for acx in [CX1 - 1.6, CX1 - 1.1, CX1 + 1.1, CX1 + 1.6]:
        cad_rect(ax, acx - 0.12, 4.15 + DY, 0.24, 0.35, lw=0.7, fill=True, zorder=4)
        cad_line(ax, acx, 4.0 + DY, acx, 4.65 + DY, lw=0.9, zorder=5) # Stud
    
    # 2. Cylindrical Skirt (Y = 4.15 to 6.2 + DY)
    draw_iso_cylinder(ax, CX1, 4.15 + DY, 6.2 + DY, RX1, RY1, fill=True, fc='white', lw=0.85)
    # Skirt Access Manway DN400
    draw_iso_ellipse(ax, CX1, 5.0 + DY, 0.40, 0.40, fill=True, fc='white', lw=0.75, zorder=4)
    cad_text(ax, CX1, 5.0 + DY, 'ACCESS\nDN400', sz=2.8, bold=True, zorder=5)
    # Skirt Gas Vents
    cad_circle(ax, CX1 - 1.0, 5.8 + DY, 0.08, fill=True, fc='white', lw=0.6, zorder=4)
    cad_circle(ax, CX1 + 1.0, 5.8 + DY, 0.08, fill=True, fc='white', lw=0.6, zorder=4)
    
    # 3. Bottom Dished Head (Y = 6.0 to 6.5 + DY)
    arc_head_b = Arc((CX1, 6.4 + DY), RX1 * 2, RY1 * 2.8, theta1=180, theta2=360, color=BK, lw=0.95, zorder=4)
    ax.add_patch(arc_head_b)
    # Bottom Drain N5
    cad_rect(ax, CX1 - 0.10, 5.5 + DY, 0.20, 0.60, lw=0.7, fill=True, zorder=3)
    cad_flange(ax, CX1, 5.5 + DY, orientation='V', length=0.45, thickness=0.08)
    cad_text(ax, CX1 + 0.65, 5.5 + DY, 'N5: DRAIN', sz=3.0, bold=True)
    
    # 4. Main Pressure Shell with Right-Half Cutaway (Y = 6.4 to 17.5 + DY)
    # Left Half: Solid Outer Shell Plate
    p_lshell = [(CX1 - RX1, 6.4 + DY), (CX1, 6.4 + DY), (CX1, 17.5 + DY), (CX1 - RX1, 17.5 + DY)]
    ax.add_patch(Polygon(p_lshell, closed=True, fc='#FAFAFA', ec=BK, lw=0.95, zorder=3))
    
    # Right Half: CUTAWAY INTERNALS EXPOSED
    p_rcut = [(CX1, 6.4 + DY), (CX1 + RX1, 6.4 + DY), (CX1 + RX1, 17.5 + DY), (CX1, 17.5 + DY)]
    ax.add_patch(Polygon(p_rcut, closed=True, fc='#FFFFFF', ec=BK, lw=0.95, zorder=3))
    cad_line(ax, CX1, 6.4 + DY, CX1, 17.5 + DY, lw=1.1, color=BK, zorder=6)
    
    # ── CUTAWAY INTERNAL HARDWARE ──
    # A. Rich Liquor Sump & Gas Inlet Deflector
    p_liq = [(CX1, 6.4 + DY), (CX1 + RX1, 6.4 + DY), (CX1 + RX1, 7.1 + DY), (CX1, 7.1 + DY)]
    ax.add_patch(Polygon(p_liq, closed=True, fc='#E0EEF8', ec=BK, lw=0.6, zorder=4))
    cad_text(ax, CX1 + 0.68, 6.75 + DY, 'LIQUID SUMP', sz=2.8, bold=True, zorder=5)
    
    # Gas Inlet Nozzle N1 entering from left
    cad_rect(ax, CX1 - RX1 - 0.85, 7.4 + DY, 0.85, 0.45, lw=0.8, fill=True, zorder=5)
    cad_flange(ax, CX1 - RX1 - 0.85, 7.62 + DY, orientation='H', length=0.65)
    cad_text(ax, CX1 - RX1 - 1.2, 8.0 + DY, 'N1: FEED GAS\n(DN150)', sz=3.0, bold=True)
    # 60° Titanium Deflector Cone
    p_cone = [(CX1 - 0.2, 7.8 + DY), (CX1 + 1.1, 7.8 + DY), (CX1 + 0.45, 8.25 + DY)]
    ax.add_patch(Polygon(p_cone, closed=True, fc='#D8D8D8', ec=BK, lw=0.8, zorder=5))
    cad_text(ax, CX1 + 0.65, 8.05 + DY, 'DEFLECTOR', sz=2.7, bold=True, zorder=6)
    
    # B. Gas-Injection Support Grid & Central Beam
    cad_rect(ax, CX1, 8.5 + DY, RX1, 0.25, lw=0.8, fill=True, fc='#C8C8C8', zorder=5)
    for ch_x in np.linspace(CX1 + 0.2, CX1 + RX1 - 0.25, 4):
        cad_rect(ax, ch_x - 0.10, 8.75 + DY, 0.20, 0.45, lw=0.7, fill=True, fc='white', zorder=5)
        cad_line(ax, ch_x, 8.85 + DY, ch_x, 9.15 + DY, lw=0.5, zorder=6)
    cad_line(ax, CX1, 8.75 + DY, CX1 + RX1, 8.75 + DY, lw=0.8, zorder=5)
    cad_text(ax, CX1 + 0.68, 9.35 + DY, 'SUPPORT GRID', sz=2.8, bold=True, zorder=6)
    
    # C. Packed Bed (Z = 4500 mm scaled)
    p_bed = [(CX1, 9.4 + DY), (CX1 + RX1, 9.4 + DY), (CX1 + RX1, 14.8 + DY), (CX1, 14.8 + DY)]
    ax.add_patch(Polygon(p_bed, closed=True, fc='#F9F9F0', ec=BK, lw=0.8, zorder=4))
    np.random.seed(42)
    for py in np.linspace(9.6 + DY, 14.6 + DY, 14):
        for px in np.linspace(CX1 + 0.2, CX1 + RX1 - 0.2, 5):
            ox = px + np.random.uniform(-0.06, 0.06)
            oy = py + np.random.uniform(-0.06, 0.06)
            draw_iso_ellipse(ax, ox, oy, 0.08, 0.05, fill=True, fc='white', lw=0.5, zorder=5)
    # Prominent packing bed label placed in clear white zone at Y = 13.0
    cad_text(ax, CX1 + 0.68, 12.8 + DY, 'PACKED BED\nZ = 4500 mm\n25 mm RINGS', sz=3.2, bold=True, bg='white', zorder=6)
    
    # D. Liquid Redistributor / Wall Wiper Ring
    cad_line(ax, CX1 + RX1 - 0.35, 12.0 + DY, CX1 + RX1, 11.85 + DY, lw=0.9, zorder=6)
    
    # E. Liquid Spray Distributor
    cad_rect(ax, CX1, 15.4 + DY, RX1, 0.18, lw=0.75, fill=True, fc='#D0D0D0', zorder=5)
    for sp_x in [CX1 + 0.35, CX1 + 0.85]:
        p_sp = [(sp_x, 15.4 + DY), (sp_x - 0.22, 14.9 + DY), (sp_x + 0.22, 14.9 + DY)]
        ax.add_patch(Polygon(p_sp, closed=True, fc='#EAF4FD', ec=BK, lw=0.5, ls='--', zorder=5))
    cad_text(ax, CX1 + 0.68, 15.7 + DY, 'DISTRIBUTOR', sz=2.8, bold=True, zorder=6)
    
    # Water Feed Inlet Nozzle N3 entering from right
    cad_rect(ax, CX1 + RX1, 15.4 + DY, 0.75, 0.32, lw=0.8, fill=True, zorder=5)
    cad_flange(ax, CX1 + RX1 + 0.75, 15.56 + DY, orientation='H', length=0.55)
    cad_text(ax, CX1 + RX1 + 0.95, 15.9 + DY, 'N3: WATER IN', sz=3.0, bold=True)
    
    # F. Knitted Wire Mesh Demister
    cad_rect(ax, CX1, 16.2 + DY, RX1, 0.55, lw=0.8, fill=True, fc='#E8E8E8', zorder=5)
    cad_hatch_rect(ax, CX1, 16.2 + DY, RX1, 0.55, pitch=0.10, angle=45, lw=0.25)
    cad_hatch_rect(ax, CX1, 16.2 + DY, RX1, 0.55, pitch=0.10, angle=-45, lw=0.25)
    cad_text(ax, CX1 + 0.68, 16.5 + DY, 'DEMISTER\n150 mm', sz=2.8, bold=True, bg='white', zorder=6)
    
    # 5. Top Dished Head & Vent Nozzle N6
    arc_head_t = Arc((CX1, 17.5 + DY), RX1 * 2, RY1 * 2.8, theta1=0, theta2=180, color=BK, lw=0.95, zorder=4)
    ax.add_patch(arc_head_t)
    cad_rect(ax, CX1 - 0.15, 18.2 + DY, 0.30, 0.65, lw=0.8, fill=True, zorder=4)
    cad_flange(ax, CX1, 18.85 + DY, orientation='V', length=0.60, thickness=0.09)
    cad_text(ax, CX1, 19.18 + DY, 'N6: TREATED GAS VENT', sz=3.1, bold=True)
    
    # Top Lifting Lugs (2 places at 180 DEG)
    for lx in [CX1 - 0.9, CX1 + 0.9]:
        cad_rect(ax, lx - 0.08, 18.0 + DY, 0.16, 0.32, lw=0.75, fill=True, zorder=5)
        cad_circle(ax, lx, 18.22 + DY, 0.04, fill=True, fc='white', lw=0.5, zorder=6)
    
    # 6. External Manways, Platforms & Ladder
    # Lower Manway M1 (DN450)
    cad_rect(ax, CX1 - RX1 - 0.55, 8.5 + DY, 0.55, 0.75, lw=0.8, fill=True, zorder=4)
    cad_rect(ax, CX1 - RX1 - 0.70, 8.4 + DY, 0.15, 0.95, lw=0.8, fill=True, zorder=4)
    cad_text(ax, CX1 - RX1 - 1.25, 8.85 + DY, 'M1 MANWAY\n(DN450)', sz=3.0, bold=True)
    
    # Upper Manway M2 (DN450)
    cad_rect(ax, CX1 - RX1 - 0.55, 15.9 + DY, 0.55, 0.75, lw=0.8, fill=True, zorder=4)
    cad_rect(ax, CX1 - RX1 - 0.70, 15.8 + DY, 0.15, 0.95, lw=0.8, fill=True, zorder=4)
    cad_text(ax, CX1 - RX1 - 1.25, 16.25 + DY, 'M2 MANWAY\n(DN450)', sz=3.0, bold=True)
    
    # Circular Platform 1 (EL +4.2 m) at Y = 10.4
    draw_iso_ellipse(ax, CX1 - 0.15, 10.4 + DY, RX1 + 0.85, RY1 + 0.20, fill=False, lw=0.85, zorder=5)
    draw_iso_ellipse(ax, CX1 - 0.15, 11.0 + DY, RX1 + 0.85, RY1 + 0.20, fill=False, lw=0.6, zorder=5)
    cad_line(ax, CX1 - RX1 - 0.85, 10.4 + DY, CX1 - RX1 - 0.85, 11.0 + DY, lw=0.6, zorder=5)
    cad_text(ax, CX1 - RX1 - 1.2, 10.7 + DY, 'PLATFORM 1\n(EL +4.2 m)', sz=3.0, bold=True)
    
    # Circular Platform 2 (EL +7.5 m) at Y = 17.2
    draw_iso_ellipse(ax, CX1 - 0.15, 17.2 + DY, RX1 + 0.85, RY1 + 0.20, fill=False, lw=0.85, zorder=5)
    draw_iso_ellipse(ax, CX1 - 0.15, 17.8 + DY, RX1 + 0.85, RY1 + 0.20, fill=False, lw=0.6, zorder=5)
    cad_text(ax, CX1 - RX1 - 1.2, 17.5 + DY, 'PLATFORM 2\n(EL +7.5 m)', sz=3.0, bold=True)
    
    # Caged Safety Ladder on left
    lad_x = CX1 - RX1 - 0.35
    cad_line(ax, lad_x, 4.2 + DY, lad_x, 17.8 + DY, lw=0.75, zorder=5)
    cad_line(ax, lad_x - 0.25, 4.2 + DY, lad_x - 0.25, 17.8 + DY, lw=0.75, zorder=5)
    for ry in np.linspace(4.4 + DY, 17.6 + DY, 26):
        cad_line(ax, lad_x - 0.25, ry, lad_x, ry, lw=0.45, zorder=5)
    
    # ═════════════════════════════════════════════════════════════════════════
    # VIEW 2: 3D EXPLODED INTERNALS ASSEMBLY (X = 11.6 to 19.6)
    # ═════════════════════════════════════════════════════════════════════════
    cad_rect(ax, 11.6, 3.4, 8.0, 16.8, lw=0.9, fill=True)
    cad_text(ax, 15.6, 19.85, 'VIEW 2 — 3D EXPLODED INTERNALS STACK', sz=5.5, bold=True)
    cad_text(ax, 15.6, 19.45, 'VERTICAL COMPONENT ORDER & ALIGNMENT — SCALE 1:25', sz=4.2, bold=True)
    
    CX2 = 15.5
    RX2 = 1.15
    RY2 = 0.30
    
    # Vertical Central Assembly Trajectory Axis
    cad_line(ax, CX2, 4.0, CX2, 18.8, lw=0.5, ls='-.', color=GREY, zorder=1)
    
    # ── ITEM 01: MIST DEMISTER PAD (Y = 17.3 to 18.0) ──
    cad_text(ax, CX2, 18.35, '01: KNITTED WIRE MESH DEMISTER (150 mm)', sz=3.2, bold=True)
    draw_iso_cylinder(ax, CX2, 17.3, 17.8, RX2, RY2, fill=True, fc='#EAEAEA', lw=0.8)
    cad_hatch_rect(ax, CX2 - RX2, 17.3, 2 * RX2, 0.50, pitch=0.10, angle=45, lw=0.25)
    cad_balloon(ax, CX2 + 1.85, 17.55, '01', radius=0.26, sz=4.5)
    cad_line(ax, CX2 + RX2, 17.55, CX2 + 1.59, 17.55, lw=0.5)
    cad_arrow(ax, CX2, 17.05, CX2, 17.25, lw=0.6, head_scale=4)
    
    # ── ITEM 02: LIQUID SPRAY DISTRIBUTOR (Y = 15.0 to 15.8) ──
    cad_text(ax, CX2, 16.05, '02: HEADER-LATERAL SPRAY DISTRIBUTOR', sz=3.2, bold=True)
    cad_rect(ax, CX2 - 0.25, 15.2, 0.50, 0.40, lw=0.8, fill=True, fc='#D8D8D8')
    cad_rect(ax, CX2 - RX2 + 0.1, 15.3, 2 * RX2 - 0.2, 0.15, lw=0.75, fill=True, fc='#D8D8D8')
    for nx in np.linspace(CX2 - RX2 + 0.3, CX2 + RX2 - 0.3, 5):
        cad_line(ax, nx, 15.3, nx, 15.05, lw=0.7)
        cad_circle(ax, nx, 15.02, 0.04, fill=True)
    cad_balloon(ax, CX2 + 1.85, 15.35, '02', radius=0.26, sz=4.5)
    cad_line(ax, CX2 + RX2, 15.35, CX2 + 1.59, 15.35, lw=0.5)
    cad_arrow(ax, CX2, 14.75, CX2, 14.95, lw=0.6, head_scale=4)
    
    # ── ITEM 03: BED HOLD-DOWN GRID (Y = 13.1 to 13.7) ──
    cad_text(ax, CX2, 13.95, '03: BED HOLD-DOWN GRID (ANTI-FLUIDIZATION)', sz=3.1, bold=True)
    draw_iso_cylinder(ax, CX2, 13.1, 13.3, RX2, RY2, fill=True, fc='#F0F0F0', lw=0.75)
    for mx in np.linspace(CX2 - RX2 + 0.3, CX2 + RX2 - 0.3, 5):
        cad_line(ax, mx, 13.1, mx, 13.3, lw=0.5)
    cad_balloon(ax, CX2 + 1.85, 13.20, '03', radius=0.26, sz=4.5)
    cad_line(ax, CX2 + RX2, 13.20, CX2 + 1.59, 13.20, lw=0.5)
    cad_arrow(ax, CX2, 12.85, CX2, 13.05, lw=0.6, head_scale=4)
    
    # ── ITEM 04: CERAMIC RASCHIG PACKING BED (Y = 9.2 to 11.6) ──
    cad_text(ax, CX2, 12.15, '04: 25-mm CERAMIC RASCHIG BED (Z = 4500 mm)', sz=3.2, bold=True)
    draw_iso_cylinder(ax, CX2, 9.2, 11.5, RX2, RY2, fill=True, fc='#FAF8F0', lw=0.85)
    for py in np.linspace(9.4, 11.3, 8):
        for px in np.linspace(CX2 - RX2 + 0.3, CX2 + RX2 - 0.3, 4):
            draw_iso_ellipse(ax, px, py, 0.08, 0.05, fill=True, fc='white', lw=0.45)
    cad_balloon(ax, CX2 + 1.85, 10.35, '04', radius=0.26, sz=4.5)
    cad_line(ax, CX2 + RX2, 10.35, CX2 + 1.59, 10.35, lw=0.5)
    cad_text(ax, CX2, 10.35, 'ACTIVE BED\nVp = 1.79 m3\n11.9 kN (1.22 t)', sz=3.0, bold=True, bg='white')
    cad_arrow(ax, CX2, 8.85, CX2, 9.15, lw=0.6, head_scale=4)
    
    # ── ITEM 05: GAS-INJECTION SUPPORT GRID ASSEMBLY (Y = 6.6 to 7.8) ──
    cad_text(ax, CX2, 8.15, '05: GAS-INJECTION SUPPORT GRID (>85% FREE)', sz=3.1, bold=True)
    cad_rect(ax, CX2 - RX2, 6.75, 2 * RX2, 0.18, lw=0.8, fill=True, fc='#D0D0D0')
    draw_iso_cylinder(ax, CX2, 6.95, 7.50, RX2, RY2, fill=True, fc='white', lw=0.8)
    for cx in np.linspace(CX2 - RX2 + 0.3, CX2 + RX2 - 0.3, 6):
        cad_line(ax, cx, 7.05, cx, 7.45, lw=0.5)
    cad_balloon(ax, CX2 + 1.85, 7.25, '05', radius=0.26, sz=4.5)
    cad_line(ax, CX2 + RX2, 7.25, CX2 + 1.59, 7.25, lw=0.5)
    cad_arrow(ax, CX2, 6.40, CX2, 6.65, lw=0.6, head_scale=4)
    
    # ── ITEM 06: GAS INLET DEFLECTOR CONE (Y = 4.3 to 5.4) ──
    cad_text(ax, CX2, 5.75, '06: AERODYNAMIC INLET DEFLECTOR (60 DEG)', sz=3.1, bold=True)
    # 3D Isometric Cone: Elliptical base + vertex
    draw_iso_ellipse(ax, CX2, 4.5, 0.85, 0.22, fill=True, fc='#D0D0D0', ec=BK, lw=0.8, zorder=3)
    p_cone3 = [(CX2 - 0.85, 4.5), (CX2 + 0.85, 4.5), (CX2, 5.35)]
    ax.add_patch(Polygon(p_cone3, closed=True, fc='#E0E0E0', ec=BK, lw=0.85, zorder=4))
    cad_balloon(ax, CX2 + 1.85, 4.85, '06', radius=0.26, sz=4.5)
    cad_line(ax, CX2 + 0.85, 4.85, CX2 + 1.59, 4.85, lw=0.5)
    
    # ═════════════════════════════════════════════════════════════════════════
    # RIGHT SIDE: TABLES & ASSEMBLY NOTES (X = 20.0 to 28.9)
    # ═════════════════════════════════════════════════════════════════════════
    # Total available width = 28.9 - 20.0 = 8.9 cm EXACTLY
    
    # TABLE 1: 3D INTERNALS EXPLODED BILL OF MATERIALS (BOM)
    T1_X = 20.0
    T1_Y = 12.6
    t1_headers = ['TAG', 'COMPONENT NAME', 'MATERIAL / SPEC', 'QTY']
    t1_widths  = [1.1, 3.4, 3.2, 1.2]  # Sum = 8.9 cm
    t1_rows = [
        ['01', 'Mist Demister Pad',      'Knitted SS316L / PTFE', '1 SET'],
        ['02', 'Spray Distributor',      'SS316L Header-Lateral', '1 SET'],
        ['03', 'Hold-Down Retaining Grid','SS316L Heavy Mesh',    '1 SET'],
        ['04', 'Ceramic Raschig Bed',    'Glazed Porcelain 25 mm','1.79 m3'],
        ['05', 'Multi-Beam Support Grid','FRP / Ti Gr 2 Chimney', '1 SET'],
        ['06', 'Inlet Deflector Cone',   'Titanium Gr 2 (60 DEG)','1 PC'],
    ]
    cad_draw_table_a4(ax, T1_X, T1_Y, t1_headers, t1_rows, t1_widths, row_h=0.38,
                      title='TABLE 1 — 3D INTERNALS EXPLODED BOM', sz=4.2)
    
    # TABLE 2: EQUIPMENT OVERALL SPECIFICATION & WEIGHTS
    T2_X = 20.0
    T2_Y = 7.8
    t2_headers = ['PARAMETER', 'VALUE', 'REMARKS / BASIS']
    t2_widths  = [2.9, 2.5, 3.5]  # Sum = 8.9 cm
    t2_rows = [
        ['Vessel ID & Total Height', '750 mm x 9625 mm',  'T/T 7200 mm + Skirt 1800 mm'],
        ['Active Packed Bed Depth',  '4500 mm (1.79 m3)', '25-mm Ceramic Raschig Rings'],
        ['Dry Column Tare Weight',   '38.2 kN (3.90 t)',  'Vessel shell, skirt & internals'],
        ['Operating Service Weight', '42.4 kN (4.32 t)',  'Dry tare + operating liq holdup'],
        ['Flooded Upset Weight',     '68.5 kN (6.98 t)',  '100% water filled hydrostatic'],
        ['Foundation Anchorage',     '8x M24 SA-193 B7',  '950 mm Bolt Circle Diameter'],
    ]
    cad_draw_table_a4(ax, T2_X, T2_Y, t2_headers, t2_rows, t2_widths, row_h=0.38,
                      title='TABLE 2 — EQUIPMENT SPECIFICATION & WEIGHTS', sz=4.0)
    
    # ASSEMBLY & ERECTION SEQUENCE NOTES
    N_X = 20.0
    N_Y = 3.4
    W_N = 8.9
    H_N = 4.0
    cad_rect(ax, N_X, N_Y, W_N, H_N, lw=0.9, fill=True)
    cad_text(ax, N_X + W_N/2, N_Y + H_N - 0.28, 'INTERNAL ASSEMBLY & ERECTION SEQUENCE NOTES', sz=4.4, bold=True)
    cad_line(ax, N_X, N_Y + H_N - 0.52, N_X + W_N, N_Y + H_N - 0.52, lw=0.6)
    
    notes_dwg6 = [
        "1. ERECTION: RIG VESSEL VIA TOP LIFTING LUGS; POSITION ON CONCRETE PIER.",
        "   TORQUE 8x M24 ANCHOR BOLTS TO 450 N*m IN STAR PATTERN. POUR 25 mm GROUT.",
        "2. SUPPORT GRID: PASS 3 SEGMENTAL PANELS THROUGH M1 MANWAY. SEAT ON",
        "   50x15 mm LEDGE RING & ISMB 100 BEAM. SECURE WITH PERIMETER J-CLAMPS.",
        "3. PACKING CHARGING: FILL COLUMN WITH WATER TO DAMPEN IMPACT; DUMP",
        "   25-mm CERAMIC RASCHIG RINGS RANDOMLY UP TO Z = 4500 mm BED MARK.",
        "4. DISTRIBUTOR: INSTALL HEADER-LATERAL MATRIX; LEVEL WITHIN +/-1.0 mm.",
        "5. DEMISTER: INSTALL KNITTED SS316L/PTFE PAD; TORQUE M1 & M2 MANWAY BLINDS.",
    ]
    for idx, nl in enumerate(notes_dwg6):
        is_hdr = any(nl.startswith(k) for k in ["1.", "2.", "3.", "4.", "5."])
        cad_text(ax, N_X + 0.25, N_Y + H_N - 0.82 - idx * 0.43, nl, sz=3.4, ha='left', bold=is_hdr)
    
    # Title Block
    draw_a4_title_block(
        ax,
        dwg_title='PACKED-BED ABSORBER (C-101) — 3D ISOMETRIC ASSEMBLY & EXPLODED INTERNALS CAD',
        dwg_no='PEDD-PBA-06',
        scale='PICTORIAL 1:25, 1:35 METRIC'
    )
    
    fig.savefig(out_pdf, dpi=300, facecolor='white')
    fig.savefig(out_png, dpi=300, facecolor='white')
    plt.close(fig)
    print(f"SUCCESS: Clean A4 DWG-06 generated at {out_pdf}")

if __name__ == '__main__':
    out_dir = r'd:\GAMES\zercxes\CAD_Engineering_Drawings\Packed_Bed_Absorber_Drawings'
    os.makedirs(out_dir, exist_ok=True)
    p_pdf = os.path.join(out_dir, '06_Packed_Bed_Absorber_3D_Isometric_Assembly_CAD.pdf')
    p_png = os.path.join(out_dir, '06_Packed_Bed_Absorber_3D_Isometric_Assembly_CAD.png')
    generate_a4_dwg06(p_pdf, p_png)
