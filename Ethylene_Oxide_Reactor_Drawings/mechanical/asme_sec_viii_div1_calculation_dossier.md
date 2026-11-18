# ASME Section VIII Division 1 & TEMA Class R Mechanical Design Dossier
## Equipment Tag: R-201 | Ethylene Oxide Packed-Bed Tubular Reactor
**Lead Process & Mechanical Engineer**: Sourish Senapati (Exam Roll No: `002310301035`)  
**Department**: Department of Chemical Engineering, Jadavpur University  
**Subject**: Process Equipment Design & Drawing (PEDD)  
**Applicable Codes**: ASME BPVC Section VIII Division 1 (2023 Edition), TEMA Class R (10th Edition), ASME B16.5 (2020), IS 800 (2007)

---

## 1. Design Conditions & Material Specifications

| Parameter | Shell Side (Coolant - Dowtherm A) | Tube Side (Process Gas - $\text{C}_2\text{H}_4 + \text{Air}$) |
| :--- | :--- | :--- |
| **Operating Pressure** | $140\text{ psig}$ ($9.53\text{ barg} = 0.965\text{ MPa}$) | $352.7\text{ psig}$ ($24.00\text{ barg} = 2.432\text{ MPa}$) |
| **Design Pressure ($P$)** | **$200\text{ psig}$** ($1.379\text{ MPa}$) | **$450\text{ psig}$** ($3.103\text{ MPa}$) |
| **Operating Temperature** | $255^\circ\text{C}$ ($491^\circ\text{F}$) | $260^\circ\text{C}$ ($500^\circ\text{F}$) |
| **Design Temperature** | **$290^\circ\text{C}$** ($554^\circ\text{F}$) | **$290^\circ\text{C}$** ($554^\circ\text{F}$) |
| **Material of Construction** | SA-516 Gr 70 Normalized Carbon Steel | SA-213 TP304 Stainless Steel (Seamless) |
| **Allowable Stress ($S$)** | $20,000\text{ psi}$ ($137.9\text{ MPa}$) | $15,600\text{ psi}$ ($107.6\text{ MPa}$) |
| **Joint Efficiency ($E$)** | $1.00$ (Full Radiographic Examination per UW-11(a)) | $1.00$ (Seamless Tubes) |
| **Corrosion Allowance ($C_A$)**| $0.125\text{ in}$ ($3.175\text{ mm}$) | $0.000\text{ in}$ ($0.0\text{ mm}$, Stainless) |

---

## 2. Cylindrical Pressure Shell Thickness (ASME UG-27)

Per ASME Section VIII Division 1, paragraph UG-27(c)(1), the minimum required thickness under internal pressure is:

$$t_{\text{req}} = \frac{P \cdot R_i}{S \cdot E - 0.6 \cdot P} + C_A$$

Where:
- $P = 450\text{ psig}$
- Inside Radius $R_i = D_s / 2 = 84.0 / 2 = 42.0\text{ in}$
- $S = 20,000\text{ psi}$
- $E = 1.00$
- $C_A = 0.125\text{ in}$

$$\text{Denominator} = 20,000 \times 1.00 - 0.6 \times 450 = 20,000 - 270 = 19,730\text{ psi}$$

$$t_{\text{pressure}} = \frac{450 \times 42.0}{19,730} = \frac{18,900}{19,730} = 0.9579\text{ in}$$

$$t_{\text{req}} = 0.9579 + 0.1250 = 1.0829\text{ in}$$

**Selected Nominal Shell Plate Thickness**:
$$t_s = 1.125\text{ in} = 1\frac{1}{8}\text{ in} = 28.575\text{ mm}$$

Maximum Allowable Working Pressure (MAWP) in corroded state:
$$\text{MAWP} = \frac{S \cdot E \cdot (t_s - C_A)}{R_i + 0.6(t_s - C_A)} = \frac{20,000 \times 1.0 \times 1.000}{42.0 + 0.6} = \frac{20,000}{42.6} = 469.48\text{ psig} > 450\text{ psig} \quad (\text{SAFE})$$

---

## 3. 2:1 Semi-Ellipsoidal Formed Heads (ASME UG-32)

Per ASME Section VIII Division 1, paragraph UG-32(d), for 2:1 ellipsoidal heads ($K = 1.0$):

$$t_h = \frac{P \cdot D_i \cdot K}{2 \cdot S \cdot E - 0.2 \cdot P} + C_A$$

Where:
- $D_i = 84.0\text{ in}$
- $K = \frac{1}{6} \left[ 2 + \left(\frac{D_i}{2h}\right)^2 \right] = 1.000$ (for $D_i / 2h = 2.0$)
- $2 \cdot S \cdot E - 0.2 \cdot P = 2 \times 20,000 \times 1.0 - 0.2 \times 450 = 40,000 - 90 = 39,910\text{ psi}$

$$t_{\text{pressure}} = \frac{450 \times 84.0 \times 1.0}{39,910} = \frac{37,800}{39,910} = 0.9471\text{ in}$$

$$t_{\text{req}} = 0.9471 + 0.1250 = 1.0721\text{ in}$$

**Selected Nominal Head Plate Thickness**:
$$t_h = 1.125\text{ in} = 1\frac{1}{8}\text{ in} = 28.575\text{ mm}$$
- Inside crown depth: $H_c = D_i / 4 = 21.0\text{ in} = 533.4\text{ mm}$
- Straight cylindrical flange: $h_{sf} = 3.00\text{ in} = 76.2\text{ mm}$

---

## 4. Fixed Tubesheet Sizing (TEMA Class R & ASME UHX)

Per TEMA Section 5, Paragraph RCB-7.13 and ASME UHX-12, the required tubesheet thickness for fixed tubesheet exchangers with shell and channel under internal pressure is:

$$t_{ts} = \frac{F \cdot G}{3} \sqrt{\frac{P_{\text{eff}}}{\eta \cdot S}} + C_A$$

Where:
- Gasket pitch diameter $G = 84.0\text{ in}$
- Factor $F = 1.0$ for fixed tubesheet
- Effective design differential pressure $P_{\text{eff}} = 450\text{ psi}$
- Ligament efficiency $\eta = \frac{P_t - D_o}{P_t} = \frac{2.375 - 1.900}{2.375} = \frac{0.475}{2.375} = 0.200$
- Tubesheet material: SA-516 Gr 70 normalized with $3/16\text{-in}$ (4.8 mm) SA-240 TP304L stainless explosive clad
- Allowable stress $S = 20,000\text{ psi}$

$$t_{\text{calc}} = \frac{1.0 \times 84.0}{3} \sqrt{\frac{450}{0.200 \times 20,000}} = 28.0 \times \sqrt{\frac{450}{4000}} = 28.0 \times \sqrt{0.1125} = 28.0 \times 0.3354 = 9.39\text{ cm} = 3.69\text{ in}$$

**Selected Nominal Tubesheet Thickness**:
$$t_{ts} = 3.75\text{ in} = 95.25\text{ mm} \quad (\text{Comprising } 3.5625\text{ in base SA-516 Gr 70} + 0.1875\text{ in 304L clad})$$

---

## 5. Catalyst Tubes & Hydraulic Sizing Verification

- Tube specification: $1.5\text{-in}$ Nominal Schedule 80 Seamless (SA-213 TP304)
- Outside Diameter: $D_o = 1.900\text{ in} = 0.15833\text{ ft} = 48.26\text{ mm}$
- Inside Diameter: $D_i = 1.500\text{ in} = 0.12500\text{ ft} = 38.10\text{ mm}$
- Wall Thickness: $t_w = 0.200\text{ in} = 5.08\text{ mm}$
- Cross-sectional flow area per tube:
  $$A_{c1} = \frac{\pi}{4} D_i^2 = \frac{\pi}{4} (0.125)^2 = 0.012272\text{ ft}^2 = 1.767\text{ in}^2$$
- Total tubes: $N_t = 1,021\text{ tubes}$
- Total flow area:
  $$A_{c,\text{tot}} = 1,021 \times 0.012272 = 12.5296\text{ ft}^2 = 1.164\text{ m}^2$$
- Total mass flow rate of gas:
  $$\dot{m} = F_{T0} \cdot M_{\text{air}} = (0.90 \times 3.440476\text{ lbmol/s}) \times 28.97\text{ lb/lbmol} = 89.702\text{ lb/s} = 322,927\text{ lb/h}$$
- Mass velocity:
  $$G = \frac{\dot{m}}{A_{c,\text{tot}}} = \frac{89.702}{12.5296} = 7.159\text{ lb/(ft}^2\cdot\text{s)} = 34.95\text{ kg/(m}^2\cdot\text{s)}$$
- Superficial velocity at reactor inlet ($T = 260^\circ\text{C}$, $P = 25\text{ atm}$, $\rho_0 = 1.0507\text{ lb/ft}^3$):
  $$u_0 = \frac{G}{\rho_0} = \frac{7.159}{1.0507} = 6.814\text{ ft/s} = 2.077\text{ m/s}$$
- Tube Burst Pressure Verification (ASME UG-27):
  $$P_{\text{burst}} = \frac{2 \cdot S \cdot t_w}{D_o - 0.8 \cdot t_w} = \frac{2 \times 15,600 \times 0.200}{1.900 - 0.160} = \frac{6,240}{1.740} = 3,586\text{ psig} \gg 450\text{ psig} \quad (\text{Factor of Safety } = 7.97)$$

---

## 6. Cylindrical Skirt Support & Anchor Bolt Sizing

Per ASME Section VIII Division 1 Appendix G and Bednar / Megyesy pressure vessel standards:
- Skirt Outside Diameter: $D_{sk} = 86.25\text{ in} = 2.191\text{ m}$
- Skirt Height: $H_{sk} = 96.0\text{ in} = 8.00\text{ ft} = 2.438\text{ m}$
- Total Operating Weight:
  - Vessel Shell & Heads: $28,450\text{ lb}$
  - Tubesheets (Pair): $12,600\text{ lb}$
  - 1,021 Schedule 80 Tubes: $37,800\text{ lb}$
  - Catalyst Bed: $26,469\text{ lb}$
  - Dowtherm A Coolant Holdup: $24,100\text{ lb}$
  - Insulation, Nozzles, Platforms: $10,500\text{ lb}$
  - **Total Operating Weight ($W_{\text{op}}$)**: **$139,919\text{ lb}$** ($63,466\text{ kg} = 63.47\text{ tonnes}$)
- Wind Design Pressure: $q_z = 35\text{ psf}$ ($100\text{ mph}$ basic wind speed per ASCE 7 / IS 875)
- Overturning Moment at base: $M_{\text{wind}} = 1,485,000\text{ ft-lb} = 2.013\text{ MN}\cdot\text{m}$
- Skirt thickness under combined deadweight and bending:
  $$t_{sk,\text{calc}} = \frac{W_{\text{op}}}{\pi D_{sk} S E} + \frac{4 M_{\text{wind}}}{\pi D_{sk}^2 S E} = \frac{139,919}{\pi \times 86.25 \times 15,000 \times 0.85} + \frac{4 \times 1,485,000 \times 12}{\pi \times 86.25^2 \times 15,000 \times 0.85} = 0.040 + 0.239 = 0.279\text{ in}$$
  **Selected Nominal Skirt Thickness**: $t_{sk} = 0.750\text{ in}$ ($19.05\text{ mm}$, SA-516 Gr 70) $\rightarrow$ Robust Safety Factor of $2.69$!
- **Anchor Bolts**:
  $$T_{\text{max}} = \frac{4 M_{\text{wind}}}{N_b \cdot D_{bc}} - \frac{W_{\text{min}}}{N_b}$$
  With $N_b = 24$ bolts on $D_{bc} = 94.0\text{ in}$ bolt circle:
  $$T_{\text{bolt}} = \frac{4 \times 17,820,000\text{ in-lb}}{24 \times 94.0\text{ in}} - \frac{105,000\text{ lb}}{24} = 31,595 - 4,375 = 27,220\text{ lb}$$
  Bolt tensile stress allowable (SA-193 B7): $S_b = 25,000\text{ psi}$
  $$A_b = \frac{27,220}{25,000} = 1.089\text{ in}^2 \rightarrow \text{Selected } 1\frac{1}{2}\text{-in (M36) Anchor Bolts } (A_{\text{root}} = 1.405\text{ in}^2)$$
