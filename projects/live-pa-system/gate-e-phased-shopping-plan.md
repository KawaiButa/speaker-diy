# GATE E — PHASED PROCUREMENT, MODULAR ASSEMBLY & VERIFICATION PLAN
## DIY Active Stage Monitor Loudspeaker (Visaton BG 20 + TPA3255 PBTL)

**Document:** Phased Procurement, Subsystem Assembly, and Gated Verification Plan  
**Project Path:** [`projects/live-pa-system/`](file:///home/kawaiibuta/Projects/speaker-diy/projects/live-pa-system/)  
**Baseline Circuit:** 100% Verified Gate D Schematic (`live-pa-system.kicad_sch`, 42 nets, 73 components)  
**Budget Ceiling:** Strictly $< 5,000,000\text{ VND}$ (Tracked Cumulative)  
**Status:** Authorized — Phased Execution Active  
**Date:** October 15, 2026  
**Revision:** 2.0 (Phased Modular Prototyping Baseline)  

---

## 1. Phased Engineering Philosophy

To eliminate financial risk and prevent unverified error propagation, this plan enforces **Staged Procurement**:
1. **Zero Upfront Bulk Buying:** The bill of materials is partitioned into 7 sequential batches (Batch 0 to Batch 6). Components for a downstream stage are purchased **only after** the current stage is physically assembled, tested, recorded, and signed off.
2. **Subsystem Isolation:** Each batch forms an electrically self-contained, testable block.
3. **No Custom PCB:** All electronics are assembled on generic, off-the-shelf FR-4 double-sided prototyping boards ($2.54\text{ mm}$ hole pitch, isolated tinned pads).
4. **Strict High-Current Separation:** High-current 36V DC (5A) and floating PBTL speaker audio lines (3.6A) are direct-wired with **18 AWG stranded silicone wire** and never run over thin perfboard pads.
5. **Zero Ground on Speaker Network:** The TPA3255 operates in PBTL mono; both speaker terminals float at $+18\text{ V}$ DC. The passive contour board (Board C) contains **zero ground connections**.

---

## 2. Master Phased Status & Cost Tracking Dashboard

```
+========================================================================================================================+
| BATCH | SUBSYSTEM DESCRIPTION              | BATCH COST (VND) | SHIPPING | CUMULATIVE (VND) | REMAINING BUDGET | STATUS    |
+========================================================================================================================+
| B-0   | Tools & Construction Consumables   |      155,000     |  25,000  |     180,000      |    4,820,000     | READY     |
| B-1   | Board B: Power & +7.5V Bias Buffer |      170,000     |  25,000  |     375,000      |    4,625,000     | READY     |
| B-2   | Board A (Zone 1): Mic Preamp       |      115,000     |  25,000  |     515,000      |    4,485,000     | BLOCKED   |
| B-3   | Board A (Zone 2): Line Rec & HPF   |      125,000     |  25,000  |     665,000      |    4,335,000     | BLOCKED   |
| B-4   | TPA3255 Amp, 36V PSU & Dummy Load  |      765,000     |  35,000  |   1,465,000      |    3,535,000     | BLOCKED   |
| B-5   | Visaton BG 20 & 25L MDF Enclosure  |    1,800,000     |  60,000  |   3,325,000      |    1,675,000     | BLOCKED   |
| B-6   | Board C: RLC Contour & Finishing   |      370,000     |  30,000  |   3,725,000      |    1,275,000     | BLOCKED   |
+========================================================================================================================+
| TOTAL ESTIMATED PROJECT EXPENDITURE:                                     3,725,000 VND                          |
| HARD MANDATORY BUDGET CEILING:                                           5,000,000 VND                          |
| FINAL CONTINGENCY RESERVE:                                              +1,275,000 VND                          |
+========================================================================================================================+
```

*Note on Status Definitions:*
- **READY:** Actionable immediately. User may procure parts and execute assembly/testing.
- **BLOCKED:** Downstream dependency. Strictly forbidden to order parts until preceding stage gate is verified and passed.
- **PASS:** Physical measurements verified against acceptance bounds.

---

## 3. Detailed Batch Specifications & Test Gates

---

### BATCH 0 — Tools, Laboratory Fixtures & Construction Consumables

#### 1. Purpose
Establish the physical workspace, safety fixtures, and reusable construction hardware required to assemble and test the monitor without damaging sensitive semiconductors or exceeding the project budget.

#### 2. Itemized Equipment & Supplies

##### A. Reusable Tools (Tracked in Separate Workshop Tools Budget — Excluded from 5M VND Speaker BOM)
| Tool / Instrument | Specification | Essential / Optional | Sourcing / Alternatives | Est. Cost (VND) |
| :--- | :--- | :---: | :--- | :---: |
| **Digital Multimeter (DMM)** | True-RMS, DC/AC Volts, Resistance, Continuity beeper | **Essential** | Own or borrow (e.g. Fluke, Victor, Zoyi) | 0 (Owned/Borrowed) |
| **Soldering Station / Iron** | $40\text{ W} \sim 60\text{ W}$, adjustable temperature ($300\sim 350^\circ\text{C}$) | **Essential** | Own or borrow (T12, 936 clone) | 0 (Owned/Borrowed) |
| **Hand Tools** | Flush micro-cutters, needle-nose pliers, wire stripper ($18\sim 28\text{ AWG}$) | **Essential** | Standard hobbyist toolbox | 0 (Owned/Borrowed) |
| **Current-Limited Bench Supply** | $0 \sim 36\text{ V}$ adjustable, $0 \sim 1\text{ A}$ current limiting | Strongly Preferred | Borrow at lab/makerspace **OR use Safe Alternative below** | 0 (Borrowed) |
| **Safe Bench Supply Alternative** | **$100\ \Omega / 10\text{ W}$ Wirewound Power Resistor** in series with 36V adapter | **Essential if no lab supply** | Purchased in Batch 0/1 (~10,000 VND). Clamps fault current to $\le 360\text{ mA}$. | 10,000 |
| **Audio Signal Generator** | $20\text{ Hz} \sim 20\text{ kHz}$ low-distortion sine source | **Essential for Stage 2/3** | **Zero-cost:** Smartphone / PC with 3.5mm jack + free app (REW) | 0 |
| **Oscilloscope** | Dual-channel $\ge 20\text{ MHz}$, AC/DC coupling | Essential for Stage 2/3/4 | Borrow bench time OR use inexpensive pocket DSO / USB scope | 0 (Borrowed) |

##### B. Consumable Construction Hardware (Included in Speaker Project Budget)
| Item | Exact Specification | Qty | Purpose | Est. Cost (VND) |
| :--- | :--- | :---: | :--- | :---: |
| **Perfboard A** | $7 \times 9\text{ cm}$ FR-4 double-sided, $2.54\text{ mm}$ pitch, isolated pads | 1 pc | Audio front-end board | 22,000 |
| **Perfboard B & C**| $5 \times 7\text{ cm}$ FR-4 double-sided, $2.54\text{ mm}$ pitch, isolated pads | 2 pcs | Power board (B) & Speaker filter (C) | 24,000 |
| **DIP-8 Sockets** | 8-pin machined round-hole tulip contacts (gold/tin plated) | 3 pcs | Op-amp sockets (U1, U2, U3) | 9,000 |
| **Screw Terminals** | $5.08\text{ mm}$ pitch 2-Pin (6 pcs) and 3-Pin (3 pcs) | 9 pcs | All board inputs, outputs, power | 30,000 |
| **Silicone Hookup Wire** | 18 AWG flexible stranded silicone wire (Red, Black, Blue, Orange) | 3 m | 36V 5A DC & floating PBTL speaker | 35,000 |
| **Jumper Wire** | 24 AWG solid tinned copper wire / insulated hookup wire | 5 m | On-board perfboard jumper links | 15,000 |
| **M3 Standoff Kit** | M3 $\times 10\text{ mm}$ nylon/brass hex standoffs + screws & nuts (pack of 20)| 1 pk | Board mounting | 20,000 |
| **Subtotal Batch 0** | **Consumable Construction Materials** | — | — | **155,000 VND** |

#### 3. Financial Tracking
- Batch 0 Materials Cost: **155,000 VND**
- Shipping: **25,000 VND**
- Cumulative Expenditure: **180,000 VND**
- Remaining Budget: **4,820,000 VND**

#### 4. Gate 0 Sign-Off Criteria
- [ ] DMM verified operational (fresh battery, test leads $< 0.2\ \Omega$ on short).
- [ ] Soldering iron, flux, and solder wire on hand.
- [ ] Safe Current-Limiting fixture ($100\ \Omega / 10\text{ W}$ resistor or lab supply) confirmed.
- [ ] Prototyping boards and hardware received and inspected.

---

### BATCH 1 — Board B: Power Conditioning & +7.5V Active Bias Buffer

#### 1. Purpose
Assemble and verify the complete power distribution and biasing subsystem on **Board B ($5 \times 7\text{ cm}$)**:
1. Reverse-polarity protection via P-MOSFET `Q1` (IRF4905) and gate clamp `D1` (12V Zener).
2. Raw DC fuse and filtering via `F1`, `C17` ($470\ \mu\text{F}$), `C18` ($100\text{ nF}$).
3. Linear $+15.0\text{ V}$ regulated rail via `U4` (LM317HVT), `D2`, `D3`, `R19`, `R20`, `C19`, `C20`, `C21`.
4. Low-noise $+7.50\text{ V}$ virtual ground generation and active buffering via `R21`, `R22`, `C22`, `U3` (NE5532P), `C23`, `C25`, `C26`.

#### 2. Exact Component Purchase List (Batch 1 Only)
| RefDes | Component Specification | Package | Qty | Vietnamese Search Keywords | Est. Cost (VND) |
| :--- | :--- | :---: | :---: | :--- | :---: |
| **Q1** | IRF4905 ($-55\text{ V}, -74\text{ A}, 20\text{ m}\Omega$ P-FET) | TO-220 | 1 | `mosfet irf4905 to-220` | 28,000 |
| **D1** | BZX79C12 ($12\text{ V} / 0.5\text{ W}$ Zener diode) | DO-35 | 1 | `diode zener 12v 0.5w` | 2,000 |
| **R18** | $100\text{ k}\Omega \pm 1\%, 1/4\text{ W}$ metal film resistor | Axial | 1 | `điện trở 100k 1/4w 1%` | 500 |
| **C17** | $470\ \mu\text{F} / 50\text{ V}$ Low-ESR $105^\circ\text{C}$ electrolytic | Radial | 1 | `tụ hóa 470uf 50v low esr` | 12,000 |
| **C18, C21, C25, C26**| $100\text{ nF} / 50\text{ V}$ monolithic ceramic / film | Radial | 4 | `tụ gốm 100nf 50v`, `tụ 104` | 6,000 |
| **U4** | LM317HVT ($V_{\text{in}} \le 60\text{ V}$ linear regulator) | TO-220 | 1 | `lm317hvt to-220`, `lm317hv` | 25,000 |
| **D2, D3** | 1N4007 ($1000\text{ V} / 1\text{ A}$ rectifier diode) | DO-41 | 2 | `diode 1n4007` | 2,000 |
| **R19** | $240\ \Omega \pm 1\%, 1/4\text{ W}$ metal film resistor | Axial | 1 | `điện trở 240 ôm 1% 1/4w` | 500 |
| **R20** | $2.64\text{ k}\Omega \pm 1\%$ ($2.4\text{k} + 240\Omega$ in series) | Axial | 2 | `điện trở 2.4k 1%`, `240 ôm` | 1,000 |
| **C19, C22** | $10\ \mu\text{F} / 25\text{ V}$ radial electrolytic | Radial | 2 | `tụ hóa 10uf 25v` | 4,000 |
| **C20** | $100\ \mu\text{F} / 25\text{ V}$ radial electrolytic | Radial | 1 | `tụ hóa 100uf 25v` | 3,000 |
| **R21, R22** | $10\text{ k}\Omega \pm 1\%, 1/4\text{ W}$ metal film resistor | Axial | 2 | `điện trở 10k 1% 1/4w` | 1,000 |
| **U3** | NE5532P dual low-noise op-amp (TI) | DIP-8 | 1 | `ic ne5532p ti dip-8` | 15,000 |
| **C23** | $47\ \mu\text{F} / 25\text{ V}$ radial electrolytic | Radial | 1 | `tụ hóa 47uf 25v` | 2,500 |
| **Heatsinks** | Aluminum clip-on heatsink ($\le 20^\circ\text{C/W}$) for U4 & Q1 | TO-220 | 2 | `tản nhiệt nhôm to-220` | 15,000 |
| **Fuse & Jack**| Panel fuse holder 5x20mm + 4A-T fuse + 5.5x2.1mm DC jack | Panel | 1 set | `đế cầu chì 5x20`, `jack dc 5.5x2.1` | 42,000 |
| **Subtotal B1** | **Batch 1 Components** | — | — | — | **170,000 VND** |

#### 3. Financial Tracking
- Batch 1 Cost: **170,000 VND**
- Shipping: **25,000 VND**
- Cumulative Expenditure: **375,000 VND**
- Remaining Budget: **4,625,000 VND**

#### 4. Board B Component Placement & Coordinate Map ($5 \times 7\text{ cm}$, 18 Cols A–R × 24 Rows 1–24)
*Diagram:* [`gate-e-board-b-assembly.svg`](file:///home/kawaiibuta/Projects/speaker-diy/projects/live-pa-system/gate-e-board-b-assembly.svg)

| RefDes | Description | Lead 1 Hole | Lead 2 Hole | Lead 3 / Extra | Assembly & Orientation Notes |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **TB_DC_IN** | 2-Pin Screw Terminal | **B2** (+36V In) | **C2** (GND Return)| — | From panel fuse F1 and DC barrel jack J3. |
| **TB_AMP_PWR**| 2-Pin Screw Terminal | **E2** (+36V Out)| **F2** (GND Out) | — | Feeds amplifier module directly (18 AWG). |
| **Q1** | IRF4905 TO-220 | **B6** (Gate) | **C6** (Drain / Tab)| **D6** (Source) | **Tab is Drain.** Floating clip-on heatsink. |
| **R18** | $100\text{ k}\Omega, 1/4\text{ W}$ | **B8** | **D8** | — | Gate pull-down to GND. |
| **D1** | BZX79C12 ($12\text{V}$ Zener)| **B9** (Cathode) | **D9** (Anode) | — | Gate-to-Source clamp. |
| **C17** | $470\ \mu\text{F} / 50\text{ V}$ | **D13** ($+$) | **E13** ($-$) | — | Bulk electrolytic. Observe negative stripe. |
| **C18** | $100\text{ nF} / 50\text{ V}$ | **B13** | **C13** | — | High-frequency rail bypass. |
| **U4** | LM317HVT TO-220 | **I9** (Pin 1 ADJ)| **J9** (Pin 2 VOUT)| **K9** (Pin 3 VIN)| **TAB IS +15V (NOT GND!).** Floating heatsink. |
| **D2** | 1N4007 Diode | **J6** (Anode) | **K6** (Cathode) | — | Reverse protection diode across U4. |
| **R19** | $240\ \Omega, 1/4\text{ W}$ | **I13** | **J13** | — | LM317 program resistor. |
| **R20** | $2.64\text{ k}\Omega, 1/4\text{ W}$ | **H15** | **I15** | — | LM317 setting resistor. |
| **C19** | $10\ \mu\text{F} / 25\text{ V}$ | **I17** ($+$) | **H17** ($-$) | — | ADJ pin ripple bypass capacitor. |
| **D3** | 1N4007 Diode | **H13** (Anode) | **I13** (Cathode) | — | Reverse protection diode across R20. |
| **C20** | $100\ \mu\text{F} / 25\text{ V}$ | **J15** ($+$) | **L15** ($-$) | — | Regulator output capacitor. |
| **C21** | $100\text{ nF} / 50\text{ V}$ | **J17** | **K17** | — | Output HF bypass. |
| **R21** | $10\text{ k}\Omega, 1/4\text{ W}$ | **N5** | **P5** | — | Virtual ground divider upper leg (+15V side). |
| **R22** | $10\text{ k}\Omega, 1/4\text{ W}$ | **N7** | **P7** | — | Virtual ground divider lower leg (GND side). |
| **C22** | $10\ \mu\text{F} / 25\text{ V}$ | **N9** ($+$) | **P9** ($-$) | — | Divider filter capacitor. |
| **U3 Socket**| DIP-8 IC Socket | **N12** (Pin 1) | **N13** (Pin 2) | Pins 3..8: N14, N15, Q15, Q14, Q13, Q12 | Notch faces Row 11 (UP). |
| **C26** | $100\text{ nF} / 50\text{ V}$ | **N17** | **Q17** | — | U3 supply decoupling (+15V Pin 8 to GND Pin 4).|
| **C23** | $47\ \mu\text{F} / 25\text{ V}$ | **N19** ($+$) | **P19** ($-$) | — | Virtual ground output reservoir. |
| **C25** | $100\text{ nF} / 50\text{ V}$ | **N21** | **P21** | — | Virtual ground HF bypass. |
| **TB_PWR_OUT**| 4-Pin Screw Terminal | **N23** (+15V Out)| **O23** (GND Out)| **P23** (VBIAS Out), **Q23** (Spare/Shield) | Clean analog feeder to Board A. |

#### 5. Step-by-Step Assembly Procedure
1. Solder passive jumpers and star ground links first on the bottom of Board B using 24 AWG wire.
2. Install DIP-8 socket for `U3` (notch facing Row 11). **Do NOT insert the NE5532P IC yet.**
3. Install resistors `R18`, `R19`, `R20`, `R21`, `R22` and diodes `D1`, `D2`, `D3`. Verify cathode bands!
4. Install ceramic capacitors `C18`, `C21`, `C25`, `C26` and radial electrolytics `C17`, `C19`, `C20`, `C22`, `C23`. Observe polarity!
5. Install `Q1` (IRF4905) and `U4` (LM317HVT) with their heatsinks. Confirm heatsinks do NOT touch each other or any adjacent pads.
6. Install terminal blocks `TB_DC_IN`, `TB_AMP_PWR`, and `TB_PWR_OUT`.

#### 6. Staged Bring-Up & Verification Procedures

> [!CAUTION]
> **Reverse-Polarity Test Fixture Rule:**  
> Never test reverse polarity on a fully populated board! Test reverse polarity **only** on the protection stage (Q1 + D1 + R18) BEFORE inserting U3 and before connecting any downstream circuits.

##### Stage 1.1: Cold Continuity Check (Zero Power)
- Measure resistance across `TB_DC_IN` (B2 to C2): Must be $> 100\text{ k}\Omega$.
- Measure resistance from `U4` heatsink tab to Board B GND: Must be **$> 1\text{ M}\Omega$** (Tab is connected to Pin 2 / +15V, completely floating from ground).
- Measure resistance from `Q1` heatsink tab to Board B GND: Must be $> 100\text{ k}\Omega$.
- Measure resistance across `TB_PWR_OUT` Pin 1 (+15V) to Pin 2 (GND): Must be $> 2.0\text{ k}\Omega$ (nominal divider $R_{19}+R_{20} = 2.88\text{ k}\Omega$).

##### Stage 1.2: Isolated Reverse-Polarity Stress Test
- Disconnect all downstream loads. U3 socket is EMPTY.
- Connect DC power supply (or 36V adapter with $100\ \Omega / 10\text{ W}$ series resistor) in **REVERSE** ($-36.0\text{ V}$ to `TB_DC_IN` Pin 1, $0\text{ V}$ to Pin 2).
- Measure current: Must read **$0.00\text{ mA}$** ($< 10\ \mu\text{A}$ on sensitive DMM).
- Measure voltage at `Q1` Source (Hole D6): Must read **$0.00\text{V} \pm 10\text{ mV}$**.
- Confirm fuse `F1` does NOT blow.

##### Stage 1.3: Forward Power-Up & +15V Regulation
- Reconnect normal forward polarity ($+36.0\text{ V}$ to Pin 1, $0\text{ V}$ to Pin 2) through current limiter ($100\text{ mA}$ limit or series $100\ \Omega$ resistor).
- Measure voltage drop across `Q1` ($V_{\text{DS}}$ between Drain Pin 2 and Source Pin 3): Must read **$\le 30\text{ mV}$** ($R_{\text{DS(on)}} \approx 20\text{ m}\Omega$).
- Measure Gate-Source voltage ($V_{\text{GS}}$ between Gate Pin 1 and Source Pin 3): Must read **$-12.0\text{V} \pm 0.5\text{V}$** (Zener clamp active).
- Measure `U4` output voltage at `TB_PWR_OUT` Pin 1: Must read **$+15.0\text{V} \pm 0.3\text{V}$**.
- Measure AC ripple on +15V rail with oscilloscope (AC coupling): Must be $< 1.0\text{ mV}_{\text{RMS}}$.

##### Stage 1.4: Virtual Ground Buffer Bring-Up
- Power down and discharge capacitors.
- Insert `U3` (NE5532P) into DIP-8 socket with notch facing UP.
- Re-apply forward $+36\text{ V}$. Measure total board quiescent current: Must read **$12\text{ mA} \sim 25\text{ mA}$**.
- Measure voltage at `TB_PWR_OUT` Pin 3 (`VBIAS_7V5`): Must read **$+7.50\text{V} \pm 0.15\text{V}$**.
- Perform 15-minute thermal soak: Measure `U4` heatsink temperature. Must not exceed **$55^\circ\text{C}$** at $25^\circ\text{C}$ ambient.

#### 7. Batch 1 Data Recording & Sign-Off Submission Form

```markdown
### Batch 1 Verification Submission Record

- Multimeter / Test Instrument: [ e.g., Fluke 87V, Serial: ____________ ]
- Ambient Temperature: [ ____ °C ]

1. Cold Continuity Checks:
   [ ] TB_DC_IN to GND resistance: ________ kΩ (Pass: > 100 kΩ)
   [ ] Q1 heatsink tab to GND: ________ kΩ (Pass: > 100 kΩ)
   [ ] U4 LM317 tab to GND: ________ MΩ (Pass: > 1.0 MΩ, strictly isolated!)
   [ ] TB_PWR_OUT +15V to GND: ________ kΩ (Pass: > 2.0 kΩ)

2. Electrical Measurements:
   - Reverse Polarity Current (-36V in): ________ mA (Pass: 0.00 mA / < 10 µA)
   - Reverse Polarity Voltage at +36V Bus: ________ mV (Pass: 0.00 V ± 10 mV)
   - Q1 Forward Voltage Drop (V_DS): ________ mV (Pass: <= 30 mV)
   - Q1 Gate-Source Voltage (V_GS): ________ V (Pass: -12.0 V ± 0.5 V)
   - U4 Regulated Output (+15V rail): ________ V (Pass: +15.0 V ± 0.3 V)
   - +15V Rail AC Ripple: ________ mV_RMS (Pass: < 1.0 mV_RMS)
   - U3 Virtual Ground (VBIAS_7V5): ________ V (Pass: +7.50 V ± 0.15 V)
   - Board B Total Quiescent Current: ________ mA (Pass: 12 mA to 25 mA)
   - U4 Heatsink Temperature (15 min): ________ °C (Pass: <= 55 °C)

3. Gate 1 Evaluation: [ PASS / FAIL / BLOCKED ]
```

> [!IMPORTANT]
> **GATE 1 ADVANCE CONDITION:**  
> **Batch 2 (Mic Preamp) may ONLY be purchased after all items in Gate 1 read PASS.** If +15V or +7.5V is out of spec, STOP and troubleshoot.

---

### BATCH 2 — Board A (Zone 1): Microphone Preamplifier

#### 1. Purpose
Assemble and verify the balanced microphone differential preamplifier and variable gain stage on the left half of **Board A ($7 \times 9\text{ cm}$)**:
- $U_{1\text{A}}$: Precision balanced differential difference amplifier ($+6.60\text{ dB}$ fixed gain, $\ge 50\text{ dB}$ CMRR using 0.1% matched pairs).
- $U_{1\text{B}}$: Variable second gain stage ($+13.4\text{ dB}$ to $+43.9\text{ dB}$, total gain $+20.0\text{ dB}$ to $+50.5\text{ dB}$).
- Input RF suppression, non-polar AC coupling, variable gain pot (`RV1`), channel volume pot (`RV2`), and panel XLR input jack (`J1`).

#### 2. Exact Component Purchase List (Batch 2 Only)
| RefDes | Component Specification | Package | Qty | Purpose | Est. Cost (VND) |
| :--- | :--- | :---: | :---: | :--- | :---: |
| **U1** | NE5532P dual low-noise audio op-amp (TI) | DIP-8 | 1 | Mic preamplifier IC (U1A + U1B) | 15,000 |
| **R3, R5** | $2.2\text{ k}\Omega \pm 0.1\%, 1/4\text{ W}$ metal film | Axial | 2 | Differential receiver input network | 5,000 |
| **R4, R6** | $4.7\text{ k}\Omega \pm 0.1\%, 1/4\text{ W}$ metal film | Axial | 2 | Differential feedback and Vbias network | 5,000 |
| **R1, R2** | $100\text{ k}\Omega \pm 1\%, 1/4\text{ W}$ metal film | Axial | 2 | Mic input DC ground reference | 1,000 |
| **R7** | $47\text{ k}\Omega \pm 1\%, 1/4\text{ W}$ metal film | Axial | 1 | Stage 2 non-inverting bias resistor | 500 |
| **R8** | $330\ \Omega \pm 1\%, 1/4\text{ W}$ metal film | Axial | 1 | Stage 2 minimum-gain limit floor | 500 |
| **R10** | $1.2\text{ k}\Omega \pm 1\%, 1/4\text{ W}$ metal film | Axial | 1 | Stage 2 gain scaling resistor | 500 |
| **C1, C2** | $47\text{ pF} / 100\text{ V}$ C0G ceramic disc | Radial | 2 | RF suppression across XLR Hot/Cold | 2,000 |
| **C4, C5** | $10\ \mu\text{F} / 50\text{ V}$ Non-Polar (Bi-Polar / BP) | Radial | 2 | Mic input AC coupling capacitors | 8,000 |
| **C3** | $100\text{ nF} / 50\text{ V}$ monolithic ceramic | Radial | 1 | U1 supply decoupling (+15V to GND) | 1,500 |
| **C6, C7** | $10\ \mu\text{F} / 25\text{ V}$ radial electrolytic | Radial | 2 | Interstage coupling capacitors | 4,000 |
| **RV1** | $50\text{ k}\Omega$ Reverse-Log (Rev-Log / C50K) pot | 16mm | 1 | Mic variable gain control | 15,000 |
| **RV2** | $10\text{ k}\Omega$ Audio Log (A10K) potentiometer | 16mm | 1 | Mic channel volume control | 12,000 |
| **J1** | Neutrik NC3FD-L-1 XLR Female panel receptacle | Panel | 1 | Mic balanced input connector | 35,000 |
| **Knobs** | 6 mm shaft rotary knobs | Panel | 2 | Knobs for RV1 & RV2 | 10,000 |
| **Subtotal B2**| **Batch 2 Components** | — | — | — | **115,000 VND** |

*Optional Order Consolidation Tip:* You may optionally purchase U2 (NE5532P for Batch 3) in this order to save shipping, but do NOT populate U2 until Batch 3.

#### 3. Financial Tracking
- Batch 2 Cost: **115,000 VND**
- Shipping: **25,000 VND**
- Cumulative Expenditure: **515,000 VND**
- Remaining Budget: **4,485,000 VND**

#### 4. Board A Placement: Zone 1 (Cols A–L, Rows 2–29)
*Diagram:* [`gate-e-board-a-assembly.svg`](file:///home/kawaiibuta/Projects/speaker-diy/projects/live-pa-system/gate-e-board-a-assembly.svg)
- `TB_MIC`: Holes B2 (GND), C2 (Hot), D2 (Cold).
- `TB_PWR`: Holes W2 (+15V), X2 (GND), Y2 (VBIAS) — fed from Board B.
- `U1 Socket`: E12..E15 (Pins 1..4), H15..H12 (Pins 5..8).
- `RV1`: C27 (CW), D27 (Wiper), E27 (CCW).
- `RV2`: G27 (CW), H27 (Wiper), I27 (CCW).

#### 5. Verification & Acceptance Gate
- **Gain Sweep:** Inject balanced $5.0\text{ mV}_{\text{RMS}}$ 1 kHz sine into XLR J1.
  - RV1 CCW: Output at C7 must read **$50\text{ mV}_{\text{RMS}} \pm 5\text{ mV}$** ($+20.0\text{ dB} \pm 1\text{ dB}$).
  - RV1 CW: Output at C7 must read **$1.67\text{ V}_{\text{RMS}} \pm 0.15\text{ V}$** ($+50.5\text{ dB} \pm 1.5\text{ dB}$).
- **Mic CMRR:** Tie XLR Pins 2 and 3 together; inject $1.0\text{ V}_{\text{RMS}}$ common-mode at 60 Hz and 1 kHz. Output must be $\le 10\text{ mV}_{\text{RMS}}$, guaranteeing **$\text{CMRR} \ge 40.0\text{ dB}$** (target $\ge 50\text{ dB}$).
- **Waveform:** Pure undistorted sine wave on DSO; no clipping or oscillation.

---

### BATCH 3 — Board A (Zone 2): LINE Receiver, Common 60 Hz HPF & Mode Selector

#### 1. Purpose
Assemble and verify the balanced LINE receiver and the master 2nd-order Sallen-Key 60 Hz High-Pass Filter on the right half of **Board A ($7 \times 9\text{ cm}$)**:
- $U_{2\text{B}}$: Balanced LINE differential receiver with precision 0.1% resistors ($A_d = -9.54\text{ dB}$, attenuation of line levels).
- $U_{2\text{A}}$: Common second-order Sallen-Key High-Pass Filter ($f_c = 60\text{ Hz}$, Butterworth $Q = 0.707$).
- Mode Selector `SW1` (DPDT): Switches between Mode A (Standalone Vocal) and Mode B (External Monitor), routing the selected signal through the HPF.
- Channel Volume `RV3` and Combo XLR/TRS input jack `J2`.

#### 2. Exact Component Purchase List (Batch 3 Only)
| RefDes | Component Specification | Package | Qty | Purpose | Est. Cost (VND) |
| :--- | :--- | :---: | :---: | :--- | :---: |
| **U2** | NE5532P dual low-noise audio op-amp (TI) | DIP-8 | 1 | Line receiver (U2B) & HPF (U2A) | 15,000 |
| **R14, R15** | $30\text{ k}\Omega \pm 0.1\%, 1/4\text{ W}$ metal film | Axial | 2 | Line receiver input divider resistors | 5,000 |
| **R16, R17** | $10\text{ k}\Omega \pm 0.1\%, 1/4\text{ W}$ metal film | Axial | 2 | Line receiver feedback / bias resistors | 5,000 |
| **R12, R13** | $100\text{ k}\Omega \pm 1\%, 1/4\text{ W}$ metal film | Axial | 2 | Line input DC ground reference | 1,000 |
| **R9** | $27\text{ k}\Omega \pm 1\%, 1/4\text{ W}$ metal film | Axial | 1 | Sallen-Key HPF feedback resistor | 500 |
| **R11** | $56\text{ k}\Omega \pm 1\%, 1/4\text{ W}$ metal film | Axial | 1 | Sallen-Key HPF non-inverting bias resistor | 500 |
| **R24** | $100\text{ k}\Omega \pm 1\%, 1/4\text{ W}$ metal film | Axial | 1 | Audio output pull-down to GND | 500 |
| **C10, C11** | $47\text{ pF} / 100\text{ V}$ C0G ceramic disc | Radial | 2 | RF suppression across Line inputs | 2,000 |
| **C12, C13** | $1.0\ \mu\text{F} / 63\text{V} \sim 100\text{V}$ metallized film (MKT) | Radial | 2 | Line input AC coupling capacitors | 12,000 |
| **C16** | $100\text{ nF} / 50\text{ V}$ monolithic ceramic | Radial | 1 | U2 supply decoupling (+15V to GND) | 1,500 |
| **C15, C14** | $10\ \mu\text{F} / 25\text{ V}$ radial electrolytic | Radial | 2 | Line out / HPF out coupling | 4,000 |
| **C8, C9** | $68\text{ nF} / 63\text{V} \sim 100\text{V}$ film (MKP/MKT) | Radial | 2 | Sallen-Key HPF frequency-determining caps | 10,000 |
| **RV3** | $10\text{ k}\Omega$ Audio Log (A10K) potentiometer | 16mm | 1 | Line channel volume control | 12,000 |
| **SW1** | DPDT slide or mini toggle switch (panel mount) | 6-pin | 1 | Mode selector switch (Vocal / Monitor) | 12,000 |
| **J2** | Neutrik NCJ6FI-S Combo XLR/TRS receptacle | Panel | 1 | Balanced Line input jack | 45,000 |
| **Subtotal B3**| **Batch 3 Components** | — | — | — | **125,000 VND** |

#### 3. Financial Tracking
- Batch 3 Cost: **125,000 VND**
- Shipping: **25,000 VND**
- Cumulative Expenditure: **665,000 VND**
- Remaining Budget: **4,335,000 VND**

#### 4. Board A Placement: Zone 2 (Cols M–Z, Rows 2–30)
*Diagram:* [`gate-e-board-a-assembly.svg`](file:///home/kawaiibuta/Projects/speaker-diy/projects/live-pa-system/gate-e-board-a-assembly.svg)
- `TB_LINE`: Holes N2 (GND), O2 (Hot), P2 (Cold).
- `U2 Socket`: Q12..Q15 (Pins 1..4), T15..T12 (Pins 5..8).
- `RV3`: N27 (CW), O27 (Wiper), P27 (CCW).
- `SW1`: U27..W28 (DPDT 6-pin footprint).
- `TB_OUT`: Holes R30 (Pin 1 Audio Sig), S30 (Pin 2 GND), T30 (Pin 3 Shield).
- `TP1 Test Point`: Hole V24.

#### 5. Verification & Acceptance Gate
- **Line Receiver Gain:** Inject balanced $+4.0\text{ dBu}$ ($1.228\text{ V}_{\text{RMS}}$) 1 kHz sine into Combo J2. Output at C15 must read **$0.41\text{ V}_{\text{RMS}} \pm 0.03\text{ V}$** ($-9.54\text{ dB}$).
- **Line Headroom Stress Test:** Inject $+22.0\text{ dBu}$ ($9.75\text{ V}_{\text{RMS}}$) 1 kHz sine into J2. Waveform at U2 Pin 7 must swing cleanly between $2.9\text{ V}$ and $12.1\text{ V}$ with **zero clipping** and $> 1.0\text{ V}$ rail margin.
- **Line CMRR:** Tie Hot and Cold together; inject $2.0\text{ V}_{\text{RMS}}$ at 60 Hz and 1 kHz. Verify **$\text{CMRR} \ge 40.0\text{ dB}$** (target $\ge 50\text{ dB}$).
- **Common 60 Hz HPF Response:** Measure at `TB_OUT` (Pin 1) relative to 1 kHz:
  - 100 Hz: attenuation $< 0.8\text{ dB}$.
  - 60 Hz: attenuation **$-3.0\text{ dB} \pm 0.5\text{ dB}$** ($f_c = 60\text{ Hz} \pm 3\text{ Hz}$).
  - 25 Hz: attenuation **$\le -15.0\text{ dB}$** (sub-bass excursion protection verified).
- **Mode Switching Verification:** Toggle `SW1` between Mode A and Mode B. **Verify that the 60 Hz HPF attenuation profile applies identically to both inputs!**

---

### BATCH 4 — Commercial Amplifier Module, 36V PSU & Load Verification

#### 1. Purpose
Procure and verify the main power chain: the commercial Wuzhi ZK-3002 Class-D amplifier module, the external 36V 5A power supply, and load testing into a power dummy load before risking the speaker driver.

#### 2. Exact Component Purchase List (Batch 4 Only)
| Item Description | Exact Specification | Qty | Purpose | Est. Cost (VND) |
| :--- | :--- | :---: | :--- | :---: |
| **Class-D Amplifier Module** | Wuzhi ZK-3002 / TPA3255 PBTL mono module (heatsink included) | 1 pc | High-power PBTL Class-D drive | 380,000 |
| **External DC Power Supply** | $36\text{ V} / 5\text{ A}$ ($180\text{ W}$) regulated switching adapter | 1 pc | Main system power source | 350,000 |
| **Power Dummy Load** | $8.0\ \Omega \pm 1\%, 100\text{ W}$ non-inductive aluminum-housed resistor | 1 pc | Safe bench load testing | 35,000 |
| **Subtotal B4** | **Batch 4 Components** | — | — | **765,000 VND** |

#### 3. Financial Tracking
- Batch 4 Cost: **765,000 VND**
- Shipping: **35,000 VND**
- Cumulative Expenditure: **1,465,000 VND**
- Remaining Budget: **3,535,000 VND**

#### 4. Wiring & Floating Bridge Connection Rules

> [!CAUTION]
> **STRICT PBTL FLOATING OUTPUT ISOLATION:**  
> The TPA3255 in PBTL configuration has **two active switching bridge outputs** (`AMP_OUT_POS` and `AMP_OUT_NEG`). Both terminals sit at **$+18.0\text{ V}$ DC half-supply**.
> - **NEVER** connect either speaker terminal to GND, chassis, or oscilloscope ground clip!
> - Use a differential oscilloscope probe, or measure with a floating battery-powered DMM.
> - High-current connections between Board B `TB_AMP_PWR` and the amplifier module use **18 AWG stranded silicone wire**.

#### 5. Verification & Acceptance Gate
- **Floating DC Bias Check:**
  - Measure DC voltage from `AMP_OUT_POS` to GND: must read **$+18.0\text{V} \pm 1.0\text{V}$**.
  - Measure DC voltage from `AMP_OUT_NEG` to GND: must read **$+18.0\text{V} \pm 1.0\text{V}$**.
  - Differential DC offset across POS and NEG: **$\le 50\text{ mV}$ DC**.
  - Resistance to chassis/ground: **$> 1.0\text{ M}\Omega$** (strictly floating).
- **Continuous Rated Power Test (10.0 W RMS into $8.0\ \Omega$):**
  - Connect $8\ \Omega$ 100W dummy load across PBTL outputs.
  - Inject 1 kHz sine into Line input; advance volume until True-RMS voltage across the load reads **$8.94\text{ V}_{\text{RMS}}$** ($12.65\text{ V}_{\text{pk}}$).
  - Calculate power: $P = (8.94)^2 / 8.0 = \mathbf{10.0\text{ W RMS}}$.
  - Inspect waveform on DSO: Pure undistorted sine wave, $\text{THD} < 0.1\%$ (visually clean).
  - 15-minute continuous thermal soak: Monitor amplifier heatsink temperature. Must remain $< 60^\circ\text{C}$.
- **Dynamic Burst Headroom Test:**
  - Brief pulse or tone burst to verify unclipped burst output up to **$25.3\text{ V}_{\text{pk}}$** (40W burst) and **$32.0\text{ V}_{\text{pk}}$** (64W burst) without power supply sagging or shutdown.

---

### BATCH 5 — Transducer & Prototype Enclosure

#### 1. Purpose
Procure the Visaton BG 20 loudspeaker driver and construct the 25 L net bass-reflex wedge enclosure. Tune the port resonance $F_b$ to 50 Hz and measure raw acoustic performance before designing the contour filter.

#### 2. Exact Component Purchase List (Batch 5 Only)
| Item Description | Exact Specification | Qty | Purpose | Est. Cost (VND) |
| :--- | :--- | :---: | :--- | :---: |
| **Loudspeaker Driver** | Visaton BG 20 ($8\ \Omega, 8\text{''}$ Full-Range, $92\text{ dB/W/m}$) | 1 pc | Main acoustic transducer | 1,150,000 |
| **MDF Sheet** | 15 mm high-density MDF sheet (cut to wedge panel dimensions) | 1 set | 25 L net stage-wedge cabinet | 400,000 |
| **PVC Port Tube** | $60\text{ mm}$ internal dia PVC pipe ($\ge 120\text{ mm}$ raw length) | 1 pc | Bass-reflex port (tune to 91.2 mm) | 30,000 |
| **Cabinet Hardware** | Damping wool ($200\text{ g}$), wood screws, rubber feet (4 pcs), gasket tape | 1 set | Enclosure assembly & sealing | 220,000 |
| **Subtotal B5** | **Batch 5 Components** | — | — | **1,800,000 VND** |

#### 3. Financial Tracking
- Batch 5 Cost: **1,800,000 VND**
- Shipping: **60,000 VND**
- Cumulative Expenditure: **3,325,000 VND**
- Remaining Budget: **1,675,000 VND**

#### 4. Cabinet Construction & Acoustic Tuning
1. **Cabinet Geometry:** 25 L net internal volume, wedge baffle angled at $45^\circ$, internal bracing, lined with $25\text{ mm}$ polyester damping wool on rear and side walls (leave clear path between driver and port).
2. **Port Tuning ($F_b$):**
   - Cut PVC port tube to initial length of **$95\text{ mm}$**.
   - Run impedance sweep with REW / DATS from 20 Hz to 200 Hz.
   - Locate the saddle minimum between the two bass impedance peaks: Target **$F_b = 50.0\text{ Hz} \pm 2\text{ Hz}$**.
   - Trim or adjust port length as required (final nominal physical cut $\approx 91.2\text{ mm}$).
3. **Acoustic Measurements:**
   - Measure sensitivity at 1 m ($2.83\text{ V}_{\text{RMS}}$): Must reach **$92\text{ dB} \pm 2\text{ dB}$ SPL**.
   - Measure maximum continuous clean SPL at 10 W RMS ($8.94\text{ V}_{\text{RMS}}$): Must reach **$\ge 102.0\text{ dB}$ SPL at 1 m** ($96\text{ dB}$ SPL at 2 m).
   - Check for air leaks around driver rim and port chuffing ($v_p = 5.7\text{ m/s}$, zero audible turbulence).
   - Inspect raw on-axis frequency response: Locate the characteristic whizzer cone presence rise between 1.5 kHz and 2.5 kHz to determine whether the RLC contour filter in Batch 6 is justified.

---

### BATCH 6 — Board C: Passive RLC Contour Filter & Final Finishing

#### 1. Purpose
If acoustic measurements in Batch 5 demonstrate excessive harshness from the BG 20 whizzer cone in vocal monitoring, procure and assemble the passive RLC contour network on **Board C ($5 \times 7\text{ cm}$)**. Complete cabinet protective corners, grille, handle, and exterior finish.

#### 2. Exact Component Purchase List (Batch 6 Only)
| Item Description | Exact Specification | Qty | Purpose | Est. Cost (VND) |
| :--- | :--- | :---: | :--- | :---: |
| **L1 Choke** | $1.0\text{ mH} \pm 5\%$ air-core inductor ($1.0\text{ mm}$ wire, $R_{\text{DC}} \le 0.35\ \Omega$)| 1 pc | Contour filter inductor | 120,000 |
| **C24 Film Cap** | $4.7\ \mu\text{F} \ge 250\text{ V}$ MKP audio polypropylene film capacitor | 1 pc | Contour filter capacitor | 65,000 |
| **R23 Power Resistor**| $8.2\ \Omega \pm 5\%, 10\text{ W}$ non-inductive wirewound / ceramic resistor | 1 pc | Contour filter damping resistor | 15,000 |
| **SW2 Switch** | SPST heavy-duty toggle switch ($\ge 3\text{ A}$) | 1 pc | Contour bypass switch | 20,000 |
| **Cabinet Finishing** | Paint / textured coating, 8x metal corners, recessed strap handle, steel grille | 1 set | Stage protection & finishing | 150,000 |
| **Subtotal B6** | **Batch 6 Components** | — | — | **370,000 VND** |

#### 3. Financial Tracking
- Batch 6 Cost: **370,000 VND**
- Shipping: **30,000 VND**
- Cumulative Expenditure: **3,725,000 VND**
- Final Remaining Budget: **+1,275,000 VND (Buffer under 5,000,000 VND ceiling)**

#### 4. Board C Placement & Floating Verification ($5 \times 7\text{ cm}$)
*Diagram:* [`gate-e-board-c-assembly.svg`](file:///home/kawaiibuta/Projects/speaker-diy/projects/live-pa-system/gate-e-board-c-assembly.svg)

> [!CAUTION]
> Board C has **NO GROUND TRACES**. Both `TB_SPK_IN` and `TB_SPK_OUT` float at $+18\text{ V}$ DC half-supply.

- `TB_SPK_IN`: Holes B2 (`AMP_OUT_POS`), C2 (`AMP_OUT_NEG`).
- `TB_SPK_OUT`: Holes B23 (`SPK_OUT_POS`), C23 (`SPK_OUT_NEG`).
- `SW2`: Holes B8, C8 (Bypasses RLC network directly).
- `L1`: Holes G11, O11 (Secured with nylon zip-ties through board holes I11 and M11).
- `C24`: Holes E17, I17.
- `R23`: Holes E21, M21 (Elevated $2\text{ mm}$ above perfboard for air circulation).

#### 5. Verification & Acceptance Gate
- **Unpowered Resistance Check:**
  - SW2 CLOSED (Bypassed): Resistance between `TB_SPK_IN` Pin 1 and `TB_SPK_OUT` Pin 1 must be **$< 0.1\ \Omega$**.
  - SW2 OPEN (Contour Active): Resistance must read **$\approx 0.34\ \Omega$ DC** ($R_{23} \parallel DCR_{L1} = 8.2\ \Omega \parallel 0.35\ \Omega$).
- **Acoustic A/B Listening Test:**
  - Confirm that activating the filter introduces a smooth **$-4.5\text{ dB} \pm 1.0\text{ dB}$ contour** between 1.5 kHz and 2.5 kHz, taming harshness and sibilance without sacrificing speech intelligibility.
  - Evaluate vocal microphone (Shure SM58) at 1.5 m: Stable gain before feedback and natural vocal presence.

---

## 4. Immediate Action Checklist: Batch 0 & Batch 1 Execution

Execute **ONLY Batch 0 and Batch 1** now. Do not purchase components for Batch 2 or beyond.

```markdown
### Immediate Action Checklist (Batch 0 & Batch 1)

1. Workspace & Tool Verification (Batch 0):
   [ ] DMM verified operational (Resistance and DC Volts calibrated).
   [ ] Soldering iron, rosin flux, 63/37 solder wire, flush cutters ready.
   [ ] Safe power bring-up fixture prepared:
       ( ) 0-40V Current-limited bench supply set to 100 mA limit, OR
       ( ) 36V DC adapter with 100 Ohm / 10W series resistor.
   [ ] Consumable prototyping materials acquired:
       ( ) 1x 7x9 cm FR-4 perfboard (Board A)
       ( ) 2x 5x7 cm FR-4 perfboard (Boards B & C)
       ( ) 3x DIP-8 machined IC sockets
       ( ) Terminal blocks (6x 2P, 3x 3P 5.08mm)
       ( ) 18 AWG silicone wire & 24 AWG jumper wire
       ( ) M3 standoffs, screws, nuts

2. Board B Procurement (Batch 1):
   [ ] IRF4905 P-FET (Q1) + BZX79C12 12V Zener (D1) + R18 (100k)
   [ ] C17 (470uF/50V Low-ESR) + C18 (100nF)
   [ ] LM317HVT (U4) + clip-on heatsink + D2, D3 (1N4007) + R19 (240R) + R20 (2.64k) + C19 (10uF) + C20 (100uF) + C21 (100nF)
   [ ] R21, R22 (10k 1%) + C22 (10uF) + U3 (NE5532P) + C23 (47uF) + C25, C26 (100nF)
   [ ] 5x20mm fuse holder + 4A-T fuse + 5.5x2.1mm DC barrel jack

3. Assembly & Staged Verification (Section 3, Batch 1):
   [ ] Solder Board B passives, socket, regulators, and terminals per gate-e-board-b-assembly.svg.
   [ ] Stage 1.1: Cold continuity checks (confirm LM317 tab > 1 MΩ to GND).
   [ ] Stage 1.2: Isolated reverse-polarity stress test (-36V in, 0.00 mA current).
   [ ] Stage 1.3: Forward power-up (+36V through 100R limiter, V_DS <= 30 mV, V_GS = -12V, +15.0V out).
   [ ] Stage 1.4: Virtual ground buffer check (+7.50V VBIAS out, 15-min thermal soak <= 55°C).

4. Submit completed Batch 1 Record:
   -> Enter readings into Section 3 (Batch 1 Form) and share results to unlock Batch 2.
```
