# DIY Active Stage Monitor Loudspeaker
### High-Efficiency, Low-Cost Active Wedge Monitor (Visaton BG 20 + TPA3255 PBTL)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![KiCad Version](https://img.shields.io/badge/KiCad-10.0-informational)](https://kicad.org)
[![SPICE Simulation](https://img.shields.io/badge/ngspice-Verified-success)](projects/live-pa-system/simulation/)
[![Budget](https://img.shields.io/badge/Budget-%3C%205%2C000%2C000%20VND-brightgreen)](#bill-of-materials--financial-dashboard)

A complete, open-hardware engineering design for a **DIY Active Stage Monitor Loudspeaker** optimized for live vocal and acoustic guitar performance at indoor venues (1–2 m listening distance). 

The design combines an ultra-efficient 8-inch full-range transducer with an analog front-end, active excursion protection, a commercial high-efficiency Class-D power amplifier, and a modular home-buildable prototyping architecture.

---

## Key System Specifications

| Parameter | Specification | Engineering Details & Rationale |
| :--- | :--- | :--- |
| **Acoustic Transducer** | Visaton BG 20 ($8\ \Omega$) | 8-inch full-range driver with whizzer cone, $92\text{ dB/W/m}$ sensitivity, $f_s = 38\text{ Hz}$. |
| **Linear Excursion Limit** | $\pm 2.0\text{ mm}$ ($X_{\text{max}}$) | Voice coil height $8\text{ mm}$, pole plate $4\text{ mm}$; continuous drive policy strictly capped at **10.0 W RMS** to prevent bottoming out. |
| **Continuous SPL Target** | $\ge 102\text{ dB}$ SPL @ 1 m ($96\text{ dB}$ @ 2 m) | Achieved cleanly at 10 W RMS without driver power compression or thermal stress. |
| **Power Amplifier** | Wuzhi ZK-3002 (TPA3255) | Preassembled Class-D module configured in **Parallel Bridge-Tied Load (PBTL)** mono. |
| **External Power Supply** | $36\text{ V} / 5\text{ A}$ ($180\text{ W}$) | Off-the-shelf regulated switch-mode DC adapter; low voltage entry into cabinet for safety. |
| **Reverse Polarity Protection**| IRF4905 P-MOSFET + 12V Zener | Forward drop $\le 25\text{ mV}$ ($0.5\text{ W}$ dissipation at 5A); blocks reverse DC up to $-55\text{ V}$ with zero leakage. |
| **Analog Power Rail** | $+15.0\text{ V}$ DC Linear Regulated | LM317HVT linear regulator ($V_{\text{in}} \le 60\text{ V}$) with diode protection and ripple rejection. |
| **Virtual Ground Rail** | $+7.50\text{ V}$ Active Buffer | Precision $10\text{ k}\Omega$ divider actively buffered by NE5532P op-amp follower. |
| **Microphone Preamplifier** | Gain $+20.0\text{ dB} \sim +50.5\text{ dB}$ | Balanced difference receiver ($U_{1\text{A}}$) + non-inverting gain stage ($U_{1\text{B}}$), $\ge 50\text{ dB}$ discrete CMRR. |
| **Line Differential Receiver**| Gain $-9.54\text{ dB}$ ($A_d = 0.333$) | Balanced difference receiver ($U_{2\text{B}}$) accepting $+4\text{ dBu}$ nominal with clean $+22\text{ dBu}$ headroom. |
| **Mode Switching** | DPDT Mechanical Selector | **Mode A:** Standalone Vocal (Mic Preamp active).<br>**Mode B:** Mixer Monitor (Line In active). |
| **Common Driver Protection** | 60 Hz 2nd-order Sallen-Key HPF | Butterworth $Q = 0.707$, $-3.0\text{ dB}$ @ $60\text{ Hz}$, $\ge 15.3\text{ dB}$ attenuation at 25 Hz. **Protects both Mic and Line paths.** |
| **Passive Contour Network** | Switchable RLC Filter | $1.0\text{ mH}$ air choke, $4.7\ \mu\text{F}$ MKP cap, $8.2\ \Omega / 10\text{ W}$ resistor. $-4.5\text{ dB}$ dip @ 1.5–2.5 kHz to tame whizzer cone. |
| **Enclosure** | 25 L Net Stage Wedge | 15 mm MDF, $45^\circ$ monitor angle, bass-reflex port tuned to $F_b = 50.0\text{ Hz} \pm 2\text{ Hz}$ (PVC tube $60\text{ mm}$ ID $\times 91.2\text{ mm}$). |
| **Total Weight & Budget** | $< 15\text{ kg}$, $< 5,000,000\text{ VND}$ | Estimated finished weight: $\approx 11.5\text{ kg}$; estimated total BOM: $\approx 3,725,000\text{ VND}$. |

---

## System Architecture

```
                                  +---------------------------------------------+
                                  | 36V 5A External DC Power Adapter (Switching)|
                                  +---------------------------------------------+
                                                         | (DC Barrel Jack J3)
                                                         v
                                  +---------------------------------------------+
                                  | Panel Fuse F1 (5x20mm 4A-T Cartridge)       |
                                  +---------------------------------------------+
                                                         | [18 AWG Red Silicone]
                                                         v
                                  +---------------------------------------------+
                                  | BOARD B: Power Conditioning (5x7 cm)        |
                                  | - Q1: IRF4905 P-FET Reverse Polarity Protect|
                                  | - C17: 470uF/50V Bulk Reservoir Capacitor   |
                                  | - U4: LM317HVT Linear Regulator (+15V Out)  |
                                  | - U3: NE5532P Active Virtual Ground (+7.5V) |
                                  +---------------------------------------------+
                                        |                             |
                   [18 AWG Heavy DC]    |                             | [22 AWG +15V, +7.5V, GND]
                   +36V & Power GND     |                             | Clean Analog Rails
                                        v                             v
+---------------------------------------------+         +---------------------------------------------+
| Wuzhi ZK-3002 (TPA3255 PBTL Mono Amplifier) |         | BOARD A: Analog Audio Front-End (7x9 cm)    |
| - High-current Class-D switching module     |         | - U1: NE5532P (Mic Preamp, Gain +20..+50dB) |
| - External preassembled heatsink & caps     |         | - U2: NE5532P (Line Rec -9.5dB, 60Hz HPF)   |
| - PBTL Mode: Pin 1 IN+ (Sig), Pin 2 IN- (GND)|         | - Inputs: XLR J1 (Mic), Combo J2 (Line)     |
+---------------------------------------------+         | - Controls: RV1 Gain, RV2/RV3 Vol, SW1 Mode |
        |                      ^                        +---------------------------------------------+
        | Floating PBTL        | Shielded Audio Coax                          |
        | Speaker Audio        | J5 Pin 1 Sig / Pin 2 GND                     |
        | [18 AWG Orange/Blue] +----------------------------------------------+
        v
+---------------------------------------------+
| BOARD C: Passive Speaker Filter (5x7 cm)    |
| - L1: 1.0 mH Air-Core Choke (1.0mm wire)    |
| - R23: 8.2 Ohm 10W Non-Inductive Resistor   |
| - C24: 4.7 uF 250V MKP Film Capacitor       |
| - SW2: Heavy-Duty SPST Contour Bypass Switch|
| * STRICT RULE: ZERO GROUND CONNECTIONS!     |
+---------------------------------------------+
        |
        | [18 AWG Direct Speaker Leads]
        v
+---------------------------------------------+
| Transducer: Visaton BG 20 (8 Ohm, 8-inch)   |
| Continuous Power Limit: 10.0 W RMS          |
| Enclosure: 25 L Net MDF Wedge (Fb = 50 Hz)  |
+---------------------------------------------+
```

---

## Modular Hardware Implementation

This project is specifically designed to be **built at home without custom PCB manufacturing, CNC milling, or chemical etching**.

All circuits are partitioned across standard **FR-4 double-sided universal prototyping boards ($2.54\text{ mm}$ pitch, isolated tinned pads)**:

### 1. Board B — Power Conditioning & +7.5V Bias Reference ($5 \times 7\text{ cm}$)
- **Dimensions:** 18 Columns (A–R) $\times$ 24 Rows (1–24).
- **Functions:** IRF4905 P-FET reverse-polarity protection, LM317HVT $+15.0\text{ V}$ linear regulator, and NE5532P active buffer producing low-impedance $+7.50\text{ V}$ virtual ground.
- **Assembly Guide:** [`gate-e-board-b-assembly.svg`](projects/live-pa-system/gate-e-board-b-assembly.svg)

### 2. Board A — Audio Analog Front-End ($7 \times 9\text{ cm}$)
- **Dimensions:** 26 Columns (A–Z) $\times$ 31 Rows (1–31).
- **Functions:**
  - **Zone 1 (Left):** Balanced Microphone Differential Preamp (U1, XLR J1, RV1 Gain pot, RV2 Volume pot).
  - **Zone 2 (Right):** Balanced Line Receiver (U2B, Combo J2, RV3 Line pot), Mode Selector Switch (SW1), and Master 60 Hz 2nd-order Sallen-Key HPF (U2A).
- **Assembly Guide:** [`gate-e-board-a-assembly.svg`](projects/live-pa-system/gate-e-board-a-assembly.svg)

### 3. Board C — Passive Speaker Filter ($5 \times 7\text{ cm}$)
- **Dimensions:** 18 Columns (A–R) $\times$ 24 Rows (1–24).
- **Functions:** Heavy-duty RLC contour notch network ($1.0\text{ mH}$, $4.7\ \mu\text{F}$, $8.2\ \Omega / 10\text{ W}$) with bypass switch (SW2).
- **CRITICAL SAFETY RULE:** **ZERO ground connections.** Both PBTL speaker outputs float at $+18.0\text{ V}$ DC half-supply.
- **Assembly Guide:** [`gate-e-board-c-assembly.svg`](projects/live-pa-system/gate-e-board-c-assembly.svg)

---

## Phased Procurement & Verification Plan

Procurement and hardware testing follow a strict **7-stage gated workflow**. No downstream components are purchased until the preceding subsystem is tested and confirmed passed:

```
+========================================================================================================================+
| BATCH | SUBSYSTEM DESCRIPTION              | ESTIMATED COST   | CUMULATIVE   | REMAINING BUDGET | GATE STATUS          |
+========================================================================================================================+
| B-0   | Tools & Construction Consumables   |      180,000 VND |  180,000 VND |    4,820,000 VND | READY (ACTIVE)       |
| B-1   | Board B: Power & +7.5V Bias Buffer |      195,000 VND |  375,000 VND |    4,625,000 VND | READY (ACTIVE)       |
| B-2   | Board A (Zone 1): Mic Preamp       |      140,000 VND |  515,000 VND |    4,485,000 VND | BLOCKED (Wait Gate 1)|
| B-3   | Board A (Zone 2): Line Rec & HPF   |      150,000 VND |  665,000 VND |    4,335,000 VND | BLOCKED (Wait Gate 2)|
| B-4   | TPA3255 Amp, 36V PSU & Dummy Load  |      800,000 VND | 1,465,000 VND|    3,535,000 VND | BLOCKED (Wait Gate 3)|
| B-5   | Visaton BG 20 & 25L MDF Enclosure  |    1,860,000 VND | 3,325,000 VND|    1,675,000 VND | BLOCKED (Wait Gate 4)|
| B-6   | Board C: RLC Contour & Finishing   |      400,000 VND | 3,725,000 VND|    1,275,000 VND | BLOCKED (Wait Gate 5)|
+========================================================================================================================+
| TOTAL ESTIMATED PROJECT INVESTMENT: 3,725,000 VND | HARD BUDGET LIMIT: 5,000,000 VND | CONTINGENCY RESERVE: +1,275,000 VND     |
+========================================================================================================================+
```

For detailed purchasing checklists and Vietnamese search keywords for Shopee/Lazada/Thegioiic, see [`gate-e-phased-shopping-plan.md`](projects/live-pa-system/gate-e-phased-shopping-plan.md).

---

## Project Directory Structure

```
speaker-diy/
├── README.md                                 # Project overview, specifications, and quickstart
├── .gitignore                                # KiCad, Python, and OS ignore patterns
├── projects/
│   └── live-pa-system/                       # Primary active monitor engineering project
│       ├── live-pa-system.kicad_sch          # Authoritative KiCad 10 schematic (42 nets, 73 components)
│       ├── live-pa-system.net                # Exported netlist
│       ├── live-pa-system.cir                # SPICE netlist for ngspice verification
│       ├── live-pa-system.kicad_pro          # KiCad project file
│       ├── gate-d-design-report.md           # Gate D engineering report & simulation audit
│       ├── gate-e-phased-shopping-plan.md    # Phased 7-batch procurement & testing plan
│       ├── gate-e-bench-testing-plan.md      # Detailed bench testing, thermal & acoustic test plan
│       ├── gate-e-protoboard-wiring.md       # Master hole-by-hole point-to-point wiring schedule
│       ├── gate-e-board-a-assembly.svg       # Scaled assembly diagram: Board A (Audio Front-End)
│       ├── gate-e-board-b-assembly.svg       # Scaled assembly diagram: Board B (Power & Bias Buffer)
│       ├── gate-e-board-c-assembly.svg       # Scaled assembly diagram: Board C (Passive RLC Filter)
│       ├── gate-e-system-wiring-diagram.svg  # Overall system interconnect wiring diagram
│       └── simulation/                       # ngspice dedicated testbenches and simulation logs
└── .agents/                                  # Specialized electronics and speaker design agent skills
```

---

## Critical Safety & Bring-Up Rules

> [!CAUTION]
> 1. **Current-Limited Power-Up:** Never connect newly assembled prototype boards directly to an unrestricted battery or power supply. Use a bench supply with current limit set to $100\text{ mA}$, or insert a **$100\ \Omega / 10\text{ W}$ power resistor** in series with the $+36\text{ V}$ adapter lead during initial bring-up to clamp short-circuit fault current to $\le 360\text{ mA}$.
> 2. **Floating PBTL Speaker Bridge Outputs:** The Wuzhi ZK-3002 / TPA3255 PBTL output operates as an active H-bridge. **Both output terminals float at $+18.0\text{ V}$ DC half-supply.** Never connect either speaker output to signal ground, chassis ground, or an oscilloscope ground clip!
> 3. **LM317HVT Heatsink Tab Isolation:** The TO-220 metal mounting tab of `U4` is internally connected to **Pin 2 (Output, $+15\text{ V}$)**, NOT ground! The heatsink must remain electrically floating with $\ge 3\text{ mm}$ clearance from adjacent components and chassis ground.
> 4. **18 AWG Direct Power Wiring:** 36V 5A DC power and speaker audio lines must never run over thin perfboard copper foil. Use direct, insulated **18 AWG stranded silicone wire**.

---

## License

This project is licensed under the [MIT License](LICENSE) — hardware schematics, wiring schedules, and documentation are provided openly for DIY audio enthusiasts and educational purposes.
