#!/usr/bin/env python3
"""
solve_ethylene_oxide_reactor.py
================================================================================
Rigorous Chemical Reaction Engineering & Hydraulic Design Suite
Problem R2: Vapor-Phase Catalytic Oxidation of Ethylene to Ethylene Oxide
             in an Isothermal Packed-Bed Tubular Reactor with Pressure Drop
================================================================================
"""

import os
import sys
import argparse
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path as MPath

def solve_reactor(
    P0_atm=25.0,
    T_C=260.0,
    FA0_s=0.9,
    X_target=0.40,
    k_rate=0.0141,
    Dp_in=0.5,
    rho_c_lbft3=140.0,
    phi=0.5,
    nom_dia_in=1.5,
    schedule=80,
    Nt=1000
):
    # -------------------------------------------------------------------------
    # 1. Thermodynamics & Physical Properties
    # -------------------------------------------------------------------------
    P0_psia = P0_atm * 14.6959488
    P0_psf = P0_psia * 144.0  # lbf / ft^2
    P0_Pa = P0_atm * 101325.0

    T_K = T_C + 273.15
    T_F = T_C * 9.0 / 5.0 + 32.0  # 500.0 F
    T_R = T_F + 459.67            # 959.67 R

    # Gas constant
    R_eng = 10.73159  # psia * ft^3 / (lbmol * R)
    R_SI = 8.314462   # J / (mol * K)

    # Reacting fluid properties identical to air at 260 C
    M_air = 28.97  # lb / lbmol (kg / kmol)
    rho0 = (P0_psia * M_air) / (R_eng * T_R)  # lb / ft^3
    rho0_kgm3 = (P0_Pa * 0.02897) / (R_SI * T_K)

    # Viscosity of air at 260 C (0.027 cP)
    mu_cP = 0.027
    mu = mu_cP * 6.719689e-4  # lb / (ft * s) = 1.8143e-5 lb / (ft * s)
    mu_lb_fth = mu * 3600.0   # lb / (ft * h)
    gc = 32.174               # lbm * ft / (lbf * s^2)

    # Catalyst bed properties
    Dp_ft = (Dp_in) / 12.0
    rho_b = rho_c_lbft3 * (1.0 - phi)  # Bulk density = 70 lb/ft^3

    # Feed molar rates
    FA0_h = FA0_s * 3600.0  # 3240.0 lbmol/h
    theta_B = 0.5           # Stoichiometric proportion: 0.5 mol O2 / mol C2H4
    theta_I = 0.5 * (79.0 / 21.0)  # 1.880952 mol N2 / mol C2H4
    theta_total = 1.0 + theta_B + theta_I  # 3.380952 mol total / mol C2H4

    yA0 = 1.0 / theta_total          # 0.295775
    yB0 = theta_B / theta_total      # 0.147887
    yI0 = theta_I / theta_total      # 0.556338

    PA0 = yA0 * P0_atm               # 7.39437 atm
    PB0 = yB0 * P0_atm               # 3.69718 atm

    # Stoichiometric expansion parameter: delta = 1 - (1 + 0.5) = -0.5
    delta = 1.0 - (1.0 + 0.5)
    eps = yA0 * delta                # -0.147887

    # Rate Law: -rA' = k * PA^(1/3) * PB^(2/3)
    # Since PB = 0.5 * PA at all conversions: -rA' = k * (0.5)^(2/3) * PA
    # With PA = PA0 * y * (1 - X) / (1 + eps * X):
    # -rA' = k_eff * y * (1 - X) / (1 + eps * X)
    k_eff = k_rate * (0.5**(2.0 / 3.0)) * PA0  # lbmol / (lb cat * h)

    # Total mass feed rate
    FT0_s = FA0_s * theta_total      # 3.042857 lbmol/s
    m_dot_total = FT0_s * M_air      # 88.1516 lb/s

    # -------------------------------------------------------------------------
    # 2. Reactor Tube Dimensions (Schedule 80)
    # -------------------------------------------------------------------------
    if nom_dia_in == 1.5 and schedule == 80:
        OD_in = 1.900
        ID_in = 1.500
        t_w_in = 0.200
    elif nom_dia_in == 1.0 and schedule == 80:
        OD_in = 1.315
        ID_in = 0.957
        t_w_in = 0.179
    elif nom_dia_in == 2.0 and schedule == 80:
        OD_in = 2.375
        ID_in = 1.939
        t_w_in = 0.218
    else:
        OD_in = nom_dia_in * 1.25
        ID_in = nom_dia_in
        t_w_in = (OD_in - ID_in) / 2.0

    ID_ft = ID_in / 12.0
    Ac1 = np.pi * (ID_ft**2) / 4.0  # Cross section area of single tube, ft^2
    Ac_total = Nt * Ac1            # Total cross section flow area, ft^2

    # Mass velocity
    G = m_dot_total / Ac_total     # lb / (ft^2 * s)

    # Ergun Equation Parameter beta0 (pressure drop per unit length at inlet)
    # beta0 = [G / (rho0 * gc * Dp)] * [(1 - phi) / phi^3] * [150 * (1 - phi) * mu / Dp + 1.75 * G]
    term1 = G / (rho0 * gc * Dp_ft)
    term2 = (1.0 - phi) / (phi**3)
    term3 = (150.0 * (1.0 - phi) * mu / Dp_ft) + (1.75 * G)
    beta0 = term1 * term2 * term3  # lbf / ft^3 = psf / ft

    # Fogler alpha parameter per total catalyst weight
    # alpha = 2 * beta0 / (P0_psf * rho_b * Ac_total)
    alpha = (2.0 * beta0) / (P0_psf * rho_b * Ac_total)  # 1 / lb cat

    # -------------------------------------------------------------------------
    # 3. Analytical Solution for Zero Pressure Drop (alpha = 0, y = 1)
    # -------------------------------------------------------------------------
    # dX/dW = (k_eff / FA0) * (1 - X) / (1 + eps * X)
    # W = (FA0 / k_eff) * [ (1 + eps) * ln(1/(1-X)) - eps * X ]
    integral_ideal = (1.0 + eps) * np.log(1.0 / (1.0 - X_target)) - eps * X_target
    W_ideal = (FA0_h / k_eff) * integral_ideal

    # -------------------------------------------------------------------------
    # 4. Numerical ODE Solution with Pressure Drop (alpha > 0)
    # -------------------------------------------------------------------------
    def odes(W, Y):
        X, y = Y
        if y <= 1e-4 or X >= 0.9999:
            return [0.0, 0.0]
        dX_dW = (k_eff / FA0_h) * y * (1.0 - X) / (1.0 + eps * X)
        dy_dW = - (alpha / (2.0 * y)) * (1.0 + eps * X)
        return [dX_dW, dy_dW]

    def reach_conversion(W, Y):
        return Y[0] - X_target
    reach_conversion.terminal = True

    sol = solve_ivp(
        odes,
        [0.0, 150000.0],
        [0.0, 1.0],
        events=reach_conversion,
        dense_output=True,
        rtol=1e-10,
        atol=1e-13
    )

    if len(sol.t_events[0]) > 0:
        W_final = sol.t_events[0][0]
        X_final, y_final = sol.y_events[0][0]
    else:
        W_final = sol.t[-1]
        X_final = sol.y[0, -1]
        y_final = sol.y[1, -1]

    # Generate fine profile along catalyst weight W
    W_pts = np.linspace(0.0, W_final, 500)
    Y_pts = sol.sol(W_pts)
    X_prof = Y_pts[0]
    y_prof = Y_pts[1]

    # Volumetric flow ratio profile: v / v0 = (1 + eps * X) / y
    v_ratio_prof = (1.0 + eps * X_prof) / y_prof
    P_prof_atm = y_prof * P0_atm
    P_prof_psia = y_prof * P0_psia

    # Partial pressure profiles
    PA_prof = PA0 * y_prof * (1.0 - X_prof) / (1.0 + eps * X_prof)
    PB_prof = 0.5 * PA_prof
    PC_prof = PA0 * y_prof * X_prof / (1.0 + eps * X_prof)
    PI_prof = theta_I * PA0 * y_prof / (1.0 + eps * X_prof)

    # Reaction rate profile
    rate_prof = k_eff * y_prof * (1.0 - X_prof) / (1.0 + eps * X_prof)

    # Ideal profile (no pressure drop) for comparison
    def X_ideal_func(W):
        from scipy.optimize import root_scalar
        res_list = []
        for w in W:
            def f(x):
                return (FA0_h / k_eff) * ((1.0 + eps) * np.log(1.0 / (1.0 - x)) - eps * x) - w
            sol_x = root_scalar(f, bracket=[0.0, 0.9999], method='brentq')
            res_list.append(sol_x.root)
        return np.array(res_list)

    X_ideal_prof = X_ideal_func(W_pts)

    # Tube length profile: L(W) = W_tube / (rho_b * Ac1)
    L_tube_final = (W_final / Nt) / (rho_b * Ac1)

    results = {
        'P0_atm': P0_atm,
        'P0_psia': P0_psia,
        'T_C': T_C,
        'T_R': T_R,
        'FA0_h': FA0_h,
        'FA0_s': FA0_s,
        'M_air': M_air,
        'rho0': rho0,
        'mu': mu,
        'Dp_in': Dp_in,
        'Dp_ft': Dp_ft,
        'phi': phi,
        'rho_c': rho_c_lbft3,
        'rho_b': rho_b,
        'theta_B': theta_B,
        'theta_I': theta_I,
        'yA0': yA0,
        'PA0': PA0,
        'eps': eps,
        'k_eff': k_eff,
        'OD_in': OD_in,
        'ID_in': ID_in,
        't_w_in': t_w_in,
        'Ac1': Ac1,
        'Nt': Nt,
        'Ac_total': Ac_total,
        'G': G,
        'beta0': beta0,
        'alpha': alpha,
        'W_ideal': W_ideal,
        'W_final': W_final,
        'X_final': X_final,
        'y_final': y_final,
        'P_exit_atm': y_final * P0_atm,
        'P_exit_psia': y_final * P0_psia,
        'deltaP_atm': (1.0 - y_final) * P0_atm,
        'deltaP_psia': (1.0 - y_final) * P0_psia,
        'v_ratio_final': (1.0 + eps * X_final) / y_final,
        'L_tube_final': L_tube_final,
        'W_pts': W_pts,
        'X_prof': X_prof,
        'X_ideal_prof': X_ideal_prof,
        'y_prof': y_prof,
        'v_ratio_prof': v_ratio_prof,
        'P_prof_atm': P_prof_atm,
        'P_prof_psia': P_prof_psia,
        'PA_prof': PA_prof,
        'PB_prof': PB_prof,
        'PC_prof': PC_prof,
        'PI_prof': PI_prof,
        'rate_prof': rate_prof
    }
    return results

def print_solution_report(res):
    print("=" * 80)
    print(" VAPOR-PHASE ETHYLENE OXIDATION TUBULAR REACTOR DESIGN (PROBLEM R2)")
    print(" Rigorous Analytical & Numerical Solution Accounting for Pressure Drop")
    print("=" * 80)
    print(f"Feed Conditions:")
    print(f"  Ethylene Feed Rate, FA0:       {res['FA0_s']:.3f} lbmol/s  ({res['FA0_h']:.1f} lbmol/h)")
    print(f"  Inlet Total Pressure, P0:      {res['P0_atm']:.2f} atm  ({res['P0_psia']:.2f} psia)")
    print(f"  Reactor Temperature, T:        {res['T_C']:.1f} deg C  ({res['T_R']:.2f} R, Isothermal)")
    print(f"  Gas Molecular Weight, M:       {res['M_air']:.2f} lb/lbmol")
    print(f"  Gas Density at Inlet, rho0:    {res['rho0']:.4f} lb/ft^3")
    print(f"  Gas Viscosity at Inlet, mu:    {res['mu']:.5e} lb/(ft*s)  (0.027 cP)")
    print()
    print(f"Stoichiometry & Kinetics:")
    print(f"  Stoichiometric Ratio, theta_B: {res['theta_B']:.4f} (0.5 mol O2 / mol C2H4)")
    print(f"  Inerts Ratio (Air N2), theta_I:{res['theta_I']:.4f} (1.881 mol N2 / mol C2H4)")
    print(f"  Inlet Mole Fraction, yA0:      {res['yA0']:.5f}")
    print(f"  Inlet Partial Pressure, PA0:   {res['PA0']:.4f} atm  ({res['PA0']*14.696:.2f} psia)")
    print(f"  Expansion Parameter, eps_A:    {res['eps']:.5f}")
    print(f"  Effective Rate Constant, k':   {res['k_eff']:.6f} lbmol/(lb cat * h)")
    print(f"  Specific Velocity, k'/FA0:     {res['k_eff']/res['FA0_h']:.6e} 1/lb cat")
    print()
    print(f"Reactor Mechanical & Packed-Bed Geometry:")
    print(f"  Tube Schedule:                 1.5-in Schedule 80 (ID = {res['ID_in']:.3f} in, OD = {res['OD_in']:.3f} in)")
    print(f"  Single Tube Flow Area, Ac1:    {res['Ac1']:.6f} ft^2  ({res['Ac1']*144:.3f} in^2)")
    print(f"  Total Number of Tubes, Nt:     {res['Nt']:d} tubes in parallel")
    print(f"  Total Cross-Section Area, Ac:  {res['Ac_total']:.4f} ft^2")
    print(f"  Catalyst Pellet Diameter, Dp:  {res['Dp_in']:.2f} in  ({res['Dp_ft']:.5f} ft)")
    print(f"  Bed Void Fraction, phi:        {res['phi']:.2f}")
    print(f"  Catalyst Bulk Density, rho_b:  {res['rho_b']:.1f} lb/ft^3  (Solid = {res['rho_c']:.1f} lb/ft^3)")
    print()
    print(f"Ergun Fluid Dynamics & Hydraulics:")
    print(f"  Superficial Mass Velocity, G:  {res['G']:.3f} lb/(ft^2 * s)")
    print(f"  Inlet Pressure Gradient, beta0:{res['beta0']:.3f} psf/ft  ({res['beta0']/144:.4f} psi/ft)")
    print(f"  Pressure Drop Parameter, alpha:{res['alpha']:.6e} 1/lb cat")
    print()
    print(f"Design Comparison at X = {res['X_final']:.2f} (40% Conversion):")
    print(f"  Ideal Weight (Zero Pressure Drop): {res['W_ideal']:.2f} lb cat  ({res['W_ideal']/2.20462:.2f} kg)")
    print(f"  Actual Weight (With Pressure Drop):{res['W_final']:.2f} lb cat  ({res['W_final']/2.20462:.2f} kg)")
    print(f"  Excess Catalyst Due to dP:         +{res['W_final']-res['W_ideal']:.2f} lb cat (+{(res['W_final']-res['W_ideal'])/res['W_ideal']*100:.2f}%)")
    print(f"  Catalyst Weight per Tube:          {res['W_final']/res['Nt']:.4f} lb cat/tube")
    print(f"  Packed Bed Length per Tube, L:     {res['L_tube_final']:.2f} ft  ({res['L_tube_final']*0.3048:.2f} m)")
    print(f"  Exit Pressure Ratio, y = P/P0:     {res['y_final']:.5f}")
    print(f"  Exit Pressure, P:                  {res['P_exit_atm']:.3f} atm  ({res['P_exit_psia']:.2f} psia)")
    print(f"  Total Pressure Drop, deltaP:       {res['deltaP_atm']:.3f} atm  ({res['deltaP_psia']:.2f} psi, {res['deltaP_atm']/res['P0_atm']*100:.2f}%)")
    print(f"  Volumetric Flow Ratio, v/v0:       {res['v_ratio_final']:.5f}  (+{(res['v_ratio_final']-1.0)*100:.2f}% expansion)")
    print("=" * 80)

def generate_performance_plots(res, out_png, out_pdf):
    fig, axs = plt.subplots(2, 3, figsize=(18, 11), dpi=300)
    fig.patch.set_facecolor('#ffffff')

    W = res['W_pts']
    W_final = res['W_final']

    # Colors
    c_blue = '#1f77b4'
    c_orange = '#ff7f0e'
    c_green = '#2ca02c'
    c_red = '#d62728'
    c_purple = '#9467bd'
    c_slate = '#34495e'

    # Subplot 1: Conversion Profile X(W)
    ax1 = axs[0, 0]
    ax1.plot(W, res['X_prof'], color=c_blue, lw=2.5, label=r'With Pressure Drop ($\alpha > 0$)')
    ax1.plot(W, res['X_ideal_prof'], color=c_slate, lw=1.8, ls='--', label=r'Zero Pressure Drop ($\alpha = 0$)')
    ax1.axhline(0.40, color=c_red, lw=1.2, ls=':', label='Target Conversion $X = 0.40$')
    ax1.axvline(W_final, color=c_red, lw=1.2, ls=':', label=f'$W = {W_final:.1f}$ lb')
    ax1.scatter([W_final], [0.40], color=c_red, s=60, zorder=5)
    ax1.scatter([res['W_ideal']], [0.40], color=c_slate, s=50, zorder=5)
    ax1.set_title('(a) Conversion Profile $X(W)$', fontsize=12, fontweight='bold', pad=10)
    ax1.set_xlabel('Catalyst Weight $W$ (lb)', fontsize=10, fontweight='bold')
    ax1.set_ylabel('Ethylene Conversion $X$', fontsize=10, fontweight='bold')
    ax1.set_xlim(0, W_final * 1.05)
    ax1.set_ylim(0, 0.45)
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.legend(loc='lower right', fontsize=8.5, framealpha=0.9)

    # Subplot 2: Pressure Ratio y(W) = P/P0 and Total Pressure P(W)
    ax2 = axs[0, 1]
    ax2.plot(W, res['y_prof'], color=c_red, lw=2.5, label=r'Pressure Ratio $y = P/P_0$')
    ax2.axhline(res['y_final'], color=c_red, lw=1.2, ls=':', label=f'Exit $y = {res["y_final"]:.4f}$')
    ax2.scatter([W_final], [res['y_final']], color=c_red, s=60, zorder=5)
    ax2.set_title('(b) Pressure Profile $y(W) = P/P_0$', fontsize=12, fontweight='bold', pad=10)
    ax2.set_xlabel('Catalyst Weight $W$ (lb)', fontsize=10, fontweight='bold')
    ax2.set_ylabel('Dimensionless Pressure $y = P/P_0$', fontsize=10, fontweight='bold', color=c_red)
    ax2.set_xlim(0, W_final * 1.05)
    ax2.set_ylim(0.75, 1.02)
    ax2.grid(True, linestyle='--', alpha=0.6)

    # Second y-axis for Absolute Pressure (atm / psia)
    ax2_twin = ax2.twinx()
    ax2_twin.plot(W, res['P_prof_atm'], color=c_orange, lw=1.5, ls='-.', label=r'Pressure $P$ (atm)')
    ax2_twin.set_ylabel('Total Pressure $P$ (atm)', fontsize=10, fontweight='bold', color=c_orange)
    ax2_twin.set_ylim(0.75 * res['P0_atm'], 1.02 * res['P0_atm'])
    ax2.legend(loc='lower left', fontsize=8.5, framealpha=0.9)

    # Subplot 3: Volumetric Flow Rate Ratio v(W) / v0
    ax3 = axs[0, 2]
    ax3.plot(W, res['v_ratio_prof'], color=c_green, lw=2.5, label=r'$\frac{v}{v_0} = \frac{1 + \epsilon_A X}{y}$')
    ax3.plot(W, 1.0 + res['eps'] * res['X_prof'], color=c_slate, lw=1.8, ls='--', label=r'Molar Ratio $\frac{F_T}{F_{T0}} = 1 + \epsilon_A X$')
    ax3.axhline(1.0, color='gray', lw=1.0, ls='-')
    ax3.axhline(res['v_ratio_final'], color=c_green, lw=1.2, ls=':', label=f'Exit $\\frac{{v}}{{v_0}} = {res["v_ratio_final"]:.4f}$')
    ax3.scatter([W_final], [res['v_ratio_final']], color=c_green, s=60, zorder=5)
    ax3.set_title('(c) Volumetric Flow Ratio $v(W)/v_0$', fontsize=12, fontweight='bold', pad=10)
    ax3.set_xlabel('Catalyst Weight $W$ (lb)', fontsize=10, fontweight='bold')
    ax3.set_ylabel('Ratio $v/v_0$', fontsize=10, fontweight='bold')
    ax3.set_xlim(0, W_final * 1.05)
    ax3.set_ylim(0.85, 1.20)
    ax3.grid(True, linestyle='--', alpha=0.6)
    ax3.legend(loc='upper left', fontsize=8.5, framealpha=0.9)

    # Subplot 4: Partial Pressure Profiles PA, PB, PC, PI
    ax4 = axs[1, 0]
    ax4.plot(W, res['PA_prof'], color=c_blue, lw=2.2, label=r'$P_A$ (Ethylene, $\text{C}_2\text{H}_4$)')
    ax4.plot(W, res['PB_prof'], color=c_orange, lw=2.2, label=r'$P_B$ (Oxygen, $\text{O}_2$)')
    ax4.plot(W, res['PC_prof'], color=c_green, lw=2.2, label=r'$P_C$ (Ethylene Oxide, $\text{C}_2\text{H}_4\text{O}$)')
    ax4.plot(W, res['PI_prof'], color=c_slate, lw=1.8, ls=':', label=r'$P_I$ (Nitrogen Carrier, $\text{N}_2$)')
    ax4.set_title('(d) Reactant & Product Partial Pressures', fontsize=12, fontweight='bold', pad=10)
    ax4.set_xlabel('Catalyst Weight $W$ (lb)', fontsize=10, fontweight='bold')
    ax4.set_ylabel('Partial Pressure (atm)', fontsize=10, fontweight='bold')
    ax4.set_xlim(0, W_final * 1.05)
    ax4.set_ylim(0, 16.0)
    ax4.grid(True, linestyle='--', alpha=0.6)
    ax4.legend(loc='center right', fontsize=8.5, framealpha=0.9)

    # Subplot 5: Reaction Rate Profile -rA'(W)
    ax5 = axs[1, 1]
    ax5.plot(W, res['rate_prof'], color=c_purple, lw=2.5, label=r"$-r'_A = k' y \frac{1-X}{1+\epsilon_A X}$")
    ax5.scatter([0], [res['rate_prof'][0]], color=c_purple, s=50)
    ax5.scatter([W_final], [res['rate_prof'][-1]], color=c_purple, s=50)
    ax5.set_title(r"(e) Reaction Rate Profile $-r'_A(W)$", fontsize=12, fontweight='bold', pad=10)
    ax5.set_xlabel('Catalyst Weight $W$ (lb)', fontsize=10, fontweight='bold')
    ax5.set_ylabel(r"$-r'_A$ [$\text{lbmol}/(\text{lb cat}\cdot\text{h})$]", fontsize=10, fontweight='bold')
    ax5.set_xlim(0, W_final * 1.05)
    ax5.set_ylim(0, res['rate_prof'][0] * 1.1)
    ax5.grid(True, linestyle='--', alpha=0.6)
    ax5.legend(loc='upper right', fontsize=8.5, framealpha=0.9)

    # Subplot 6: Parametric Study - Tube Count Nt vs Length L & Pressure Drop
    ax6 = axs[1, 2]
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
    ax6.set_title('(f) Hydraulic Sensitivity vs Tube Count $N_t$', fontsize=12, fontweight='bold', pad=10)
    ax6.set_xlabel('Number of Tubes in Parallel $N_t$', fontsize=10, fontweight='bold')
    ax6.set_ylabel('Packed Tube Length $L$ (ft)', fontsize=10, fontweight='bold', color=c_blue)
    ax6.grid(True, linestyle='--', alpha=0.6)

    ax6_twin = ax6.twinx()
    ax6_twin.plot(Nt_range, dP_list, color=c_red, lw=2.2, ls='-.', label=r'Pressure Drop $\Delta P$ (atm)')
    ax6_twin.scatter([1000], [res['deltaP_atm']], color=c_red, s=60, zorder=5)
    ax6_twin.set_ylabel(r'Pressure Drop $\Delta P$ (atm)', fontsize=10, fontweight='bold', color=c_red)

    lines_1, labels_1 = ax6.get_legend_handles_labels()
    lines_2, labels_2 = ax6_twin.get_legend_handles_labels()
    ax6.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right', fontsize=8.0, framealpha=0.9)

    plt.suptitle(
        'VAPOR-PHASE ETHYLENE OXIDATION IN PACKED-BED TUBULAR REACTOR (PROBLEM R2)\n'
        r'Isothermal Operation at $260^\circ\text{C}$, $P_0 = 25\text{ atm}$, $F_{A0} = 0.9\text{ lbmol/s}$, $X = 0.40$, 1.5-in Sch 80 Tubes ($N_t = 1000$)',
        fontsize=13, fontweight='bold', y=0.98
    )
    plt.tight_layout(rect=[0, 0.03, 1, 0.94])

    plt.savefig(out_png, dpi=300)
    plt.savefig(out_pdf)
    plt.close()
    print(f"[SUCCESS] Performance plot saved: {out_png}")
    print(f"[SUCCESS] Performance plot saved: {out_pdf}")

def generate_scale_cad_drawing(res, out_png, out_pdf):
    """
    Renders an engineering-grade, to-scale CAD General Arrangement & Detail Drawing
    of the Multi-Tubular Packed-Bed Catalytic Reactor for Ethylene Oxide Production.
    Standard ANSI/ASME layout with Title Block, Bill of Materials, Sectional Views,
    and Exact Proportional Sizing.
    """
    fig = plt.figure(figsize=(20, 14), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax = fig.add_subplot(111)
    ax.set_facecolor('#ffffff')

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 72)
    ax.axis('off')

    # Borders
    ax.plot([1.2, 98.8, 98.8, 1.2, 1.2], [1.2, 1.2, 70.8, 70.8, 1.2], color='#111111', lw=2.2)
    ax.plot([1.7, 98.3, 98.3, 1.7, 1.7], [1.7, 1.7, 70.3, 70.3, 1.7], color='#111111', lw=1.0)

    # -------------------------------------------------------------------------
    # MAIN HEADER
    # -------------------------------------------------------------------------
    ax.text(50.0, 68.8, 'VAPOR-PHASE ETHYLENE OXIDATION MULTI-TUBULAR PACKED-BED REACTOR',
            fontsize=13.5, fontweight='bold', ha='center', va='center', color='#111111')
    ax.text(50.0, 67.2, 'EXACT TO-SCALE ENGINEERING DESIGN & GENERAL ARRANGEMENT DRAWING (ASME SEC VIII DIV 1 / TEMA R)',
            fontsize=9.2, ha='center', va='center', color='#444444')
    ax.plot([15.0, 85.0], [66.3, 66.3], color='#2980b9', lw=1.2)

    # -------------------------------------------------------------------------
    # TITLE BLOCK (Lower Right)
    # -------------------------------------------------------------------------
    tb_x0, tb_y0, tb_w, tb_h = 57.0, 2.5, 41.0, 14.5
    ax.add_patch(patches.Rectangle((tb_x0, tb_y0), tb_w, tb_h, fill=True, facecolor='#ffffff', edgecolor='#111111', lw=1.5))
    ax.plot([tb_x0, tb_x0 + tb_w], [tb_y0 + 9.5, tb_y0 + 9.5], color='#111111', lw=1.2)
    ax.plot([tb_x0, tb_x0 + tb_w], [tb_y0 + 4.8, tb_y0 + 4.8], color='#111111', lw=1.0)
    ax.plot([tb_x0 + 20.5, tb_x0 + 20.5], [tb_y0, tb_y0 + 9.5], color='#111111', lw=1.0)
    ax.plot([tb_x0 + 31.0, tb_x0 + 31.0], [tb_y0, tb_y0 + 4.8], color='#111111', lw=1.0)

    ax.text(tb_x0 + 20.5, tb_y0 + 12.0, 'DEPARTMENT OF CHEMICAL ENGINEERING\nPROCESS EQUIPMENT DESIGN & CAD FACILITY',
            fontsize=9.2, fontweight='bold', ha='center', va='center', color='#111111')
    ax.text(tb_x0 + 20.5, tb_y0 + 7.2, 'ETHYLENE OXIDE PACKED-BED TUBULAR REACTOR (R-201)\nGENERAL ARRANGEMENT, HYDRAULIC SIZING & DETAIL',
            fontsize=8.8, fontweight='bold', ha='center', va='center', color='#0a3d62')

    ax.text(tb_x0 + 1.2, tb_y0 + 3.2, 'PROJECT: CRE-II / PROBLEM R2', fontsize=7.8, fontweight='bold')
    ax.text(tb_x0 + 1.2, tb_y0 + 1.4, f'DESIGN: 1000 TUBES, 1.5" SCH 80', fontsize=7.2)
    ax.text(tb_x0 + 21.5, tb_y0 + 3.2, 'SCALE: 1:35 (ELEVATION)', fontsize=7.8, fontweight='bold')
    ax.text(tb_x0 + 21.5, tb_y0 + 1.4, 'UNITS: US CUST. & SI', fontsize=7.2)
    ax.text(tb_x0 + 31.8, tb_y0 + 3.2, 'DWG NO: R2-CAD-01', fontsize=7.8, fontweight='bold')
    ax.text(tb_x0 + 31.8, tb_y0 + 1.4, 'STATUS: FINAL / VERIFIED', fontsize=7.2, color='#27ae60', fontweight='bold')

    # -------------------------------------------------------------------------
    # BILL OF MATERIALS (BOM) & SPECIFICATION TABLE (Top Right)
    # -------------------------------------------------------------------------
    bom_x0, bom_y0, bom_w, bom_h = 57.0, 18.0, 41.0, 47.0
    ax.add_patch(patches.Rectangle((bom_x0, bom_y0), bom_w, bom_h, fill=True, facecolor='#f8f9fa', edgecolor='#111111', lw=1.2))
    ax.text(bom_x0 + bom_w / 2.0, bom_y0 + bom_h - 1.6, 'EQUIPMENT DATA SHEET & DESIGN PARAMETERS',
            fontsize=9.8, fontweight='bold', ha='center', va='center', color='#111111')
    ax.plot([bom_x0, bom_x0 + bom_w], [bom_y0 + bom_h - 3.0, bom_y0 + bom_h - 3.0], color='#111111', lw=1.2)

    specs = [
        ("Tag Number / Service", "R-201 / Ethylene Oxidation Reactor"),
        ("Reaction", "C2H4 + 0.5 O2 -> C2H4O (Vapor phase)"),
        ("Catalyst Type & Size", "Silver on Alumina, 0.5 in (12.7 mm) Spheres"),
        ("Catalyst Solid Density", f"{res['rho_c']:.1f} lb/ft3 (2,243 kg/m3)"),
        ("Bed Void Fraction (phi)", f"{res['phi']:.2f} (Bulk Density = {res['rho_b']:.1f} lb/ft3)"),
        ("Total Catalyst Weight (W)", f"{res['W_final']:.1f} lb ({res['W_final']/2.20462:.1f} kg)"),
        ("Ethylene Feed Rate (FA0)", f"{res['FA0_s']:.2f} lbmol/s = {res['FA0_h']:.1f} lbmol/h"),
        ("Total Feed Rate (FT0)", f"{res['FA0_s']*(1+res['theta_B']+res['theta_I']):.3f} lbmol/s (Air feed)"),
        ("Operating Temperature", f"{res['T_C']:.1f} deg C (500 deg F / 960 R, Isothermal)"),
        ("Inlet Total Pressure (P0)", f"{res['P0_atm']:.1f} atm (367.4 psia / 2.53 MPa)"),
        ("Exit Total Pressure (P_exit)", f"{res['P_exit_atm']:.2f} atm (308.6 psia / 2.13 MPa)"),
        ("Total Pressure Drop (deltaP)", f"{res['deltaP_atm']:.2f} atm ({res['deltaP_psia']:.2f} psi, {res['deltaP_atm']/res['P0_atm']*100:.1f}%)"),
        ("Target Conversion (X)", f"{res['X_final']*100:.1f} % (Exit v/v0 = {res['v_ratio_final']:.4f})"),
        ("Tube Count & Specification", f"{res['Nt']:d} Tubes, 1.5 in Schedule 80"),
        ("Tube Outside Diameter (OD)", f'{res["OD_in"]:.3f} in (48.26 mm)'),
        ("Tube Inside Diameter (ID)", f'{res["ID_in"]:.3f} in (38.10 mm)'),
        ("Tube Wall Thickness (tw)", f'{res["t_w_in"]:.3f} in (5.08 mm)'),
        ("Packed Tube Length (L)", f"{res['L_tube_final']:.2f} ft ({res['L_tube_final']*0.3048:.2f} m)"),
        ("Catalyst Weight per Tube", f"{res['W_final']/res['Nt']:.3f} lb cat/tube"),
        ("Tube Pitch & Layout", '2.375 in (60.3 mm), 30 deg Triangular'),
        ("Shell Inside Diameter (IDs)", '84.0 in (2.134 m) ID Shell'),
        ("Shell Design Pressure", '400 psig (2.76 MPa) / ASME Sec VIII Div 1'),
        ("Shell Material of Constr.", 'SA-516 Gr 70 Carbon Steel, 1.0 in Thk'),
        ("Tube Material of Constr.", 'SA-214 Carbon Steel / SA-249 TP304'),
        ("Shell Cooling Medium", 'Boiling Water / Dowtherm A Jacket at 260 C')
    ]

    y_cur = bom_y0 + bom_h - 4.5
    row_h = (bom_h - 5.0) / len(specs)
    for i, (k, v) in enumerate(specs):
        bg_col = '#ffffff' if i % 2 == 0 else '#f1f2f6'
        ax.add_patch(patches.Rectangle((bom_x0 + 0.4, y_cur - row_h + 0.2), bom_w - 0.8, row_h,
                                      fill=True, facecolor=bg_col, edgecolor='none'))
        ax.text(bom_x0 + 1.0, y_cur - row_h / 2.0 + 0.2, k, fontsize=7.2, fontweight='bold', va='center', color='#2c3e50')
        ax.text(bom_x0 + bom_w - 1.0, y_cur - row_h / 2.0 + 0.2, v, fontsize=7.2, ha='right', va='center', color='#111111')
        ax.plot([bom_x0 + 0.4, bom_x0 + bom_w - 0.4], [y_cur - row_h + 0.2, y_cur - row_h + 0.2], color='#e2e8f0', lw=0.4)
        y_cur -= row_h

    # -------------------------------------------------------------------------
    # MAIN REACTOR ELEVATION SECTION (Left Side, To-Scale)
    # -------------------------------------------------------------------------
    rx0 = 16.5   # Centerline x
    ry0 = 16.5   # Bottom tubesheet y
    rw = 12.0    # Shell diameter
    rh = 36.0    # Tube bundle length
    r_r = rw / 2.0

    # Centerline
    ax.plot([rx0, rx0], [ry0 - 11.5, ry0 + rh + 11.5], color='#e74c3c', lw=0.8, ls='dashdot')

    # Reactor Shell Body
    ax.add_patch(patches.Rectangle((rx0 - r_r, ry0), rw, rh, fill=False, edgecolor='#111111', lw=2.0))

    # Cooling Jacket / Baffle Shell surrounding tube bundle
    baffle_w = rw + 1.8
    ax.add_patch(patches.Rectangle((rx0 - baffle_w / 2.0, ry0 + 1.0), baffle_w, rh - 2.0, fill=False,
                                  edgecolor='#2980b9', lw=1.3, ls='--'))

    # Top & Bottom Tubesheets
    ts_h = 1.1
    ax.add_patch(patches.Rectangle((rx0 - r_r - 1.0, ry0 + rh), rw + 2.0, ts_h, fill=True, facecolor='#bdc3c7', edgecolor='#111111', lw=1.5))
    ax.add_patch(patches.Rectangle((rx0 - r_r - 1.0, ry0 - ts_h), rw + 2.0, ts_h, fill=True, facecolor='#bdc3c7', edgecolor='#111111', lw=1.5))
    ax.text(rx0 + r_r + 1.8, ry0 + rh + ts_h / 2.0, 'Top Tubesheet (SA-516 Gr 70)', fontsize=7.2, va='center', color='#2c3e50')
    ax.text(rx0 - r_r - 1.8, ry0 - ts_h / 2.0, 'Bottom Tubesheet & Screen', fontsize=7.2, va='center', ha='right', color='#2c3e50')

    # Top Head (Ellipsoidal 2:1)
    top_head_h = 4.8
    th_path = [
        (MPath.MOVETO, (rx0 - r_r, ry0 + rh + ts_h)),
        (MPath.CURVE4, (rx0 - r_r, ry0 + rh + ts_h + top_head_h * 0.8)),
        (MPath.CURVE4, (rx0 + r_r, ry0 + rh + ts_h + top_head_h * 0.8)),
        (MPath.CURVE4, (rx0 + r_r, ry0 + rh + ts_h))
    ]
    codes, verts = zip(*th_path)
    th_patch = patches.PathPatch(MPath(verts, codes), fill=True, facecolor='#ecf0f1', edgecolor='#111111', lw=1.8)
    ax.add_patch(th_patch)

    # Bottom Head (Ellipsoidal 2:1)
    bh_path = [
        (MPath.MOVETO, (rx0 - r_r, ry0 - ts_h)),
        (MPath.CURVE4, (rx0 - r_r, ry0 - ts_h - top_head_h * 0.8)),
        (MPath.CURVE4, (rx0 + r_r, ry0 - ts_h - top_head_h * 0.8)),
        (MPath.CURVE4, (rx0 + r_r, ry0 - ts_h))
    ]
    codes, verts = zip(*bh_path)
    bh_patch = patches.PathPatch(MPath(verts, codes), fill=True, facecolor='#ecf0f1', edgecolor='#111111', lw=1.8)
    ax.add_patch(bh_patch)

    # Inlet Gas Nozzle (N1) - Ethylene + Air Feed
    noz_w, noz_h = 2.2, 3.2
    ax.add_patch(patches.Rectangle((rx0 - noz_w / 2.0, ry0 + rh + ts_h + top_head_h * 0.75), noz_w, noz_h, fill=True, facecolor='#ecf0f1', edgecolor='#111111', lw=1.5))
    ax.add_patch(patches.Rectangle((rx0 - noz_w * 0.8, ry0 + rh + ts_h + top_head_h * 0.75 + noz_h), noz_w * 1.6, 0.5, fill=True, facecolor='#95a5a6', edgecolor='#111111', lw=1.2))
    ax.annotate('N1: REACTANT FEED INLET\n14" CL300 ANSI Flange\nC2H4 + Air @ 25 atm, 260 deg C',
                xy=(rx0, ry0 + rh + ts_h + top_head_h * 0.75 + noz_h + 0.5), xytext=(rx0 - 8.5, ry0 + rh + 9.5),
                arrowprops=dict(facecolor='#111111', arrowstyle='->', lw=1.0),
                fontsize=7.2, fontweight='bold', color='#111111', ha='center')

    # Outlet Gas Nozzle (N2) - Ethylene Oxide + Unreacted Gas
    ax.add_patch(patches.Rectangle((rx0 - noz_w / 2.0, ry0 - ts_h - top_head_h * 0.75 - noz_h), noz_w, noz_h, fill=True, facecolor='#ecf0f1', edgecolor='#111111', lw=1.5))
    ax.add_patch(patches.Rectangle((rx0 - noz_w * 0.8, ry0 - ts_h - top_head_h * 0.75 - noz_h - 0.5), noz_w * 1.6, 0.5, fill=True, facecolor='#95a5a6', edgecolor='#111111', lw=1.2))
    ax.annotate('N2: REACTOR PRODUCT OUTLET\n14" CL300 ANSI Flange\nC2H4O + Inerts @ 21 atm (X = 0.40)',
                xy=(rx0, ry0 - ts_h - top_head_h * 0.75 - noz_h - 0.5), xytext=(rx0 - 5.5, 4.8),
                arrowprops=dict(facecolor='#111111', arrowstyle='->', lw=1.0),
                fontsize=7.2, fontweight='bold', color='#111111', ha='right', va='center')

    # Coolant Inlet & Outlet Nozzles on Shell (N3 & N4)
    c_noz_w, c_noz_h = 1.8, 1.6
    # Coolant Inlet at Bottom Shell
    ax.add_patch(patches.Rectangle((rx0 + r_r + 0.9, ry0 + 3.0), c_noz_w, c_noz_h, fill=True, facecolor='#95a5a6', edgecolor='#111111', lw=1.2))
    ax.annotate('N3: COOLANT INLET\n10" CL300 (BFW/Dowtherm)\nIsothermal @ 260 deg C',
                xy=(rx0 + r_r + 0.9 + c_noz_w, ry0 + 3.0 + c_noz_h / 2.0), xytext=(rx0 + r_r + 3.2, ry0 + 3.8),
                arrowprops=dict(facecolor='#2980b9', arrowstyle='->', lw=1.0),
                fontsize=6.8, fontweight='bold', color='#2980b9', ha='left', va='center')

    # Coolant Outlet at Top Shell
    ax.add_patch(patches.Rectangle((rx0 + r_r + 0.9, ry0 + rh - 4.5), c_noz_w, c_noz_h, fill=True, facecolor='#95a5a6', edgecolor='#111111', lw=1.2))
    ax.annotate('N4: COOLANT OUTLET\n12" CL300 (Steam/Vapor)\nTo Steam Drum',
                xy=(rx0 + r_r + 0.9 + c_noz_w, ry0 + rh - 4.5 + c_noz_h / 2.0), xytext=(rx0 + r_r + 3.5, ry0 + rh - 6.5),
                arrowprops=dict(facecolor='#2980b9', arrowstyle='->', lw=1.0),
                fontsize=6.8, fontweight='bold', color='#2980b9', ha='left', va='top')

    # Representative Tubes & Catalyst Pellets inside the Shell
    n_disp_tubes = 13
    tube_xs = np.linspace(rx0 - r_r + 0.9, rx0 + r_r - 0.9, n_disp_tubes)
    t_dia_dwg = 0.50

    for tx in tube_xs:
        ax.plot([tx - t_dia_dwg / 2.0, tx - t_dia_dwg / 2.0], [ry0, ry0 + rh], color='#7f8c8d', lw=0.9)
        ax.plot([tx + t_dia_dwg / 2.0, tx + t_dia_dwg / 2.0], [ry0, ry0 + rh], color='#7f8c8d', lw=0.9)
        ax.add_patch(patches.Rectangle((tx - t_dia_dwg / 2.0, ry0), t_dia_dwg, rh, fill=True,
                                      facecolor='#f5cd79', edgecolor='none', alpha=0.55))
        for py_s in np.linspace(ry0 + 1.5, ry0 + rh - 1.5, 13):
            ax.add_patch(patches.Circle((tx, py_s), 0.14, facecolor='#e67e22', edgecolor='#d35400', lw=0.35))

    # Internal Baffles (Segmental Coolant Baffles)
    baffle_cuts = [ry0 + 6.5, ry0 + 13.5, ry0 + 20.5, ry0 + 27.5]
    for i, by in enumerate(baffle_cuts):
        if i % 2 == 0:
            ax.plot([rx0 - r_r, rx0 + r_r - 2.8], [by, by], color='#2980b9', lw=1.5)
        else:
            ax.plot([rx0 - r_r + 2.8, rx0 + r_r], [by, by], color='#2980b9', lw=1.5)

    # Catalyst Retaining Grid (Top) and Support Screen (Bottom)
    ax.plot([rx0 - r_r, rx0 + r_r], [ry0 + rh - 0.35, ry0 + rh - 0.35], color='#2c3e50', lw=1.8, ls=':')
    ax.plot([rx0 - r_r, rx0 + r_r], [ry0 + 0.35, ry0 + 0.35], color='#2c3e50', lw=1.8, ls=':')

    # Reactor Skirt Support & Foundation
    skirt_h = 6.5
    ax.plot([rx0 - r_r, rx0 - r_r - 0.7], [ry0 - ts_h, ry0 - ts_h - skirt_h], color='#111111', lw=1.8)
    ax.plot([rx0 + r_r, rx0 + r_r + 0.7], [ry0 - ts_h, ry0 - ts_h - skirt_h], color='#111111', lw=1.8)
    ax.add_patch(patches.Rectangle((rx0 - r_r - 1.8, ry0 - ts_h - skirt_h - 0.8), (rw + 3.6), 0.8,
                                  fill=True, facecolor='#7f8c8d', edgecolor='#111111', lw=1.4))
    ax.text(rx0 - r_r - 2.2, ry0 - ts_h - skirt_h / 2.0, 'Support Skirt &\nAnchor Base Plate',
            fontsize=6.8, ha='right', va='center')

    # Dimensions Leaders (Left Side)
    dim_x = rx0 - r_r - 4.2
    ax.annotate('', xy=(dim_x, ry0 - ts_h - top_head_h * 0.75 - noz_h - 0.5), xytext=(dim_x, ry0 + rh + ts_h + top_head_h * 0.75 + noz_h + 0.5),
                arrowprops=dict(arrowstyle='<->', color='#111111', lw=1.2))
    ax.text(dim_x - 0.8, ry0 + rh / 2.0, f'TOTAL O.A. HEIGHT = 46.5 ft (14.17 m)',
            fontsize=7.8, fontweight='bold', rotation=90, va='center', ha='center')

    dim_x2 = rx0 - r_r - 1.8
    ax.annotate('', xy=(dim_x2, ry0), xytext=(dim_x2, ry0 + rh),
                arrowprops=dict(arrowstyle='<->', color='#2980b9', lw=1.2))
    ax.text(dim_x2 - 0.6, ry0 + rh / 2.0, f'PACKED TUBE LENGTH L = {res["L_tube_final"]:.2f} ft (9.39 m)',
            fontsize=7.2, fontweight='bold', color='#2980b9', rotation=90, va='center', ha='center')

    dim_y = ry0 + rh + ts_h + 1.2
    ax.annotate('', xy=(rx0 - r_r, dim_y), xytext=(rx0 + r_r, dim_y),
                arrowprops=dict(arrowstyle='<->', color='#111111', lw=1.1))
    ax.text(rx0, dim_y + 0.7, f'SHELL ID = 84.0 in (2.134 m)', fontsize=7.2, fontweight='bold', ha='center')

    # Section Callout
    ax.text(rx0, 2.5, 'SECTIONAL ELEVATION A-A\nSCALE 1:35',
            fontsize=8.5, fontweight='bold', ha='center', va='center', color='#111111')

    # -------------------------------------------------------------------------
    # DETAIL B: SINGLE TUBE & CATALYST PACKING DETAIL (Middle Right)
    # -------------------------------------------------------------------------
    dt_x0, dt_y0, dt_w, dt_h = 34.5, 36.5, 20.5, 28.5
    ax.add_patch(patches.Rectangle((dt_x0, dt_y0), dt_w, dt_h, fill=True, facecolor='#ffffff', edgecolor='#111111', lw=1.2))
    ax.text(dt_x0 + dt_w / 2.0, dt_y0 + dt_h - 1.4, 'DETAIL B: TUBE & CATALYST PACKING',
            fontsize=8.2, fontweight='bold', ha='center', va='center', color='#0a3d62')
    ax.plot([dt_x0, dt_x0 + dt_w], [dt_y0 + dt_h - 2.6, dt_y0 + dt_h - 2.6], color='#111111', lw=1.0)

    tb_cx = dt_x0 + 5.5
    tb_cy = dt_y0 + 12.5
    tb_od = 3.8
    tb_id = 3.0
    tb_len = 20.0

    ax.add_patch(patches.Rectangle((tb_cx - tb_od / 2.0, tb_cy - tb_len / 2.0), tb_od, tb_len, fill=True, facecolor='#bdc3c7', edgecolor='#111111', lw=1.2))
    ax.add_patch(patches.Rectangle((tb_cx - tb_id / 2.0, tb_cy - tb_len / 2.0), tb_id, tb_len, fill=True, facecolor='#fff2cc', edgecolor='#7f8c8d', lw=1.0))

    np.random.seed(42)
    py = tb_cy - tb_len / 2.0 + 0.9
    while py < tb_cy + tb_len / 2.0 - 0.7:
        for px_offset in [-0.75, 0.0, 0.75]:
            p_jitter = (np.random.rand() - 0.5) * 0.12
            ax.add_patch(patches.Circle((tb_cx + px_offset + p_jitter, py), 0.40,
                                        facecolor='#e67e22', edgecolor='#b94a48', lw=0.5))
        py += 0.80

    ax.plot([tb_cx - tb_id / 2.0, tb_cx + tb_id / 2.0], [tb_cy - tb_len / 2.0 + 0.4, tb_cy - tb_len / 2.0 + 0.4], color='#111111', lw=1.8, ls=':')
    ax.plot([tb_cx - tb_id / 2.0, tb_cx + tb_id / 2.0], [tb_cy + tb_len / 2.0 - 0.4, tb_cy + tb_len / 2.0 - 0.4], color='#111111', lw=1.8, ls=':')

    ann_x = dt_x0 + 10.2
    ax.text(ann_x, tb_cy + 8.2, f'1.5" Schedule 80 Tube\nOD = {res["OD_in"]:.3f}" (48.26 mm)\nID = {res["ID_in"]:.3f}" (38.10 mm)\nWall = {res["t_w_in"]:.3f}" (5.08 mm)',
            fontsize=7.0, fontweight='bold', va='top')
    ax.text(ann_x, tb_cy + 2.0, f'Catalyst Pellets:\nDp = 0.50" (12.7 mm)\nSolid rho = {res["rho_c"]:.0f} lb/ft3\nBulk rho = {res["rho_b"]:.0f} lb/ft3\nVoid Fraction phi = 0.50',
            fontsize=7.0, va='top', color='#c0392b')
    ax.text(ann_x, tb_cy - 4.2, f'Single Tube Loading:\nCat W = {res["W_final"]/res["Nt"]:.2f} lb/tube\nLength L = {res["L_tube_final"]:.2f} ft\ndP = {res["deltaP_atm"]:.2f} atm',
            fontsize=7.0, va='top', color='#27ae60')

    ax.annotate('', xy=(tb_cx - tb_od / 2.0, tb_cy + tb_len / 2.0 + 0.8), xytext=(tb_cx + tb_od / 2.0, tb_cy + tb_len / 2.0 + 0.8),
                arrowprops=dict(arrowstyle='<->', color='#111111', lw=1.0))
    ax.text(tb_cx, tb_cy + tb_len / 2.0 + 1.5, f'OD 1.90"', fontsize=6.8, ha='center')

    ax.annotate('', xy=(tb_cx - tb_id / 2.0, tb_cy + tb_len / 2.0 + 0.2), xytext=(tb_cx + tb_id / 2.0, tb_cy + tb_len / 2.0 + 0.2),
                arrowprops=dict(arrowstyle='<->', color='#2980b9', lw=1.0))
    ax.text(tb_cx, tb_cy + tb_len / 2.0 - 1.1, f'ID 1.50"', fontsize=6.5, ha='center', color='#2980b9')

    # -------------------------------------------------------------------------
    # DETAIL C: TUBE SHEET LAYOUT (Cross Section Plan View) (Lower Middle)
    # -------------------------------------------------------------------------
    ts_x0, ts_y0, ts_w, ts_h_box = 34.5, 18.0, 20.5, 17.0
    ax.add_patch(patches.Rectangle((ts_x0, ts_y0), ts_w, ts_h_box, fill=True, facecolor='#ffffff', edgecolor='#111111', lw=1.2))
    ax.text(ts_x0 + ts_w / 2.0, ts_y0 + ts_h_box - 1.3, 'DETAIL C: TUBESHEET LAYOUT (1000 TUBES)',
            fontsize=8.2, fontweight='bold', ha='center', va='center', color='#0a3d62')
    ax.plot([ts_x0, ts_x0 + ts_w], [ts_y0 + ts_h_box - 2.4, ts_y0 + ts_h_box - 2.4], color='#111111', lw=1.0)

    tsc_x = ts_x0 + 6.5
    tsc_y = ts_y0 + 6.8
    tsc_r = 5.2
    ax.add_patch(patches.Circle((tsc_x, tsc_y), tsc_r, fill=True, facecolor='#ecf0f1', edgecolor='#111111', lw=1.4))
    ax.add_patch(patches.Circle((tsc_x, tsc_y), tsc_r - 0.5, fill=False, edgecolor='#7f8c8d', lw=0.7, ls='--'))

    grid_r = tsc_r - 0.8
    for rx in np.linspace(-grid_r, grid_r, 10):
        for ry_offset in np.linspace(-grid_r, grid_r, 10):
            if rx**2 + ry_offset**2 <= (grid_r - 0.2)**2:
                ax.add_patch(patches.Circle((tsc_x + rx, tsc_y + ry_offset), 0.18,
                                            facecolor='#34495e', edgecolor='none'))

    ax.text(ts_x0 + 13.2, ts_y0 + 10.5, f'Pattern: 30 deg Tri.\nPitch Pt = 2.375"\n(Pt / Do = 1.25)\n\nNt = 1,000 Tubes\nShell ID = 84.0"\nThk = 1.00" SA-516',
            fontsize=6.8, va='top', color='#2c3e50')

    plt.tight_layout()
    plt.savefig(out_png, dpi=300)
    plt.savefig(out_pdf)
    plt.close()
    print(f"[SUCCESS] Scale CAD drawing saved: {out_png}")
    print(f"[SUCCESS] Scale CAD drawing saved: {out_pdf}")

def main():
    parser = argparse.ArgumentParser(description="Ethylene Oxide Reactor Sizing Suite")
    parser.add_argument("--conversion", type=float, default=0.40, help="Target ethylene conversion (default: 0.40)")
    parser.add_argument("--P0", type=float, default=25.0, help="Inlet pressure in atm (default: 25.0)")
    parser.add_argument("--T", type=float, default=260.0, help="Operating temperature in C (default: 260.0)")
    parser.add_argument("--FA0", type=float, default=0.9, help="Ethylene feed rate in lbmol/s (default: 0.9)")
    parser.add_argument("--Nt", type=int, default=1000, help="Number of tubes in parallel (default: 1000)")
    parser.add_argument("--schedule", type=int, default=80, help="Pipe schedule (default: 80)")
    parser.add_argument("--nominal_dia", type=float, default=1.5, help="Nominal pipe diameter in inches (default: 1.5)")
    args = parser.parse_args()

    # Solve reactor
    res = solve_reactor(
        P0_atm=args.P0,
        T_C=args.T,
        FA0_s=args.FA0,
        X_target=args.conversion,
        Nt=args.Nt,
        schedule=args.schedule,
        nom_dia_in=args.nominal_dia
    )

    # Print comprehensive report to console
    print_solution_report(res)

    # Output file paths
    dirs = [
        r"d:\GAMES\zercxes\CAD_Engineering_Drawings",
        r"D:\Downloads\pedd",
        r"D:\user\SOURISH SENAPATI\Downloads\pedd",
        r"C:\Users\SOURISH SENAPATI\.gemini\antigravity\brain\ccfd5b92-7eb1-499b-94b8-0f0185a2992f"
    ]

    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # Generate plots in local directory first
    p_png = os.path.join(dirs[0], "07_Ethylene_Oxide_Reactor_Performance_Curves.png")
    p_pdf = os.path.join(dirs[0], "07_Ethylene_Oxide_Reactor_Performance_Curves.pdf")
    cad_png = os.path.join(dirs[0], "08_Ethylene_Oxide_Reactor_Scale_CAD_Drawing.png")
    cad_pdf = os.path.join(dirs[0], "08_Ethylene_Oxide_Reactor_Scale_CAD_Drawing.pdf")

    generate_performance_plots(res, p_png, p_pdf)
    generate_scale_cad_drawing(res, cad_png, cad_pdf)

    # Copy files to destination directories
    import shutil
    for d in dirs[1:]:
        for fname in [
            "07_Ethylene_Oxide_Reactor_Performance_Curves.png",
            "07_Ethylene_Oxide_Reactor_Performance_Curves.pdf",
            "08_Ethylene_Oxide_Reactor_Scale_CAD_Drawing.png",
            "08_Ethylene_Oxide_Reactor_Scale_CAD_Drawing.pdf"
        ]:
            src = os.path.join(dirs[0], fname)
            dst = os.path.join(d, fname)
            shutil.copy2(src, dst)
            print(f"[DEPLOYED] Copied {fname} -> {d}")

if __name__ == "__main__":
    main()
