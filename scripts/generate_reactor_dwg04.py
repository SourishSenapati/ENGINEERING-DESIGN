"""
DWG-04: RIGOROUS CHEMICAL REACTION KINETIC & HYDRAULIC PERFORMANCE CURVES
VAPOR-PHASE ETHYLENE OXIDATION MULTI-TUBULAR REACTOR (R-201)
COUPLED ERGUN PRESSURE DROP ODE INTEGRATION (RK-45) & PARAMETRIC PROFILES
STUDENT: SOURISH SENAPATI | ROLL: 002310301035 | DATE: 17/11/2026
SUBJECT: CHEMICAL REACTION ENGINEERING - II / PEDD | JADAVPUR UNIVERSITY
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

from cad_common import (
    create_cad_canvas, draw_sheet_border, draw_title_block,
    cad_line, cad_rect, cad_circle, cad_arc, cad_text, cad_arrow,
    cad_dim_h, cad_dim_v, cad_dim_leader, cad_balloon, cad_flange,
    cad_hatch_rect, cad_draw_table, W, H, BK, GREY
)

from solve_ethylene_oxide_reactor import solve_reactor

def generate_reactor_dwg04(out_pdf, out_png):
    res = solve_reactor()
    
    fig = plt.figure(figsize=(W / 2.54, H / 2.54), dpi=300)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor('white')
    
    draw_sheet_border(ax)

    # ═════════════════════════════════════════════════════════════════════════
    # HEADER BANNER
    # ═════════════════════════════════════════════════════════════════════════
    cad_text(ax, W / 2.0, H - 2.0, 'TRIPLE-EFFECT / MULTI-STAGE REACTION KINETICS & HYDRAULIC PERFORMANCE CURVES', sz=10.5, bold=True)
    cad_text(ax, W / 2.0, H - 2.8, 'VAPOR-PHASE ETHYLENE OXIDATION MULTI-TUBULAR PACKED BED REACTOR (R-201) — VERIFIED ODE PROFILES', sz=7.8, bold=True, color='#0a3d62')
    cad_line(ax, 8.0, H - 3.4, W - 8.0, H - 3.4, lw=1.2, color='#2980b9')

    # ═════════════════════════════════════════════════════════════════════════
    # EMBED 6 HIGH-PRECISION ENGINEERING PLOTS ACROSS 2 ROWS x 3 COLUMNS
    # Row 1 (Top): Y = 31.0 to 51.5 (height = 20.5 cm)
    # Row 2 (Btm): Y = 8.5 to 29.0 (height = 20.5 cm)
    # Col 1: X = 2.5 to 27.5 (width = 25.0 cm)
    # Col 2: X = 29.5 to 54.5 (width = 25.0 cm)
    # Col 3: X = 56.5 to 81.5 (width = 25.0 cm)
    # ═════════════════════════════════════════════════════════════════════════
    plots_cfg = [
        # (row, col, x0_norm, y0_norm, w_norm, h_norm)
        (0, 0, 0.045, 0.54, 0.28, 0.35),
        (0, 1, 0.365, 0.54, 0.28, 0.35),
        (0, 2, 0.685, 0.54, 0.28, 0.35),
        (1, 0, 0.045, 0.14, 0.28, 0.35),
        (1, 1, 0.365, 0.14, 0.28, 0.35),
        (1, 2, 0.685, 0.14, 0.28, 0.35)
    ]
    
    W_pts = res['W_pts']
    W_final = res['W_final']
    
    c_blue = '#1f77b4'
    c_orange = '#ff7f0e'
    c_green = '#2ca02c'
    c_red = '#d62728'
    c_purple = '#9467bd'
    c_slate = '#34495e'

    # PLOT 1: Conversion Profile X(W)
    ax1 = fig.add_axes([plots_cfg[0][2], plots_cfg[0][3], plots_cfg[0][4], plots_cfg[0][5]])
    ax1.plot(W_pts, res['X_prof'], color=c_blue, lw=2.5, label=r'With Pressure Drop ($\alpha > 0$)')
    ax1.plot(W_pts, res['X_ideal_prof'], color=c_slate, lw=1.8, ls='--', label=r'Zero Pressure Drop ($\alpha = 0$)')
    ax1.axhline(0.40, color=c_red, lw=1.2, ls=':', label='Target Conversion $X = 0.40$')
    ax1.axvline(W_final, color=c_red, lw=1.2, ls=':', label=f'$W = {W_final:.1f}$ lb')
    ax1.scatter([W_final], [0.40], color=c_red, s=60, zorder=5)
    ax1.scatter([res['W_ideal']], [0.40], color=c_slate, s=50, zorder=5)
    ax1.set_title('(a) Conversion Profile $X(W)$', fontsize=11, fontweight='bold', pad=8)
    ax1.set_xlabel('Catalyst Weight $W$ (lb)', fontsize=9.5, fontweight='bold')
    ax1.set_ylabel('Ethylene Conversion $X$', fontsize=9.5, fontweight='bold')
    ax1.set_xlim(0, W_final * 1.05)
    ax1.set_ylim(0, 0.45)
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.legend(loc='lower right', fontsize=8.0, framealpha=0.9)

    # PLOT 2: Pressure Ratio y(W) = P/P0
    ax2 = fig.add_axes([plots_cfg[1][2], plots_cfg[1][3], plots_cfg[1][4], plots_cfg[1][5]])
    ax2.plot(W_pts, res['y_prof'], color=c_red, lw=2.5, label=r'Pressure Ratio $y = P/P_0$')
    ax2.axhline(res['y_final'], color=c_red, lw=1.2, ls=':', label=f'Exit $y = {res["y_final"]:.4f}$')
    ax2.scatter([W_final], [res['y_final']], color=c_red, s=60, zorder=5)
    ax2.set_title('(b) Pressure Profile $y(W) = P/P_0$', fontsize=11, fontweight='bold', pad=8)
    ax2.set_xlabel('Catalyst Weight $W$ (lb)', fontsize=9.5, fontweight='bold')
    ax2.set_ylabel('Dimensionless Pressure $y = P/P_0$', fontsize=9.5, fontweight='bold', color=c_red)
    ax2.set_xlim(0, W_final * 1.05)
    ax2.set_ylim(0.75, 1.02)
    ax2.grid(True, linestyle='--', alpha=0.6)
    
    ax2_twin = ax2.twinx()
    ax2_twin.plot(W_pts, res['P_prof_atm'], color=c_orange, lw=1.5, ls='-.', label=r'Pressure $P$ (atm)')
    ax2_twin.set_ylabel('Total Pressure $P$ (atm)', fontsize=9.5, fontweight='bold', color=c_orange)
    ax2_twin.set_ylim(0.75 * res['P0_atm'], 1.02 * res['P0_atm'])
    ax2.legend(loc='lower left', fontsize=8.0, framealpha=0.9)

    # PLOT 3: Volumetric Flow Ratio v(W)/v0
    ax3 = fig.add_axes([plots_cfg[2][2], plots_cfg[2][3], plots_cfg[2][4], plots_cfg[2][5]])
    ax3.plot(W_pts, res['v_ratio_prof'], color=c_green, lw=2.5, label=r'$\frac{v}{v_0} = \frac{1 + \epsilon_A X}{y}$')
    ax3.plot(W_pts, 1.0 + res['eps'] * res['X_prof'], color=c_slate, lw=1.8, ls='--', label=r'Molar Ratio $\frac{F_T}{F_{T0}} = 1 + \epsilon_A X$')
    ax3.axhline(1.0, color='gray', lw=1.0, ls='-')
    ax3.axhline(res['v_ratio_final'], color=c_green, lw=1.2, ls=':', label=f'Exit $\\frac{{v}}{{v_0}} = {res["v_ratio_final"]:.4f}$')
    ax3.scatter([W_final], [res['v_ratio_final']], color=c_green, s=60, zorder=5)
    ax3.set_title('(c) Volumetric Flow Ratio $v(W)/v_0$', fontsize=11, fontweight='bold', pad=8)
    ax3.set_xlabel('Catalyst Weight $W$ (lb)', fontsize=9.5, fontweight='bold')
    ax3.set_ylabel('Ratio $v/v_0$', fontsize=9.5, fontweight='bold')
    ax3.set_xlim(0, W_final * 1.05)
    ax3.set_ylim(0.85, 1.20)
    ax3.grid(True, linestyle='--', alpha=0.6)
    ax3.legend(loc='upper left', fontsize=8.0, framealpha=0.9)

    # PLOT 4: Partial Pressures PA, PB, PC, PI
    ax4 = fig.add_axes([plots_cfg[3][2], plots_cfg[3][3], plots_cfg[3][4], plots_cfg[3][5]])
    ax4.plot(W_pts, res['PA_prof'], color=c_blue, lw=2.2, label=r'$P_A$ (Ethylene, $\text{C}_2\text{H}_4$)')
    ax4.plot(W_pts, res['PB_prof'], color=c_orange, lw=2.2, label=r'$P_B$ (Oxygen, $\text{O}_2$)')
    ax4.plot(W_pts, res['PC_prof'], color=c_green, lw=2.2, label=r'$P_C$ (Ethylene Oxide, $\text{C}_2\text{H}_4\text{O}$)')
    ax4.plot(W_pts, res['PI_prof'], color=c_slate, lw=1.8, ls=':', label=r'$P_I$ (Nitrogen Carrier, $\text{N}_2$)')
    ax4.set_title('(d) Reactant & Product Partial Pressures', fontsize=11, fontweight='bold', pad=8)
    ax4.set_xlabel('Catalyst Weight $W$ (lb)', fontsize=9.5, fontweight='bold')
    ax4.set_ylabel('Partial Pressure (atm)', fontsize=9.5, fontweight='bold')
    ax4.set_xlim(0, W_final * 1.05)
    ax4.set_ylim(0, 16.0)
    ax4.grid(True, linestyle='--', alpha=0.6)
    ax4.legend(loc='center right', fontsize=8.0, framealpha=0.9)

    # PLOT 5: Reaction Rate Profile -rA'(W)
    ax5 = fig.add_axes([plots_cfg[4][2], plots_cfg[4][3], plots_cfg[4][4], plots_cfg[4][5]])
    ax5.plot(W_pts, res['rate_prof'], color=c_purple, lw=2.5, label=r"$-r'_A = k' y \frac{1-X}{1+\epsilon_A X}$")
    ax5.scatter([0], [res['rate_prof'][0]], color=c_purple, s=50)
    ax5.scatter([W_final], [res['rate_prof'][-1]], color=c_purple, s=50)
    ax5.set_title(r"(e) Reaction Rate Profile $-r'_A(W)$", fontsize=11, fontweight='bold', pad=8)
    ax5.set_xlabel('Catalyst Weight $W$ (lb)', fontsize=9.5, fontweight='bold')
    ax5.set_ylabel(r"$-r'_A$ [$\text{lbmol}/(\text{lb cat}\cdot\text{h})$]", fontsize=9.5, fontweight='bold')
    ax5.set_xlim(0, W_final * 1.05)
    ax5.set_ylim(0, res['rate_prof'][0] * 1.1)
    ax5.grid(True, linestyle='--', alpha=0.6)
    ax5.legend(loc='upper right', fontsize=8.0, framealpha=0.9)

    # PLOT 6: Hydraulic Sensitivity vs Tube Count Nt
    ax6 = fig.add_axes([plots_cfg[5][2], plots_cfg[5][3], plots_cfg[5][4], plots_cfg[5][5]])
    Nt_range = np.linspace(800, 2000, 13)
    L_list = []
    dP_list = []
    for nt in Nt_range:
        r_nt = solve_reactor(Nt=int(nt))
        L_list.append(r_nt['L_tube_final'])
        dP_list.append(r_nt['deltaP_atm'])

    ax6.plot(Nt_range, L_list, color=c_blue, lw=2.2, label='Tube Length $L$ (ft)')
    ax6.axvline(1000, color='gray', lw=1.2, ls='--', label=r'Design Point ($N_t = 1000$)')
    ax6.scatter([1000], [res['L_tube_final']], color=c_blue, s=60, zorder=5)
    ax6.set_title('(f) Hydraulic Sensitivity vs Tube Count $N_t$', fontsize=11, fontweight='bold', pad=8)
    ax6.set_xlabel('Number of Tubes in Parallel $N_t$', fontsize=9.5, fontweight='bold')
    ax6.set_ylabel('Packed Tube Length $L$ (ft)', fontsize=9.5, fontweight='bold', color=c_blue)
    ax6.grid(True, linestyle='--', alpha=0.6)

    ax6_twin = ax6.twinx()
    ax6_twin.plot(Nt_range, dP_list, color=c_red, lw=2.2, ls='-.', label=r'Pressure Drop $\Delta P$ (atm)')
    ax6_twin.scatter([1000], [res['deltaP_atm']], color=c_red, s=60, zorder=5)
    ax6_twin.set_ylabel(r'Pressure Drop $\Delta P$ (atm)', fontsize=9.5, fontweight='bold', color=c_red)

    lines_1, labels_1 = ax6.get_legend_handles_labels()
    lines_2, labels_2 = ax6_twin.get_legend_handles_labels()
    ax6.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right', fontsize=8.0, framealpha=0.9)

    # ═════════════════════════════════════════════════════════════════════════
    # TITLE BLOCK (Bottom Full Width)
    # ═════════════════════════════════════════════════════════════════════════
    draw_title_block(
        ax,
        dwg_title='RIGOROUS REACTION KINETICS & HYDRAULIC PERFORMANCE CURVES',
        dwg_no='DWG-04',
        rev='00',
        sheet_no='04 OF 05',
        scale='ENGINEERING PLOTS / MATHEMATICALLY VERIFIED',
        equip_desc='ETHYLENE OXIDATION MULTI-TUBULAR REACTOR (R-201) — KINETIC & PRESSURE PROFILES',
        duty_desc='COUPLED ODE SOLUTION | W_ACTUAL = 26,469 LB | deltaP = 4.00 ATM | EXIT v/v0 = 1.1202'
    )

    plt.savefig(out_png, dpi=300)
    plt.savefig(out_pdf)
    plt.close()
    print(f"[SUCCESS] DWG-04 generated: {out_png}")
    print(f"[SUCCESS] DWG-04 generated: {out_pdf}")

if __name__ == '__main__':
    out_dir = r"d:\GAMES\zercxes\CAD_Engineering_Drawings"
    generate_reactor_dwg04(
        os.path.join(out_dir, "04_Ethylene_Oxide_Reactor_Kinetic_Hydraulic_Performance_Curves_CAD.pdf"),
        os.path.join(out_dir, "04_Ethylene_Oxide_Reactor_Kinetic_Hydraulic_Performance_Curves_CAD.png")
    )
