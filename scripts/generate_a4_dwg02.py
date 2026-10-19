"""
A4 OPTIMIZED: DWG-02 INTERNAL ASSEMBLY & PROCESS INTERNALS DETAILED CAD
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

def generate_a4_dwg02(out_pdf, out_png):
    fig, ax = create_a4_canvas()
    draw_a4_border(ax)
    
    # ── 4 Main Internal Detail Panels ────────────────────────────────────────
    # Panel A: Liquid Distributor (Top-Left: X = 0.8 to 9.8, Y = 11.8 to 20.2)
    # Panel B: Mist Eliminator (Top-Center: X = 10.2 to 19.2, Y = 11.8 to 20.2)
    # Panel C: Raschig Ring Geometry (Btm-Left: X = 0.8 to 9.8, Y = 3.4 to 11.4)
    # Panel D: Gas Inlet & Deflector (Btm-Center: X = 10.2 to 19.2, Y = 3.4 to 11.4)
    # Right Side: Tables & Engineering Notes (X = 19.6 to 28.9, Y = 3.4 to 20.2)
    
    # ─────────────────────────────────────────────────────────────────────────
    # DETAIL A: LIQUID DISTRIBUTOR (HEADER-LATERAL PIPE MATRIX)
    # ─────────────────────────────────────────────────────────────────────────
    cad_rect(ax, 0.8, 11.8, 9.0, 8.4, lw=0.85, fill=True)
    cad_text(ax, 5.3, 19.8, 'DETAIL A — LIQUID DISTRIBUTOR', sz=6.0, bold=True)
    cad_text(ax, 5.3, 19.35, 'HEADER-LATERAL MATRIX (SCALE 1:20 METRIC)', sz=4.8, bold=True)
    
    CX_A = 5.3
    CY_A = 16.0
    R_A = 3.3  # Column ID 750 mm scaled
    
    # Shell Walls
    cad_line(ax, CX_A - R_A, CY_A - 2.5, CX_A - R_A, CY_A + 2.5, lw=0.9)
    cad_line(ax, CX_A + R_A, CY_A - 2.5, CX_A + R_A, CY_A + 2.5, lw=0.9)
    cad_line(ax, CX_A, CY_A - 2.8, CX_A, CY_A + 2.8, lw=0.35, ls='-.')
    
    # Water Feed Inlet Nozzle N3 entering from right
    cad_rect(ax, CX_A + R_A, CY_A + 1.2, 0.75, 0.32, lw=0.75, fill=True)
    cad_flange(ax, CX_A + R_A + 0.75, CY_A + 1.36, orientation='H', length=0.55)
    cad_balloon(ax, CX_A + R_A + 1.1, CY_A + 1.85, 'N3', radius=0.20, sz=4.0)
    cad_text(ax, CX_A + R_A + 0.15, CY_A + 0.75, 'N3: WATER IN\nDN 80 CL 150', sz=3.8, ha='left', bold=True)
    
    # Main Header (DN100 / 4" Sch 40S)
    cad_rect(ax, CX_A - 0.45, CY_A - 0.22, 0.90, 0.44, lw=0.85, fill=True)
    cad_text(ax, CX_A, CY_A + 0.40, 'HEADER DN100', sz=3.8, bold=True)
    
    # Laterals (4 branches DN50 / 2" Sch 40S)
    cad_rect(ax, CX_A - R_A + 0.35, CY_A - 0.12, 2 * R_A - 0.70, 0.24, lw=0.75, fill=True)
    
    # Orifices & Spray Jets
    for ox in np.linspace(CX_A - R_A + 0.7, CX_A + R_A - 0.7, 7):
        cad_line(ax, ox - 0.07, CY_A - 0.20, ox + 0.07, CY_A - 0.20, lw=0.7) # Splash baffle
        cad_arrow(ax, ox, CY_A - 0.20, ox, CY_A - 0.75, lw=0.55, head_scale=4)
    cad_text(ax, CX_A, CY_A - 1.15, 'ORIFICES (do = 6 mm, PITCH = 75 mm)\nIRRIGATION DENSITY = 64 PTS/m2', sz=4.0, bold=True, bg='white')
    
    # Wall wiper ring
    cad_line(ax, CX_A - R_A, CY_A - 0.75, CX_A - R_A + 0.55, CY_A - 1.05, lw=0.85)
    cad_line(ax, CX_A + R_A, CY_A - 0.75, CX_A + R_A - 0.55, CY_A - 1.05, lw=0.85)
    cad_text(ax, CX_A, CY_A - 2.05, 'WALL WIPER RING REDIRECTS WALL FLOW', sz=3.8, bold=True)
    cad_dim_h(ax, CX_A - R_A, CX_A + R_A, CY_A + 2.35, 'ID 750 mm')
    
    # ─────────────────────────────────────────────────────────────────────────
    # DETAIL B: MIST ELIMINATOR (KNITTED WIRE MESH DEMISTER)
    # ─────────────────────────────────────────────────────────────────────────
    cad_rect(ax, 10.2, 11.8, 9.0, 8.4, lw=0.85, fill=True)
    cad_text(ax, 14.7, 19.8, 'DETAIL B — MIST ELIMINATOR (DEMISTER)', sz=6.0, bold=True)
    cad_text(ax, 14.7, 19.35, 'KNITTED WIRE MESH (150 mm) — SCALE 1:20 METRIC', sz=4.8, bold=True)
    
    CX_B = 14.7
    CY_B = 15.6
    R_B = 3.3
    
    # Shell Walls
    cad_line(ax, CX_B - R_B, CY_B - 2.6, CX_B - R_B, CY_B + 2.6, lw=0.9)
    cad_line(ax, CX_B + R_B, CY_B - 2.6, CX_B + R_B, CY_B + 2.6, lw=0.9)
    cad_line(ax, CX_B, CY_B - 3.0, CX_B, CY_B + 3.0, lw=0.35, ls='-.')
    
    # Support Ledge Ring (50x8 mm)
    cad_rect(ax, CX_B - R_B, CY_B - 1.1, 0.45, 0.12, lw=0.75, fill=True)
    cad_rect(ax, CX_B + R_B - 0.45, CY_B - 1.1, 0.45, 0.12, lw=0.75, fill=True)
    
    # Demister Pad (150 mm thick)
    h_dem = 1.1
    cad_rect(ax, CX_B - R_B + 0.1, CY_B - h_dem/2, 2 * R_B - 0.2, h_dem, lw=0.85, fill=True)
    cad_hatch_rect(ax, CX_B - R_B + 0.1, CY_B - h_dem/2, 2 * R_B - 0.2, h_dem, pitch=0.14, angle=45, lw=0.25)
    cad_hatch_rect(ax, CX_B - R_B + 0.1, CY_B - h_dem/2, 2 * R_B - 0.2, h_dem, pitch=0.14, angle=-45, lw=0.25)
    
    # Retaining Grids & J-Bolts
    cad_line(ax, CX_B - R_B + 0.1, CY_B - h_dem/2, CX_B + R_B - 0.1, CY_B - h_dem/2, lw=0.85)
    cad_line(ax, CX_B - R_B + 0.1, CY_B + h_dem/2, CX_B + R_B - 0.1, CY_B + h_dem/2, lw=0.85)
    for jx in [CX_B - R_B + 0.3, CX_B + R_B - 0.3]:
        cad_line(ax, jx, CY_B - h_dem/2 - 0.25, jx, CY_B + h_dem/2 + 0.22, lw=0.75)
    
    # Demister Wash Nozzles (N11, DN40)
    cad_line(ax, CX_B - 1.6, CY_B + 1.7, CX_B + 1.6, CY_B + 1.7, lw=0.75)
    for nx in [CX_B - 1.1, CX_B, CX_B + 1.1]:
        cad_circle(ax, nx, CY_B + 1.6, 0.07, fill=True)
        cad_line(ax, nx, CY_B + 1.5, nx - 0.35, CY_B + 0.8, lw=0.45, ls=':')
        cad_line(ax, nx, CY_B + 1.5, nx + 0.35, CY_B + 0.8, lw=0.45, ls=':')
    cad_text(ax, CX_B, CY_B + 2.2, 'N11: DEMISTER FLUSH SYSTEM (DN40)', sz=4.0, bold=True)
    
    cad_text(ax, CX_B, CY_B,
             'KNITTED SS316L / PTFE MESH (150 mm)\n'
             'EFFICIENCY: >99.5% FOR DROPLETS >= 5 um\n'
             'DESIGN DP: 120 Pa AT vG = 0.599 m/s',
             sz=4.0, bold=True, bg='white')
    cad_dim_v(ax, CX_B - R_B - 0.35, CY_B - h_dem/2, CY_B + h_dem/2, '150 mm', text_offset=-0.30)
    
    # ─────────────────────────────────────────────────────────────────────────
    # DETAIL C: 25-mm CERAMIC RASCHIG RING & BED DETAIL
    # ─────────────────────────────────────────────────────────────────────────
    cad_rect(ax, 0.8, 3.4, 9.0, 8.0, lw=0.85, fill=True)
    cad_text(ax, 5.3, 11.0, 'DETAIL C — 25-mm CERAMIC RASCHIG RING', sz=6.0, bold=True)
    cad_text(ax, 5.3, 10.55, 'ORTHOGRAPHIC & 3D ISOMETRIC (SCALE 1:2 METRIC)', sz=4.8, bold=True)
    
    # 3D Isometric View
    RX_ISO = 2.3
    RY_ISO = 7.4
    cad_arc(ax, RX_ISO, RY_ISO + 0.65, 1.5, 0.70, theta1=0, theta2=360, lw=0.85)
    cad_arc(ax, RX_ISO, RY_ISO + 0.65, 0.95, 0.40, theta1=0, theta2=360, lw=0.65)
    cad_line(ax, RX_ISO - 0.75, RY_ISO + 0.65, RX_ISO - 0.75, RY_ISO - 0.65, lw=0.85)
    cad_line(ax, RX_ISO + 0.75, RY_ISO + 0.65, RX_ISO + 0.75, RY_ISO - 0.65, lw=0.85)
    cad_arc(ax, RX_ISO, RY_ISO - 0.65, 1.5, 0.70, theta1=180, theta2=360, lw=0.85)
    cad_text(ax, RX_ISO, RY_ISO - 1.35, '3D ISOMETRIC', sz=4.0, bold=True)
    
    # 2D Orthographic Section
    RX_2D = 4.3
    RY_2D = 7.4
    cad_rect(ax, RX_2D - 0.60, RY_2D - 0.60, 1.2, 1.2, lw=0.85, fill=True)
    cad_hatch_rect(ax, RX_2D - 0.60, RY_2D - 0.60, 0.18, 1.2, pitch=0.10, lw=0.25)
    cad_hatch_rect(ax, RX_2D + 0.42, RY_2D - 0.60, 0.18, 1.2, pitch=0.10, lw=0.25)
    cad_line(ax, RX_2D, RY_2D - 0.85, RX_2D, RY_2D + 0.85, lw=0.30, ls='-.')
    cad_text(ax, RX_2D, RY_2D - 1.35, 'SECTION A-A', sz=4.0, bold=True)
    
    cad_dim_h(ax, RX_2D - 0.60, RX_2D + 0.60, RY_2D + 0.80, 'OD 25 mm')
    cad_dim_v(ax, RX_2D - 0.80, RY_2D - 0.60, RY_2D + 0.60, '25 mm', text_offset=-0.22)
    
    # Specification Block
    cad_text(ax, 5.75, 7.4,
             'CERAMIC PACKING SPECIFICATION:\n'
             '- PACKING RANDOM-DUMPED; NOMINAL SIZE 25 mm\n'
             '- PACKING BED DEPTH: Z = 4500 mm (Vp = 1.79 m3)\n'
             '- Glazed Chemical Porcelain (ASTM C515)\n'
             '- Specific Surface Area: a = 190 m2/m3\n'
             '- Bed Voidage: eps = 0.74 (74% Free Void)\n'
             '- Bulk Density: rho_bulk = 680 kg/m3\n'
             '- Packing Factor: Fp = 100 m-1 (30 ft-1)\n'
             '- Dry Packing Weight: 11.9 kN (1.22 t)',
             sz=3.3, ha='left', bold=True)
    
    # ─────────────────────────────────────────────────────────────────────────
    # DETAIL D: GAS INLET & AERODYNAMIC DEFLECTOR
    # ─────────────────────────────────────────────────────────────────────────
    cad_rect(ax, 10.2, 3.4, 9.0, 8.0, lw=0.85, fill=True)
    cad_text(ax, 14.7, 11.0, 'DETAIL D — GAS INLET & DEFLECTOR', sz=6.0, bold=True)
    cad_text(ax, 14.7, 10.55, 'AERODYNAMIC CHEVRON & SUMP (SCALE 1:20 METRIC)', sz=4.8, bold=True)
    
    CX_D = 14.7
    CY_D = 7.4
    R_D = 3.3
    
    # Shell & Sump
    cad_line(ax, CX_D - R_D, CY_D - 1.1, CX_D - R_D, CY_D + 2.5, lw=0.9)
    cad_line(ax, CX_D + R_D, CY_D - 1.1, CX_D + R_D, CY_D + 2.5, lw=0.9)
    cad_arc(ax, CX_D, CY_D - 1.1, 2 * R_D, 1.5, theta1=180, theta2=360, lw=0.9)
    cad_line(ax, CX_D, CY_D - 2.6, CX_D, CY_D + 2.6, lw=0.35, ls='-.')
    
    # Gas Inlet Nozzle N1
    cad_rect(ax, CX_D - R_D - 0.75, CY_D + 0.35, 0.75, 0.50, lw=0.75, fill=True)
    cad_flange(ax, CX_D - R_D - 0.75, CY_D + 0.60, orientation='H', length=0.75)
    cad_arrow(ax, CX_D - R_D - 1.2, CY_D + 0.60, CX_D - R_D - 0.15, CY_D + 0.60, lw=0.9, head_scale=5)
    cad_balloon(ax, CX_D - R_D - 0.85, CY_D + 1.25, 'N1', radius=0.18, sz=3.8)
    cad_text(ax, CX_D - R_D + 0.1, CY_D - 0.1, 'N1: GAS INLET\nDN 150 CL 150', sz=3.6, ha='left', bold=True)
    
    # 60° Chevron Deflector
    p_def2 = [(CX_D - 1.5, CY_D + 0.1), (CX_D, CY_D + 1.1), (CX_D + 1.5, CY_D + 0.1)]
    ax.add_patch(Polygon(p_def2, closed=False, ec=BK, lw=1.0, fill=False))
    for gx in [-0.85, 0.85]:
        cad_arrow(ax, CX_D + gx, CY_D + 1.3, CX_D + gx, CY_D + 2.2, lw=0.55, head_scale=4)
    cad_text(ax, CX_D, CY_D + 1.6, 'vG = 0.599 m/s', sz=3.6, bold=True, bg='white')
    
    # Anti-Vortex Baffle & Outlet N4
    cad_line(ax, CX_D, CY_D - 1.7, CX_D, CY_D - 1.0, lw=0.85)
    cad_rect(ax, CX_D - 0.14, CY_D - 2.6, 0.28, 0.75, lw=0.75, fill=True)
    cad_flange(ax, CX_D, CY_D - 2.6, orientation='V', length=0.55)
    cad_balloon(ax, CX_D - 0.40, CY_D - 2.6, 'N4', radius=0.18, sz=3.8)
    cad_text(ax, CX_D + 0.35, CY_D - 2.6, 'N4: RICH WATER OUT\nDN 80 (x1 = 2.79 x 10^-4)', sz=3.6, ha='left', bold=True)
    
    # ═════════════════════════════════════════════════════════════════════════
    # RIGHT SIDE: TABLES & NOTES (X = 19.6 to 28.9)
    # ═════════════════════════════════════════════════════════════════════════
    
    # TABLE 1: INTERNALS SPECIFICATIONS
    T1_X = 19.6
    T1_Y = 11.2
    t1_headers = ['INTERNAL', 'MATERIAL / TYPE', 'FUNCTION / CAPACITY']
    t1_widths  = [2.8, 3.2, 3.3]
    t1_rows = [
        ['Distributor',  'SS316L Header-Lateral', '64 pts/m2 irrigation density'],
        ['Redistributor','Titanium Wall Wiper',   'Captures wall-flow liquid'],
        ['Hold-Down',    'SS316L Heavy Grid',     'Prevents ring fluidization'],
        ['Packing Bed',  'Ceramic Raschig 25 mm', 'Z = 4500 mm, Vp = 1.79 m3'],
        ['Support Grid', 'High-Free Area FRP/Ti', 'Free area >85% (anti-flood)'],
        ['Gas Deflector','Titanium 60 DEG Chevron','Reduces 14 m/s to 0.6 m/s'],
        ['Mist Demister','Knitted SS316L/PTFE',   '>99.5% droplet separation'],
    ]
    cad_draw_table_a4(ax, T1_X, T1_Y, t1_headers, t1_rows, t1_widths, row_h=0.38,
                      title='INTERNALS SPECIFICATION SUMMARY', sz=4.2)
    
    # TABLE 2: BILL OF MATERIALS
    T2_X = 19.6
    T2_Y = 7.3
    t2_headers = ['ITEM', 'DESCRIPTION', 'QTY', 'WEIGHT']
    t2_widths  = [1.1, 4.6, 1.4, 2.2]
    t2_rows = [
        ['1', 'Mist Demister Pad',      '1 SET', '18.5 kg'],
        ['2', 'Distributor Manifold',   '1 SET', '45.0 kg'],
        ['3', 'Wall Wiper Rings',       '2 PCS', '14.8 kg'],
        ['4', 'Ceramic Raschig Rings',  '1.79 m3','1220 kg'],
        ['5', 'Support Grid & Cleats',  '1 SET', '65.0 kg'],
        ['6', 'Inlet Deflector Cone',   '1 PC',  '16.5 kg'],
        ['7', 'Anti-Vortex Sump Baffle','1 SET', '11.0 kg'],
    ]
    cad_draw_table_a4(ax, T2_X, T2_Y, t2_headers, t2_rows, t2_widths, row_h=0.38,
                      title='INTERNALS BILL OF MATERIALS (BOM)', sz=4.2)
    
    # NOTES
    N_X = 19.6
    N_Y = 3.4
    W_N = 9.3
    H_N = 3.5
    cad_rect(ax, N_X, N_Y, W_N, H_N, lw=0.85, fill=True)
    cad_text(ax, N_X + W_N/2, N_Y + H_N - 0.28, 'FABRICATION & INSTALLATION NOTES', sz=5.0, bold=True)
    cad_line(ax, N_X, N_Y + H_N - 0.52, N_X + W_N, N_Y + H_N - 0.52, lw=0.6)
    
    notes_dwg2 = [
        "1. DISTRIBUTOR: HORIZONTAL LEVEL +/-1.0 mm OVER 750 mm DIA.",
        "2. WET PACKING: 25-mm RINGS DUMPED IN WATER-FILLED COLUMN.",
        "3. HIGH FREE AREA (>85%): MANDATORY ON PACKING SUPPORT GRID.",
        "4. FASTENERS: TITANIUM GR 2 / HASTELLOY C-276 IN WETTED ZONES.",
    ]
    for idx, nl in enumerate(notes_dwg2):
        cad_text(ax, N_X + 0.35, N_Y + H_N - 0.95 - idx * 0.52, nl, sz=3.8, ha='left', bold=(idx in [0, 1]))
    
    # Title Block
    draw_a4_title_block(
        ax,
        dwg_title='PACKED-BED ABSORBER (C-101) — INTERNAL ASSEMBLY CAD',
        dwg_no='PEDD-PBA-02',
        scale='DETAILED 1:2, 1:20'
    )
    
    fig.savefig(out_pdf, dpi=300, facecolor='white')
    fig.savefig(out_png, dpi=300, facecolor='white')
    plt.close(fig)
    print(f"SUCCESS: Clean A4 DWG-02 generated at {out_pdf}")

if __name__ == '__main__':
    out_dir = r'd:\GAMES\zercxes\CAD_Engineering_Drawings\Packed_Bed_Absorber_Drawings'
    os.makedirs(out_dir, exist_ok=True)
    p_pdf = os.path.join(out_dir, '02_Packed_Bed_Absorber_Internal_Assembly_CAD.pdf')
    p_png = os.path.join(out_dir, '02_Packed_Bed_Absorber_Internal_Assembly_CAD.png')
    generate_a4_dwg02(p_pdf, p_png)
