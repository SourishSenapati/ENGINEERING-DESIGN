"""
A4 OPTIMIZED: DWG-01 ACETALDEHYDE-PROPYLENE OXIDE DISTILLATION PROCESS FLOW DIAGRAM (PFD)
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
    cad_balloon, cad_valve, cad_hatch_rect, cad_flange, cad_draw_table_a4,
    W, H, BK, GREY
)

def generate_acetaldehyde_dwg01(out_pdf, out_png):
    fig, ax = create_a4_canvas()
    draw_a4_border(ax)
    
    SUB_INFO = 'ACETALDEHYDE DISTILLATION (C-301)  |  12000 kg/h FEED (50 wt% AcH)  |  ID 2.00 m, R=3.89  |  ASME SEC VIII / TEMA'
    draw_a4_title_block(ax, 'PROCESS FLOW DIAGRAM (PFD) & HEAT-MASS BALANCES',
                        'JU/ChE/ED/DWG-01', scale='DIAGRAMMATIC', date='17 / 11 / 2026', sub_info=SUB_INFO)
    
    # Drawing Header
    cad_text(ax, W/2, H - 1.20, 'PROCESS FLOW DIAGRAM (PFD) — ACETALDEHYDE–PROPYLENE OXIDE DISTILLATION TRAIN', sz=6.6, bold=True)
    cad_text(ax, W/2, H - 1.55, 'BASIS: 12000 kg/h FEED (50 wt% AcH, 60% VAPOUR) | DISTILLATE: 97 wt% AcH | BOTTOMS: 3 wt% AcH | REFLUX: R=3.8855', sz=4.6, bold=False)
    
    # ═════════════════════════════════════════════════════════════════════════
    # EQUIPMENT DRAWINGS (UPPER PROCESS REGION Y = 7.5 TO 18.5)
    # ═════════════════════════════════════════════════════════════════════════
    
    # ─────────────────────────────────────────────────────────────────────────
    # 1. FEED STORAGE TANK T-301 (X=2.2, Y=13.8)
    # ─────────────────────────────────────────────────────────────────────────
    TX, TY = 2.2, 13.8
    # Concrete foundation pad
    cad_rect(ax, TX - 0.15, TY - 0.20, 1.70, 0.20, lw=0.75, fill=True)
    cad_hatch_rect(ax, TX - 0.15, TY - 0.20, 1.70, 0.20, pitch=0.10, angle=-45, lw=0.25)
    # Cylindrical Shell & Flat Bottom
    cad_rect(ax, TX, TY, 1.40, 2.00, lw=0.90, fill=True)
    # Conical Roof
    p_roof = [(TX - 0.05, TY + 2.00), (TX + 0.70, TY + 2.40), (TX + 1.45, TY + 2.00)]
    ax.add_patch(Polygon(p_roof, closed=True, fc='#ffffff', ec=BK, lw=0.90, zorder=3))
    # Roof Gooseneck Vent
    cad_line(ax, TX + 0.70, TY + 2.40, TX + 0.70, TY + 2.65, lw=0.6)
    cad_arc(ax, TX + 0.80, TY + 2.65, 0.20, 0.20, theta1=0, theta2=180, lw=0.6)
    cad_line(ax, TX + 0.90, TY + 2.65, TX + 0.90, TY + 2.50, lw=0.6)
    # Liquid Level Line (75% Full)
    cad_line(ax, TX + 0.08, TY + 1.50, TX + 1.32, TY + 1.50, lw=0.55, ls='--', color='#0066cc')
    # Level Bridle on Tank Side
    cad_line(ax, TX - 0.10, TY + 0.35, TX - 0.10, TY + 1.75, lw=0.5)
    cad_line(ax, TX, TY + 0.35, TX - 0.10, TY + 0.35, lw=0.5)
    cad_line(ax, TX, TY + 1.75, TX - 0.10, TY + 1.75, lw=0.5)
    cad_text(ax, TX + 0.70, TY + 1.00, 'T-301\nFEED TANK\n60 m3 (CS)', sz=4.0, bold=True)
    
    # ─────────────────────────────────────────────────────────────────────────
    # 2. FEED PUMPS P-301A/B (DUTY / STANDBY) (X=2.9, Y=10.4)
    # ─────────────────────────────────────────────────────────────────────────
    PX, PY = 2.9, 10.4
    # Concrete plinth
    cad_rect(ax, PX - 0.60, PY - 0.55, 1.20, 0.15, lw=0.65, fill=True)
    # Motor Housing & Coupling
    cad_rect(ax, PX - 0.55, PY - 0.20, 0.32, 0.40, lw=0.75, fill=True)
    cad_line(ax, PX - 0.23, PY, PX - 0.12, PY, lw=0.9)
    # Volute Casing & Impeller
    cad_circle(ax, PX + 0.12, PY, 0.32, lw=0.85, fill=True)
    # Tangential discharge nozzle
    cad_line(ax, PX + 0.12 + 0.32, PY, PX + 0.12 + 0.32, PY + 0.42, lw=0.75)
    cad_flange(ax, PX + 0.44, PY + 0.42, orientation='V', length=0.22)
    cad_text(ax, PX, PY - 0.82, 'P-301A/B\nFEED PUMPS (12 t/h)', sz=3.8, bold=True)
    
    # Line T-301 bottom draw to Pump suction
    cad_line(ax, TX + 0.70, TY, TX + 0.70, PY, lw=0.8)
    cad_line(ax, TX + 0.70, PY, PX - 0.12, PY, lw=0.8)
    cad_valve(ax, TX + 0.70, PY + 1.20, orientation='V', size=0.25)
    cad_text(ax, TX + 1.05, PY + 1.20, 'V-101', sz=2.8, bold=False)
    # Y-Strainer symbol on suction line
    cad_line(ax, PX - 0.02, PY - 0.12, PX - 0.02, PY + 0.12, lw=0.6)
    
    # ─────────────────────────────────────────────────────────────────────────
    # 3. FEED PREHEATER / PARTIAL VAPORIZER E-301 (X=5.8, Y=12.8)
    # ─────────────────────────────────────────────────────────────────────────
    EX, EY = 5.8, 12.8
    # Shell Dimensions: 1.4 cm long x 0.65 cm diameter
    ESW, ESH = 1.40, 0.65
    cad_rect(ax, EX - ESW/2, EY - ESH/2, ESW, ESH, lw=0.85, fill=True)
    # Tubesheet Flanges
    cad_rect(ax, EX - ESW/2 - 0.08, EY - ESH/2 - 0.08, 0.08, ESH + 0.16, lw=0.65, fill=True)
    cad_rect(ax, EX + ESW/2, EY - ESH/2 - 0.08, 0.08, ESH + 0.16, lw=0.65, fill=True)
    # Channel Heads (Bonnet Type)
    cad_arc(ax, EX - ESW/2 - 0.08, EY, 0.25, ESH, theta1=90, theta2=270, lw=0.85)
    cad_arc(ax, EX + ESW/2 + 0.08, EY, 0.25, ESH, theta1=270, theta2=450, lw=0.85)
    # Tube Bundle (Dashed lines)
    cad_line(ax, EX - ESW/2, EY - 0.14, EX + ESW/2, EY - 0.14, lw=0.35, ls='--')
    cad_line(ax, EX - ESW/2, EY + 0.14, EX + ESW/2, EY + 0.14, lw=0.35, ls='--')
    # Saddle supports
    cad_line(ax, EX - 0.40, EY - ESH/2, EX - 0.40, EY - ESH/2 - 0.20, lw=0.7)
    cad_line(ax, EX + 0.40, EY - ESH/2, EX + 0.40, EY - ESH/2 - 0.20, lw=0.7)
    cad_text(ax, EX, EY + 0.85, 'E-301\nFEED PREHEATER\n(60% VAPOUR, q=0.40)', sz=3.8, bold=True)
    
    # LP Steam Inlet to Preheater shell top
    cad_line(ax, EX - 0.25, EY + ESH/2 + 0.60, EX - 0.25, EY + ESH/2, lw=0.7)
    cad_arrow(ax, EX - 0.25, EY + ESH/2 + 0.45, EX - 0.25, EY + ESH/2 + 0.10, head_scale=4)
    cad_text(ax, EX - 0.25, EY + ESH/2 + 0.80, 'LP STEAM', sz=3.0, bold=True)
    # Condensate out from Preheater shell bottom
    cad_line(ax, EX + 0.25, EY - ESH/2, EX + 0.25, EY - ESH/2 - 0.45, lw=0.7)
    cad_arrow(ax, EX + 0.25, EY - ESH/2 - 0.20, EX + 0.25, EY - ESH/2 - 0.45, head_scale=4)
    cad_text(ax, EX + 0.25, EY - ESH/2 - 0.65, 'CONDENSATE', sz=3.0, bold=True)
    
    # Line Pump discharge to E-301 inlet (left channel)
    cad_line(ax, PX + 0.44, PY + 0.42, PX + 0.44, EY, lw=0.8)
    cad_line(ax, PX + 0.44, EY, EX - ESW/2 - 0.20, EY, lw=0.8)
    cad_arrow(ax, EX - ESW/2 - 0.45, EY, EX - ESW/2 - 0.22, EY, head_scale=6)
    
    # ─────────────────────────────────────────────────────────────────────────
    # 4. DISTILLATION COLUMN C-301 (X=11.0, Y=7.5 to 17.5)
    # ─────────────────────────────────────────────────────────────────────────
    CX = 11.0
    CY_BOT = 9.2
    CY_TOP = 16.5
    CW = 1.30  # Column Width (ID 2000 mm scaled)
    
    # Column Shell & Heads
    cad_line(ax, CX - CW/2, CY_BOT, CX - CW/2, CY_TOP, lw=1.1)
    cad_line(ax, CX + CW/2, CY_BOT, CX + CW/2, CY_TOP, lw=1.1)
    cad_arc(ax, CX, CY_TOP, CW, 0.60, theta1=0, theta2=180, lw=1.1)
    cad_arc(ax, CX, CY_BOT, CW, 0.60, theta1=180, theta2=360, lw=1.1)
    
    # Skirt & Foundation Base
    cad_rect(ax, CX - CW/2, 7.6, CW, CY_BOT - 7.6, lw=0.85)
    cad_line(ax, CX - CW/2 - 0.35, 7.6, CX + CW/2 + 0.35, 7.6, lw=1.2)
    cad_circle(ax, CX, 8.4, 0.22, lw=0.6)
    cad_text(ax, CX, 8.4, 'ACCESS', sz=3.0, bold=True)
    
    # Internal Trays (Schematic Representation of 24 Sieve Trays)
    cad_text(ax, CX, CY_TOP - 0.40, 'TRAY 1 (TOP)', sz=3.4, bold=True)
    for i in range(11):
        yt = CY_TOP - 0.75 - i * 0.55
        is_feed = (i == 5)
        lw_t = 0.85 if is_feed else 0.45
        ls_t = '-'
        col_t = '#006600' if is_feed else BK
        cad_line(ax, CX - CW/2 + 0.12, yt, CX + CW/2 - 0.12, yt, lw=lw_t, ls=ls_t, color=col_t)
        if is_feed:
            cad_text(ax, CX + 0.15, yt + 0.15, 'FEED TRAY (13)', sz=3.6, bold=True, color='#006600')
    cad_text(ax, CX, CY_BOT + 0.50, 'TRAY 24 (BOT)', sz=3.4, bold=True)
    
    # Demister Pad at top disengagement
    cad_rect(ax, CX - CW/2 + 0.08, CY_TOP - 0.20, CW - 0.16, 0.22, lw=0.55, fill=True)
    cad_hatch_rect(ax, CX - CW/2 + 0.08, CY_TOP - 0.20, CW - 0.16, 0.22, pitch=0.08, lw=0.25)
    
    cad_text(ax, CX, CY_TOP + 1.15, 'C-301\nDISTILLATION COLUMN\nID 2000 mm | 24 SIEVE TRAYS', sz=5.0, bold=True)
    
    # Line E-301 outlet to Column Feed Tray (Stage 13)
    Y_FEED = CY_TOP - 0.75 - 5 * 0.55  # ~13.0
    cad_line(ax, EX + ESW/2 + 0.20, EY, CX - CW/2, Y_FEED, lw=0.8)
    cad_arrow(ax, CX - CW/2 - 0.35, Y_FEED, CX - CW/2, Y_FEED, head_scale=6)
    
    # ─────────────────────────────────────────────────────────────────────────
    # 5. OVERHEAD CONDENSER E-303 (X=16.0, Y=16.8)
    # ─────────────────────────────────────────────────────────────────────────
    CDX, CDY = 16.0, 16.8
    # Shell: 2.2 cm long x 0.90 cm diameter
    CDSW, CDSH = 2.20, 0.90
    cad_rect(ax, CDX - CDSW/2, CDY - CDSH/2, CDSW, CDSH, lw=0.85, fill=True)
    # Tubesheets
    cad_rect(ax, CDX - CDSW/2 - 0.09, CDY - CDSH/2 - 0.08, 0.09, CDSH + 0.16, lw=0.65, fill=True)
    cad_rect(ax, CDX + CDSW/2, CDY - CDSH/2 - 0.08, 0.09, CDSH + 0.16, lw=0.65, fill=True)
    # Channel Heads (Right: Channel A with Pass Partition; Left: Bonnet L)
    cad_arc(ax, CDX - CDSW/2 - 0.09, CDY, 0.35, CDSH, theta1=90, theta2=270, lw=0.85)
    cad_rect(ax, CDX + CDSW/2 + 0.09, CDY - CDSH/2, 0.35, CDSH, lw=0.85, fill=True)
    cad_line(ax, CDX + CDSW/2 + 0.09, CDY, CDX + CDSW/2 + 0.44, CDY, lw=0.7) # Pass partition
    # Internal Tube Bundle Lines
    cad_line(ax, CDX - CDSW/2, CDY - 0.22, CDX + CDSW/2, CDY - 0.22, lw=0.35, ls='--')
    cad_line(ax, CDX - CDSW/2, CDY + 0.22, CDX + CDSW/2, CDY + 0.22, lw=0.35, ls='--')
    # Saddles
    cad_line(ax, CDX - 0.65, CDY - CDSH/2, CDX - 0.65, CDY - CDSH/2 - 0.22, lw=0.7)
    cad_line(ax, CDX + 0.65, CDY - CDSH/2, CDX + 0.65, CDY - CDSH/2 - 0.22, lw=0.7)
    cad_text(ax, CDX, CDY + 0.85, 'E-303 TOTAL CONDENSER\n4733.9 kW (CHILLED WTR)', sz=4.2, bold=True)
    
    # Chilled Water In & Out Nozzles
    cad_line(ax, CDX + CDSW/2 + 0.25, CDY - CDSH/2 - 0.65, CDX + CDSW/2 + 0.25, CDY - CDSH/2, lw=0.7)
    cad_arrow(ax, CDX + CDSW/2 + 0.25, CDY - CDSH/2 - 0.45, CDX + CDSW/2 + 0.25, CDY - CDSH/2 - 0.05, head_scale=5)
    cad_text(ax, CDX + CDSW/2 + 0.25, CDY - CDSH/2 - 0.85, 'CHW IN (7 C)', sz=3.2, bold=True)
    
    cad_line(ax, CDX + CDSW/2 + 0.25, CDY + CDSH/2, CDX + CDSW/2 + 0.25, CDY + CDSH/2 + 0.65, lw=0.7)
    cad_arrow(ax, CDX + CDSW/2 + 0.25, CDY + CDSH/2 + 0.20, CDX + CDSW/2 + 0.25, CDY + CDSH/2 + 0.60, head_scale=5)
    cad_text(ax, CDX + CDSW/2 + 0.25, CDY + CDSH/2 + 0.85, 'CHW OUT (12 C)', sz=3.2, bold=True)
    
    # Overhead Vapor Line from C-301 Top to E-303
    cad_line(ax, CX, CY_TOP + 0.30, CX, CDY, lw=0.85)
    cad_line(ax, CX, CDY, CDX - CDSW/2 - 0.35, CDY, lw=0.85)
    cad_arrow(ax, CDX - CDSW/2 - 0.60, CDY, CDX - CDSW/2 - 0.38, CDY, head_scale=6)
    
    # ─────────────────────────────────────────────────────────────────────────
    # 6. REFLUX DRUM V-301 (X=16.0, Y=13.4)
    # ─────────────────────────────────────────────────────────────────────────
    RX, RY = 16.0, 13.4
    # Horizontal drum: 1.7 cm long x 0.8 cm diameter
    cad_rect(ax, RX - 0.85, RY - 0.40, 1.70, 0.80, lw=0.85, fill=True)
    cad_arc(ax, RX - 0.85, RY, 0.40, 0.80, theta1=90, theta2=270, lw=0.85)
    cad_arc(ax, RX + 0.85, RY, 0.40, 0.80, theta1=270, theta2=90, lw=0.85)
    # Saddle supports
    cad_line(ax, RX - 0.55, RY - 0.40, RX - 0.55, RY - 0.62, lw=0.7)
    cad_line(ax, RX + 0.55, RY - 0.40, RX + 0.55, RY - 0.62, lw=0.7)
    # Boot / Sump Well
    cad_rect(ax, RX - 0.15, RY - 0.65, 0.30, 0.25, lw=0.75, fill=True)
    # Liquid level line
    cad_line(ax, RX - 0.75, RY, RX + 0.75, RY, lw=0.50, ls='--', color='#0066cc')
    cad_text(ax, RX, RY + 0.05, 'V-301\nREFLUX DRUM\n6.0 m3 (SS316L)', sz=3.8, bold=True)
    
    # Condensate line from E-303 bottom to V-301 top
    cad_line(ax, CDX - 0.40, CDY - CDSH/2, CDX - 0.40, RY + 0.65, lw=0.8)
    cad_line(ax, CDX - 0.40, RY + 0.65, RX, RY + 0.65, lw=0.8)
    cad_line(ax, RX, RY + 0.65, RX, RY + 0.40, lw=0.8)
    cad_arrow(ax, RX, RY + 0.55, RX, RY + 0.42, head_scale=6)
    
    # Off-Gas Vent from V-301 top
    cad_line(ax, RX + 0.60, RY + 0.40, RX + 0.60, RY + 1.10, lw=0.6)
    cad_arrow(ax, RX + 0.60, RY + 0.85, RX + 0.60, RY + 1.15, head_scale=5)
    cad_text(ax, RX + 0.60, RY + 1.35, 'TO OFF-GAS/VENT', sz=3.4, bold=True)
    
    # ─────────────────────────────────────────────────────────────────────────
    # 7. REFLUX & DISTILLATE PUMPS P-302A/B (X=16.0, Y=10.4)
    # ─────────────────────────────────────────────────────────────────────────
    RPX, RPY = 16.0, 10.4
    # Concrete plinth
    cad_rect(ax, RPX - 0.60, RPY - 0.55, 1.20, 0.15, lw=0.65, fill=True)
    # Motor Housing & Volute
    cad_rect(ax, RPX - 0.55, RPY - 0.20, 0.32, 0.40, lw=0.75, fill=True)
    cad_line(ax, RPX - 0.23, RPY, RPX - 0.12, RPY, lw=0.9)
    cad_circle(ax, RPX + 0.12, RPY, 0.32, lw=0.85, fill=True)
    cad_line(ax, RPX + 0.44, RPY, RPX + 0.44, RPY + 0.42, lw=0.75)
    cad_flange(ax, RPX + 0.44, RPY + 0.42, orientation='V', length=0.22)
    cad_text(ax, RPX, RPY - 0.82, 'P-302A/B\nREFLUX PUMPS', sz=3.8, bold=True)
    
    # Suction line from V-301 boot to pump suction
    cad_line(ax, RX, RY - 0.65, RX, RPY, lw=0.8)
    cad_line(ax, RX, RPY, RPX - 0.12, RPY, lw=0.8)
    
    # Pump discharge splits: Reflux return to C-301 and Distillate Product
    cad_line(ax, RPX + 0.44, RPY + 0.42, RPX + 1.60, RPY + 0.42, lw=0.8)
    cad_line(ax, RPX + 1.60, RPY + 0.42, RPX + 1.60, RPY + 1.60, lw=0.8)
    
    # Reflux Line (returning left to top tray of C-301)
    cad_line(ax, RPX + 1.60, RPY + 1.60, CX + CW/2 + 0.80, RPY + 1.60, lw=0.8)
    cad_line(ax, CX + CW/2 + 0.80, RPY + 1.60, CX + CW/2 + 0.80, CY_TOP - 0.60, lw=0.8)
    cad_line(ax, CX + CW/2 + 0.80, CY_TOP - 0.60, CX + CW/2, CY_TOP - 0.60, lw=0.8)
    cad_arrow(ax, CX + CW/2 + 0.30, CY_TOP - 0.60, CX + CW/2, CY_TOP - 0.60, head_scale=6)
    cad_valve(ax, CX + CW/2 + 0.80, RPY + 1.60, orientation='H', size=0.25)
    cad_text(ax, CX + CW/2 + 0.80, RPY + 1.95, 'FCV-304', sz=2.8, bold=False)
    
    # Distillate Product Line (going right to battery limits)
    cad_line(ax, RPX + 1.60, RPY + 0.42, RPX + 3.80, RPY + 0.42, lw=0.8)
    cad_arrow(ax, RPX + 3.50, RPY + 0.42, RPX + 3.90, RPY + 0.42, head_scale=6)
    cad_valve(ax, RPX + 2.50, RPY + 0.42, orientation='H', size=0.25)
    cad_text(ax, RPX + 4.10, RPY + 0.55, 'DISTILLATE PRODUCT D\n(97 wt% / 97.71 mol% AcH)', sz=4.0, bold=True, ha='left')
    
    # ─────────────────────────────────────────────────────────────────────────
    # 8. THERMOSIPHON REBOILER E-302 (X=7.5, Y=8.8)
    # ─────────────────────────────────────────────────────────────────────────
    RBX, RBY = 7.5, 8.8
    # Vertical shell: 0.90 cm wide x 2.2 cm tall
    RBSW, RBSH = 0.90, 2.20
    cad_rect(ax, RBX - RBSW/2, RBY - RBSH/2, RBSW, RBSH, lw=0.85, fill=True)
    # Tubesheet Flanges
    cad_rect(ax, RBX - RBSW/2 - 0.08, RBY + RBSH/2, RBSW + 0.16, 0.08, lw=0.65, fill=True)
    cad_rect(ax, RBX - RBSW/2 - 0.08, RBY - RBSH/2 - 0.08, RBSW + 0.16, 0.08, lw=0.65, fill=True)
    # Channel Heads (Bonnet B)
    cad_arc(ax, RBX, RBY + RBSH/2 + 0.08, RBSW, 0.40, theta1=0, theta2=180, lw=0.85)
    cad_arc(ax, RBX, RBY - RBSH/2 - 0.08, RBSW, 0.40, theta1=180, theta2=360, lw=0.85)
    # Tube bundle vertical lines
    cad_line(ax, RBX - 0.22, RBY - RBSH/2, RBX - 0.22, RBY + RBSH/2, lw=0.35, ls='--')
    cad_line(ax, RBX + 0.22, RBY - RBSH/2, RBX + 0.22, RBY + RBSH/2, lw=0.35, ls='--')
    cad_text(ax, RBX, RBY, 'E-302\nREBOILER\n3912.5 kW', sz=3.6, bold=True)
    
    # Steam in (from left at Y = RBY + 0.6)
    cad_line(ax, RBX - 1.60, RBY + 0.60, RBX - RBSW/2, RBY + 0.60, lw=0.8)
    cad_arrow(ax, RBX - 0.70, RBY + 0.60, RBX - RBSW/2, RBY + 0.60, head_scale=5)
    cad_valve(ax, RBX - 1.10, RBY + 0.60, orientation='H', size=0.25)
    cad_text(ax, RBX - 1.70, RBY + 0.60, 'STEAM 1.5 bar', sz=3.4, bold=True, ha='right')
    
    # Condensate out (to left at Y = RBY - 0.6)
    cad_line(ax, RBX - RBSW/2, RBY - 0.60, RBX - 1.60, RBY - 0.60, lw=0.8)
    cad_arrow(ax, RBX - 1.30, RBY - 0.60, RBX - 1.60, RBY - 0.60, head_scale=5)
    cad_text(ax, RBX - 1.70, RBY - 0.60, 'CONDENSATE', sz=3.4, bold=True, ha='right')
    
    # Column Sump draw to Reboiler bottom channel head
    cad_line(ax, CX - CW/2, CY_BOT + 0.30, RBX, CY_BOT + 0.30, lw=0.8)
    cad_line(ax, RBX, CY_BOT + 0.30, RBX, RBY - RBSH/2 - 0.20, lw=0.8)
    cad_arrow(ax, RBX + 0.30, CY_BOT + 0.30, RBX + 0.05, CY_BOT + 0.30, head_scale=6)
    
    # Reboiler top channel head to Column vapor return
    cad_line(ax, RBX, RBY + RBSH/2 + 0.20, RBX, CY_BOT + 1.60, lw=0.85)
    cad_line(ax, RBX, CY_BOT + 1.60, CX - CW/2, CY_BOT + 1.60, lw=0.85)
    cad_arrow(ax, CX - CW/2 - 0.30, CY_BOT + 1.60, CX - CW/2, CY_BOT + 1.60, head_scale=6)
    
    # ─────────────────────────────────────────────────────────────────────────
    # 9. BOTTOMS PRODUCT & COOLER E-305 (X=5.4, Y=7.8)
    # ─────────────────────────────────────────────────────────────────────────
    # Bottoms liquid draw from column base
    cad_line(ax, CX, CY_BOT - 0.30, CX, 7.80, lw=0.8)
    cad_line(ax, CX, 7.80, 6.00, 7.80, lw=0.8)
    cad_arrow(ax, 6.40, 7.80, 6.00, 7.80, head_scale=5)
    
    # E-305 Trim Cooler (Shell & Tube symbol)
    cad_rect(ax, 4.60, 7.45, 1.20, 0.70, lw=0.75, fill=True)
    cad_line(ax, 4.60, 7.65, 5.80, 7.65, lw=0.35, ls='--')
    cad_text(ax, 5.20, 7.80, 'E-305\nCOOLER', sz=3.4, bold=True)
    cad_line(ax, 4.60, 7.80, 3.40, 7.80, lw=0.75)
    cad_arrow(ax, 3.70, 7.80, 3.30, 7.80, head_scale=5)
    cad_text(ax, 3.20, 8.10, 'BOTTOMS PRODUCT W (25 C)\n(3 wt% AcH, 97 wt% PO)', sz=3.6, bold=True, ha='right')
    
    # ═════════════════════════════════════════════════════════════════════════
    # STREAM FLAGS / NUMBERING DIAMONDS (1 TO 10)
    # ═════════════════════════════════════════════════════════════════════════
    def cad_stream_flag(ax, x, y, num):
        d = 0.24
        pts = [(x, y + d), (x + d*1.2, y), (x, y - d), (x - d*1.2, y)]
        ax.add_patch(Polygon(pts, closed=True, fc='#ffeecc', ec=BK, lw=0.75, zorder=7))
        cad_text(ax, x, y, str(num), sz=4.4, bold=True, zorder=8)
    
    cad_stream_flag(ax, 1.80, PY, 1)            # Raw feed from storage
    cad_stream_flag(ax, 4.40, PY, 2)            # Feed pump discharge
    cad_stream_flag(ax, 8.80, Y_FEED, 3)        # Preheated feed (60% vapor)
    cad_stream_flag(ax, 13.50, CDY, 4)          # Overhead vapor
    cad_stream_flag(ax, 16.00, RY + 0.55, 5)    # Condensed liquid to drum
    cad_stream_flag(ax, 14.20, RPY + 1.60, 6)   # Reflux return (R=3.89)
    cad_stream_flag(ax, 19.20, RPY + 0.42, 7)   # Distillate product D
    cad_stream_flag(ax, 9.40, CY_BOT + 0.30, 8) # Bottoms liquid to reboiler
    cad_stream_flag(ax, 9.40, CY_BOT + 1.60, 9) # Reboiler vapor return
    cad_stream_flag(ax, 4.00, 7.80, 10)         # Bottoms product W
    
    # ═════════════════════════════════════════════════════════════════════════
    # RIGOROUS MASS & ENERGY BALANCE STREAM TABLE (Y = 3.25 TO 7.15)
    # ═════════════════════════════════════════════════════════════════════════
    headers = ['STR', 'DESCRIPTION', 'FLOW (kmol/h)', 'MASS (kg/h)', 'wt% AcH', 'mol% AcH', 'TEMP (C)', 'PRESS (kPa)', 'PHASE']
    rows = [
        ['1', 'Raw Feed from Storage (T-301)', '239.51', '12,000', '50.00', '56.87', '15.0', '101.3', 'Subcooled Liq'],
        ['2', 'Feed Pump Discharge (P-301A/B)', '239.51', '12,000', '50.00', '56.87', '15.2', '250.0', 'Subcooled Liq'],
        ['3', 'Preheated Feed to C-301 (Tray 13)', '239.51', '12,000', '50.00', '56.87', '26.5', '120.0', '60% Vapour (q=0.40)'],
        ['4', 'Overhead Vapour to Condenser (E-303)', '660.63', '29,313', '97.00', '97.71', '20.8', '105.0', 'Vapour (Dew Pt)'],
        ['5', 'Total Condensate to Reflux Drum', '660.63', '29,313', '97.00', '97.71', '20.0', '101.3', 'Saturated Liquid'],
        ['6', 'Reflux Return to Top Tray (R=3.89)', '525.41', '23,313', '97.00', '97.71', '20.0', '140.0', 'Liquid Reflux'],
        ['7', 'Distillate Product D to Storage', '135.22', '6,000', '97.00', '97.71', '20.0', '140.0', 'Liquid Product'],
        ['8', 'Bottoms Liquid to Reboiler (E-302)', '621.21', '35,556', '3.00', '3.92', '33.8', '125.0', 'Saturated Liquid'],
        ['9', 'Reboiler Vapour Return to C-301', '516.92', '29,556', '4.95', '6.43', '34.0', '125.0', 'Stripping Vapour'],
        ['10', 'Bottoms Product W to Cooler (E-305)', '104.29', '6,000', '3.00', '3.92', '25.0', '101.3', 'Liquid Product'],
    ]
    col_w = [1.0, 6.4, 2.6, 2.5, 2.4, 2.4, 1.8, 2.3, 3.2]
    
    cad_draw_table_a4(ax, 2.4, 3.25, headers, rows, col_w,
                      row_h=0.31, title='TABLE 1: RIGOROUS HEAT & MASS BALANCE STREAM DATA (ACETALDEHYDE-PROPYLENE OXIDE)',
                      title_sz=4.6, sz=3.7)
    
    # Save Outputs
    fig.savefig(out_pdf, format='pdf', dpi=300)
    fig.savefig(out_png, format='png', dpi=300)
    plt.close(fig)
    print(f"  [OK] DWG-01 generated: {os.path.basename(out_pdf)}")

if __name__ == '__main__':
    out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Acetaldehyde_PropyleneOxide_Distillation_Drawings')
    os.makedirs(out_dir, exist_ok=True)
    generate_acetaldehyde_dwg01(
        os.path.join(out_dir, '01_Acetaldehyde_Distillation_Process_Flow_Diagram_PFD.pdf'),
        os.path.join(out_dir, '01_Acetaldehyde_Distillation_Process_Flow_Diagram_PFD.png')
    )
