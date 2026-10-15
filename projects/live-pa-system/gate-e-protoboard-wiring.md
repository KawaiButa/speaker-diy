# Gate E Prototyping Board Wiring & Assembly Guide
## DIY Active Stage Monitor Loudspeaker (Visaton BG 20 + TPA3255 PBTL)

**Document:** Universal Perfboard Wiring Schedule, Placement Map & Point-to-Point Checklist  
**Project Path:** [`projects/live-pa-system/`](file:///home/kawaiibuta/Projects/speaker-diy/projects/live-pa-system/)  
**Baseline Circuit:** 100% Netlist Verified (`live-pa-system.kicad_sch`, 42 nets, 73 components)  
**Target Hardware:** Off-the-shelf double-sided FR-4 perfboards ($2.54\text{ mm}$ pitch, isolated tinned pads)  
**Date:** October 15, 2026  
**Revision:** 2.1 (Phased Subsystem Modular Mapping)  

---

## 1. Physical Grid & Board Coordinate System

Three generic universal prototyping boards are used. Every pad is addressed by **(Column Letter, Row Number)**:

* **Board A ($7 \times 9\text{ cm}$, Audio Analog Front-End):**
  * **Columns:** $26$ columns, labeled **A to Z** (left to right).
  * **Rows:** $31$ rows, labeled **1 to 31** (top to bottom).
  * **Hole Pitch:** $2.54\text{ mm}$ ($0.1\text{''}$).
  * **Mounting Holes:** 4 $\times$ M3 corner holes at $(A, 1)$, $(Z, 1)$, $(A, 31)$, $(Z, 31)$.
  * **Functional Partition:** Zone 1 = Mic Preamp (Cols A–L); Zone 2 = Line Receiver & Common 60 Hz HPF (Cols M–Z).
* **Board B ($5 \times 7\text{ cm}$, Power Conditioning & +7.5V Active Bias Reference):**
  * **Columns:** $18$ columns, labeled **A to R**.
  * **Rows:** $24$ rows, labeled **1 to 24**.
  * **Mounting Holes:** 4 $\times$ M3 corner holes at $(A, 1)$, $(R, 1)$, $(A, 24)$, $(R, 24)$.
  * **Functional Partition:** Left (Cols A–G) = Protection & 36V; Center (Cols H–L) = LM317 +15V; Right (Cols M–R) = U3 Virtual Ground Buffer.
* **Board C ($5 \times 7\text{ cm}$, Passive RLC Speaker Filter):**
  * **Columns:** $18$ columns, labeled **A to R**.
  * **Rows:** $24$ rows, labeled **1 to 24**.
  * **Mounting Holes:** 4 $\times$ M3 corner holes at $(A, 1)$, $(R, 1)$, $(A, 24)$, $(R, 24)$.
  * **STRICT ISOLATION:** ZERO ground traces or ground pads. Both rails float at $+18\text{ V}$ DC half-supply.

---

## 2. Master Component Placement Tables

### Board B: Power Conditioning & +7.5V Bias Reference ($5 \times 7\text{ cm}$)
*Scaled Diagram:* [`gate-e-board-b-assembly.svg`](file:///home/kawaiibuta/Projects/speaker-diy/projects/live-pa-system/gate-e-board-b-assembly.svg)

| RefDes | Value | Package / Footprint | Lead 1 Hole | Lead 2 Hole | Lead 3 / Extra | Orientation / Assembly Notes |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **TB_DC_IN** | 2-Pin Screw Terminal | Pitch $5.08\text{ mm}$ | **B2** (+36V In) | **C2** (GND Return)| — | From panel fuse `F1` (3.15A/4A) and DC jack `J3`. |
| **TB_AMP_PWR**| 2-Pin Screw Terminal | Pitch $5.08\text{ mm}$ | **E2** (+36V Out)| **F2** (GND Out) | — | Feeds TPA3255 amplifier directly (18 AWG silicone). |
| **Q1** | IRF4905 | TO-220 Power P-FET | **B6** (Gate) | **C6** (Drain / Tab)| **D6** (Source) | **Tab is Drain.** Floating clip-on heatsink. |
| **R18** | $100\text{ k}\Omega, 1/4\text{ W}$ | Axial $1/4\text{ W}, 1\%$ | **B8** | **D8** | — | Gate pull-down to GND. |
| **D1** | BZX79C12 ($12\text{V}$)| DO-35 Zener Diode | **B9** (Cathode) | **D9** (Anode) | — | Clamps Gate-to-Source to 12V maximum. |
| **C17** | $470\ \mu\text{F} / 50\text{ V}$| Radial Low-ESR Electrolytic | **D13** ($+$) | **E13** ($-$) | — | Bulk reservoir capacitor. Observe negative stripe. |
| **C18** | $100\text{ nF} / 50\text{ V}$| Monolithic Ceramic / Film | **B13** | **C13** | — | High-frequency DC rail bypass. |
| **U4** | LM317HVT | TO-220 Linear Regulator | **I9** (Pin 1 ADJ) | **J9** (Pin 2 VOUT)| **K9** (Pin 3 VIN)| **TAB IS +15V (NOT GND!).** Floating heatsink. |
| **D2** | 1N4007 | DO-41 Rectifier Diode | **J6** (Anode) | **K6** (Cathode) | — | Reverse protection diode across LM317. |
| **R19** | $240\ \Omega, 1/4\text{ W}$ | Axial $1/4\text{ W}, 1\%$ | **I13** | **J13** | — | LM317 program resistor. |
| **R20** | $2.64\text{ k}\Omega, 1/4\text{ W}$ | Axial $1/4\text{ W}, 1\%$ | **H15** | **I15** | — | LM317 setting resistor ($2.4\text{k} + 240\Omega$). |
| **C19** | $10\ \mu\text{F} / 25\text{ V}$ | Radial Polarized Electrolytic | **I17** ($+$) | **H17** ($-$) | — | ADJ pin ripple bypass capacitor. |
| **D3** | 1N4007 | DO-41 Rectifier Diode | **H13** (Anode) | **I13** (Cathode) | — | Reverse protection diode across R20. |
| **C20** | $100\ \mu\text{F} / 25\text{ V}$| Radial Polarized Electrolytic | **J15** ($+$) | **L15** ($-$) | — | Output filter capacitor. |
| **C21** | $100\text{ nF} / 50\text{ V}$| Monolithic Ceramic / Film | **J17** | **K17** | — | Output high-frequency bypass. |
| **R21** | $10\text{ k}\Omega, 1/4\text{ W}$ | Axial $1/4\text{ W}, 1\%$ | **N5** | **P5** | — | Virtual ground divider upper leg (+15V side). |
| **R22** | $10\text{ k}\Omega, 1/4\text{ W}$ | Axial $1/4\text{ W}, 1\%$ | **N7** | **P7** | — | Virtual ground divider lower leg (GND side). |
| **C22** | $10\ \mu\text{F} / 25\text{ V}$ | Radial Polarized Electrolytic | **N9** ($+$) | **P9** ($-$) | — | Divider filter capacitor. |
| **U3 Socket**| DIP-8 IC Socket | Machined Tulip Contact | **N12** (Pin 1) | **N13** (Pin 2) | Pins 3..8: N14, N15, Q15, Q14, Q13, Q12 | Notch faces Row 11 (UP). |
| **C26** | $100\text{ nF} / 50\text{ V}$| Monolithic Ceramic / Film | **N17** | **Q17** | — | U3 supply decoupling (+15V to GND). |
| **C23** | $47\ \mu\text{F} / 25\text{ V}$ | Radial Polarized Electrolytic | **N19** ($+$) | **P19** ($-$) | — | Virtual ground output reservoir. |
| **C25** | $100\text{ nF} / 50\text{ V}$| Monolithic Ceramic / Film | **N21** | **P21** | — | Virtual ground HF bypass. |
| **TB_PWR_OUT**| 4-Pin Screw Terminal | Pitch $5.08\text{ mm}$ | **N23** (+15V Out)| **O23** (GND Out) | **P23** (VBIAS Out), **Q23** (Spare/Shield) | Clean analog feeder to Board A. |

---

### Board A: Audio Analog Front-End ($7 \times 9\text{ cm}$)
*Scaled Diagram:* [`gate-e-board-a-assembly.svg`](file:///home/kawaiibuta/Projects/speaker-diy/projects/live-pa-system/gate-e-board-a-assembly.svg)

| RefDes | Value | Package / Footprint | Lead 1 Hole | Lead 2 Hole | Lead 3 / Extra | Orientation / Assembly Notes |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **TB_MIC** | 3-Pin Screw Terminal | Pitch $5.08\text{ mm}$ | **B2** (Pin 1 GND) | **C2** (Pin 2 HOT) | **D2** (Pin 3 COLD) | From panel XLR female jack `J1`. |
| **TB_LINE**| 3-Pin Screw Terminal | Pitch $5.08\text{ mm}$ | **N2** (Pin 1 GND) | **O2** (Pin 2 HOT) | **P2** (Pin 3 COLD) | From panel Combo jack `J2`. |
| **TB_PWR** | 3-Pin Screw Terminal | Pitch $5.08\text{ mm}$ | **W2** (Pin 1 +15V)| **X2** (Pin 2 GND) | **Y2** (Pin 3 VBIAS)| Fed from Board B `TB_PWR_OUT`. |
| **TB_OUT** | 3-Pin Screw Terminal | Pitch $5.08\text{ mm}$ | **R30** (Pin 1 SIG)| **S30** (Pin 2 GND)| **T30** (Pin 3 SHLD)| Shielded audio cable to TPA3255 input. |
| **U1 Socket**| DIP-8 Socket | Machined Tulip Contact | **E12** (Pin 1) | **E13** (Pin 2) | Pins 3..8: E14, E15, H15, H14, H13, H12 | Mic Preamp. Notch faces Row 11 (UP). |
| **U2 Socket**| DIP-8 Socket | Machined Tulip Contact | **Q12** (Pin 1) | **Q13** (Pin 2) | Pins 3..8: Q14, Q15, T15, T14, T13, T12 | Line & HPF. Notch faces Row 11 (UP). |
| **RV1** | $50\text{ k}\Omega$ Rev-Log | 3-Pin Potentiometer | **C27** (Pin 1 CW) | **D27** (Pin 2 WIP)| **E27** (Pin 3 CCW)| Mic Gain control. |
| **RV2** | $10\text{ k}\Omega$ Log | 3-Pin Potentiometer | **G27** (Pin 1 CW) | **H27** (Pin 2 WIP)| **I27** (Pin 3 CCW)| Mic Volume control. |
| **RV3** | $10\text{ k}\Omega$ Log | 3-Pin Potentiometer | **N27** (Pin 1 CW) | **O27** (Pin 2 WIP)| **P27** (Pin 3 CCW)| Line Volume control. |
| **SW1** | DPDT Slide Switch | 6-Pin ($2 \times 3$ grid) | **U27** (Pin 1) | **V27** (Pin 2 WIP)| Pins 3..6: W27, U28, V28, W28 | Mode Selector (Vocal / Monitor). |
| **TP1** | Test Point Pad | Single Pin / Turret | **V24** | — | — | Probe point for 60 Hz HPF output. |
| **C1, C2** | $47\text{ pF} / 100\text{ V}$ | Disc Ceramic ($5\text{ mm}$) | **C4**, **C5** | **D4**, **D5** | — | RF filters across Mic Hot/Cold. |
| **R1, R2** | $100\text{ k}\Omega, 1/4\text{ W}$ | Axial $1/4\text{ W}, 1\%$ | **B6**, **B7** | **D6**, **D7** | — | Mic Hot/Cold DC ground references. |
| **C4, C5** | $10\ \mu\text{F} / 50\text{ V}$ | Bi-Polar Radial Electrolytic | **B9**, **B10** | **D9**, **D10** | — | Non-polar input AC coupling. |
| **R3, R5** | $2.2\text{ k}\Omega, 1/4\text{ W}$ | Axial $0.1\%$ Precision | **B11**, **B13** | **D11**, **D13** | — | Diff receiver input resistors. |
| **R4, R6** | $4.7\text{ k}\Omega, 1/4\text{ W}$ | Axial $0.1\%$ Precision | **F11**, **B14** | **G11**, **D14** | — | Diff receiver reference & feedback. |
| **C3** | $100\text{ nF} / 50\text{ V}$| Monolithic Ceramic / Film | **E16** | **H16** | — | U1 supply decoupling (+15V to GND). |
| **C6** | $10\ \mu\text{F} / 25\text{ V}$ | Radial Polarized Electrolytic | **E18** ($+$) | **F18** ($-$) | — | Stage 1 to Stage 2 coupling. |
| **R10** | $1.2\text{ k}\Omega, 1/4\text{ W}$ | Axial $1/4\text{ W}, 1\%$ | **F19** | **G19** | — | Mic gain scaling resistor. |
| **R8** | $330\ \Omega, 1/4\text{ W}$ | Axial $1/4\text{ W}, 1\%$ | **F20** | **G20** | — | Mic minimum gain floor resistor. |
| **R7** | $47\text{ k}\Omega, 1/4\text{ W}$ | Axial $1/4\text{ W}, 1\%$ | **F21** | **G21** | — | Mic Stage 2 non-inverting bias. |
| **C7** | $10\ \mu\text{F} / 25\text{ V}$ | Radial Polarized Electrolytic | **G23** ($+$) | **H23** ($-$) | — | Mic Preamp output coupling. |
| **C10, C11**| $47\text{ pF} / 100\text{ V}$ | Disc Ceramic ($5\text{ mm}$) | **N4**, **N5** | **O4**, **O5** | — | RF filters across Line Hot/Cold. |
| **R12, R13**| $100\text{ k}\Omega, 1/4\text{ W}$ | Axial $1/4\text{ W}, 1\%$ | **M6**, **M7** | **O6**, **O7** | — | Line Hot/Cold DC ground references. |
| **C12, C13**| $1.0\ \mu\text{F} / 63\text{ V}$| Metallized Film (MKT) | **M9**, **M10** | **O9**, **O10** | — | Line input AC coupling capacitors. |
| **R14, R15**| $30\text{ k}\Omega, 1/4\text{ W}$ | Axial $0.1\%$ Precision | **M11**, **P11** | **O11**, **Q11** | — | Line diff receiver input resistors. |
| **R16, R17**| $10\text{ k}\Omega, 1/4\text{ W}$ | Axial $0.1\%$ Precision | **P13**, **P14** | **R13**, **R14** | — | Line diff receiver reference & feedback. |
| **C16** | $100\text{ nF} / 50\text{ V}$| Monolithic Ceramic / Film | **Q16** | **T16** | — | U2 supply decoupling (+15V to GND). |
| **C15** | $10\ \mu\text{F} / 25\text{ V}$ | Radial Polarized Electrolytic | **R18** ($+$) | **S18** ($-$) | — | Line receiver output coupling. |
| **C8, C9** | $68\text{ nF} / 63\text{ V}$ | Metallized Film (MKP/MKT) | **S19**, **S20** | **U19**, **U20** | — | Sallen-Key 60 Hz HPF capacitors. |
| **R9** | $27\text{ k}\Omega, 1/4\text{ W}$ | Axial $1/4\text{ W}, 1\%$ | **S21** | **U21** | — | Sallen-Key HPF feedback resistor. |
| **R11** | $56\text{ k}\Omega, 1/4\text{ W}$ | Axial $1/4\text{ W}, 1\%$ | **S22** | **U22** | — | Sallen-Key HPF reference to Vbias. |
| **C14** | $10\ \mu\text{F} / 25\text{ V}$ | Radial Polarized Electrolytic | **R24** ($+$) | **T24** ($-$) | — | HPF output coupling capacitor. |
| **R24** | $100\text{ k}\Omega, 1/4\text{ W}$ | Axial $1/4\text{ W}, 1\%$ | **R25** | **T25** | — | Master audio output pull-down. |

---

### Board C: Passive Speaker Filter ($5 \times 7\text{ cm}$)
*Scaled Diagram:* [`gate-e-board-c-assembly.svg`](file:///home/kawaiibuta/Projects/speaker-diy/projects/live-pa-system/gate-e-board-c-assembly.svg)

| RefDes | Value | Package / Footprint | Lead 1 Hole | Lead 2 Hole | Lead 3 / Extra | Orientation / Assembly Notes |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **TB_SPK_IN** | 2-Pin Screw Terminal | Pitch $5.08\text{ mm}$ | **B2** (PBTL +) | **C2** (PBTL -) | — | From TPA3255 PBTL output. **STRICTLY FLOATING.** |
| **TB_SPK_OUT**| 2-Pin Screw Terminal | Pitch $5.08\text{ mm}$ | **B23** (SPK +) | **C23** (SPK -) | — | To Visaton BG 20 loudspeaker. **STRICTLY FLOATING.** |
| **SW2** | SPST Slide / Toggle | Panel / Board | **B8** (Pole) | **C8** (Throw) | — | Contour bypass switch (bypasses RLC network). |
| **L1** | $1.0\text{ mH}$ Air Choke | Radial ($1.0\text{ mm}$ wire) | **G11** | **O11** | Zip-Ties at I11, M11 | Securely anchored through perfboard holes. |
| **C24** | $4.7\ \mu\text{F} / 250\text{ V}$| MKP Rectangular Film | **E17** | **I17** | — | Non-polar audio-grade capacitor. |
| **R23** | $8.2\ \Omega / 10\text{ W}$ | Non-Inductive Resistor | **E21** | **M21** | — | **Elevate 2 mm above board** for air cooling. |

---

## 3. High-Current & Safety Point-to-Point Wiring Schedule

### 18 AWG High-Current Silicone Wire Schedule
All connections carrying $\ge 1\text{ A}$ must use **18 AWG flexible stranded silicone wire** soldered directly into terminal blocks or lugs:

| From Point | To Point | Net Name | Wire Color | Max Current |
| :--- | :--- | :--- | :---: | :---: |
| **DC Barrel Jack J3 (Center Pin)** | **Panel Fuse Holder F1 (Pin 1)** | `DC_IN_RAW` | 18 AWG Red | 5.0 A DC |
| **Panel Fuse Holder F1 (Pin 2)** | **Board B TB_DC_IN (Pin 1)** | `DC_FUSE_OUT` | 18 AWG Red | 5.0 A DC |
| **DC Barrel Jack J3 (Outer Shell)** | **Board B TB_DC_IN (Pin 2)** | `GND` | 18 AWG Black | 5.0 A DC |
| **Board B TB_AMP_PWR (Pin 1)** | **TPA3255 Module DC+ Terminal** | `+36V` | 18 AWG Red | 5.0 A DC |
| **Board B TB_AMP_PWR (Pin 2)** | **TPA3255 Module DC- Terminal** | `GND` | 18 AWG Black | 5.0 A DC |
| **TPA3255 Speaker OUT+ Terminal** | **Board C TB_SPK_IN (Pin 1)** | `AMP_OUT_POS` | 18 AWG Orange | 3.6 A Audio (Floating) |
| **TPA3255 Speaker OUT- Terminal** | **Board C TB_SPK_IN (Pin 2)** | `AMP_OUT_NEG` | 18 AWG Blue | 3.6 A Audio (Floating) |
| **Board C TB_SPK_OUT (Pin 1)** | **Visaton BG 20 Positive (+) Terminal**| `SPK_OUT_POS` | 18 AWG Orange | 3.6 A Audio (Floating) |
| **Board C TB_SPK_OUT (Pin 2)** | **Visaton BG 20 Negative (-) Terminal**| `AMP_OUT_NEG` | 18 AWG Blue | 3.6 A Audio (Floating) |

---

## 4. Master 42-Net Point-to-Point Verification Checklist

Every single net from the authoritative KiCad schematic is itemized below for physical continuity inspection with a digital multimeter:

- [ ] **Net 1: `/+15V`** (14 nodes) — `U4:2`, `D2:2`, `D3:1`, `R19:1`, `C20:1`, `C21:1`, `R21:1`, `U3:8`, `C26:1`, `TB_PWR_OUT:1` $\to$ `TB_PWR:1` (Board A), `U1:8`, `U2:8`, `C3:1`, `C16:1`, `SW1:4`.
- [ ] **Net 2: `/+36V`** (7 nodes) — `Q1:3`, `D1:1`, `D2:1`, `C17:1`, `C18:1`, `U4:3`, `TB_AMP_PWR:1` $\to$ TPA3255 Power IN+.
- [ ] **Net 3: `/AMP_INPUT_SIG`** (3 nodes) — `C14:2`, `R24:1`, `TB_OUT:1` $\to$ TPA3255 Audio IN Pin 1.
- [ ] **Net 4: `/AMP_OUT_NEG`** (2 nodes) — `TB_SPK_IN:2` $\to$ `TB_SPK_OUT:2` $\to$ Visaton BG 20 (-). (Floating PBTL negative rail).
- [ ] **Net 5: `/AMP_OUT_POS`** (5 nodes) — `TB_SPK_IN:1`, `SW2:1`, `L1:1`, `C24:1`, `R23:1`.
- [ ] **Net 6: `/DC_FUSE_OUT`** (2 nodes) — Panel Fuse `F1:2` $\to$ `TB_DC_IN:1` $\to$ `Q1:2` (Drain).
- [ ] **Net 7: `/DC_IN_RAW`** (2 nodes) — DC Jack `J3:1` $\to$ Panel Fuse `F1:1`.
- [ ] **Net 8: `/GND`** (32 nodes) — Master Star Ground Bus across Board B and Board A.
- [ ] **Net 9: `/GND_CHASSIS`** (3 nodes) — `TB_MIC:1` (XLR Pin 1), `TB_LINE:1` (Combo Sleeve), `TB_OUT:3` (Cable Shield).
- [ ] **Net 10: `/HPF_MID_NODE`** (3 nodes) — `C8:2`, `C9:1`, `R9:2`.
- [ ] **Net 11: `/HPF_NONINV`** (3 nodes) — `C9:2`, `R11:1`, `U2:3`.
- [ ] **Net 12: `/HPF_OUT`** (4 nodes) — `U2:1`, `U2:2`, `R9:1`, `C14:1`.
- [ ] **Net 13: `/LINE_COLD_AC`** (2 nodes) — `C13:1`, `R15:2`.
- [ ] **Net 14: `/LINE_COLD_RAW`** (4 nodes) — `TB_LINE:3`, `C11:1`, `C13:2`, `R13:1`.
- [ ] **Net 15: `/LINE_HOT_AC`** (2 nodes) — `C12:2`, `R14:1`.
- [ ] **Net 16: `/LINE_HOT_RAW`** (4 nodes) — `TB_LINE:2`, `C10:2`, `C12:1`, `R12:2`.
- [ ] **Net 17: `/LINE_REC_INV`** (3 nodes) — `R15:1`, `R17:1`, `U2:6`.
- [ ] **Net 18: `/LINE_REC_NONINV`** (3 nodes) — `R14:2`, `R16:2`, `U2:5`.
- [ ] **Net 19: `/LINE_REC_OUT`** (3 nodes) — `U2:7`, `R17:2`, `C15:1`.
- [ ] **Net 20: `/LINE_VOL_POT_IN`** (2 nodes) — `C15:2`, `RV3:1` (CW).
- [ ] **Net 21: `/LM317_ADJ`** (5 nodes) — `U4:1`, `R19:2`, `R20:1`, `C19:1`, `D3:2`.
- [ ] **Net 22: `/MIC_COLD_AC`** (2 nodes) — `C5:1`, `R5:2`.
- [ ] **Net 23: `/MIC_COLD_RAW`** (4 nodes) — `TB_MIC:3`, `C2:1`, `C5:2`, `R2:1`.
- [ ] **Net 24: `/MIC_GAIN_POT_CW`** (2 nodes) — `R10:2`, `RV1:1` (CW).
- [ ] **Net 25: `/MIC_HOT_AC`** (2 nodes) — `C4:2`, `R3:1`.
- [ ] **Net 26: `/MIC_HOT_RAW`** (4 nodes) — `TB_MIC:2`, `C1:2`, `C4:1`, `R1:2`.
- [ ] **Net 27: `/MIC_PRE1_INV`** (3 nodes) — `U1:2`, `R5:1`, `R6:1`.
- [ ] **Net 28: `/MIC_PRE1_NONINV`** (3 nodes) — `U1:3`, `R3:2`, `R4:2`.
- [ ] **Net 29: `/MIC_PRE2_INV`** (3 nodes) — `U1:6`, `R8:1`, `R10:1`.
- [ ] **Net 30: `/MIC_PRE_OUT`** (4 nodes) — `U1:7`, `RV1:2`, `RV1:3`, `C7:1`.
- [ ] **Net 31: `/MIC_STG1_OUT`** (3 nodes) — `U1:1`, `R6:2`, `C6:1`.
- [ ] **Net 32: `/MIC_STG2_IN`** (3 nodes) — `C6:2`, `R7:1`, `U1:5`.
- [ ] **Net 33: `/MIC_VOL_POT_IN`** (2 nodes) — `C7:2`, `RV2:1` (CW).
- [ ] **Net 34: `/MODE_A_MIC_SIG`** (2 nodes) — `RV2:2` (Wiper), `SW1:1`.
- [ ] **Net 35: `/MODE_B_LINE_SIG`** (2 nodes) — `RV3:2` (Wiper), `SW1:3`.
- [ ] **Net 36: `/MODE_STATUS`** (2 nodes) — `SW1:5`, `TP1:1` (Hole V24).
- [ ] **Net 37: `/PMOS_GATE`** (3 nodes) — `Q1:1`, `D1:2`, `R18:1`.
- [ ] **Net 38: `/SELECTED_AUDIO`** (2 nodes) — `SW1:2` (Common Wiper), `C8:1` (HPF Input).
- [ ] **Net 39: `/SPARE_OUT`** (2 nodes) — `U3:6`, `U3:7` (Unused op-amp tied as unity-gain follower).
- [ ] **Net 40: `/SPK_OUT_POS`** (5 nodes) — `L1:2`, `C24:2`, `R23:2`, `SW2:2`, `TB_SPK_OUT:1`.
- [ ] **Net 41: `/VBIAS_7V5`** (10 nodes) — `U3:1`, `U3:2`, `U3:5`, `C23:1`, `C25:1`, `TB_PWR_OUT:3` $\to$ `TB_PWR:3` (Board A), `R4:1`, `R7:2`, `R8:2`, `R11:2`, `R16:1`.
- [ ] **Net 42: `/VBIAS_DIV`** (4 nodes) — `R21:2`, `R22:1`, `C22:1`, `U3:3`.

---

## 5. Professional Hand-Soldering & Perfboard Assembly Best Practices

1. **Machined DIP-8 Sockets Only:** Never solder the NE5532P op-amps directly to the perfboard. Solder the sockets first, verify all DC voltages at Pin 8 (+15V) and Pin 4 (GND) before inserting the ICs.
2. **Insulated Jumper Leads:** When crossing other traces or component leads on the bottom of the board, use stripped Teflon tubing, heat-shrink, or Kynar wire. Never leave long bare wire spans exposed.
3. **Elevated Power Resistors:** Resistor `R23` ($8.2\ \Omega / 10\text{ W}$) can become warm during extended high-volume testing. Elevate its ceramic body $2\text{ mm}$ above the surface of Board C to allow natural air convection.
4. **Mechanical Fastening for Inductor L1:** Do not rely solely on soldered copper wire to support `L1` ($1.0\text{ mH}$ air choke). Secure its body firmly against Board C using two nylon cable zip-ties through dedicated perfboard holes.
5. **LM317 Tab Clearance:** The metal mounting tab of `U4` sits at $+15\text{ V}$ DC. Ensure the heatsink has at least $3\text{ mm}$ air clearance and cannot pivot or touch any adjacent component leads.
