import numpy as np
from scipy.integrate import solve_ivp

P0_atm = 25.0
P0_psia = P0_atm * 14.6959488
P0_psf = P0_psia * 144.0
T_C = 260.0
T_R = (T_C * 9.0 / 5.0 + 32.0) + 459.67
FA0_s = 0.9
FA0_h = FA0_s * 3600.0
X_target = 0.40
k_rate = 0.0141
Dp_in = 0.5
Dp_ft = Dp_in / 12.0
rho_c = 140.0
phi = 0.5
rho_b = rho_c * (1.0 - phi)
R_eng = 10.73159
M_air = 28.97
rho0 = (P0_psia * M_air) / (R_eng * T_R)
mu_cP = 0.027
mu = mu_cP * 6.719689e-4
gc = 32.174

theta_B = 0.5
theta_I = 0.5 * (79.0 / 21.0)
theta_tot = 1.0 + theta_B + theta_I
yA0 = 1.0 / theta_tot
PA0 = yA0 * P0_atm
delta = -0.5
eps = yA0 * delta
k_eff = k_rate * (0.5**(2.0/3.0)) * PA0

FT0_s = FA0_s * theta_tot
m_dot = FT0_s * M_air

W_ideal = (FA0_h / k_eff) * ((1.0 + eps)*np.log(1.0/(1.0 - X_target)) - eps*X_target)

def run_case(nom_in, Nt):
    if nom_in == 1.5:
        ID_in = 1.500
        OD_in = 1.900
    elif nom_in == 2.0:
        ID_in = 1.939
        OD_in = 2.375
    elif nom_in == 1.0:
        ID_in = 0.957
        OD_in = 1.315
    elif nom_in == 1.25:
        ID_in = 1.278
        OD_in = 1.660

    ID_ft = ID_in / 12.0
    Ac1 = np.pi * (ID_ft**2) / 4.0
    Ac_tot = Nt * Ac1
    G = m_dot / Ac_tot
    term1 = G / (rho0 * gc * Dp_ft)
    term2 = (1.0 - phi) / (phi**3)
    term3 = (150.0 * (1.0 - phi) * mu / Dp_ft) + (1.75 * G)
    beta0 = term1 * term2 * term3
    alpha = (2.0 * beta0) / (P0_psf * rho_b * Ac_tot)

    def odes(w, Y):
        X, y = Y
        if y <= 1e-4 or X >= 0.9999:
            return [0.0, 0.0]
        dX = (k_eff / FA0_h) * y * (1.0 - X) / (1.0 + eps * X)
        dy = - (alpha / (2.0 * y)) * (1.0 + eps * X)
        return [dX, dy]

    def event_X(w, Y):
        return Y[0] - X_target
    event_X.terminal = True
    event_X.direction = 1

    sol = solve_ivp(odes, [0, 200000], [0.0, 1.0], events=event_X, max_step=10.0, rtol=1e-8, atol=1e-10)
    if sol.t_events[0].size > 0:
        W_act = sol.t_events[0][0]
        y_act = sol.y_events[0][0][1]
        X_act = sol.y_events[0][0][0]
        P_act = y_act * P0_atm
        dP = P0_atm - P_act
        L = (W_act / Nt) / (rho_b * Ac1)
        v_ratio = (1.0 + eps * X_act) / y_act
        return {
            'Nt': Nt, 'nom': nom_in, 'ID_in': ID_in, 'G': G, 'beta0': beta0,
            'alpha': alpha, 'W': W_act, 'excess_pct': (W_act - W_ideal)/W_ideal*100,
            'L': L, 'y': y_act, 'P_exit': P_act, 'dP': dP, 'dP_pct': dP/P0_atm*100,
            'v_ratio': v_ratio
        }
    else:
        return None

print(f"Ideal Catalyst Weight (zero dP): W_ideal = {W_ideal:.2f} lb cat ({W_ideal*0.45359237:.2f} kg)\n")

for nom in [1.5, 2.0, 1.0]:
    print(f"=== {nom}-in Schedule 80 Tubes ===")
    print(f"{'Nt':>5} | {'G (lb/ft2s)':>11} | {'beta0 (psi/ft)':>14} | {'alpha (1/lb)':>12} | {'W (lb cat)':>10} | {'Excess':>7} | {'L (ft)':>7} | {'P_exit':>7} | {'dP (%)':>7} | {'v/v0':>6}")
    print("-" * 105)
    for nt in [200, 300, 400, 500, 600, 700, 800, 900, 1000, 1200, 1500, 2000, 3000]:
        res = run_case(nom, nt)
        if res:
            print(f"{res['Nt']:5d} | {res['G']:11.3f} | {res['beta0']/144.0:14.4f} | {res['alpha']:12.3e} | {res['W']:10.2f} | {res['excess_pct']:6.2f}% | {res['L']:7.2f} | {res['P_exit']:6.2f}a | {res['dP_pct']:6.2f}% | {res['v_ratio']:6.3f}")
        else:
            print(f"{nt:5d} | CHOKED / P -> 0 BEFORE X = 0.40")
    print()
