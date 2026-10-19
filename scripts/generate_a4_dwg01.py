"""
A4 OPTIMIZED: DWG-01 GENERAL ARRANGEMENT & ELEVATION SECTIONAL CAD
PACKED-BED ABSORBER (C-101) — 750 mm ID x 4500 mm BED
STUDENT: SOURISH SENAPATI | ROLL: 002310301035 | DATE: 29/09/2026
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

def generate_a4_dwg01(out_pdf, out_png):
    fig, ax = create_a4_canvas()
    draw_a4_border(ax)
    
    # Scale: 1 cm canvas = 640 mm real (1:64 Metric)
    SCALE = 1.0 / 640.0
    R_ID = 750.0 / 2.0 * SCALE   # 0.586 cm
    THK  = 0.05
    R_OD = R_ID + THK
    
    Y_GND = 3.6
    y_at = lambda z_mm: Y_GND + z_mm * SCALE
    
    Z_SKIRT = 1800.0
    Z_GAS_IN = 2400.0
    Z_GRID = 3000.0
    Z_BED_TOP = 7500.0
    Z_DIST = 7800.0
    Z_DEM = 8300.0
    Z_TOP_TAN = 9000.0
    Z_TOP_APEX = 9187.5
    Z_VENT = 9625.0
    
    CX_SEC = 5.4   # Sectional Elevation Centerline
    CX_EXT = 11.6  # Exterior Elevation Centerline
    
    # ═════════════════════════════════════════════════════════════════════════
    # VIEW 1: SECTIONAL ELEVATION A-A (CX = 5.4)
    # ═════════════════════════════════════════════════════════════════════════
    cad_line(ax, CX_SEC, Y_GND - 0.4, CX_SEC, y_at(Z_VENT) + 0.5, lw=0.35, ls='-.')
    cad_text(ax, CX_SEC, y_at(Z_VENT) + 0.80, 'SECTIONAL ELEVATION A-A', sz=6.2, bold=True)
    cad_text(ax, CX_SEC, y_at(Z_VENT) + 0.42, 'SCALE 1:50 METRIC', sz=4.8, bold=True)
    
    # Concrete Foundation
    cad_rect(ax, CX_SEC - 1.1, Y_GND - 0.35, 2.2, 0.35, lw=0.75, fill=True)
    cad_hatch_rect(ax, CX_SEC - 1.1, Y_GND - 0.35, 2.2, 0.35, pitch=0.16, angle=-45, lw=0.25)
    cad_line(ax, CX_SEC - 1.4, Y_GND, CX_SEC + 1.4, Y_GND, lw=0.85)
    
    # Skirt & Base Ring
    cad_rect(ax, CX_SEC - 0.82, Y_GND, 1.64, 0.10, lw=0.75, fill=True)
    cad_rect(ax, CX_SEC - R_OD, Y_GND + 0.10, 2 * R_OD, y_at(Z_SKIRT) - Y_GND - 0.10, lw=0.75)
    cad_circle(ax, CX_SEC, y_at(900.0), 0.28, lw=0.65, fill=True)
    cad_text(ax, CX_SEC, y_at(900.0), 'DN400', sz=3.6, bold=True)
    
    # Bottom Head & Sump Outlet N4
    cad_arc(ax, CX_SEC, y_at(Z_SKIRT), 2 * R_OD, 0.55, theta1=180, theta2=360, lw=0.85)
    cad_arc(ax, CX_SEC, y_at(Z_SKIRT), 2 * R_ID, 0.45, theta1=180, theta2=360, lw=0.55)
    cad_rect(ax, CX_SEC - 0.07, y_at(Z_SKIRT - 480), 0.14, 0.45, lw=0.65, fill=True)
    cad_flange(ax, CX_SEC, y_at(Z_SKIRT - 480), orientation='V', length=0.32)
    cad_balloon(ax, CX_SEC - 0.32, y_at(Z_SKIRT - 480), 'N4', radius=0.20, sz=4.0)
    
    # Shell Walls
    cad_line(ax, CX_SEC - R_OD, y_at(Z_SKIRT), CX_SEC - R_OD, y_at(Z_TOP_TAN), lw=0.9)
    cad_line(ax, CX_SEC + R_OD, y_at(Z_SKIRT), CX_SEC + R_OD, y_at(Z_TOP_TAN), lw=0.9)
    cad_line(ax, CX_SEC - R_ID, y_at(Z_SKIRT), CX_SEC - R_ID, y_at(Z_TOP_TAN), lw=0.45)
    cad_line(ax, CX_SEC + R_ID, y_at(Z_SKIRT), CX_SEC + R_ID, y_at(Z_TOP_TAN), lw=0.45)
    
    # Gas Inlet N1 & Deflector
    y_g = y_at(Z_GAS_IN)
    cad_rect(ax, CX_SEC - R_OD - 0.50, y_g - 0.10, 0.50, 0.20, lw=0.75, fill=True)
    cad_flange(ax, CX_SEC - R_OD - 0.50, y_g, orientation='H', length=0.40)
    cad_balloon(ax, CX_SEC - R_OD - 0.78, y_g + 0.25, 'N1', radius=0.20, sz=4.0)
    p_def = [(CX_SEC - 0.32, y_g - 0.10), (CX_SEC, y_g + 0.16), (CX_SEC + 0.32, y_g - 0.10)]
    ax.add_patch(Polygon(p_def, closed=False, ec=BK, lw=0.85, fill=False))
    
    # Support Grid
    y_grd = y_at(Z_GRID)
    cad_line(ax, CX_SEC - R_ID, y_grd, CX_SEC + R_ID, y_grd, lw=0.95)
    cad_line(ax, CX_SEC - R_ID, y_grd - 0.07, CX_SEC + R_ID, y_grd - 0.07, lw=0.95)
    cad_text(ax, CX_SEC, y_grd - 0.24, 'SUPPORT GRID', sz=3.6, bold=True)
    
    # Packed Bed (4500 mm depth)
    y_btop = y_at(Z_BED_TOP)
    h_b = y_btop - y_grd
    cad_rect(ax, CX_SEC - R_ID, y_grd, 2 * R_ID, h_b, lw=0.55, fill=True)
    cad_hatch_rect(ax, CX_SEC - R_ID, y_grd, 2 * R_ID, h_b, pitch=0.20, angle=45, lw=0.25, color=GREY)
    cad_hatch_rect(ax, CX_SEC - R_ID, y_grd, 2 * R_ID, h_b, pitch=0.20, angle=-45, lw=0.25, color=GREY)
    cad_text(ax, CX_SEC, y_grd + h_b/2,
             'PACKED BED\nZ = 4500 mm\n25-mm CERAMIC\nRASCHIG RINGS',
             sz=4.2, bold=True, bg='white')
    
    # Hold-Down Grid
    cad_line(ax, CX_SEC - R_ID, y_btop, CX_SEC + R_ID, y_btop, lw=0.85)
    
    # Liquid Distributor
    y_dst = y_at(Z_DIST)
    cad_rect(ax, CX_SEC + R_OD, y_dst - 0.07, 0.50, 0.14, lw=0.75, fill=True)
    cad_flange(ax, CX_SEC + R_OD + 0.50, y_dst, orientation='H', length=0.35)
    cad_balloon(ax, CX_SEC + R_OD + 0.78, y_dst + 0.22, 'N3', radius=0.20, sz=4.0)
    cad_line(ax, CX_SEC - R_ID + 0.1, y_dst, CX_SEC + R_ID - 0.1, y_dst, lw=0.85)
    for sx in np.linspace(CX_SEC - R_ID + 0.18, CX_SEC + R_ID - 0.18, 4):
        cad_arrow(ax, sx, y_dst, sx, y_dst - 0.20, lw=0.5, head_scale=4)
    
    # Demister
    y_dm = y_at(Z_DEM)
    cad_rect(ax, CX_SEC - R_ID, y_dm - 0.11, 2 * R_ID, 0.22, lw=0.75, fill=True)
    cad_hatch_rect(ax, CX_SEC - R_ID, y_dm - 0.11, 2 * R_ID, 0.22, pitch=0.09, lw=0.25)
    cad_text(ax, CX_SEC, y_dm, 'DEMISTER', sz=3.6, bold=True, bg='white')
    
    # Top Head & Vent N6
    cad_arc(ax, CX_SEC, y_at(Z_TOP_TAN), 2 * R_OD, 0.55, theta1=0, theta2=180, lw=0.85)
    cad_arc(ax, CX_SEC, y_at(Z_TOP_TAN), 2 * R_ID, 0.45, theta1=0, theta2=180, lw=0.55)
    y_vt = y_at(Z_VENT)
    cad_rect(ax, CX_SEC - 0.07, y_at(Z_TOP_APEX), 0.14, y_vt - y_at(Z_TOP_APEX), lw=0.65, fill=True)
    cad_flange(ax, CX_SEC, y_vt, orientation='V', length=0.32)
    cad_balloon(ax, CX_SEC - 0.32, y_vt + 0.22, 'N6', radius=0.20, sz=4.0)
    
    # Manways M1 & M2
    y_m1 = y_at(3400.0)
    cad_rect(ax, CX_SEC + R_OD, y_m1 - 0.18, 0.30, 0.36, lw=0.75, fill=True)
    cad_flange(ax, CX_SEC + R_OD + 0.30, y_m1, orientation='H', length=0.55)
    cad_balloon(ax, CX_SEC + R_OD + 0.72, y_m1, 'M1', radius=0.20, sz=4.0)
    
    y_m2 = y_at(8600.0)
    cad_rect(ax, CX_SEC - R_OD - 0.30, y_m2 - 0.18, 0.30, 0.36, lw=0.75, fill=True)
    cad_flange(ax, CX_SEC - R_OD - 0.30, y_m2, orientation='H', length=0.55)
    cad_balloon(ax, CX_SEC - R_OD - 0.72, y_m2, 'M2', radius=0.20, sz=4.0)
    
    # ═════════════════════════════════════════════════════════════════════════
    # VIEW 2: EXTERIOR ELEVATION & GA (CX = 11.6)
    # ═════════════════════════════════════════════════════════════════════════
    cad_line(ax, CX_EXT, Y_GND - 0.4, CX_EXT, y_at(Z_VENT) + 0.5, lw=0.35, ls='-.')
    cad_text(ax, CX_EXT, y_at(Z_VENT) + 0.80, 'EXTERIOR ELEVATION & GA', sz=6.2, bold=True)
    cad_text(ax, CX_EXT, y_at(Z_VENT) + 0.42, 'SCALE 1:50 METRIC', sz=4.8, bold=True)
    
    # Foundation & Skirt
    cad_rect(ax, CX_EXT - 1.1, Y_GND - 0.35, 2.2, 0.35, lw=0.75, fill=True)
    cad_hatch_rect(ax, CX_EXT - 1.1, Y_GND - 0.35, 2.2, 0.35, pitch=0.16, angle=-45, lw=0.25)
    cad_line(ax, CX_EXT - 1.4, Y_GND, CX_EXT + 1.4, Y_GND, lw=0.85)
    cad_rect(ax, CX_EXT - 0.82, Y_GND, 1.64, 0.10, lw=0.75, fill=True)
    cad_rect(ax, CX_EXT - R_OD, Y_GND + 0.10, 2 * R_OD, y_at(Z_SKIRT) - Y_GND - 0.10, lw=0.85, fill=True)
    cad_arc(ax, CX_EXT, y_at(Z_SKIRT), 2 * R_OD, 0.55, theta1=180, theta2=360, lw=0.85)
    
    # Shell Body
    cad_rect(ax, CX_EXT - R_OD, y_at(Z_SKIRT), 2 * R_OD, y_at(Z_TOP_TAN) - y_at(Z_SKIRT), lw=0.9, fill=True)
    cad_arc(ax, CX_EXT, y_at(Z_TOP_TAN), 2 * R_OD, 0.55, theta1=0, theta2=180, lw=0.85)
    
    # Platforms
    y_p1 = y_at(4200.0)
    cad_rect(ax, CX_EXT - 1.35, y_p1 - 0.07, 2.70, 0.07, lw=0.85, fill=True)
    cad_line(ax, CX_EXT - 1.35, y_p1, CX_EXT - 1.35, y_p1 + 0.70, lw=0.65)
    cad_line(ax, CX_EXT + 1.35, y_p1, CX_EXT + 1.35, y_p1 + 0.70, lw=0.65)
    cad_line(ax, CX_EXT - 1.35, y_p1 + 0.70, CX_EXT + 1.35, y_p1 + 0.70, lw=0.75)
    cad_text(ax, CX_EXT + 1.5, y_p1 + 0.30, 'PLATFORM 1\n(EL +4.2 m)', sz=3.8, ha='left', bold=True)
    
    y_p2 = y_at(7500.0)
    cad_rect(ax, CX_EXT - 1.35, y_p2 - 0.07, 2.70, 0.07, lw=0.85, fill=True)
    cad_line(ax, CX_EXT - 1.35, y_p2, CX_EXT - 1.35, y_p2 + 0.70, lw=0.65)
    cad_line(ax, CX_EXT + 1.35, y_p2, CX_EXT + 1.35, y_p2 + 0.70, lw=0.65)
    cad_line(ax, CX_EXT - 1.35, y_p2 + 0.70, CX_EXT + 1.35, y_p2 + 0.70, lw=0.75)
    cad_text(ax, CX_EXT + 1.5, y_p2 + 0.30, 'PLATFORM 2\n(EL +7.5 m)', sz=3.8, ha='left', bold=True)
    
    # Caged Ladder
    lad_x = CX_EXT - 1.05
    cad_line(ax, lad_x - 0.07, Y_GND, lad_x - 0.07, y_p2, lw=0.65)
    cad_line(ax, lad_x + 0.07, Y_GND, lad_x + 0.07, y_p2, lw=0.65)
    for rz in np.arange(450.0, 7500.0, 450.0):
        cad_line(ax, lad_x - 0.07, y_at(rz), lad_x + 0.07, y_at(rz), lw=0.40)
    for cz in np.arange(2200.0, 7500.0, 900.0):
        cad_arc(ax, lad_x, y_at(cz), 0.30, 0.10, theta1=0, theta2=180, lw=0.55)
    
    # Dimensions
    cad_dim_v(ax, 2.4, Y_GND, y_at(Z_SKIRT), '1800')
    cad_dim_v(ax, 2.4, y_at(Z_GRID), y_at(Z_BED_TOP), 'BED 4500')
    cad_dim_v(ax, 1.4, Y_GND, y_at(Z_VENT), 'HEIGHT 9625 mm', text_offset=0.0)
    cad_dim_h(ax, CX_SEC - R_ID, CX_SEC + R_ID, y_grd + 1.1, 'ID 750 mm')
    cad_dim_h(ax, CX_SEC - 0.82, CX_SEC + 0.82, Y_GND - 0.22, 'BASE OD 1050')
    
    # ═════════════════════════════════════════════════════════════════════════
    # RIGHT SIDE: STANDARD CAD TABLES & CONCISE GENERAL NOTES
    # ═════════════════════════════════════════════════════════════════════════
    
    # TABLE 1: VESSEL MECHANICAL DESIGN DATA
    T1_X = 15.0
    T1_Y = 11.2
    t1_headers = ['PARAMETER', 'VALUE', 'SPECIFICATION / BASIS']
    t1_widths  = [4.4, 3.8, 5.3]
    t1_rows = [
        ['Process Service',       'Wet Bromine Scrubbing', 'Absorption of 2.0% Br2 with Water'],
        ['Internal Diameter (ID)','750 mm ID (Ac=0.44 m2)', '70% Flooding Limit (vG = 0.599 m/s)'],
        ['Shell & Head Material', 'SA-516 Gr 70 Carbon St.', '8 mm Shell / Head TBD (Prelim CAD)'],
        ['Corrosion Barrier',     '3.0 mm Bonded PVDF',    '15 kV High-Voltage Spark Tested'],
        ['Design Press / Temp',   '1.50 bar g / 65 DEG C', 'Full Vacuum (-1.0 bar g) Rating'],
        ['Operating Press / Temp','1.07 bar a / 25 DEG C', 'Inlet Gas at P = 803 mmHg'],
        ['Inlet Gas Flow (QG)',   '0.25 m3/s (900 m3/h)',  'Inlet: 2.0 mol% -> Outlet: 0.20 mol%'],
        ['Absorbent Water (L)',   '17.25 kg/s (62.1 t/h)', 'Demineralized Water (L/G = 90.5)'],
        ['Packed Bed Depth (Z)',  '4500 mm (Vp = 1.79 m3)','25-mm Glazed Ceramic Raschig Rings'],
        ['Overall Column Height', '9625 mm (T/T: 7200 mm)','Ground to Top Vent Flange Face'],
        ['Operating / Flood Load','16.1 kN / 26.4 kN',     'Normal Service / Flooded Upset'],
    ]
    cad_draw_table_a4(ax, T1_X, T1_Y, t1_headers, t1_rows, t1_widths, row_h=0.38,
                      title='VESSEL MECHANICAL DESIGN & OPERATING CONDITIONS', sz=4.2)
    
    # TABLE 2: NOZZLE SCHEDULE
    T2_X = 15.0
    T2_Y = 7.3
    t2_headers = ['TAG', 'SERVICE DESCRIPTION', 'SIZE (DN)', 'RATING', 'FACING']
    t2_widths  = [1.1, 5.0, 2.5, 2.2, 2.7]
    t2_rows = [
        ['N1', 'Gas Inlet Mixture',     'DN 150 (6")', 'CL 150', 'RF Flange'],
        ['N3', 'Water Absorbent Inlet', 'DN 80 (3")',   'CL 150', 'RF Flange'],
        ['N4', 'Rich Liquor Outlet',    'DN 80 (3")',   'CL 150', 'RF Flange'],
        ['N5', 'Column Shell Drain',    'DN 40 (1.5")', 'CL 150', 'RF Flange'],
        ['N6', 'Treated Gas Vent',      'DN 50 (2")',   'CL 150', 'RF Flange'],
        ['M1', 'Lower Packing Access',  'DN 450 (18")', 'CL 150', 'RF Blind'],
        ['M2', 'Upper Internals Manway','DN 450 (18")', 'CL 150', 'RF Blind'],
    ]
    cad_draw_table_a4(ax, T2_X, T2_Y, t2_headers, t2_rows, t2_widths, row_h=0.38,
                      title='NOZZLE SCHEDULE (ASME B16.5 CLASS 150 RF)', sz=4.2)
    
    # GENERAL NOTES (CONCISE STANDARD CAD NOTES)
    N_X = 15.0
    N_Y = 3.4
    W_N = 13.5
    H_N = 3.5
    cad_rect(ax, N_X, N_Y, W_N, H_N, lw=0.85, fill=True)
    cad_text(ax, N_X + W_N/2, N_Y + H_N - 0.28, 'GENERAL ENGINEERING NOTES', sz=5.0, bold=True)
    cad_line(ax, N_X, N_Y + H_N - 0.52, N_X + W_N, N_Y + H_N - 0.52, lw=0.6)
    
    notes = [
        "1. ALL DIMENSIONS ARE IN MILLIMETERS UNLESS SPECIFIED OTHERWISE.",
        "2. DESIGN BASIS: PRELIMINARY MECHANICAL DESIGN — SUBJECT TO ASME SEC VIII DIV 1 VERIFICATION.",
        "3. PROCESS VALUES: COLUMN ID 750 mm, PACKED BED DEPTH 4500 mm (Vp = 1.79 m3).",
        "   PACKING MASS 1.22 t, WATER FLOW 17.25 kg/s, DRY GRAVITY LOAD 11.9 kN.",
        "4. PRELIMINARY CAD: SHELL THK 8 mm (PRELIM), HEAD THK TBD (PRELIM), SKIRT HT 1800 mm, BASE RING OD 1050 mm.",
        "5. MOC: SA-516 GR 70 WITH 3.0 mm BONDED PVDF LINER FOR WET BROMINE SERVICE.",
        "6. ANCHORAGE: 8x M24 ANCHOR BOLTS (SA-193 B7) EMBEDDED 450 mm IN CONCRETE.",
    ]
    for idx, nl in enumerate(notes):
        cad_text(ax, N_X + 0.35, N_Y + H_N - 0.88 - idx * 0.38, nl, sz=3.8, ha='left', bold=(idx in [0, 1, 2]))
    
    # Title Block
    draw_a4_title_block(
        ax,
        dwg_title='PACKED-BED ABSORBER (C-101) — GENERAL ARRANGEMENT & ELEVATION',
        dwg_no='PEDD-PBA-01',
        scale='1:50 METRIC'
    )
    
    fig.savefig(out_pdf, dpi=300, facecolor='white')
    fig.savefig(out_png, dpi=300, facecolor='white')
    plt.close(fig)
    print(f"SUCCESS: Clean A4 DWG-01 generated at {out_pdf}")

if __name__ == '__main__':
    out_dir = r'd:\GAMES\zercxes\CAD_Engineering_Drawings\Packed_Bed_Absorber_Drawings'
    os.makedirs(out_dir, exist_ok=True)
    p_pdf = os.path.join(out_dir, '01_Packed_Bed_Absorber_General_Arrangement_CAD.pdf')
    p_png = os.path.join(out_dir, '01_Packed_Bed_Absorber_General_Arrangement_CAD.png')
    generate_a4_dwg01(p_pdf, p_png)
