# Gate E Prototyping Shopping List & Hardware Acquisition Guide
**Project:** DIY Active Stage Monitor — Gate E Universal Prototyping Implementation  
**Project Path:** [`projects/live-pa-system/`](file:///home/kawaiibuta/Projects/speaker-diy/projects/live-pa-system/)  
**Target Budget Ceiling:** Strictly $< 5,000,000\text{ VND}$  
**Date:** October 15, 2026  

---

## 1. Modular Prototyping Board Selection

To eliminate any requirement for custom PCB fabrication, CNC milling, or chemical etching, the physical implementation is partitioned across three standard, commercially available universal prototyping boards:

| Board Identifier | Functional Subsystem | Commercial Size | Grid Pitch & Dimensions | Quantity | Est. Unit Price (VND) | Total (VND) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Board A** | Audio Analog Front-End (Mic Preamp, Line Receiver, 60Hz HPF, Vbias Buffer) | **7 × 9 cm** | $2.54\text{ mm}$ pitch, $26 \times 31$ holes ($806$ pads), FR-4 | 1 | 22,000 | 22,000 |
| **Board B** | Low-Voltage Power Conditioning (IRF4905 P-FET, LM317HVT +15V Regulator) | **5 × 7 cm** | $2.54\text{ mm}$ pitch, $18 \times 24$ holes ($432$ pads), FR-4 | 1 | 12,000 | 12,000 |
| **Board C** | Passive RLC Contour Filter (1.0mH Choke, 8.2Ω 10W Resistor, 4.7µF MKP Cap) | **5 × 7 cm** | $2.54\text{ mm}$ pitch, $18 \times 24$ holes ($432$ pads), FR-4 | 1 | 12,000 | 12,000 |
| **Subtotal** | Prototyping Boards | — | — | 3 | — | **46,000** |

> [!TIP]
> **Preferred Board Specification:** Single-sided or double-sided plated-through-hole (PTH) FR-4 universal board with green solder mask and tinned circular pads. Avoid brown paper-phenolic (bakelite) perfboards, as copper pads easily delaminate during hand soldering and rework.

---

## 2. Prototyping Hardware, Sockets, Terminals & Wiring

These items are required to assemble the three prototyping boards cleanly and safely without PCB fabrication:

| Item Description | Detailed Specification | Qty | Vietnamese Search Keywords (Shopee / Lazada / Thegioiic) | Est. Cost (VND) |
| :--- | :--- | :---: | :--- | :---: |
| **DIP-8 IC Sockets** | 8-pin machined round-hole (gold-plated contact or tin-plated tulip contact) | 3 pcs | `đế ic 8 chân tròn dip-8`, `socket ic 8 chân` | 9,000 |
| **Screw Terminal Blocks (2-Pin)** | Pitch $5.08\text{ mm}$, interlocking, rated $\ge 250\text{ V} / 10\text{ A}$ (Phoenix/WJ128 type) | 6 pcs | `cọc đấu dây 2 pin 5.08mm`, `terminal block 2p 5.08` | 18,000 |
| **Screw Terminal Blocks (3-Pin)** | Pitch $5.08\text{ mm}$, interlocking, rated $\ge 250\text{ V} / 10\text{ A}$ | 3 pcs | `terminal block 3 pin 5.08mm`, `cọc nối 3p 5.08` | 12,000 |
| **Panel-Mount Fuse Holder** | $5 \times 20\text{ mm}$ chassis screw-cap holder, rated $250\text{ V} / 10\text{ A}$ | 1 pc | `hộp cầu chì 5x20 bắt panel`, `đế cầu chì 5x20 vặn` | 15,000 |
| **Cartridge Fuses (5×20mm)** | $3.15\text{ A}$ or $4.0\text{ A}$ Slow-Blow (T-type) or Fast (F-type) glass/ceramic | 3 pcs | `cầu chì ống 5x20 3.15A`, `cầu chì thủy tinh 5x20 4A` | 10,000 |
| **Panel DC Barrel Jack** | $5.5 \times 2.1\text{ mm}$ (or $2.5\text{ mm}$ matching external PSU), metal threaded nut | 1 pc | `jack nguồn dc 5.5x2.1 cái bắt vít kim loại` | 12,000 |
| **Panel XLR Female Receptacle** | Neutrik `NC3FD-L-1` or compatible D-series 3-pin XLR female with solder cups | 1 pc | `jack xlr cái bắt panel d-size`, `jack canon cái neutrik` | 35,000 |
| **Panel Combo XLR/TRS Jack** | Neutrik `NCJ6FI-S` (solder cup) or `NCJ6FI-H` (modified for point-to-point) | 1 pc | `jack combo xlr 6 ly cái neutrik ncj6fi` | 45,000 |
| **High-Current Hookup Wire (18 AWG)** | $18\text{ AWG}$ ($0.75\text{ mm}^2$ to $1.0\text{ mm}^2$) flexible silicone/PVC wire (Red, Black, Blue) | 3 m | `dây điện silicone 18awg`, `dây điện chịu nhiệt 18 awg` | 35,000 |
| **Signal Jumper Wire (24 AWG)** | $24\text{ AWG}$ ($0.5\text{ mm}$) solid tinned copper wire / insulated breadboard hookup wire | 1 spool | `dây đồng tráng thiếc 0.5mm`, `dây câu mạch 24awg` | 30,000 |
| **Wrap/Kynar Wire (30 AWG)** | $30\text{ AWG}$ Kynar/ETFE insulated fine wire for high-density audio point-to-point | 1 spool | `cuộn dây kynar 30awg`, `dây quấn mạch ok line` | 25,000 |
| **Heat-Shrink Tubing Kit** | Assorted diameters ($1.5\text{ mm}, 2.5\text{ mm}, 4.0\text{ mm}, 6.0\text{ mm}$) | 1 set | `ống co nhiệt cách điện`, `bộ gen co nhiệt` | 20,000 |
| **M3 PCB Standoff Spacers** | M3 $\times 10\text{ mm}$ hex nylon/brass standoffs + M3 screws & nuts (pack of 20) | 1 pack | `trụ đồng m3 10mm`, `trụ nhựa m3 10mm bắt pcb` | 25,000 |
| **TO-220 Heatsinks** | Aluminum clip-on or screw-on heatsink ($\theta_{\text{SA}} \le 20^\circ\text{C/W}$) for LM317 and IRF4905 | 2 pcs | `nhôm tản nhiệt to-220`, `tản nhiệt to220 có ốc` | 15,000 |
| **Silicone Insulating Pads** | TO-220 silicone thermal pads + plastic insulating bushings | 2 sets | `miếng lót cách điện to-220`, `núm nhựa cách điện to220` | 10,000 |
| **Cable Zip-Ties** | $100\text{ mm} \times 2.5\text{ mm}$ nylon cable ties (for mounting L1 inductor and securing cable bundles) | 1 pack | `dây rút nhựa 10cm`, `lạt nhựa 100mm` | 8,000 |
| **Subtotal** | Prototyping Hardware & Hookup Materials | — | — | — | **324,000** |

---

## 3. Existing BOM Components (From Verified Gate D Design)

These components are already specified in the approved Gate D design report and BOM:

| RefDes | Component Description | Value / Specification | Qty | Unit Price (VND) | Total (VND) |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **U1, U2, U3** | Dual Low-Noise Audio Op-Amp | `NE5532P` (Texas Instruments, DIP-8) | 3 | 15,000 | 45,000 |
| **U4** | High-Voltage Linear Regulator | `LM317HVT` ($V_{\text{in}} \le 60\text{ V}$, TO-220) | 1 | 25,000 | 25,000 |
| **Q1** | P-Channel Power MOSFET | `IRF4905` ($-55\text{ V}, -74\text{ A}, 20\text{ m}\Omega$, TO-220) | 1 | 28,000 | 28,000 |
| **D1** | Zener Gate-Protection Diode | `BZX79C12` ($12\text{ V} / 0.5\text{ W}$, DO-35) | 1 | 2,000 | 2,000 |
| **D2, D3** | Protection Diodes | `1N4007` ($1000\text{ V} / 1\text{ A}$, DO-41) | 2 | 1,000 | 2,000 |
| **R1, R2, R12, R13, R18, R24** | Metal Film Resistors | $100\text{ k}\Omega, 1/4\text{ W}, 1\%$ | 6 | 500 | 3,000 |
| **R3, R5** | Precision Matched Resistors | $2.2\text{ k}\Omega, 1/4\text{ W}, 0.1\%$ | 2 | 2,500 | 5,000 |
| **R4, R6** | Precision Matched Resistors | $4.7\text{ k}\Omega, 1/4\text{ W}, 0.1\%$ | 2 | 2,500 | 5,000 |
| **R7** | Metal Film Resistor | $47\text{ k}\Omega, 1/4\text{ W}, 1\%$ | 1 | 500 | 500 |
| **R8** | Metal Film Resistor | $330\ \Omega, 1/4\text{ W}, 1\%$ | 1 | 500 | 500 |
| **R9** | HPF Sallen-Key Resistor | $27\text{ k}\Omega, 1/4\text{ W}, 1\%$ | 1 | 500 | 500 |
| **R10** | Metal Film Resistor | $1.2\text{ k}\Omega, 1/4\text{ W}, 1\%$ | 1 | 500 | 500 |
| **R11** | HPF Sallen-Key Resistor | $56\text{ k}\Omega, 1/4\text{ W}, 1\%$ | 1 | 500 | 500 |
| **R14, R15** | Precision Matched Resistors | $30\text{ k}\Omega, 1/4\text{ W}, 0.1\%$ | 2 | 2,500 | 5,000 |
| **R16, R17** | Precision Matched Resistors | $10\text{ k}\Omega, 1/4\text{ W}, 0.1\%$ | 2 | 2,500 | 5,000 |
| **R19** | LM317 Program Resistor | $240\ \Omega, 1/4\text{ W}, 1\%$ | 1 | 500 | 500 |
| **R20** | LM317 Program Resistor | $2.64\text{ k}\Omega, 1/4\text{ W}, 1\%$ ($2.4\text{k} + 240\Omega$) | 1 | 1,000 | 1,000 |
| **R21, R22** | Virtual Ground Divider | $10\text{ k}\Omega, 1/4\text{ W}, 1\%$ | 2 | 500 | 1,000 |
| **R23** | Passive Contour Resistor | $8.2\ \Omega, 10\text{ W}$ Non-Inductive Wirewound | 1 | 35,000 | 35,000 |
| **RV1** | Mic Gain Potentiometer | $50\text{ k}\Omega$ Reverse-Logarithmic (Rev-Log / C50K) | 1 | 15,000 | 15,000 |
| **RV2, RV3** | Volume Potentiometers | $10\text{ k}\Omega$ Logarithmic (Audio Taper / A10K) | 2 | 12,000 | 24,000 |
| **SW1** | Mode Selector Switch | DPDT Slide Switch or Toggle Switch (Panel mount) | 1 | 12,000 | 12,000 |
| **SW2** | Contour Bypass Switch | SPST Heavy-Duty Slide or Mini Toggle Switch | 1 | 8,000 | 8,000 |
| **C1, C2, C10, C11** | RF Suppression Capacitors | $47\text{ pF} / 100\text{ V}$ Ceramic Disc / C0G | 4 | 1,000 | 4,000 |
| **C3, C16, C18, C21, C25, C26**| Supply Decoupling Capacitors| $100\text{ nF} / 50\text{ V}$ Monolithic Ceramic / Film | 6 | 1,500 | 9,000 |
| **C4, C5** | Mic AC Coupling Capacitors | $10\ \mu\text{F} / 50\text{ V}$ Non-Polar (Bi-Polar) Electrolytic | 2 | 4,000 | 8,000 |
| **C6, C7, C14, C15, C19, C22**| Interstage / Filter Caps | $10\ \mu\text{F} / 25\text{ V}$ Low-ESR Radial Electrolytic | 6 | 2,000 | 12,000 |
| **C8, C9** | HPF Sallen-Key Capacitors | $68\text{ nF} / 63\text{ V}$ Metallized Polyester/Polypropylene Film | 2 | 5,000 | 10,000 |
| **C12, C13** | Line AC Coupling Capacitors| $1.0\ \mu\text{F} / 63\text{ V}$ Metallized Film (MKT/MKP) | 2 | 6,000 | 12,000 |
| **C17** | Bulk Reservoir Capacitor | $470\ \mu\text{F} / 50\text{ V}$ Low-ESR ($105^\circ\text{C}$) Electrolytic | 1 | 12,000 | 12,000 |
| **C20** | Regulator Output Cap | $100\ \mu\text{F} / 25\text{ V}$ Low-ESR Electrolytic | 1 | 3,000 | 3,000 |
| **C23** | Virtual Ground Buffer Cap | $47\ \mu\text{F} / 25\text{ V}$ Low-ESR Electrolytic | 1 | 2,500 | 2,500 |
| **C24** | Passive Contour Capacitor | $4.7\ \mu\text{F} / 250\text{ V}$ MKP Polypropylene Film | 1 | 65,000 | 65,000 |
| **L1** | Passive Contour Choke | $1.0\text{ mH}$ Air-Core Inductor ($1.0\text{ mm}$ wire, $R_{\text{DC}} \le 0.35\ \Omega$) | 1 | 120,000 | 120,000 |
| **AMP** | Class-D Power Amplifier | Wuzhi ZK-3002 / TPA3255 PBTL mono module | 1 | 380,000 | 380,000 |
| **PSU** | External DC Power Supply | $36\text{ V} / 5\text{ A}$ ($180\text{ W}$) Switch-Mode DC Adapter | 1 | 350,000 | 350,000 |
| **SPK** | Loudspeaker Driver | Visaton BG 20 ($8\ \Omega$, $8\text{''}$ Full-Range) | 1 | 1,150,000 | 1,150,000 |
| **CAB** | Enclosure Materials | 15 mm MDF sheet, damping wool, port tube, screws, feet | 1 set | 650,000 | 650,000 |
| **Subtotal** | Major Components, Transducers & Cabinet | — | — | — | **3,037,500** |

---

## 4. Total Project Cost & Budget Verification

```
+---------------------------------------------------------------------------------+
| COST ITEM SUMMARY                                                    AMOUNT     |
+---------------------------------------------------------------------------------+
| 1. Transducers, Cabinet & Preassembled Modules (BG 20, TPA3255, 36V PSU, MDF):  |
|    - Visaton BG 20 driver:                                      1,150,000 VND   |
|    - Wuzhi ZK-3002 / TPA3255 PBTL amplifier module:               380,000 VND   |
|    - 36V 5A external DC power adapter:                            350,000 VND   |
|    - 15mm MDF enclosure materials, damping, port tube, hardware:  650,000 VND   |
|    Subtotal:                                                    2,530,000 VND   |
|                                                                                 |
| 2. Passive RLC Contour Components (L1 1.0mH, R23 10W, C24 MKP):   220,000 VND   |
|                                                                                 |
| 3. Analog Electronics, Op-Amps, Transistors & Passives:           287,500 VND   |
|                                                                                 |
| 4. Universal Prototyping Boards (1x 7x9cm, 2x 5x7cm):              46,000 VND   |
|                                                                                 |
| 5. Prototyping Hardware, DIP Sockets, Terminals, Wire, Standoffs: 324,000 VND   |
|                                                                                 |
| 6. Project Contingency Buffer (Shipping, consumables):            200,000 VND   |
+---------------------------------------------------------------------------------+
| TOTAL ESTIMATED BUILD COST:                                     3,607,500 VND   |
| HARD BUDGET LIMIT:                                              5,000,000 VND   |
| REMAINING BUDGET CONTINGENCY RESERVE:                           1,392,500 VND   |
+---------------------------------------------------------------------------------+
```

> [!NOTE]
> The total estimated materials cost is **3,607,500 VND**, which is **1,392,500 VND below the 5,000,000 VND ceiling**. This proves that switching to universal prototyping boards significantly reduces total expenditure while removing any dependency on external PCB fabrication.

---

## 5. Tools & Test Equipment Required for Home Assembly

To assemble and test this build at home, the following basic hobbyist tools and equipment are needed:

1. **Soldering Equipment:**
   - Temperature-controlled soldering iron ($40\text{ W} \sim 60\text{ W}$, set to $320^\circ\text{C} \sim 350^\circ\text{C}$).
   - High-quality leaded or lead-free solder wire with rosin flux core ($0.8\text{ mm}$ dia, e.g., 63/37 Sn/Pb or SAC305).
   - Soldering tip cleaner (brass wire ball or damp sponge).
   - Desoldering pump (solder sucker) and copper desoldering braid / wick ($2.0\text{ mm}$).
2. **Hand Tools:**
   - Flush wire cutters (diagonal micro-shears).
   - Precision needle-nose pliers (for bending component leads cleanly to $2.54\text{ mm}$ hole pitch).
   - Wire stripper ($18\text{ AWG}$ to $30\text{ AWG}$).
   - Screwdrivers (small flathead for terminal blocks, Phillips for M3 standoffs and enclosure).
   - Heat gun or lighter with flame spreader (for shrinking heat-shrink tubing).
3. **Bench Verification Test Equipment:**
   - **Digital Multimeter (DMM):** DC voltage, AC voltage, resistance, and continuity beeper (mandatory for Stage E1 and E2).
   - **Current-Limited Bench DC Power Supply:** Adjustable $0 \sim 30\text{ V}$ or $0 \sim 36\text{ V}$ with $0 \sim 1\text{ A}$ current limit (for safe initial bring-up in Stage E2).
   - **Audio Signal Source:** PC soundcard, smartphone with audio test generator app, or dedicated DDS signal generator (sine wave $20\text{ Hz} \sim 20\text{ kHz}$).
   - **Oscilloscope (Dual-Trace):** For verifying preamp gain, clipping margins, and 60 Hz HPF frequency response in Stage E3.
   - **$8\ \Omega / 50\text{ W} \sim 100\text{ W}$ Non-Inductive Dummy Load:** For amplifier load testing in Stage E4 before connecting the speaker.
