# GATE E — Bench Prototyping & Physical Verification Plan
## DIY Active Stage Monitor Loudspeaker (Visaton BG 20 + TPA3255 PBTL)

**Project:** DIY Active Stage Monitor Loudspeaker  
**Location:** `projects/live-pa-system/`  
**Phase:** Gate E — Bench Prototyping, Staged Electrical Bring-Up, and Acoustic Verification  
**Status:** Authorized — In Progress (Hardware Verification Pending)  
**Date:** October 2026  
**Revision:** 1.1 (Reconciled CMRR Analysis & Formal Actual Measurement Records)  

---

## 1. Objectives and Scope

The engineering design and digital simulation baseline for Gate D have passed all acceptance criteria:
- Schematics and netlist are 100% verified (KiCad 10, 0 ERC errors, 0 unconnected pins, 42 nets, 73 components).
- Common 60 Hz 2nd-order Sallen-Key HPF protects both Mic and Line paths ($\ge 15.3\text{ dB}$ attenuation at 25 Hz).
- Precision 0.1% metal-film resistors guarantee $\ge 50.5\text{ dB}$ worst-case discrete CMRR.
- P-MOSFET reverse-polarity protection has verified pin mapping (Pin 2 Drain to Input, Pin 3 Source to Protected Rail).
- Continuous rated operating level is strictly **10.0 W RMS** into $8\ \Omega$ to respect the driver's $\pm 2.0\text{ mm}$ linear excursion limit.

**Gate E Scope:**
Gate E executes the physical verification of this design through staged bench procedures. No hardware step proceeds until the preceding electrical validation gate passes.

> [!CAUTION]
> **Safety & Protection Protocols:**
> 1. Always bring up circuits using a current-limited DC bench power supply. Never connect an unverified board directly to an unrestricted battery or high-current adapter.
> 2. The TPA3255 output operates in Parallel Bridge-Tied Load (PBTL). **Both output terminals (`AMP_OUT_POS` and `AMP_OUT_NEG`) are floating bridge outputs.** Neither terminal may ever be connected to signal Ground, chassis Ground, or the oscilloscope probe ground clip! Use differential oscilloscope probes or floating battery-powered meters.
> 3. Verify analog rail voltages (+15V, +7.5V Vbias) before connecting op-amps or powering the TPA3255 amplifier module.
> 4. Test amplifier power output into an $8.0\ \Omega\ 100\text{W}$ non-inductive dummy load before connecting the Visaton BG 20 loudspeaker driver.
> 5. Never fabricate, assume, or copy simulated numbers into actual measurement fields. Keep simulated baselines in a separate column and record only real bench readings.

---

## 2. Theoretical Clarifications & CMRR Reconciliation

### 2.1 CMRR Analytical Worst-Case vs. SPICE Simulation
During Gate D review, a distinction was established between the mathematically guaranteed worst-case CMRR of discrete 0.1% resistors and the specific results produced by SPICE simulation:

For a classic single op-amp differential difference amplifier with ideal open-loop gain, the worst-case common-mode rejection ratio due to resistor tolerance $\epsilon_R$ is given by:
$$\text{CMRR}_{\text{wc}} \approx \frac{1 + A_d}{4 \epsilon_R}$$

Where:
- $A_d$ is the differential gain of the stage.
- $\epsilon_R$ is the fractional resistor tolerance ($\pm 0.1\% = 0.001$).

1. **Microphone Differential Preamplifier Stage ($U_{1\text{A}}$):**
   - $R_1 = R_3 = R_4 = 2.2\text{ k}\Omega$, $R_2 = R_5 = R_6 = 4.7\text{ k}\Omega$.
   - Differential gain $A_d = R_2 / R_1 = 4.7\text{ k} / 2.2\text{ k} = 2.1364$ ($+6.60\text{ dB}$).
   - Theoretical worst-case bound with independent $\pm 0.1\%$ resistors:
     $$\text{CMRR}_{\text{wc, mic}} \approx \frac{1 + 2.1364}{4 \times 0.001} = \frac{3.1364}{0.004} = 784.1 \implies \mathbf{57.89\text{ dB}}$$
   - *ngspice Simulation Result:* In `sim_d1_mic_preamp`, ngspice yielded **$71.28\text{ dB}$** at 60 Hz / 1 kHz because the nominal macromodel resistors matched closely and the NE5532 macromodel contributed finite internal common-mode rejection.
   - *Bench Testing Target:* **$\text{CMRR} \ge 40.0\text{ dB}$** mandatory minimum; typical bench measurement expected between **$50.0\text{ dB}$ and $65.0\text{ dB}$**.

2. **Line Differential Receiver Stage ($U_{2\text{B}}$):**
   - $R_{14} = R_{15} = 30\text{ k}\Omega$, $R_{16} = R_{17} = 10\text{ k}\Omega$.
   - Differential gain $A_d = R_{16} / R_{14} = 10\text{ k} / 30\text{ k} = 0.3333$ ($-9.54\text{ dB}$).
   - Theoretical worst-case bound with independent $\pm 0.1\%$ resistors:
     $$\text{CMRR}_{\text{wc, line}} \approx \frac{1 + 0.3333}{4 \times 0.001} = \frac{1.3333}{0.004} = 333.3 \implies \mathbf{50.46\text{ dB}}$$
   - *ngspice Simulation Result:* In `sim_d1_line_receiver`, ngspice yielded **$60.5\text{ dB}$**.
   - *Bench Testing Target:* **$\text{CMRR} \ge 40.0\text{ dB}$** mandatory minimum; typical bench measurement expected between **$48.0\text{ dB}$ and $58.0\text{ dB}$**.

Both physical circuits easily exceed the project acceptance criterion ($\ge 40.0\text{ dB}$), guaranteeing excellent immunity to 50/60 Hz stage ground hum and lighting EMI.

---

## 3. Required Test Equipment and Instrumentation

| Equipment | Specification | Intended Verification Task |
| :--- | :--- | :--- |
| **Bench DC Power Supply** | 0–40V DC, 0–5A adjustable, current-limiting | Stages E1, E2, E3, E4 (controlled bring-up) |
| **Digital Storage Oscilloscope (DSO)** | 2-channel or 4-channel, $\ge 100\text{ MHz}$, 1 GS/s | Signal swing, clipping, transient headroom, noise |
| **Differential Scope Probe / Isolator** | $10\times/100\times$, floating isolation | Measuring floating PBTL bridge speaker terminals |
| **True-RMS Digital Multimeter (DMM)** | $\ge 4.5\text{ digits}$, AC+DC True-RMS | Rail voltages, quiescent current, continuity, DC offset |
| **Low-Distortion Audio Signal Generator** | $10\text{ Hz to } 50\text{ kHz}$, balanced output | Preamp gain sweeps, HPF frequency response, CMRR |
| **Non-Inductive Power Dummy Load** | $8.0\ \Omega \pm 1\%, 100\text{W}$ rating (aluminum housed) | Amplifier power verification without acoustic hazard |
| **Contact Thermocouple / IR Thermometer** | Accuracy $\pm 1^\circ\text{C}$, range up to $150^\circ\text{C}$ | LM317HVT and TPA3255 heatsink thermal soak tests |
| **Audio Measurement Interface & Mic** | Calibrated measurement microphone (e.g. UMIK-1) + REW | Stage E5 acoustic response, SPL, port tuning ($F_b$) |
| **Audio Impedance Measurement Jig** | REW / DATS or known sense resistor method | Driver Thiele-Small verification, cabinet tuning $F_b$ |

---

## 4. Staged Verification Procedure

```
  +-------------------------------------------------------------------------------+
  | Stage E1: Cold Inspection & Continuity (Zero Power Applied, DMM Only)         |
  +-------------------------------------------------------------------------------+
                                         |
                                         v
  +-------------------------------------------------------------------------------+
  | Stage E2: Power Conditioning & Thermal Soak (Bench Supply 36V @ 50-100mA)     |
  +-------------------------------------------------------------------------------+
                                         |
                                         v
  +-------------------------------------------------------------------------------+
  | Stage E3: Small-Signal Audio Front-End (Gen + DSO, No Power Amp Connected)    |
  +-------------------------------------------------------------------------------+
                                         |
                                         v
  +-------------------------------------------------------------------------------+
  | Stage E4: Power Amplifier & Load Testing (TPA3255 PBTL into 8-Ohm Dummy Load) |
  +-------------------------------------------------------------------------------+
                                         |
                                         v
  +-------------------------------------------------------------------------------+
  | Stage E5: Transducer Integration & Acoustic Verification (Visaton BG 20 + Box)|
  +-------------------------------------------------------------------------------+
```

---

### Stage E1: Mechanical Inspection, Component Verification & Cold DC Checks
- **Objective:** Verify physical assembly, solder joint integrity, pinouts, and unpowered continuity before any voltage is introduced.
- **Visual Inspection Checkpoints:**
  1. **Q1 (IRF4905) TO-220 Pinout:**
     - Facing front of package (plastic face towards you, pins pointing down):
       - Pin 1 (Left) = Gate $\to$ Connected to $R_{22}$ / Zener $D_1$ Anode.
       - Pin 2 (Center & Mounting Tab) = Drain $\to$ Connected to fuse $F_1$ output (`DC_FUSE_OUT`).
       - Pin 3 (Right) = Source $\to$ Connected to internal protected bus (`+36V`).
     - *Diode Orientation:* The intrinsic body diode has Anode at Pin 2 (Drain) and Cathode at Pin 3 (Source).
  2. **Diodes Polarity:**
     - $D_1$ (12V Zener 1N4742A): Cathode band connected to Source (`+36V`); Anode connected to Gate (Pin 1).
     - $D_2$ (1N4007 reverse bypass): Cathode band to Pin 3 (Input) of LM317HVT; Anode to Pin 2 (Output, `+15V`).
     - $D_3$ (1N4007 cadj bypass): Cathode band to Pin 2 (Output); Anode to Pin 1 (Adj).
  3. **LM317HVT TO-220 Mounting Tab Isolation:**
     - **CRITICAL:** The mounting tab of LM317 is internally tied to Pin 2 (Output, `+15V`).
     - If the heatsink is in electrical contact with chassis ground, a mica/silicone insulating washer and nylon shoulder washer are **mandatory**.
     - Verify with DMM: Resistance between LM317 mounting tab and chassis ground must read **$\mathbf{> 1\text{ M}\Omega}$**.
  4. **Polarized Capacitors Orientation (Negative Stripe):**
     - $C_{17}$ ($470\ \mu\text{F} / 50\text{V}$): Negative stripe to `GND`.
     - $C_{20}$ ($100\ \mu\text{F} / 25\text{V}$): Negative stripe to `GND`.
     - $C_{22}$ ($10\ \mu\text{F} / 25\text{V}$): Negative stripe to `GND`.
     - $C_{23}$ ($47\ \mu\text{F} / 25\text{V}$): Negative stripe to `GND`.
     - Signal coupling electrolytics ($C_6, C_7, C_{14}, C_{15}$, $10\ \mu\text{F} / 25\text{V}$): Verify positive terminals face the DC bias (+7.5V virtual ground side).
  5. **IC Socket / Op-Amp Notch Alignment:**
     - $U_1, U_2, U_3$ (NE5532P): Verify pin 1 index notch. Pin 8 must connect to `+15V`, Pin 4 must connect to `GND`.
- **Cold Continuity Measurements (DMM Resistance Mode):**
  - **Measurement E1.1 (DC Input J3 to GND):** Measure resistance across J3 input terminals. Must read $> 100\text{ k}\Omega$ (no direct solder bridge).
  - **Measurement E1.2 (`+36V` to `GND`):** Probe between protected bus and signal GND. Meter reading should start low as $C_{17}$ charges from the DMM test voltage, then climb steadily to **$> 10\text{ k}\Omega$** (nominal divider $R_{21} + R_{22} = 40.2\text{ k}\Omega$).
  - **Measurement E1.3 (`+15V` to `GND`):** Probe between LM317 output and signal GND. Resistance must read **$> 2\text{ k}\Omega$** (nominal divider $R_{27} + R_{28} = 2.44\text{ k}\Omega$).
  - **Measurement E1.4 (`VBIAS_7V5` to `GND`):** Probe between $U_{3\text{A}}$ Pin 1 and signal GND. Resistance must read **$> 5\text{ k}\Omega$**.
  - **Measurement E1.5 (Chassis Ground Bond):** Probe between XLR pin 1 / chassis lug and signal ground. With J4 ground jumper installed, resistance must read **$< 0.5\ \Omega$**.
  - **Measurement E1.6 (Floating PBTL Speaker Terminals Isolation):** Probe between `AMP_OUT_POS` and `GND`, and between `AMP_OUT_NEG` and `GND`. Both must read **$> 1\text{ M}\Omega$** (completely floating).
- **Success Gate E1:** All visual checks confirmed; all cold continuity readings within specified bounds. **DO NOT APPLY POWER until Stage E1 is signed off.**

---

### Stage E2: Protection, Linear Regulation & Thermal Soak Verification
- **Objective:** Validate reverse-polarity isolation, +15V regulation, virtual ground buffer, and LM317 thermal stability under controlled bench current limit.
- **Procedure:**
  1. **Low-Current Forward Power-Up:**
     - Set bench power supply to $+36.0\text{V}$ with current limit set to **$100\text{ mA}$**.
     - Connect to J3 DC input. Switch on bench supply.
     - Measure current draw: must be between **$25\text{ mA}$ and $45\text{ mA}$** (3x NE5532 quiescent + dividers).
     - Measure voltage drop across Q1 ($V_{\text{DS}}$): must read $\le 30\text{ mV}$.
     - Measure Gate-Source voltage ($V_{\text{GS}}$): must read $-12.0\text{V} \pm 0.5\text{V}$ (Zener clamp active).
  2. **Reverse-Polarity Stress Test:**
     - Power down bench supply. Set current limit to **$50\text{ mA}$**.
     - Invert input polarity: apply **$-36.0\text{V}$** to J3 DC input.
     - Measure current draw on bench supply: must read **$0.00\text{ mA}$** ($< 10\ \mu\text{A}$ on sensitive DMM).
     - Measure voltage on internal `+36V` rail: must read **$0.00\text{V} \pm 10\text{ mV}$**.
     - Confirm fuse F1 does not blow.
  3. **Linear Regulator & Virtual Ground Measurements:**
     - Reconnect normal $+36.0\text{V}$ polarity.
     - Measure LM317 output voltage: must read **$+15.0\text{V} \pm 0.3\text{V}$** DC.
     - Measure `VBIAS_7V5` buffer output (U3A Pin 1): must read **$+7.50\text{V} \pm 0.15\text{V}$** DC.
     - Measure AC ripple on +15V rail with oscilloscope (AC coupling, 20 MHz BW limit): must be $< 1.0\text{ mV}_{\text{RMS}}$.
  4. **Thermal Soak Test (LM317HVT):**
     - Attach thermocouple to the mounting tab of LM317HVT / aluminum clip-on heatsink.
     - Run under normal operating current ($37\text{ mA}$) for 30 minutes at room ambient ($\sim 25^\circ\text{C}$).
     - Record stabilized heatsink temperature: must not exceed **$55^\circ\text{C}$** at $25^\circ\text{C}$ ambient (extrapolating to $< 75^\circ\text{C}$ at $45^\circ\text{C}$ stage ambient).
- **Success Gate E2:** Reverse polarity fully blocked; rails regulate within $\pm 2\%$; heatsink stabilizes with $> 45^\circ\text{C}$ margin.

---

### Stage E3: Small-Signal Audio Front-End Verification
- **Objective:** Measure gain range, CMRR, dynamic headroom, and Common HPF transfer function without power amplifier connected.
- **Procedure:**
  1. **Microphone Preamp (Mode A):**
     - Select Mode A on SW1 (confirm Pin 5 `MODE_STATUS` reads $+15\text{V}$).
     - Inject balanced $5.0\text{ mV}_{\text{RMS}}$ ($14.1\text{ mV}_{\text{pp}}$) 1 kHz sine into XLR J1 (Pins 2 and 3).
     - Measure output at Mic Vol pot top (C7):
       - With RV1 at minimum (fully CCW): Gain must be **$+20.0\text{ dB} \pm 1.0\text{ dB}$** ($50\text{ mV}_{\text{RMS}}$).
       - With RV1 at maximum (fully CW): Gain must be **$+50.5\text{ dB} \pm 1.5\text{ dB}$** ($1.67\text{ V}_{\text{RMS}}$).
       - Inspect waveform on DSO: must show clean, undistorted sine wave without clipping.
     - **Mic CMRR Measurement:**
       - Tie Pins 2 and 3 together; inject $1.0\text{ V}_{\text{RMS}}$ common-mode signal at 60 Hz and 1 kHz.
       - Measure output voltage; compute $\text{CMRR} = 20 \log_{10}(V_{\text{diff\_out}} / V_{\text{cm\_out}})$.
       - Criterion: **$\text{CMRR} \ge 40.0\text{ dB}$** (target $\ge 50\text{ dB}$).
  2. **Line Receiver & Headroom (Mode B):**
     - Select Mode B on SW1 (confirm Pin 5 `MODE_STATUS` reads $0\text{V}$).
     - Inject balanced $+4.0\text{ dBu}$ ($1.228\text{ V}_{\text{RMS}}$) 1 kHz sine into Combo J2.
     - Measure output at Line Vol pot top (C15): must read **$0.41\text{ V}_{\text{RMS}} \pm 0.03\text{ V}_{\text{RMS}}$** ($-9.54\text{ dB}$ gain).
     - **Stress Headroom Test (+22.0 dBu):**
       - Increase input generator to $+22.0\text{ dBu}$ ($9.75\text{ V}_{\text{RMS}} = 13.79\text{ V}_{\text{pk}}$ differential).
       - Inspect U2B Pin 7 on DSO: waveform must show clean sine swinging between $\sim 2.9\text{V}$ and $\sim 12.1\text{V}$.
       - Verify $> 1.0\text{V}$ headroom margin to both rails ($+1.8\text{V}$ and $+13.2\text{V}$) with **zero clipping**.
     - **Line CMRR Measurement:**
       - Tie Line Hot and Cold together; inject $2.0\text{ V}_{\text{RMS}}$ at 60 Hz and 1 kHz.
       - Criterion: **$\text{CMRR} \ge 40.0\text{ dB}$**.
  3. **Common 60 Hz 2nd-Order Sallen-Key HPF Verification:**
     - Measure frequency response at `AMP_INPUT_SIG` (J5 Pin 1) while sweeping generator from 10 Hz to 500 Hz:
       - Set reference at 1 kHz ($0\text{ dB}$).
       - 100 Hz: attenuation must be $< 0.8\text{ dB}$.
       - 60 Hz: attenuation must be **$-3.0\text{ dB} \pm 0.5\text{ dB}$** ($f_c = 60\text{ Hz} \pm 3\text{ Hz}$).
       - 50 Hz: attenuation must be $-4.8\text{ dB} \pm 0.8\text{ dB}$.
       - 25 Hz: attenuation must be **$\le -15.0\text{ dB}$** (verify sub-bass protection).
     - Switch between Mode A and Mode B: **confirm that the HPF attenuation profile applies identically to both inputs!**
- **Success Gate E3:** All gain, CMRR, headroom, and HPF criteria validated on bench.

---

### Stage E4: Power Amplifier Testing into 8-Ohm Dummy Load
- **Objective:** Verify TPA3255 PBTL amplifier output, continuous power, burst headroom, and floating bridge isolation before connecting the speaker.
- **Procedure:**
  1. Connect J4/J6 power leads from the protected +36V rail to the TPA3255 board.
  2. Connect an $8.0\ \Omega\ 100\text{W}$ non-inductive dummy load across `AMP_OUT_POS` and `AMP_OUT_NEG`.
  3. **Floating Bridge Isolation Check:**
     - Using DMM on DC volts, measure between `AMP_OUT_POS` and signal `GND`: reads approximately $+18\text{V}$ DC (half-supply).
     - Measure between `AMP_OUT_NEG` and signal `GND`: reads approximately $+18\text{V}$ DC.
     - Measure between `AMP_OUT_POS` and `AMP_OUT_NEG`: must read **$\le 50\text{ mV}$ DC offset**.
     - Confirm zero continuity to chassis ground.
  4. **Continuous Rated Power Test (10.0 W RMS):**
     - Inject 1 kHz sine into Line In; adjust RV3 until the True-RMS voltage across the $8\ \Omega$ dummy load reads **$8.94\text{ V}_{\text{RMS}}$** ($12.65\text{ V}_{\text{pk}}$).
     - Calculate power: $P = (8.94)^2 / 8.0 = \mathbf{10.0\text{ W RMS}}$.
     - Inspect waveform on DSO using differential probe: verify pure sine wave with $\text{THD+N} < 0.1\%$ (visually distortion-free).
     - Run continuous soak for 15 minutes; monitor TPA3255 heatsink temperature with thermocouple ($T_{\text{heatsink}} < 60^\circ\text{C}$).
  5. **Dynamic Peak Burst Test (48 W to 64 W Peak):**
     - Apply a 1 kHz tone burst (10 cycles ON, 100 cycles OFF) or brief transient pulse.
     - Increase drive until peak voltage reaches **$25.3\text{ V}_{\text{pk}}$** (40W burst) and up to **$32.0\text{ V}_{\text{pk}}$** (64W burst).
     - Verify clean burst envelope on DSO without power-supply sagging or amplifier rail collapse.
- **Success Gate E4:** Clean 10 W RMS continuous power; unclipped 64 W burst headroom; floating bridge confirmed; amplifier thermal stability validated.

---

### Stage E5: Transducer Integration, Cabinet Tuning, and Acoustic Measurements
- **Objective:** Mount Visaton BG 20 in 25 L wedge enclosure, tune port, measure acoustic transfer function, and evaluate RLC contour filter.
- **Procedure:**
  1. **Cabinet Assembly & Port Tuning ($F_b$):**
     - Mount Visaton BG 20 in 25 L net wedge cabinet with silicone sealing gasket and M4 tee-nuts.
     - Connect REW / DATS impedance measurement jig to speaker terminals.
     - Run impedance sweep from 20 Hz to 200 Hz.
     - Locate the saddle minimum between the two bass impedance peaks: this is the port resonance $F_b$.
     - Adjust PVC port length (nominal physical cut **91.2 mm**):
       - If $F_b > 52\text{ Hz}$: extend port slightly.
       - If $F_b < 48\text{ Hz}$: trim port slightly.
       - Final Target: **$F_b = 50.0\text{ Hz} \pm 2\text{ Hz}$**.
  2. **Acoustic Gated Frequency Response & SPL Measurement:**
     - Position active monitor in wedge position (facing up at $45^\circ$).
     - Place calibrated measurement microphone at $1.0\text{ m}$ on-axis.
     - Perform gated sine-sweep measurement (5 ms reflection gate) using REW.
     - Verify sensitivity: at $2.83\text{ V}_{\text{RMS}}$ ($1\text{ W}$ into $8\ \Omega$), baseline output should reach **$92\text{ dB} \pm 2\text{ dB}$ SPL at 1 m**.
     - Verify maximum continuous clean output: at 10 W RMS ($8.94\text{ V}_{\text{RMS}}$), measured SPL should reach **$102\text{ dB} \pm 2\text{ dB}$ SPL at 1 m** ($96\text{ dB}$ SPL at 2 m).
  3. **Passive RLC Contour Filter A/B Listening & Verification:**
     - Measure on-axis acoustic frequency response with SW2 Open (RLC Active) versus SW2 Closed (Bypassed).
     - Confirm that activating the filter introduces a smooth **$-4.5\text{ dB} \pm 1.0\text{ dB}$ contour** between 1.0 kHz and 2.5 kHz, taming whizzer cone harshness.
     - Perform listening tests with vocal dynamic microphone (Shure SM58) and acoustic guitar.
     - Evaluate vocal clarity, presence, and feedback rejection at 1.5 m listening distance.
- **Success Gate E5:** Cabinet tuned to $50\text{ Hz} \pm 2\text{ Hz}$; SPL reaches 102 dB at 1 m without port chuffing; vocal tone natural and articulate with RLC filter active.

---

## 5. Comprehensive Hardware Verification & Actual Measurement Matrix

> [!IMPORTANT]
> **Measurement Record Rules:**
> - `SPICE Baseline` reflects the validated Gate D digital simulation.
> - `Actual Measurement` and `Instrument / Serial` MUST be filled strictly from physical bench tests.
> - Status begins at **NOT TESTED** or **PENDING** and is updated only upon user submission of verified readings.

| Test ID | Test Condition | Expected Range | SPICE Baseline | Actual Measurement | Instrument / Serial | Status | Notes |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **E1.1** | DC Input J3 to GND (Unpowered) | $> 100\text{ k}\Omega$ | N/A | [ Blank ] | [ Blank ] | NOT TESTED | Cold DMM resistance check |
| **E1.2** | `+36V` Bus to GND (Unpowered) | $> 10\text{ k}\Omega$ (rises as C17 charges) | $40.2\text{ k}\Omega$ | [ Blank ] | [ Blank ] | NOT TESTED | Divider $R_{21}+R_{22}$ check |
| **E1.3** | `+15V` Rail to GND (Unpowered) | $> 2.0\text{ k}\Omega$ | $2.44\text{ k}\Omega$ | [ Blank ] | [ Blank ] | NOT TESTED | Divider $R_{27}+R_{28}$ check |
| **E1.4** | `VBIAS_7V5` to GND (Unpowered) | $> 5.0\text{ k}\Omega$ | $> 100\text{ k}\Omega$ | [ Blank ] | [ Blank ] | NOT TESTED | Op-amp rail check |
| **E1.5** | Chassis Ground Bond (J4 installed) | $< 0.5\ \Omega$ | $0.0\ \Omega$ | [ Blank ] | [ Blank ] | NOT TESTED | Shell to signal GND |
| **E1.6** | PBTL Bridge Outputs to GND/Chassis | $> 1.0\text{ M}\Omega$ | $> 10\text{ M}\Omega$ | [ Blank ] | [ Blank ] | NOT TESTED | Both POS & NEG isolated |
| **E1.7** | Q1 Pinout & D1 Zener Polarity | Pin 1 G, 2 D, 3 S; D1 Cathode to S | Confirmed | [ Blank ] | [ Blank ] | NOT TESTED | Visual & diode test |
| **E1.8** | LM317HVT Heatsink Tab Isolation | $> 1.0\text{ M}\Omega$ to chassis | Isolated | [ Blank ] | [ Blank ] | NOT TESTED | Tab is Pin 2 (+15V) |
| **E1.9** | Polarized Capacitors & IC Orientation | C17, C20, C22, C23, C6, C7, C14, C15, U1–U3 | Confirmed | [ Blank ] | [ Blank ] | NOT TESTED | Visual inspection |
| **E2.1** | Quiescent Current (+36V, 100mA limit) | $25\text{ mA} \text{ to } 45\text{ mA}$ | $36.9\text{ mA}$ | [ Blank ] | [ Blank ] | PENDING | Bench supply reading |
| **E2.2** | Q1 Forward Voltage Drop ($V_{\text{DS}}$) | $\le 30\text{ mV}$ | $25.6\text{ mV}$ | [ Blank ] | [ Blank ] | PENDING | P-MOSFET enhanced |
| **E2.3** | Q1 Gate-Source Voltage ($V_{\text{GS}}$) | $-12.0\text{V} \pm 0.5\text{V}$ | $-12.00\text{V}$ | [ Blank ] | [ Blank ] | PENDING | D1 Zener clamp active |
| **E2.4** | Reverse Polarity Current (-36V DC) | $< 10\ \mu\text{A}$ ($0.00\text{ mA}$ on supply) | $1.07\text{ nA}$ | [ Blank ] | [ Blank ] | PENDING | Reverse polarity block |
| **E2.5** | Internal Rail Voltage under -36V In | $0.00\text{V} \pm 10\text{ mV}$ | $0.00\text{V}$ | [ Blank ] | [ Blank ] | PENDING | Reverse protection bus |
| **E2.6** | LM317HVT Regulated Output (+15V) | $+15.0\text{V} \pm 0.3\text{V}$ | $+15.02\text{V}$ | [ Blank ] | [ Blank ] | PENDING | Regulated analog rail |
| **E2.7** | Virtual Ground Buffer (`VBIAS_7V5`) | $+7.50\text{V} \pm 0.15\text{V}$ | $+7.50\text{V}$ | [ Blank ] | [ Blank ] | PENDING | $U_{3\text{A}}$ buffer output |
| **E2.8** | +15V Rail AC Ripple & Noise | $< 1.0\text{ mV}_{\text{RMS}}$ (20 MHz BW) | $< 0.1\text{ mV}$ | [ Blank ] | [ Blank ] | PENDING | DSO AC coupling |
| **E2.9** | LM317HVT Heatsink Temp (30 min) | $T_{\text{heatsink}} \le 55^\circ\text{C}$ (at $25^\circ\text{C}$ amb) | $49.7^\circ\text{C}$ | [ Blank ] | [ Blank ] | PENDING | Thermocouple contact |
| **E3.1** | Mic Preamp Min Gain (RV1 CCW, 1 kHz) | $+20.0\text{ dB} \pm 1.0\text{ dB}$ ($50\text{ mV}_{\text{RMS}}$) | $+20.0\text{ dB}$ | [ Blank ] | [ Blank ] | PENDING | 5mV RMS input |
| **E3.2** | Mic Preamp Max Gain (RV1 CW, 1 kHz) | $+50.5\text{ dB} \pm 1.5\text{ dB}$ ($1.67\text{ V}_{\text{RMS}}$) | $+50.8\text{ dB}$ | [ Blank ] | [ Blank ] | PENDING | 5mV RMS input |
| **E3.3** | Mic CMRR (60 Hz & 1 kHz) | $\ge 40.0\text{ dB}$ (target $\ge 50\text{ dB}$) | $71.28\text{ dB}$ (typ) / $57.9\text{ dB}$ (wc) | [ Blank ] | [ Blank ] | PENDING | Tied Hot+Cold (1V RMS) |
| **E3.4** | Line Receiver Gain (+4 dBu / 1.228V in) | $-9.54\text{ dB} \pm 0.5\text{ dB}$ ($0.41\text{ V}_{\text{RMS}}$) | $-9.54\text{ dB}$ | [ Blank ] | [ Blank ] | PENDING | 1 kHz sine |
| **E3.5** | Line Headroom (+22 dBu / 9.75V RMS in) | Clean unclipped sine ($> 1\text{V}$ margin) | Clean $9.15\text{ V}_{\text{pp}}$ swing | [ Blank ] | [ Blank ] | PENDING | $U_{2\text{B}}$ pin 7 on DSO |
| **E3.6** | Line CMRR (60 Hz & 1 kHz) | $\ge 40.0\text{ dB}$ (target $\ge 50\text{ dB}$) | $60.5\text{ dB}$ (typ) / $50.5\text{ dB}$ (wc) | [ Blank ] | [ Blank ] | PENDING | Tied Hot+Cold (2V RMS) |
| **E3.7** | Common HPF Cutoff Frequency ($f_c$) | $60.0\text{ Hz} \pm 3.0\text{ Hz}$ (-3.0 dB point) | $59.2\text{ Hz}$ | [ Blank ] | [ Blank ] | PENDING | Frequency sweep |
| **E3.8** | Common HPF Attenuation at 25 Hz | $\le -15.0\text{ dB}$ relative to 1 kHz | $-15.35\text{ dB}$ | [ Blank ] | [ Blank ] | PENDING | Sub-bass protection |
| **E3.9** | Mode A vs Mode B HPF Consistency | Curve matches within $\pm 0.2\text{ dB}$ | Identical | [ Blank ] | [ Blank ] | PENDING | Verify SW1 wiper routing |
| **E4.1** | PBTL DC Output Bias to GND | $+18.0\text{V} \pm 1.0\text{V}$ DC (both pins) | $+18.0\text{V}$ | [ Blank ] | [ Blank ] | PENDING | Floating half-supply |
| **E4.2** | PBTL Differential DC Offset | $\le 50\text{ mV}$ DC across POS/NEG | $< 10\text{ mV}$ | [ Blank ] | [ Blank ] | PENDING | Measured across load |
| **E4.3** | Continuous Power into $8.0\ \Omega$ (1 kHz) | $8.94\text{ V}_{\text{RMS}} \pm 0.2\text{ V}$ ($10.0\text{ W}$) | $8.94\text{ V}_{\text{RMS}}$ | [ Blank ] | [ Blank ] | PENDING | Non-inductive dummy load |
| **E4.4** | Continuous Power THD+N & Waveform | $\text{THD} < 0.1\%$, clean sine on DSO | Pure sine | [ Blank ] | [ Blank ] | PENDING | Differential probe |
| **E4.5** | Amplifier Heatsink Soak (15 min @ 10W) | $T_{\text{sink}} < 60^\circ\text{C}$ (at $25^\circ\text{C}$ amb) | $< 52^\circ\text{C}$ | [ Blank ] | [ Blank ] | PENDING | Thermocouple contact |
| **E4.6** | Dynamic Burst Output into $8.0\ \Omega$ | $25.3\text{--}32.0\text{ V}_{\text{pk}}$ (40W–64W burst) | Up to $32.0\text{ V}_{\text{pk}}$ unclipped | [ Blank ] | [ Blank ] | PENDING | Tone burst / pulse |
| **E5.1** | Cabinet Port Resonance ($F_b$) | $50.0\text{ Hz} \pm 2.0\text{ Hz}$ | $50.0\text{ Hz}$ | [ Blank ] | [ Blank ] | PENDING | Impedance sweep trough |
| **E5.2** | Driver Free-Air Resonance ($f_s$) | $38\text{ Hz} \pm 4\text{ Hz}$ | $38\text{ Hz}$ | [ Blank ] | [ Blank ] | PENDING | Impedance sweep peak |
| **E5.3** | Sensitivity SPL at 1 m (2.83V RMS, 1W) | $92.0\text{ dB} \pm 2.0\text{ dB}$ SPL | $92\text{ dB}$ SPL | [ Blank ] | [ Blank ] | PENDING | Calibrated mic in REW |
| **E5.4** | Max Continuous SPL at 1 m (8.94V, 10W) | $\ge 102.0\text{ dB}$ SPL ($96\text{ dB}$ @ 2 m) | $102\text{ dB}$ SPL | [ Blank ] | [ Blank ] | PENDING | Clean continuous drive |
| **E5.5** | Port Chuffing / Turbulence at 10 W RMS | Zero audible chuffing ($v_p < 15\text{ m/s}$) | $v_p = 5.7\text{ m/s}$ | [ Blank ] | [ Blank ] | PENDING | 50 Hz sine drive |
| **E5.6** | RLC Contour Attenuation (1.0–2.5 kHz) | $-4.5\text{ dB} \pm 1.0\text{ dB}$ dip | $-4.6\text{ dB}$ at $1.5\text{--}2.3\text{ kHz}$ | [ Blank ] | [ Blank ] | PENDING | Acoustic gated sweep |
| **E5.7** | Vocal Clarity & Feedback Margin | Articulate tone, stable gain before feedback | Pass | [ Blank ] | [ Blank ] | PENDING | Shure SM58 listening test |

---

## 6. Immediate Action Item: Stage E1 Measurement Entry Form

Please execute the physical visual inspection and cold continuity checks as detailed in **Section 4 (Stage E1)** using your DMM before applying any DC power.

Fill in your actual measured values and instrument details below:

```markdown
### Stage E1 Cold Verification Submission Form

- Multimeter Model & Calibration / Serial: [ e.g., Fluke 87V, sn: 12345678 ]
- Ambient Temperature: [ e.g., 26 °C ]

1. Visual Checks:
   [ ] Q1 IRF4905 pinout verified (Pin 1 Gate, Pin 2 Drain to Fuse, Pin 3 Source to +36V bus)
   [ ] D1 12V Zener polarity verified (Cathode to Source / +36V, Anode to Gate)
   [ ] D2 & D3 1N4007 polarities verified across LM317HVT
   [ ] LM317HVT heatsink tab is electrically isolated from chassis ground (Resistance: _____ MΩ)
   [ ] Electrolytic capacitors C17, C20, C22, C23, C6, C7, C14, C15 orientations verified
   [ ] NE5532P op-amps U1, U2, U3 notch orientation verified (Pin 8 = +15V, Pin 4 = GND)

2. Cold Resistance Measurements (Power OFF, Capacitors Discharged):
   - E1.1 J3 DC Input to GND: ____________ kΩ  (Expected: > 100 kΩ)
   - E1.2 +36V Bus to GND: ____________ kΩ    (Expected: climbing to > 10 kΩ, nominal 40.2 kΩ)
   - E1.3 +15V Rail to GND: ____________ kΩ   (Expected: > 2.0 kΩ, nominal 2.44 kΩ)
   - E1.4 VBIAS_7V5 to GND: ____________ kΩ   (Expected: > 5.0 kΩ)
   - E1.5 Chassis Ground Bond (J4): ______ Ω  (Expected: < 0.5 Ω)
   - E1.6 PBTL Out POS to GND: ___________ MΩ (Expected: > 1.0 MΩ)
   - E1.6 PBTL Out NEG to GND: ___________ MΩ (Expected: > 1.0 MΩ)

3. Discrepancies or Irregularities Observed:
   [ None / Describe any solder bridge, component deviation, or unusual reading ]
```

> [!WARNING]
> Do NOT connect the 36V power adapter, bench supply, or loudspeaker driver until these cold checks are reviewed and confirmed!
