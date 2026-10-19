"""
A4 OPTIMIZED: DWG-03 DISTILLATION COLUMN GENERAL ARRANGEMENT & ELEVATION
ETHANOL DISTILLATION SYSTEM (C-201) — 700 kmol/h FEED (7 mol% EtOH)
STUDENT: SOURISH SENAPATI | ROLL: 002310301035 | DATE: 01/09/2026
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
    cad_dim_h, cad_dim_v, cad_balloon, cad_flange, cad_hatch_rect,
    cad_draw_table_a4, W, H, BK, GREY
)

def generate_ethanol_dwg03(out_pdf, out_png):
    fig, ax = create_a4_canvas()
    draw_a4_border(ax)
    
    SUB_INFO = 'ETHANOL DISTILLATION (C-201)  |  700 kmol/h FEED (7 mol% EtOH)  |  ID 1.20 m, R=3.0  |  ASME SEC VIII / TEMA'
    draw_a4_title_block(ax, 'DISTILLATION COLUMN GENERAL ARRANGEMENT & ELEVATION',
                        'JU/ChE/ED/DWG-03', scale='1:120 METRIC', date='01 / 09 / 2026', sub_info=SUB_INFO)
    
    # Scale: 1 cm canvas = 1200 mm real (1:120 Metric)
    SCALE = 1.0 / 1200.0
    R_ID = 1200.0 / 2.0 * SCALE   # 0.50 cm (1.0 cm diameter)
    THK  = 0.05
    R_OD = R_ID + THK
    
    Y_GND = 3.6
    y_at = lambda z_mm: Y_GND + z_mm * SCALE
    
    # Key Elevations (mm)
    Z_SKIRT = 2500.0
    Z_SUMP_LOW = 3000.0
    Z_REB_RET = 4200.0
    Z_STRIP_BOT = 4700.0
    Z_FEED_TRAY = 7850.0   # Tray 11 (Transition between stripping and rectifying)
    Z_RECT_TOP = 15500.0   # Tray 1 (Top tray)
    Z_DEMISTER = 16300.0
    Z_TOP_TAN = 16700.0
    Z_OVERHEAD = 17500.0
    
    CX_SEC = 4.2   # Sectional Elevation Centerline
    CX_EXT = 9.8   # Exterior Elevation Centerline
    
    # ═════════════════════════════════════════════════════════════════════════
    # VIEW 1: SECTIONAL ELEVATION A-A (CX = 4.2)
    # ═════════════════════════════════════════════════════════════════════════
    cad_line(ax, CX_SEC, Y_GND - 0.4, CX_SEC, y_at(Z_OVERHEAD) + 0.5, lw=0.35, ls='-.')
    cad_text(ax, CX_SEC, y_at(Z_OVERHEAD) + 0.75, 'SECTIONAL ELEVATION A-A', sz=5.8, bold=True)
    cad_text(ax, CX_SEC, y_at(Z_OVERHEAD) + 0.42, 'SCALE 1:120 METRIC', sz=4.4, bold=True)
    
    # Concrete Foundation
    cad_rect(ax, CX_SEC - 1.1, Y_GND - 0.35, 2.2, 0.35, lw=0.75, fill=True)
    cad_hatch_rect(ax, CX_SEC - 1.1, Y_GND - 0.35, 2.2, 0.35, pitch=0.18, angle=-45, lw=0.25)
    cad_line(ax, CX_SEC - 1.4, Y_GND, CX_SEC + 1.4, Y_GND, lw=0.85)
    
    # Skirt & Base Ring
    cad_rect(ax, CX_SEC - 0.78, Y_GND, 1.56, 0.10, lw=0.75, fill=True)
    cad_rect(ax, CX_SEC - R_OD, Y_GND + 0.10, 2 * R_OD, y_at(Z_SKIRT) - Y_GND - 0.10, lw=0.75)
    cad_circle(ax, CX_SEC, y_at(1200.0), 0.24, lw=0.60, fill=True)
    cad_text(ax, CX_SEC, y_at(1200.0), 'DN500\nACCESS', sz=3.0, bold=True)
    
    # Bottom Head & Bottoms Outlet N5
    cad_arc(ax, CX_SEC, y_at(Z_SKIRT), 2 * R_OD, 0.55, theta1=180, theta2=360, lw=0.85)
    cad_arc(ax, CX_SEC, y_at(Z_SKIRT), 2 * R_ID, 0.45, theta1=180, theta2=360, lw=0.55)
    cad_rect(ax, CX_SEC - 0.08, y_at(Z_SKIRT - 350), 0.16, 0.35, lw=0.65, fill=True)
    cad_flange(ax, CX_SEC, y_at(Z_SKIRT - 350), orientation='V', length=0.32)
    cad_balloon(ax, CX_SEC - 0.38, y_at(Z_SKIRT - 350), 'N5', radius=0.20, sz=3.8)
    
    # Reboiler Liquid Feed Nozzle N6 (Sump side draw)
    y_n6 = y_at(3200.0)
    cad_rect(ax, CX_SEC - R_OD - 0.40, y_n6 - 0.09, 0.40, 0.18, lw=0.65, fill=True)
    cad_flange(ax, CX_SEC - R_OD - 0.40, y_n6, orientation='H', length=0.36)
    cad_balloon(ax, CX_SEC - R_OD - 0.68, y_n6, 'N6', radius=0.20, sz=3.8)
    
    # Shell Walls
    cad_line(ax, CX_SEC - R_OD, y_at(Z_SKIRT), CX_SEC - R_OD, y_at(Z_TOP_TAN), lw=0.9)
    cad_line(ax, CX_SEC + R_OD, y_at(Z_SKIRT), CX_SEC + R_OD, y_at(Z_TOP_TAN), lw=0.9)
    cad_line(ax, CX_SEC - R_ID, y_at(Z_SKIRT), CX_SEC - R_ID, y_at(Z_TOP_TAN), lw=0.45)
    cad_line(ax, CX_SEC + R_ID, y_at(Z_SKIRT), CX_SEC + R_ID, y_at(Z_TOP_TAN), lw=0.45)
    
    # Reboiler Vapor Return Nozzle N4
    y_n4 = y_at(Z_REB_RET)
    cad_rect(ax, CX_SEC - R_OD - 0.42, y_n4 - 0.10, 0.42, 0.20, lw=0.65, fill=True)
    cad_flange(ax, CX_SEC - R_OD - 0.42, y_n4, orientation='H', length=0.38)
    cad_balloon(ax, CX_SEC - R_OD - 0.70, y_n4, 'N4', radius=0.20, sz=3.8)
    
    # Internal Trays (24 Sieve Trays schematic representation)
    # Trays spaced 450 mm real = 450 * SCALE = 0.375 cm on canvas
    tray_y_list = np.linspace(y_at(Z_STRIP_BOT), y_at(Z_RECT_TOP), 24)
    for idx, yt in enumerate(tray_y_list):
        is_feed = (idx == 13) # Tray 11 from top (index 13 from bottom)
        lw_tr = 0.85 if is_feed else 0.40
        col_tr = '#008800' if is_feed else BK
        # Crossflow alternating downcomers
        if idx % 2 == 0:
            cad_line(ax, CX_SEC - R_ID + 0.08, yt, CX_SEC + R_ID - 0.18, yt, lw=lw_tr, color=col_tr)
            cad_line(ax, CX_SEC + R_ID - 0.18, yt, CX_SEC + R_ID - 0.18, yt - 0.25, lw=0.40) # Downcomer apron
        else:
            cad_line(ax, CX_SEC - R_ID + 0.18, yt, CX_SEC + R_ID - 0.08, yt, lw=lw_tr, color=col_tr)
            cad_line(ax, CX_SEC - R_ID + 0.18, yt, CX_SEC - R_ID + 0.18, yt - 0.25, lw=0.40)
            
    # Feed Inlet Nozzle N3
    y_n3 = tray_y_list[13]
    cad_rect(ax, CX_SEC - R_OD - 0.35, y_n3 - 0.08, 0.35, 0.16, lw=0.65, fill=True)
    cad_flange(ax, CX_SEC - R_OD - 0.35, y_n3, orientation='H', length=0.32)
    cad_balloon(ax, CX_SEC - R_OD - 0.62, y_n3, 'N3', radius=0.20, sz=3.8)
    cad_text(ax, CX_SEC - R_OD - 0.65, y_n3 - 0.28, 'FEED TRAY\n(STAGE 11)', sz=3.4, bold=True, color='#008800')
    
    # Reflux Return Nozzle N2
    y_n2 = tray_y_list[-1] + 0.20
    cad_rect(ax, CX_SEC + R_OD, y_n2 - 0.08, 0.35, 0.16, lw=0.65, fill=True)
    cad_flange(ax, CX_SEC + R_OD + 0.35, y_n2, orientation='H', length=0.32)
    cad_balloon(ax, CX_SEC + R_OD + 0.62, y_n2, 'N2', radius=0.20, sz=3.8)
    
    # Wire Mesh Demister Pad
    y_dem = y_at(Z_DEMISTER)
    cad_rect(ax, CX_SEC - R_ID + 0.05, y_dem - 0.10, 2*R_ID - 0.10, 0.20, lw=0.60, fill=True)
    cad_hatch_rect(ax, CX_SEC - R_ID + 0.05, y_dem - 0.10, 2*R_ID - 0.10, 0.20, pitch=0.08, lw=0.25)
    cad_text(ax, CX_SEC + R_OD + 0.40, y_dem, 'DEMISTER PAD (150 mm)', sz=3.2, bold=True, ha='left')
    
    # Top Head & Overhead Vapor Outlet N1
    cad_arc(ax, CX_SEC, y_at(Z_TOP_TAN), 2 * R_OD, 0.55, theta1=0, theta2=180, lw=0.85)
    cad_arc(ax, CX_SEC, y_at(Z_TOP_TAN), 2 * R_ID, 0.45, theta1=0, theta2=180, lw=0.55)
    cad_rect(ax, CX_SEC - 0.10, y_at(Z_TOP_TAN + 280), 0.20, 0.40, lw=0.65, fill=True)
    cad_flange(ax, CX_SEC, y_at(Z_TOP_TAN + 680), orientation='V', length=0.42)
    cad_balloon(ax, CX_SEC - 0.40, y_at(Z_TOP_TAN + 680), 'N1', radius=0.20, sz=3.8)
    
    # ═════════════════════════════════════════════════════════════════════════
    # VIEW 2: EXTERIOR ELEVATION & STRUCTURAL PLATFORMS (CX = 9.8)
    # ═════════════════════════════════════════════════════════════════════════
    cad_line(ax, CX_EXT, Y_GND - 0.4, CX_EXT, y_at(Z_OVERHEAD) + 0.5, lw=0.35, ls='-.')
    cad_text(ax, CX_EXT, y_at(Z_OVERHEAD) + 0.75, 'EXTERIOR ELEVATION', sz=5.8, bold=True)
    cad_text(ax, CX_EXT, y_at(Z_OVERHEAD) + 0.42, 'SCALE 1:120 METRIC', sz=4.4, bold=True)
    
    # Concrete Foundation
    cad_rect(ax, CX_EXT - 1.1, Y_GND - 0.35, 2.2, 0.35, lw=0.75, fill=True)
    cad_hatch_rect(ax, CX_EXT - 1.1, Y_GND - 0.35, 2.2, 0.35, pitch=0.18, angle=-45, lw=0.25)
    cad_line(ax, CX_EXT - 1.4, Y_GND, CX_EXT + 1.4, Y_GND, lw=0.85)
    
    # Skirt & Anchor Bolts
    cad_rect(ax, CX_EXT - 0.78, Y_GND, 1.56, 0.10, lw=0.75, fill=True)
    cad_rect(ax, CX_EXT - R_OD, Y_GND + 0.10, 2 * R_OD, y_at(Z_SKIRT) - Y_GND - 0.10, lw=0.75)
    for bx in [CX_EXT - 0.65, CX_EXT + 0.65]:
        cad_line(ax, bx, Y_GND, bx, Y_GND + 0.22, lw=0.7)
        cad_rect(ax, bx - 0.04, Y_GND + 0.12, 0.08, 0.06, fill=True)
    
    # Exterior Vessel Body with Insulation
    cad_rect(ax, CX_EXT - R_OD, y_at(Z_SKIRT), 2 * R_OD, y_at(Z_TOP_TAN) - y_at(Z_SKIRT), lw=0.9)
    cad_arc(ax, CX_EXT, y_at(Z_TOP_TAN), 2 * R_OD, 0.55, theta1=0, theta2=180, lw=0.85)
    cad_arc(ax, CX_EXT, y_at(Z_SKIRT), 2 * R_OD, 0.55, theta1=180, theta2=360, lw=0.85)
    
    # Exterior Manways M1, M2, M3, M4 (DN500)
    for my_elev, m_tag in [(4000.0, 'M1'), (7850.0, 'M2'), (11800.0, 'M3'), (15800.0, 'M4')]:
        ym = y_at(my_elev)
        cad_circle(ax, CX_EXT, ym, 0.22, lw=0.65, fill=True)
        cad_circle(ax, CX_EXT, ym, 0.14, lw=0.45)
        cad_text(ax, CX_EXT + R_OD + 0.35, ym, f'{m_tag} DN500', sz=3.4, bold=True, ha='left')
    
    # Structural Platforms & Handrails (3 Levels: EL +6.5m, EL +11.5m, EL +16.2m)
    for p_elev in [6500.0, 11500.0, 16200.0]:
        yp = y_at(p_elev)
        # Platform Deck
        cad_line(ax, CX_EXT - 1.25, yp, CX_EXT + 1.25, yp, lw=0.85)
        # Handrail (1.0m high = 1000 * SCALE = 0.83 cm)
        cad_line(ax, CX_EXT - 1.25, yp + 0.70, CX_EXT - 0.65, yp + 0.70, lw=0.55)
        cad_line(ax, CX_EXT + 0.65, yp + 0.70, CX_EXT + 1.25, yp + 0.70, lw=0.55)
        cad_line(ax, CX_EXT - 1.25, yp, CX_EXT - 1.25, yp + 0.70, lw=0.55)
        cad_line(ax, CX_EXT + 1.25, yp, CX_EXT + 1.25, yp + 0.70, lw=0.55)
        # Diagonal Knee Braces
        cad_line(ax, CX_EXT - 1.25, yp, CX_EXT - R_OD, yp - 0.55, lw=0.60)
        cad_line(ax, CX_EXT + 1.25, yp, CX_EXT + R_OD, yp - 0.55, lw=0.60)
        
    # Safety Ladder & Cages (on the right)
    LX = CX_EXT + 1.15
    cad_line(ax, LX, y_at(Z_SKIRT), LX, y_at(16200.0), lw=0.6)
    cad_line(ax, LX + 0.15, y_at(Z_SKIRT), LX + 0.15, y_at(16200.0), lw=0.6)
    for ry in np.arange(y_at(Z_SKIRT), y_at(16200.0), 0.25):
        cad_line(ax, LX, ry, LX + 0.15, ry, lw=0.40)
    
    # ═════════════════════════════════════════════════════════════════════════
    # DIMENSION CALLOUTS
    # ═════════════════════════════════════════════════════════════════════════
    # Horizontal diameter
    cad_dim_h(ax, CX_SEC - R_ID, CX_SEC + R_ID, y_at(Z_STRIP_BOT) - 0.35, 'ID 1200', sz=4.0)
    # Vertical overall elevations
    cad_dim_v(ax, 2.4, Y_GND, y_at(Z_SKIRT), '2500 SKIRT', sz=3.8, text_offset=0.20)
    cad_dim_v(ax, 2.4, y_at(Z_SKIRT), y_at(Z_TOP_TAN), '14200 T-T', sz=3.8, text_offset=0.20)
    cad_dim_v(ax, 1.8, Y_GND, y_at(Z_OVERHEAD), '17500 TOTAL ELEV', sz=4.2, text_offset=0.25)
    
    # ═════════════════════════════════════════════════════════════════════════
    # RIGHT HALF: NOZZLE SCHEDULE & MECHANICAL SPECIFICATIONS
    # ═════════════════════════════════════════════════════════════════════════
    RX_BASE = 14.8
    
    # 1. Nozzle Schedule Table
    noz_headers = ['NOZ', 'DN (mm)', 'RATING', 'FACING', 'SERVICE / DESTINATION']
    noz_rows = [
        ['N1', '250 (10")', 'CL 150', 'RF', 'Overhead Vapor to Condenser (E-102)'],
        ['N2', '100 (4")', 'CL 150', 'RF', 'Reflux Return to Tray 1'],
        ['N3', '80 (3")', 'CL 150', 'RF', 'Preheated Feed to Tray 11 (Bubble Pt)'],
        ['N4', '300 (12")', 'CL 150', 'RF', 'Reboiler Vapor Return from E-103'],
        ['N5', '80 (3")', 'CL 150', 'RF', 'Bottoms Liquid Draw to Heat Exchanger'],
        ['N6', '300 (12")', 'CL 150', 'RF', 'Reboiler Liquid Feed to E-103'],
        ['M1-M4', '500 (20")', 'CL 150', 'RF', 'Manways (Sump, Feed, Mid, Top)'],
        ['PSV-1', '100 (4")', 'CL 150', 'RF', 'Overpressure Safety Relief to Flare'],
        ['VENT', '50 (2")', 'CL 150', 'RF', 'Nitrogen Purge / Startup Vent'],
        ['DRAIN', '50 (2")', 'CL 150', 'RF', 'Column Bottom Drain / Cleanout'],
    ]
    noz_col_w = [1.2, 1.8, 1.6, 1.4, 7.6]
    cad_draw_table_a4(ax, RX_BASE, 11.10, noz_headers, noz_rows, noz_col_w,
                      row_h=0.32, title='TABLE 1: NOZZLE & MANWAY SCHEDULE (ASME B16.5 CLASS 150 RF)',
                      title_sz=4.6, sz=3.8)
    
    # 2. Mechanical Design Parameters Table
    mec_headers = ['PARAMETER', 'VALUE', 'UNIT', 'STANDARD / REMARKS']
    mec_rows = [
        ['Design Pressure', '0.35 / FV', 'MPa(g)', 'Full vacuum rated for steam-out'],
        ['Design Temperature', '130.0', 'C', 'Maximum boiling conditions'],
        ['Operating Pressure (Top)', '101.325', 'kPa(a)', 'Atmospheric rectification'],
        ['Operating Temperature (Top)', '78.15', 'C', 'Ethanol-water vapor temperature'],
        ['Operating Temperature (Bottom)', '99.8', 'C', 'Boiling water bottoms'],
        ['Vessel Inside Diameter', '1200', 'mm', 'Uniform ID throughout column'],
        ['Tangent-to-Tangent Height', '14,200', 'mm', 'Active tray section + disengagement'],
        ['Overall Vessel Height', '17,500', 'mm', 'Including skirt and ellipsoidal heads'],
        ['Shell / Head Material', 'SA-240 304L', '-', 'Corrosion resistant austenitic SS'],
        ['Head Geometry', '2:1 Ellipsoidal', '-', 'ASME BPVC Section VIII Division 1'],
        ['Corrosion Allowance', '1.5', 'mm', 'Organic chemical service'],
        ['Skirt Support Material', 'SA-516 Gr 70', '-', 'Structural carbon steel skirt'],
        ['Radiography Examination', '100 % (Full)', '-', 'Joint efficiency E = 1.0'],
        ['Hydrostatic Test Pressure', '0.525', 'MPa(g)', '1.5 x Design Pressure'],
    ]
    mec_col_w = [4.2, 2.2, 1.4, 5.8]
    cad_draw_table_a4(ax, RX_BASE, 4.40, mec_headers, mec_rows, mec_col_w,
                      row_h=0.32, title='TABLE 2: PRESSURE VESSEL SPECIFICATIONS (ASME SEC VIII DIV 1)',
                      title_sz=4.6, sz=3.8)
    
    # Save Outputs
    fig.savefig(out_pdf, format='pdf', dpi=300)
    fig.savefig(out_png, format='png', dpi=300)
    plt.close(fig)
    print(f"  [OK] DWG-03 generated: {os.path.basename(out_pdf)}")

if __name__ == '__main__':
    out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Ethanol_Water_Distillation_Drawings')
    os.makedirs(out_dir, exist_ok=True)
    generate_ethanol_dwg03(
        os.path.join(out_dir, '03_Ethanol_Column_General_Arrangement_Elevation_CAD.pdf'),
        os.path.join(out_dir, '03_Ethanol_Column_General_Arrangement_Elevation_CAD.png')
    )
