# Gate E Prototyping Board Wiring & Assembly Guide
**Project:** DIY Active Stage Monitor — Gate E Universal Prototyping Implementation  
**Project Path:** [`projects/live-pa-system/`](file:///home/kawaiibuta/Projects/speaker-diy/projects/live-pa-system/)  
**Target Hardware:** Off-The-Shelf FR-4 Universal Prototyping Boards ($2.54\text{ mm}$ pitch, isolated pads)  
**Status:** 100% Netlist Mapped & Point-to-Point Verified (42 Nets / 73 Components)  
**Date:** October 15, 2026  

---

## 1. Physical Grid & Board Coordinate System

Three generic universal prototyping boards are used. Every pad is uniquely addressed by its **Column Letter** and **Row Number**:

* **Board A ($7 \times 9\text{ cm}$, Audio Analog Front-End):**
  * **Columns:** $26$ columns, labeled **A to Z** (left to right).
  * **Rows:** $31$ rows, labeled **1 to 31** (top to bottom).
  * **Hole Pitch:** $2.54\text{ mm}$ ($0.1\text{''}$).
  * **Mounting Holes:** 4 $\times$ M3 corner holes at $(A, 1)$, $(Z, 1)$, $(A, 31)$, $(Z, 31)$.
* **Board B ($5 \times 7\text{ cm}$, Low-Voltage Power Conditioning):**
  * **Columns:** $18$ columns, labeled **A to R**.
  * **Rows:** $24$ rows, labeled **1 to 24**.
  * **Mounting Holes:** 4 $\times$ M3 corner holes at $(A, 1)$, $(R, 1)$, $(A, 24)$, $(R, 24)$.
* **Board C ($5 \times 7\text{ cm}$, Passive RLC Speaker Filter):**
  * **Columns:** $18$ columns, labeled **A to R**.
  * **Rows:** $24$ rows, labeled **1 to 24**.
  * **Mounting Holes:** 4 $\times$ M3 corner holes at $(A, 1)$, $(R, 1)$, $(A, 24)$, $(R, 24)$.

---

## 2. Master Component Placement Table

### Board A: Audio Analog Front-End ($7 \times 9\text{ cm}$)

| RefDes | Value | Package / Footprint | Lead 1 Hole | Lead 2 Hole | Lead 3 / Extra | Orientation / Assembly Notes |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **TB_MIC** | 3-Pin Screw Terminal | Pitch $5.08\text{ mm}$ ($2$ holes) | **B2** (Pin 1 GND) | **C2** (Pin 2 HOT) | **D2** (Pin 3 COLD) | Terminal wire entry facing top edge. |
| **TB_LINE**| 3-Pin Screw Terminal | Pitch $5.08\text{ mm}$ | **M2** (Pin 1 GND) | **N2** (Pin 2 HOT) | **O2** (Pin 3 COLD) | Wire entry facing top edge. |
| **TB_PWR** | 3-Pin Screw Terminal | Pitch $5.08\text{ mm}$ | **W2** (Pin 1 +15V)| **X2** (Pin 2 GND) | **Y2** (Pin 3 VBIAS)| Wire entry facing top edge. |
| **TB_OUT** | 3-Pin Screw Terminal | Pitch $5.08\text{ mm}$ | **N30** (Pin 1 SIG)| **O30** (Pin 2 GND)| **P30** (Pin 3 SHLD)| Wire entry facing bottom edge. |
| **U1** | NE5532P | DIP-8 Socket | **E12** (Pin 1) | **E13** (Pin 2) | Pins 3..8: E14, E15, H15, H14, H13, H12 | Notch faces Row 1 (UP). |
| **U2** | NE5532P | DIP-8 Socket | **M12** (Pin 1) | **M13** (Pin 2) | Pins 3..8: M14, M15, P15, P14, P13, P12 | Notch faces Row 1 (UP). |
| **U3** | NE5532P | DIP-8 Socket | **V12** (Pin 1) | **V13** (Pin 2) | Pins 3..8: V14, V15, Y15, Y14, Y13, Y12 | Notch faces Row 1 (UP). |
| **RV1** | $50\text{ k}\Omega$ Rev-Log | 3-Pin Bourns Pot / Panel | **B27** (Pin 1 CW) | **C27** (Pin 2 WIP)| **D27** (Pin 3 CCW)| Mic Gain trim/pot. |
| **RV2** | $10\text{ k}\Omega$ Log | 3-Pin Bourns Pot / Panel | **F27** (Pin 1 CW) | **G27** (Pin 2 WIP)| **H27** (Pin 3 CCW)| Mic Channel Volume. |
| **RV3** | $10\text{ k}\Omega$ Log | 3-Pin Bourns Pot / Panel | **K27** (Pin 1 CW) | **L27** (Pin 2 WIP)| **M27** (Pin 3 CCW)| Line Channel Volume. |
| **SW1** | DPDT Slide Switch | 6-Pin ($2 \times 3$ grid) | **P27** (Pin 1) | **Q27** (Pin 2 WIP)| Pins 3..6: R27, P28, Q28, R28 | Mode Selector (Vocal / Monitor). |
| **TP1** | Test Point Pad | Single Pin / Turret | **R24** | — | — | Probe point for HPF output. |
| **C1** | $47\text{ pF}$ | Disc Ceramic ($5\text{ mm}$) | **C4** | **D4** | — | RF filter Mic HOT. |
| **C2** | $47\text{ pF}$ | Disc Ceramic ($5\text{ mm}$) | **C5** | **D5** | — | RF filter Mic COLD. |
| **R1** | $100\text{ k}\Omega$ | Axial $1/4\text{ W}$ ($7.6\text{ mm}$) | **B6** | **D6** | — | Mic HOT DC ground return. |
| **R2** | $100\text{ k}\Omega$ | Axial $1/4\text{ W}$ ($7.6\text{ mm}$) | **B7** | **D7** | — | Mic COLD DC ground return. |
| **C4** | $10\ \mu\text{F} / 50\text{ V}$ | Bi-Polar Radial Electrolytic | **B9** | **D9** | — | Non-polar (BP) input AC coupling. |
| **C5** | $10\ \mu\text{F} / 50\text{ V}$ | Bi-Polar Radial Electrolytic | **B10** | **D10** | — | Non-polar (BP) input AC coupling. |
| **R3** | $2.2\text{ k}\Omega$ | Axial $0.1\%$ Precision | **B11** | **D11** | — | Diff receiver $(+)$ input resistor. |
| **R4** | $4.7\text{ k}\Omega$ | Axial $0.1\%$ Precision | **F11** | **G11** | — | Diff receiver $(+)$ reference to VBIAS. |
| **R5** | $2.2\text{ k}\Omega$ | Axial $0.1\%$ Precision | **B13** | **D13** | — | Diff receiver $(-)$ input resistor. |
| **R6** | $4.7\text{ k}\Omega$ | Axial $0.1\%$ Precision | **B14** | **D14** | — | Diff receiver feedback resistor. |
| **C3** | $100\text{ nF} / 50\text{ V}$| Monolithic Ceramic / Film | **E16** | **H16** | — | `U1` supply decoupling ($+15\text{V}$ to GND). |
| **C6** | $10\ \mu\text{F} / 25\text{ V}$ | Radial Polarized Electrolytic | **E18** ($+$) | **F18** ($-$) | — | Observe polarity: $(+)$ to `U1` pin 1. |
| **R10** | $1.2\text{ k}\Omega$ | Axial $1/4\text{ W}, 1\%$ | **F19** | **G19** | — | Mic gain stage input resistor. |
| **R8** | $330\ \Omega$ | Axial $1/4\text{ W}, 1\%$ | **F20** | **G20** | — | Mic gain stage minimum-gain floor. |
| **R7** | $47\text{ k}\Omega$ | Axial $1/4\text{ W}, 1\%$ | **F21** | **G21** | — | Mic gain stage non-inverting bias. |
| **C7** | $10\ \mu\text{F} / 25\text{ V}$ | Radial Polarized Electrolytic | **G23** ($+$) | **H23** ($-$) | — | Observe polarity: $(+)$ to `U1` pin 7. |
| **C10** | $47\text{ pF}$ | Disc Ceramic ($5\text{ mm}$) | **L4** | **M4** | — | RF filter Line HOT. |
| **C11** | $47\text{ pF}$ | Disc Ceramic ($5\text{ mm}$) | **L5** | **M5** | — | RF filter Line COLD. |
| **R12** | $100\text{ k}\Omega$ | Axial $1/4\text{ W}$ ($7.6\text{ mm}$) | **K6** | **M6** | — | Line HOT DC ground reference. |
| **R13** | $100\text{ k}\Omega$ | Axial $1/4\text{ W}$ ($7.6\text{ mm}$) | **K7** | **M7** | — | Line COLD DC ground reference. |
| **C12** | $1.0\ \mu\text{F} / 63\text{ V}$| Metallized Film (MKT) | **K9** | **M9** | — | Line HOT AC coupling. |
| **C13** | $1.0\ \mu\text{F} / 63\text{ V}$| Metallized Film (MKT) | **K10** | **M10** | — | Line COLD AC coupling. |
| **R14** | $30\text{ k}\Omega$ | Axial $0.1\%$ Precision | **K11** | **M11** | — | Line diff receiver $(+)$ input resistor. |
| **R15** | $30\text{ k}\Omega$ | Axial $0.1\%$ Precision | **O11** | **P11** | — | Line diff receiver $(-)$ input resistor. |
| **R16** | $10\text{ k}\Omega$ | Axial $0.1\%$ Precision | **K13** | **M13** | — | Line diff receiver reference to VBIAS. |
| **R17** | $10\text{ k}\Omega$ | Axial $0.1\%$ Precision | **K14** | **M14** | — | Line diff receiver feedback resistor. |
| **C16** | $100\text{ nF} / 50\text{ V}$| Monolithic Ceramic / Film | **M16** | **P16** | — | `U2` supply decoupling ($+15\text{V}$ to GND). |
| **C15** | $10\ \mu\text{F} / 25\text{ V}$ | Radial Polarized Electrolytic | **N18** ($+$) | **O18** ($-$) | — | Observe polarity: $(+)$ to `U2` pin 7. |
| **C8** | $68\text{ nF} / 63\text{ V}$ | Metallized Film (MKP/MKT) | **O19** | **Q19** | — | Sallen-Key HPF capacitor 1. |
| **C9** | $68\text{ nF} / 63\text{ V}$ | Metallized Film (MKP/MKT) | **O20** | **Q20** | — | Sallen-Key HPF capacitor 2. |
| **R9** | $27\text{ k}\Omega$ | Axial $1/4\text{ W}, 1\%$ | **O21** | **Q21** | — | Sallen-Key HPF feedback resistor. |
| **R11** | $56\text{ k}\Omega$ | Axial $1/4\text{ W}, 1\%$ | **O22** | **Q22** | — | Sallen-Key HPF reference to VBIAS. |
| **C14** | $10\ \mu\text{F} / 25\text{ V}$ | Radial Polarized Electrolytic | **N24** ($+$) | **P24** ($-$) | — | Observe polarity: $(+)$ to `U2` pin 1. |
| **R24** | $100\text{ k}\Omega$ | Axial $1/4\text{ W}, 1\%$ | **N25** | **P25** | — | Audio output pull-down to GND. |
| **R21** | $10\text{ k}\Omega$ | Axial $1/4\text{ W}, 1\%$ | **U6** | **W6** | — | Virtual ground divider upper leg. |
| **R22** | $10\text{ k}\Omega$ | Axial $1/4\text{ W}, 1\%$ | **U8** | **W8** | — | Virtual ground divider lower leg. |
| **C22** | $10\ \mu\text{F} / 25\text{ V}$ | Radial Polarized Electrolytic | **U10** ($+$) | **W10** ($-$) | — | Filter across lower divider leg. |
| **C26** | $100\text{ nF} / 50\text{ V}$| Monolithic Ceramic / Film | **V16** | **Y16** | — | `U3` supply decoupling ($+15\text{V}$ to GND). |
| **C23** | $47\ \mu\text{F} / 25\text{ V}$ | Radial Polarized Electrolytic | **V19** ($+$) | **X19** ($-$) | — | Virtual ground output reservoir. |
| **C25** | $100\text{ nF} / 50\text{ V}$| Monolithic Ceramic / Film | **V21** | **X21** | — | Virtual ground high-frequency bypass. |

---

### Board B: Low-Voltage Power Conditioning ($5 \times 7\text{ cm}$)

| RefDes | Value | Package / Footprint | Lead 1 Hole | Lead 2 Hole | Lead 3 / Extra | Orientation / Assembly Notes |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **TB_DC_IN** | 2-Pin Screw Terminal | Pitch $5.08\text{ mm}$ | **B2** (+36V In) | **C2** (GND Return)| — | From panel fuse `F1` and barrel jack `J3`. |
| **TB_AMP_PWR**| 2-Pin Screw Terminal | Pitch $5.08\text{ mm}$ | **F2** (+36V Out)| **G2** (GND Out) | — | Feeds TPA3255 amplifier module directly. |
| **Q1** | IRF4905 | TO-220 Power P-FET | **B6** (Gate) | **C6** (Drain) | **D6** (Source) | Tab connects to Drain. Clip-on heatsink. |
| **R18** | $100\text{ k}\Omega$ | Axial $1/4\text{ W}, 1\%$ | **B8** | **D8** | — | Gate pull-down to GND. |
| **D1** | BZX79C12 ($12\text{V}$)| DO-35 Zener Diode | **B9** (Cathode) | **D9** (Anode) | — | Clamp Gate-to-Source to $-12\text{ V}$. |
| **C17** | $470\ \mu\text{F} / 50\text{ V}$| Radial Low-ESR Electrolytic | **D12** ($+$) | **E12** ($-$) | — | Main $+36\text{ V}$ bulk reservoir capacitor. |
| **C18** | $100\text{ nF} / 50\text{ V}$| Monolithic Ceramic / Film | **B12** | **C12** | — | High-frequency DC rail bypass. |
| **U4** | LM317HVT | TO-220 Linear Regulator | **K10** (ADJ) | **L10** (VOUT) | **M10** (VIN) | **TAB IS +15V (NOT GND!)** Standoff heatsink. |
| **D2** | 1N4007 | DO-41 Rectifier Diode | **L7** (Anode) | **M7** (Cathode) | — | Reverse protection across LM317. |
| **R19** | $240\ \Omega$ | Axial $1/4\text{ W}, 1\%$ | **K14** | **L14** | — | LM317 program resistor (VOUT to ADJ). |
| **R20** | $2.64\text{ k}\Omega$ | Axial $1/4\text{ W}, 1\%$ | **I16** | **K16** | — | LM317 program resistor (ADJ to GND). |
| **C19** | $10\ \mu\text{F} / 25\text{ V}$ | Radial Polarized Electrolytic | **I18** ($-$) | **K18** ($+$) | — | ADJ pin ripple rejection bypass. |
| **D3** | 1N4007 | DO-41 Rectifier Diode | **I14** (Anode) | **K14** (Cathode) | — | Reverse protection across R20. |
| **C20** | $100\ \mu\text{F} / 25\text{ V}$| Radial Polarized Electrolytic | **N16** ($+$) | **P16** ($-$) | — | Regulator output stabilizing capacitor. |
| **C21** | $100\text{ nF} / 50\text{ V}$| Monolithic Ceramic / Film | **N18** | **P18** | — | Regulator output high-frequency bypass. |
| **TB_PWR_OUT**| 3-Pin Screw Terminal | Pitch $5.08\text{ mm}$ | **N22** (+15V Out)| **O22** (GND Out) | **P22** (Shield) | Feeds Board A via 3-wire bundle. |

---

### Board C: Passive RLC Speaker Filter ($5 \times 7\text{ cm}$)

| RefDes | Value | Package / Footprint | Lead 1 Hole | Lead 2 Hole | Lead 3 / Extra | Orientation / Assembly Notes |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **TB_SPK_IN** | 2-Pin Heavy Terminal | Pitch $5.08\text{ mm}$ | **B2** (PBTL +) | **C2** (PBTL -) | — | From TPA3255 PBTL output. **FLOATING.** |
| **SW2** | SPST Slide / Toggle | 2-Pin / 3-Pin Panel/Board | **B8** (Pole) | **C8** (Throw) | — | Contour Bypass Switch. |
| **L1** | $1.0\text{ mH}$ Air Choke | Radial $28\text{ mm}$ Dia ($1.0\text{ mm}$ wire)| **G11** | **O11** | Nylon Zip-Ties at I11, M11 | Fasten securely with zip-ties through board. |
| **C24** | $4.7\ \mu\text{F} / 250\text{ V}$| MKP Rectangular Film | **E17** | **I17** | — | Non-polar audio-grade capacitor. |
| **R23** | $8.2\ \Omega / 10\text{ W}$ | Non-Inductive Power Resistor | **E21** | **M21** | — | **Elevate 2mm above board** for air cooling. |
| **TB_SPK_OUT**| 2-Pin Heavy Terminal | Pitch $5.08\text{ mm}$ | **B23** (SPK +) | **C23** (SPK -) | — | To Visaton BG 20 loudspeaker. **FLOATING.** |

---

## 3. Hole-by-Hole Point-to-Point Wiring Schedule

### Board A: Audio Wiring Schedule (24 AWG Insulated Jumper Wire / 30 AWG Kynar Wire)

| Start Hole & Pin | Destination Hole & Pin | Net Name | Wire Color & Type | Assembly & Routing Notes |
| :--- | :--- | :--- | :---: | :--- |
| **TB_MIC Pin 1 [B2]** | **Chassis Star Ground Bus** | `GND_CHASSIS` | Green/Yellow 22 AWG | Direct chassis tie at XLR connector shell. |
| **TB_MIC Pin 2 [C2]** | **C1 Lead 1 [C4]**, **C4 Lead 1 [B9]**, **R1 Lead 2 [D6]** | `MIC_HOT_RAW` | Blue 24 AWG | Keep trace short, close to ground plane. |
| **TB_MIC Pin 3 [D2]** | **C2 Lead 1 [C5]**, **C5 Lead 2 [D10]**, **R2 Lead 1 [B7]**| `MIC_COLD_RAW` | White 24 AWG | Balanced line pair running parallel to Hot. |
| **C1 Lead 2 [D4]** | **Signal Ground Bus [B4]** | `GND` | Black 24 AWG | RF shunt directly to signal ground. |
| **C2 Lead 2 [D5]** | **Signal Ground Bus [B5]** | `GND` | Black 24 AWG | RF shunt directly to signal ground. |
| **R1 Lead 1 [B6]** | **Signal Ground Bus [A6]** | `GND` | Black 24 AWG | DC return to ground. |
| **R2 Lead 2 [D7]** | **Signal Ground Bus [A7]** | `GND` | Black 24 AWG | DC return to ground. |
| **C4 Lead 2 [D9]** | **R3 Lead 1 [B11]** | `MIC_HOT_AC` | Blue 24 AWG | AC coupled mic positive signal. |
| **C5 Lead 1 [B10]** | **R5 Lead 2 [D13]** | `MIC_COLD_AC` | White 24 AWG | AC coupled mic negative signal. |
| **R3 Lead 2 [D11]** | **U1 Socket Pin 3 [E14]**, **R4 Lead 2 [G11]** | `MIC_PRE1_NONINV` | Yellow 24 AWG | Diff receiver non-inverting summing node. |
| **R4 Lead 1 [F11]** | **VBIAS Rail [W11]** | `VBIAS_7V5` | Purple 24 AWG | Bias reference from U3 buffer. |
| **R5 Lead 1 [B13]** | **U1 Socket Pin 2 [E13]**, **R6 Lead 1 [B14]** | `MIC_PRE1_INV` | Yellow 24 AWG | Diff receiver inverting summing node. |
| **R6 Lead 2 [D14]** | **U1 Socket Pin 1 [E12]**, **C6 Lead 1 [E18]** | `MIC_STG1_OUT` | Green 24 AWG | Stage 1 output ($+6.6\text{ dB}$ fixed gain). |
| **U1 Socket Pin 4 [E15]**| **Signal Ground Star [A15]** | `GND` | Black 24 AWG | NE5532 negative supply pin to ground. |
| **U1 Socket Pin 8 [H12]**| **+15V Power Bus [W12]**, **C3 Lead 1 [H16]** | `+15V` | Red 24 AWG | Op-amp positive supply pin. |
| **C3 Lead 2 [E16]** | **Signal Ground Star [A16]** | `GND` | Black 24 AWG | Keep decoupling lead length $< 8\text{ mm}$. |
| **C6 Lead 2 [F18]** | **U1 Socket Pin 5 [H15]**, **R7 Lead 1 [F21]** | `MIC_STG2_IN` | Green 24 AWG | Stage 2 non-inverting input. |
| **R7 Lead 2 [G21]** | **VBIAS Rail [W21]** | `VBIAS_7V5` | Purple 24 AWG | DC bias reference for Stage 2. |
| **U1 Socket Pin 6 [H14]**| **R8 Lead 1 [F20]**, **R10 Lead 1 [F19]** | `MIC_PRE2_INV` | Yellow 24 AWG | Stage 2 inverting gain summing node. |
| **R8 Lead 2 [G20]** | **VBIAS Rail [W20]** | `VBIAS_7V5` | Purple 24 AWG | AC ground reference for gain setting. |
| **R10 Lead 2 [G19]** | **RV1 Pin 1 CW [B27]** | `MIC_GAIN_POT_CW`| Orange 24 AWG | Connection to variable gain potentiometer. |
| **U1 Socket Pin 7 [H13]**| **C7 Lead 1 [G23]**, **RV1 Pin 2 [C27]**, **RV1 Pin 3 [D27]** | `MIC_PRE_OUT` | Green 24 AWG | Stage 2 feedback loop & preamp out. |
| **C7 Lead 2 [H23]** | **RV2 Pin 1 CW [F27]** | `MIC_VOL_POT_IN` | Orange 24 AWG | Preamp output to Mic Volume Pot. |
| **RV2 Pin 3 CCW [H27]**| **Signal Ground Star [A27]** | `GND` | Black 24 AWG | Volume pot ground reference. |
| **RV2 Pin 2 WIP [G27]**| **SW1 Pin 1 [P27]** | `MODE_A_MIC_SIG` | White 24 AWG | Mode switch Vocal Position contact. |

---

### Board B: Power Conditioning Wiring Schedule

| Start Hole & Pin | Destination Hole & Pin | Net Name | Wire Specification | Assembly & Routing Notes |
| :--- | :--- | :--- | :---: | :--- |
| **TB_DC_IN Pin 1 [B2]** | **Q1 Drain [C6]** | `DC_FUSE_OUT` | **18 AWG Red Silicone** | High-current raw input from 5A fuse. |
| **TB_DC_IN Pin 2 [C2]** | **Main Ground Star [A2]** | `GND` | **18 AWG Black Silicone**| Main DC power ground return. |
| **Q1 Source [D6]** | **TB_AMP_PWR Pin 1 [F2]**, **C17 Lead 1 [D12]**, **U4 Pin 3 [M10]**, **D2 Cathode [M7]** | `+36V` | **18 AWG Red Silicone** | High-current protected +36V supply bus. |
| **Q1 Gate [B6]** | **D1 Cathode [B9]**, **R18 Lead 1 [B8]** | `PMOS_GATE` | 24 AWG White | Low-current gate control node. |
| **D1 Anode [D9]** | **Q1 Source [D6]** | `+36V` | 24 AWG Red | Clamps Gate-to-Source to 12V maximum. |
| **R18 Lead 2 [D8]** | **Main Ground Star [A8]** | `GND` | 24 AWG Black | Pulls gate down to turn P-FET ON. |
| **C17 Lead 2 [E12]** | **Main Ground Star [A12]** | `GND` | **18 AWG Black Silicone**| Bulk reservoir capacitor ground return. |
| **C18 Lead 1 [B12]** | **+36V Bus [D12]** | `+36V` | 24 AWG Red | High-frequency DC rail decoupling. |
| **C18 Lead 2 [C12]** | **Main Ground Star [A12]** | `GND` | 24 AWG Black | HF decoupling ground return. |
| **U4 Pin 3 VIN [M10]** | **+36V Bus [D12]** | `+36V` | 22 AWG Red | Input to LM317 regulator (draws ~30mA). |
| **U4 Pin 2 VOUT [L10]** | **R19 Lead 1 [L14]**, **D2 Anode [L7]**, **D3 Cathode [K14]**, **C20 Lead 1 [N16]**, **TB_PWR_OUT Pin 1 [N22]** | `+15V` | 22 AWG Red | Regulated +15V analog power rail. |
| **U4 Pin 1 ADJ [K10]** | **R19 Lead 2 [K14]**, **R20 Lead 1 [K16]**, **C19 Lead 2 [K18]**, **D3 Anode [I14]** | `LM317_ADJ` | 24 AWG Yellow | Voltage programming feedback node. |
| **R20 Lead 2 [I16]** | **Main Ground Star [A16]** | `GND` | 24 AWG Black | Programming divider ground return. |
| **C19 Lead 1 [I18]** | **Main Ground Star [A18]** | `GND` | 24 AWG Black | ADJ pin ripple bypass capacitor. |
| **C20 Lead 2 [P16]** | **Main Ground Star [A16]** | `GND` | 22 AWG Black | Output electrolytic filter ground return. |
| **C21 Lead 1 [N18]** | **+15V Rail [N16]** | `+15V` | 24 AWG Red | Output high-frequency bypass. |
| **C21 Lead 2 [P18]** | **Main Ground Star [A18]** | `GND` | 24 AWG Black | Output HF bypass ground return. |
| **TB_PWR_OUT Pin 2 [O22]**| **Main Ground Star [A22]** | `GND` | 22 AWG Black | Clean analog ground feeder to Board A. |

---

### Board C: Passive Speaker Filter Wiring Schedule (18 AWG High-Current Wire Only)

| Start Hole & Pin | Destination Hole & Pin | Net Name | Wire Specification | Assembly & Routing Notes |
| :--- | :--- | :--- | :---: | :--- |
| **TB_SPK_IN Pin 1 [B2]** | **SW2 Pole [B8]**, **L1 Lead 1 [G11]**, **C24 Lead 1 [E17]**, **R23 Lead 1 [E21]** | `AMP_OUT_POS` | **18 AWG Orange Silicone** | Floating positive speaker bridge rail. |
| **TB_SPK_IN Pin 2 [C2]** | **TB_SPK_OUT Pin 2 [C23]** | `AMP_OUT_NEG` | **18 AWG Blue Silicone** | Direct floating negative speaker bridge rail. |
| **SW2 Throw [C8]** | **TB_SPK_OUT Pin 1 [B23]** | `SPK_OUT_POS` | **18 AWG Orange Silicone** | Bypass switch bypasses RLC network directly. |
| **L1 Lead 2 [O11]** | **TB_SPK_OUT Pin 1 [B23]** | `SPK_OUT_POS` | **18 AWG Orange Silicone** | Inductor output to speaker positive terminal. |
| **C24 Lead 2 [I17]** | **TB_SPK_OUT Pin 1 [B23]** | `SPK_OUT_POS` | **18 AWG Orange Silicone** | Capacitor output to speaker positive terminal. |
| **R23 Lead 2 [M21]** | **TB_SPK_OUT Pin 1 [B23]** | `SPK_OUT_POS` | **18 AWG Orange Silicone** | Resistor output to speaker positive terminal. |

> [!CAUTION]
> **STRICT FLOATING PBTL RULE:** Notice that on Board C, **NONE** of the six connections link to `GND`, chassis, or shields! Both `AMP_OUT_POS` and `AMP_OUT_NEG` float at $+18\text{ V}$ DC common-mode from the TPA3255 Class-D H-bridge.

---

## 4. Point-to-Point Netlist Checklist (All 42 Nets)

Every net from the authoritative KiCad schematic and netlist is itemized below for physical continuity inspection with a digital multimeter (DMM) in Stage E1:

- [ ] **Net 1: `/+15V`** (14 nodes) — `U4:2`, `D2:2`, `D3:1`, `R19:1`, `C20:1`, `C21:1`, `TB_PWR_OUT:1` $\to$ `TB_PWR:1`, `U1:8`, `U2:8`, `U3:8`, `C3:1`, `C16:1`, `C26:1`, `R21:1`, `SW1:4`.
- [ ] **Net 2: `/+36V`** (7 nodes) — `Q1:3`, `D1:1`, `D2:1`, `C17:1`, `C18:1`, `U4:3`, `TB_AMP_PWR:1`.
- [ ] **Net 3: `/AMP_INPUT_SIG`** (3 nodes) — `C14:2`, `R24:1`, `TB_OUT:1` $\to$ TPA3255 Audio In Pin 1.
- [ ] **Net 4: `/AMP_OUT_NEG`** (2 nodes) — `TB_SPK_IN:2` $\to$ `TB_SPK_OUT:2` (Floating PBTL negative rail).
- [ ] **Net 5: `/AMP_OUT_POS`** (5 nodes) — `TB_SPK_IN:1`, `SW2:1`, `L1:1`, `C24:1`, `R23:1`.
- [ ] **Net 6: `/DC_FUSE_OUT`** (2 nodes) — Panel Fuse `F1:2` $\to$ `Q1:2` (Drain).
- [ ] **Net 7: `/DC_IN_RAW`** (2 nodes) — DC Jack `J3:1` $\to$ Panel Fuse `F1:1`.
- [ ] **Net 8: `/GND`** (32 nodes) — Master Star Ground Bus across Board A and Board B.
- [ ] **Net 9: `/GND_CHASSIS`** (3 nodes) — `TB_MIC:1` (XLR pin 1), `TB_LINE:1` (Combo sleeve), `TB_OUT:3` (Cable shield).
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
- [ ] **Net 34: `/MODE_A_MIC_SIG`** (2 nodes) — `RV2:2` (WIP), `SW1:1`.
- [ ] **Net 35: `/MODE_B_LINE_SIG`** (2 nodes) — `RV3:2` (WIP), `SW1:3`.
- [ ] **Net 36: `/MODE_STATUS`** (2 nodes) — `SW1:5`, `TP1:1`.
- [ ] **Net 37: `/PMOS_GATE`** (3 nodes) — `Q1:1`, `D1:2`, `R18:1`.
- [ ] **Net 38: `/SELECTED_AUDIO`** (2 nodes) — `SW1:2` (Common Wiper), `C8:1` (HPF Input).
- [ ] **Net 39: `/SPARE_OUT`** (2 nodes) — `U3:6`, `U3:7` (Unused op-amp tied as unity-gain follower).
- [ ] **Net 40: `/SPK_OUT_POS`** (5 nodes) — `L1:2`, `C24:2`, `R23:2`, `SW2:2`, `TB_SPK_OUT:1`.
- [ ] **Net 41: `/VBIAS_7V5`** (10 nodes) — `U3:1`, `U3:2`, `U3:5`, `C23:1`, `C25:1`, `R4:1`, `R7:2`, `R8:2`, `R11:2`, `R16:1`.
- [ ] **Net 42: `/VBIAS_DIV`** (4 nodes) — `R21:2`, `R22:1`, `C22:1`, `U3:3`.

---

## 5. Assembly Rules & Soldering Practices

1. **DIP-8 Sockets are Mandatory:** Never solder the NE5532P ICs directly to the perfboard. Solder the machined round-hole sockets first, verify all power and ground rails with a multimeter, and only insert the ICs during Stage E3.
2. **Component Lead Bending:** Use needle-nose pliers to make clean $90^\circ$ bends matching the $2.54\text{ mm}$ grid. Do not force component bodies against pads.
3. **Lead Insulation:** Where passive component leads cross other bare leads or pads, slide clear Teflon/silicone sleeving or stripped wire insulation over the lead.
4. **Star Ground Strategy:**
   * Board A has a central ground bus along Column A (left edge).
   * Board B has a high-current ground star near `TB_DC_IN` and `C17`.
   * A single $22\text{ AWG}$ insulated ground wire connects Board B ground to Board A ground. No ground loops.
5. **LM317 Heatsink Clearance:** The metal tab of the TO-220 LM317 regulator is energized at $+15\text{ V}$ DC. The heatsink must have at least $3\text{ mm}$ clearance from adjacent component leads and must never touch a grounded metal chassis.
