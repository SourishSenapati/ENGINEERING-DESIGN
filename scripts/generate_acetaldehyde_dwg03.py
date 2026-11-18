"""
A4 OPTIMIZED: DWG-03 ACETALDEHYDE COLUMN GENERAL ARRANGEMENT & ELEVATION
ACETALDEHYDE DISTILLATION SYSTEM (C-301) — 12000 kg/h FEED (50 wt% AcH, 60% VAPOUR)
STUDENT: SOURISH SENAPATI | ROLL NO.: 002310301035 | DATE: 17/11/2026
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

def generate_acetaldehyde_dwg03(out_pdf, out_png):
    fig, ax = create_a4_canvas()
    draw_a4_border(ax)
    
    SUB_INFO = 'ACETALDEHYDE DISTILLATION (C-301)  |  12000 kg/h FEED (50 wt% AcH)  |  ID 2.00 m, R=3.89  |  ASME SEC VIII / TEMA'
    draw_a4_title_block(ax, 'DISTILLATION COLUMN GENERAL ARRANGEMENT & ELEVATION',
                        'JU/ChE/ED/DWG-03', scale='1:150 METRIC', date='17 / 11 / 2026', sub_info=SUB_INFO)
    
    # Scale: 1 cm canvas = 1500 mm real (1:150 Metric)
    SCALE = 1.0 / 1500.0
    R_ID = 2000.0 / 2.0 * SCALE   # 0.667 cm (1.333 cm ID)
    THK  = 0.05
    R_OD = R_ID + THK
    
    Y_GND = 3.6
    y_at = lambda z_mm: Y_GND + z_mm * SCALE
    
    # Key Elevations (mm)
    Z_SKIRT = 3500.0
    Z_REB_RET = 5600.0
    Z_STRIP_BOT = 6200.0
    Z_FEED_TRAY = 12200.0   # Tray 13 (Feed tray transition)
    Z_RECT_TOP = 18200.0    # Tray 1 (Top tray)
    Z_DEMISTER = 19100.0
    Z_TOP_TAN = 19700.0
    Z_OVERHEAD = 20700.0
    
    CX_SEC = 4.2   # Sectional Elevation Centerline
    CX_EXT = 9.8   # Exterior Elevation Centerline
    
    # ═════════════════════════════════════════════════════════════════════════
    # VIEW 1: SECTIONAL ELEVATION A-A (CX = 4.2)
    # ═════════════════════════════════════════════════════════════════════════
    cad_line(ax, CX_SEC, Y_GND - 0.4, CX_SEC, y_at(Z_OVERHEAD) + 0.5, lw=0.35, ls='-.')
    cad_text(ax, CX_SEC, y_at(Z_OVERHEAD) + 0.75, 'SECTIONAL ELEVATION A-A', sz=5.8, bold=True)
    cad_text(ax, CX_SEC, y_at(Z_OVERHEAD) + 0.42, 'SCALE 1:150 METRIC', sz=4.4, bold=True)
    
    # Concrete Foundation
    cad_rect(ax, CX_SEC - 1.25, Y_GND - 0.35, 2.50, 0.35, lw=0.75, fill=True)
    cad_hatch_rect(ax, CX_SEC - 1.25, Y_GND - 0.35, 2.50, 0.35, pitch=0.18, angle=-45, lw=0.25)
    cad_line(ax, CX_SEC - 1.5, Y_GND, CX_SEC + 1.5, Y_GND, lw=0.85)
    
    # Skirt & Base Ring
    cad_rect(ax, CX_SEC - 0.90, Y_GND, 1.80, 0.10, lw=0.75, fill=True)
    cad_rect(ax, CX_SEC - R_OD, Y_GND + 0.10, 2 * R_OD, y_at(Z_SKIRT) - Y_GND - 0.10, lw=0.75)
    cad_circle(ax, CX_SEC, y_at(1800.0), 0.26, lw=0.60, fill=True)
    cad_text(ax, CX_SEC, y_at(1800.0), 'DN600\nACCESS', sz=3.0, bold=True)
    
    # Bottom Head & Bottoms Outlet N6
    cad_arc(ax, CX_SEC, y_at(Z_SKIRT), 2 * R_OD, 0.65, theta1=180, theta2=360, lw=0.85)
    cad_arc(ax, CX_SEC, y_at(Z_SKIRT), 2 * R_ID, 0.55, theta1=180, theta2=360, lw=0.55)
    cad_rect(ax, CX_SEC - 0.09, y_at(Z_SKIRT - 450), 0.18, 0.45, lw=0.65, fill=True)
    cad_flange(ax, CX_SEC, y_at(Z_SKIRT - 450), orientation='V', length=0.36)
    cad_balloon(ax, CX_SEC - 0.42, y_at(Z_SKIRT - 450), 'N6', radius=0.20, sz=3.8)
    # Vortex Breaker & Sump Liquid Level (NLL)
    cad_line(ax, CX_SEC - 0.14, y_at(Z_SKIRT) - 0.40, CX_SEC + 0.14, y_at(Z_SKIRT) - 0.40, lw=0.75)
    cad_line(ax, CX_SEC, y_at(Z_SKIRT) - 0.47, CX_SEC, y_at(Z_SKIRT) - 0.33, lw=0.75)
    y_nll = y_at(Z_SKIRT + 500)
    cad_line(ax, CX_SEC - R_ID + 0.08, y_nll, CX_SEC + R_ID - 0.08, y_nll, lw=0.45, ls='--', color='#0066cc')
    cad_text(ax, CX_SEC, y_nll + 0.12, 'NLL (50% SUMP)', sz=2.8, bold=True, color='#0066cc')
    
    # Reboiler Liquid Feed Nozzle N5 (Sump side draw)
    y_n5 = y_at(4200.0)
    cad_rect(ax, CX_SEC - R_OD - 0.40, y_n5 - 0.09, 0.40, 0.18, lw=0.65, fill=True)
    cad_flange(ax, CX_SEC - R_OD - 0.40, y_n5, orientation='H', length=0.36)
    cad_balloon(ax, CX_SEC - R_OD - 0.68, y_n5, 'N5', radius=0.20, sz=3.8)
    
    # Shell Walls
    cad_line(ax, CX_SEC - R_OD, y_at(Z_SKIRT), CX_SEC - R_OD, y_at(Z_TOP_TAN), lw=0.9)
    cad_line(ax, CX_SEC + R_OD, y_at(Z_SKIRT), CX_SEC + R_OD, y_at(Z_TOP_TAN), lw=0.9)
    cad_line(ax, CX_SEC - R_ID, y_at(Z_SKIRT), CX_SEC - R_ID, y_at(Z_TOP_TAN), lw=0.45)
    cad_line(ax, CX_SEC + R_ID, y_at(Z_SKIRT), CX_SEC + R_ID, y_at(Z_TOP_TAN), lw=0.45)
    
    # Reboiler Vapor Return Nozzle N4 & Internal Deflector Baffle
    y_n4 = y_at(Z_REB_RET)
    cad_rect(ax, CX_SEC - R_OD - 0.45, y_n4 - 0.11, 0.45, 0.22, lw=0.65, fill=True)
    cad_flange(ax, CX_SEC - R_OD - 0.45, y_n4, orientation='H', length=0.42)
    cad_balloon(ax, CX_SEC - R_OD - 0.72, y_n4, 'N4', radius=0.20, sz=3.8)
    cad_line(ax, CX_SEC - R_ID + 0.06, y_n4 + 0.18, CX_SEC - R_ID + 0.38, y_n4 + 0.32, lw=0.75)
    
    # Internal Trays (24 Sieve Trays schematic representation)
    tray_y_list = np.linspace(y_at(Z_STRIP_BOT), y_at(Z_RECT_TOP), 24)
    for idx, yt in enumerate(tray_y_list):
        is_feed = (idx == 11) # Tray 13 from top (index 11 from bottom: 24 total -> 0..11 stripping, 12..23 rectifying)
        lw_tr = 0.85 if is_feed else 0.40
        col_tr = '#008800' if is_feed else BK
        # Crossflow alternating downcomers
        if idx % 2 == 0:
            cad_line(ax, CX_SEC - R_ID + 0.10, yt, CX_SEC + R_ID - 0.22, yt, lw=lw_tr, color=col_tr)
            cad_line(ax, CX_SEC + R_ID - 0.22, yt, CX_SEC + R_ID - 0.22, yt - 0.22, lw=0.40) # Downcomer apron
        else:
            cad_line(ax, CX_SEC - R_ID + 0.22, yt, CX_SEC + R_ID - 0.10, yt, lw=lw_tr, color=col_tr)
            cad_line(ax, CX_SEC - R_ID + 0.22, yt, CX_SEC - R_ID + 0.22, yt - 0.22, lw=0.40)
            
    # Feed Inlet Nozzle N3
    y_n3 = tray_y_list[11]
    cad_rect(ax, CX_SEC - R_OD - 0.38, y_n3 - 0.08, 0.38, 0.16, lw=0.65, fill=True)
    cad_flange(ax, CX_SEC - R_OD - 0.38, y_n3, orientation='H', length=0.34)
    cad_balloon(ax, CX_SEC - R_OD - 0.65, y_n3, 'N3', radius=0.20, sz=3.8)
    cad_text(ax, CX_SEC + R_OD + 0.35, y_n3, 'FEED TRAY (STAGE 13)', sz=3.4, bold=True, color='#008800', ha='left')
    
    # Reflux Return Nozzle N2
    y_n2 = tray_y_list[-1] + 0.20
    cad_rect(ax, CX_SEC + R_OD, y_n2 - 0.08, 0.35, 0.16, lw=0.65, fill=True)
    cad_flange(ax, CX_SEC + R_OD + 0.35, y_n2, orientation='H', length=0.32)
    cad_balloon(ax, CX_SEC + R_OD + 0.62, y_n2, 'N2', radius=0.20, sz=3.8)
    
    # Wire Mesh Demister Pad
    y_dem = y_at(Z_DEMISTER)
    cad_rect(ax, CX_SEC - R_ID + 0.06, y_dem - 0.10, 2*R_ID - 0.12, 0.20, lw=0.60, fill=True)
    cad_hatch_rect(ax, CX_SEC - R_ID + 0.06, y_dem - 0.10, 2*R_ID - 0.12, 0.20, pitch=0.08, lw=0.25)
    cad_text(ax, CX_SEC + R_OD + 0.40, y_dem, 'DEMISTER PAD (150 mm)', sz=3.2, bold=True, ha='left')
    
    # Top Head & Overhead Vapor Outlet N1
    cad_arc(ax, CX_SEC, y_at(Z_TOP_TAN), 2 * R_OD, 0.65, theta1=0, theta2=180, lw=0.85)
    cad_arc(ax, CX_SEC, y_at(Z_TOP_TAN), 2 * R_ID, 0.55, theta1=0, theta2=180, lw=0.55)
    cad_rect(ax, CX_SEC - 0.12, y_at(Z_TOP_TAN + 300), 0.24, 0.42, lw=0.65, fill=True)
    cad_flange(ax, CX_SEC, y_at(Z_TOP_TAN + 720), orientation='V', length=0.48)
    cad_balloon(ax, CX_SEC - 0.45, y_at(Z_TOP_TAN + 720), 'N1', radius=0.20, sz=3.8)
    
    # ═════════════════════════════════════════════════════════════════════════
    # VIEW 2: EXTERIOR ELEVATION & STRUCTURAL PLATFORMS (CX = 9.8)
    # ═════════════════════════════════════════════════════════════════════════
    cad_line(ax, CX_EXT, Y_GND - 0.4, CX_EXT, y_at(Z_OVERHEAD) + 0.5, lw=0.35, ls='-.')
    cad_text(ax, CX_EXT, y_at(Z_OVERHEAD) + 0.75, 'EXTERIOR ELEVATION', sz=5.8, bold=True)
    cad_text(ax, CX_EXT, y_at(Z_OVERHEAD) + 0.42, 'SCALE 1:150 METRIC', sz=4.4, bold=True)
    
    # Concrete Foundation
    cad_rect(ax, CX_EXT - 1.25, Y_GND - 0.35, 2.50, 0.35, lw=0.75, fill=True)
    cad_hatch_rect(ax, CX_EXT - 1.25, Y_GND - 0.35, 2.50, 0.35, pitch=0.18, angle=-45, lw=0.25)
    cad_line(ax, CX_EXT - 1.5, Y_GND, CX_EXT + 1.5, Y_GND, lw=0.85)
    
    # Skirt & Anchor Bolts
    cad_rect(ax, CX_EXT - 0.90, Y_GND, 1.80, 0.10, lw=0.75, fill=True)
    cad_rect(ax, CX_EXT - R_OD, Y_GND + 0.10, 2 * R_OD, y_at(Z_SKIRT) - Y_GND - 0.10, lw=0.75)
    for bx in [CX_EXT - 0.75, CX_EXT + 0.75]:
        cad_line(ax, bx, Y_GND, bx, Y_GND + 0.22, lw=0.7)
        cad_rect(ax, bx - 0.04, Y_GND + 0.12, 0.08, 0.06, fill=True)
        
    # Exterior Vessel Body with Insulation
    cad_rect(ax, CX_EXT - R_OD, y_at(Z_SKIRT), 2 * R_OD, y_at(Z_TOP_TAN) - y_at(Z_SKIRT), lw=0.9)
    cad_arc(ax, CX_EXT, y_at(Z_TOP_TAN), 2 * R_OD, 0.65, theta1=0, theta2=180, lw=0.85)
    cad_arc(ax, CX_EXT, y_at(Z_SKIRT), 2 * R_OD, 0.65, theta1=180, theta2=360, lw=0.85)
    
    # Exterior Manways M1, M2, M3, M4 (DN600)
    for my_elev, m_tag in [(5000.0, 'M1'), (10500.0, 'M2'), (15500.0, 'M3'), (19000.0, 'M4')]:
        ym = y_at(my_elev)
        cad_circle(ax, CX_EXT, ym, 0.24, lw=0.65, fill=True)
        cad_circle(ax, CX_EXT, ym, 0.15, lw=0.45)
        cad_text(ax, CX_EXT + R_OD + 0.35, ym, f'{m_tag} DN600', sz=3.4, bold=True, ha='left')
        
    # Structural Platforms & Handrails (4 Levels: EL +4.5m, EL +9.5m, EL +14.5m, EL +19.5m)
    for p_elev in [4500.0, 9500.0, 14500.0, 19500.0]:
        yp = y_at(p_elev)
        # Platform Deck
        cad_line(ax, CX_EXT - 1.45, yp, CX_EXT + 1.45, yp, lw=0.85)
        # Handrail (1.0m high = 1000 * SCALE = 0.67 cm)
        cad_line(ax, CX_EXT - 1.45, yp + 0.67, CX_EXT - 0.80, yp + 0.67, lw=0.55)
        cad_line(ax, CX_EXT + 0.80, yp + 0.67, CX_EXT + 1.45, yp + 0.67, lw=0.55)
        cad_line(ax, CX_EXT - 1.45, yp, CX_EXT - 1.45, yp + 0.67, lw=0.55)
        cad_line(ax, CX_EXT + 1.45, yp, CX_EXT + 1.45, yp + 0.67, lw=0.55)
        # Diagonal Knee Braces
        cad_line(ax, CX_EXT - 1.45, yp, CX_EXT - R_OD, yp - 0.50, lw=0.60)
        cad_line(ax, CX_EXT + 1.45, yp, CX_EXT + R_OD, yp - 0.50, lw=0.60)
        
    # Safety Ladder & Cages (on the right)
    LX = CX_EXT + 1.35
    cad_line(ax, LX, y_at(Z_SKIRT), LX, y_at(19500.0), lw=0.6)
    cad_line(ax, LX + 0.15, y_at(Z_SKIRT), LX + 0.15, y_at(19500.0), lw=0.6)
    for ry in np.arange(y_at(Z_SKIRT), y_at(19500.0), 0.25):
        cad_line(ax, LX, ry, LX + 0.15, ry, lw=0.40)
        
    # ═════════════════════════════════════════════════════════════════════════
    # DIMENSION CALLOUTS
    # ═════════════════════════════════════════════════════════════════════════
    cad_dim_h(ax, CX_SEC - R_ID, CX_SEC + R_ID, y_at(Z_STRIP_BOT) - 0.35, 'ID 2000', sz=4.0)
    cad_dim_v(ax, 2.3, Y_GND, y_at(Z_SKIRT), '3500 SKIRT', sz=3.8, text_offset=0.20)
    cad_dim_v(ax, 2.3, y_at(Z_SKIRT), y_at(Z_TOP_TAN), '16200 T-T', sz=3.8, text_offset=0.20)
    cad_dim_v(ax, 1.7, Y_GND, y_at(Z_OVERHEAD), '20700 TOTAL ELEV', sz=4.2, text_offset=0.25)
    
    # ═════════════════════════════════════════════════════════════════════════
    # RIGHT HALF: NOZZLE SCHEDULE & MECHANICAL SPECIFICATIONS
    # ═════════════════════════════════════════════════════════════════════════
    RX_BASE = 14.8
    
    # 1. Nozzle Schedule Table
    noz_headers = ['NOZ', 'DN (mm)', 'RATING', 'FACING', 'SERVICE / DESTINATION']
    noz_rows = [
        ['N1', '350 (14")', 'CL 150', 'RF', 'Overhead Vapour to Condenser (E-303)'],
        ['N2', '150 (6")', 'CL 150', 'RF', 'Reflux Return to Tray 1 (Liquid)'],
        ['N3', '150 (6")', 'CL 150', 'RF', 'Feed Inlet to Tray 13 (60% Vapour)'],
        ['N4', '400 (16")', 'CL 150', 'RF', 'Reboiler Vapour Return from E-302'],
        ['N5', '250 (10")', 'CL 150', 'RF', 'Reboiler Liquid Draw to E-302'],
        ['N6', '100 (4")', 'CL 150', 'RF', 'Bottoms Product Draw to Cooler (E-305)'],
        ['M1-M4', '600 (24")', 'CL 150', 'RF', 'Manways with Davit Arms (4 Levels)'],
        ['PSV-1', '100 (4")', 'CL 150', 'RF', 'Safety Relief Valve to Flare Header'],
        ['VENT', '50 (2")', 'CL 150', 'RF', 'Nitrogen Purge & Maintenance Vent'],
        ['DRAIN', '50 (2")', 'CL 150', 'RF', 'Column Bottoms Sump Drain / Flush'],
    ]
    noz_col_w = [1.2, 1.8, 1.6, 1.4, 7.6]
    cad_draw_table_a4(ax, RX_BASE, 11.10, noz_headers, noz_rows, noz_col_w,
                      row_h=0.32, title='TABLE 1: NOZZLE & MANWAY SCHEDULE (ASME B16.5 CLASS 150 RF)',
                      title_sz=4.6, sz=3.8)
    
    # 2. Mechanical Design Parameters Table
    mec_headers = ['PARAMETER', 'VALUE', 'UNIT', 'STANDARD / REMARKS']
    mec_rows = [
        ['Design Pressure', '0.35 / FV', 'MPa(g)', 'Full vacuum rated for steam-out / purge'],
        ['Design Temperature', '120.0', 'C', 'Maximum upset reboiler conditions'],
        ['Operating Pressure (Top)', '105.0', 'kPa(a)', 'Low-pressure rectification train'],
        ['Operating Temperature (Top)', '20.8', 'C', 'Dew point of 97 wt% Acetaldehyde'],
        ['Operating Temperature (Bottom)', '33.8', 'C', 'Bubble point of stripped PO bottoms'],
        ['Vessel Inside Diameter', '2000', 'mm', 'Uniform ID throughout column shell'],
        ['Tangent-to-Tangent Height', '16,200', 'mm', 'Active tray section + disengagement zones'],
        ['Overall Vessel Height', '20,700', 'mm', 'Including skirt support and heads'],
        ['Shell / Head Material', 'SA-516 Gr 70', '-', 'Carbon steel + 3 mm SS316L cladding'],
        ['Head Geometry', '2:1 Ellipsoidal', '-', 'ASME BPVC Section VIII Division 1'],
        ['Corrosion Allowance', '3.0', 'mm', 'Volatile organic oxide service'],
        ['Skirt Support Material', 'SA-516 Gr 70', '-', 'Cylindrical structural skirt with base ring'],
        ['Radiography Examination', '100 % (Full)', '-', 'Joint efficiency E = 1.0 (UW-11(a))'],
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
    out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Acetaldehyde_PropyleneOxide_Distillation_Drawings')
    os.makedirs(out_dir, exist_ok=True)
    generate_acetaldehyde_dwg03(
        os.path.join(out_dir, '03_Acetaldehyde_Column_General_Arrangement_Elevation_CAD.pdf'),
        os.path.join(out_dir, '03_Acetaldehyde_Column_General_Arrangement_Elevation_CAD.png')
    )
