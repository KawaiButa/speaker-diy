# Comprehensive KiCad PCB Layout & Routing Report
**Project:** DIY Active Stage Monitor — Analog Preamp, Filter & Power Conditioning PCB  
**Design File:** [`live-pa-system.kicad_pcb`](file:///home/kawaiibuta/Projects/speaker-diy/projects/live-pa-system/live-pa-system.kicad_pcb)  
**Schematic:** [`live-pa-system.kicad_sch`](file:///home/kawaiibuta/Projects/speaker-diy/projects/live-pa-system/live-pa-system.kicad_sch)  
**Status:** 100% Routed & Silkscreen Verified (DRC 0 Errors, 0 Unconnected Nets)  
**Date:** October 15, 2026  

---

## 1. Executive Summary & Routing Status

The custom 2-layer PCB layout for the **DIY Active Stage Monitor** has been fully routed and detailed with complete top and bottom silkscreen markings:

- **Board Dimensions:** $180.0\text{ mm} \times 110.0\text{ mm}$, $1.6\text{ mm}$ FR4, $1\text{ oz}$ ($35\ \mu\text{m}$) copper.
- **Mounting:** 4 $\times$ M3 mounting holes (`H1`–`H4`) with $5.0\text{ mm}$ corner inset and $6.0\text{ mm}$ keepout diameter.
- **Routing Completion:** **100% Complete — 0 Unconnected Nets** (355 routed track segments: 203 on `B.Cu` solder side, 152 on `F.Cu` component side, 5 interlayer vias).
- **Bottom Silkscreen (`B.SilkS`):** Comprehensive legend including board identification, all connector pinouts (`J1`–`J7`), switch and potentiometer indicators (`SW1`, `SW2`, `RV1`–`RV3`), test point `TP1`, and prominent safety warnings.
- **Physical DRC Status:** **0 short circuits, 0 clearance errors, 0 courtyard overlaps, 0 hole-to-hole violations, 0 unconnected items**.

```
=================================================================================================
                                   TOP VIEW (COMPONENT SIDE F.Cu)
+-----------------------------------------------------------------------------------------------+
| H1 [5,5]                                                                              H2 [175,5]
|                                                                                               |
|  [J1: XLR In]      [J2: Combo In]     [ZONE 3: VBIAS]      [J4: 36V Out]  [J3: DC In]  [F1]   |
|                                         U3 (NE5532)        [Q1: IRF4905]   [C17: 470uF]       |
|  ZONE 1: MIC PRE   ZONE 2: LINE & HPF                      [U4: LM317HVT]  [C18: 100nF]       |
|  U1 (NE5532)       U2 (NE5532)                             ZONE 4: POWER & +15V REG           |
|                                                                                               |
|  [RV1: Gain]       [RV3: Line Vol]                                 [L1: 1.0mH Choke]          |
|  [RV2: Mic Vol]    [SW1: Mode Sel]     [J5: To Amp]        [J6: Spk In]    [J7: To Spk]     |
|                                                            [SW2: Bypass]   [C24: 4.7uF]       |
|                                                            [R23: 10W Res]  ZONE 5: RLC        |
| H4 [5,105]                                                                            H3 [175,105]
+-----------------------------------------------------------------------------------------------+
                                  BOTTOM VIEW (SOLDER SIDE B.Cu)
+-----------------------------------------------------------------------------------------------+
| H2 [175,5]                                                                            H1 [5,5]
|  [ZONE 4: POWER & +15V]   [ZONE 3: VBIAS]     [ZONE 2: LINE/HPF]      [ZONE 1: MIC PREAMP]    |
|   J3: +36V DC IN           U3: VBIAS BUFFER    J2: BAL LINE IN (COMBO) J1: BAL MIC IN         |
|   J4: 36V TO AMP                                1/S:GND 2/T:+ 3/R:-     1:GND 2:HOT 3:COLD    |
|   F1: 5A FUSE                                  U2: LINE & HPF          U1: NE5532 PRE         |
|   U4: LM317 (TAB=+15V)                                                                        |
|                                                                                               |
|  [ZONE 5: RLC & PBTL SPK]          [ SAFETY NOTICE: PBTL FLOATING +18V ]                      |
|   J6: AMP PBTL IN (+/-)    SW2: BYPASS         SW1: MODE SEL           RV1: GAIN              |
|   L1: 1.0mH CHOKE          R23: 8.2R 10W       J5: AUDIO TO AMP        RV2: MIC VOL           |
|   J7: TO BG 20 SPK (+/-)   C24: 4.7uF MKP                              RV3: LINE VOL          |
| H3 [175,105]                                                                          H4 [5,105]
+-----------------------------------------------------------------------------------------------+
```

---

## 2. Copper Routing Breakdown

| Copper Layer | Segment Count | Track Width Range | Purpose |
| :--- | :---: | :---: | :--- |
| **`B.Cu` (Bottom Solder Side)** | **203** | $0.30\text{ mm} \sim 2.50\text{ mm}$ | Primary routing layer for through-hole soldering, high-current $+36\text{ V}$ bus, and PBTL speaker tracks. |
| **`F.Cu` (Top Component Side)** | **152** | $0.30\text{ mm} \sim 2.50\text{ mm}$ | Cross-overs, analog small-signal audio links, and local decoupling returns. |
| **Vias (`Through`)** | **5** | Drill: $0.40\text{ mm}$, Size: $0.80\text{ mm}$ | Minimal via count preserving ground plane and trace integrity. |
| **Total Unconnected Nets** | **0** | — | **100% nets fully connected.** |

### Net Class Width Enforcement
1. **`Power_HighCurrent` ($2.50\text{ mm}$ / $98\text{ mil}$):** Used for `+36V`, `DC_IN_RAW`, and `DC_FUSE_OUT` to handle $5.0\text{ A}$ continuous DC with $\Delta T < 10^\circ\text{C}$ on $1\text{ oz}$ copper.
2. **`Speaker_Bridge` ($1.80\text{ mm}$ / $71\text{ mil}$):** Used for `AMP_OUT_POS`, `AMP_OUT_NEG`, and `SPK_OUT_POS` to provide low-impedance audio drive ($3.6\text{ A}_{\text{peak}}$) directly to the Visaton BG 20 driver.
3. **`Power_AnalogRegulated` ($0.60\text{ mm}$ / $24\text{ mil}$):** Used for $+15\text{ V}$ and virtual ground $+7.5\text{ V}$ distribution.
4. **`Signal_AnalogAudio` ($0.30\text{ mm}$ / $12\text{ mil}$):** Used for all 31 low-level balanced and single-ended audio signals.

---

## 3. Back Silkscreen (`B.SilkS`) Documentation

The solder side of the board contains 34 dedicated silkscreen legends (mirrored so they read naturally from left-to-right when inspecting the bottom):

1. **Board Title:** `LIVE-PA ACTIVE STAGE MONITOR — REV 2.1` & `ANALOG PREAMP, 60Hz HPF & POWER INTERFACE`.
2. **Connector Pinouts:**
   - **`J1` (Mic In):** `1:GND  2:HOT(+)  3:COLD(-)`
   - **`J2` (Line In Combo):** `1/S:GND  2/T:HOT  3/R:COLD`
   - **`J3` (DC In):** `+36V DC IN (2.1mm +)`
   - **`J4` (Amp Power):** `36V TO AMP`
   - **`J5` (Audio Out):** `AUDIO TO AMP`
   - **`J6` (PBTL In):** `AMP PBTL IN (+/-)`
   - **`J7` (Speaker Out):** `TO BG 20 SPK (+/-)`
3. **Controls & Test Points:**
   - `RV1: GAIN` ($20\text{ dB}$ to $54\text{ dB}$)
   - `RV2: MIC VOL`
   - `RV3: LINE VOL`
   - `SW1: MODE SELECT` (`VOCAL` / `MONITOR`)
   - `SW2: RLC BYPASS`
   - `TP1: HPF OUT`
4. **Critical Safety Warnings:**
   - `CAUTION: FLOATING PBTL SPEAKER OUTPUTS (J6, J7) ARE AT +18V DC.`
   - `DO NOT CONNECT ANY SPEAKER WIRE TO GROUND OR CHASSIS!`
   - `U4 LM317 METAL TAB IS AT +15V DC (NOT GROUND).`

---

## 4. Visual Inspection Assets

- **3D Bottom View (Solder Side with Tracks & Silkscreen):** [`live-pa-system-board-3d-bottom.png`](file:///home/kawaiibuta/Projects/speaker-diy/projects/live-pa-system/live-pa-system-board-3d-bottom.png)
- **3D Top View (Component Side):** [`live-pa-system-board-3d.png`](file:///home/kawaiibuta/Projects/speaker-diy/projects/live-pa-system/live-pa-system-board-3d.png)
- **2D Vector Layout Preview:** [`live-pa-system-board-preview.svg`](file:///home/kawaiibuta/Projects/speaker-diy/projects/live-pa-system/live-pa-system-board-preview.svg)
- **DRC Acceptance Report:** [`live-pa-system-pcb-drc.rpt`](file:///home/kawaiibuta/Projects/speaker-diy/projects/live-pa-system/live-pa-system-pcb-drc.rpt)
