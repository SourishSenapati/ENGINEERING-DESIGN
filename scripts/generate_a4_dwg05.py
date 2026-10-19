"""
A4 OPTIMIZED: DWG-05 PIPING & INSTRUMENTATION DIAGRAM (P&ID) CAD
PACKED-BED ABSORBER (C-101) — 750 mm ID x 4500 mm BED
STUDENT: SOURISH SENAPATI | ROLL NO.: 002310301035 | DATE: 29/09/2026
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
    cad_balloon, cad_valve, cad_instrument_bubble, cad_hatch_rect,
    cad_draw_table_a4, W, H, BK, GREY
)

def generate_a4_dwg05(out_pdf, out_png):
    fig, ax = create_a4_canvas()
    draw_a4_border(ax)
    
    # ── Geometry & Layout Coordinates ─────────────────────────────────────────
    # Inner border: X in [0.8, 28.9], Y in [0.8, 20.2]
    # Title Block: Y in [0.8, 3.10]
    # P&ID Drawing Area: X in [1.0, 18.0], Y in [3.3, 20.0]
    # Right Panel (Tables/Notes): X in [18.2, 28.7], Y in [3.3, 20.0]
    
    CX_C = 10.2  # Column Centerline X
    CY_C = 11.6  # Column Centerline Y
    W_C  = 2.4   # Column OD representation
    H_C  = 8.0   # Shell Height (T/T)
    
    y_shell_t = CY_C + H_C/2   # 15.6 cm (Top Tangent)
    y_shell_b = CY_C - H_C/2   # 7.6 cm  (Bottom Tangent)
    y_head_t  = 16.2           # Top Dished Head Apex
    y_head_b  = 7.0            # Bottom Dished Head Apex
    y_skirt_b = 5.2            # Skirt Base Plate
    
    # Column Centerline
    cad_line(ax, CX_C, 4.2, CX_C, 19.2, lw=0.35, ls='-.')
    
    # Column Body & 2:1 Ellipsoidal Heads
    cad_rect(ax, CX_C - W_C/2, y_shell_b, W_C, H_C, lw=1.2, fill=True)
    cad_arc(ax, CX_C, y_shell_t, W_C, 1.2, theta1=0, theta2=180, lw=1.2)
    cad_arc(ax, CX_C, y_shell_b, W_C, 1.2, theta1=180, theta2=360, lw=1.2)
    
    # Support Skirt & Anchor Base
    cad_rect(ax, CX_C - W_C/2, y_skirt_b, W_C, y_shell_b - y_skirt_b, lw=0.9, fill=True)
    cad_rect(ax, CX_C - W_C/2 - 0.25, y_skirt_b - 0.15, W_C + 0.5, 0.15, lw=0.9, fill=True)
    cad_text(ax, CX_C, 6.2, 'SUPPORT SKIRT', sz=3.8, bold=True)
    
    # ── Column Internals ─────────────────────────────────────────────────────
    # Demister Pad
    y_dem = 15.0
    cad_rect(ax, CX_C - W_C/2 + 0.1, y_dem - 0.20, W_C - 0.2, 0.40, lw=0.8, fill=True)
    cad_hatch_rect(ax, CX_C - W_C/2 + 0.1, y_dem - 0.20, W_C - 0.2, 0.40, pitch=0.10, lw=0.3)
    cad_text(ax, CX_C, y_dem, 'DEMISTER PAD', sz=3.8, bold=True, bg='white')
    
    # Liquid Spray Distributor
    y_dist = 14.2
    cad_line(ax, CX_C - W_C/2 + 0.15, y_dist, CX_C + W_C/2 - 0.15, y_dist, lw=0.9)
    for sx in np.linspace(CX_C - W_C/2 + 0.35, CX_C + W_C/2 - 0.35, 4):
        cad_arrow(ax, sx, y_dist, sx, y_dist - 0.32, lw=0.5, head_scale=4)
    cad_text(ax, CX_C, y_dist + 0.25, 'SPRAY DISTRIBUTOR', sz=3.6, bold=True)
    
    # Packed Bed (Z = 4500 mm)
    y_bed_t = 13.5
    y_bed_b = 9.2
    h_bed = y_bed_t - y_bed_b
    cad_rect(ax, CX_C - W_C/2 + 0.1, y_bed_b, W_C - 0.2, h_bed, lw=0.8, fill=True)
    cad_hatch_rect(ax, CX_C - W_C/2 + 0.1, y_bed_b, W_C - 0.2, h_bed, pitch=0.22, angle=45, lw=0.25, color=GREY)
    cad_hatch_rect(ax, CX_C - W_C/2 + 0.1, y_bed_b, W_C - 0.2, h_bed, pitch=0.22, angle=-45, lw=0.25, color=GREY)
    cad_text(ax, CX_C, 11.35,
             'PACKED BED\nZ = 4500 mm\n25-mm CERAMIC\nRASCHIG RINGS',
             sz=3.8, bold=True, bg='white')
    
    # Packing Support Grid
    cad_line(ax, CX_C - W_C/2 + 0.05, y_bed_b, CX_C + W_C/2 - 0.05, y_bed_b, lw=1.2)
    cad_text(ax, CX_C, y_bed_b - 0.30, 'SUPPORT GRID', sz=3.6, bold=True)
    
    # Gas Inlet Deflector Chevron
    y_gas = 8.2
    p_def = [(CX_C - 0.55, y_gas - 0.18), (CX_C, y_gas + 0.22), (CX_C + 0.55, y_gas - 0.18)]
    ax.add_patch(Polygon(p_def, closed=False, ec=BK, lw=0.85, fill=False))
    
    # ── Equipment Tag Box (C-101) ────────────────────────────────────────────
    # Placed in clear space to the right of top head
    tag_box_x = 12.2
    tag_box_y = 17.2
    cad_rect(ax, tag_box_x, tag_box_y, 3.2, 1.0, lw=1.0, fill=True)
    cad_text(ax, tag_box_x + 1.6, tag_box_y + 0.68, 'C-101', sz=6.5, bold=True)
    cad_text(ax, tag_box_x + 1.6, tag_box_y + 0.30, 'PACKED ABSORBER', sz=4.0, bold=True)
    
    # ── Nozzle Identification Balloons ───────────────────────────────────────
    cad_balloon(ax, CX_C - W_C/2 - 0.40, y_gas, 'N1', radius=0.18, sz=3.8)
    cad_balloon(ax, CX_C + W_C/2 + 0.40, y_dist, 'N3', radius=0.18, sz=3.8)
    cad_balloon(ax, CX_C - 0.40, y_head_b - 0.3, 'N4', radius=0.18, sz=3.8)
    cad_balloon(ax, CX_C - 0.40, y_head_t + 0.3, 'N6', radius=0.18, sz=3.8)
    cad_balloon(ax, CX_C - W_C/2 - 0.40, y_bed_b + 0.2, 'N7', radius=0.18, sz=3.8)
    cad_balloon(ax, CX_C - W_C/2 - 0.40, y_bed_t - 0.2, 'N8', radius=0.18, sz=3.8)
    
    # ─────────────────────────────────────────────────────────────────────────
    # STREAM 1: RAW FEED GAS TRAIN (LEFT TO C-101)
    # ─────────────────────────────────────────────────────────────────────────
    y_gline = y_gas  # 8.2
    cad_line(ax, 1.0, y_gline, CX_C - W_C/2, y_gline, lw=1.2)
    cad_arrow(ax, 1.4, y_gline, 1.9, y_gline, lw=0.9, head_scale=5)
    
    # Stream 1 Label (Well above pipe and blower)
    cad_text(ax, 1.1, y_gline + 0.95, 'STR 1: RAW FEED GAS (6"-BRG-101)\n0.25 m3/s | 2.0 mol% Br2', sz=3.8, ha='left', bold=True)
    
    # Feed Gas Blower B-101 (VFD)
    cad_circle(ax, 3.2, y_gline, 0.50, lw=0.9, fill=True)
    cad_text(ax, 3.2, y_gline - 0.85, 'B-101 (VFD)', sz=3.7, bold=True)
    
    # Emergency Isolation Valve XV-101 (FC)
    cad_valve(ax, 4.6, y_gline, orientation='H', size=0.40, valve_type='CONTROL')
    cad_text(ax, 4.6, y_gline - 0.55, 'XV-101\n(FC)', sz=3.6, bold=True)
    
    # Flow Transmitter FT-101 & Ratio Controller FFIC-102
    cad_circle(ax, 5.8, y_gline, 0.07, fill=True)
    cad_line(ax, 5.8, y_gline, 5.8, y_gline + 1.2, lw=0.5, ls='--')
    cad_instrument_bubble(ax, 5.8, y_gline + 1.2, 'FT', '101', loc='FIELD', r=0.29, sz=3.7)
    cad_line(ax, 5.8, y_gline + 1.49, 5.8, y_gline + 2.3, lw=0.5, ls='--')
    cad_instrument_bubble(ax, 5.8, y_gline + 2.3, 'FFIC', '102', loc='DCS', r=0.29, sz=3.5)
    
    # Gas Analyzer AI-101 (Tapped downwards into clear space)
    cad_circle(ax, 7.2, y_gline, 0.07, fill=True)
    cad_line(ax, 7.2, y_gline, 7.2, y_gline - 1.1, lw=0.5, ls='--')
    cad_instrument_bubble(ax, 7.2, y_gline - 1.1, 'AI', '101', loc='DCS', r=0.29, sz=3.7)
    cad_text(ax, 7.2, y_gline - 1.65, '2.0% Br2', sz=3.5, bold=True)
    
    # ─────────────────────────────────────────────────────────────────────────
    # STREAM 3: FRESH SCRUBBING WATER & RATIO CONTROL LOOP
    # ─────────────────────────────────────────────────────────────────────────
    y_wline = y_dist  # 14.2
    cad_line(ax, 17.8, 16.5, 15.0, 16.5, lw=1.2)
    cad_line(ax, 15.0, 16.5, 15.0, y_wline, lw=1.2)
    cad_line(ax, 15.0, y_wline, CX_C + W_C/2, y_wline, lw=1.2)
    cad_arrow(ax, 17.2, 16.5, 16.4, 16.5, lw=0.9, head_scale=5)
    cad_arrow(ax, 14.2, y_wline, 13.5, y_wline, lw=0.9, head_scale=5)
    cad_text(ax, 15.5, 17.05, 'STR 3: FRESH WATER (3"-PWT-103) | 17.25 kg/s (62.1 t/h)', sz=3.8, bold=True)
    
    # Water Feed Pump P-101A/B
    cad_circle(ax, 15.0, 15.4, 0.48, lw=0.9, fill=True)
    cad_text(ax, 15.9, 15.4, 'P-101A/B\n(1W+1S)', sz=3.6, ha='left', bold=True)
    
    # Water Control Valve FCV-102 (FO)
    cad_valve(ax, 13.0, y_wline, orientation='H', size=0.40, valve_type='CONTROL')
    cad_text(ax, 13.4, y_wline - 0.50, 'FCV-102\n(FO)', sz=3.6, ha='left', bold=True)
    
    # Ratio signal line from FFIC-102 to FCV-102
    cad_line(ax, 5.8, y_gline + 2.59, 5.8, 12.4, lw=0.5, ls=':')
    cad_line(ax, 5.8, 12.4, 13.0, 12.4, lw=0.5, ls=':')
    cad_line(ax, 13.0, 12.4, 13.0, y_wline - 0.25, lw=0.5, ls=':')
    cad_text(ax, 10.2, 12.4, 'RATIO CONTROL LOOP: L/G = 90.5 mol/mol (L = 1.40 Lmin)', sz=3.7, bold=True, bg='white')
    
    # ─────────────────────────────────────────────────────────────────────────
    # DIFFERENTIAL PRESSURE MONITORING (PDT-101)
    # ─────────────────────────────────────────────────────────────────────────
    cad_line(ax, CX_C - W_C/2, y_bed_b + 0.2, 7.4, y_bed_b + 0.2, lw=0.5)
    cad_line(ax, CX_C - W_C/2, y_bed_t - 0.2, 7.4, y_bed_t - 0.2, lw=0.5)
    cad_line(ax, 7.4, y_bed_b + 0.2, 7.4, 11.0, lw=0.5)
    cad_line(ax, 7.4, y_bed_t - 0.2, 7.4, 11.7, lw=0.5)
    cad_instrument_bubble(ax, 7.4, 11.35, 'PDT', '101', loc='FIELD', r=0.29, sz=3.7)
    cad_text(ax, 7.4, 10.55, 'DP = 1.15 kPa\nPDAH: 2.5 kPa', sz=3.5, bold=True, bg='white')
    
    # ─────────────────────────────────────────────────────────────────────────
    # STREAM 4: RICH LIQUOR BOTTOMS & LEVEL CONTROL
    # ─────────────────────────────────────────────────────────────────────────
    y_bline = 4.3  # Generously 1.2 cm above title block top (3.10)
    
    cad_line(ax, CX_C, y_head_b, CX_C, y_bline, lw=1.2)
    cad_line(ax, CX_C, y_bline, 17.8, y_bline, lw=1.2)
    cad_arrow(ax, 16.8, y_bline, 17.5, y_bline, lw=0.9, head_scale=5)
    
    # Level Control Valve LCV-101 (FC)
    cad_valve(ax, 13.4, y_bline, orientation='H', size=0.40, valve_type='CONTROL')
    cad_text(ax, 13.4, y_bline - 0.55, 'LCV-101 (FC)', sz=3.6, bold=True)
    
    # Stream 4 text placed neatly to the right of the control valve
    cad_text(ax, 14.1, y_bline + 0.65, 'STR 4: RICH WATER (3"-RBL-104)\n(x1 = 2.79 x 10^-4 | 17.28 kg/s)', sz=3.4, ha='left', bold=True)
    # Small dashed continuation block for outside scope
    cad_rect(ax, 16.3, y_bline - 0.45, 1.6, 0.90, lw=0.6, ls='--', fill=True)
    cad_text(ax, 17.1, y_bline, 'DOWNSTREAM\nSTRIPPER\n(OUT OF SCOPE)', sz=2.8, bold=True)
    
    # Level Transmitter LT-101 & Controller LIC-101
    cad_line(ax, CX_C + W_C/2, y_shell_b + 0.4, 12.2, y_shell_b + 0.4, lw=0.5)
    cad_line(ax, CX_C + W_C/2, y_shell_b - 0.4, 12.2, y_shell_b - 0.4, lw=0.5)
    cad_line(ax, 12.2, y_shell_b - 0.4, 12.2, y_shell_b + 0.4, lw=0.5)
    cad_instrument_bubble(ax, 12.2, 7.6, 'LIC', '101', loc='DCS', r=0.29, sz=3.5)
    # Signal line to LCV-101 (drops down cleanly with no line collision)
    cad_line(ax, 12.2, 7.31, 12.2, y_bline + 0.8, lw=0.5, ls=':')
    cad_line(ax, 12.2, y_bline + 0.8, 13.4, y_bline + 0.8, lw=0.5, ls=':')
    cad_line(ax, 13.4, y_bline + 0.8, 13.4, y_bline + 0.35, lw=0.5, ls=':')
    
    # ─────────────────────────────────────────────────────────────────────────
    # STREAM 2: TREATED OVERHEAD GAS & RELIEF SYSTEM
    # ─────────────────────────────────────────────────────────────────────────
    y_tline = 18.6  # Generously 1.6 cm below top inner border (20.2)
    
    cad_line(ax, CX_C, y_head_t, CX_C, y_tline, lw=1.2)
    cad_line(ax, CX_C, y_tline, 1.0, y_tline, lw=1.2)
    cad_arrow(ax, 4.6, y_tline, 3.8, y_tline, lw=0.9, head_scale=5)
    cad_text(ax, 4.8, y_tline + 0.45, 'STR 2: TREATED GAS TO STACK (4"-TOG-102) | 90% Br2 REMOVED (y2 = 0.002)', sz=3.8, bold=True)
    
    # Vent Analyzer AI-102
    cad_circle(ax, 6.0, y_tline, 0.07, fill=True)
    cad_line(ax, 6.0, y_tline, 6.0, y_tline - 1.1, lw=0.5, ls='--')
    cad_instrument_bubble(ax, 6.0, y_tline - 1.1, 'AI', '102', loc='DCS', r=0.29, sz=3.7)
    cad_text(ax, 6.0, y_tline - 1.65, '0.2% Br2', sz=3.5, bold=True)
    
    # Safety Relief Valve PSV-101
    cad_line(ax, 8.5, y_tline, 8.5, 19.2, lw=0.7)
    cad_valve(ax, 8.5, 19.2, orientation='H', size=0.35, valve_type='SRV')
    cad_text(ax, 8.5, 19.70, 'PSV-101 (150 kPa g)', sz=3.5, bold=True)
    
    # ═════════════════════════════════════════════════════════════════════════
    # RIGHT SIDE: STREAM TABLE, LINE SCHEDULE & CONTROL PHILOSOPHY
    # ═════════════════════════════════════════════════════════════════════════
    
    # TABLE 1: STREAM MASS & HEAT BALANCE TABLE
    T1_X = 18.2
    T1_Y = 16.5
    t1_headers = ['STR', 'SERVICE', 'MASS FLOW', 'TEMP', 'PRESS', 'COMPOSITION']
    t1_widths  = [0.9, 2.7, 2.1, 1.1, 1.4, 2.3]
    t1_rows = [
        ['1', 'Raw Feed Gas',  '0.341 kg/s', '25 DEG C', '803 mmHg', '2.0 mol% Br2'],
        ['2', 'Treated Vent',  '0.315 kg/s', '25 DEG C', '794 mmHg', '0.2 mol% Br2'],
        ['3', 'Scrub Water In','17.25 kg/s', '25 DEG C', '2.5 bar g','100 wt% Water'],
        ['4', 'Rich Liquor Out','17.28 kg/s','25 DEG C', '1.1 bar g','x1 = 2.79 x 10^-4'],
    ]
    cad_draw_table_a4(ax, T1_X, T1_Y, t1_headers, t1_rows, t1_widths, row_h=0.40,
                      title='TABLE 1 — STREAM OPERATING BALANCE', sz=4.0)
    
    # TABLE 2: PIPING LINE SCHEDULE
    T2_X = 18.2
    T2_Y = 11.2
    t2_headers = ['LINE TAG', 'SERVICE', 'SIZE', 'MATERIAL']
    t2_widths  = [3.1, 3.2, 1.6, 2.6]
    t2_rows = [
        ['6"-BRG-101-CS/PVDF', 'Raw Bromine Gas Inlet',   'DN 150', 'SA-106 + PVDF'],
        ['4"-TOG-102-CS/PVDF', 'Treated Overhead Gas',     'DN 100', 'SA-106 + PVDF'],
        ['3"-PWT-103-CS',      'Fresh Scrubbing Water',    'DN 80',  'Carbon Steel'],
        ['3"-RBL-104-CS/PVDF', 'Rich Bromine Water Bottoms','DN 80', 'SA-106 + PVDF'],
        ['1.5"-DMW-106-SS',    'Demister Wash Flush Line', 'DN 40',  'SS316L'],
    ]
    cad_draw_table_a4(ax, T2_X, T2_Y, t2_headers, t2_rows, t2_widths, row_h=0.38,
                      title='TABLE 2 — PROCESS PIPING LINE SCHEDULE', sz=4.0)
    
    # CONTROL PHILOSOPHY & SIS NOTES
    N_X = 18.2
    N_Y = 3.4
    H_N = 6.4
    W_N = 10.5
    cad_rect(ax, N_X, N_Y, W_N, H_N, lw=0.9, fill=True)
    cad_rect(ax, N_X, N_Y + H_N - 0.55, W_N, 0.55, lw=0.7, fill=True)
    cad_text(ax, N_X + W_N/2, N_Y + H_N - 0.28, 'PROCESS CONTROL PHILOSOPHY & SIS INTERLOCK LOGIC', sz=4.6, bold=True)
    
    notes_dwg5 = [
        "1. RATIO CONTROL LOOP (FFIC-102):",
        "   WATER FLOW (FCV-102) AUTOMATICALLY SLAVED TO RAW GAS INLET (FT-101).",
        "   MAINTAINS CONSTANT L/G = 90.5 mol/mol (L = 1.40 Lmin) TO GUARANTEE 90% Br2 RECOVERY.",
        "2. BED DIFFERENTIAL PRESSURE SAFETY PROTECTION (PDT-101):",
        "   NORMAL OPERATING DP = 1.15 kPa across 4.5 m BED; HIGH ALARM PDAH AT 2.5 kPa (70% FLOOD).",
        "   HIGH-HIGH INTERLOCK TRIP AT 3.8 kPa CLOSES XV-101 & TRIPS BLOWER B-101.",
        "3. BOTTOMS SUMP LEVEL CONTROL (LIC-101):",
        "   MODULATES LCV-101 TO MAINTAIN 50% SUMP LIQUID LEVEL (30 s LIQUID RESIDENCE TIME).",
        "4. ENVIRONMENTAL & EMISSION MONITORING (AI-102):",
        "   CONTINUOUS Br2 STACK ANALYZER (AI-102) MONITORS OUTLET CONCENTRATION;",
        "   ALARMS IF OUTLET Br2 EXCEEDS PROJECT-SPECIFIED DISCHARGE LIMIT.",
        "5. OVERPRESSURE SAFETY RELIEF (PSV-101):",
        "   SET AT 150 kPa g DISCHARGING TO CAUSTIC EMERGENCY SCRUBBING HEADER SYSTEM.",
    ]
    for idx, nl in enumerate(notes_dwg5):
        is_hdr = any(nl.startswith(k) for k in ["1.", "2.", "3.", "4.", "5."])
        sz_note = 3.7 if is_hdr else 3.4
        cad_text(ax, N_X + 0.30, N_Y + H_N - 0.85 - idx * 0.47, nl, sz=sz_note, ha='left', bold=is_hdr)
    
    # Title Block
    draw_a4_title_block(
        ax,
        dwg_title='PACKED-BED ABSORBER (C-101) — PIPING & INSTRUMENTATION (P&ID) CAD',
        dwg_no='PEDD-PBA-05',
        scale='ISA-5.1 STANDARD'
    )
    
    fig.savefig(out_pdf, dpi=300, facecolor='white')
    fig.savefig(out_png, dpi=300, facecolor='white')
    plt.close(fig)
    print(f"SUCCESS: Clean A4 DWG-05 generated at {out_pdf}")

if __name__ == '__main__':
    out_dir = r'd:\GAMES\zercxes\CAD_Engineering_Drawings\Packed_Bed_Absorber_Drawings'
    os.makedirs(out_dir, exist_ok=True)
    p_pdf = os.path.join(out_dir, '05_Packed_Bed_Absorber_PID_Instrumentation_CAD.pdf')
    p_png = os.path.join(out_dir, '05_Packed_Bed_Absorber_PID_Instrumentation_CAD.png')
    generate_a4_dwg05(p_pdf, p_png)
