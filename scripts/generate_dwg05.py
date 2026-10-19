"""
DWG-05: DETAILED PIPING & INSTRUMENTATION DIAGRAM (P&ID) CAD
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
    cad_hatch_rect, cad_valve, cad_instrument_bubble, cad_draw_table,
    W, H, BK, GREY
)

def generate_dwg05():
    fig, ax = create_cad_canvas()
    draw_sheet_border(ax)
    
    # ═════════════════════════════════════════════════════════════════════════
    # SHEET LAYOUT: ISA-5.1 DETAILED P&ID SCHEMATIC & CONTROL ARCHITECTURE
    # Left/Center: Main Process Equipment & Instrumentation (X = 2.5 to 52.0, Y = 7.2 to 52.0)
    # Right Panel: Stream Tables, Line Schedule & Control Logic (X = 53.5 to 81.5, Y = 7.2 to 52.0)
    # ═════════════════════════════════════════════════════════════════════════
    
    # Main Column Centerline & Coordinates:
    CX_COL = 27.5
    CY_COL = 28.5
    W_COL = 4.2  # 750 mm ID scaled for P&ID
    H_COL = 26.0 # Column shell height
    
    # ─────────────────────────────────────────────────────────────────────────
    # 1. CENTRAL EQUIPMENT: PACKED ABSORPTION COLUMN (C-101)
    # ─────────────────────────────────────────────────────────────────────────
    # Column Shell
    cad_rect(ax, CX_COL - W_COL/2, CY_COL - H_COL/2, W_COL, H_COL, lw=1.4, fill=True)
    # Top and Bottom Ellipsoidal Heads
    cad_arc(ax, CX_COL, CY_COL + H_COL/2, W_COL, 2.2, theta1=0, theta2=180, lw=1.4)
    cad_arc(ax, CX_COL, CY_COL - H_COL/2, W_COL, 2.2, theta1=180, theta2=360, lw=1.4)
    cad_line(ax, CX_COL, CY_COL - H_COL/2 - 2.5, CX_COL, CY_COL + H_COL/2 + 2.5, lw=0.4, ls='-.')
    
    # Internals Representation inside C-101
    # Demister Pad
    y_pid_dem = CY_COL + H_COL/2 - 2.5
    cad_rect(ax, CX_COL - W_COL/2 + 0.2, y_pid_dem - 0.5, W_COL - 0.4, 1.0, lw=0.9, fill=True)
    cad_hatch_rect(ax, CX_COL - W_COL/2 + 0.2, y_pid_dem - 0.5, W_COL - 0.4, 1.0, pitch=0.20, lw=0.35)
    cad_text(ax, CX_COL, y_pid_dem, 'DEMISTER PAD', sz=4.2, bold=True, bg='white')
    
    # Liquid Distributor
    y_pid_dist = CY_COL + H_COL/2 - 5.0
    cad_line(ax, CX_COL - W_COL/2 + 0.3, y_pid_dist, CX_COL + W_COL/2 - 0.3, y_pid_dist, lw=1.1)
    for sx in np.linspace(CX_COL - W_COL/2 + 0.6, CX_COL + W_COL/2 - 0.6, 5):
        cad_arrow(ax, sx, y_pid_dist, sx, y_pid_dist - 0.8, lw=0.7, head_scale=5)
    cad_text(ax, CX_COL, y_pid_dist + 0.5, 'DISTRIBUTOR', sz=4.2, bold=True)
    
    # Packed Bed (4500 mm depth)
    y_pid_bed_top = CY_COL + H_COL/2 - 6.5
    y_pid_bed_btm = CY_COL - H_COL/2 + 5.5
    h_pid_bed = y_pid_bed_top - y_pid_bed_btm
    cad_rect(ax, CX_COL - W_COL/2 + 0.2, y_pid_bed_btm, W_COL - 0.4, h_pid_bed, lw=0.9, fill=True)
    cad_hatch_rect(ax, CX_COL - W_COL/2 + 0.2, y_pid_bed_btm, W_COL - 0.4, h_pid_bed, pitch=0.35, angle=45, lw=0.35, color=GREY)
    cad_hatch_rect(ax, CX_COL - W_COL/2 + 0.2, y_pid_bed_btm, W_COL - 0.4, h_pid_bed, pitch=0.35, angle=-45, lw=0.35, color=GREY)
    cad_text(ax, CX_COL, CY_COL,
             'PACKED BED (Z = 4500 mm)\n'
             '25-mm CERAMIC RASCHIG RINGS\n'
             'VOLUME Vp = 1.79 m³\n'
             'MASS Mp = 1.22 tonnes',
             sz=4.8, bold=True, bg='white')
    
    # Packing Support Grid
    cad_line(ax, CX_COL - W_COL/2 + 0.1, y_pid_bed_btm, CX_COL + W_COL/2 - 0.1, y_pid_bed_btm, lw=1.2)
    cad_line(ax, CX_COL - W_COL/2 + 0.1, y_pid_bed_btm - 0.4, CX_COL + W_COL/2 - 0.1, y_pid_bed_btm - 0.4, lw=1.2)
    cad_text(ax, CX_COL, y_pid_bed_btm - 0.8, 'SUPPORT GRID', sz=4.0, bold=True)
    
    # Gas Inlet Deflector
    y_pid_gas_in = CY_COL - H_COL/2 + 3.2
    p_pid_def = [(CX_COL - 1.2, y_pid_gas_in - 0.4), (CX_COL, y_pid_gas_in + 0.5), (CX_COL + 1.2, y_pid_gas_in - 0.4)]
    ax.add_patch(Polygon(p_pid_def, closed=False, ec=BK, lw=1.1, fill=False))
    
    # Bottom Liquid Sump & Anti-Vortex Baffle
    cad_line(ax, CX_COL, CY_COL - H_COL/2 - 0.8, CX_COL, CY_COL - H_COL/2 + 0.8, lw=1.0)
    
    # Skirt Support Body
    cad_rect(ax, CX_COL - W_COL/2, CY_COL - H_COL/2 - 4.5, W_COL, 3.5, lw=1.1, fill=True)
    cad_rect(ax, CX_COL - W_COL/2 - 0.6, CY_COL - H_COL/2 - 4.8, W_COL + 1.2, 0.3, lw=1.0, fill=True) # Base ring
    cad_text(ax, CX_COL, CY_COL - H_COL/2 - 2.8, 'SKIRT SUPPORT', sz=4.5, bold=True)
    
    # Equipment Tag Callout Box
    cad_rect(ax, CX_COL - 3.5, CY_COL + H_COL/2 + 2.8, 7.0, 1.8, lw=1.2, fill=True)
    cad_text(ax, CX_COL, CY_COL + H_COL/2 + 4.0, 'C-101', sz=8.0, bold=True)
    cad_text(ax, CX_COL, CY_COL + H_COL/2 + 3.2, 'PACKED ABSORPTION COLUMN', sz=4.8, bold=True)
    
    # Nozzle Tags on Column
    cad_balloon(ax, CX_COL - W_COL/2 - 0.8, y_pid_gas_in, 'N1', radius=0.35, sz=5.0)
    cad_balloon(ax, CX_COL + W_COL/2 + 0.8, y_pid_dist, 'N3', radius=0.35, sz=5.0)
    cad_balloon(ax, CX_COL, CY_COL - H_COL/2 - 1.8, 'N4', radius=0.35, sz=5.0)
    cad_balloon(ax, CX_COL + 1.8, CY_COL - H_COL/2 - 1.8, 'N5', radius=0.35, sz=5.0)
    cad_balloon(ax, CX_COL, CY_COL + H_COL/2 + 1.8, 'N6', radius=0.35, sz=5.0)
    cad_balloon(ax, CX_COL - W_COL/2 - 0.8, y_pid_bed_btm - 0.2, 'N7', radius=0.35, sz=5.0)
    cad_balloon(ax, CX_COL - W_COL/2 - 0.8, y_pid_bed_top + 0.2, 'N8', radius=0.35, sz=5.0)
    cad_balloon(ax, CX_COL + W_COL/2 + 0.8, y_pid_dem + 1.2, 'N11', radius=0.35, sz=5.0)
    
    # ─────────────────────────────────────────────────────────────────────────
    # 2. FEED GAS PIPING & INSTRUMENTATION (STREAM 1)
    # ─────────────────────────────────────────────────────────────────────────
    y_gline = y_pid_gas_in
    # Feed gas line from left (X = 3.5 to CX_COL - W_COL/2)
    cad_line(ax, 3.5, y_gline, CX_COL - W_COL/2, y_gline, lw=1.6)
    cad_arrow(ax, 5.0, y_gline, 6.0, y_gline, lw=1.4, head_scale=9)
    cad_text(ax, 5.5, y_gline + 0.6, 'STREAM 1: WET Br2 FEED GAS\n6"-BRG-101-CS/PVDF-N (0.25 m3/s, 2.0 mol% Br2)', sz=4.8, bold=True)
    
    # Feed Blower B-101
    cad_circle(ax, 9.5, y_gline, 1.2, lw=1.2, fill=True)
    cad_line(ax, 9.5, y_gline - 1.2, 9.5 + 0.8, y_gline + 0.9, lw=1.0)
    cad_line(ax, 9.5, y_gline - 1.2, 9.5 - 0.8, y_gline + 0.9, lw=1.0)
    cad_text(ax, 9.5, y_gline - 1.8, 'B-101\nFEED BLOWER (VFD)', sz=4.8, bold=True)
    
    # Gas Inlet Valve XV-101 (Emergency Shutoff Valve, Fail-Closed)
    cad_valve(ax, 13.5, y_gline, orientation='H', size=0.8, valve_type='CONTROL')
    cad_text(ax, 13.5, y_gline - 0.8, 'XV-101\n(FC)', sz=4.5, bold=True)
    
    # Gas Flow Transmitter (FT-101 / FIC-101)
    cad_circle(ax, 16.5, y_gline, 0.12, fill=True)
    cad_line(ax, 16.5, y_gline, 16.5, y_gline + 2.5, lw=0.6, ls='--')
    cad_instrument_bubble(ax, 16.5, y_gline + 2.5, 'FT', '101', loc='FIELD')
    cad_line(ax, 16.5, y_gline + 3.1, 16.5, y_gline + 4.5, lw=0.6, ls='--')
    cad_instrument_bubble(ax, 16.5, y_gline + 4.5, 'FFIC', '102', loc='DCS') # Feeds water ratio controller!
    
    # Gas Composition Analyzer (AI-101 / AT-101, Bromine Analyzer)
    cad_circle(ax, 19.5, y_gline, 0.12, fill=True)
    cad_line(ax, 19.5, y_gline, 19.5, y_gline + 2.5, lw=0.6, ls='--')
    cad_instrument_bubble(ax, 19.5, y_gline + 2.5, 'AT', '101', loc='FIELD')
    cad_line(ax, 19.5, y_gline + 3.1, 19.5, y_gline + 4.5, lw=0.6, ls='--')
    cad_instrument_bubble(ax, 19.5, y_gline + 4.5, 'AI', '101', loc='DCS')
    cad_text(ax, 19.5, y_gline + 5.5, 'Br2: 2.0 mol%', sz=4.2, bold=True)
    
    # Gas Inlet Pressure & Temperature (PT-101, TT-101)
    cad_circle(ax, 22.5, y_gline, 0.12, fill=True)
    cad_line(ax, 22.5, y_gline, 22.5, y_gline - 2.5, lw=0.6, ls='--')
    cad_instrument_bubble(ax, 22.5, y_gline - 2.5, 'PT', '101', loc='DCS')
    cad_text(ax, 22.5, y_gline - 3.5, '803 mmHg', sz=4.2, bold=True)
    
    cad_circle(ax, 24.2, y_gline, 0.12, fill=True)
    cad_line(ax, 24.2, y_gline, 24.2, y_gline - 2.5, lw=0.6, ls='--')
    cad_instrument_bubble(ax, 24.2, y_gline - 2.5, 'TT', '101', loc='DCS')
    cad_text(ax, 24.2, y_gline - 3.5, '25.0 °C', sz=4.2, bold=True)
    
    # ─────────────────────────────────────────────────────────────────────────
    # 3. SCRUBBING WATER SUPPLY & RATIO CONTROL LOOP (STREAM 3)
    # ─────────────────────────────────────────────────────────────────────────
    y_wline = CY_COL + H_COL/2 - 5.0
    # Water Feed Line coming from top-right down to N3
    cad_line(ax, 48.0, 48.0, 40.0, 48.0, lw=1.6)
    cad_line(ax, 40.0, 48.0, 40.0, y_wline, lw=1.6)
    cad_line(ax, 40.0, y_wline, CX_COL + W_COL/2, y_wline, lw=1.6)
    cad_arrow(ax, 45.0, 48.0, 44.0, 48.0, lw=1.4, head_scale=8)
    cad_arrow(ax, 35.0, y_wline, 34.0, y_wline, lw=1.4, head_scale=8)
    cad_text(ax, 45.0, 49.0, 'STREAM 3: FRESH SCRUBBING WATER\n3"-PWT-103-CS-N (L = 17.25 kg/s = 62.1 t/h)', sz=4.8, bold=True)
    
    # Water Circulation Pumps P-101A/B (1 Operating + 1 Standby)
    cad_circle(ax, 40.0, 44.5, 0.9, lw=1.1, fill=True)
    cad_text(ax, 42.5, 44.5, 'P-101A/B\nWATER PUMPS\n(1W + 1S)', sz=4.5, ha='left', bold=True)
    
    # Water Flow Control Valve FCV-102 (Fail-Open FO)
    cad_valve(ax, 36.5, y_wline, orientation='H', size=0.8, valve_type='CONTROL')
    cad_text(ax, 36.5, y_wline - 0.8, 'FCV-102\n(FO)', sz=4.5, bold=True)
    
    # Water Flowmeter FT-102 & Ratio Controller connection
    cad_circle(ax, 40.0, y_wline + 2.5, 0.12, fill=True)
    cad_line(ax, 40.0, y_wline + 2.5, 43.5, y_wline + 2.5, lw=0.6, ls='--')
    cad_instrument_bubble(ax, 43.5, y_wline + 2.5, 'FT', '102', loc='FIELD')
    # Signal from FT-102 to FFIC-102
    cad_line(ax, 43.5, y_wline + 3.1, 43.5, y_gline + 4.5, lw=0.6, ls=':')
    cad_line(ax, 43.5, y_gline + 4.5, 17.1, y_gline + 4.5, lw=0.6, ls=':')
    # Control output from FFIC-102 to FCV-102 actuator
    cad_line(ax, 16.5, y_gline + 5.1, 16.5, y_wline + 5.5, lw=0.6, ls=':')
    cad_line(ax, 16.5, y_wline + 5.5, 36.5, y_wline + 5.5, lw=0.6, ls=':')
    cad_line(ax, 36.5, y_wline + 5.5, 36.5, y_wline + 0.8, lw=0.6, ls=':')
    cad_text(ax, 26.0, y_wline + 6.0,
             'AUTOMATIC RATIO CONTROL LOOP (FFIC-102): MAINTAINS L/Lmin = 1.40 CONSTANT\n'
             'ACROSS WIDE FEED GAS TURNDOWN (RATIO L/G = 90.5 mol/mol)', sz=4.6, bold=True, bg='white')
    
    # ─────────────────────────────────────────────────────────────────────────
    # 4. DIFFERENTIAL PRESSURE TRANSMITTER ACROSS PACKED BED (PDT-101)
    # ─────────────────────────────────────────────────────────────────────────
    y_pdt_lo = y_pid_bed_btm - 0.2
    y_pdt_hi = y_pid_bed_top + 0.2
    x_pdt_tap = CX_COL - W_COL/2
    x_pdt_inst = x_pdt_tap - 4.5
    
    # Impulse lines from N7 and N8
    cad_line(ax, x_pdt_tap, y_pdt_lo, x_pdt_inst, y_pdt_lo, lw=0.7)
    cad_line(ax, x_pdt_tap, y_pdt_hi, x_pdt_inst, y_pdt_hi, lw=0.7)
    cad_line(ax, x_pdt_inst, y_pdt_lo, x_pdt_inst, CY_COL - 0.8, lw=0.7)
    cad_line(ax, x_pdt_inst, y_pdt_hi, x_pdt_inst, CY_COL + 0.8, lw=0.7)
    
    # 3-Valve Manifold & PDT-101 Transmitter
    cad_valve(ax, x_pdt_inst, y_pdt_lo + 1.2, orientation='V', size=0.4, valve_type='GATE')
    cad_valve(ax, x_pdt_inst, y_pdt_hi - 1.2, orientation='V', size=0.4, valve_type='GATE')
    cad_instrument_bubble(ax, x_pdt_inst, CY_COL, 'PDT', '101', loc='FIELD')
    cad_line(ax, x_pdt_inst - 0.6, CY_COL, x_pdt_inst - 1.8, CY_COL, lw=0.6, ls='--')
    cad_instrument_bubble(ax, x_pdt_inst - 1.8, CY_COL, 'PDI', '101', loc='DCS')
    cad_text(ax, x_pdt_inst - 1.8, CY_COL - 1.2,
             'PDAH-101 (80% FLOOD ALARM)\n'
             'PDAL-101 (CHANNELLING ALARM)\n'
             'NORMAL ΔP = 1.15 kPa (115 mm H2O)', sz=4.4, bold=True, bg='white')
    
    # ─────────────────────────────────────────────────────────────────────────
    # 5. BOTTOM LIQUID LEVEL CONTROL & RICH WATER DISCHARGE (STREAM 4)
    # ─────────────────────────────────────────────────────────────────────────
    y_btm_nozzle = CY_COL - H_COL/2 - 1.8
    # Bottom piping
    cad_line(ax, CX_COL, y_btm_nozzle, CX_COL, y_btm_nozzle - 2.5, lw=1.6)
    cad_line(ax, CX_COL, y_btm_nozzle - 2.5, 48.0, y_btm_nozzle - 2.5, lw=1.6)
    cad_arrow(ax, 38.0, y_btm_nozzle - 2.5, 39.0, y_btm_nozzle - 2.5, lw=1.4, head_scale=8)
    cad_text(ax, 40.0, y_btm_nozzle - 1.8,
             'STREAM 4: RICH BROMINE WATER OUTLET\n3"-RBL-104-CS/PVDF-N (TO BROMINE STRIPPER)', sz=4.8, bold=True)
    
    # Bottom Level Control Valve LCV-101 (Fail-Closed FC)
    cad_valve(ax, 34.0, y_btm_nozzle - 2.5, orientation='H', size=0.8, valve_type='CONTROL')
    cad_text(ax, 34.0, y_btm_nozzle - 3.5, 'LCV-101\n(FC)', sz=4.5, bold=True)
    
    # Level Transmitter (LT-101) & Level Gauge (LG-101) on external bridle
    x_bridle = CX_COL + W_COL/2 + 2.2
    y_sump_hi = CY_COL - H_COL/2 + 2.0
    y_sump_lo = CY_COL - H_COL/2 - 0.5
    cad_line(ax, CX_COL + W_COL/2, y_sump_hi, x_bridle, y_sump_hi, lw=0.7)
    cad_line(ax, CX_COL + W_COL/2, y_sump_lo, x_bridle, y_sump_lo, lw=0.7)
    cad_line(ax, x_bridle, y_sump_lo, x_bridle, y_sump_hi, lw=0.9)
    # Level transmitter bubble
    cad_instrument_bubble(ax, x_bridle + 1.8, (y_sump_hi + y_sump_lo)/2, 'LT', '101', loc='FIELD')
    cad_line(ax, x_bridle, (y_sump_hi + y_sump_lo)/2, x_bridle + 1.2, (y_sump_hi + y_sump_lo)/2, lw=0.6, ls='--')
    cad_instrument_bubble(ax, x_bridle + 1.8, (y_sump_hi + y_sump_lo)/2 - 1.8, 'LIC', '101', loc='DCS')
    # Signal from LIC-101 to LCV-101
    cad_line(ax, x_bridle + 1.8, (y_sump_hi + y_sump_lo)/2 - 2.4, x_bridle + 1.8, y_btm_nozzle - 2.5, lw=0.6, ls=':')
    cad_line(ax, x_bridle + 1.8, y_btm_nozzle - 2.5, 34.0, y_btm_nozzle - 2.5, lw=0.6, ls=':')
    cad_text(ax, x_bridle + 2.6, (y_sump_hi + y_sump_lo)/2, 'RADAR LEVEL TRANSMITTER\n(SUMP LEVEL CONTROL 50%)', sz=4.2, ha='left', bold=True)
    
    # ─────────────────────────────────────────────────────────────────────────
    # 6. OVERHEAD TREATED GAS EMISSION & RELIEF SYSTEM (STREAM 2)
    # ─────────────────────────────────────────────────────────────────────────
    y_top_nozzle = CY_COL + H_COL/2 + 1.8
    # Overhead Line
    cad_line(ax, CX_COL, y_top_nozzle, CX_COL, 50.0, lw=1.6)
    cad_line(ax, CX_COL, 50.0, 3.5, 50.0, lw=1.6)
    cad_arrow(ax, 15.0, 50.0, 14.0, 50.0, lw=1.4, head_scale=9)
    cad_text(ax, 16.0, 51.0,
             'STREAM 2: TREATED CLEAN GAS TO SCRUBBER STACK\n4"-TOG-102-CS/PVDF-N (90% Br2 REMOVED, y2 = 0.0020)', sz=4.8, bold=True)
    
    # Top Pressure Transmitter (PT-102)
    cad_circle(ax, 23.5, 50.0, 0.12, fill=True)
    cad_line(ax, 23.5, 50.0, 23.5, 47.5, lw=0.6, ls='--')
    cad_instrument_bubble(ax, 23.5, 47.5, 'PT', '102', loc='DCS')
    
    # Continuous Emission Gas Analyzer (AI-102 / AT-102, ppm Br2 monitor)
    cad_circle(ax, 19.5, 50.0, 0.12, fill=True)
    cad_line(ax, 19.5, 50.0, 19.5, 47.5, lw=0.6, ls='--')
    cad_instrument_bubble(ax, 19.5, 47.5, 'AT', '102', loc='FIELD')
    cad_line(ax, 19.5, 46.9, 19.5, 45.2, lw=0.6, ls='--')
    cad_instrument_bubble(ax, 19.5, 45.2, 'AI', '102', loc='DCS')
    cad_text(ax, 19.5, 44.2, 'AAH-102 (>2500 ppm)\nEMISSION COMPLIANCE', sz=4.2, bold=True)
    
    # Safety Relief Valve (PSV-101) & Rupture Disc (PSE-101)
    cad_line(ax, CX_COL, 48.0, CX_COL + 5.0, 48.0, lw=1.2)
    cad_line(ax, CX_COL + 5.0, 48.0, CX_COL + 5.0, 49.5, lw=1.2)
    # Rupture disc
    cad_arc(ax, CX_COL + 5.0, 48.8, 0.6, 0.3, theta1=0, theta2=180, lw=0.9)
    cad_instrument_bubble(ax, CX_COL + 7.0, 48.8, 'PSE', '101', loc='FIELD', r=0.45, sz=4.8)
    # Safety Valve
    cad_valve(ax, CX_COL + 5.0, 49.8, orientation='H', size=0.6, valve_type='SRV')
    cad_line(ax, CX_COL + 5.0, 50.4, CX_COL + 5.0, 51.5, lw=1.2)
    cad_arrow(ax, CX_COL + 5.0, 50.8, CX_COL + 5.0, 51.5, lw=1.0, head_scale=6)
    cad_instrument_bubble(ax, CX_COL + 7.0, 50.2, 'PSV', '101', loc='FIELD', r=0.45, sz=4.8)
    cad_text(ax, CX_COL + 5.2, 52.0, 'TO EMERGENCY CAUSTIC QUENCH HEADER (SET: 150 kPa g)', sz=4.4, ha='left', bold=True)
    
    # ─────────────────────────────────────────────────────────────────────────
    # 7. DEMISTER INTERMITTENT WASH SYSTEM (STREAM 6)
    # ─────────────────────────────────────────────────────────────────────────
    cad_line(ax, 40.0, y_wline + 4.5, CX_COL + W_COL/2 + 1.2, y_wline + 4.5, lw=1.1)
    cad_line(ax, CX_COL + W_COL/2 + 1.2, y_wline + 4.5, CX_COL + W_COL/2, y_pid_dem + 1.2, lw=1.1)
    # Solenoid valve XV-103
    cad_valve(ax, 34.0, y_wline + 4.5, orientation='H', size=0.6, valve_type='CONTROL')
    cad_text(ax, 34.0, y_wline + 3.6, 'XV-103\n(SOLENOID)', sz=4.2, bold=True)
    cad_line(ax, 34.0, y_wline + 4.9, 34.0, y_wline + 5.8, lw=0.5, ls='--')
    cad_instrument_bubble(ax, 34.0, y_wline + 5.8, 'TIRC', '103', loc='DCS', r=0.45, sz=4.5)
    cad_text(ax, 34.0, y_wline + 6.6, 'PROGRAMMABLE CYCLE TIMER\n(10 MIN FLUSH / 24 HRS)', sz=4.0, bold=True)
    
    # ═════════════════════════════════════════════════════════════════════════
    # RIGHT PANEL: STREAM BALANCE TABLES, LINE SPEC & CONTROL LOGIC
    # ═════════════════════════════════════════════════════════════════════════
    
    # TABLE 1: STREAM OPERATING MASS & HEAT BALANCE TABLE
    T1_X = 53.5
    T1_Y = 36.5
    t1_headers = ['STR', 'STREAM SERVICE', 'FLUID / PHASE', 'MASS FLOW', 'TEMP', 'PRESS', 'COMPOSITION']
    t1_widths  = [1.4, 6.8, 4.4, 4.4, 2.2, 3.2, 5.6]
    t1_rows = [
        ['1', 'Feed Gas Mixture',   'Gas / Vapor', '0.341 kg/s (1228 kg/h)', '25 °C', '803 mmHg', '2.00 mol% Br2, 98% Air'],
        ['2', 'Treated Overhead Gas','Gas / Vapor', '0.315 kg/s (1134 kg/h)', '25 °C', '794 mmHg', '0.20 mol% Br2 (90% Rem)'],
        ['3', 'Scrubbing Water Feed','Liquid / H2O','17.25 kg/s (62.1 t/h)',   '25 °C', '2.5 bar g','100.0 wt% Pure Water'],
        ['4', 'Rich Liquor Bottoms', 'Liquid Soln', '17.28 kg/s (62.2 t/h)',   '25 °C', '1.1 bar g','x1 = 2.79x10⁻⁴ (Br2)'],
        ['5', 'Safety Relief Vent',  'Emergency',   'Discontinuous / Upset',  '25 °C', '1.5 bar g','Raw Gas / Relief Quench'],
        ['6', 'Demister Wash Water', 'Liquid / H2O','2.50 kg/s (Batch Flush)', '25 °C', '3.0 bar g','Intermittent Washdown'],
    ]
    cad_draw_table(ax, T1_X, T1_Y, t1_headers, t1_rows, t1_widths, row_h=0.55,
                   title='TABLE 1 — STREAM OPERATING MASS & HEAT BALANCE TABLE', sz=4.8)
    
    # TABLE 2: PROCESS PIPING LINE DESIGNATION & SPECIFICATION TABLE
    T2_X = 53.5
    T2_Y = 24.5
    t2_headers = ['LINE NUMBER', 'SERVICE DESCRIPTION', 'SIZE', 'CLASS', 'PIPE MATERIAL', 'INSULATION']
    t2_widths  = [4.8, 8.4, 2.6, 2.6, 6.8, 2.8]
    t2_rows = [
        ['6"-BRG-101-CS/PVDF-N', 'Raw Bromine Gas Inlet',   '6" (DN150)', 'CL 150', 'SA-106 Gr B + 3 mm PVDF', 'None'],
        ['4"-TOG-102-CS/PVDF-N', 'Treated Gas Vent to Stack','4" (DN100)', 'CL 150', 'SA-106 Gr B + 3 mm PVDF', 'None'],
        ['3"-PWT-103-CS-N',      'Fresh Water Supply Header','3" (DN80)',  'CL 150', 'Carbon Steel SA-106 Gr B', 'None'],
        ['3"-RBL-104-CS/PVDF-N', 'Rich Bromine Water Bottoms','3" (DN80)', 'CL 150', 'SA-106 Gr B + 3 mm PVDF', 'None'],
        ['1.5"-DRN-105-CS/PVDF-N','Vessel Drain Line',       '1.5" (DN40)','CL 150', 'SA-106 Gr B + 3 mm PVDF', 'None'],
        ['1.5"-DMW-106-SS316L-N','Demister Flush Water',    '1.5" (DN40)','CL 150', 'SS316L Stainless Steel',   'None'],
    ]
    cad_draw_table(ax, T2_X, T2_Y, t2_headers, t2_rows, t2_widths, row_h=0.48,
                   title='TABLE 2 — PIPING LINE DESIGNATION & SPECIFICATION SCHEDULE', sz=4.8)
    
    # TABLE 3: ISA-5.1 INSTRUMENTATION & CONTROL VALVES SUMMARY
    T3_X = 53.5
    T3_Y = 13.5
    t3_headers = ['TAG', 'DESCRIPTION', 'TYPE / TECHNOLOGY', 'RANGE / SETPOINT', 'FAIL ACTION']
    t3_widths  = [2.2, 8.8, 7.5, 6.5, 3.0]
    t3_rows = [
        ['FFIC-102', 'Water-to-Gas Ratio Controller', 'DCS Ratio Algorithm', 'L/G = 90.5 mol/mol', 'Auto Tracking'],
        ['FCV-102',  'Water Supply Control Valve',    'Globe / Diaphragm Act.', '0 - 25 kg/s Water',   'Fail-Open (FO)'],
        ['LIC-101',  'Bottom Sump Level Controller',  'DCS PID Loop',        'Set: 50% Sump Height', 'Auto Control'],
        ['LCV-101',  'Rich Liquor Discharge Valve',   'Globe / PTFE Lined',  '0 - 25 kg/s Liquor',   'Fail-Closed (FC)'],
        ['PDT-101',  'Packed Bed Diff. Pressure',     'Diaphragm Seal (Hast)','0 - 5.0 kPa (0-500 mm)', 'Alarm High/Low'],
        ['XV-101',   'Feed Gas Isolation Valve',      'Pneumatic Ball Valve', 'Tight Shutoff (TSO)',  'Fail-Closed (FC)'],
        ['PSV-101',  'Emergency Safety Relief Valve', 'Conventional Flanged', 'Set: 150 kPa (g)',     'Relief to Quench'],
    ]
    cad_draw_table(ax, T3_X, T3_Y, t3_headers, t3_rows, t3_widths, row_h=0.48,
                   title='TABLE 3 — INSTRUMENTATION & AUTOMATIC CONTROL VALVES SCHEDULE', sz=4.8)
    
    # CONTROL PHILOSOPHY & SAFETY INTERLOCK LOGIC NOTES
    N5_X = 53.5
    N5_Y = 7.2
    cad_rect(ax, N5_X, N5_Y, 28.0, 5.8, lw=1.2, fill=True)
    cad_text(ax, N5_X + 14.0, N5_Y + 5.4, 'PROCESS CONTROL PHILOSOPHY & SAFETY INTERLOCK SYSTEM (SIS)', sz=6.5, bold=True)
    
    notes_dwg5 = [
        "1. GAS-LIQUID RATIO CONTROL STRATEGY (FFIC-102):",
        "   - FLOW OF SCRUBBING WATER (FCV-102) IS CONTINUOUSLY SLAVED TO INLET GAS MASS FLOW (FT-101).",
        "   - RATIO MAINTAINED AT L = 1.40 Lmin (L/G = 90.5 mol/mol). IF GAS FLOW INCREASES, WATER FLOW",
        "     RAMPS UP PROPORTIONATELY TO GUARANTEE 90% BROMINE CAPTURE EFFICIENCY AT ALL TIMES.",
        "2. BED DIFFERENTIAL PRESSURE FLOODING PROTECTION (PDT-101):",
        "   - NORMAL OPERATING BED PRESSURE DROP: 1.15 kPa (115 mm H2O).",
        "   - HIGH ALARM (PDAH-101 AT 2.5 kPa): WARNS OPERATOR OF INCIPIENT BED FLOODING.",
        "   - HIGH-HIGH INTERLOCK (PDAHH-101 AT 3.8 kPa): AUTOMATICALLY TRIPS FEED BLOWER B-101 AND",
        "     CLOSES XV-101 TO PREVENT BROMINE LIQUID CARRYOVER INTO OVERHEAD DUCTWORK.",
        "3. LEVEL & OVERFLOW INTERLOCKS (LT-101 / LIC-101):",
        "   - LOW-LOW LEVEL (LSLL-101): TRIPS BOTTOM PUMPS TO PREVENT CAVITATION & GAS BLOW-THROUGH.",
        "   - HIGH-HIGH LEVEL (LSHH-101): SOUNDS CRITICAL EVAPORATOR/ABSORBER ALARM IN MAIN DCS CONTROL ROOM.",
    ]
    for n_idx, n_line in enumerate(notes_dwg5):
        bold_flag = ("1." in n_line or "2." in n_line or "3." in n_line)
        cad_text(ax, N5_X + 0.35, N5_Y + 4.8 - n_idx * 0.52, n_line, sz=4.2, ha='left', bold=bold_flag)
    
    # ── Title Block ─────────────────────────────────────────────────────────
    draw_title_block(
        ax,
        dwg_title='PACKED-BED ABSORBER SYSTEM (C-101) — PIPING & INSTRUMENTATION DIAGRAM (P&ID) CAD',
        dwg_no='PEDD-PBA-05',
        rev='00',
        sheet_no='05 OF 05',
        scale='DIAGRAMMATIC / ISA-5.1 STANDARD',
        equip_desc='PACKED BED ABSORBER PROCESS PIPING & AUTOMATIC INSTRUMENTATION',
        duty_desc='FEED: 0.25 m³/s (2% Br2) | WATER: 17.25 kg/s | 90% RECOVERY | RATIO L/G = 90.5'
    )
    
    # ── Save Outputs ────────────────────────────────────────────────────────
    OUT_DIR = r'd:\GAMES\zercxes\CAD_Engineering_Drawings'
    pdf_path = os.path.join(OUT_DIR, '05_Packed_Bed_Absorber_PID_Instrumentation_CAD.pdf')
    png_path = os.path.join(OUT_DIR, '05_Packed_Bed_Absorber_PID_Instrumentation_CAD.png')
    
    fig.savefig(pdf_path, dpi=300, bbox_inches='tight', facecolor='white')
    fig.savefig(png_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"SUCCESS: DWG-05 generated at {pdf_path} and {png_path}")

if __name__ == '__main__':
    generate_dwg05()
