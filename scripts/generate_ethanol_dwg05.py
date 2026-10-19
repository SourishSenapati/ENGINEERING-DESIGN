"""
A4 OPTIMIZED: DWG-05 PIPING & INSTRUMENTATION DIAGRAM (P&ID)
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
    cad_valve, cad_instrument_bubble, cad_draw_table_a4, W, H, BK, GREY
)

def generate_ethanol_dwg05(out_pdf, out_png):
    fig, ax = create_a4_canvas()
    draw_a4_border(ax)
    
    SUB_INFO = 'ETHANOL DISTILLATION (C-201)  |  700 kmol/h FEED (7 mol% EtOH)  |  ID 1.20 m, R=3.0  |  ASME SEC VIII / TEMA'
    draw_a4_title_block(ax, 'PIPING & INSTRUMENTATION DIAGRAM (P&ID) — ISA-5.1',
                        'JU/ChE/ED/DWG-05', scale='SCHEMATIC (ISA-5.1)', date='01 / 09 / 2026', sub_info=SUB_INFO)
    
    # Drawing Header
    cad_text(ax, W/2, H - 1.25, 'PIPING & INSTRUMENTATION DIAGRAM (P&ID) — DISTILLATION SYSTEM (C-201)', sz=6.6, bold=True)
    cad_text(ax, W/2, H - 1.62, 'ISA-5.1 INSTRUMENTATION LOOPS: REFLUX CASCADE, SPLIT-RANGE PRESSURE, SUMP LEVEL & STEAM INTERLOCKS', sz=4.8, bold=False)
    
    # ═════════════════════════════════════════════════════════════════════════
    # EQUIPMENT DRAWINGS (P&ID SCHEMATIC LAYOUT)
    # ═════════════════════════════════════════════════════════════════════════
    
    # 1. DISTILLATION COLUMN C-201 (X=10.4, Y=4.8 to 14.8)
    CX = 10.4
    CY_BOT = 4.8
    CY_TOP = 14.6
    CW = 1.30
    
    cad_rect(ax, CX - CW/2, CY_BOT, CW, CY_TOP - CY_BOT, lw=1.1, fill=True)
    cad_arc(ax, CX, CY_TOP, CW, 0.55, theta1=0, theta2=180, lw=1.1)
    cad_arc(ax, CX, CY_BOT, CW, 0.55, theta1=180, theta2=360, lw=1.1)
    cad_text(ax, CX, CY_TOP + 1.15, 'C-201\nDISTILLATION COLUMN\nID 1200 mm | 24 TRAYS', sz=4.8, bold=True)
    
    # Skirt
    cad_rect(ax, CX - CW/2, 3.4, CW, CY_BOT - 3.4, lw=0.85)
    cad_line(ax, CX - CW/2 - 0.25, 3.4, CX + CW/2 + 0.25, 3.4, lw=1.1)
    
    # Internal Trays (Schematic)
    for i in range(9):
        yt = CY_TOP - 0.9 - i * 0.95
        cad_line(ax, CX - CW/2 + 0.1, yt, CX + CW/2 - 0.1, yt, lw=0.45, ls='--')
    cad_text(ax, CX, 9.75, 'FEED TRAY (11)', sz=3.6, bold=True, color='#008800')
    
    # 2. FEED SYSTEM & PREHEATER E-101 (X=3.4, Y=9.75)
    cad_line(ax, 1.2, 9.75, 4.4, 9.75, lw=0.9)  # Feed line
    cad_arrow(ax, 2.0, 9.75, 2.4, 9.75, head_scale=6)
    cad_text(ax, 1.8, 10.15, 'FEED 700 kmol/h\n(7.0 mol% EtOH)', sz=3.8, bold=True)
    
    # Feed Control Valve FCV-201
    cad_valve(ax, 3.0, 9.75, orientation='H', size=0.35, valve_type='CONTROL')
    cad_text(ax, 3.0, 9.35, 'FCV-201\n(FC)', sz=3.4, bold=True)
    
    # Feed Preheater E-101
    cad_circle(ax, 4.8, 9.75, 0.55, lw=0.85, fill=True)
    cad_text(ax, 4.8, 10.60, 'E-101\nFEED PREHEATER', sz=3.8, bold=True)
    
    # Line into Column C-201
    cad_line(ax, 5.35, 9.75, CX - CW/2, 9.75, lw=0.9)
    cad_arrow(ax, CX - CW/2 - 0.4, 9.75, CX - CW/2, 9.75, head_scale=6)
    
    # 3. OVERHEAD CONDENSER E-102 (X=15.4, Y=14.6)
    CDX, CDY = 15.4, 14.6
    cad_rect(ax, CDX - 1.1, CDY - 0.45, 2.2, 0.90, lw=0.85, fill=True)
    cad_text(ax, CDX, CDY + 0.85, 'E-102 TOTAL CONDENSER', sz=4.2, bold=True)
    
    # Overhead vapor line
    cad_line(ax, CX, CY_TOP + 0.28, CX, CDY, lw=0.9)
    cad_line(ax, CX, CDY, CDX - 1.1, CDY, lw=0.9)
    cad_arrow(ax, CDX - 1.4, CDY, CDX - 1.12, CDY, head_scale=6)
    cad_text(ax, 12.8, CDY + 0.25, 'OVERHEAD VAPOR (10" DN250)', sz=3.5, bold=True)
    
    # Cooling water line with Control Valve PCV-202A
    cad_line(ax, CDX - 0.5, CDY - 1.4, CDX - 0.5, CDY - 0.45, lw=0.7)
    cad_arrow(ax, CDX - 0.5, CDY - 0.7, CDX - 0.5, CDY - 0.48, head_scale=5)
    cad_valve(ax, CDX - 0.5, CDY - 1.0, orientation='V', size=0.30, valve_type='CONTROL')
    cad_text(ax, CDX - 1.1, CDY - 1.0, 'PCV-202A\n(FO)', sz=3.2, bold=True)
    cad_text(ax, CDX - 0.5, CDY - 1.6, 'CW INLET', sz=3.4, bold=True)
    
    # 4. REFLUX DRUM V-101 (X=15.4, Y=10.6)
    RX, RY = 15.4, 10.6
    cad_rect(ax, RX - 0.85, RY - 0.4, 1.7, 0.8, lw=0.85, fill=True)
    cad_arc(ax, RX - 0.85, RY, 0.4, 0.8, theta1=90, theta2=270, lw=0.85)
    cad_arc(ax, RX + 0.85, RY, 0.4, 0.8, theta1=270, theta2=90, lw=0.85)
    cad_text(ax, RX, RY, 'V-101\nREFLUX DRUM', sz=4.0, bold=True)
    
    # Line E-102 to V-101
    cad_line(ax, CDX + 0.7, CDY - 0.45, CDX + 0.7, RY + 0.6, lw=0.8)
    cad_line(ax, CDX + 0.7, RY + 0.6, RX, RY + 0.6, lw=0.8)
    cad_line(ax, RX, RY + 0.6, RX, RY + 0.4, lw=0.8)
    cad_arrow(ax, RX, RY + 0.55, RX, RY + 0.42, head_scale=6)
    
    # Off-gas / Vent line with PCV-202B
    cad_line(ax, RX + 0.6, RY + 0.4, RX + 0.6, RY + 1.6, lw=0.6)
    cad_valve(ax, RX + 0.6, RY + 1.0, orientation='V', size=0.25, valve_type='CONTROL')
    cad_text(ax, RX + 1.15, RY + 1.0, 'PCV-202B\n(FC)', sz=3.2, bold=True)
    cad_arrow(ax, RX + 0.6, RY + 1.3, RX + 0.6, RY + 1.7, head_scale=5)
    cad_text(ax, RX + 0.6, RY + 1.9, 'TO OFF-GAS / FLARE', sz=3.4, bold=True)
    
    # 5. REFLUX PUMPS P-102A/B & LINES (X=15.4, Y=7.4)
    RPX, RPY = 15.4, 7.4
    cad_circle(ax, RPX, RPY, 0.36, lw=0.85, fill=True)
    cad_text(ax, RPX, RPY - 0.6, 'P-102A/B\nREFLUX PUMPS', sz=3.8, bold=True)
    cad_line(ax, RX, RY - 0.4, RX, RPY + 0.36, lw=0.8)
    
    # Pump Discharge
    cad_line(ax, RPX + 0.36, RPY, RPX + 1.5, RPY, lw=0.8)
    cad_line(ax, RPX + 1.5, RPY, RPX + 1.5, RPY + 1.8, lw=0.8)
    
    # Reflux return to column top
    cad_line(ax, RPX + 1.5, RPY + 1.8, CX + CW/2, RPY + 1.8, lw=0.8)
    cad_arrow(ax, CX + CW/2 + 0.35, RPY + 1.8, CX + CW/2, RPY + 1.8, head_scale=6)
    cad_valve(ax, 13.6, RPY + 1.8, orientation='H', size=0.30, valve_type='CONTROL')
    cad_text(ax, 13.6, RPY + 2.25, 'FCV-204 (FO)', sz=3.4, bold=True)
    cad_text(ax, 12.6, RPY + 1.55, 'REFLUX LINE (R=3.0)', sz=3.2, bold=True)
    
    # Distillate product line
    cad_line(ax, RPX + 1.5, RPY, 19.2, RPY, lw=0.8)
    cad_valve(ax, 17.6, RPY, orientation='H', size=0.30, valve_type='CONTROL')
    cad_text(ax, 17.6, RPY - 0.45, 'LCV-203 (FC)', sz=3.4, bold=True)
    cad_arrow(ax, 18.9, RPY, 19.3, RPY, head_scale=6)
    cad_text(ax, 19.4, RPY + 0.15, 'DISTILLATE PRODUCT\n(85 mol% EtOH)', sz=3.6, bold=True, ha='left')
    
    # 6. REBOILER E-103 (X=6.8, Y=4.2)
    RBX, RBY = 6.8, 4.2
    cad_rect(ax, RBX - 0.42, RBY - 0.9, 0.84, 1.8, lw=0.85, fill=True)
    cad_text(ax, RBX, RBY - 1.25, 'E-103\nTHERMOSIPHON\nREBOILER', sz=3.8, bold=True)
    
    # Recirculation Loop: Sump to Reboiler
    cad_line(ax, CX - CW/2, CY_BOT + 0.35, RBX, CY_BOT + 0.35, lw=0.8)
    cad_line(ax, RBX, CY_BOT + 0.35, RBX, RBY - 0.9, lw=0.8)
    # Vapor Return: Reboiler to Column
    cad_line(ax, RBX, RBY + 0.9, RBX, CY_BOT + 1.6, lw=0.85)
    cad_line(ax, RBX, CY_BOT + 1.6, CX - CW/2, CY_BOT + 1.6, lw=0.85)
    cad_arrow(ax, CX - CW/2 - 0.3, CY_BOT + 1.6, CX - CW/2, CY_BOT + 1.6, head_scale=6)
    
    # Reboiler Steam Inlet line with Control Valve FCV-206
    cad_line(ax, RBX - 1.8, RBY + 0.5, RBX - 0.42, RBY + 0.5, lw=0.75)
    cad_arrow(ax, RBX - 0.7, RBY + 0.5, RBX - 0.45, RBY + 0.5, head_scale=5)
    cad_valve(ax, RBX - 1.2, RBY + 0.5, orientation='H', size=0.30, valve_type='CONTROL')
    cad_text(ax, RBX - 1.2, RBY + 0.90, 'FCV-206 (FC)', sz=3.4, bold=True)
    cad_text(ax, RBX - 2.0, RBY + 0.5, 'STEAM 3 bar', sz=3.4, bold=True, ha='right')
    
    # 7. BOTTOMS DRAW & LEVEL VALVE LCV-207
    cad_line(ax, CX, CY_BOT - 0.28, CX, 2.8, lw=0.8)
    cad_line(ax, CX, 2.8, 4.4, 2.8, lw=0.8)
    cad_valve(ax, 3.2, 2.8, orientation='H', size=0.30, valve_type='CONTROL')
    cad_text(ax, 3.2, 2.4, 'LCV-207 (FC)', sz=3.4, bold=True)
    cad_arrow(ax, 4.1, 2.8, 4.4, 2.8, head_scale=5)
    cad_text(ax, 4.5, 2.8, 'BOTTOMS TO E-101 / EFFLUENT', sz=3.4, bold=True, ha='left')
    
    # ═════════════════════════════════════════════════════════════════════════
    # ISA-5.1 INSTRUMENTATION BUBBLES & CONTROL LOOPS
    # ═════════════════════════════════════════════════════════════════════════
    # Loop 1: Feed Flow Control Loop (FIC-201)
    cad_instrument_bubble(ax, 2.2, 11.2, 'FT', '201', loc='FIELD', sz=3.8)
    cad_instrument_bubble(ax, 3.0, 11.2, 'FIC', '201', loc='DCS', sz=3.8)
    cad_line(ax, 2.2, 9.75, 2.2, 10.85, lw=0.45, ls='--')
    cad_line(ax, 2.55, 11.2, 2.65, 11.2, lw=0.45, ls='--')
    cad_line(ax, 3.0, 10.85, 3.0, 9.95, lw=0.45, ls='--')
    
    # Loop 2: Top Column Pressure Control (PIC-202 Split Range)
    cad_instrument_bubble(ax, 11.6, 16.0, 'PT', '202', loc='FIELD', sz=3.8)
    cad_instrument_bubble(ax, 12.8, 16.0, 'PIC', '202', loc='DCS', sz=3.8)
    cad_line(ax, 11.6, CDY, 11.6, 15.65, lw=0.45, ls='--')
    cad_line(ax, 11.95, 16.0, 12.45, 16.0, lw=0.45, ls='--')
    cad_line(ax, 12.8, 15.65, CDX - 0.5, CDY - 0.8, lw=0.45, ls='--') # to PCV-202A
    cad_line(ax, 13.15, 16.0, RX + 0.6, RY + 1.2, lw=0.45, ls='--')   # to PCV-202B
    
    # Loop 3: Reflux Drum Level (LIC-203)
    cad_instrument_bubble(ax, 17.6, 11.8, 'LT', '203', loc='FIELD', sz=3.8)
    cad_instrument_bubble(ax, 17.6, 10.4, 'LIC', '203', loc='DCS', sz=3.8)
    cad_line(ax, RX + 0.85, RY, 17.25, 11.8, lw=0.45, ls='--')
    cad_line(ax, 17.6, 11.45, 17.6, 10.75, lw=0.45, ls='--')
    cad_line(ax, 17.6, 10.05, 17.6, RPY + 0.25, lw=0.45, ls='--') # to LCV-203
    
    # Loop 4: Sensitive Tray Temp & Reflux Cascade (TIC-204 -> FIC-204)
    cad_instrument_bubble(ax, 11.6, 11.8, 'TT', '204', loc='FIELD', sz=3.8)
    cad_instrument_bubble(ax, 12.6, 11.8, 'TIC', '204', loc='DCS', sz=3.8)
    cad_instrument_bubble(ax, 13.6, 11.8, 'FIC', '204', loc='DCS', sz=3.8)
    cad_line(ax, CX + CW/2, 11.8, 11.25, 11.8, lw=0.45, ls='--')
    cad_line(ax, 11.95, 11.8, 12.25, 11.8, lw=0.45, ls='--')
    cad_line(ax, 12.95, 11.8, 13.25, 11.8, lw=0.45, ls='--')
    cad_line(ax, 13.6, 11.45, 13.6, RPY + 2.05, lw=0.45, ls='--') # to FCV-204
    
    # Loop 5: Column Differential Pressure Transmitter (PDIT-205) & Reboiler Steam (FIC-206)
    cad_instrument_bubble(ax, 8.8, 13.2, 'PDIT', '205', loc='DCS', sz=3.4)
    cad_line(ax, CX - CW/2, CY_TOP - 0.5, 8.8, 13.55, lw=0.40, ls='--') # High tap
    cad_line(ax, CX - CW/2, CY_BOT + 0.8, 8.8, 12.85, lw=0.40, ls='--') # Low tap
    cad_instrument_bubble(ax, 5.4, 6.2, 'FIC', '206', loc='DCS', sz=3.8)
    cad_line(ax, 8.8, 12.85, 5.4, 6.55, lw=0.45, ls='--')                # Interlock to steam
    cad_line(ax, 5.4, 5.85, RBX - 1.2, RBY + 0.70, lw=0.45, ls='--')    # to FCV-206
    
    # Loop 6: Column Sump Level Control (LIC-207)
    cad_instrument_bubble(ax, 8.8, 3.8, 'LT', '207', loc='FIELD', sz=3.8)
    cad_instrument_bubble(ax, 8.8, 2.8, 'LIC', '207', loc='DCS', sz=3.8)
    cad_line(ax, CX - CW/2, CY_BOT, 8.8, 4.15, lw=0.45, ls='--')
    cad_line(ax, 8.8, 3.45, 8.8, 3.15, lw=0.45, ls='--')
    cad_line(ax, 8.45, 2.8, 3.4, 2.8, lw=0.45, ls='--') # to LCV-207
    
    # Loop 7: Safety Relief Valve PSV-201
    cad_valve(ax, 8.8, CY_TOP + 0.28, orientation='H', size=0.30, valve_type='SRV')
    cad_line(ax, CX - CW/2, CY_TOP - 0.2, 8.8, CY_TOP - 0.2, lw=0.7)
    cad_line(ax, 8.8, CY_TOP - 0.2, 8.8, CY_TOP + 0.15, lw=0.7)
    cad_line(ax, 8.8, CY_TOP + 0.45, 8.8, CY_TOP + 1.2, lw=0.7)
    cad_arrow(ax, 8.8, CY_TOP + 0.8, 8.8, CY_TOP + 1.25, head_scale=5)
    cad_text(ax, 8.8, CY_TOP + 1.45, 'PSV-201A/B SET 0.35 MPa(g)\nTO FLARE HEADER', sz=3.4, bold=True)
    
    # ═════════════════════════════════════════════════════════════════════════
    # RIGHT HALF: INSTRUMENT SCHEDULE & INTERLOCK LOGIC SCHEDULE
    # ═════════════════════════════════════════════════════════════════════════
    RX_BASE = 14.8
    
    # 1. Instrument Schedule Table
    t1_headers = ['TAG NO.', 'SERVICE / LOOP', 'RANGE', 'SETPOINT', 'ACTION / FAIL']
    t1_rows = [
        ['FT/FIC-201', 'Feed Flow to Column', '0 - 1000 kmol/h', '700.0 kmol/h', 'FCV-201 (Fail Closed)'],
        ['PT/PIC-202', 'Top Vapor Pressure', '0 - 200 kPa(a)', '101.325 kPa', 'Split: PCV-202A (FO) / B (FC)'],
        ['LT/LIC-203', 'Reflux Drum Level', '0 - 100 %', '50.0 % level', 'LCV-203 (Fail Closed)'],
        ['TT/TIC-204', 'Tray 18 Temperature', '50 - 120 C', '79.2 C', 'Cascades to FIC-204'],
        ['FT/FIC-204', 'Reflux Liquid Flow', '0 - 300 kmol/h', '167.7 kmol/h', 'FCV-204 (Fail Open - FO)'],
        ['PDIT-205', 'Column Differential Press.', '0 - 30.0 kPa', '13.0 kPa', 'Alarm High @ 17.5 kPa'],
        ['FT/FIC-206', 'Reboiler 3 bar Steam', '0 - 6,000 kg/h', '4,850 kg/h', 'FCV-206 (Fail Closed)'],
        ['LT/LIC-207', 'Bottoms Sump Level', '0 - 100 %', '50.0 % level', 'LCV-207 (Fail Closed)'],
        ['PSV-201A/B', 'Column Overpressure Relief', '0 - 0.50 MPa', '0.35 MPa(g)', 'Pop Action to Flare Header'],
    ]
    t1_col_w = [2.2, 4.4, 2.5, 2.3, 2.2]
    cad_draw_table_a4(ax, RX_BASE, 8.85, t1_headers, t1_rows, t1_col_w,
                      row_h=0.33, title='TABLE 1: ISA-5.1 INSTRUMENT & CONTROL LOOP SCHEDULE',
                      title_sz=4.6, sz=3.7)
    
    # 2. Safety Interlock & Cause-and-Effect Logic Table
    t2_headers = ['TRIP ID', 'INITIATING EVENT', 'LOGIC / SETPOINT', 'AUTOMATED SAFETY ACTION']
    t2_rows = [
        ['I-01', 'Column High DP (Flooding)', 'PDIT-205 > 17.5 kPa', 'Cut reboiler steam FCV-206 to 30%; Alarm'],
        ['I-02', 'Low Sump Level (Dryout)', 'LT-207 < 15.0 %', 'Trip steam FCV-206 closed; Stop bottoms draw'],
        ['I-03', 'Reflux Pump Failure (No flow)', 'FIC-204 < 20.0 kmol/h', 'Auto-start standby P-102B; Hold feed rate'],
        ['I-04', 'High Column Pressure (Overpress)', 'PT-202 > 135 kPa(a)', 'Open PCV-202B vent to flare; Trip steam'],
        ['I-05', 'Reflux Drum High Level', 'LT-203 > 85.0 %', 'Open LCV-203 full; Cut column feed rate'],
    ]
    t2_col_w = [1.6, 4.4, 3.4, 4.2]
    cad_draw_table_a4(ax, RX_BASE, 4.40, t2_headers, t2_rows, t2_col_w,
                      row_h=0.33, title='TABLE 2: SAFETY INTERLOCK & CAUSE-AND-EFFECT MATRIX',
                      title_sz=4.6, sz=3.7)
    
    # Save Outputs
    fig.savefig(out_pdf, format='pdf', dpi=300)
    fig.savefig(out_png, format='png', dpi=300)
    plt.close(fig)
    print(f"  [OK] DWG-05 generated: {os.path.basename(out_pdf)}")

if __name__ == '__main__':
    out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Ethanol_Water_Distillation_Drawings')
    os.makedirs(out_dir, exist_ok=True)
    generate_ethanol_dwg05(
        os.path.join(out_dir, '05_Ethanol_Column_PID_Instrumentation_CAD.pdf'),
        os.path.join(out_dir, '05_Ethanol_Column_PID_Instrumentation_CAD.png')
    )
