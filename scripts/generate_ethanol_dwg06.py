"""
A4 OPTIMIZED: DWG-06 REBOILER & CONDENSER DETAILS & 3D ISOMETRIC ASSEMBLY
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
    cad_dim_h, cad_dim_v, cad_flange, cad_hatch_rect,
    cad_draw_table_a4, W, H, BK, GREY
)

def generate_ethanol_dwg06(out_pdf, out_png):
    fig, ax = create_a4_canvas()
    draw_a4_border(ax)
    
    SUB_INFO = 'ETHANOL DISTILLATION (C-201)  |  700 kmol/h FEED (7 mol% EtOH)  |  ID 1.20 m, R=3.0  |  ASME SEC VIII / TEMA'
    draw_a4_title_block(ax, 'REBOILER & CONDENSER DETAILS & 3D ISOMETRIC ASSEMBLY',
                        'JU/ChE/ED/DWG-06', scale='AS NOTED', date='01 / 09 / 2026', sub_info=SUB_INFO)
    
    # Drawing Header
    cad_text(ax, W/2, H - 1.25, 'HEAT EXCHANGER FABRICATION DETAILS & 3D ISOMETRIC PLANT ASSEMBLY', sz=6.6, bold=True)
    cad_text(ax, W/2, H - 1.62, 'THERMOSIPHON REBOILER (TEMA BEM) | CONDENSER (TEMA AEL) | ISOMETRIC SPATIAL LAYOUT', sz=4.8, bold=False)
    
    # ═════════════════════════════════════════════════════════════════════════
    # VIEW 1: VERTICAL THERMOSIPHON REBOILER E-103 (TEMA BEM) - TOP LEFT
    # ═════════════════════════════════════════════════════════════════════════
    RX1, RY1 = 3.8, 13.6
    cad_text(ax, RX1, RY1 + 2.8, 'VIEW 1: REBOILER E-103 (TEMA BEM)', sz=5.2, bold=True)
    cad_text(ax, RX1, RY1 + 2.45, 'VERTICAL THERMOSIPHON | 3.24 MW', sz=3.8, bold=True)
    
    # Shell Dimensions: 0.9 cm wide x 3.6 cm tall (representing 500 mm ID x 2500 mm tube length)
    SW, SH = 0.90, 3.4
    cad_rect(ax, RX1 - SW/2, RY1 - SH/2, SW, SH, lw=0.85, fill=True)
    # Tubesheet Top & Bottom
    cad_rect(ax, RX1 - SW/2 - 0.12, RY1 + SH/2, SW + 0.24, 0.12, lw=0.75, fill=True)
    cad_rect(ax, RX1 - SW/2 - 0.12, RY1 - SH/2 - 0.12, SW + 0.24, 0.12, lw=0.75, fill=True)
    # Channel Heads (Bonnet Type B)
    cad_arc(ax, RX1, RY1 + SH/2 + 0.12, SW, 0.45, theta1=0, theta2=180, lw=0.85)
    cad_arc(ax, RX1, RY1 - SH/2 - 0.12, SW, 0.45, theta1=180, theta2=360, lw=0.85)
    
    # Tube bundle vertical lines (schematic)
    for tx in np.linspace(RX1 - SW/2 + 0.15, RX1 + SW/2 - 0.15, 5):
        cad_line(ax, tx, RY1 - SH/2, tx, RY1 + SH/2, lw=0.35, ls='--')
        
    # Segmental Baffles
    for idx, by in enumerate(np.linspace(RY1 - SH/2 + 0.5, RY1 + SH/2 - 0.5, 5)):
        if idx % 2 == 0:
            cad_line(ax, RX1 - SW/2, by, RX1 + SW/2 - 0.22, by, lw=0.6)
        else:
            cad_line(ax, RX1 - SW/2 + 0.22, by, RX1 + SW/2, by, lw=0.6)
            
    # Steam Inlet Nozzle (Shell side top)
    cad_rect(ax, RX1 - SW/2 - 0.35, RY1 + SH/2 - 0.5, 0.35, 0.18, lw=0.65, fill=True)
    cad_flange(ax, RX1 - SW/2 - 0.35, RY1 + SH/2 - 0.41, orientation='H', length=0.32)
    cad_text(ax, RX1 - SW/2 - 0.42, RY1 + SH/2 - 0.41, 'STEAM IN\nDN150', sz=3.2, bold=True, ha='right')
    
    # Condensate Drain Nozzle (Shell side bottom)
    cad_rect(ax, RX1 - SW/2 - 0.35, RY1 - SH/2 + 0.35, 0.35, 0.14, lw=0.65, fill=True)
    cad_flange(ax, RX1 - SW/2 - 0.35, RY1 - SH/2 + 0.42, orientation='H', length=0.28)
    cad_text(ax, RX1 - SW/2 - 0.42, RY1 - SH/2 + 0.42, 'CONDENSATE\nDN80', sz=3.2, bold=True, ha='right')
    
    # Bottom Liquid Feed Nozzle (Channel side bottom)
    cad_rect(ax, RX1 - 0.12, RY1 - SH/2 - 0.55, 0.24, 0.35, lw=0.65, fill=True)
    cad_flange(ax, RX1, RY1 - SH/2 - 0.55, orientation='V', length=0.40)
    cad_text(ax, RX1, RY1 - SH/2 - 0.75, 'LIQUID IN (DN300)\nFROM SUMP', sz=3.2, bold=True)
    
    # Top Vapor Return Nozzle (Channel side top)
    cad_rect(ax, RX1 - 0.12, RY1 + SH/2 + 0.35, 0.24, 0.35, lw=0.65, fill=True)
    cad_flange(ax, RX1, RY1 + SH/2 + 0.70, orientation='V', length=0.40)
    cad_text(ax, RX1, RY1 + SH/2 + 0.95, 'VAPOR OUT (DN300)\nTO COLUMN', sz=3.2, bold=True)
    
    # ═════════════════════════════════════════════════════════════════════════
    # VIEW 2: HORIZONTAL OVERHEAD CONDENSER E-102 (TEMA AEL) - BOTTOM LEFT
    # ═════════════════════════════════════════════════════════════════════════
    CX2, CY2 = 3.8, 6.4
    cad_text(ax, CX2, CY2 + 2.2, 'VIEW 2: CONDENSER E-102 (TEMA AEL)', sz=5.2, bold=True)
    cad_text(ax, CX2, CY2 + 1.85, 'HORIZONTAL SHELL & TUBE | 2.88 MW (CW)', sz=3.8, bold=True)
    
    # Shell Dimensions: 3.8 cm long x 1.0 cm diameter (representing 3000 mm tube length x 600 mm ID)
    CSW, CSH = 3.6, 1.0
    cad_rect(ax, CX2 - CSW/2, CY2 - CSH/2, CSW, CSH, lw=0.85, fill=True)
    # Tubesheet Left & Right
    cad_rect(ax, CX2 - CSW/2 - 0.12, CY2 - CSH/2 - 0.12, 0.12, CSH + 0.24, lw=0.75, fill=True)
    cad_rect(ax, CX2 + CSW/2, CY2 - CSH/2 - 0.12, 0.12, CSH + 0.24, lw=0.75, fill=True)
    # Channel Heads (Left: Dual-pass channel A; Right: Bonnet L)
    cad_rect(ax, CX2 - CSW/2 - 0.65, CY2 - CSH/2, 0.53, CSH, lw=0.85, fill=True)
    cad_line(ax, CX2 - CSW/2 - 0.65, CY2, CX2 - CSW/2 - 0.12, CY2, lw=0.7) # Pass partition plate
    cad_arc(ax, CX2 + CSW/2 + 0.12, CY2, 0.45, CSH, theta1=270, theta2=90, lw=0.85)
    
    # Tube bundle horizontal lines (schematic)
    for ty in [CY2 - 0.30, CY2 - 0.12, CY2 + 0.12, CY2 + 0.30]:
        cad_line(ax, CX2 - CSW/2, ty, CX2 + CSW/2, ty, lw=0.35, ls='--')
        
    # Vapor Inlet Dome Nozzle (Top of shell)
    cad_rect(ax, CX2 - 0.5, CY2 + CSH/2, 0.35, 0.35, lw=0.65, fill=True)
    cad_flange(ax, CX2 - 0.32, CY2 + CSH/2 + 0.35, orientation='V', length=0.42)
    cad_text(ax, CX2 - 0.32, CY2 + CSH/2 + 0.55, 'VAPOR IN (DN250)\nFROM COLUMN TOP', sz=3.2, bold=True)
    
    # Condensate Drain Nozzle (Bottom of shell)
    cad_rect(ax, CX2 + 0.5, CY2 - CSH/2 - 0.35, 0.22, 0.35, lw=0.65, fill=True)
    cad_flange(ax, CX2 + 0.61, CY2 - CSH/2 - 0.35, orientation='V', length=0.32)
    cad_text(ax, CX2 + 0.61, CY2 - CSH/2 - 0.55, 'CONDENSATE OUT (DN100)\nTO REFLUX DRUM', sz=3.2, bold=True)
    
    # Cooling water inlet & outlet on channel head
    cad_text(ax, CX2 - CSW/2 - 0.75, CY2 - 0.25, 'CW IN (DN150)', sz=3.2, bold=True, ha='right')
    cad_text(ax, CX2 - CSW/2 - 0.75, CY2 + 0.25, 'CW OUT (DN150)', sz=3.2, bold=True, ha='right')
    
    # ═════════════════════════════════════════════════════════════════════════
    # VIEW 3: 3D ISOMETRIC ASSEMBLY & PIPING SPATIAL LAYOUT (CENTER / RIGHT)
    # ═════════════════════════════════════════════════════════════════════════
    IX0, IY0 = 10.4, 4.2
    
    cad_text(ax, IX0 + 1.8, 17.0, 'VIEW 3: 3D ISOMETRIC PLANT ASSEMBLY & STRUCTURAL INTEGRATION', sz=5.5, bold=True)
    cad_text(ax, IX0 + 1.8, 16.65, 'AXONOMETRIC PERSPECTIVE VIEW SHOWING COLUMN, LOOP & SKID', sz=4.2, bold=True)
    
    # Axonometric projection angles: 30 deg left, 30 deg right
    ANG = np.radians(30)
    cos30 = np.cos(ANG)
    sin30 = np.sin(ANG)
    
    def to_iso(x, y, z):
        u = IX0 + (x - y) * cos30 * 0.70
        v = IY0 + (x + y) * sin30 * 0.70 + z * 0.72
        return u, v
    
    # 1. Concrete Foundation Pad in Isometric
    p_fnd = [to_iso(-2.0, -2.0, 0), to_iso(4.0, -2.0, 0), to_iso(4.0, 3.5, 0), to_iso(-2.0, 3.5, 0)]
    ax.add_patch(Polygon(p_fnd, closed=True, fc='#f0f0f0', ec=BK, lw=0.8, zorder=2))
    p_fnd_b = [to_iso(-2.0, -2.0, -0.4), to_iso(4.0, -2.0, -0.4), to_iso(4.0, -2.0, 0), to_iso(-2.0, -2.0, 0)]
    ax.add_patch(Polygon(p_fnd_b, closed=True, fc='#d0d0d0', ec=BK, lw=0.6, zorder=2))
    
    # 2. Distillation Column C-201 Cylinder in Isometric (Center at x=0, y=0)
    COL_R = 0.85
    # Base Skirt Ring
    cad_circle(ax, to_iso(0, 0, 0)[0], to_iso(0, 0, 0)[1], COL_R * 0.65, lw=0.85)
    # Column Body (from z=0.5 to z=13.5)
    u_c, v_c_bot = to_iso(0, 0, 0.5)
    _, v_c_top = to_iso(0, 0, 13.5)
    
    # Column Outline
    cad_line(ax, u_c - COL_R, v_c_bot, u_c - COL_R, v_c_top, lw=1.1)
    cad_line(ax, u_c + COL_R, v_c_bot, u_c + COL_R, v_c_top, lw=1.1)
    # Top and Bottom Ellipses
    ax.add_patch(Arc((u_c, v_c_top), 2*COL_R, COL_R * 0.6, theta1=0, theta2=360, ec=BK, lw=1.1, zorder=4))
    ax.add_patch(Arc((u_c, v_c_bot), 2*COL_R, COL_R * 0.6, theta1=180, theta2=360, ec=BK, lw=1.1, zorder=4))
    
    # Internal Tray Cutaway (Quarter cutaway displaying internal trays)
    cad_line(ax, u_c, v_c_bot + 1.2, u_c, v_c_top - 1.2, lw=0.6, ls='-.')
    for zi in np.linspace(2.5, 11.5, 10):
        ui, vi = to_iso(0, 0, zi)
        cad_line(ax, ui - COL_R*0.75, vi, ui + COL_R*0.75, vi, lw=0.45, color='#0044aa')
        
    cad_text(ax, u_c, v_c_top + 0.85, 'C-201 COLUMN\n(ID 1200 mm)', sz=4.2, bold=True)
    
    # 3. Thermosiphon Reboiler E-103 in Isometric (at x= -1.6, y= 0.8)
    ur, vr_bot = to_iso(-1.8, 0.5, 1.0)
    _, vr_top = to_iso(-1.8, 0.5, 4.2)
    cad_rect(ax, ur - 0.35, vr_bot, 0.70, vr_top - vr_bot, lw=0.85, fill=True)
    cad_text(ax, ur, vr_bot - 0.45, 'E-103 REBOILER', sz=3.4, bold=True)
    
    # Piping Sump to Reboiler
    cad_line(ax, u_c - COL_R, v_c_bot + 0.4, ur + 0.35, vr_bot + 0.4, lw=1.1, color='#aa0000')
    # Vapor Return from Reboiler to Column
    cad_line(ax, ur + 0.35, vr_top - 0.4, u_c - COL_R, v_c_bot + 2.2, lw=1.2, color='#aa0000')
    
    # 4. Elevated Overhead Condenser E-102 (at x= 2.4, y= -0.5, z= 12.0)
    uc, vc = to_iso(2.6, -0.6, 12.0)
    cad_rect(ax, uc - 0.9, vc - 0.3, 1.8, 0.6, lw=0.85, fill=True)
    cad_text(ax, uc, vc + 0.55, 'E-102 CONDENSER', sz=3.4, bold=True)
    
    # Overhead vapor pipe from column top to condenser
    cad_line(ax, u_c, v_c_top + 0.3, u_c + 0.8, v_c_top + 0.3, lw=1.1)
    cad_line(ax, u_c + 0.8, v_c_top + 0.3, uc - 0.9, vc, lw=1.1)
    
    # 5. Reflux Drum V-101 (at x= 2.6, y= -0.6, z= 8.5)
    uv, vv = to_iso(2.6, -0.6, 8.5)
    cad_rect(ax, uv - 0.6, vv - 0.28, 1.2, 0.56, lw=0.85, fill=True)
    cad_text(ax, uv, vv - 0.45, 'V-101 REFLUX DRUM', sz=3.4, bold=True)
    # Drain from Condenser to Reflux Drum
    cad_line(ax, uc + 0.4, vc - 0.3, uv + 0.4, vv + 0.28, lw=0.85)
    
    # 6. Structural Steel Platforms and Cage Ladders
    for pl_z in [4.5, 8.5, 12.0]:
        up, vp = to_iso(0, 0, pl_z)
        cad_line(ax, up - 1.4, vp, up + 1.4, vp, lw=0.75, color='#444444')
        cad_line(ax, up - 1.4, vp + 0.4, up + 1.4, vp + 0.4, lw=0.45, color='#444444')
        
    # ═════════════════════════════════════════════════════════════════════════
    # BOTTOM RIGHT: MECHANICAL SPECIFICATIONS & HEAT EXCHANGER TABLES
    # ═════════════════════════════════════════════════════════════════════════
    TX_BASE = 16.0
    
    # 1. Heat Exchanger Thermal & Mechanical Data Table
    t1_headers = ['SPECIFICATION', 'REBOILER (E-103)', 'CONDENSER (E-102)']
    t1_rows = [
        ['TEMA Classification', 'BEM (Fixed Tubesheet)', 'AEL (Removable Bundle)'],
        ['Heat Duty', '3.24 MW (2.79 Gcal/h)', '2.88 MW (2.48 Gcal/h)'],
        ['Heat Transfer Surface Area', '92.5 m2', '145.0 m2'],
        ['Shell Diameter (ID)', '500 mm', '600 mm'],
        ['Tube Length', '2500 mm (Vertical)', '3000 mm (Horizontal)'],
        ['Tube OD x Wall Thickness', '19.05 mm (3/4") x 1.65 mm', '19.05 mm (3/4") x 1.65 mm'],
        ['Tube Pitch & Arrangement', '25.4 mm Triangular (30 deg)', '23.8 mm Triangular (30 deg)'],
        ['Tube Count / Material', '180 Tubes / 304L SS', '320 Tubes / 304L SS'],
        ['Shell Material', 'SA-516 Gr 70 / 304L Clad', 'SA-516 Gr 70 Carbon Steel'],
        ['Design Pressure (Shell/Tube)', '0.50 / 0.35 MPa(g)', '0.40 / 0.60 MPa(g)'],
        ['Design Temp. (Shell/Tube)', '160 C / 130 C', '110 C / 65 C'],
    ]
    t1_col_w = [4.4, 4.0, 4.0]
    cad_draw_table_a4(ax, TX_BASE, 8.45, t1_headers, t1_rows, t1_col_w,
                      row_h=0.33, title='TABLE 1: HEAT EXCHANGER MECHANICAL & TEMA DESIGN DATA',
                      title_sz=4.6, sz=3.8)
    
    # 2. Piping & Skid Interconnection Schedule Table
    t2_headers = ['SERVICE LINE', 'NOMINAL SIZE', 'SPEC / RATING', 'FLOW REGIME']
    t2_rows = [
        ['Overhead Vapor', 'DN250 (10")', '304L SS CL 150 RF', 'Vapor (22.5 m/s)'],
        ['Reflux Return', 'DN100 (4")', '304L SS CL 150 RF', 'Liquid (1.4 m/s)'],
        ['Distillate Run-down', 'DN80 (3")', '304L SS CL 150 RF', 'Liquid (1.1 m/s)'],
        ['Reboiler Liquid Feed', 'DN300 (12")', '304L SS CL 150 RF', 'Saturated Liquid'],
        ['Reboiler Vapor Return', 'DN300 (12")', '304L SS CL 150 RF', 'Two-Phase Mist'],
        ['Column Bottoms Effluent', 'DN80 (3")', '304L SS CL 150 RF', 'Hot Liquid (1.2 m/s)'],
        ['Reboiler LP Steam', 'DN150 (6")', 'Carbon Steel CL 150', 'Dry Saturated Steam'],
    ]
    t2_col_w = [3.6, 2.4, 3.6, 2.8]
    cad_draw_table_a4(ax, TX_BASE, 4.40, t2_headers, t2_rows, t2_col_w,
                      row_h=0.33, title='TABLE 2: PIPING SPECIFICATION & VELOCITY CRITERIA',
                      title_sz=4.6, sz=3.8)
    
    # Save Outputs
    fig.savefig(out_pdf, format='pdf', dpi=300)
    fig.savefig(out_png, format='png', dpi=300)
    plt.close(fig)
    print(f"  [OK] DWG-06 generated: {os.path.basename(out_pdf)}")

if __name__ == '__main__':
    out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Ethanol_Water_Distillation_Drawings')
    os.makedirs(out_dir, exist_ok=True)
    generate_ethanol_dwg06(
        os.path.join(out_dir, '06_Ethanol_Distillation_Reboiler_Condenser_3D_Isometric_CAD.pdf'),
        os.path.join(out_dir, '06_Ethanol_Distillation_Reboiler_Condenser_3D_Isometric_CAD.png')
    )
