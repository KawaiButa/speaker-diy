# GATE E — BENCH PROTOTYPING & PHASED PHYSICAL VERIFICATION PLAN
## DIY Active Stage Monitor Loudspeaker (Visaton BG 20 + TPA3255 PBTL)

**Project:** DIY Active Stage Monitor Loudspeaker  
**Location:** [`projects/live-pa-system/`](file:///home/kawaiibuta/Projects/speaker-diy/projects/live-pa-system/)  
**Phase:** Gate E — Phased Procurement, Modular Bench Assembly & Staged Verification  
**Status:** Authorized — Phased Execution Active  
**Date:** October 15, 2026  
**Revision:** 2.0 (Phased Modular Prototyping Baseline)  

---

## 1. Objectives and Scope

The engineering design and digital simulation baseline for Gate D have passed all acceptance criteria:
- Schematics and netlist are 100% verified (KiCad 10, 0 ERC errors, 0 unconnected pins, 42 nets, 73 components).
- Common 60 Hz 2nd-order Sallen-Key HPF protects both Mic and Line paths ($\ge 15.3\text{ dB}$ attenuation at 25 Hz).
- Precision 0.1% metal-film resistors guarantee $\ge 50.5\text{ dB}$ worst-case discrete CMRR.
- P-MOSFET reverse-polarity protection has verified pin mapping (Pin 2 Drain to Input, Pin 3 Source to Protected Rail).
- Continuous rated operating level is strictly **10.0 W RMS** into $8\ \Omega$ to respect the driver's $\pm 2.0\text{ mm}$ linear excursion limit.

**Gate E Phased Scope:**
Gate E executes the physical verification of this design through **staged procurement and progressive subsystem testing**. No downstream components are ordered until the preceding hardware block passes its electrical verification gate.

> [!CAUTION]
> **Safety & Protection Protocols:**
> 1. **Current-Limited Power-Up:** Always bring up newly assembled circuits using a current-limited DC bench power supply ($100\text{ mA}$ limit) **OR** the approved safe alternative: a $100\ \Omega / 10\text{ W}$ power resistor in series with the 36V DC adapter positive lead. Never connect an unverified board directly to an unrestricted supply!
> 2. **PBTL Floating Speaker Isolation:** The TPA3255 operates in Parallel Bridge-Tied Load (PBTL). **Both output terminals (`AMP_OUT_POS` and `AMP_OUT_NEG`) are floating bridge outputs at $+18.0\text{ V}$ DC half-supply.** Neither terminal may ever connect to signal ground, chassis ground, or an oscilloscope probe ground clip! Board C contains zero ground traces.
> 3. **High-Current Wiring:** 36V 5A DC power and speaker audio lines must use direct **18 AWG stranded silicone wire** and never run over thin perfboard copper pads.
> 4. **Pre-Power Rail Checks:** Verify analog rail voltages (+15V, +7.5V Vbias) before inserting NE5532P op-amps into DIP-8 sockets or powering the TPA3255 amplifier module.
> 5. **Dummy Load First:** Test amplifier power into an $8.0\ \Omega\ 100\text{W}$ non-inductive dummy load before connecting the Visaton BG 20 loudspeaker driver.
> 6. **Authentic Data Only:** Never copy simulation values into actual measurement fields. Record only genuine bench instrument readings.

---

## 2. Phased Subsystem Status & Gate Tracker

```
+========================================================================================================================+
| BATCH | SUBSYSTEM DESCRIPTION              | ESTIMATED COST   | CUMULATIVE   | REMAINING BUDGET | GATE STATUS          |
+========================================================================================================================+
| B-0   | Tools & Construction Consumables   |      180,000 VND |  180,000 VND |    4,820,000 VND | READY (NOT STARTED)  |
| B-1   | Board B: Power & +7.5V Bias Buffer |      195,000 VND |  375,000 VND |    4,625,000 VND | READY (NOT STARTED)  |
| B-2   | Board A (Zone 1): Mic Preamp       |      140,000 VND |  515,000 VND |    4,485,000 VND | BLOCKED (Wait Gate 1)|
| B-3   | Board A (Zone 2): Line Rec & HPF   |      150,000 VND |  665,000 VND |    4,335,000 VND | BLOCKED (Wait Gate 2)|
| B-4   | TPA3255 Amp, 36V PSU & Dummy Load  |      800,000 VND | 1,465,000 VND|    3,535,000 VND | BLOCKED (Wait Gate 3)|
| B-5   | Visaton BG 20 & 25L MDF Enclosure  |    1,860,000 VND | 3,325,000 VND|    1,675,000 VND | BLOCKED (Wait Gate 4)|
| B-6   | Board C: RLC Contour & Finishing   |      400,000 VND | 3,725,000 VND|    1,275,000 VND | BLOCKED (Wait Gate 5)|
+========================================================================================================================+
| TOTAL PROJECT INVESTMENT: 3,725,000 VND | HARD BUDGET CEILING: 5,000,000 VND | CONTINGENCY RESERVE: +1,275,000 VND     |
+========================================================================================================================+
```

---

## 3. Required Test Equipment & Safe Bring-Up Fixture

| Equipment | Specification | Essential / Alternative | Usage |
| :--- | :--- | :---: | :--- |
| **True-RMS Multimeter (DMM)** | $\ge 4.5$ digits, AC+DC True-RMS | **Essential** | Voltage, current, continuity, cold resistance checks |
| **Soldering Station** | $40\text{ W} \sim 60\text{ W}$ temperature-controlled | **Essential** | Clean point-to-point perfboard assembly |
| **Current-Limited Bench Supply** | $0 \sim 36\text{ V}, 0 \sim 1\text{ A}$ adjustable | Strongly Preferred | Controlled power bring-up in Stage E1 / E2 |
| **Safe Bring-Up Resistor Fixture**| **$100\ \Omega / 10\text{ W}$ wirewound ceramic resistor** in series with 36V adapter | **Essential if no lab supply** | Limits fault current to $\le 360\text{ mA}$; prevents damage during shorts |
| **Oscilloscope** | Dual-channel $\ge 20\text{ MHz}$, 1 GS/s | Essential for Batches 2–4 | Signal swing, clipping, HPF frequency response |
| **Differential Scope Probe** | $10\times/100\times$ floating isolation | Essential for PBTL bridge | Measuring floating PBTL speaker output terminals |
| **Audio Signal Generator** | $10\text{ Hz} \sim 50\text{ kHz}$ low-distortion sine | **Zero-cost alternative** | Smartphone / PC 3.5mm jack with free REW signal generator |
| **Power Dummy Load** | $8.0\ \Omega \pm 1\%, 100\text{ W}$ non-inductive | Essential for Batch 4 | Amplifier continuous power and burst testing |
| **Contact Thermocouple** | Accuracy $\pm 1^\circ\text{C}$ | Essential for Batches 1 & 4 | LM317HVT and TPA3255 heatsink thermal soak tests |
| **Measurement Microphone** | Calibrated mic (e.g. UMIK-1) + REW | Essential for Batch 5 & 6 | Cabinet port tuning ($F_b$), SPL, and RLC contour validation |

---

## 4. Staged Verification Procedures

```
  +---------------------------------------------------------------------------------------+
  | BATCH 1: Board B Power Conditioning & +7.5V Active Bias Buffer                        |
  | (Cold resistance -> Isolated reverse-polarity -> Forward +15V & +7.5V -> Thermal soak)|
  +---------------------------------------------------------------------------------------+
                                             |
                                             v
  +---------------------------------------------------------------------------------------+
  | BATCH 2: Board A (Zone 1) Microphone Preamplifier                                     |
  | (Min/Max gain -> Headroom/clipping -> 60Hz/1kHz CMRR >= 40dB)                         |
  +---------------------------------------------------------------------------------------+
                                             |
                                             v
  +---------------------------------------------------------------------------------------+
  | BATCH 3: Board A (Zone 2) Balanced LINE Receiver, Common 60Hz HPF & Mode Selector     |
  | (Nominal +4dBu gain -> +22dBu headroom -> 60Hz HPF fc -> Mode A/B common routing)    |
  +---------------------------------------------------------------------------------------+
                                             |
                                             v
  +---------------------------------------------------------------------------------------+
  | BATCH 4: Power Amplifier & Load Testing (TPA3255 PBTL into 8-Ohm Dummy Load)          |
  | (Floating bridge bias -> 10.0W RMS continuous -> 64W burst -> Heatsink soak < 60°C)   |
  +---------------------------------------------------------------------------------------+
                                             |
                                             v
  +---------------------------------------------------------------------------------------+
  | BATCH 5: Transducer Integration & Acoustic Verification (Visaton BG 20 + 25L Wedge)   |
  | (Impedance sweep port tuning Fb = 50Hz -> 102dB SPL @ 1m -> Whizzer peak measurement) |
  +---------------------------------------------------------------------------------------+
                                             |
                                             v
  +---------------------------------------------------------------------------------------+
  | BATCH 6: Board C Passive RLC Contour Filter & Final Stage Finishing                   |
  | (Zero-GND verification -> -4.5dB contour between 1.5-2.5 kHz -> Vocal A/B listening) |
  +---------------------------------------------------------------------------------------+
```

---

## 5. Comprehensive Hardware Verification & Measurement Matrix

| Test ID | Test Condition | Expected Range | SPICE Baseline | Actual Measurement | Instrument / Serial | Status | Notes |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **B1.1** | Board B TB_DC_IN to GND (Cold) | $> 100\text{ k}\Omega$ | N/A | [ Blank ] | [ Blank ] | NOT TESTED | Cold DMM unpowered check |
| **B1.2** | LM317HVT Heatsink Tab to GND | $> 1.0\text{ M}\Omega$ | Isolated | [ Blank ] | [ Blank ] | NOT TESTED | Tab is Pin 2 (+15V, FLOATING!) |
| **B1.3** | Reverse Polarity Current (-36V DC In) | $< 10\ \mu\text{A}$ ($0.00\text{ mA}$) | $1.07\text{ nA}$ | [ Blank ] | [ Blank ] | NOT TESTED | Isolated Q1 protection check |
| **B1.4** | +36V Bus Voltage under -36V In | $0.00\text{V} \pm 10\text{ mV}$ | $0.00\text{V}$ | [ Blank ] | [ Blank ] | NOT TESTED | Reverse-polarity blocked |
| **B1.5** | Q1 Forward Voltage Drop ($V_{\text{DS}}$) | $\le 30\text{ mV}$ | $25.6\text{ mV}$ | [ Blank ] | [ Blank ] | NOT TESTED | P-FET forward conduction |
| **B1.6** | Q1 Gate-Source Voltage ($V_{\text{GS}}$) | $-12.0\text{V} \pm 0.5\text{V}$ | $-12.00\text{V}$ | [ Blank ] | [ Blank ] | NOT TESTED | D1 Zener clamp active |
| **B1.7** | LM317HVT Regulated Output (+15V Rail) | $+15.0\text{V} \pm 0.3\text{V}$ | $+15.02\text{V}$ | [ Blank ] | [ Blank ] | NOT TESTED | Linear regulated rail |
| **B1.8** | +15V Rail AC Ripple & Noise | $< 1.0\text{ mV}_{\text{RMS}}$ | $< 0.1\text{ mV}$ | [ Blank ] | [ Blank ] | NOT TESTED | DSO 20 MHz BW limit |
| **B1.9** | U3 Virtual Ground Buffer (`VBIAS_7V5`)| $+7.50\text{V} \pm 0.15\text{V}$ | $+7.50\text{V}$ | [ Blank ] | [ Blank ] | NOT TESTED | Active follower output |
| **B1.10**| LM317HVT Heatsink Temp (15 min soak) | $T_{\text{heatsink}} \le 55^\circ\text{C}$ | $49.7^\circ\text{C}$ | [ Blank ] | [ Blank ] | NOT TESTED | Thermocouple contact |
| **B2.1** | Mic Preamp Min Gain (RV1 CCW, 1 kHz) | $+20.0\text{ dB} \pm 1.0\text{ dB}$ | $+20.0\text{ dB}$ | [ Blank ] | [ Blank ] | BLOCKED | $5\text{ mV}_{\text{RMS}}$ in $\to 50\text{ mV}_{\text{RMS}}$ out |
| **B2.2** | Mic Preamp Max Gain (RV1 CW, 1 kHz) | $+50.5\text{ dB} \pm 1.5\text{ dB}$ | $+50.8\text{ dB}$ | [ Blank ] | [ Blank ] | BLOCKED | $5\text{ mV}_{\text{RMS}}$ in $\to 1.67\text{ V}_{\text{RMS}}$ out |
| **B2.3** | Mic CMRR (60 Hz & 1 kHz) | $\ge 40.0\text{ dB}$ (target $\ge 50\text{ dB}$) | $71.28\text{ dB}$ | [ Blank ] | [ Blank ] | BLOCKED | Tied Hot+Cold (1V RMS in) |
| **B3.1** | Line Receiver Gain (+4 dBu / 1.228V in) | $-9.54\text{ dB} \pm 0.5\text{ dB}$ | $-9.54\text{ dB}$ | [ Blank ] | [ Blank ] | BLOCKED | Measured at C15 ($0.41\text{ V}_{\text{RMS}}$) |
| **B3.2** | Line Headroom (+22 dBu / 9.75V RMS in) | Clean sine, zero clipping | Clean $9.15\text{ V}_{\text{pp}}$ | [ Blank ] | [ Blank ] | BLOCKED | $U_{2\text{B}}$ pin 7 on DSO |
| **B3.3** | Line CMRR (60 Hz & 1 kHz) | $\ge 40.0\text{ dB}$ (target $\ge 50\text{ dB}$) | $60.5\text{ dB}$ | [ Blank ] | [ Blank ] | BLOCKED | Tied Hot+Cold (2V RMS in) |
| **B3.4** | Common HPF Cutoff Frequency ($f_c$) | $60.0\text{ Hz} \pm 3.0\text{ Hz}$ | $59.2\text{ Hz}$ | [ Blank ] | [ Blank ] | BLOCKED | -3.0 dB relative to 1 kHz |
| **B3.5** | Common HPF Attenuation at 25 Hz | $\le -15.0\text{ dB}$ relative to 1 kHz | $-15.35\text{ dB}$ | [ Blank ] | [ Blank ] | BLOCKED | Sub-bass driver protection |
| **B3.6** | Mode A vs Mode B HPF Equivalence | Curves match within $\pm 0.2\text{ dB}$ | Identical | [ Blank ] | [ Blank ] | BLOCKED | Verify SW1 wiper routing |
| **B4.1** | PBTL DC Output Bias to GND | $+18.0\text{V} \pm 1.0\text{V}$ DC (both pins) | $+18.0\text{V}$ | [ Blank ] | [ Blank ] | BLOCKED | Floating bridge half-supply |
| **B4.2** | PBTL Differential DC Offset | $\le 50\text{ mV}$ DC across POS/NEG | $< 10\text{ mV}$ | [ Blank ] | [ Blank ] | BLOCKED | Measured across dummy load |
| **B4.3** | Continuous Power into $8.0\ \Omega$ (1 kHz) | $8.94\text{ V}_{\text{RMS}} \pm 0.2\text{ V}$ ($10.0\text{ W}$) | $8.94\text{ V}_{\text{RMS}}$ | [ Blank ] | [ Blank ] | BLOCKED | $8\ \Omega$ non-inductive load |
| **B4.4** | Continuous Power Waveform & THD | Clean undistorted sine, $\text{THD} < 0.1\%$ | Pure sine | [ Blank ] | [ Blank ] | BLOCKED | Differential scope probe |
| **B4.5** | Amplifier Heatsink Soak (15 min @ 10W) | $T_{\text{sink}} < 60^\circ\text{C}$ (at $25^\circ\text{C}$ amb) | $< 52^\circ\text{C}$ | [ Blank ] | [ Blank ] | BLOCKED | Thermocouple contact |
| **B4.6** | Dynamic Burst Output into $8.0\ \Omega$ | $25.3\text{--}32.0\text{ V}_{\text{pk}}$ (40W–64W burst) | Up to $32\text{ V}_{\text{pk}}$ | [ Blank ] | [ Blank ] | BLOCKED | Tone burst envelope |
| **B5.1** | Cabinet Port Resonance ($F_b$) | $50.0\text{ Hz} \pm 2.0\text{ Hz}$ | $50.0\text{ Hz}$ | [ Blank ] | [ Blank ] | BLOCKED | Impedance sweep saddle minimum |
| **B5.2** | Driver Free-Air Resonance ($f_s$) | $38\text{ Hz} \pm 4\text{ Hz}$ | $38\text{ Hz}$ | [ Blank ] | [ Blank ] | BLOCKED | Driver unmounted sweep |
| **B5.3** | Sensitivity SPL at 1 m (2.83V RMS, 1W) | $92.0\text{ dB} \pm 2.0\text{ dB}$ SPL | $92\text{ dB}$ SPL | [ Blank ] | [ Blank ] | BLOCKED | Calibrated measurement mic |
| **B5.4** | Max Continuous SPL at 1 m (8.94V, 10W) | $\ge 102.0\text{ dB}$ SPL ($96\text{ dB}$ @ 2 m) | $102\text{ dB}$ SPL | [ Blank ] | [ Blank ] | BLOCKED | Clean continuous 10W drive |
| **B5.5** | Port Chuffing / Turbulence at 10 W RMS | Zero audible chuffing ($v_p < 15\text{ m/s}$) | $v_p = 5.7\text{ m/s}$ | [ Blank ] | [ Blank ] | BLOCKED | 50 Hz sine drive |
| **B6.1** | Board C Ground Isolation Check | $> 1.0\text{ M}\Omega$ to GND / chassis | Isolated | [ Blank ] | [ Blank ] | BLOCKED | ZERO ground connections! |
| **B6.2** | RLC Contour Attenuation (1.5–2.5 kHz) | $-4.5\text{ dB} \pm 1.0\text{ dB}$ contour dip | $-4.6\text{ dB}$ | [ Blank ] | [ Blank ] | BLOCKED | Gated acoustic sine sweep |
| **B6.3** | Vocal Clarity & Feedback Margin | Articulate tone, stable gain | Pass | [ Blank ] | [ Blank ] | BLOCKED | Shure SM58 listening test |

---

## 6. Immediate Action Item: Batch 1 Verification Form

Execute physical assembly of **Board B** and record your actual instrument measurements below:

```markdown
### Batch 1 Verification Submission Record

- Multimeter / Test Instrument: [ e.g., Fluke 87V, Serial: ____________ ]
- Ambient Temperature: [ ____ °C ]

1. Cold Continuity Checks (Unpowered):
   [ ] TB_DC_IN to GND resistance: ________ kΩ (Expected: > 100 kΩ)
   [ ] Q1 heatsink tab to GND: ________ kΩ (Expected: > 100 kΩ)
   [ ] U4 LM317 tab to GND: ________ MΩ (Expected: > 1.0 MΩ, strictly isolated!)
   [ ] TB_PWR_OUT +15V to GND: ________ kΩ (Expected: > 2.0 kΩ)

2. Electrical Measurements:
   - Reverse Polarity Current (-36V in): ________ mA (Expected: 0.00 mA / < 10 µA)
   - Reverse Polarity Voltage at +36V Bus: ________ mV (Expected: 0.00 V ± 10 mV)
   - Q1 Forward Voltage Drop (V_DS): ________ mV (Expected: <= 30 mV)
   - Q1 Gate-Source Voltage (V_GS): ________ V (Expected: -12.0 V ± 0.5 V)
   - U4 Regulated Output (+15V rail): ________ V (Expected: +15.0 V ± 0.3 V)
   - +15V Rail AC Ripple: ________ mV_RMS (Expected: < 1.0 mV_RMS)
   - U3 Virtual Ground (VBIAS_7V5): ________ V (Expected: +7.50 V ± 0.15 V)
   - Board B Total Quiescent Current: ________ mA (Expected: 12 mA to 25 mA)
   - U4 Heatsink Temperature (15 min soak): ________ °C (Expected: <= 55 °C)

3. Discrepancies or Irregularities Observed:
   [ None / Describe any solder bridge, component deviation, or unusual reading ]

4. Batch 1 Gate Decision: [ PASS / FAIL / BLOCKED ]
```

> [!WARNING]
> Do NOT purchase Batch 2 components or apply power to downstream audio op-amps until this Batch 1 record is submitted and confirmed PASS!
