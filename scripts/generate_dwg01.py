"""
DWG-01: GENERAL ARRANGEMENT & ELEVATION SECTIONAL CAD
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

def generate_dwg01():
    fig, ax = create_cad_canvas()
    draw_sheet_border(ax)
    
    # ── Scale & Layout Parameters ───────────────────────────────────────────
    # Scale: 1 unit on canvas = 250 mm real (1:25 Metric)
    # 750 mm ID = 3.00 cm on sheet
    # 4500 mm bed = 18.00 cm on sheet
    
    SCALE = 1.0 / 250.0  # mm to canvas cm
    
    R_ID = 750.0 / 2.0 * SCALE     # 1.50 cm
    THK  = 8.0 * SCALE             # Shell thickness ~0.032 cm -> visually drawn as 0.08 cm for CAD readability
    R_OD = R_ID + 0.08
    
    # Vertical datum levels (in real mm from ground +0.000):
    Z_GND       = 0.0
    Z_BASE_RING = 50.0
    Z_SKIRT_TOP = 1800.0   # Bottom head weld line / skirt tan
    Z_BTM_TAN   = 1800.0
    Z_BTM_APEX  = 1800.0 - 187.5  # 2:1 Ellipsoidal depth = D/4 = 187.5 mm
    Z_SUMP_OUT  = Z_BTM_APEX - 300.0
    
    Z_GAS_IN    = 2400.0   # Centerline of gas inlet N1
    Z_GRID      = 3000.0   # Packing support grid elevation
    Z_BED_TOP   = 3000.0 + 4500.0  # 7500.0 mm
    Z_DIST_PIPE = 7800.0   # Liquid distributor centerline
    Z_DEMISTER  = 8300.0   # Demister centerline (150 mm thick)
    Z_TOP_TAN   = 9000.0   # Top head tangent line
    Z_TOP_APEX  = 9000.0 + 187.5
    Z_VENT_FACE = Z_TOP_APEX + 350.0 # Top vent nozzle face
    
    # Convert datums to canvas Y coordinates (Ground at Y = 9.0 cm)
    Y_GND = 9.0
    y_at = lambda z_mm: Y_GND + z_mm * SCALE
    
    # Centerlines of the two elevations:
    CX_SEC = 15.5   # Sectional Elevation (Left)
    CX_EXT = 34.5   # Exterior Elevation (Right)
    
    # ═════════════════════════════════════════════════════════════════════════
    # VIEW 1: DETAILED SECTIONAL ELEVATION (CX = CX_SEC = 15.5)
    # ═════════════════════════════════════════════════════════════════════════
    
    # Centerline
    cad_line(ax, CX_SEC, y_at(Z_SUMP_OUT - 200), CX_SEC, y_at(Z_VENT_FACE + 250), lw=0.5, ls='-.', color=BK)
    cad_text(ax, CX_SEC, y_at(Z_VENT_FACE + 350), 'SECTIONAL ELEVATION A-A', sz=8.5, bold=True)
    cad_text(ax, CX_SEC, y_at(Z_VENT_FACE + 200), 'SCALE 1:25 METRIC', sz=6.5, bold=True)
    
    # 1. Concrete Foundation & Base Plate
    cad_rect(ax, CX_SEC - 2.8, Y_GND - 1.2, 5.6, 1.2, lw=1.2, fill=True, ec=BK)
    cad_hatch_rect(ax, CX_SEC - 2.8, Y_GND - 1.2, 5.6, 1.2, pitch=0.35, angle=-45, lw=0.4)
    cad_line(ax, CX_SEC - 3.5, Y_GND, CX_SEC + 3.5, Y_GND, lw=1.2) # Ground Line
    cad_text(ax, CX_SEC - 3.0, Y_GND - 0.35, 'FOUNDATION (CONCRETE)', sz=5.2, bold=True, ha='right')
    
    # Skirt Base Ring & Gussets
    y_base = y_at(Z_BASE_RING)
    cad_rect(ax, CX_SEC - 2.1, Y_GND, 4.2, (y_base - Y_GND), lw=1.0, fill=True)
    cad_text(ax, CX_SEC + 2.4, y_base, 'BASE RING OD 1050', sz=5.0, ha='left', bold=True)
    
    # Skirt Shell (Cylindrical)
    y_skirt_top = y_at(Z_SKIRT_TOP)
    cad_rect(ax, CX_SEC - R_OD, y_base, 2 * R_OD, y_skirt_top - y_base, lw=1.0)
    # Skirt Access Hole (DN400)
    cad_circle(ax, CX_SEC, y_at(900.0), 0.80, lw=0.9, fill=True)
    cad_circle(ax, CX_SEC, y_at(900.0), 0.65, lw=0.6, ls='--')
    cad_text(ax, CX_SEC, y_at(900.0), 'SKIRT ACCESS\nDN 400', sz=4.8, bold=True)
    # Skirt Vents
    cad_circle(ax, CX_SEC - 1.1, y_at(1600.0), 0.15, lw=0.7, fill=True)
    cad_circle(ax, CX_SEC + 1.1, y_at(1600.0), 0.15, lw=0.7, fill=True)
    
    # 2. Bottom Head (2:1 Ellipsoidal Section)
    y_btm_tan = y_at(Z_BTM_TAN)
    y_btm_apex = y_at(Z_BTM_APEX)
    # Outer head contour
    cad_arc(ax, CX_SEC, y_btm_tan, 2 * R_OD, 2 * (y_btm_tan - y_btm_apex), theta1=180, theta2=360, lw=1.1)
    # Inner head contour
    cad_arc(ax, CX_SEC, y_btm_tan, 2 * R_ID, 2 * (y_btm_tan - y_btm_apex - 0.08), theta1=180, theta2=360, lw=0.8)
    
    # Liquid Sump & Anti-Vortex Baffle
    cad_rect(ax, CX_SEC - 0.40, y_btm_apex - 0.25, 0.80, 0.25, lw=0.9, fill=True)
    cad_line(ax, CX_SEC, y_btm_apex - 0.20, CX_SEC, y_btm_apex + 0.30, lw=1.0) # Vortex Baffle
    cad_line(ax, CX_SEC - 0.30, y_btm_apex + 0.05, CX_SEC + 0.30, y_btm_apex + 0.05, lw=1.0)
    cad_text(ax, CX_SEC + 0.55, y_btm_apex + 0.10, 'ANTI-VORTEX\nBAFFLE', sz=4.8, ha='left', bold=True)
    
    # Bottom Liquid Outlet Nozzle N4 (DN80 Class 150)
    y_sump_out = y_at(Z_SUMP_OUT)
    cad_rect(ax, CX_SEC - 0.16, y_sump_out, 0.32, y_btm_apex - 0.25 - y_sump_out, lw=0.9, fill=True)
    cad_flange(ax, CX_SEC, y_sump_out, orientation='V', length=0.65)
    cad_balloon(ax, CX_SEC - 0.60, y_sump_out, 'N4')
    cad_text(ax, CX_SEC + 0.45, y_sump_out, 'N4: RICH WATER OUT\nDN 80 CL 150 RF', sz=5.0, ha='left', bold=True)
    
    # 3. Main Column Shell Section
    y_top_tan = y_at(Z_TOP_TAN)
    # Outer walls
    cad_line(ax, CX_SEC - R_OD, y_btm_tan, CX_SEC - R_OD, y_top_tan, lw=1.2)
    cad_line(ax, CX_SEC + R_OD, y_btm_tan, CX_SEC + R_OD, y_top_tan, lw=1.2)
    # Inner walls
    cad_line(ax, CX_SEC - R_ID, y_btm_tan, CX_SEC - R_ID, y_top_tan, lw=0.7)
    cad_line(ax, CX_SEC + R_ID, y_btm_tan, CX_SEC + R_ID, y_top_tan, lw=0.7)
    # Wall hatching (ASME shell thickness representation)
    cad_hatch_rect(ax, CX_SEC - R_OD, y_btm_tan, 0.08, y_top_tan - y_btm_tan, pitch=0.25, lw=0.4)
    cad_hatch_rect(ax, CX_SEC + R_ID, y_btm_tan, 0.08, y_top_tan - y_btm_tan, pitch=0.25, lw=0.4)
    
    # 4. Gas Inlet Nozzle N1 (DN150 Class 150) & Internal Deflector
    y_gas_in = y_at(Z_GAS_IN)
    # Left side nozzle penetration
    cad_rect(ax, CX_SEC - R_OD - 1.2, y_gas_in - 0.30, 1.2, 0.60, lw=0.9, fill=True)
    cad_flange(ax, CX_SEC - R_OD - 1.2, y_gas_in, orientation='H', length=0.90)
    cad_arrow(ax, CX_SEC - R_OD - 1.8, y_gas_in, CX_SEC - R_OD - 0.2, y_gas_in, lw=1.2)
    cad_balloon(ax, CX_SEC - R_OD - 1.5, y_gas_in + 0.60, 'N1')
    cad_text(ax, CX_SEC - R_OD - 1.5, y_gas_in - 0.65, 'N1: GAS INLET\nDN 150 (QG=0.25 m3/s)', sz=5.0, bold=True)
    
    # Internal Gas Deflector Baffle (Inverted Cone / Chevron)
    p_deflector = [(CX_SEC - 0.8, y_gas_in - 0.25), (CX_SEC, y_gas_in + 0.40), (CX_SEC + 0.8, y_gas_in - 0.25)]
    ax.add_patch(Polygon(p_deflector, closed=False, ec=BK, lw=1.2, fill=False))
    cad_line(ax, CX_SEC - 0.8, y_gas_in - 0.25, CX_SEC - 0.8, y_gas_in - 0.45, lw=0.9)
    cad_line(ax, CX_SEC + 0.8, y_gas_in - 0.25, CX_SEC + 0.8, y_gas_in - 0.45, lw=0.9)
    cad_text(ax, CX_SEC, y_gas_in - 0.10, 'AERODYNAMIC GAS DEFLECTOR\n& ENTRAINMENT SHEDDER', sz=4.8, bold=True)
    
    # 5. Packing Support Grid Assembly (Z = 3000.0)
    y_grid = y_at(Z_GRID)
    # Shell Support Ring Ledge
    cad_rect(ax, CX_SEC - R_ID, y_grid - 0.15, 0.30, 0.15, lw=1.0, fill=True)
    cad_rect(ax, CX_SEC + R_ID - 0.30, y_grid - 0.15, 0.30, 0.15, lw=1.0, fill=True)
    # Central Support I-Beam
    cad_rect(ax, CX_SEC - 0.15, y_grid - 0.45, 0.30, 0.45, lw=0.9, fill=True)
    cad_rect(ax, CX_SEC - 0.40, y_grid - 0.45, 0.80, 0.08, lw=0.9, fill=True)
    # Multi-beam high open area grid bars
    for gx in np.linspace(CX_SEC - R_ID + 0.35, CX_SEC + R_ID - 0.35, 11):
        cad_line(ax, gx, y_grid - 0.12, gx, y_grid + 0.12, lw=1.1)
    cad_line(ax, CX_SEC - R_ID, y_grid + 0.12, CX_SEC + R_ID, y_grid + 0.12, lw=1.1)
    cad_line(ax, CX_SEC - R_ID, y_grid - 0.12, CX_SEC + R_ID, y_grid - 0.12, lw=1.1)
    cad_text(ax, CX_SEC, y_grid - 0.70, 'GAS-INJECTION SUPPORT GRID (>85% FREE AREA)\nDRY LOAD: 11.9 kN | OPERATING: 16.1 kN', sz=4.8, bold=True)
    
    # 6. Packed Bed (4500 mm depth, 25-mm Ceramic Raschig Rings)
    y_bed_top = y_at(Z_BED_TOP)
    h_bed = y_bed_top - y_grid
    # Packing hatched pattern (Dense Raschig ring cross-hatch representation)
    cad_hatch_rect(ax, CX_SEC - R_ID, y_grid + 0.12, 2 * R_ID, h_bed - 0.12, pitch=0.32, angle=45, lw=0.35, color=GREY)
    cad_hatch_rect(ax, CX_SEC - R_ID, y_grid + 0.12, 2 * R_ID, h_bed - 0.12, pitch=0.32, angle=-45, lw=0.35, color=GREY)
    
    # Distinct ceramic rings drawn inside the bed for absolute CAD fidelity
    ring_locs = [
        (CX_SEC - 0.8, y_grid + 2.5), (CX_SEC + 0.6, y_grid + 4.2),
        (CX_SEC - 0.4, y_grid + 7.5), (CX_SEC + 0.7, y_grid + 10.8),
        (CX_SEC - 0.6, y_grid + 14.0), (CX_SEC + 0.3, y_grid + 16.2)
    ]
    for rx, ry in ring_locs:
        cad_rect(ax, rx - 0.18, ry - 0.18, 0.36, 0.36, lw=0.9, fill=True, ec=BK)
        cad_line(ax, rx - 0.10, ry - 0.18, rx - 0.10, ry + 0.18, lw=0.7)
        cad_line(ax, rx + 0.10, ry - 0.18, rx + 0.10, ry + 0.18, lw=0.7)
    
    # Packing Bed Annotation Box inside section
    cad_text(ax, CX_SEC, y_grid + h_bed/2 + 0.8,
             'PACKED BED (CALCULATED)\n'
             'HEIGHT Z = 4500 mm (SELECTED)\n'
             'INTERNAL DIAMETER D = 750 mm\n'
             '25-mm CERAMIC RASCHIG RINGS\n'
             'VOLUME Vp = 1.79 m³ | MASS Mp ≈ 1.22 t\n'
             'N_OG = 5.09 | H_OG = 0.84 m',
             sz=6.0, bold=True, bg='white')
    
    # Packing Hold-Down Grid (Top of Bed)
    cad_rect(ax, CX_SEC - R_ID, y_bed_top, 2 * R_ID, 0.15, lw=1.0, fill=True)
    for hx in np.linspace(CX_SEC - R_ID + 0.2, CX_SEC + R_ID - 0.2, 9):
        cad_line(ax, hx, y_bed_top, hx, y_bed_top + 0.15, lw=0.9)
    cad_text(ax, CX_SEC, y_bed_top + 0.35, 'HOLD-DOWN RETAINING GRID', sz=4.8, bold=True)
    
    # 7. Liquid Distributor Assembly (Z = 7800.0)
    y_dist = y_at(Z_DIST_PIPE)
    # Feed pipe entering from right shell
    cad_rect(ax, CX_SEC + R_OD, y_dist - 0.15, 1.2, 0.30, lw=0.9, fill=True)
    cad_flange(ax, CX_SEC + R_OD + 1.2, y_dist, orientation='H', length=0.65)
    cad_arrow(ax, CX_SEC + R_OD + 1.8, y_dist, CX_SEC + R_OD + 0.2, y_dist, lw=1.2)
    cad_balloon(ax, CX_SEC + R_OD + 1.5, y_dist + 0.60, 'N3')
    cad_text(ax, CX_SEC + R_OD + 1.5, y_dist - 0.65, 'N3: WATER INLET\nDN 80 (L=17.25 kg/s)', sz=5.0, bold=True)
    
    # Header & Lateral manifold
    cad_rect(ax, CX_SEC - 0.20, y_dist - 0.20, 0.40, 0.40, lw=1.0, fill=True) # Central header
    cad_rect(ax, CX_SEC - R_ID + 0.25, y_dist - 0.10, 2 * R_ID - 0.50, 0.20, lw=0.9, fill=True) # Laterals
    # Distributor orifices & spray discharge arrows
    for dx in np.linspace(CX_SEC - R_ID + 0.40, CX_SEC + R_ID - 0.40, 7):
        cad_arrow(ax, dx, y_dist - 0.10, dx, y_dist - 0.45, lw=0.8, head_scale=7)
    cad_text(ax, CX_SEC, y_dist + 0.55, 'HEADER-LATERAL LIQUID DISTRIBUTOR\n(UNIFORM JET IRRIGATION > 60 PTS/m²)', sz=4.8, bold=True)
    
    # Wall wiper / redistributor ring
    cad_line(ax, CX_SEC - R_ID, y_dist - 0.40, CX_SEC - R_ID + 0.25, y_dist - 0.55, lw=1.0)
    cad_line(ax, CX_SEC + R_ID, y_dist - 0.40, CX_SEC + R_ID - 0.25, y_dist - 0.55, lw=1.0)
    
    # 8. Wire Mesh Demister (Mist Eliminator, Z = 8300.0)
    y_dem = y_at(Z_DEMISTER)
    dem_thk = 150.0 * SCALE # 0.60 cm
    cad_rect(ax, CX_SEC - R_ID, y_dem - dem_thk/2, 2 * R_ID, dem_thk, lw=1.0, fill=True)
    cad_hatch_rect(ax, CX_SEC - R_ID, y_dem - dem_thk/2, 2 * R_ID, dem_thk, pitch=0.18, angle=45, lw=0.4)
    cad_line(ax, CX_SEC - R_ID, y_dem - dem_thk/2, CX_SEC + R_ID, y_dem - dem_thk/2, lw=1.1)
    cad_line(ax, CX_SEC - R_ID, y_dem + dem_thk/2, CX_SEC + R_ID, y_dem + dem_thk/2, lw=1.1)
    cad_text(ax, CX_SEC, y_dem, 'KNITTED WIRE MESH DEMISTER (150 mm THK)\nSS316L / PTFE COMPOSITE', sz=5.0, bold=True, bg='white')
    
    # 9. Top Head & Overhead Vent Nozzle N6 (DN50 Class 150)
    y_top_apex = y_at(Z_TOP_APEX)
    cad_arc(ax, CX_SEC, y_top_tan, 2 * R_OD, 2 * (y_top_apex - y_top_tan), theta1=0, theta2=180, lw=1.1)
    cad_arc(ax, CX_SEC, y_top_tan, 2 * R_ID, 2 * (y_top_apex - y_top_tan - 0.08), theta1=0, theta2=180, lw=0.8)
    
    # Top Vent Nozzle N6
    y_vent = y_at(Z_VENT_FACE)
    cad_rect(ax, CX_SEC - 0.12, y_top_apex, 0.24, y_vent - y_top_apex, lw=0.9, fill=True)
    cad_flange(ax, CX_SEC, y_vent, orientation='V', length=0.55)
    cad_arrow(ax, CX_SEC, y_vent, CX_SEC, y_vent + 0.65, lw=1.2)
    cad_balloon(ax, CX_SEC - 0.50, y_vent + 0.40, 'N6')
    cad_text(ax, CX_SEC + 0.45, y_vent + 0.35, 'N6: TREATED GAS VENT\nDN 50 (y2=0.002, 90% REMOVAL)', sz=5.0, ha='left', bold=True)
    
    # Manways M1 & M2 on Section View
    # M1 (Lower Manway DN450 at Z = 3400.0)
    y_m1 = y_at(3400.0)
    cad_rect(ax, CX_SEC + R_OD, y_m1 - 0.45, 0.70, 0.90, lw=0.9, fill=True)
    cad_flange(ax, CX_SEC + R_OD + 0.70, y_m1, orientation='H', length=1.2)
    cad_rect(ax, CX_SEC + R_OD + 0.85, y_m1 - 0.60, 0.18, 1.20, lw=0.9, fill=True) # Blind flange
    cad_balloon(ax, CX_SEC + R_OD + 1.6, y_m1 + 0.60, 'M1')
    cad_text(ax, CX_SEC + R_OD + 1.4, y_m1 - 0.85, 'M1: LOWER MANWAY\nDN 450 CL 150 RF', sz=5.0, bold=True)
    
    # M2 (Upper Manway DN450 at Z = 8600.0)
    y_m2 = y_at(8600.0)
    cad_rect(ax, CX_SEC - R_OD - 0.70, y_m2 - 0.45, 0.70, 0.90, lw=0.9, fill=True)
    cad_flange(ax, CX_SEC - R_OD - 0.70, y_m2, orientation='H', length=1.2)
    cad_rect(ax, CX_SEC - R_OD - 0.88, y_m2 - 0.60, 0.18, 1.20, lw=0.9, fill=True) # Blind flange
    cad_balloon(ax, CX_SEC - R_OD - 1.6, y_m2 + 0.60, 'M2')
    cad_text(ax, CX_SEC - R_OD - 1.4, y_m2 - 0.85, 'M2: UPPER MANWAY\nDN 450 CL 150 RF', sz=5.0, bold=True)
    
    # Differential Pressure Taps N7 (below bed) & N8 (above bed)
    y_n7 = y_at(2900.0)
    y_n8 = y_at(7600.0)
    cad_rect(ax, CX_SEC - R_OD - 0.50, y_n7 - 0.10, 0.50, 0.20, lw=0.8, fill=True)
    cad_flange(ax, CX_SEC - R_OD - 0.50, y_n7, orientation='H', length=0.45)
    cad_balloon(ax, CX_SEC - R_OD - 0.95, y_n7, 'N7', radius=0.35, sz=5.2)
    cad_text(ax, CX_SEC - R_OD - 1.5, y_n7 - 0.35, 'N7: DP TAP (LO)', sz=4.8, bold=True)
    
    cad_rect(ax, CX_SEC - R_OD - 0.50, y_n8 - 0.10, 0.50, 0.20, lw=0.8, fill=True)
    cad_flange(ax, CX_SEC - R_OD - 0.50, y_n8, orientation='H', length=0.45)
    cad_balloon(ax, CX_SEC - R_OD - 0.95, y_n8, 'N8', radius=0.35, sz=5.2)
    cad_text(ax, CX_SEC - R_OD - 1.5, y_n8 + 0.35, 'N8: DP TAP (HI)', sz=4.8, bold=True)
    
    # ═════════════════════════════════════════════════════════════════════════
    # VIEW 2: EXTERIOR ELEVATION, ACCESS PLATFORMS & LADDER (CX = CX_EXT = 34.5)
    # ═════════════════════════════════════════════════════════════════════════
    
    # Centerline
    cad_line(ax, CX_EXT, y_at(Z_SUMP_OUT - 200), CX_EXT, y_at(Z_VENT_FACE + 250), lw=0.5, ls='-.', color=BK)
    cad_text(ax, CX_EXT, y_at(Z_VENT_FACE + 350), 'EXTERIOR ELEVATION & GA', sz=8.5, bold=True)
    cad_text(ax, CX_EXT, y_at(Z_VENT_FACE + 200), 'SCALE 1:25 METRIC', sz=6.5, bold=True)
    
    # Concrete Foundation Pedestal
    cad_rect(ax, CX_EXT - 2.8, Y_GND - 1.2, 5.6, 1.2, lw=1.2, fill=True, ec=BK)
    cad_hatch_rect(ax, CX_EXT - 2.8, Y_GND - 1.2, 5.6, 1.2, pitch=0.35, angle=-45, lw=0.4)
    cad_line(ax, CX_EXT - 3.5, Y_GND, CX_EXT + 3.5, Y_GND, lw=1.2)
    
    # Base Ring & Anchor Bolts
    cad_rect(ax, CX_EXT - 2.1, Y_GND, 4.2, (y_base - Y_GND), lw=1.0, fill=True)
    # 8 Anchor Bolt Chairs
    for ab_x in [CX_EXT - 1.8, CX_EXT - 1.1, CX_EXT + 1.1, CX_EXT + 1.8]:
        cad_rect(ax, ab_x - 0.15, Y_GND, 0.30, (y_base - Y_GND) + 0.25, lw=0.8, fill=True)
        cad_line(ax, ab_x, Y_GND - 0.6, ab_x, Y_GND + 0.4, lw=1.0) # Anchor stud
    
    # Skirt Outer Body
    cad_rect(ax, CX_EXT - R_OD, y_base, 2 * R_OD, y_skirt_top - y_base, lw=1.2, fill=True)
    # Skirt Access Opening Cover
    cad_circle(ax, CX_EXT, y_at(900.0), 0.80, lw=1.0, fill=True)
    for bp in np.linspace(0, 2*np.pi, 8, endpoint=False):
        cad_circle(ax, CX_EXT + 0.70*np.cos(bp), y_at(900.0) + 0.70*np.sin(bp), 0.05, fill=True)
    cad_text(ax, CX_EXT, y_at(900.0), 'MANHOLE\nCOVER', sz=4.8, bold=True)
    
    # Bottom Head Exterior Contour
    cad_arc(ax, CX_EXT, y_btm_tan, 2 * R_OD, 2 * (y_btm_tan - y_btm_apex), theta1=180, theta2=360, lw=1.2)
    
    # Column Outer Shell
    cad_rect(ax, CX_EXT - R_OD, y_btm_tan, 2 * R_OD, y_top_tan - y_btm_tan, lw=1.2, fill=True)
    # Circumferential weld girth seams
    for seam_z in [1800.0, 3600.0, 5400.0, 7200.0, 9000.0]:
        cad_line(ax, CX_EXT - R_OD, y_at(seam_z), CX_EXT + R_OD, y_at(seam_z), lw=0.6, ls='--')
    
    # Top Head Exterior Contour
    cad_arc(ax, CX_EXT, y_top_tan, 2 * R_OD, 2 * (y_top_apex - y_top_tan), theta1=0, theta2=180, lw=1.2)
    
    # Top Lifting Lugs (2x)
    for lug_x in [CX_EXT - R_ID + 0.2, CX_EXT + R_ID - 0.2]:
        cad_rect(ax, lug_x - 0.25, y_top_apex - 0.10, 0.50, 0.65, lw=1.0, fill=True)
        cad_circle(ax, lug_x, y_top_apex + 0.35, 0.12, lw=0.8, fill=True)
    cad_text(ax, CX_EXT, y_top_apex + 0.85, 'HEAVY-DUTY LIFTING LUGS (2X)', sz=5.0, bold=True)
    
    # Top Vent Flange
    cad_rect(ax, CX_EXT - 0.12, y_top_apex, 0.24, y_vent - y_top_apex, lw=0.9, fill=True)
    cad_flange(ax, CX_EXT, y_vent, orientation='V', length=0.55)
    
    # Grounding / Earthing Boss near base
    cad_rect(ax, CX_EXT + R_OD, y_at(300.0) - 0.10, 0.25, 0.20, lw=0.8, fill=True)
    cad_line(ax, CX_EXT + R_OD + 0.25, y_at(300.0), CX_EXT + R_OD + 0.65, y_at(300.0), lw=0.8)
    cad_line(ax, CX_EXT + R_OD + 0.65, y_at(300.0) - 0.15, CX_EXT + R_OD + 0.65, y_at(300.0) + 0.15, lw=0.8)
    cad_line(ax, CX_EXT + R_OD + 0.73, y_at(300.0) - 0.10, CX_EXT + R_OD + 0.73, y_at(300.0) + 0.10, lw=0.8)
    cad_line(ax, CX_EXT + R_OD + 0.81, y_at(300.0) - 0.05, CX_EXT + R_OD + 0.81, y_at(300.0) + 0.05, lw=0.8)
    cad_text(ax, CX_EXT + R_OD + 1.2, y_at(300.0), 'EARTHING BOSS', sz=4.8, ha='left', bold=True)
    
    # ASME Vessel Nameplate Bracket
    cad_rect(ax, CX_EXT - R_ID + 0.2, y_at(2000.0), 0.70, 0.45, lw=0.8, fill=True)
    cad_text(ax, CX_EXT - R_ID + 0.55, y_at(2000.0) + 0.22, 'ASME SEC VIII\nNAMEPLATE', sz=4.2, bold=True)
    
    # ── External Access Platforms & Caged Ladders ───────────────────────────
    # Platform 1 at EL +4200 (servicing M1 & Bed Inspection)
    y_p1 = y_at(4200.0)
    cad_rect(ax, CX_EXT - 3.2, y_p1 - 0.20, 6.4, 0.20, lw=1.1, fill=True) # Grating floor
    cad_hatch_rect(ax, CX_EXT - 3.2, y_p1 - 0.20, 6.4, 0.20, pitch=0.15, lw=0.4)
    # Handrails (1000 mm high = 4.0 cm canvas)
    h_rail = 1000.0 * SCALE
    cad_line(ax, CX_EXT - 3.2, y_p1, CX_EXT - 3.2, y_p1 + h_rail, lw=1.0)
    cad_line(ax, CX_EXT + 3.2, y_p1, CX_EXT + 3.2, y_p1 + h_rail, lw=1.0)
    cad_line(ax, CX_EXT - 3.2, y_p1 + h_rail, CX_EXT + 3.2, y_p1 + h_rail, lw=1.0) # Top handrail
    cad_line(ax, CX_EXT - 3.2, y_p1 + h_rail/2, CX_EXT + 3.2, y_p1 + h_rail/2, lw=0.7) # Mid rail
    cad_rect(ax, CX_EXT - 3.2, y_p1, 6.4, 0.12, lw=0.8, fill=True) # Toe plate
    # Platform Cantilever Brackets
    cad_line(ax, CX_EXT - 3.2, y_p1 - 0.20, CX_EXT - R_OD, y_p1 - 0.90, lw=1.1)
    cad_line(ax, CX_EXT + 3.2, y_p1 - 0.20, CX_EXT + R_OD, y_p1 - 0.90, lw=1.1)
    cad_text(ax, CX_EXT + 3.4, y_p1 + h_rail/2, 'PLATFORM 1 (EL +4.200 m)\nACCESS TO M1 & N7', sz=4.8, ha='left', bold=True)
    
    # Platform 2 at EL +7500 (servicing M2, Distributor, Demister)
    y_p2 = y_at(7500.0)
    cad_rect(ax, CX_EXT - 3.2, y_p2 - 0.20, 6.4, 0.20, lw=1.1, fill=True)
    cad_hatch_rect(ax, CX_EXT - 3.2, y_p2 - 0.20, 6.4, 0.20, pitch=0.15, lw=0.4)
    cad_line(ax, CX_EXT - 3.2, y_p2, CX_EXT - 3.2, y_p2 + h_rail, lw=1.0)
    cad_line(ax, CX_EXT + 3.2, y_p2, CX_EXT + 3.2, y_p2 + h_rail, lw=1.0)
    cad_line(ax, CX_EXT - 3.2, y_p2 + h_rail, CX_EXT + 3.2, y_p2 + h_rail, lw=1.0)
    cad_line(ax, CX_EXT - 3.2, y_p2 + h_rail/2, CX_EXT + 3.2, y_p2 + h_rail/2, lw=0.7)
    cad_rect(ax, CX_EXT - 3.2, y_p2, 6.4, 0.12, lw=0.8, fill=True)
    cad_line(ax, CX_EXT - 3.2, y_p2 - 0.20, CX_EXT - R_OD, y_p2 - 0.90, lw=1.1)
    cad_line(ax, CX_EXT + 3.2, y_p2 - 0.20, CX_EXT + R_OD, y_p2 - 0.90, lw=1.1)
    cad_text(ax, CX_EXT + 3.4, y_p2 + h_rail/2, 'PLATFORM 2 (EL +7.500 m)\nACCESS TO M2 & DISTRIBUTOR', sz=4.8, ha='left', bold=True)
    
    # Vertical Caged Ladder (Left side of exterior view: X = CX_EXT - 2.5)
    lx = CX_EXT - 2.5
    # Ladder stringers
    cad_line(ax, lx - 0.20, Y_GND, lx - 0.20, y_p2, lw=0.9)
    cad_line(ax, lx + 0.20, Y_GND, lx + 0.20, y_p2, lw=0.9)
    # Ladder rungs (300 mm spacing)
    for r_z in np.arange(300.0, 7500.0, 300.0):
        cad_line(ax, lx - 0.20, y_at(r_z), lx + 0.20, y_at(r_z), lw=0.6)
    # Safety Cage Hoops (starting at 2.2 m above ground)
    for c_z in np.arange(2200.0, 7500.0, 600.0):
        cad_arc(ax, lx, y_at(c_z), 0.70, 0.25, theta1=0, theta2=180, lw=0.8)
    cad_line(ax, lx - 0.35, y_at(2200.0), lx - 0.35, y_p2, lw=0.7)
    cad_line(ax, lx + 0.35, y_at(2200.0), lx + 0.35, y_p2, lw=0.7)
    cad_text(ax, lx - 0.60, y_at(2500.0), 'CAGED SAFETY\nLADDER', sz=4.8, ha='right', bold=True)
    
    # ═════════════════════════════════════════════════════════════════════════
    # DIMENSIONING STRINGS (CAD STANDARD CHAIN & BASELINE)
    # ═════════════════════════════════════════════════════════════════════════
    
    # Left Elevation Dimensions (Overall & Internal Zones)
    dim_x1 = 7.5
    dim_x2 = 5.5
    
    # Chain Dimensions (Zone heights)
    cad_dim_v(ax, dim_x1, y_at(Z_GND), y_at(Z_SKIRT_TOP), 'SKIRT 1800')
    cad_dim_v(ax, dim_x1, y_at(Z_SKIRT_TOP), y_at(Z_GRID), 'GAS SPACE 1200')
    cad_dim_v(ax, dim_x1, y_at(Z_GRID), y_at(Z_BED_TOP), 'PACKED BED 4500 (CALCULATED)')
    cad_dim_v(ax, dim_x1, y_at(Z_BED_TOP), y_at(Z_TOP_TAN), 'TOP SPACE 1500')
    
    # Total Height Dimension
    cad_dim_v(ax, dim_x2, y_at(Z_GND), y_at(Z_VENT_FACE), 'TOTAL HEIGHT O.A. 9625 mm', text_offset=-0.65)
    
    # Diameters
    cad_dim_h(ax, CX_SEC - R_ID, CX_SEC + R_ID, y_grid + 2.0, 'ID 750 mm (CALCULATED)')
    cad_dim_h(ax, CX_SEC - 2.1, CX_SEC + 2.1, Y_GND - 0.6, 'BASE RING OD 1050 mm')
    cad_dim_h(ax, CX_EXT - 3.2, CX_EXT + 3.2, y_p1 - 0.5, 'PLATFORM OD 1800 mm')
    
    # Elevation Reference Markers on right side of section
    elev_x = 24.0
    elev_data = [
        (Z_VENT_FACE, '+9.625 m (VENT FLANGE FACE)'),
        (Z_TOP_TAN,   '+9.000 m (TOP TAN LINE)'),
        (Z_DEMISTER,  '+8.300 m (DEMISTER C/L)'),
        (Z_DIST_PIPE, '+7.800 m (DISTRIBUTOR C/L)'),
        (Z_BED_TOP,   '+7.500 m (PACKING BED TOP)'),
        (Z_GRID,      '+3.000 m (PACKING SUPPORT GRID)'),
        (Z_GAS_IN,    '+2.400 m (GAS INLET N1 C/L)'),
        (Z_SKIRT_TOP, '+1.800 m (BOTTOM TAN LINE)'),
        (Z_GND,       '±0.000 m (FINISHED GROUND LEVEL)'),
    ]
    for z_val, el_txt in elev_data:
        ey = y_at(z_val)
        cad_line(ax, CX_SEC + R_OD, ey, elev_x, ey, lw=0.4, ls=':')
        cad_arrow(ax, elev_x - 0.6, ey, elev_x, ey, lw=0.8, head_scale=6)
        cad_text(ax, elev_x + 0.15, ey, f'EL {el_txt}', sz=4.8, ha='left', bold=True)
    
    # ═════════════════════════════════════════════════════════════════════════
    # ENGINEERING TABLES & NOTES (RIGHT PANEL: X = 48.5 to 81.5)
    # ═════════════════════════════════════════════════════════════════════════
    
    # TABLE 1: PROCESS DESIGN SPECIFICATION & EQUIPMENT DATA
    T1_X = 48.5
    T1_Y = 37.0
    t1_headers = ['PARAMETER / SPECIFICATION', 'CALCULATED VALUE', 'DESIGN BASIS & REMARKS']
    t1_widths  = [10.5, 7.5, 14.5]
    t1_rows = [
        ['Equipment Tag & Service',     'C-101 (Absorber)',     'Counter-Current Packed Absorption Column'],
        ['Solute Gas / Carrier Gas',     'Bromine (Br2) / Air',  'Dilute Toxic Gas Neutralization / Recovery'],
        ['Gas Volumetric Flow (QG)',    '0.25 m³/s (900 m³/h)', 'Ideal Gas at Operating T and P'],
        ['Operating Pressure & Temp',   '803 mmHg (107.06 kPa)','25.0 °C (298.15 K) Ambient Condition'],
        ['Inlet Br2 Concentration (y1)','2.0 mol% (0.0200)',   'Raw Off-Gas from Halogenation Header'],
        ['Outlet Br2 Concentration (y2)','0.2 mol% (0.0020)',   '90.0% Br2 Recovery / Emission Compliance'],
        ['Absorbent Solvent / Liquid',  'Process Water (H2O)', 'Density = 997 kg/m³, M = 0.018015 kg/mol'],
        ['Henry\'s Constant (Hcp)',      '7.20 x 10⁻³ mol/m³Pa', 'm = ρL / (ML * Hcp * P) = 71.8'],
        ['Equilibrium Line Relationship','y* = 71.8 x',         'Linear Dilute Henry\'s Law Regime'],
        ['Minimum Liquid Rate (Lmin)',  '683.7 mol/s',          'x1* = y1 / m = 2.79 x 10⁻⁴'],
        ['Actual Liquid Rate (L = 1.4Lmin)','957.2 mol/s (17.25 kg/s)','62.10 t/h Scrubbing Circulation Rate'],
        ['Operating Line Slope (L/G)',  '90.50',                'y = 0.002 + 90.5 x'],
        ['Absorption Factor (A)',       '0.794',                'A = m*G / L  (Sub-critical Absorption)'],
        ['Number of Transfer Units (NOG)','5.09 Transfer Units', 'Colburn Logarithmic Transfer Equation'],
        ['Selected Packing Type & Size','25-mm Ceramic Raschig','ap=190 m²/m³, ε=0.74, Fp=100 m⁻¹'],
        ['Packing Bulk Density',        '680 kg/m³',            'Dry Bed Mass Mp ≈ 1.22 tonnes'],
        ['Column Internal Diameter (D)','750 mm (0.75 m)',      'Calc: 0.73 m at 70% Flooding; Sel: 0.75 m'],
        ['Overall Height of Transfer Unit','HOG = 0.84 m',      'HG = 0.17 m, HL = 0.83 m (Onda Correl.)'],
        ['Required Packed Height (Z)',  '4500 mm (4.50 m)',     'Calculated: 4.30 m | Selected Margin: 4.50 m'],
        ['Active Packing Volume (Vp)',  '1.79 m³ (1.99 m³ sel)','Dry Packing Gravity Load: 11.9 kN'],
        ['Packing Support Operating Load','16.1 kN (26.4 kN fl)','Dry Packing + Liquid Holdup + Grid Weight'],
    ]
    cad_draw_table(ax, T1_X, T1_Y, t1_headers, t1_rows, t1_widths, row_h=0.46,
                   title='TABLE 1 — PROCESS DESIGN SPECIFICATIONS & SIZING DATA (CALCULATED)', sz=5.0)
    
    # TABLE 2: NOZZLE SCHEDULE (ASME B16.5 CLASS 150 RF)
    T2_X = 48.5
    T2_Y = 22.5
    t2_headers = ['NOZ', 'SERVICE DESCRIPTION', 'SIZE (DN)', 'RATING', 'FACING', 'ELEVATION']
    t2_widths  = [1.6, 11.2, 3.2, 3.4, 3.6, 9.5]
    t2_rows = [
        ['N1', 'Feed Gas Mixture Inlet', 'DN 150 (6")', 'CL 150', 'RF Flange', 'EL +2.400 m (Gas Space)'],
        ['N2', 'Gas Sampling Connection', 'DN 40 (1.5")', 'CL 150', 'RF Flange', 'EL +2.600 m (Inlet Neck)'],
        ['N3', 'Water Absorbent Inlet',  'DN 80 (3")',   'CL 150', 'RF Flange', 'EL +7.800 m (Distributor)'],
        ['N4', 'Rich Liquor Sump Outlet','DN 80 (3")',   'CL 150', 'RF Flange', 'EL -0.300 m (Btm Head Sump)'],
        ['N5', 'Column Shell Drain',     'DN 40 (1.5")', 'CL 150', 'RF Flange', 'EL -0.300 m (Lowest Point)'],
        ['N6', 'Treated Overhead Gas Vent','DN 50 (2")', 'CL 150', 'RF Flange', 'EL +9.625 m (Top Apex)'],
        ['N7', 'Bed Differential Press (Lo)','DN 50 (2")', 'CL 150', 'RF Flange', 'EL +2.900 m (Below Grid)'],
        ['N8', 'Bed Differential Press (Hi)','DN 50 (2")', 'CL 150', 'RF Flange', 'EL +7.600 m (Above Bed)'],
        ['N9', 'Gas Temperature Thermowell','DN 40 (1.5")', 'CL 150', 'RF Flange', 'EL +2.200 m (Inlet Gas)'],
        ['N10','Liquid Level Instrument Taps','DN 50 (2")', 'CL 150', 'RF Flange', 'EL +0.300 / +1.500 m'],
        ['N11','Demister Flush Spray In', 'DN 40 (1.5")', 'CL 150', 'RF Flange', 'EL +8.500 m (Above Mesh)'],
        ['M1', 'Lower Packing Access Manway','DN 450 (18")','CL 150', 'RF Flange', 'EL +3.400 m (Grid Level)'],
        ['M2', 'Upper Distributor Manway',  'DN 450 (18")','CL 150', 'RF Flange', 'EL +8.600 m (Top Internals)'],
    ]
    cad_draw_table(ax, T2_X, T2_Y, t2_headers, t2_rows, t2_widths, row_h=0.45,
                   title='TABLE 2 — PRELIMINARY NOZZLE SCHEDULE (ASME B16.5 CLASS 150 RF)', sz=5.0)
    
    # ENGINEERING DESIGN CRITERIA & CODE COMPLIANCE NOTES
    N_X = 48.5
    N_Y = 7.2
    cad_rect(ax, N_X, N_Y, 32.5, 14.2, lw=1.2, fill=True)
    cad_text(ax, N_X + 16.25, N_Y + 13.7, 'ENGINEERING DESIGN CRITERIA & TECHNICAL NOTES', sz=7.5, bold=True)
    
    notes = [
        "1. DESIGN STATUS CLASSIFICATION (STRICT ENGINEERING COMPLIANCE):",
        "   (A) CALCULATED PROCESS PARAMETERS: COLUMN ID 750 mm, PACKED BED HEIGHT 4500 mm, BED VOLUME 1.79 m3,",
        "       PACKING MASS 1.22 t, WATER FLOW 17.25 kg/s (62.1 t/h), DRY PACKING LOAD 11.9 kN, N_OG 5.09, H_OG 0.84 m.",
        "   (B) PRELIMINARY CAD ASSUMPTIONS: SHELL THICKNESS (8 mm), 2:1 ELLIPSOIDAL HEADS, SKIRT BASE RING OD 1050 mm,",
        "       PLATFORMS, CAGED LADDER, NOZZLE PROJECTIONS, AND PIPING LAYOUTS PROPORTIONED FOR GENERAL ARRANGEMENT.",
        "   (C) TO BE MECHANICALLY VERIFIED: EXACT SHELL/HEAD THICKNESS PER ASME SEC VIII DIV 1 (UG-27/UG-32) UNDER",
        "       INTERNAL PRESSURE (107.06 kPa) + FULL VACUUM CONTINGENCY; SEISMIC/WIND STABILITY PER IS 875 / ASCE 7.",
        "2. CORROSION & METALLURGY SPECIFICATION:",
        "   - WET BROMINE AND HYDROBROMIC ACID (Br2 + H2O <-> HBr + HOBr) ARE SEVERELY CORROSIVE TO STANDARD CARBON STEEL.",
        "   - COLUMN SHELL MOC: SA-516 GR. 70 WITH SOLID 3.0 mm PVDF (FLUOROPOLYMER) LINER OR TITANIUM GR. 2 CLADDING.",
        "   - NOZZLE NECKS & FLANGE WETTED PARTS: PTFE/PVDF LINED OR TITANIUM GR. 2 LINED PER ASTM B363 / B381.",
        "   - PACKING: 25-mm CHEMICAL STONEWARE / PORCELAIN CERAMIC RASCHIG RINGS (ZERO CORROSION IN WET HALOGENS).",
        "3. MECHANICAL FABRICATION & TESTING STANDARDS:",
        "   - VESSEL FABRICATION CODE: ASME SECTION VIII DIVISION 1 (EDITION 2023), JOINT CATEGORY A & B, FULL RT (UW-11).",
        "   - HYDROSTATIC LEAK TEST: 1.5x DESIGN PRESSURE WITH CHLORIDE-FREE DEMINERALIZED WATER; HOLD TIME >= 2 HOURS.",
        "   - PNEUMATIC SPARK TESTING OF PVDF LINER AT 15 kV PER NACE SP0188 TO ENSURE 100% PINHOLE-FREE INTEGRITY.",
        "4. CIVIL & FOUNDATION INTERFACE:",
        "   - 8x M24 ANCHOR BOLTS (SA-193 B7) EMBEDDED 450 mm IN REINFORCED CONCRETE PEDESTAL (M25 GRADE).",
        "   - BASEPLATE TOP GROUTED WITH NON-SHRINK HIGH-STRENGTH EPOXY GROUT (25 mm MINIMUM THICKNESS).",
    ]
    for n_idx, n_line in enumerate(notes):
        bold_flag = ("1." in n_line or "2." in n_line or "3." in n_line or "4." in n_line)
        cad_text(ax, N_X + 0.40, N_Y + 13.0 - n_idx * 0.58, n_line, sz=4.8, ha='left', bold=bold_flag)
    
    # ── Title Block ─────────────────────────────────────────────────────────
    draw_title_block(
        ax,
        dwg_title='PACKED-BED ABSORBER (C-101) — GENERAL ARRANGEMENT & ELEVATION SECTIONAL CAD',
        dwg_no='PEDD-PBA-01',
        rev='00',
        sheet_no='01 OF 05',
        scale='1:25 METRIC / PROPORTIONED',
        equip_desc='PACKED ABSORPTION COLUMN (C-101) — 750 MM ID x 4500 MM BED',
        duty_desc='0.25 M³/S GAS (2 MOL% Br2) | 90% RECOVERY | WATER: 17.25 KG/S'
    )
    
    # ── Save Outputs ────────────────────────────────────────────────────────
    OUT_DIR = r'd:\GAMES\zercxes\CAD_Engineering_Drawings'
    pdf_path = os.path.join(OUT_DIR, '01_Packed_Bed_Absorber_General_Arrangement_CAD.pdf')
    png_path = os.path.join(OUT_DIR, '01_Packed_Bed_Absorber_General_Arrangement_CAD.png')
    
    fig.savefig(pdf_path, dpi=300, bbox_inches='tight', facecolor='white')
    fig.savefig(png_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"SUCCESS: DWG-01 generated at {pdf_path} and {png_path}")

if __name__ == '__main__':
    generate_dwg01()
