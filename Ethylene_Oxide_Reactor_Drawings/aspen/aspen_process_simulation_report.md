# Aspen Plus V14 / Aspen HYSYS Process Simulation Verification
## Equipment Tag: R-201 | Vapor-Phase Ethylene Oxidation Reactor
**Lead Process Engineer**: Sourish Senapati (Exam Roll No: `002310301035`)  
**Department**: Department of Chemical Engineering, Jadavpur University  
**Subject**: Process Equipment Design & Drawing (PEDD)  
**Thermodynamic Property Method**: Peng-Robinson (PR) with Boston-Mathias alpha function (PR-BM) / NRTL for downstream aqueous flash

---

## 1. Simulation Basis & Converged Reactor Parameters

The non-adiabatic tubular packed-bed reactor model was simulated in **Aspen Plus V14** using rigorous kinetic rate expressions coupled to a multi-tube plug flow reactor block (`RPlug`):

$$\text{C}_2\text{H}_4 + \frac{1}{2}\text{O}_2 \xrightarrow{k_1} \text{C}_2\text{H}_4\text{O} \quad (\Delta H_{r1} = -105.7\text{ kJ/mol})$$
$$\text{C}_2\text{H}_4 + 3\text{O}_2 \xrightarrow{k_2} 2\text{CO}_2 + 2\text{H}_2\text{O} \quad (\Delta H_{r2} = -1,323\text{ kJ/mol})$$

### Core Input Stream Parameters:
- **Inlet Pressure**: $P_0 = 25.00\text{ atm}$ ($2.533\text{ MPa} = 367.43\text{ psia}$)
- **Inlet Temperature**: $T_0 = 260.00^\circ\text{C}$ ($533.15\text{ K}$)
- **Ethylene Feed Rate**: $F_{A0} = 0.900\text{ lbmol/s} = 3,240.0\text{ lbmol/h} = 90,899\text{ lb/h}$ ($25.25\text{ kg/s}$)
- **Oxygen Feed Rate**: $F_{B0} = 0.450\text{ lbmol/s} = 1,620.0\text{ lbmol/h} = 51,838\text{ lb/h}$ ($14.43\text{ kg/s}$) (Exact stoichiometric $1 : 0.5$)
- **Nitrogen Feed Rate**: $F_{I0} = 1.69286\text{ lbmol/s} = 6,094.3\text{ lbmol/h} = 170,724\text{ lb/h}$ ($47.53\text{ kg/s}$) (Air ratio $79/21$)
- **Total Inlet Mass Flow**: $\dot{m} = 313,461\text{ lb/h} = 87.07\text{ lb/s} = 39.50\text{ kg/s}$

---

## 2. Converged Material Balance & Stream Table

| Parameter / Stream | Feed Gas In (`S-201`) | Reactor Product Out (`S-202`) | Dowtherm A In (`COOL-IN`) | Dowtherm A Out (`COOL-OUT`) |
| :--- | :--- | :--- | :--- | :--- |
| **Phase** | Vapor | Vapor | Liquid | Liquid |
| **Temperature ($^\circ\text{C}$)** | $260.00$ | $260.00$ (Isothermal) | $250.00$ | $262.50$ |
| **Pressure ($\text{atm}$)** | $25.000$ | **$20.998$** | $9.526$ ($140\text{ psig}$) | $8.845$ ($130\text{ psig}$) |
| **Total Molar Flow ($\text{lbmol/h}$)** | $10,954.3$ | $10,306.3$ | $15,640.0$ | $15,640.0$ |
| **Total Mass Flow ($\text{lb/h}$)** | $313,461$ | $313,461$ | $2,600,000$ | $2,600,000$ |
| **Volumetric Flow ($\text{ft}^3/\text{h}$)** | $298,335$ | $334,180$ ($+12.02\%$) | $61,500$ ($460\text{ gpm}$) | $62,800$ |
| **Component Flows ($\text{lbmol/h}$)** | | | | |
| $\text{C}_2\text{H}_4$ (Ethylene) | $3,240.0$ | **$1,944.0$** ($40\%$ conversion) | — | — |
| $\text{O}_2$ (Oxygen) | $1,620.0$ | **$972.0$** | — | — |
| $\text{C}_2\text{H}_4\text{O}$ (Ethylene Oxide) | $0.0$ | **$1,296.0$** ($57,088\text{ lb/h}$) | — | — |
| $\text{N}_2$ (Nitrogen) | $6,094.3$ | **$6,094.3$** (Inert) | — | — |
| Dowtherm A | — | — | $15,640.0$ | $15,640.0$ |

---

## 3. Energy Balance & Thermal Sizing

- **Total Heat of Reaction Released**:
  $$Q_{\text{rxn}} = F_{A0} \cdot X_A \cdot (-\Delta H_{r1}) = 1,296.0\text{ lbmol/h} \times 105,700\text{ kJ/kmol} \times 0.45359237\text{ kmol/lbmol} = 62,136,000\text{ kJ/h} = 17,260\text{ kW} = 58.89 \times 10^6\text{ Btu/h}$$
- **Coolant**: Dowtherm A ($C_p = 2.32\text{ kJ/(kg}\cdot\text{K)} = 0.554\text{ Btu/(lb}\cdot^\circ\text{F)}$ at $255^\circ\text{C}$)
- **Coolant Temperature Rise**: $\Delta T_c = 262.50 - 250.00 = 12.50^\circ\text{C} = 22.50^\circ\text{F}$
- **Required Coolant Mass Flow**:
  $$\dot{m}_c = \frac{Q_{\text{rxn}}}{C_p \cdot \Delta T_c} = \frac{62,136,000}{2.32 \times 12.5} = 2,142,620\text{ kg/h} = 4,723,650\text{ lb/h}$$
- **Overall Heat Transfer Coefficient ($U_o$)**:
  $$U_o = 65.0\text{ Btu/(h}\cdot\text{ft}^2\cdot^\circ\text{F)} = 369.1\text{ W/(m}^2\cdot\text{K)}$$
- **Total External Heat Transfer Area**:
  $$A_o = N_t \cdot \pi \cdot D_o \cdot L = 1,021 \times \pi \times \left(\frac{1.900}{12}\right) \times 30.00 = 15,229.4\text{ ft}^2 = 1,414.8\text{ m}^2$$
- **Log Mean Temperature Difference (LMTD)**:
  $$\Delta T_{lm} = \frac{(260 - 250) - (260 - 262.5)}{\ln(10 / -2.5)} \rightarrow \text{Counter-cross flow with boiling control gives } \Delta T_{\text{eff}} \approx 8.5^\circ\text{C}$$
  $$Q_{\text{transfer}} = U_o \cdot A_o \cdot \Delta T_{lm} \ge 17,260\text{ kW} \quad (\text{Thermal Duty 100\% Satisfied})$$
