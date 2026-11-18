"""
A4 OPTIMIZED: DWG-05 ACETALDEHYDE COLUMN PIPING & INSTRUMENTATION DIAGRAM (P&ID)
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
    cad_valve, cad_instrument_bubble, cad_draw_table_a4, W, H, BK, GREY
)

def generate_acetaldehyde_dwg05(out_pdf, out_png):
    fig, ax = create_a4_canvas()
    draw_a4_border(ax)
    
    SUB_INFO = 'ACETALDEHYDE DISTILLATION (C-301)  |  12000 kg/h FEED (50 wt% AcH)  |  ID 2.00 m, R=3.89  |  ASME SEC VIII / TEMA'
    draw_a4_title_block(ax, 'PIPING & INSTRUMENTATION DIAGRAM (P&ID) — ISA-5.1',
                        'JU/ChE/ED/DWG-05', scale='SCHEMATIC (ISA-5.1)', date='17 / 11 / 2026', sub_info=SUB_INFO)
    
    # Drawing Header
    cad_text(ax, W/2, H - 1.25, 'PIPING & INSTRUMENTATION DIAGRAM (P&ID) — DISTILLATION SYSTEM (C-301)', sz=6.6, bold=True)
    cad_text(ax, W/2, H - 1.62, 'ISA-5.1 INSTRUMENTATION LOOPS: SENSITIVE TRAY CASCADE, SPLIT-RANGE PRESSURE, SUMP LEVEL & STEAM FLOODING INTERLOCKS', sz=4.4, bold=False)
    
    # ═════════════════════════════════════════════════════════════════════════
    # EQUIPMENT DRAWINGS (P&ID SCHEMATIC LAYOUT: LEFT HALF X in [1.0, 14.8])
    # ═════════════════════════════════════════════════════════════════════════
    
    # 1. DISTILLATION COLUMN C-301 (CX=7.6, Y=6.2 to 15.2)
    CX = 7.6
    CY_BOT = 6.2
    CY_TOP = 15.2
    CW = 1.30
    
    cad_rect(ax, CX - CW/2, CY_BOT, CW, CY_TOP - CY_BOT, lw=1.1, fill=True)
    cad_arc(ax, CX, CY_TOP, CW, 0.55, theta1=0, theta2=180, lw=1.1)
    cad_arc(ax, CX, CY_BOT, CW, 0.55, theta1=180, theta2=360, lw=1.1)
    
    # Column Tag Box (Upper Left clear area)
    cad_rect(ax, 3.8, 14.4, 2.6, 1.2, lw=0.85, fill=True)
    cad_text(ax, 5.1, 15.25, 'C-301', sz=5.5, bold=True)
    cad_text(ax, 5.1, 14.75, 'DISTILLATION COLUMN\nID 2000 mm | 24 TRAYS', sz=3.4, bold=True)
    
    # Skirt & Foundation Base
    cad_rect(ax, CX - CW/2, 4.2, CW, CY_BOT - 4.2, lw=0.85)
    cad_line(ax, CX - CW/2 - 0.25, 4.2, CX + CW/2 + 0.25, 4.2, lw=1.1)
    cad_circle(ax, CX, 5.2, 0.22, lw=0.6)
    cad_text(ax, CX, 5.2, 'ACCESS', sz=3.0, bold=True)
    
    # Internal Trays (Schematic)
    for i in range(11):
        yt = CY_TOP - 0.75 - i * 0.70
        is_feed = (i == 5) # Tray 13
        lw_t = 0.85 if is_feed else 0.40
        ls_t = '-' if is_feed else '--'
        col_t = '#008800' if is_feed else BK
        cad_line(ax, CX - CW/2 + 0.1, yt, CX + CW/2 - 0.1, yt, lw=lw_t, ls=ls_t, color=col_t)
        
    cad_text(ax, CX, 10.60, 'FEED TRAY 13', sz=3.2, bold=True, color='#008800')
    
    # 2. FEED SYSTEM & PREHEATER E-301 (X=1.0 to 6.95, Y=10.6)
    cad_line(ax, 1.0, 10.6, CX - CW/2, 10.6, lw=0.9)  # Feed line
    cad_arrow(ax, 1.8, 10.6, 2.1, 10.6, head_scale=5)
    cad_arrow(ax, CX - CW/2 - 0.35, 10.6, CX - CW/2, 10.6, head_scale=5)
    cad_text(ax, 1.0, 11.20, 'FEED 12,000 kg/h\n(50 wt% AcH, 60% Vap)', sz=3.6, bold=True, ha='left')
    
    # Feed Control Valve FCV-301
    cad_valve(ax, 2.8, 10.6, orientation='H', size=0.32, valve_type='CONTROL')
    cad_text(ax, 2.8, 10.15, 'FCV-301 (FC)', sz=3.2, bold=True)
    
    # Feed Preheater E-301
    cad_circle(ax, 4.4, 10.6, 0.48, lw=0.85, fill=True)
    cad_text(ax, 4.4, 11.45, 'E-301\nFEED PREHEATER\n(q = 0.40)', sz=3.4, bold=True)
    
    # Feed Flow Instruments FT-301 & FIC-301
    cad_instrument_bubble(ax, 1.8, 12.0, 'FT', '301', loc='FIELD', sz=3.6)
    cad_instrument_bubble(ax, 2.8, 12.0, 'FIC', '301', loc='DCS', sz=3.6)
    cad_line(ax, 1.8, 10.6, 1.8, 11.65, lw=0.45, ls='--')
    cad_line(ax, 2.15, 12.0, 2.45, 12.0, lw=0.45, ls='--')
    cad_line(ax, 2.8, 11.65, 2.8, 10.80, lw=0.45, ls='--') # to FCV-301
    
    # 3. REBOILER E-302 (X=3.6, Y=6.0)
    RBX, RBY = 3.6, 6.0
    cad_rect(ax, RBX - 0.38, RBY - 0.75, 0.76, 1.50, lw=0.85, fill=True)
    cad_text(ax, RBX, RBY, 'E-302\nREBOILER\n(3.91 MW)', sz=3.4, bold=True)
    
    # Liquid Recirculation: Sump to Reboiler
    cad_line(ax, CX - CW/2, CY_BOT + 0.4, RBX, CY_BOT + 0.4, lw=0.8)
    cad_line(ax, RBX, CY_BOT + 0.4, RBX, RBY - 0.75, lw=0.8)
    cad_arrow(ax, RBX, CY_BOT + 0.4, RBX, RBY - 0.70, head_scale=5)
    
    # Vapor Return: Reboiler to Column
    cad_line(ax, RBX, RBY + 0.75, RBX, CY_BOT + 1.4, lw=0.85)
    cad_line(ax, RBX, CY_BOT + 1.4, CX - CW/2, CY_BOT + 1.4, lw=0.85)
    cad_arrow(ax, CX - CW/2 - 0.35, CY_BOT + 1.4, CX - CW/2, CY_BOT + 1.4, head_scale=5)
    
    # Reboiler Steam Inlet Line & FCV-306
    cad_line(ax, 1.2, RBY, RBX - 0.38, RBY, lw=0.75)
    cad_arrow(ax, 1.5, RBY, 1.9, RBY, head_scale=5)
    cad_valve(ax, 2.4, RBY, orientation='H', size=0.30, valve_type='CONTROL')
    cad_text(ax, 2.4, RBY - 0.42, 'FCV-306 (FC)', sz=3.2, bold=True)
    cad_text(ax, 1.1, RBY + 0.35, 'STEAM 1.5 bar\n(6,458 kg/h)', sz=3.2, bold=True, ha='left')
    
    # 4. BOTTOMS DRAW & SUMP LEVEL CONTROL LCV-307
    cad_line(ax, CX, CY_BOT - 0.28, CX, 3.8, lw=0.8)
    cad_line(ax, CX, 3.8, 3.0, 3.8, lw=0.8)
    cad_valve(ax, 4.8, 3.8, orientation='H', size=0.30, valve_type='CONTROL')
    cad_text(ax, 4.8, 3.42, 'LCV-307 (FC)', sz=3.2, bold=True)
    cad_arrow(ax, 3.4, 3.8, 3.0, 3.8, head_scale=5)
    cad_text(ax, 2.9, 3.8, 'BOTTOMS TO COOLER (E-305)', sz=3.2, bold=True, ha='right')
    
    # Sump Level Instruments LT-307 & LIC-307
    cad_instrument_bubble(ax, 6.0, 4.8, 'LT', '307', loc='FIELD', sz=3.6)
    cad_instrument_bubble(ax, 6.0, 3.8, 'LIC', '307', loc='DCS', sz=3.6)
    cad_line(ax, CX - CW/2, CY_BOT, 6.0, 4.8, lw=0.45, ls='--')
    cad_line(ax, 6.0, 4.45, 6.0, 4.15, lw=0.45, ls='--')
    cad_line(ax, 5.65, 3.8, 5.0, 3.8, lw=0.45, ls='--') # to LCV-307
    
    # 5. OVERHEAD CONDENSER E-303 (CDX=12.0, CDY=15.4)
    CDX, CDY = 12.0, 15.4
    cad_rect(ax, CDX - 1.0, CDY - 0.40, 2.0, 0.80, lw=0.85, fill=True)
    cad_text(ax, CDX, CDY + 0.70, 'E-303 TOTAL CONDENSER\n4733.9 kW (CHW)', sz=3.8, bold=True)
    
    # Overhead Vapor Line from Column to E-303
    cad_line(ax, CX, CY_TOP + 0.28, CX, 16.4, lw=0.9)
    cad_line(ax, CX, 16.4, CDX, 16.4, lw=0.9)
    cad_line(ax, CDX, 16.4, CDX, CDY + 0.40, lw=0.9)
    cad_arrow(ax, CDX, 16.3, CDX, CDY + 0.42, head_scale=5)
    cad_text(ax, 9.6, 16.70, 'OVERHEAD VAPOR (14" DN350)', sz=3.4, bold=True)
    
    # PSV-301 Safety Relief Valve to Flare Header
    cad_valve(ax, CX, 17.2, orientation='V', size=0.28, valve_type='SRV')
    cad_line(ax, CX, 16.4, CX, 17.05, lw=0.7)
    cad_line(ax, CX, 17.35, CX, 17.7, lw=0.7)
    cad_line(ax, CX, 17.7, 9.2, 17.7, lw=0.7)
    cad_arrow(ax, 8.8, 17.7, 9.3, 17.7, head_scale=5)
    cad_text(ax, 9.4, 17.7, 'PSV-301 (0.35 MPa g) TO FLARE HEADER', sz=3.3, bold=True, ha='left')
    
    # Chilled Water Line & TV-302A (Cooling Control)
    cad_line(ax, 14.6, CDY, CDX + 1.0, CDY, lw=0.7)
    cad_arrow(ax, 14.4, CDY, 14.1, CDY, head_scale=4)
    cad_valve(ax, 13.6, CDY, orientation='H', size=0.28, valve_type='CONTROL')
    cad_text(ax, 13.6, CDY - 0.42, 'TV-302A (FO)', sz=3.2, bold=True)
    cad_text(ax, 14.65, CDY + 0.30, 'CHW IN (7 C)', sz=3.2, bold=True, ha='right')
    
    # 6. REFLUX DRUM V-301 (RX=12.0, RY=12.2)
    RX, RY = 12.0, 12.2
    cad_rect(ax, RX - 0.75, RY - 0.35, 1.50, 0.70, lw=0.85, fill=True)
    cad_arc(ax, RX - 0.75, RY, 0.35, 0.70, theta1=90, theta2=270, lw=0.85)
    cad_arc(ax, RX + 0.75, RY, 0.35, 0.70, theta1=270, theta2=90, lw=0.85)
    cad_text(ax, RX, RY, 'V-301\nREFLUX DRUM\n6.0 m3', sz=3.6, bold=True)
    
    # Condensate drain line E-303 to V-301
    cad_line(ax, CDX, CDY - 0.40, CDX, RY + 0.35, lw=0.8)
    cad_arrow(ax, CDX, RY + 0.60, CDX, RY + 0.38, head_scale=5)
    
    # Off-Gas Vent Line & PCV-302B (Split Range Pressure Control)
    cad_line(ax, RX + 0.55, RY + 0.35, RX + 0.55, 13.6, lw=0.6)
    cad_line(ax, RX + 0.55, 13.6, 14.6, 13.6, lw=0.6)
    cad_valve(ax, 13.4, 13.6, orientation='H', size=0.26, valve_type='CONTROL')
    cad_text(ax, 13.4, 14.02, 'PCV-302B (FC)', sz=3.2, bold=True)
    cad_arrow(ax, 14.2, 13.6, 14.6, 13.6, head_scale=5)
    cad_text(ax, 14.65, 13.25, 'TO FLARE / OFF-GAS', sz=3.2, bold=True, ha='right')
    
    # 7. REFLUX PUMPS P-302A/B & LINES (RPX=12.0, RPY=9.4)
    RPX, RPY = 12.0, 9.4
    cad_circle(ax, RPX, RPY, 0.34, lw=0.85, fill=True)
    cad_text(ax, RPX, RPY - 0.58, 'P-302A/B\nREFLUX PUMPS', sz=3.5, bold=True)
    cad_line(ax, RX, RY - 0.35, RX, RPY + 0.34, lw=0.8)
    
    # Pump Discharge Manifold
    cad_line(ax, RPX + 0.34, RPY, 13.0, RPY, lw=0.8)
    
    # Branch 1: Reflux Return Line to Column Top (Tray 1)
    cad_line(ax, 13.0, RPY, 13.0, 14.4, lw=0.8)
    cad_line(ax, 13.0, 14.4, CX + CW/2, 14.4, lw=0.8)
    cad_arrow(ax, CX + CW/2 + 0.35, 14.4, CX + CW/2, 14.4, head_scale=5)
    cad_valve(ax, 10.4, 14.4, orientation='H', size=0.28, valve_type='CONTROL')
    cad_text(ax, 10.4, 14.80, 'FCV-304 (FO)', sz=3.2, bold=True)
    cad_text(ax, 9.4, 14.05, 'REFLUX (R=3.89)', sz=3.2, bold=True)
    
    # Branch 2: Distillate Product Line
    cad_line(ax, 13.0, RPY, 14.6, RPY, lw=0.8)
    cad_valve(ax, 13.8, RPY, orientation='H', size=0.28, valve_type='CONTROL')
    cad_text(ax, 13.8, RPY - 0.42, 'LCV-303 (FC)', sz=3.2, bold=True)
    cad_arrow(ax, 14.2, RPY, 14.6, RPY, head_scale=5)
    cad_text(ax, 14.65, RPY + 0.35, 'DISTILLATE (D)\n(97 wt% AcH)', sz=3.3, bold=True, ha='right')
    
    # ═════════════════════════════════════════════════════════════════════════
    # ISA-5.1 CONTROL LOOPS & DCS TRANSMITTERS
    # ═════════════════════════════════════════════════════════════════════════
    
    # Loop 2: Column Overhead Pressure Control (PT-302 -> PIC-302 Split Range)
    cad_instrument_bubble(ax, 10.4, 17.4, 'PT', '302', loc='FIELD', sz=3.6)
    cad_instrument_bubble(ax, 11.6, 17.4, 'PIC', '302', loc='DCS', sz=3.6)
    cad_line(ax, 10.4, 16.4, 10.4, 17.05, lw=0.45, ls='--')
    cad_line(ax, 10.75, 17.4, 11.25, 17.4, lw=0.45, ls='--')
    cad_line(ax, 11.6, 17.05, 13.6, CDY + 0.15, lw=0.45, ls='--') # to TV-302A
    cad_line(ax, 11.95, 17.4, 13.4, 13.75, lw=0.45, ls='--')      # to PCV-302B
    
    # Loop 3: Reflux Drum Level Control (LT-303 -> LIC-303)
    cad_instrument_bubble(ax, 14.2, 12.6, 'LT', '303', loc='FIELD', sz=3.5)
    cad_instrument_bubble(ax, 14.2, 11.5, 'LIC', '303', loc='DCS', sz=3.5)
    cad_line(ax, RX + 0.75, RY, 13.85, 12.6, lw=0.45, ls='--')
    cad_line(ax, 14.2, 12.25, 14.2, 11.85, lw=0.45, ls='--')
    cad_line(ax, 14.2, 11.15, 13.8, RPY + 0.15, lw=0.45, ls='--') # to LCV-303
    
    # Loop 4: Sensitive Tray 18 Temperature Cascade to Reflux (TT-304 -> TIC-304 -> FIC-304)
    # Tray 18 tap at column right shell (elevation 8.8 cm)
    cad_instrument_bubble(ax, 9.2, 8.8, 'TT', '304', loc='FIELD', sz=3.6)
    cad_instrument_bubble(ax, 9.2, 11.0, 'TIC', '304', loc='DCS', sz=3.6)
    cad_instrument_bubble(ax, 9.2, 12.5, 'FIC', '304', loc='DCS', sz=3.6)
    cad_line(ax, CX + CW/2, 8.8, 8.85, 8.8, lw=0.45, ls='--')
    cad_line(ax, 9.2, 9.15, 9.2, 10.65, lw=0.45, ls='--')
    cad_line(ax, 9.2, 11.35, 9.2, 12.15, lw=0.45, ls='--')
    cad_line(ax, 9.55, 12.5, 10.4, 14.25, lw=0.45, ls='--') # to FCV-304
    cad_text(ax, 9.2, 13.30, 'TRAY 18 TEMP CASCADE\n(REFLUX RATIO R=3.89)', sz=3.0, bold=True, color='#004488')
    
    # Loop 5: Column Differential Pressure Flooding Interlock (PDIT-305)
    cad_instrument_bubble(ax, 5.8, 12.8, 'PDIT', '305', loc='DCS', sz=3.4)
    cad_line(ax, CX - CW/2, CY_TOP - 0.4, 5.8, 13.15, lw=0.40, ls='--') # High tap
    cad_line(ax, CX - CW/2, CY_BOT + 0.8, 5.8, 12.45, lw=0.40, ls='--') # Low tap
    cad_line(ax, 5.8, 12.45, 2.4, RBY + 0.15, lw=0.45, ls='--')          # Interlock to steam FCV-306
    
    # ═════════════════════════════════════════════════════════════════════════
    # RIGHT HALF: INSTRUMENT SCHEDULE & INTERLOCK LOGIC SCHEDULE (X >= 15.4)
    # ═════════════════════════════════════════════════════════════════════════
    RX_BASE = 15.4
    
    # 1. Instrument Schedule Table (Y=10.5 to 14.3)
    t1_headers = ['TAG NO.', 'SERVICE / LOOP', 'RANGE', 'SETPOINT', 'ACTION / FAIL']
    t1_rows = [
        ['FT/FIC-301', 'Feed Flow to Column', '0 - 15,000 kg/h', '12,000 kg/h', 'FCV-301 (Fail Closed)'],
        ['PT/PIC-302', 'Top Vapor Pressure', '0 - 200 kPa(a)', '105.0 kPa', 'Split: TV-302A (FO) / PCV-302B (FC)'],
        ['LT/LIC-303', 'Reflux Drum Level', '0 - 100 %', '50.0 % level', 'LCV-303 (Fail Closed)'],
        ['TT/TIC-304', 'Tray 18 Sensitive Temp', '20 - 50 C', '28.4 C', 'Cascades to Reflux FIC-304'],
        ['FT/FIC-304', 'Reflux Liquid Flow', '0 - 35,000 kg/h', '23,313 kg/h', 'FCV-304 (Fail Open - FO)'],
        ['PDIT-305', 'Column Differential Press.', '0 - 30.0 kPa', '14.5 kPa', 'Alarm High @ 18.5 kPa (Flooding)'],
        ['FT/FIC-306', 'Reboiler 1.5 bar Steam', '0 - 10,000 kg/h', '6,458 kg/h', 'FCV-306 (Fail Closed) w/ DP override'],
        ['LT/LIC-307', 'Bottoms Sump Level', '0 - 100 %', '50.0 % level', 'LCV-307 (Fail Closed)'],
        ['PSV-301A/B', 'Column Overpressure Relief', '0 - 0.50 MPa', '0.35 MPa(g)', 'Pop Action to Flare Header'],
    ]
    t1_col_w = [2.2, 4.4, 2.4, 2.2, 2.2]
    cad_draw_table_a4(ax, RX_BASE, 10.60, t1_headers, t1_rows, t1_col_w,
                      row_h=0.33, title='TABLE 1: ISA-5.1 INSTRUMENT & CONTROL LOOP SCHEDULE',
                      title_sz=4.6, sz=3.6)
    
    # 2. Safety Interlock & Cause-and-Effect Logic Table (Y=6.6 to 9.2)
    t2_headers = ['TRIP ID', 'INITIATING EVENT', 'LOGIC / SETPOINT', 'AUTOMATED SAFETY ACTION']
    t2_rows = [
        ['I-01', 'Column High DP (Flooding)', 'PDIT-305 > 18.5 kPa', 'Cut reboiler steam FCV-306 to 30%; Alarm'],
        ['I-02', 'Low Sump Level (Dryout)', 'LT-307 < 15.0 %', 'Trip steam FCV-306 closed; Stop bottoms draw'],
        ['I-03', 'Reflux Pump Failure (No flow)', 'FIC-304 < 5,000 kg/h', 'Auto-start standby P-302B; Hold feed rate'],
        ['I-04', 'High Column Pressure (Overpress)', 'PT-302 > 135 kPa(a)', 'Open PCV-302B vent to flare; Trip steam'],
        ['I-05', 'Reflux Drum High Level', 'LT-303 > 85.0 %', 'Open LCV-303 full; Cut column feed rate'],
    ]
    t2_col_w = [1.6, 4.4, 3.4, 4.0]
    cad_draw_table_a4(ax, RX_BASE, 6.60, t2_headers, t2_rows, t2_col_w,
                      row_h=0.33, title='TABLE 2: SAFETY INTERLOCK & CAUSE-AND-EFFECT MATRIX',
                      title_sz=4.6, sz=3.6)
    
    # 3. Process Control Philosophy & SIS Notes Box (Y=3.35 to 6.20)
    N_X = RX_BASE
    N_Y = 3.35
    H_N = 2.85
    W_N = 13.4
    cad_rect(ax, N_X, N_Y, W_N, H_N, lw=0.85, fill=True)
    cad_rect(ax, N_X, N_Y + H_N - 0.45, W_N, 0.45, lw=0.7, fill=True)
    cad_text(ax, N_X + W_N/2, N_Y + H_N - 0.22, 'PROCESS CONTROL PHILOSOPHY & SIS INTERLOCK NOTES', sz=4.4, bold=True)
    
    notes_dwg5 = [
        "1. DUAL QUALITY CASCADE: Sensitive Tray 18 temp (TIC-304) cascades to reflux FIC-304 (R=3.89).",
        "2. SPLIT-RANGE PRESSURE (PIC-302): Modulates condenser CHW TV-302A (0-50%) and vent PCV-302B (50-100%).",
        "3. SUMP & REFLUX LEVEL (LIC-307 / LIC-303): Modulate draw valves with 5-min surge capacity.",
        "4. COLUMN DP INTERLOCK (PDIT-305): Throttles 1.5 bar steam FCV-306 on high DP (> 18.5 kPa flooding).",
    ]
    for idx, nl in enumerate(notes_dwg5):
        cad_text(ax, N_X + 0.25, N_Y + H_N - 0.80 - idx * 0.55, nl, sz=3.4, bold=False, ha='left')
    
    # Save Outputs
    fig.savefig(out_pdf, format='pdf', dpi=300)
    fig.savefig(out_png, format='png', dpi=300)
    plt.close(fig)
    print(f"  [OK] DWG-05 generated: {os.path.basename(out_pdf)}")

if __name__ == '__main__':
    out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Acetaldehyde_PropyleneOxide_Distillation_Drawings')
    os.makedirs(out_dir, exist_ok=True)
    generate_acetaldehyde_dwg05(
        os.path.join(out_dir, '05_Acetaldehyde_Column_PID_Instrumentation_CAD.pdf'),
        os.path.join(out_dir, '05_Acetaldehyde_Column_PID_Instrumentation_CAD.png')
    )
