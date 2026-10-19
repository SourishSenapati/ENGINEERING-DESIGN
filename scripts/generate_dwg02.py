"""
DWG-02: INTERNAL ASSEMBLY & PROCESS INTERNALS DETAILED CAD
PACKED-BED ABSORBER (C-101) — 750 MM ID x 4500 MM RASCHIG RING BED
STUDENT: SOURISH SENAPATI | ROLL: 002310301035 | DATE: 29/09/2026
SUBJECT: PROCESS EQUIPMENT DESIGN & DRAWING | JADAVPUR UNIVERSITY
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon, Arc, Wedge
from cad_common import (
    create_cad_canvas, draw_sheet_border, draw_title_block,
    cad_line, cad_rect, cad_circle, cad_arc, cad_text, cad_arrow,
    cad_dim_h, cad_dim_v, cad_dim_leader, cad_balloon, cad_flange,
    cad_hatch_rect, cad_draw_table, W, H, BK, GREY
)

def generate_dwg02():
    fig, ax = create_cad_canvas()
    draw_sheet_border(ax)
    
    # ═════════════════════════════════════════════════════════════════════════
    # SHEET LAYOUT: 4 LARGE ENLARGED CAD DETAILS
    # Detail A: Liquid Distributor Assembly (Top-Left: X = 2.5 to 26.0, Y = 28.5 to 52.0)
    # Detail B: Mist Eliminator (Demister) (Top-Right: X = 28.0 to 51.5, Y = 28.5 to 52.0)
    # Detail C: Raschig Ring Geometry & Bed Detail (Btm-Left: X = 2.5 to 26.0, Y = 7.2 to 27.0)
    # Detail D: Gas Inlet & Deflector Assembly (Btm-Right: X = 28.0 to 51.5, Y = 7.2 to 27.0)
    # Right Panel: Tables & Engineering Notes (X = 53.0 to 81.5, Y = 7.2 to 52.0)
    # ═════════════════════════════════════════════════════════════════════════
    
    # ─────────────────────────────────────────────────────────────────────────
    # DETAIL A: LIQUID DISTRIBUTOR (HEADER & LATERAL PIPE TYPE)
    # ─────────────────────────────────────────────────────────────────────────
    DA_X, DA_Y, DA_W, DA_H = 2.5, 29.0, 24.5, 23.5
    cad_rect(ax, DA_X, DA_Y, DA_W, DA_H, lw=1.2, fill=True)
    cad_text(ax, DA_X + DA_W/2, DA_Y + DA_H - 0.7,
             'DETAIL A — HEADER-AND-LATERAL LIQUID DISTRIBUTOR', sz=7.8, bold=True)
    cad_text(ax, DA_X + DA_W/2, DA_Y + DA_H - 1.4,
             'SECTIONAL ELEVATION & PLAN VIEW (SCALE 1:10 METRIC)', sz=5.5, bold=True)
    
    # Sub-view 1: Sectional Elevation of Distributor inside 750 mm ID Shell
    # Centerline at X = DA_X + 12.25 = 14.75, Y datum = DA_Y + 14.5
    CX_DA = DA_X + 12.25
    CY_DA_ELEV = DA_Y + 15.5
    R_COL = 7.5  # 750 mm scaled for detail view (15.0 cm total diameter)
    
    # Column Shell Walls
    cad_line(ax, CX_DA - R_COL, CY_DA_ELEV - 5.0, CX_DA - R_COL, CY_DA_ELEV + 5.0, lw=1.2)
    cad_line(ax, CX_DA + R_COL, CY_DA_ELEV - 5.0, CX_DA + R_COL, CY_DA_ELEV + 5.0, lw=1.2)
    cad_line(ax, CX_DA - R_COL - 0.25, CY_DA_ELEV - 5.0, CX_DA - R_COL - 0.25, CY_DA_ELEV + 5.0, lw=0.6)
    cad_line(ax, CX_DA + R_COL + 0.25, CY_DA_ELEV - 5.0, CX_DA + R_COL + 0.25, CY_DA_ELEV + 5.0, lw=0.6)
    cad_hatch_rect(ax, CX_DA - R_COL - 0.25, CY_DA_ELEV - 5.0, 0.25, 10.0, pitch=0.20, lw=0.35)
    cad_hatch_rect(ax, CX_DA + R_COL, CY_DA_ELEV - 5.0, 0.25, 10.0, pitch=0.20, lw=0.35)
    cad_line(ax, CX_DA, CY_DA_ELEV - 5.5, CX_DA, CY_DA_ELEV + 5.5, lw=0.5, ls='-.')
    
    # Water Feed Inlet Nozzle N3 (DN80) entering from Right
    cad_rect(ax, CX_DA + R_COL, CY_DA_ELEV + 2.0, 2.5, 0.80, lw=1.0, fill=True)
    cad_flange(ax, CX_DA + R_COL + 2.5, CY_DA_ELEV + 2.4, orientation='H', length=1.4)
    cad_arrow(ax, CX_DA + R_COL + 3.8, CY_DA_ELEV + 2.4, CX_DA + R_COL + 1.2, CY_DA_ELEV + 2.4, lw=1.2)
    cad_balloon(ax, CX_DA + R_COL + 3.2, CY_DA_ELEV + 3.3, 'N3')
    cad_text(ax, CX_DA + R_COL + 3.5, CY_DA_ELEV + 1.2, 'N3: WATER IN\nDN 80 CL 150 RF', sz=4.8, bold=True)
    
    # Internal Feed Pipe down to central manifold
    cad_line(ax, CX_DA + R_COL, CY_DA_ELEV + 2.8, CX_DA + 0.8, CY_DA_ELEV + 2.8, lw=1.0)
    cad_line(ax, CX_DA + R_COL, CY_DA_ELEV + 2.0, CX_DA - 0.8, CY_DA_ELEV + 2.0, lw=1.0)
    # Downcomer pipe into header
    cad_line(ax, CX_DA - 0.8, CY_DA_ELEV + 2.0, CX_DA - 0.8, CY_DA_ELEV + 0.8, lw=1.0)
    cad_line(ax, CX_DA + 0.8, CY_DA_ELEV + 2.8, CX_DA + 0.8, CY_DA_ELEV + 0.8, lw=1.0)
    
    # Central Main Header (DN100 / 4" Sch 40S)
    cad_rect(ax, CX_DA - 1.2, CY_DA_ELEV - 0.4, 2.4, 1.2, lw=1.2, fill=True)
    cad_text(ax, CX_DA, CY_DA_ELEV + 0.2, 'MAIN HEADER\nDN 100 SCH 40S', sz=4.8, bold=True)
    
    # Lateral Distribution Pipes (4 Branch Arms: DN50 / 2" Sch 40S)
    cad_rect(ax, CX_DA - R_COL + 0.6, CY_DA_ELEV - 0.30, 2 * R_COL - 1.2, 0.60, lw=1.0, fill=True)
    # Pipe End Caps
    cad_arc(ax, CX_DA - R_COL + 0.6, CY_DA_ELEV, 0.4, 0.6, theta1=90, theta2=270, lw=1.0)
    cad_arc(ax, CX_DA + R_COL - 0.6, CY_DA_ELEV, 0.4, 0.6, theta1=270, theta2=450, lw=1.0)
    
    # Downward Orifice Holes & Splash Baffles
    for ox in np.linspace(CX_DA - R_COL + 1.2, CX_DA + R_COL - 1.2, 11):
        cad_line(ax, ox - 0.08, CY_DA_ELEV - 0.30, ox - 0.08, CY_DA_ELEV - 0.50, lw=0.8)
        cad_line(ax, ox + 0.08, CY_DA_ELEV - 0.30, ox + 0.08, CY_DA_ELEV - 0.50, lw=0.8)
        # Splash plate
        cad_line(ax, ox - 0.22, CY_DA_ELEV - 0.65, ox + 0.22, CY_DA_ELEV - 0.65, lw=1.0)
        # Jet spray cone
        cad_line(ax, ox - 0.20, CY_DA_ELEV - 0.65, ox - 0.55, CY_DA_ELEV - 2.2, lw=0.6, ls=':')
        cad_line(ax, ox + 0.20, CY_DA_ELEV - 0.65, ox + 0.55, CY_DA_ELEV - 2.2, lw=0.6, ls=':')
    cad_text(ax, CX_DA, CY_DA_ELEV - 1.4, 'ORIFICE DISCHARGE JETS (do = 6 mm, PITCH = 75 mm)\nIRRIGATION DENSITY = 64 POINTS/m²', sz=4.6, bold=True, bg='white')
    
    # Wall Wiper Ring (redirecting liquid away from shell wall)
    cad_line(ax, CX_DA - R_COL, CY_DA_ELEV - 1.2, CX_DA - R_COL + 1.1, CY_DA_ELEV - 1.8, lw=1.2)
    cad_line(ax, CX_DA + R_COL, CY_DA_ELEV - 1.2, CX_DA + R_COL - 1.1, CY_DA_ELEV - 1.8, lw=1.2)
    cad_text(ax, CX_DA - R_COL + 2.0, CY_DA_ELEV - 2.2, 'PERIPHERAL WALL WIPER\n& REDISTRIBUTOR RING', sz=4.2, ha='left', bold=True)
    
    # Leveling Jacking Screws & Support Brackets
    for b_side in [-1, 1]:
        bx = CX_DA + b_side * (R_COL - 0.2)
        cad_rect(ax, min(bx, bx - b_side*1.2), CY_DA_ELEV - 0.8, 1.2, 0.40, lw=0.9, fill=True)
        # Jacking bolt
        cad_line(ax, bx - b_side*0.6, CY_DA_ELEV - 1.2, bx - b_side*0.6, CY_DA_ELEV - 0.2, lw=0.9)
    cad_text(ax, CX_DA + R_COL - 2.5, CY_DA_ELEV - 0.5, 'LEVELING SCREWS\n(±1.0 mm TOLERANCE)', sz=4.2, ha='right', bold=True)
    
    # Sub-view 2: Plan View (Below Elevation)
    CY_DA_PLAN = DA_Y + 5.5
    cad_circle(ax, CX_DA, CY_DA_PLAN, 3.8, lw=1.2, fill=True) # Column ID (scaled)
    cad_circle(ax, CX_DA, CY_DA_PLAN, 3.95, lw=0.6) # Column OD
    cad_line(ax, CX_DA - 4.5, CY_DA_PLAN, CX_DA + 4.5, CY_DA_PLAN, lw=0.4, ls='-.')
    cad_line(ax, CX_DA, CY_DA_PLAN - 4.5, CX_DA, CY_DA_PLAN + 4.5, lw=0.4, ls='-.')
    
    # Central Header
    cad_rect(ax, CX_DA - 0.4, CY_DA_PLAN - 2.8, 0.8, 5.6, lw=1.0, fill=True)
    # Laterals
    for ly in [CY_DA_PLAN - 1.8, CY_DA_PLAN - 0.6, CY_DA_PLAN + 0.6, CY_DA_PLAN + 1.8]:
        lw_w = 2 * np.sqrt(max(0, 3.6**2 - (ly - CY_DA_PLAN)**2))
        cad_rect(ax, CX_DA - lw_w/2, ly - 0.15, lw_w, 0.30, lw=0.8, fill=True)
        # Orifice marks on plan
        for px in np.linspace(CX_DA - lw_w/2 + 0.4, CX_DA + lw_w/2 - 0.4, 5):
            cad_circle(ax, px, ly, 0.05, fill=True, fc=BK)
    cad_text(ax, CX_DA, CY_DA_PLAN - 4.2, 'PLAN VIEW: HEADER-LATERAL PIPE MATRIX (4 BRANCHES)', sz=4.8, bold=True)
    
    # Dimensions on Distributor Detail
    cad_dim_h(ax, CX_DA - R_COL, CX_DA + R_COL, CY_DA_ELEV + 4.2, 'COLUMN ID 750 mm')
    cad_dim_h(ax, CX_DA - 1.2, CX_DA + 1.2, CY_DA_ELEV + 1.5, 'HEADER DN100')
    
    # ─────────────────────────────────────────────────────────────────────────
    # DETAIL B: MIST ELIMINATOR (DEMISTER) ASSEMBLY
    # ─────────────────────────────────────────────────────────────────────────
    DB_X, DB_Y, DB_W, DB_H = 27.5, 29.0, 24.5, 23.5
    cad_rect(ax, DB_X, DB_Y, DB_W, DB_H, lw=1.2, fill=True)
    cad_text(ax, DB_X + DB_W/2, DB_Y + DB_H - 0.7,
             'DETAIL B — WIRE MESH DEMISTER (MIST ELIMINATOR) ASSEMBLY', sz=7.8, bold=True)
    cad_text(ax, DB_X + DB_W/2, DB_Y + DB_H - 1.4,
             'CROSS-SECTION & HOLD-DOWN DETAILS (SCALE 1:8 METRIC)', sz=5.5, bold=True)
    
    CX_DB = DB_X + 12.25
    CY_DB = DB_Y + 12.5
    R_DB = 8.0  # 750 mm scaled for demister view
    
    # Shell Walls
    cad_line(ax, CX_DB - R_DB, CY_DB - 8.0, CX_DB - R_DB, CY_DB + 8.0, lw=1.2)
    cad_line(ax, CX_DB + R_DB, CY_DB - 8.0, CX_DB + R_DB, CY_DB + 8.0, lw=1.2)
    cad_line(ax, CX_DB - R_DB - 0.25, CY_DB - 8.0, CX_DB - R_DB - 0.25, CY_DB + 8.0, lw=0.6)
    cad_line(ax, CX_DB + R_DB + 0.25, CY_DB - 8.0, CX_DB + R_DB + 0.25, CY_DB + 8.0, lw=0.6)
    cad_hatch_rect(ax, CX_DB - R_DB - 0.25, CY_DB - 8.0, 0.25, 16.0, pitch=0.20, lw=0.35)
    cad_hatch_rect(ax, CX_DB + R_DB, CY_DB - 8.0, 0.25, 16.0, pitch=0.20, lw=0.35)
    cad_line(ax, CX_DB, CY_DB - 8.5, CX_DB, CY_DB + 8.5, lw=0.5, ls='-.')
    
    # Internal Shell Support Ring (50x8 mm continuous ring)
    cad_rect(ax, CX_DB - R_DB, CY_DB - 2.5, 1.2, 0.35, lw=1.0, fill=True)
    cad_rect(ax, CX_DB + R_DB - 1.2, CY_DB - 2.5, 1.2, 0.35, lw=1.0, fill=True)
    # Drain weep holes in ring
    cad_circle(ax, CX_DB - R_DB + 0.5, CY_DB - 2.32, 0.08, fill=True)
    cad_circle(ax, CX_DB + R_DB - 0.5, CY_DB - 2.32, 0.08, fill=True)
    cad_text(ax, CX_DB + R_DB - 1.8, CY_DB - 3.1, 'SUPPORT RING (50x8 mm)\nWITH WEEP HOLES', sz=4.5, ha='right', bold=True)
    
    # Demister Mesh Pad (150 mm thick)
    h_dem = 3.2  # 150 mm scaled
    cad_rect(ax, CX_DB - R_DB + 0.2, CY_DB - h_dem/2, 2 * R_DB - 0.4, h_dem, lw=1.1, fill=True)
    cad_hatch_rect(ax, CX_DB - R_DB + 0.2, CY_DB - h_dem/2, 2 * R_DB - 0.4, h_dem, pitch=0.18, angle=45, lw=0.4)
    cad_hatch_rect(ax, CX_DB - R_DB + 0.2, CY_DB - h_dem/2, 2 * R_DB - 0.4, h_dem, pitch=0.18, angle=-45, lw=0.4)
    
    # Bottom Support Grid (welded flat bars 25x3 mm on 100 mm pitch)
    cad_rect(ax, CX_DB - R_DB + 0.1, CY_DB - h_dem/2 - 0.45, 2 * R_DB - 0.2, 0.45, lw=1.0, fill=True)
    for bx in np.linspace(CX_DB - R_DB + 1.2, CX_DB + R_DB - 1.2, 7):
        cad_line(ax, bx, CY_DB - h_dem/2 - 0.45, bx, CY_DB - h_dem/2, lw=0.9)
    cad_text(ax, CX_DB, CY_DB - h_dem/2 - 0.85, 'BOTTOM SUPPORT GRID (FLAT BARS 25x3 mm)', sz=4.5, bold=True)
    
    # Top Hold-Down Grid
    cad_rect(ax, CX_DB - R_DB + 0.1, CY_DB + h_dem/2, 2 * R_DB - 0.2, 0.45, lw=1.0, fill=True)
    for bx in np.linspace(CX_DB - R_DB + 1.2, CX_DB + R_DB - 1.2, 7):
        cad_line(ax, bx, CY_DB + h_dem/2, bx, CY_DB + h_dem/2 + 0.45, lw=0.9)
    cad_text(ax, CX_DB, CY_DB + h_dem/2 + 0.85, 'TOP RETAINING GRID & HOLD-DOWN J-BOLTS', sz=4.5, bold=True)
    
    # J-Bolts / Clamping Tie Rods (clamping top grid to bottom ring)
    for j_side in [-1, 1]:
        jx = CX_DB + j_side * (R_DB - 0.6)
        cad_line(ax, jx, CY_DB - h_dem/2 - 0.8, jx, CY_DB + h_dem/2 + 0.7, lw=0.9)
        # Hook bottom
        cad_arc(ax, jx - j_side*0.2, CY_DB - h_dem/2 - 0.8, 0.4, 0.4, theta1=180, theta2=360, lw=0.9)
        # Nut on top
        cad_rect(ax, jx - 0.2, CY_DB + h_dem/2 + 0.5, 0.4, 0.25, lw=0.8, fill=True)
    
    # Demister Wash Spray Header (Nozzle N11, DN40) above mesh
    cad_rect(ax, CX_DB - 3.5, CY_DB + 4.5, 7.0, 0.35, lw=0.9, fill=True)
    for sx in [CX_DB - 2.0, CX_DB, CX_DB + 2.0]:
        cad_line(ax, sx, CY_DB + 4.5, sx, CY_DB + 3.8, lw=0.8)
        # Full cone spray nozzle
        cad_circle(ax, sx, CY_DB + 3.7, 0.15, fill=True)
        cad_line(ax, sx, CY_DB + 3.6, sx - 1.1, CY_DB + 1.2, lw=0.6, ls=':')
        cad_line(ax, sx, CY_DB + 3.6, sx + 1.1, CY_DB + 1.2, lw=0.6, ls=':')
    cad_text(ax, CX_DB, CY_DB + 5.2, 'N11: DEMISTER FLUSH SPRAY SYSTEM (DN 40)\nINTERMITTENT SOLUTE / SALT WASHDOWN', sz=4.8, bold=True)
    
    # Mesh Specification Callout Box
    cad_text(ax, CX_DB, CY_DB,
             'KNITTED WIRE MESH PAD (150 mm THICKNESS)\n'
             'MOC: SS316L WIRE + CO-KNITTED PTFE FILAMENTS\n'
             'BULK DENSITY: 144 kg/m³ | VOID FRACTION: 98.2%\n'
             'EFFICIENCY: >99.5% SEPARATION (DROPLETS ≥ 5 µm)\n'
             'DESIGN ΔP: 120 Pa (12 mm H2O) AT vG = 0.599 m/s',
             sz=5.0, bold=True, bg='white')
    
    # Dimensions on Demister Detail
    cad_dim_h(ax, CX_DB - R_DB, CX_DB + R_DB, CY_DB + 6.8, 'COLUMN ID 750 mm')
    cad_dim_v(ax, CX_DB - R_DB - 1.2, CY_DB - h_dem/2, CY_DB + h_dem/2, 'PAD 150 mm', text_offset=-0.45)
    
    # ─────────────────────────────────────────────────────────────────────────
    # DETAIL C: RASCHIG RING GEOMETRY & PACKING BED DETAILS
    # ─────────────────────────────────────────────────────────────────────────
    DC_X, DC_Y, DC_W, DC_H = 2.5, 7.2, 24.5, 21.0
    cad_rect(ax, DC_X, DC_Y, DC_W, DC_H, lw=1.2, fill=True)
    cad_text(ax, DC_X + DC_W/2, DC_Y + DC_H - 0.7,
             'DETAIL C — 25-mm CERAMIC RASCHIG RING & BED DETAIL', sz=7.8, bold=True)
    cad_text(ax, DC_X + DC_W/2, DC_Y + DC_H - 1.4,
             '3D ISOMETRIC, ORTHOGRAPHIC CAD & PROPERTIES (SCALE 1:1 METRIC)', sz=5.5, bold=True)
    
    # Orthographic Projection 1: Front Elevation & Section of Single Ring
    # Diameter = 25 mm -> Canvas 3.0 cm, Height = 25 mm -> Canvas 3.0 cm
    RX1 = DC_X + 4.5
    RY1 = DC_Y + 11.0
    cad_rect(ax, RX1 - 1.5, RY1 - 1.5, 3.0, 3.0, lw=1.2, fill=True) # OD 25
    # Cross-section showing wall thickness 4 mm (scaled to 0.48 cm)
    cad_line(ax, RX1 - 1.5, RY1 - 1.5, RX1 - 1.5, RY1 + 1.5, lw=1.2)
    cad_line(ax, RX1 - 1.02, RY1 - 1.5, RX1 - 1.02, RY1 + 1.5, lw=0.9)
    cad_line(ax, RX1 + 1.02, RY1 - 1.5, RX1 + 1.02, RY1 + 1.5, lw=0.9)
    cad_line(ax, RX1 + 1.5, RY1 - 1.5, RX1 + 1.5, RY1 + 1.5, lw=1.2)
    cad_hatch_rect(ax, RX1 - 1.5, RY1 - 1.5, 0.48, 3.0, pitch=0.15, lw=0.35)
    cad_hatch_rect(ax, RX1 + 1.02, RY1 - 1.5, 0.48, 3.0, pitch=0.15, lw=0.35)
    cad_line(ax, RX1, RY1 - 2.0, RX1, RY1 + 2.0, lw=0.4, ls='-.') # Centerline
    cad_text(ax, RX1, RY1 - 2.3, 'FRONT SECTION A-A', sz=4.8, bold=True)
    
    # Orthographic Projection 2: Plan View of Single Ring
    RY2 = DC_Y + 4.5
    cad_circle(ax, RX1, RY2, 1.5, lw=1.2, fill=True) # OD 25
    cad_circle(ax, RX1, RY2, 1.02, lw=0.9) # ID 17
    cad_line(ax, RX1 - 1.8, RY2, RX1 + 1.8, RY2, lw=0.4, ls='-.')
    cad_line(ax, RX1, RY2 - 1.8, RX1, RY2 + 1.8, lw=0.4, ls='-.')
    cad_text(ax, RX1, RY2 - 2.2, 'TOP PLAN VIEW', sz=4.8, bold=True)
    
    # Dimensions on Ring
    cad_dim_h(ax, RX1 - 1.5, RX1 + 1.5, RY1 + 1.8, 'OD 25.0 mm')
    cad_dim_v(ax, RX1 - 1.8, RY1 - 1.5, RY1 + 1.5, '25.0 mm', text_offset=-0.40)
    cad_dim_h(ax, RX1 - 1.02, RX1 + 1.02, RY2 + 1.7, 'ID 17.0 mm (t=4 mm)')
    
    # 3D Isometric View of Single Ring
    RX_ISO = DC_X + 11.5
    RY_ISO = DC_Y + 11.5
    # Outer top ellipse
    cad_arc(ax, RX_ISO, RY_ISO + 1.2, 3.2, 1.3, theta1=0, theta2=360, lw=1.2)
    # Inner top ellipse
    cad_arc(ax, RX_ISO, RY_ISO + 1.2, 2.1, 0.85, theta1=0, theta2=360, lw=0.9)
    # Outer cylinder sides
    cad_line(ax, RX_ISO - 1.6, RY_ISO + 1.2, RX_ISO - 1.6, RY_ISO - 1.2, lw=1.2)
    cad_line(ax, RX_ISO + 1.6, RY_ISO + 1.2, RX_ISO + 1.6, RY_ISO - 1.2, lw=1.2)
    # Outer bottom ellipse (lower half)
    cad_arc(ax, RX_ISO, RY_ISO - 1.2, 3.2, 1.3, theta1=180, theta2=360, lw=1.2)
    # Inner bore bottom dashed
    cad_arc(ax, RX_ISO, RY_ISO - 1.2, 2.1, 0.85, theta1=180, theta2=360, lw=0.6, ls='--')
    cad_text(ax, RX_ISO, RY_ISO - 2.3, '3D ISOMETRIC PROJECTION', sz=4.8, bold=True)
    
    # Engineering Specifications & Physical Data Panel
    TX_PROP = DC_X + 15.2
    TY_PROP = DC_Y + 17.5
    cad_rect(ax, TX_PROP, DC_Y + 1.5, 8.8, 17.0, lw=1.0, fill=True)
    cad_text(ax, TX_PROP + 4.4, TY_PROP - 0.4, 'RASCHIG RING DESIGN DATA', sz=5.8, bold=True)
    cad_line(ax, TX_PROP, TY_PROP - 0.8, TX_PROP + 8.8, TY_PROP - 0.8, lw=0.8)
    
    prop_lines = [
        ("Nominal Ring Size:", "25 mm (1.0 inch)"),
        ("Material of Constr.:", "Glazed Chemical Stoneware"),
        ("Standard / Code:", "ASTM C515 Class 1"),
        ("Specific Surface (ap):", "190 m²/m³"),
        ("Bed Void Fraction (ε):", "0.74 (74.0% Void)"),
        ("Bulk Density (ρbulk):", "680 kg/m³"),
        ("Packing Factor (Fp):", "100 m⁻¹ (30.48 ft²/ft³)"),
        ("Acid Resistance:", ">99.8% (Boiling H2SO4)"),
        ("Water Absorption:", "<0.5% (Non-porous)"),
        ("Compressive Strength:", ">150 MPa"),
        ("Active Bed Height (Z):", "4500 mm (Calculated)"),
        ("Active Bed Volume (Vp):", "1.79 m³ (Selected 1.99 m³)"),
        ("Dry Packing Mass (Mp):", "1220 kg (1.22 tonnes)"),
        ("Dry Gravity Load (Wp):", "11.9 kN (Calculated)"),
        ("Flooded Holdup Load:", "12.9 kN (Contingency)"),
        ("Support Design Load:", "16.1 kN (26.4 kN Upset)"),
    ]
    for idx, (label, val) in enumerate(prop_lines):
        yy = TY_PROP - 1.5 - idx * 0.95
        cad_text(ax, TX_PROP + 0.3, yy, label, sz=4.4, ha='left', bold=True)
        cad_text(ax, TX_PROP + 8.5, yy, val, sz=4.4, ha='right', bold=('11.9' in val or '4500' in val or '190' in val))
    
    # ─────────────────────────────────────────────────────────────────────────
    # DETAIL D: BOTTOM GAS INLET & GAS DEFLECTOR ASSEMBLY
    # ─────────────────────────────────────────────────────────────────────────
    DD_X, DD_Y, DD_W, DD_H = 27.5, 7.2, 24.5, 21.0
    cad_rect(ax, DD_X, DD_Y, DD_W, DD_H, lw=1.2, fill=True)
    cad_text(ax, DD_X + DD_W/2, DD_Y + DD_H - 0.7,
             'DETAIL D — BOTTOM GAS INLET & AERODYNAMIC DEFLECTOR', sz=7.8, bold=True)
    cad_text(ax, DD_X + DD_W/2, DD_Y + DD_H - 1.4,
             'CROSS-SECTION & FLOW DISTRIBUTION INTERNALS (SCALE 1:8 METRIC)', sz=5.5, bold=True)
    
    CX_DD = DD_X + 12.25
    CY_DD = DD_Y + 11.5
    R_DD = 8.0  # 750 mm scaled
    
    # Shell Walls & Bottom Head Tangent Line
    cad_line(ax, CX_DD - R_DD, CY_DD - 3.5, CX_DD - R_DD, CY_DD + 7.5, lw=1.2)
    cad_line(ax, CX_DD + R_DD, CY_DD - 3.5, CX_DD + R_DD, CY_DD + 7.5, lw=1.2)
    cad_line(ax, CX_DD - R_DD - 0.25, CY_DD - 3.5, CX_DD - R_DD - 0.25, CY_DD + 7.5, lw=0.6)
    cad_line(ax, CX_DD + R_DD + 0.25, CY_DD - 3.5, CX_DD + R_DD + 0.25, CY_DD + 7.5, lw=0.6)
    cad_hatch_rect(ax, CX_DD - R_DD - 0.25, CY_DD - 3.5, 0.25, 11.0, pitch=0.20, lw=0.35)
    cad_hatch_rect(ax, CX_DD + R_DD, CY_DD - 3.5, 0.25, 11.0, pitch=0.20, lw=0.35)
    cad_line(ax, CX_DD, CY_DD - 7.5, CX_DD, CY_DD + 8.0, lw=0.5, ls='-.')
    
    # Bottom Ellipsoidal Head contour
    cad_arc(ax, CX_DD, CY_DD - 3.5, 2 * R_DD, 4.0, theta1=180, theta2=360, lw=1.2)
    cad_arc(ax, CX_DD, CY_DD - 3.5, 2 * (R_DD - 0.25), 3.5, theta1=180, theta2=360, lw=0.8)
    
    # Gas Inlet Nozzle N1 (DN150 Class 150 RF) entering from Left
    cad_rect(ax, CX_DD - R_DD - 2.8, CY_DD - 0.8, 2.8, 1.6, lw=1.1, fill=True)
    cad_flange(ax, CX_DD - R_DD - 2.8, CY_DD, orientation='H', length=2.2)
    cad_arrow(ax, CX_DD - R_DD - 4.2, CY_DD, CX_DD - R_DD - 1.5, CY_DD, lw=1.4, head_scale=12)
    cad_balloon(ax, CX_DD - R_DD - 3.6, CY_DD + 1.5, 'N1')
    cad_text(ax, CX_DD - R_DD - 3.6, CY_DD - 1.8, 'N1: GAS INLET\nDN 150 CL 150 RF\n(QG = 0.25 m3/s)', sz=4.8, bold=True)
    
    # Aerodynamic Gas Deflector (Inverted 60° Chevron / Conical Baffle)
    p_def = [(CX_DD - 4.2, CY_DD - 1.2), (CX_DD, CY_DD + 1.8), (CX_DD + 4.2, CY_DD - 1.2)]
    ax.add_patch(Polygon(p_def, closed=False, ec=BK, lw=1.6, fill=False))
    # Lip skirts
    cad_line(ax, CX_DD - 4.2, CY_DD - 1.2, CX_DD - 4.2, CY_DD - 2.0, lw=1.2)
    cad_line(ax, CX_DD + 4.2, CY_DD - 1.2, CX_DD + 4.2, CY_DD - 2.0, lw=1.2)
    # Stiffener rib & shell mounting gussets
    cad_line(ax, CX_DD, CY_DD + 1.8, CX_DD, CY_DD + 0.2, lw=1.0)
    cad_line(ax, CX_DD - 4.2, CY_DD - 1.2, CX_DD - R_DD, CY_DD - 1.2, lw=0.9, ls='--')
    cad_line(ax, CX_DD + 4.2, CY_DD - 1.2, CX_DD + R_DD, CY_DD - 1.2, lw=0.9, ls='--')
    
    # Gas Flow Distribution Arrows (Aerodynamic deflection upward)
    for ax_offset in [-3.0, -1.5, 1.5, 3.0]:
        cad_arrow(ax, CX_DD + ax_offset, CY_DD + 2.2, CX_DD + ax_offset, CY_DD + 5.2, lw=1.0, head_scale=8)
    cad_text(ax, CX_DD, CY_DD + 3.8, 'UPWARD GAS PLENUM FLOW (vG = 0.599 m/s)\nUNIFORM CROSS-SECTIONAL VELOCITY', sz=4.6, bold=True, bg='white')
    
    # Falling Liquid Drainage & Sump
    for lx_pos in [-6.0, -5.2, 5.2, 6.0]:
        cad_arrow(ax, CX_DD + lx_pos, CY_DD + 1.0, CX_DD + lx_pos, CY_DD - 3.2, lw=0.9, ls=':', head_scale=6)
    cad_text(ax, CX_DD - 5.5, CY_DD - 1.8, 'LIQUID RAIN\nBYPASSES GAS INLET', sz=4.0, ha='center', bold=True)
    
    # Sump, Anti-Vortex Baffle & Rich Liquid Outlet N4
    cad_rect(ax, CX_DD - 0.7, CY_DD - 5.5, 1.4, 0.6, lw=0.9, fill=True)
    cad_line(ax, CX_DD, CY_DD - 5.3, CX_DD, CY_DD - 3.8, lw=1.2) # Anti-vortex baffle
    cad_line(ax, CX_DD - 0.8, CY_DD - 4.5, CX_DD + 0.8, CY_DD - 4.5, lw=1.2)
    cad_text(ax, CX_DD + 1.2, CY_DD - 4.4, 'ANTI-VORTEX\nCROSS BAFFLE', sz=4.4, ha='left', bold=True)
    
    # Bottom Liquid Outlet Nozzle N4 (DN80)
    cad_rect(ax, CX_DD - 0.45, CY_DD - 7.5, 0.90, 2.0, lw=1.0, fill=True)
    cad_flange(ax, CX_DD, CY_DD - 7.5, orientation='V', length=1.4)
    cad_arrow(ax, CX_DD, CY_DD - 7.5, CX_DD, CY_DD - 8.6, lw=1.2)
    cad_balloon(ax, CX_DD - 1.2, CY_DD - 8.0, 'N4')
    cad_text(ax, CX_DD + 1.0, CY_DD - 8.0, 'N4: RICH WATER OUTLET\nDN 80 CL 150 RF (x1 = 2.79 x 10⁻⁴)', sz=4.8, ha='left', bold=True)
    
    # Dimensions on Gas Inlet Detail
    cad_dim_h(ax, CX_DD - R_DD, CX_DD + R_DD, CY_DD + 6.8, 'COLUMN ID 750 mm')
    cad_dim_v(ax, CX_DD - R_DD - 1.2, CY_DD - 0.8, CY_DD + 0.8, 'DN 150', text_offset=-0.40)
    
    # ═════════════════════════════════════════════════════════════════════════
    # RIGHT PANEL: TABLES & INTERNALS ENGINEERING NOTES (X = 53.0 to 81.5)
    # ═════════════════════════════════════════════════════════════════════════
    
    # TABLE 1: ABSORBER INTERNALS MECHANICAL DESIGN & HYDRAULIC SUMMARY
    T1_X = 53.0
    T1_Y = 36.5
    t1_headers = ['INTERNAL COMPONENT', 'DESIGN PARAMETERS / MOC', 'HYDRAULIC FUNCTION / CAPACITY']
    t1_widths  = [8.2, 9.8, 10.5]
    t1_rows = [
        ['Liquid Distributor',   'Header-Lateral (4 branches)\nSS316L / PVDF lined', 'Irrigation density = 64 pts/m²\nOrifice velocity = 1.65 m/s'],
        ['Liquid Redistributor', 'Perforated cone + wall wiper\nTitanium Gr 2 / PTFE', 'Collects wall flow (<5% wall channeling)\nRedistributes across active bed'],
        ['Packing Hold-Down',    'Heavy-duty grid + mesh\nSS316L (50x5 mm frame)', 'Prevents ring lifting & bed expansion\nDesign upward gas thrust = 1.8 kN'],
        ['Raschig Ring Bed',     '25-mm Ceramic Raschig Rings\n4500 mm Depth | Vp = 1.79 m³', 'Total gas transfer units N_OG = 5.09\nH_OG = 0.84 m (Onda correlation)'],
        ['Packing Support Grid', 'Multi-beam gas-injection\nFree flow area > 85%', 'Carries 16.1 kN normal operating load\nPrevents premature flooding at support'],
        ['Gas Inlet Deflector',  'Inverted 60° conical chevron\nTitanium Gr 2 (4 mm thk)', 'Reduces gas inlet velocity from 14.1 m/s\nto uniform column velocity 0.599 m/s'],
        ['Mist Eliminator',      'Knitted wire mesh (150 mm)\nSS316L + PTFE composite', '>99.5% droplet removal (≥5 µm)\nPressure drop ΔP = 120 Pa at design flow'],
        ['Demister Spray Wash',  'Full-cone spray nozzles (3x)\nDN 40 manifold (SS316L)', 'Periodic flush of captured bromine\nPrevents mesh salt fouling and high ΔP'],
        ['Anti-Vortex Baffle',   'Cross-plate baffle (4 mm thk)\nSA-516 Gr 70 + PVDF lined', 'Suppresses liquid vortexing & air entrainment\nEnsures steady suction to bottoms pump'],
    ]
    cad_draw_table(ax, T1_X, T1_Y, t1_headers, t1_rows, t1_widths, row_h=0.75,
                   title='TABLE 1 — ABSORBER INTERNALS MECHANICAL DESIGN & HYDRAULIC SUMMARY', sz=4.8)
    
    # TABLE 2: BILL OF MATERIALS (BOM) FOR COLUMN INTERNALS
    T2_X = 53.0
    T2_Y = 22.0
    t2_headers = ['ITEM', 'DESCRIPTION', 'QTY', 'MATERIAL SPECIFICATION', 'WEIGHT (KG)']
    t2_widths  = [1.4, 9.2, 1.6, 12.0, 4.3]
    t2_rows = [
        ['1', 'Mist Eliminator Pad',    '1 SET', 'SS316L Wire + PTFE Knitted Mesh', '18.5 kg'],
        ['2', 'Demister Retaining Grids','2 PCS', 'SS316L Flat Bars (25x3 mm)',      '24.0 kg'],
        ['3', 'Demister Flush Header',  '1 SET', 'DN 40 Sch 40S SS316L + 3 Nozzles', '12.2 kg'],
        ['4', 'Liquid Distributor Manifold','1 SET','DN 100/50 Sch 40S + PVDF Liner', '45.0 kg'],
        ['5', 'Wall Wiper Rings',       '2 SET', 'Titanium Gr 2 (3 mm Sheet)',       '14.8 kg'],
        ['6', 'Hold-Down Top Grid',     '1 SET', 'SS316L Heavy Mesh + Ring Frame',   '28.5 kg'],
        ['7', 'Ceramic Raschig Rings',   '1.79 m³','ASTM C515 Glazed Ceramic (25 mm)','1220.0 kg'],
        ['8', 'Gas-Injection Support Grid','1 SET','High-Strength FRP / Titanium Gr 2','65.0 kg'],
        ['9', 'Support Ring & Gussets',  '1 SET', 'SA-516 Gr 70 + 3 mm PVDF Clad',   '42.0 kg'],
        ['10','Gas Inlet Deflector Cone','1 PC',  'Titanium Gr 2 / PVDF Plate (4 mm)','16.5 kg'],
        ['11','Sump Anti-Vortex Baffle', '1 SET', 'SA-516 Gr 70 + PVDF (4 mm Plt)',  '11.0 kg'],
    ]
    cad_draw_table(ax, T2_X, T2_Y, t2_headers, t2_rows, t2_widths, row_h=0.48,
                   title='TABLE 2 — BILL OF MATERIALS (BOM) FOR ABSORBER INTERNALS', sz=4.8)
    
    # INTERNALS INSTALLATION & FABRICATION SPECIFICATIONS
    N2_X = 53.0
    N2_Y = 7.2
    cad_rect(ax, N2_X, N2_Y, 28.5, 14.2, lw=1.2, fill=True)
    cad_text(ax, N2_X + 14.25, N2_Y + 13.7, 'INTERNALS FABRICATION, TOLERANCES & INSTALLATION NOTES', sz=7.0, bold=True)
    
    notes_dwg2 = [
        "1. DISTRIBUTOR HORIZONTAL LEVELING TOLERANCE:",
        "   - DISTRIBUTOR LATERALS SHALL BE LEVELED WITHIN +/- 1.0 mm ACROSS THE FULL 750 mm COLUMN DIAMETER.",
        "   - VERIFICATION TO BE CONDUCTED USING WATER FLOODING TEST PRIOR TO PACKING CHARGING.",
        "2. PACKING BED CHARGING & FLOTATION PREVENTION:",
        "   - 25-mm CERAMIC RASCHIG RINGS SHALL BE DUMPED INTO A WATER-FILLED COLUMN (WET PACKING METHOD)",
        "     TO CUSHION RING IMPACT AND PREVENT CHIPPING / BREAKAGE OF PORCELAIN WALLS.",
        "   - TOP HOLD-DOWN GRID MUST BE FASTENED SECURELY TO SHELL CLEATS TO PREVENT RING FLUIDIZATION.",
        "3. SUPPORT GRID FREE AREA REQUIREMENT:",
        "   - SUPPORT GRID FREE FLOW AREA MUST EXCEED 85% OF COLUMN CROSS-SECTIONAL AREA TO ELIMINATE",
        "     BOTTLENECKING OF GAS INJECTION AND LOCAL PREMATURE FLOODING AT THE BED BASE.",
        "4. CORROSION & MATERIAL SELECTION RIGOR:",
        "   - DUE TO EXTREME AGGRESSIVENESS OF WET BROMINE (Br2 + H2O), ALL METALLIC FASTENERS EXPOSED",
        "     TO PROCESS VAPORS MUST BE HASTELLOY C-276 OR TITANIUM GRADE 2 (ASTM B348 / F468).",
        "   - GASKETS FOR INTERNAL FLANGES: VIRGIN PTFE ENVELOPE GASKETS (100% CORROSION RESISTANT).",
    ]
    for n_idx, n_line in enumerate(notes_dwg2):
        bold_flag = ("1." in n_line or "2." in n_line or "3." in n_line or "4." in n_line)
        cad_text(ax, N2_X + 0.40, N2_Y + 13.0 - n_idx * 0.70, n_line, sz=4.6, ha='left', bold=bold_flag)
    
    # ── Title Block ─────────────────────────────────────────────────────────
    draw_title_block(
        ax,
        dwg_title='PACKED-BED ABSORBER (C-101) — INTERNAL ASSEMBLY & PROCESS INTERNALS DETAILED CAD',
        dwg_no='PEDD-PBA-02',
        rev='00',
        sheet_no='02 OF 05',
        scale='DETAILED VIEWS 1:1, 1:8, 1:10 METRIC',
        equip_desc='ABSORBER PROCESS INTERNALS — DISTRIBUTOR, DEMISTER, PACKING & DEFLECTOR',
        duty_desc='25-mm CERAMIC RASCHIG RINGS | AP = 190 m²/m³ | ε = 0.74 | L = 17.25 kg/s'
    )
    
    # ── Save Outputs ────────────────────────────────────────────────────────
    OUT_DIR = r'd:\GAMES\zercxes\CAD_Engineering_Drawings'
    pdf_path = os.path.join(OUT_DIR, '02_Packed_Bed_Absorber_Internal_Assembly_CAD.pdf')
    png_path = os.path.join(OUT_DIR, '02_Packed_Bed_Absorber_Internal_Assembly_CAD.png')
    
    fig.savefig(pdf_path, dpi=300, bbox_inches='tight', facecolor='white')
    fig.savefig(png_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"SUCCESS: DWG-02 generated at {pdf_path} and {png_path}")

if __name__ == '__main__':
    generate_dwg02()
