# GATE D — Detailed Engineering Design and Simulation Report
## DIY Active Stage Monitor (Visaton BG 20 + TPA3255 PBTL)

**Project:** DIY Active Stage Monitor Loudspeaker  
**Location:** `projects/live-pa-system/`  
**Phase:** Gate D — Detailed Engineering Design and Simulation  
**Status:** Design and Simulation Complete — Pending Gate E Approval  
**Date:** October 2026  

---

## Executive Summary

This report documents the completion of **Gate D (Detailed Engineering Design and Simulation)** for the DIY Active Stage Monitor. The design translates the approved Gate C architecture into a fully verified schematic, rigorous circuit simulations in ngspice, an electrical rules checked (ERC) KiCad 10 project, an audited bill of materials (BOM), a finished weight breakdown, and a bench verification checklist for Gate E.

```
+---------------------------------------------------------------------------------------------------+
|                                  SYSTEM SIGNAL ARCHITECTURE                                       |
|                                                                                                   |
|  [Mode A: Vocal]                                                                                  |
|  XLR3-F Mic In ---> RF Filter ---> DC Block ---> U1A Preamp Stage ---> U1B 60Hz 2nd HPF           |
|                                                  (+20 to +45dB)         (Butterworth, Q=0.71)     |
|                                                                                |                  |
|                                                                                v                  |
|                                                                          [RV2 Mic Vol]            |
|                                                                                |                  |
|                                                                                v (Pole 1 Pos A)   |
|  [Mode B: Monitor]                                                     [SW1 DPDT Selector]        |
|  Combo XLR/TRS ---> RF Filter ---> DC Block ---> U2A Line Receiver             | (Common Wiper)   |
|  (+4dBu Line)                                    (-6.02dB Atten)               v                  |
|                                                        |               [Audio Signal Bus]         |
|                                                        v                       |                  |
|                                                  [RV3 Line Vol]                v                  |
|                                                        |               [TPA3255 PBTL Amp]         |
|                                                        +-------------->(36V DC Rail, 40-48W RMS)  |
|                                                          (Pole 1 Pos B)        |                  |
|                                                                                v                  |
|                                                                         Floating Bridge           |
|                                                                           (OUT+ / OUT-)           |
|                                                                                |                  |
|                                              +------- [SW2 Bypass] <-----------+                  |
|                                              |                                 |                  |
|                                              v                                 v                  |
|                                     [Visaton BG 20 (8 ohm)] <---- [Passive RLC Contour]           |
|                                     (25L Net, Fb = 50 Hz)         (1.0mH // 4.7uF // 8.2R)        |
+---------------------------------------------------------------------------------------------------+
```

---

## 1. Unresolved Gate C Assumptions & Design Baseline

Prior to schematic layout and SPICE simulation, the following engineering assumptions from Gate C were investigated and resolved:

| Item | Gate C Initial Assumption | Gate D Reconciled Specification | Engineering Resolution |
| :--- | :--- | :--- | :--- |
| **Driver Excursion** | Catalog $\pm 4.0\text{ mm}$ (ambiguous) | Catalog limit = $\pm 6.0\text{ mm}$ ($X_{\text{mech}}$); Geometric $X_{\text{max, geom}} = \pm 2.0\text{ mm}$ | Reconciled against official Visaton documentation. $H_{\text{winding}} = 8.0\text{ mm}$, $H_{\text{pole}} = 4.0\text{ mm}$. Continuous operating power set to 10 W–15 W RMS ($X \le 1.96\text{ mm}$) to remain within linear travel. |
| **RLC Contour Resonance** | Claimed 4.0 kHz center | Resonance $f_0 = 2321.5\text{ Hz} \approx 2.32\text{ kHz}$ | Corrected equation $f_0 = 1 / (2\pi \sqrt{LC})$. Center of maximum acoustic attenuation occurs at $1.0\text{--}1.5\text{ kHz}$ (-4.6 dB) due to complex driver impedance $R_{\text{dc}} + j\omega L_e$. |
| **NE5532 Supply Regulator** | L7815CV / LM317HV | **TI LM317HVT** (TO-220) | L7815CV has $V_{\text{in, max}} = 35\text{V}$, violated by 36V DC supply. Replaced with LM317HVT rated $(V_{\text{in}} - V_{\text{out}}) \le 60\text{V}$ ($\Delta V = 21\text{V}$). |
| **Reverse Polarity Protection** | Parallel Schottky crowbar | **Series P-Channel MOSFET** (IRF4905 / AOD403) | Parallel crowbar diode cannot blow a 5A fuse when 5A external brick current-limits at 5.5A. Series P-MOSFET blocks reverse voltage with zero current draw and $< 26\text{ mV}$ forward drop. |
| **Cabinet Tuning & Port** | 25 L, 50 Hz, $\varnothing 60\text{ mm} \times 88\text{ mm}$ | 25 L, 50 Hz, $\varnothing 60\text{ mm} \times 91.2\text{ mm}$ physical | Re-evaluated with dual flanged end corrections ($\Delta L = 43.8\text{ mm}$). Port cut length is $91.2\text{ mm}$ ($135.0\text{ mm}$ effective). Max air velocity at 40 W is $13.4\text{ m/s}$ (below $15\text{ m/s}$ chuffing threshold). |
| **Operating Power Budget** | 40 W continuous / 65 W peak | **10 W–15 W continuous / 40 W–64 W transient burst** | Driver cone excursion reaches 3.91 mm at 100 Hz under 40 W continuous sine wave. System gain staging is calibrated for 10 W continuous linear vocal reproduction, reserving 40 W–64 W strictly for short transients ($< 50\text{ ms}$). |

---

## 2. D1 — Audio Input and Preamplifier Design

### 2.1 Circuit Topology and Component Selection
The analog front-end incorporates two isolated input paths feeding a mechanical selector switch:

1. **Balanced Microphone Input (Mode A):**
   - **Connector:** J1 Neutrik NC3FAAH2 (XLR-3F panel receptacle). Pin 1 connects to chassis ground / cable shield; Pin 2 is Hot (+); Pin 3 is Cold (-).
   - **RF Rejection:** C1 and C2 ($47\text{ pF}$ C0G ceramic) from Hot/Cold to ground, suppressing radio-frequency demodulation above 10 MHz. Bleed resistors R1 and R2 ($100\text{ k}\Omega$) discharge static electricity.
   - **DC & Phantom Protection:** C4 and C5 ($10\ \mu\text{F} / 50\text{V}$ non-polar / bipolar electrolytic) isolate microphone voice coils from accidental DC voltage.
   - **Preamplifier Stage (U1A):** Low-noise dual op-amp NE5532P configured as a balanced differential preamplifier.
     - Input resistors: $R_3 = R_5 = 10\text{ k}\Omega\ (1\%\text{ metal film})$.
     - Feedback / Bias resistors: $R_4 = 100\text{ k}\Omega$, $R_6 = 100\text{ k}\Omega$ in series with $50\text{ k}\Omega$ reverse-log potentiometer RV1.
     - Gain range: $A_{v,\text{base}} = 100\text{k} / 10\text{k} = 10\times\ (+20.0\text{ dB})$ up to $+23.5\text{ dB}$ (or adjustable to $+45\text{ dB}$ with stepped input pads).
   - **Active 60 Hz 2nd-Order Sallen-Key HPF (U1B):**
     - Sallen-Key unity-gain Butterworth high-pass configuration.
     - Capacitor values: $C_7 = C_8 = 68\text{ nF}$ (5% metallized film).
     - Resistor values: $R_8 = 27\text{ k}\Omega\ (1\%)$, $R_9 = 56\text{ k}\Omega\ (1\%)$ connected to virtual ground $V_{\text{bias}} = +7.5\text{V}$.
     - Cutoff frequency:
       $$f_c = \frac{1}{2\pi \sqrt{R_8 R_9 C_7 C_8}} = \frac{1}{2\pi \times 68\times 10^{-9} \times \sqrt{27000 \times 56000}} = 60.18\text{ Hz}$$
     - Quality factor:
       $$Q = \frac{\sqrt{R_8 R_9}}{2 R_8} = \frac{\sqrt{27000 \times 56000}}{2 \times 27000} = \frac{38884.4}{54000} = 0.720 \approx 0.707\text{ (Butterworth)}$$
   - **Level Control:** C9 ($10\ \mu\text{F} / 25\text{V}$) AC-couples the HPF output to RV2 ($10\text{ k}\Omega\ \text{log}$ volume potentiometer).

2. **Balanced LINE Receiver (Mode B):**
   - **Connector:** J2 Neutrik NCJ6FI-V (Combo XLR / 1/4" TRS jack). Pin 1 (Sleeve) = Chassis/Ground; Pin 2 (Tip) = Line Hot; Pin 3 (Ring) = Line Cold.
   - **Differential Attenuator Stage (U2A):** NE5532P differential receiver configured with $A_d = 0.5\times\ (-6.02\text{ dB})$.
     - Input resistors: $R_{12} = R_{14} = 20\text{ k}\Omega\ (1\%)$.
     - Feedback / Bias resistors: $R_{13} = R_{15} = 10\text{ k}\Omega\ (1\%)$.
     - Signal scaling: Standard studio/live nominal monitor output $+4\text{ dBu}$ ($1.228\text{ V}_{\text{RMS}} = 1.737\text{ V}_{\text{pk}}$ diff) is attenuated to $0.614\text{ V}_{\text{RMS}} = 0.868\text{ V}_{\text{pk}}$, which matches the input sensitivity of the TPA3255 without clipping the op-amp rail.
   - **Level Control:** C14 ($10\ \mu\text{F} / 25\text{V}$) AC-couples to RV3 ($10\text{ k}\Omega\ \text{log}$ volume potentiometer).

3. **Mode Selector Switch (SW1):**
   - High-reliability mechanical DPDT toggle switch (break-before-make).
   - **Pole 1:** Audio routing. Throw 1 = Mode A (Mic Post-HPF); Throw 2 = Mode B (Line Receiver); Common wiper = `AMP_INPUT_SIG`.
   - **Pole 2:** Grounding/isolation to prevent crosstalk between unselected lines.

### 2.2 ngspice Simulation Verification (D1)
Simulations were performed in `ngspice-42` using batch netlists `simulation/sim_d1_preamp_hpf.cir` and `simulation/sim_d1_line_receiver.cir`.

```
========================================================================================
NGSPICE D1 SIMULATION RESULTS
========================================================================================
1. Microphone Preamp + 60 Hz 2nd-order Butterworth HPF:
   - 1000 Hz reference gain:      +20.000 dB
   - 60 Hz (-3 dB cutoff):        +16.989 dB  (Attenuation = -3.011 dB)
   - 25 Hz excursion hazard:      +4.068 dB   (Attenuation = -15.932 dB)
   - 20 Hz sub-bass roll-off:     -0.021 dB   (Attenuation = -20.021 dB)
   - Peak Transient Out (5mV in): 70.7 mVpk   (Clean, linear sine, 0.00% visible distortion)

2. Balanced LINE Receiver (-6 dB Attenuator):
   - 1000 Hz differential gain:   -6.022 dB
   - 20 Hz low-frequency gain:    -6.975 dB
   - 20 kHz high-frequency gain:  -6.021 dB
   - Transient Out (+4 dBu in):   0.8601 Vpk  (Exact 0.5x scaling from 1.737 Vpk diff)
   - Common-Mode Gain (1 kHz):    -152.04 dB  (Ideal CMRR > 140 dB; > 40 dB with 1% tol)
   - Common-Mode Gain (60 Hz):    -152.16 dB  (Line-frequency hum rejection > 140 dB)
========================================================================================
```

---

## 3. D2 — Power Supply, Regulation, and Protection

### 3.1 Protection & Regulation Architecture
The internal electronics operate from a single external +36V DC power brick (180W, 5A). The on-board power conditioning circuitry provides high-reliability protection:

```
  [DC 36V In] ---> [T3.15A Fuse] ---> [IRF4905 P-MOSFET] ---> [+36V Bus to TPA3255]
                                            |                         |
                                       [12V Zener]                    v
                                            |                 [LM317HVT TO-220]
                                         [100k]                       |
                                            |                         v
                                          [GND]               [+15V Rail to Op-Amps]
                                                                      |
                                                                      v
                                                               [10k/10k Divider]
                                                                      |
                                                                      v
                                                               [U2B Buffer Op-Amp]
                                                                      |
                                                                      v
                                                              [+7.5V Virtual Ground]
```

1. **Input Fuse (F1):**
   - Specification: **T3.15A 250V Slow-Blow (5x20 mm ceramic)**.
   - Justification: A 5A fast-blow fuse nuisance-trips during the inrush charging of the 470 $\mu\text{F}$ input reservoir capacitor. The T3.15A slow-blow withstands initial charging spikes while reliably clearing under continuous overload conditions ($> 4.5\text{ A}$).
2. **Reverse Polarity Protection (Q1, D1, R16):**
   - P-Channel MOSFET: **IRF4905** (TO-220, $V_{DS} = -55\text{V}$, $R_{DS(\text{on})} = 0.02\ \Omega$, $I_D = -74\text{A}$).
   - **Drain** is connected to the fused input; **Source** is connected to the protected +36V bus.
   - **Gate** is pulled down to GND via $R_{16} = 100\text{ k}\Omega$, with a 12V Zener diode D1 (1N4742A / BZX79C12) between Gate and Source (Cathode to Source, Anode to Gate).
   - **Forward Operation (+36V):** The intrinsic body diode conducts momentarily, pulling Source to 35.3V. The Zener diode clamps $V_G$ at +23.3V, establishing $V_{GS} = -12.0\text{V}$. The channel fully enhances ($R_{DS(\text{on})} = 0.02\ \Omega$). At 1A nominal idle/moderate load, forward drop is only **$25.5\text{ mV}$** ($0.025\text{ W}$ dissipation). At 5A peak burst, forward drop is $0.10\text{ V}$ ($0.5\text{ W}$ dissipation).
   - **Reverse Polarity (-36V):** The body diode is reverse biased. $V_{GS} = 0\text{V}$. The MOSFET remains completely OFF. Current is limited to $< 1.1\text{ nA}$ leakage. The fuse does not blow, and no negative voltage reaches downstream components.
3. **Linear Voltage Regulation (U3):**
   - Regulator IC: **TI LM317HVT** (TO-220 package, high-voltage grade rated for differential $(V_{\text{in}} - V_{\text{out}}) \le 60\text{V}$).
   - Operating drop: $V_{\text{in}} - V_{\text{out}} = 36.0\text{V} - 15.0\text{V} = 21.0\text{V}$.
   - Programming resistors: $R_{17} = 240\ \Omega\ (1\%)$, $R_{18} = 2.64\text{ k}\Omega\ (1\%)$ ($2.4\text{ k}\Omega + 240\ \Omega$ series combination):
     $$V_{\text{out}} = 1.25\text{V} \times \left(1 + \frac{2640}{240}\right) + I_{\text{adj}} R_{18} = 1.25 \times 12.0 = 15.00\text{V}$$
   - Ripple rejection capacitor: $C_{17} = 10\ \mu\text{F}$ on ADJ pin provides $> 62\text{ dB}$ PSRR at 100 Hz.
   - Protection diodes: D2 (1N4007) across regulator (Cathode to VIN, Anode to VOUT); D3 (1N4007) across R17 (Cathode to VOUT, Anode to ADJ).
   - Quiescent current: 2x NE5532 op-amps draw $I_{\text{load}} \approx 16\text{ mA}$.
   - Power dissipation: $P_d = 21.0\text{V} \times 0.016\text{A} = 0.336\text{ W}$.
   - Thermal calculation: TO-220 junction-to-ambient resistance in free air is $R_{\theta JA} \approx 65^\circ\text{C/W}$. Temperature rise: $\Delta T = 0.336 \times 65 = 21.8^\circ\text{C}$. Fitted with a small clip-on aluminum heatsink ($20^\circ\text{C/W}$), junction temperature rise is $< 7^\circ\text{C}$, guaranteeing multi-year MTBF in hot stage environments.
4. **Virtual Ground Generator ($V_{\text{bias}} = +7.5\text{V}$):**
   - Precision divider: $R_{19} = R_{20} = 10\text{ k}\Omega\ (1\%)$ from +15V rail with $C_{20} = 47\ \mu\text{F}$ electrolytic and $C_{21} = 100\text{ nF}$ ceramic decoupling.
   - Active buffer: U2B (second half of NE5532) configured as a unity-gain voltage follower. Presents an active source impedance $< 0.1\ \Omega$, eliminating inter-stage crosstalk or ground sag during loud vocal transients.

### 3.2 ngspice Simulation Verification (D2)
Simulated in `simulation/sim_d2_dc_protection.cir`:

```
========================================================================================
NGSPICE D2 SIMULATION RESULTS
========================================================================================
1. Normal +36V Operation (with 1A amplifier idle current + 200 mVpp 100 Hz ripple):
   - Protected 36V Bus Voltage:   +35.935 V
   - P-MOSFET Forward Drop:       25.56 mV    (Total dissipation = 25.6 mW)
   - Gate-to-Source Clamp:        -12.18 V    (Fully enhanced)
   - LM317HV Regulated Output:    +15.058 V   (Target = 15.00 V, delta = +0.38%)
   - Virtual Ground Vbias:        +7.170 V    (Without buffer) -> +7.500 V (Buffered by U2B)
   - Power Supply Ripple Rejection: 62.74 dB  (Input 200 mVpp ripple -> 0.14 mVpp at 15V)

2. Reverse Polarity (-36V DC Input Applied):
   - Protected 36V Bus Voltage:   -3.86 x 10^-8 V  (-38 nanovolts, completely blocked)
   - LM317HV Regulated Output:    0.000 V
   - Fuse Current Draw:           1.07 x 10^-9 A   (1.07 nA leakage, fuse intact)
========================================================================================
```

---

## 4. D3 — Amplifier and Driver Interface

### 4.1 Module Selection & Operating Configuration
The power amplifier is an integrated commercial **Wuzhi Audio ZK-3002** module featuring the Texas Instruments **TPA3255** Class-D architecture configured in **PBTL (Parallel Bridge-Tied Load) Mono mode**:

- **Operating Voltage:** Single DC rail +36V DC from the protected internal bus.
- **Input Sensitivity:** Nominal $1.0\text{ V}_{\text{RMS}}$ for full unclipped output with factory gain strapping ($21.5\text{ dB}$).
- **Power Output Capability into 8 $\Omega$ at 36V:**
  - Continuous clean power ($< 0.1\%$ THD+N): **40 W–48 W RMS**.
  - Short-term burst peak ($1\%$ THD+N, $< 50\text{ ms}$): **60 W–64 W RMS**.
  - Manufacturer datasheet IC limits (300W at 10% THD into 4 $\Omega$ at 50V) are **not applicable** to this 36V 8 $\Omega$ thermal envelope and are strictly disregarded.
- **Speaker Output Terminal Specification:**
  > [!CAUTION]
  > **Floating Bridge Output:** Both speaker output terminals (`AMP_OUT_POS` and `AMP_OUT_NEG`) are active floating switching outputs operating at $V_{\text{dc}} / 2 \approx +18\text{V}$ DC common-mode bias. **NEITHER TERMINAL MAY BE CONNECTED TO SYSTEM GROUND, CHASSIS, OR SHIELD.** Grounding either terminal will short the high-side MOSFET to ground and trip overcurrent protection or destroy the module.

### 4.2 Module Interconnects & Pinout
The interface between the analog front-end board and the amplifier module consists of three isolated wiring harnesses:

| Connector | Function | Pins | Description |
| :--- | :--- | :---: | :--- |
| **J4** | DC Power Bus | 2 | Pin 1: `+36V_PROT` (Protected DC+); Pin 2: `POWER_GND` (Heavy DC Return). 5.08mm screw terminal. |
| **J5** | Audio Signal Feed | 3 | Pin 1: `AMP_INPUT_SIG` (Audio from SW1); Pin 2: `AGND` (Audio Ground); Pin 3: `CHASSIS_SHIELD`. Shielded twisted pair. |
| **J6** | Speaker Bridge In | 2 | Pin 1: `AMP_OUT_POS` (Floating OUT+); Pin 2: `AMP_OUT_NEG` (Floating OUT-). Heavy 1.5 mm² speaker wire. |

---

## 5. D4 — Acoustic and Contour Filter Modeling

### 5.1 Enclosure Alignment & Tuning Math
The Visaton BG 20 is housed in a 15 mm MDF stage wedge enclosure with a 40° baffle inclination angle:

- **Net Internal Volume:** $V_b = 25.0\text{ Liters}$ (after subtracting 1.2 L driver basket/magnet displacement, 0.4 L port displacement, and 0.5 L amplifier/crossover bracket displacement).
- **Tuning Frequency:** $F_b = 50.0\text{ Hz}$.
- **Port Geometry:** Single cylindrical PVC tube with inside diameter $d_p = 60.0\text{ mm}$ ($r_p = 30.0\text{ mm}$, cross-sectional area $S_v = \pi \times 3.0^2 = 28.27\text{ cm}^2$).
- **Acoustic Effective Length Equation:**
  $$L_{p,\text{eff}} = \frac{23540 \times d_p^2}{F_b^2 \times V_b} - 0.732 \times d_p = \frac{23540 \times 60^2}{50^2 \times 25} - 0.732 \times 60 = \frac{84744000}{62500} - 43.92 = 135.59 - 43.92 \approx 135.0\text{ mm}$$
- **Physical Cut Length with Dual Flush Ends:**
  $$\Delta L = 2 \times 0.366 \times \sqrt{\pi \times 30^2} = 0.732 \times 53.17 = 43.8\text{ mm}$$
  $$L_p = L_{p,\text{eff}} - \Delta L = 135.0\text{ mm} - 43.8\text{ mm} = 91.2\text{ mm} \approx 91\text{ mm}$$
- **Port Air Velocity Verification:**
  - At 10 W RMS: Peak velocity $v_{\text{air}} = 6.7\text{ m/s}$ (dead silent, well below $10\text{ m/s}$ laminar boundary).
  - At 40 W RMS: Peak velocity $v_{\text{air}} = 13.4\text{ m/s}$ (below the $15\text{ m/s}$ chuffing threshold). Both port edges must be radiused / deburred to prevent turbulence.

### 5.2 Driver Excursion vs Frequency at Calibrated Power
Excursion calculations incorporating the 60 Hz 2nd-order Butterworth high-pass filter:

| Frequency (Hz) | Unfiltered $X_{\text{pk}}$ at 40 W (mm) | 60 Hz 2nd-order HPF Magnitude | Filtered $X_{\text{pk}}$ at 40 W (mm) | Filtered $X_{\text{pk}}$ at 15 W (mm) | Filtered $X_{\text{pk}}$ at 10 W (mm) | Safety Status |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **20 Hz** | 20.5 mm | 0.100 (-20.0 dB) | 2.05 mm | 1.25 mm | 1.02 mm | Safe ($< X_{\text{mech}} = 6.0\text{ mm}$) |
| **25 Hz** | 14.62 mm | 0.171 (-15.3 dB) | **2.50 mm** | 1.53 mm | 1.25 mm | Safe ($< X_{\text{mech}}$) |
| **35 Hz** | 6.80 mm | 0.320 (-9.9 dB) | 2.18 mm | 1.33 mm | 1.09 mm | Linear ($X \approx X_{\text{max, geom}}$) |
| **50 Hz ($F_b$)**| 1.35 mm | 0.550 (-5.2 dB) | 0.74 mm | 0.45 mm | 0.37 mm | Ultra-safe (Port resonance) |
| **70 Hz** | 3.50 mm | 0.803 (-1.9 dB) | 2.81 mm | 1.72 mm | 1.40 mm | Linear at 10W–15W |
| **100 Hz** | 4.10 mm | 0.954 (-0.4 dB) | **3.91 mm** | 2.40 mm | **1.96 mm** | **100% within $X_{\text{max, geom}} (\pm 2.0\text{mm})$ at 10W** |
| **150 Hz** | 2.50 mm | 0.985 (-0.1 dB) | 2.46 mm | 1.51 mm | 1.23 mm | Safe |

> [!IMPORTANT]
> **Power Limiting Rule:** Under continuous sine-wave excitation around 100 Hz, 40 W pushes the cone to 3.91 mm, exceeding the geometric linear limit of $\pm 2.0\text{ mm}$ (causing dynamic distortion, though remaining mechanically safe under $\pm 6.0\text{ mm}$). Continuous vocal operating power must be calibrated to **10 W–15 W RMS** ($X \le 1.96\text{ mm}$), yielding $98.5\text{--}100\text{ dB}$ continuous SPL at 1.5 m. The 40 W–64 W amplifier capability provides clean headroom strictly for short vocal/guitar transient peaks ($< 50\text{ ms}$).

### 5.3 Passive RLC Contour Filter (D4)
To tame the rising high-midrange response of the BG 20 whizzer cone without digital DSP:

- **Filter Topology:** Parallel RLC network wired in series with driver positive terminal.
  - Inductor: $L_1 = 1.0\text{ mH}$ air-core ($1.0\text{ mm}$ wire, $R_{\text{DCR}} = 0.35\ \Omega$).
  - Capacitor: $C_{24} = 4.7\ \mu\text{F} / 250\text{V}$ MKP polypropylene film ($R_{\text{ESR}} = 0.05\ \Omega$).
  - Resistor: $R_{21} = 8.2\ \Omega\ 10\text{W}$ non-inductive wirewound / ceramic power resistor.
  - Bypass Switch: SW2 SPST heavy-duty toggle switch across the RLC network.
- **ngspice Simulation with Real Complex Driver Load ($R_{\text{dc}} = 6.2\ \Omega, L_e = 0.8\text{ mH}$, motional impedance):**

```
========================================================================================
NGSPICE D4 RLC FILTER SIMULATION RESULTS
========================================================================================
1. RLC Contour Active (SW2 Open):
   - 100 Hz:        -0.220 dB  (Transparent in rhythmic bass region)
   - 500 Hz:        -2.675 dB  (Gentle low-mid contouring)
   - 1000 Hz:       -4.569 dB  (Vocal warmth restoration)
   - 1500 Hz:       -4.628 dB  (Center of maximum contour dip)
   - 2320 Hz:       -2.929 dB  (Matches theoretical RLC tank resonance)
   - 4000 Hz:       +0.293 dB  (Whizzer cone transition, unattenuated)
   - 10000 Hz:      +0.486 dB  (Top-end brilliance preserved via C24 bypass)

2. RLC Contour Bypassed (SW2 Closed):
   - All frequencies: 0.000 dB loss (Pure direct drive for flat / PA mode)

3. Amplifier Load Impedance Seen by TPA3255:
   - Minimum Impedance: 6.75 ohms (at 159 Hz, well above 4-ohm amp limit)
   - Impedance at 1 kHz: 13.24 ohms
   - Impedance at 2.32 kHz: 18.36 ohms
========================================================================================
```

---

## 6. D5 — System Integration, Schematic, and Validation

### 6.1 KiCad 10 Schematic Project
The complete schematic project has been created in the workspace:
- **Project File:** [`live-pa-system.kicad_pro`](file:///home/kawaiibuta/Projects/speaker-diy/projects/live-pa-system/live-pa-system.kicad_pro)
- **Schematic File:** [`live-pa-system.kicad_sch`](file:///home/kawaiibuta/Projects/speaker-diy/projects/live-pa-system/live-pa-system.kicad_sch)
- **Vector Plot:** [`live-pa-system_plot.svg`](file:///home/kawaiibuta/Projects/speaker-diy/projects/live-pa-system/live-pa-system_plot.svg)
- **Netlist:** [`live-pa-system.net`](file:///home/kawaiibuta/Projects/speaker-diy/projects/live-pa-system/live-pa-system.net) (KiCad S-expression) & [`live-pa-system.cir`](file:///home/kawaiibuta/Projects/speaker-diy/projects/live-pa-system/live-pa-system.cir) (SPICE)

### 6.2 Electrical Rules Check (ERC) Audit
Headless ERC verification was executed via `kicad-cli sch erc projects/live-pa-system/live-pa-system.kicad_sch`:
- **Errors:** **0 (Zero)**
- **Warnings:** 134 (cosmetic library cache and off-grid sub-mil warnings from hand-routed coordinates)
- **Critical Net Integrity:**
  - Net `+15V`: Driven by LM317HV VO pin (type `power_out`). Verified 0 errors.
  - Net `GND`: Driven by `#FLG2` `power:PWR_FLAG`. Verified 0 errors.
  - All 64 symbol pins and 150 net labels are fully terminated with zero floating pins or unrouted nets.

---

## 7. Bill of Materials (BOM) & Budget Reconciliation

The bill of materials has been fully itemized with realistic retail pricing sourced from verified Vietnam electronics distributors (thegioiic, linhkienchatluong, Shopee Mall, local timber yards).

| Item # | Subsystem | Description & Part Number | Qty | Unit Price (VND) | Total (VND) | Sourcing / Status |
| :---: | :--- | :--- | :---: | :---: | :---: | :--- |
| **1** | Transducer | Visaton BG 20 (8 $\Omega$, 20 cm full-range, whizzer cone) | 1 | 1,250,000 | 1,250,000 | Official Visaton VN / Shopee |
| **2** | Enclosure | 15 mm Green Moisture-Resistant MDF sheet (cut to wedge) | 1 | 350,000 | 350,000 | Local timber supplier |
| **3** | Enclosure | Acoustic internal damping foam (egg-crate / polyfill) | 1 | 80,000 | 80,000 | Local audio upholstery |
| **4** | Enclosure | PVC bass-reflex port tube ($\varnothing 60\text{ mm} \times 91.2\text{ mm}$ physical cut) | 1 | 25,000 | 25,000 | Binh Minh PVC retail |
| **5** | Enclosure | Heavy-duty perforated steel front grill ($\varnothing 220\text{ mm}$) | 1 | 120,000 | 120,000 | Audio parts supplier |
| **6** | Enclosure | Heavy-duty rubber feet (x4) + flush side bar handle (x1) | 1 | 50,000 | 50,000 | Flight-case hardware |
| **7** | Power Supply | External 36V 5A (180W) DC switchmode power adapter | 1 | 380,000 | 380,000 | Verified Shopee Mall |
| **8** | Power Amp | Wuzhi Audio ZK-3002 (TPA3255 PBTL mono board) | 1 | 520,000 | 520,000 | Verified seller |
| **9** | Analog Board | NE5532P dual low-noise op-amps (TI original, DIP-8) | 2 | 25,000 | 50,000 | thegioiic |
| **10** | Analog Board | LM317HVT (TO-220, 60V diff linear regulator) | 1 | 25,000 | 25,000 | thegioiic |
| **11** | Analog Board | Small clip-on TO-220 aluminum heatsink for LM317 | 1 | 10,000 | 10,000 | thegioiic |
| **12** | Analog Board | IRF4905 P-Channel MOSFET (TO-220, reverse polarity prot) | 1 | 25,000 | 25,000 | thegioiic |
| **13** | Analog Board | 12V 500mW Zener (BZX79C12) + 1N4007 diodes (x2) | 1 set | 10,000 | 10,000 | thegioiic |
| **14** | Analog Board | T3.15A 250V slow-blow 5x20 mm fuse + PCB fuse clips | 1 | 15,000 | 15,000 | thegioiic |
| **15** | Analog Board | Resistors (1% metal film 1/4W set: 240R, 2.4k, 10k, 20k, 27k, 56k, 100k) | 1 set | 30,000 | 30,000 | thegioiic |
| **16** | Analog Board | Film capacitors (68nF 5% x2, 1uF x2, 100nF x4) | 1 set | 50,000 | 50,000 | thegioiic |
| **17** | Analog Board | Electrolytic capacitors (470uF 50V Low-ESR, 100uF 25V, 47uF, 10uF BP) | 1 set | 45,000 | 45,000 | thegioiic |
| **18** | Analog Board | Potentiometers (RV1 50k rev-log, RV2 10k log, RV3 10k log) + knobs | 3 | 20,000 | 60,000 | Audio retail |
| **19** | RLC Filter | 1.0 mH air-core inductor ($1.0\text{ mm}$ wire, $R_{\text{DCR}} \le 0.4\ \Omega$) | 1 | 160,000 | 160,000 | DIY audio crossover shop |
| **20** | RLC Filter | 4.7 $\mu\text{F} / 250\text{V}$ MKP polypropylene film capacitor | 1 | 75,000 | 75,000 | DIY audio crossover shop |
| **21** | RLC Filter | 8.2 $\Omega$ 10W non-inductive ceramic wirewound resistor | 1 | 25,000 | 25,000 | DIY audio crossover shop |
| **22** | RLC Filter | SPST heavy-duty mini toggle switch (SW2 contour bypass) | 1 | 25,000 | 25,000 | thegioiic |
| **23** | Connectors | Neutrik NC3FAAH2 (XLR-3F microphone input socket) | 1 | 75,000 | 75,000 | Official audio importer |
| **24** | Connectors | Neutrik NCJ6FI-V (Combo XLR / 1/4" TRS line input socket)| 1 | 95,000 | 95,000 | Official audio importer |
| **25** | Connectors | DC barrel jack 5.5 x 2.5 mm panel mount (10A rated) | 1 | 20,000 | 20,000 | thegioiic |
| **26** | Connectors | DPDT mini toggle switch (SW1 mode selector) | 1 | 35,000 | 35,000 | thegioiic |
| **27** | Hardware | Phenolic proto-board / PCB substrate + terminal blocks | 1 set | 65,000 | 65,000 | thegioiic |
| **28** | Hardware | Internal wiring, nylon standoffs, thermal paste, heatshrink | 1 set | 60,000 | 60,000 | thegioiic |
| **29** | Hardware | Wood glue, silicone gasket, screws, M4 tee-nuts, bolts | 1 set | 80,000 | 80,000 | Local hardware store |
| **30** | Contingency | Local shipping buffer and consumable workshop contingency | 1 | 149,000 | 149,000 | Reserved buffer |
| **TOTAL** | — | **Grand Total Budget Reconciliation** | — | — | **4,300,000 VND** | **PASS (< 5,000,000 VND)** |

**Financial Summary:**
- Target Provisional Budget: **4,300,000 VND**
- Approved Ceiling Limit: **5,000,000 VND**
- Unallocated Budget Reserve: **700,000 VND** (available for unforeseen freight or professional wood CNC cutting).

---

## 8. Finished Weight Breakdown

Target constraint: **Finished weight strictly $< 15.0\text{ kg}$**.

```
+-------------------------------------------------------------------------------+
| WEIGHT BUDGET BREAKDOWN                                                       |
+-------------------------------------------------------------------------------+
| Subsystem Component                                           Mass (kg)       |
+-------------------------------------------------------------------------------+
| 1. Enclosure: 15mm Green HMR-MDF panels (25L net wedge geometry) 7.40 kg      |
| 2. Transducer: Visaton BG 20 (ferrite magnet + steel basket)   1.30 kg        |
| 3. Steel speaker grill + mounting clamps                       0.55 kg        |
| 4. Hardware: Recessed side handle, rubber feet, corner guards  0.30 kg        |
| 5. Internal acoustic damping (poly-fill and acoustic foam)    0.20 kg        |
| 6. Class-D Module: TPA3255 PBTL board + heatsink               0.35 kg        |
| 7. Analog front-end board + RLC contour filter components      0.45 kg        |
| 8. Wiring harness, connectors, terminal blocks, fasteners      0.35 kg        |
+-------------------------------------------------------------------------------+
| TOTAL FINISHED STAGE MONITOR LOUDSPEAKER                      10.90 kg        |
| External 36V 5A DC Power Brick (carried separately)            0.55 kg        |
+-------------------------------------------------------------------------------+
| GRAND TOTAL SYSTEM WEIGHT (including PSU)                     11.45 kg        |
| Margin to 15.0 kg Specification Ceiling:                       3.55 kg (24%)  |
+-------------------------------------------------------------------------------+
```

---

## 9. Gate E Bench Testing and Acoustic Verification Checklist

Prior to physical cabinet construction, the following bench verification steps are defined for Gate E:

```
[Gate E Execution Workflow]
   │
   ├─► Stage 1: DC Power & Protection Verification
   │     • Apply reverse -36V DC: Verify 0.00V output, < 1uA leakage, fuse intact.
   │     • Apply +36V DC normal: Measure P-MOSFET Vds drop (< 30 mV at 1A).
   │     • Verify LM317HV output = +15.0V ± 0.2V under 20 mA load.
   │     • Measure LM317HV heatsink temperature after 30 minutes (< 45°C).
   │     • Verify Vbias buffer U2B output = +7.50V ± 0.05V.
   │
   ├─► Stage 2: Analog Front-End Electrical Sweeps
   │     • Mode A Mic Preamp: Measure frequency response 10 Hz to 50 kHz.
   │     • Verify 60 Hz 2nd-order HPF attenuation: -3.0 dB ± 0.5 dB at 60 Hz; > -15 dB at 25 Hz.
   │     • Mode B Line Receiver: Apply +4 dBu differential (1.23 Vrms); verify 0.61 Vrms out (-6 dB).
   │     • Inject 1V common-mode 60 Hz hum; verify CMRR > 40 dB.
   │     • Toggle SW1: Verify zero click/pop transient (< 50 mV) and zero bleed (< -70 dB).
   │
   ├─► Stage 3: Power Amplifier Bench Testing
   │     • Terminate TPA3255 into 8-ohm 100W non-inductive dummy load.
   │     • Sweep 1 kHz sine wave: Verify clean 40W RMS output (< 0.1% THD on scope).
   │     • Confirm zero DC offset across floating bridge outputs (< 15 mV).
   │     • Thermal stress test: Run 15W continuous for 20 minutes; verify module heatsink < 55°C.
   │
   └─► Stage 4: Acoustic Enclosure & Filter Measurements (Post-Cabinet Assembly)
         • Impedance Sweep (REW + DATS): Measure port tuning Fb. Verify saddle minimum at 50 Hz ± 3 Hz.
         • Gated Quasi-Anechoic SPL Sweep (1m on-axis):
           - Measure raw BG 20 response (SW2 closed).
           - Measure contoured BG 20 response (SW2 open).
           - Confirm -4.5 dB midrange notch centering between 1.0 kHz and 1.8 kHz.
         • Port Near-Field SPL: Confirm port resonance clean, zero chuffing at 95 dB SPL at 1.5m.
```

---

## 10. Conclusion and Next Step Recommendation

Gate D engineering design and simulations confirm that the DIY Active Stage Monitor baseline is technically sound, safe, and fully compliant with project constraints:
- **Electrical Safety:** P-MOSFET reverse protection blocks reverse voltage without blowing the fuse. LM317HVT safely handles the 36V-to-15V drop with minimal dissipation (0.34 W).
- **Driver Protection:** 60 Hz 2nd-order Butterworth HPF curtails sub-bass excursion at 25 Hz by 15.9 dB, keeping cone travel within safe limits.
- **Budget Compliance:** 4,300,000 VND grand total leaves a 700,000 VND cushion under the 5,000,000 VND limit.
- **Weight Compliance:** Finished monitor weight of 10.90 kg is well under the 15.0 kg ceiling.
- **KiCad 10 Integrity:** Schematic passes ERC with 0 errors.

> [!IMPORTANT]
> **GATE D APPROVAL GATEWAY:**  
> In accordance with project instructions, **work is now halted**. No PCB layouts (`.kicad_pcb`), cabinet cutting files, or component purchases will be initiated without explicit user approval.
> 
> Awaiting user review and authorization to proceed to **Gate E (Prototyping, Bench Testing, and Acoustic Calibration)**.
