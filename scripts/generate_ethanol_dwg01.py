"""
A4 OPTIMIZED: DWG-01 ETHANOL-WATER RECOVERY PROCESS FLOW DIAGRAM (PFD)
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
    cad_balloon, cad_valve, cad_draw_table_a4, W, H, BK, GREY
)

def generate_ethanol_dwg01(out_pdf, out_png):
    fig, ax = create_a4_canvas()
    draw_a4_border(ax)
    
    SUB_INFO = 'ETHANOL DISTILLATION (C-201)  |  700 kmol/h FEED (7 mol% EtOH)  |  ID 1.20 m, R=3.0  |  ASME SEC VIII / TEMA'
    draw_a4_title_block(ax, 'PROCESS FLOW DIAGRAM (PFD) & HEAT-MASS BALANCES',
                        'JU/ChE/ED/DWG-01', scale='DIAGRAMMATIC', date='01 / 09 / 2026', sub_info=SUB_INFO)
    
    # Drawing Header
    cad_text(ax, W/2, H - 1.25, 'PROCESS FLOW DIAGRAM (PFD) — ETHANOL-WATER RECOVERY DISTILLATION TRAIN', sz=6.8, bold=True)
    cad_text(ax, W/2, H - 1.62, 'BASIS: 700.0 kmol/h FEED @ 7.00 mol% ETHANOL | PRODUCT: 82.00 mol% (91.90 wt%) DISTILLATE | RECOVERY: 97.4%', sz=4.8, bold=False)
    
    # ═════════════════════════════════════════════════════════════════════════
    # EQUIPMENT DRAWINGS (FLOWSHEET: LEFT-TO-RIGHT)
    # ═════════════════════════════════════════════════════════════════════════
    
    # 1. FEED TANK T-101 (X=2.4, Y=9.8)
    TX, TY = 2.4, 9.8
    cad_rect(ax, TX, TY, 1.4, 2.0, lw=0.85, fill=True)
    cad_arc(ax, TX + 0.7, TY + 2.0, 1.4, 0.45, theta1=0, theta2=180, lw=0.85)
    cad_arc(ax, TX + 0.7, TY, 1.4, 0.45, theta1=180, theta2=360, lw=0.85)
    cad_text(ax, TX + 0.7, TY + 1.15, 'T-101\nFEED TANK\n50 m3', sz=4.4, bold=True)
    
    # 2. FEED PUMP P-101A/B (X=3.1, Y=6.4)
    PX, PY = 3.1, 6.4
    cad_circle(ax, PX, PY, 0.40, lw=0.85, fill=True)
    cad_line(ax, PX - 0.40, PY, PX, PY + 0.55, lw=0.75)
    cad_line(ax, PX + 0.40, PY, PX, PY + 0.55, lw=0.75)
    cad_text(ax, PX, PY - 0.65, 'P-101A/B\nFEED PUMPS', sz=4.2, bold=True)
    
    # Line T-101 bottom to Pump suction
    cad_line(ax, TX + 0.7, TY - 0.22, TX + 0.7, PY, lw=0.8)
    cad_line(ax, TX + 0.7, PY, PX - 0.40, PY, lw=0.8)
    cad_valve(ax, TX + 0.7, PY + 0.8, orientation='V', size=0.25)
    
    # 3. FEED PREHEATER / ECONOMIZER E-101 (X=6.2, Y=8.8)
    EX, EY = 6.2, 8.8
    cad_circle(ax, EX, EY, 0.65, lw=0.85, fill=True)
    cad_line(ax, EX - 0.65, EY - 0.65, EX + 0.65, EY + 0.65, lw=0.6, ls='--')
    cad_text(ax, EX, EY + 0.95, 'E-101\nFEED PREHEATER\n(ECONOMIZER)', sz=4.2, bold=True)
    
    # Line Pump discharge to E-101
    cad_line(ax, PX + 0.40, PY, EX - 1.2, PY, lw=0.8)
    cad_line(ax, EX - 1.2, PY, EX - 1.2, EY, lw=0.8)
    cad_line(ax, EX - 1.2, EY, EX - 0.65, EY, lw=0.8)
    cad_arrow(ax, EX - 0.9, EY, EX - 0.7, EY, head_scale=6)
    
    # 4. DISTILLATION COLUMN C-201 (X=11.2, Y=5.5)
    CX = 11.2
    CY_BOT = 5.6
    CY_TOP = 14.8
    CW = 1.30  # Column Width
    
    # Column Shell & Heads
    cad_line(ax, CX - CW/2, CY_BOT, CX - CW/2, CY_TOP, lw=1.1)
    cad_line(ax, CX + CW/2, CY_BOT, CX + CW/2, CY_TOP, lw=1.1)
    cad_arc(ax, CX, CY_TOP, CW, 0.60, theta1=0, theta2=180, lw=1.1)
    cad_arc(ax, CX, CY_BOT, CW, 0.60, theta1=180, theta2=360, lw=1.1)
    
    # Skirt
    cad_rect(ax, CX - CW/2, 3.8, CW, CY_BOT - 3.8, lw=0.85)
    cad_circle(ax, CX, 4.7, 0.25, lw=0.6)
    cad_text(ax, CX, 4.7, 'ACCESS', sz=3.2, bold=True)
    cad_line(ax, CX - CW/2 - 0.3, 3.8, CX + CW/2 + 0.3, 3.8, lw=1.2)
    
    # Internal Trays (Schematic Trays)
    cad_text(ax, CX, CY_TOP - 0.5, 'TRAY 1 (TOP)', sz=3.6, bold=True)
    for i in range(11):
        yt = CY_TOP - 0.9 - i * 0.70
        is_feed = (i == 6)
        lw_t = 0.85 if is_feed else 0.45
        ls_t = '-' if not is_feed else '-'
        col_t = '#006600' if is_feed else BK
        cad_line(ax, CX - CW/2 + 0.12, yt, CX + CW/2 - 0.12, yt, lw=lw_t, ls=ls_t, color=col_t)
        if is_feed:
            cad_text(ax, CX + 0.15, yt + 0.16, 'FEED TRAY (TRAY 11)', sz=3.8, bold=True, color='#006600')
    cad_text(ax, CX, CY_BOT + 0.6, 'TRAY 24 (BOTTOM)', sz=3.6, bold=True)
    
    cad_text(ax, CX, CY_TOP + 1.25, 'C-201\nDISTILLATION COLUMN\nID 1200 mm | 24 SIEVE TRAYS', sz=5.2, bold=True)
    
    # Line E-101 outlet to Column Feed Tray
    Y_FEED = CY_TOP - 0.9 - 6 * 0.70  # ~9.7
    cad_line(ax, EX + 0.65, EY, CX - CW/2 - 0.9, EY, lw=0.8)
    cad_line(ax, CX - CW/2 - 0.9, EY, CX - CW/2 - 0.9, Y_FEED, lw=0.8)
    cad_line(ax, CX - CW/2 - 0.9, Y_FEED, CX - CW/2, Y_FEED, lw=0.8)
    cad_arrow(ax, CX - CW/2 - 0.3, Y_FEED, CX - CW/2, Y_FEED, head_scale=6)
    
    # 5. OVERHEAD CONDENSER E-102 (X=16.2, Y=14.8)
    CDX, CDY = 16.2, 14.8
    cad_rect(ax, CDX - 1.1, CDY - 0.45, 2.2, 0.90, lw=0.85, fill=True)
    cad_line(ax, CDX - 0.9, CDY - 0.3, CDX + 0.9, CDY + 0.3, lw=0.55)
    cad_line(ax, CDX - 0.9, CDY + 0.3, CDX + 0.9, CDY - 0.3, lw=0.55)
    cad_text(ax, CDX, CDY + 0.85, 'E-102\nTOTAL CONDENSER\n2.88 MW (CW)', sz=4.4, bold=True)
    
    # Cooling water in/out
    cad_arrow(ax, CDX - 0.6, CDY - 0.9, CDX - 0.6, CDY - 0.45, head_scale=5)
    cad_text(ax, CDX - 0.6, CDY - 1.1, 'CW IN (30 C)', sz=3.5, bold=True)
    cad_arrow(ax, CDX + 0.6, CDY + 0.45, CDX + 0.6, CDY + 0.9, head_scale=5)
    cad_text(ax, CDX + 0.6, CDY + 1.1, 'CW OUT (42 C)', sz=3.5, bold=True)
    
    # Overhead vapor line from C-201 to E-102
    cad_line(ax, CX, CY_TOP + 0.30, CX, CDY, lw=0.85)
    cad_line(ax, CX, CDY, CDX - 1.1, CDY, lw=0.85)
    cad_arrow(ax, CDX - 1.4, CDY, CDX - 1.15, CDY, head_scale=6)
    
    # 6. REFLUX DRUM V-101 (X=16.2, Y=10.5)
    RX, RY = 16.2, 10.6
    cad_rect(ax, RX - 0.9, RY - 0.4, 1.8, 0.8, lw=0.85, fill=True)
    cad_arc(ax, RX - 0.9, RY, 0.4, 0.8, theta1=90, theta2=270, lw=0.85)
    cad_arc(ax, RX + 0.9, RY, 0.4, 0.8, theta1=270, theta2=90, lw=0.85)
    cad_text(ax, RX, RY, 'V-101\nREFLUX DRUM\n2.5 m3', sz=4.2, bold=True)
    
    # Condensate line E-102 to V-101
    cad_line(ax, CDX + 0.8, CDY - 0.45, CDX + 0.8, RY + 0.7, lw=0.8)
    cad_line(ax, CDX + 0.8, RY + 0.7, RX, RY + 0.7, lw=0.8)
    cad_line(ax, RX, RY + 0.7, RX, RY + 0.4, lw=0.8)
    cad_arrow(ax, RX, RY + 0.6, RX, RY + 0.45, head_scale=6)
    
    # Vent from V-101 top
    cad_line(ax, RX + 0.6, RY + 0.4, RX + 0.6, RY + 1.1, lw=0.6)
    cad_arrow(ax, RX + 0.6, RY + 0.9, RX + 0.6, RY + 1.2, head_scale=5)
    cad_text(ax, RX + 0.6, RY + 1.35, 'TO OFF-GAS/VENT', sz=3.4, bold=True)
    
    # 7. REFLUX & DISTILLATE PUMPS P-102A/B (X=16.2, Y=7.5)
    RPX, RPY = 16.2, 7.5
    cad_circle(ax, RPX, RPY, 0.38, lw=0.85, fill=True)
    cad_line(ax, RPX - 0.38, RPY, RPX, RPY + 0.52, lw=0.75)
    cad_line(ax, RPX + 0.38, RPY, RPX, RPY + 0.52, lw=0.75)
    cad_text(ax, RPX, RPY - 0.65, 'P-102A/B\nREFLUX PUMPS', sz=4.0, bold=True)
    
    # Line V-101 bottom to Pump suction
    cad_line(ax, RX, RY - 0.4, RX, RPY + 0.52, lw=0.8)
    
    # Pump discharge splits: Reflux return to C-201 and Distillate Product
    cad_line(ax, RPX + 0.38, RPY, RPX + 1.6, RPY, lw=0.8)
    cad_line(ax, RPX + 1.6, RPY, RPX + 1.6, RPY + 1.8, lw=0.8)
    
    # Reflux Line (going left back to top tray of C-201)
    cad_line(ax, RPX + 1.6, RPY + 1.8, CX + CW/2 + 0.8, RPY + 1.8, lw=0.8)
    cad_line(ax, CX + CW/2 + 0.8, RPY + 1.8, CX + CW/2 + 0.8, CY_TOP - 0.8, lw=0.8)
    cad_line(ax, CX + CW/2 + 0.8, CY_TOP - 0.8, CX + CW/2, CY_TOP - 0.8, lw=0.8)
    cad_arrow(ax, CX + CW/2 + 0.3, CY_TOP - 0.8, CX + CW/2, CY_TOP - 0.8, head_scale=6)
    cad_valve(ax, CX + CW/2 + 0.8, RPY + 1.8, orientation='H', size=0.25)
    
    # Distillate Product Line (going right to storage)
    cad_line(ax, RPX + 1.6, RPY, RPX + 3.8, RPY, lw=0.8)
    cad_arrow(ax, RPX + 3.5, RPY, RPX + 3.9, RPY, head_scale=6)
    cad_text(ax, RPX + 4.8, RPY, 'DISTILLATE PRODUCT\n(82 mol% / 91.9 wt% EtOH)', sz=4.2, bold=True, ha='left')
    
    # 8. THERMOSIPHON REBOILER E-103 (X=7.8, Y=4.8)
    RBX, RBY = 7.8, 4.8
    cad_rect(ax, RBX - 0.45, RBY - 1.1, 0.90, 2.2, lw=0.85, fill=True)
    cad_line(ax, RBX - 0.3, RBY - 0.9, RBX + 0.3, RBY + 0.9, lw=0.55)
    cad_line(ax, RBX - 0.3, RBY + 0.9, RBX + 0.3, RBY - 0.9, lw=0.55)
    cad_text(ax, RBX, RBY - 1.5, 'E-103\nTHERMOSIPHON REBOILER\n3.24 MW (STEAM 3 bar)', sz=4.2, bold=True)
    
    # Steam in & Condensate out
    cad_arrow(ax, RBX - 1.2, RBY + 0.6, RBX - 0.45, RBY + 0.6, head_scale=5)
    cad_text(ax, RBX - 1.5, RBY + 0.6, 'STEAM IN\n(3 bar(g))', sz=3.4, bold=True, ha='right')
    cad_arrow(ax, RBX - 0.45, RBY - 0.6, RBX - 1.2, RBY - 0.6, head_scale=5)
    cad_text(ax, RBX - 1.5, RBY - 0.6, 'CONDENSATE OUT', sz=3.4, bold=True, ha='right')
    
    # Column Sump to Reboiler bottom
    cad_line(ax, CX - CW/2, CY_BOT + 0.4, RBX + 0.45, CY_BOT + 0.4, lw=0.8)
    cad_line(ax, RBX + 0.45, CY_BOT + 0.4, RBX, CY_BOT + 0.4, lw=0.8)
    cad_line(ax, RBX, CY_BOT + 0.4, RBX, RBY - 1.1, lw=0.8)
    cad_arrow(ax, RBX + 0.2, CY_BOT + 0.4, RBX + 0.05, CY_BOT + 0.4, head_scale=6)
    
    # Reboiler top to Column vapor return
    cad_line(ax, RBX, RBY + 1.1, RBX, CY_BOT + 1.8, lw=0.85)
    cad_line(ax, RBX, CY_BOT + 1.8, CX - CW/2, CY_BOT + 1.8, lw=0.85)
    cad_arrow(ax, CX - CW/2 - 0.3, CY_BOT + 1.8, CX - CW/2, CY_BOT + 1.8, head_scale=6)
    
    # 9. BOTTOMS EFFLUENT & COOLER E-104 (X=11.2, Y=2.5)
    # Bottoms liquid draw from column base
    cad_line(ax, CX, CY_BOT - 0.30, CX, 3.2, lw=0.8)
    cad_line(ax, CX, 3.2, 5.0, 3.2, lw=0.8)
    cad_line(ax, 5.0, 3.2, 5.0, EY - 0.65, lw=0.8)  # Feeds hot bottoms to E-101 shell
    cad_arrow(ax, 5.0, EY - 1.0, 5.0, EY - 0.70, head_scale=5)
    cad_text(ax, 4.3, 3.4, 'HOT BOTTOMS (99.6 C)', sz=3.6, bold=True)
    
    # Cooled bottoms from E-101 to Trim Cooler E-104
    cad_line(ax, EX, EY + 0.65, EX, 11.2, lw=0.75)
    cad_line(ax, EX, 11.2, 8.8, 11.2, lw=0.75)
    cad_arrow(ax, 7.8, 11.2, 7.3, 11.2, head_scale=5)
    cad_text(ax, 7.8, 11.45, 'WARM BOTTOMS (65 C)', sz=3.5, bold=True)
    
    # E-104 Trim Cooler (X=5.5, Y=11.2)
    cad_rect(ax, 5.0, 10.7, 1.2, 0.8, lw=0.75, fill=True)
    cad_text(ax, 5.6, 11.1, 'E-104\nTRIM COOLER', sz=3.6, bold=True)
    cad_line(ax, 5.0, 11.1, 4.0, 11.1, lw=0.75)
    cad_arrow(ax, 4.3, 11.1, 3.9, 11.1, head_scale=5)
    cad_text(ax, 3.8, 11.4, 'BOTTOMS TO EFFLUENT (40 C)\n(0.20 mol% EtOH, 97.4% RECOVERY)', sz=3.8, bold=True, ha='right')
    
    # ═════════════════════════════════════════════════════════════════════════
    # STREAM FLAGS / NUMBERING DIAMONDS (1 TO 8)
    # ═════════════════════════════════════════════════════════════════════════
    def cad_stream_flag(ax, x, y, num):
        d = 0.26
        pts = [(x, y + d), (x + d*1.2, y), (x, y - d), (x - d*1.2, y)]
        ax.add_patch(Polygon(pts, closed=True, fc='#ffeecc', ec=BK, lw=0.75, zorder=7))
        cad_text(ax, x, y, str(num), sz=4.8, bold=True, zorder=8)
    
    cad_stream_flag(ax, 2.0, PY, 1)            # Raw feed
    cad_stream_flag(ax, 9.4, Y_FEED, 2)        # Preheated feed
    cad_stream_flag(ax, 13.5, CDY, 3)          # Overhead vapor
    cad_stream_flag(ax, 16.2, RY + 0.55, 4)    # Condensed liquid
    cad_stream_flag(ax, 14.5, RPY + 1.8, 5)    # Reflux return
    cad_stream_flag(ax, 19.4, RPY, 6)          # Distillate product
    cad_stream_flag(ax, 8.2, 3.2, 7)           # Hot bottoms draw
    cad_stream_flag(ax, 4.4, 11.1, 8)          # Cooled bottoms effluent
    
    # ═════════════════════════════════════════════════════════════════════════
    # RIGOROUS MASS & ENERGY BALANCE STREAM TABLE (100.000% CLOSURE)
    # ═════════════════════════════════════════════════════════════════════════
    # MW EtOH = 46.069, MW Water = 18.015
    # Feed: 700.0 kmol/h @ 7.00 mol% = 19.979 kg/kmol -> 13,985.2 kg/h (16.14 wt%)
    # Distillate: 58.19 kmol/h @ 82.00 mol% = 41.020 kg/kmol -> 2,387.0 kg/h (91.90 wt%)
    # Bottoms: 641.81 kmol/h @ 0.20 mol% = 18.071 kg/kmol -> 11,598.2 kg/h (0.51 wt%)
    # Balance: 2,387.0 + 11,598.2 = 13,985.2 kg/h (Exact 100.000% closure)
    headers = ['STR', 'DESCRIPTION', 'FLOW (kmol/h)', 'MASS (kg/h)', 'mol% EtOH', 'wt% EtOH', 'TEMP (C)', 'PRESS (kPa)', 'PHASE']
    rows = [
        ['1', 'Raw Feed from Storage (T-101)', '700.0', '13,985', '7.00', '16.14', '30.0', '101.3', 'Liquid'],
        ['2', 'Preheated Feed to Column (Tray 11)', '700.0', '13,985', '7.00', '16.14', '83.5', '120.0', 'Bubble Liq (q=1)'],
        ['3', 'Overhead Vapor to Condenser (E-102)', '232.8', '9,548', '82.00', '91.90', '78.4', '101.3', 'Vapor (Dew Pt)'],
        ['4', 'Total Condensed Liquid to Reflux Drum', '232.8', '9,548', '82.00', '91.90', '78.0', '101.3', 'Subcooled Liq'],
        ['5', 'Reflux Return to Top Tray (R=3.0)', '174.6', '7,161', '82.00', '91.90', '78.0', '115.0', 'Liquid'],
        ['6', 'Distillate Product to Battery Limits', '58.2', '2,387', '82.00', '91.90', '78.0', '115.0', 'Liquid Product'],
        ['7', 'Column Bottoms to Reboiler / Exchanger', '641.8', '11,598', '0.20', '0.51', '99.6', '125.0', 'Saturated Liq'],
        ['8', 'Treated Bottoms Effluent to Storage', '641.8', '11,598', '0.20', '0.51', '40.0', '101.3', 'Liquid Effluent'],
    ]
    col_w = [0.8, 6.2, 2.5, 2.4, 2.3, 2.2, 1.8, 2.2, 2.7]
    
    cad_draw_table_a4(ax, 3.4, 0.95 + 2.30 + 0.12, headers, rows, col_w,
                      row_h=0.32, title='TABLE 1: RIGOROUS HEAT & MASS BALANCE STREAM DATA (ETHANOL-WATER SYSTEM)',
                      title_sz=4.8, sz=3.8)
    
    # Save Outputs
    fig.savefig(out_pdf, format='pdf', dpi=300)
    fig.savefig(out_png, format='png', dpi=300)
    plt.close(fig)
    print(f"  [OK] DWG-01 generated: {os.path.basename(out_pdf)}")

if __name__ == '__main__':
    out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Ethanol_Water_Distillation_Drawings')
    os.makedirs(out_dir, exist_ok=True)
    generate_ethanol_dwg01(
        os.path.join(out_dir, '01_Ethanol_Distillation_Process_Flow_Diagram_PFD.pdf'),
        os.path.join(out_dir, '01_Ethanol_Distillation_Process_Flow_Diagram_PFD.png')
    )
