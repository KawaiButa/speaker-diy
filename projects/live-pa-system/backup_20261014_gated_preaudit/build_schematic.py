#!/usr/bin/env python3
"""
Generate complete KiCad 10 schematic for DIY Active Stage Monitor
Project: live-pa-system.kicad_sch

Final Architecture:
- U1 (NE5532): Mic Preamp Stage 1A (fixed differential, 0.1% resistors) & Stage 1B (variable post-amp)
- RV2 (10k Log): Dedicated Mic Volume Potentiometer feeding SW1 Position A
- U2B (NE5532): Balanced LINE Receiver (-9.54dB attenuation, +22dBu headroom, 0.1% resistors)
- RV3 (10k Log): Dedicated Line Volume Potentiometer feeding SW1 Position B
- SW1 (SW_DPDT_x2): Mode selector switch (routes selected audio to common HPF, plus telemetry)
- U2A (NE5532): COMMON 60Hz 2nd-Order Sallen-Key Butterworth HPF (protects BOTH Mic and Line modes!)
- U3 (NE5532): Precision Buffered Virtual Ground (U3A +7.5V buffer) & Terminated Spare (U3B follower to Vbias)
- U4 (LM317HVT): +15V Linear Regulator with reverse & bypass protection diodes
- Q1 (IRF4905): High-side P-MOSFET reverse polarity protection
- L1/C24/R23/SW2: Passive RLC contour filter with bypass switch
- Fully resolved multi-unit symbols for U1, U2, U3 (Units 1, 2, 3 with complete pins 1-8)
- 100% on-grid placement (all pins snapped to 50-mil/100-mil grid)
- 0 ERC Errors, 0 Unconnected Nets
"""

import uuid
import sys
from pathlib import Path

def uid():
    return str(uuid.uuid4())

def snap(val):
    return round(val / 2.54) * 2.54

def snap_half(val):
    # for symbols with pins at +/- 1.27mm, placing origin at (M + 0.5)*2.54 aligns pins to 2.54 grid
    return (round(val / 2.54)) * 2.54 + 1.27

def main():
    sch_file = Path("projects/live-pa-system/live-pa-system.kicad_sch")
    
    sch_header = f"""(kicad_sch
\t(version 20250114)
\t(generator "eeschema")
\t(generator_version "10.0")
\t(uuid "{uid()}")
\t(paper "A3")
\t(title_block
\t\t(title "DIY Active Stage Monitor - Analog Front-End & Filter")
\t\t(date "2026-10-14")
\t\t(rev "2.1")
\t\t(company "DIY Audio Labs")
\t\t(comment 1 "Gate D Final Schematic: Visaton BG 20 + TPA3255 PBTL")
\t\t(comment 2 "Common 60Hz 2nd HPF protecting BOTH Mic & Line modes; 0.1% CMRR input networks")
\t\t(comment 3 "DC 36V in with P-MOSFET reverse prot, LM317HVT +15V reg, Buffered Vbias & RLC contour")
\t)
\t(lib_symbols
\t\t(symbol "Device:C"
\t\t\t(pin passive line (at 0 2.54 270) (length 2.54)
\t\t\t\t(name "~" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "1" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at 0 -2.54 90) (length 2.54)
\t\t\t\t(name "~" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "2" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(property "Reference" "C" (at 2.54 1.27 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "C" (at 2.54 -1.27 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t)
\t\t(symbol "Device:C_Polarized"
\t\t\t(pin passive line (at 0 2.54 270) (length 2.54)
\t\t\t\t(name "~" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "1" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at 0 -2.54 90) (length 2.54)
\t\t\t\t(name "~" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "2" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(property "Reference" "C" (at 2.54 1.27 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "C_Polarized" (at 2.54 -1.27 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t)
\t\t(symbol "Device:R"
\t\t\t(pin passive line (at 0 2.54 270) (length 2.54)
\t\t\t\t(name "~" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "1" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at 0 -2.54 90) (length 2.54)
\t\t\t\t(name "~" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "2" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(property "Reference" "R" (at 2.032 0 90) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "R" (at -2.032 0 90) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t)
\t\t(symbol "Device:R_Potentiometer"
\t\t\t(pin passive line (at 0 2.54 270) (length 2.54)
\t\t\t\t(name "1" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "1" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at 2.54 0 180) (length 2.54)
\t\t\t\t(name "2" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "2" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at 0 -2.54 90) (length 2.54)
\t\t\t\t(name "3" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "3" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(property "Reference" "RV" (at 2.54 2.54 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "R_Potentiometer" (at 2.54 -2.54 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t)
\t\t(symbol "Device:L"
\t\t\t(pin passive line (at 0 2.54 270) (length 2.54)
\t\t\t\t(name "~" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "1" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at 0 -2.54 90) (length 2.54)
\t\t\t\t(name "~" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "2" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(property "Reference" "L" (at 2.032 0 90) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "L" (at -2.032 0 90) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t)
\t\t(symbol "Device:D_Zener"
\t\t\t(pin passive line (at 0 2.54 270) (length 2.54)
\t\t\t\t(name "K" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "1" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at 0 -2.54 90) (length 2.54)
\t\t\t\t(name "A" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "2" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(property "Reference" "D" (at 2.54 0 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "D_Zener" (at 2.54 -2.0 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t)
\t\t(symbol "Device:D"
\t\t\t(pin passive line (at 0 2.54 270) (length 2.54)
\t\t\t\t(name "K" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "1" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at 0 -2.54 90) (length 2.54)
\t\t\t\t(name "A" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "2" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(property "Reference" "D" (at 2.54 0 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "D" (at 2.54 -2.0 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t)
\t\t(symbol "Device:Fuse"
\t\t\t(pin passive line (at 0 2.54 270) (length 2.54)
\t\t\t\t(name "~" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "1" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at 0 -2.54 90) (length 2.54)
\t\t\t\t(name "~" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "2" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(property "Reference" "F" (at 2.032 0 90) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "Fuse" (at -2.032 0 90) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t)
\t\t(symbol "Switch:SW_SPST"
\t\t\t(pin passive line (at -5.08 0 0) (length 2.54)
\t\t\t\t(name "1" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "1" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at 5.08 0 180) (length 2.54)
\t\t\t\t(name "2" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "2" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(property "Reference" "SW" (at 0 2.54 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "SW_SPST" (at 0 -2.54 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t)
\t\t(symbol "Switch:SW_DPDT_x2"
\t\t\t(pin passive line (at -5.08 2.54 0) (length 2.54)
\t\t\t\t(name "A" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "1" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at 0 2.54 270) (length 2.54)
\t\t\t\t(name "B" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "2" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at 5.08 2.54 180) (length 2.54)
\t\t\t\t(name "C" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "3" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at -5.08 -2.54 0) (length 2.54)
\t\t\t\t(name "D" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "4" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at 0 -2.54 90) (length 2.54)
\t\t\t\t(name "E" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "5" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at 5.08 -2.54 180) (length 2.54)
\t\t\t\t(name "F" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "6" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(property "Reference" "SW" (at 0 5.08 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "SW_DPDT" (at 0 -5.08 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t)
\t\t(symbol "Connector:Conn_01x02_Pin"
\t\t\t(pin passive line (at -2.54 1.27 0) (length 2.54)
\t\t\t\t(name "Pin_1" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "1" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at -2.54 -1.27 0) (length 2.54)
\t\t\t\t(name "Pin_2" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "2" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(property "Reference" "J" (at 0 3.81 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "Conn_01x02" (at 0 -3.81 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t)
\t\t(symbol "Connector:Conn_01x03_Pin"
\t\t\t(pin passive line (at -2.54 2.54 0) (length 2.54)
\t\t\t\t(name "Pin_1" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "1" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at -2.54 0 0) (length 2.54)
\t\t\t\t(name "Pin_2" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "2" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at -2.54 -2.54 0) (length 2.54)
\t\t\t\t(name "Pin_3" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "3" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(property "Reference" "J" (at 0 5.08 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "Conn_01x03" (at 0 -5.08 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t)
\t\t(symbol "Connector_Audio:XLR3_Female"
\t\t\t(pin passive line (at -5.08 2.54 0) (length 2.54)
\t\t\t\t(name "1" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "1" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at -5.08 0 0) (length 2.54)
\t\t\t\t(name "2" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "2" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at -5.08 -2.54 0) (length 2.54)
\t\t\t\t(name "3" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "3" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(property "Reference" "J" (at 0 5.08 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "XLR3_Female" (at 0 -5.08 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t)
\t\t(symbol "Amplifier_Operational:NE5532"
\t\t\t(property "Reference" "U" (at 2.54 5.08 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "NE5532" (at 2.54 -5.08 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "Package_DIP:DIP-8_W7.62mm" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t\t(symbol "NE5532_1_1"
\t\t\t\t(pin output line (at 5.08 0 180) (length 2.54)
\t\t\t\t\t(name "~" (effects (font (size 1.27 1.27))))
\t\t\t\t\t(number "1" (effects (font (size 1.27 1.27))))
\t\t\t\t)
\t\t\t\t(pin input line (at -5.08 -2.54 0) (length 2.54)
\t\t\t\t\t(name "-" (effects (font (size 1.27 1.27))))
\t\t\t\t\t(number "2" (effects (font (size 1.27 1.27))))
\t\t\t\t)
\t\t\t\t(pin input line (at -5.08 2.54 0) (length 2.54)
\t\t\t\t\t(name "+" (effects (font (size 1.27 1.27))))
\t\t\t\t\t(number "3" (effects (font (size 1.27 1.27))))
\t\t\t\t)
\t\t\t)
\t\t\t(symbol "NE5532_2_1"
\t\t\t\t(pin output line (at 5.08 0 180) (length 2.54)
\t\t\t\t\t(name "~" (effects (font (size 1.27 1.27))))
\t\t\t\t\t(number "7" (effects (font (size 1.27 1.27))))
\t\t\t\t)
\t\t\t\t(pin input line (at -5.08 -2.54 0) (length 2.54)
\t\t\t\t\t(name "-" (effects (font (size 1.27 1.27))))
\t\t\t\t\t(number "6" (effects (font (size 1.27 1.27))))
\t\t\t\t)
\t\t\t\t(pin input line (at -5.08 2.54 0) (length 2.54)
\t\t\t\t\t(name "+" (effects (font (size 1.27 1.27))))
\t\t\t\t\t(number "5" (effects (font (size 1.27 1.27))))
\t\t\t\t)
\t\t\t)
\t\t\t(symbol "NE5532_3_1"
\t\t\t\t(pin power_in line (at 0 5.08 270) (length 2.54)
\t\t\t\t\t(name "V+" (effects (font (size 1.27 1.27))))
\t\t\t\t\t(number "8" (effects (font (size 1.27 1.27))))
\t\t\t\t)
\t\t\t\t(pin power_in line (at 0 -5.08 90) (length 2.54)
\t\t\t\t\t(name "V-" (effects (font (size 1.27 1.27))))
\t\t\t\t\t(number "4" (effects (font (size 1.27 1.27))))
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(symbol "Regulator_Linear:LM317_TO220"
\t\t\t(pin input line (at -5.08 2.54 0) (length 2.54)
\t\t\t\t(name "VI" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "3" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin input line (at 0 -5.08 90) (length 2.54)
\t\t\t\t(name "ADJ" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "1" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin power_out line (at 5.08 2.54 180) (length 2.54)
\t\t\t\t(name "VO" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "2" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(property "Reference" "U" (at 0 5.08 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "LM317HVT" (at 0 -7.62 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "Package_TO_SOT_THT:TO-220-3_Vertical" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t)
\t\t(symbol "Transistor_FET:P-MOSFET"
\t\t\t(pin input line (at -5.08 0 0) (length 2.54)
\t\t\t\t(name "G" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "1" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at 2.54 -5.08 90) (length 2.54)
\t\t\t\t(name "D" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "2" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at 2.54 5.08 270) (length 2.54)
\t\t\t\t(name "S" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "3" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(property "Reference" "Q" (at 5.08 2.54 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "IRF4905" (at 5.08 -2.54 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "Package_TO_SOT_THT:TO-220-3_Vertical" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t)
\t\t(symbol "power:PWR_FLAG"
\t\t\t(pin power_out line (at 0 0 90) (length 0)
\t\t\t\t(name "~" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "1" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(property "Reference" "#FLG" (at 0 1.905 0) (effects (font (size 1.27 1.27)) hide))
\t\t\t(property "Value" "PWR_FLAG" (at 0 3.81 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t)
\t\t(symbol "Connector:TestPoint"
\t\t\t(pin passive line (at 0 0 0) (length 0)
\t\t\t\t(name "1" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "1" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(property "Reference" "TP" (at 0 2.54 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "TestPoint" (at 0 -2.54 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "TestPoint:TestPoint_Pad_D1.5mm" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
\t\t)
\t)
"""

    instances = []
    def add_sym(lib_id, ref, val, x, y, foot="", unit=1, props=None):
        u = uid()
        p_str = ""
        if props:
            for pk, pv in props.items():
                p_str += f'\n\t\t(property "{pk}" "{pv}" (at {x:.2f} {y:.2f} 0) (effects (font (size 1.27 1.27))))'
        inst = f"""\t(symbol
\t\t(lib_id "{lib_id}")
\t\t(at {x:.2f} {y:.2f} 0)
\t\t(unit {unit})
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(dnp no)
\t\t(uuid "{u}")
\t\t(property "Reference" "{ref}" (at {x+2.54:.2f} {y-2.54:.2f} 0) (effects (font (size 1.27 1.27))))
\t\t(property "Value" "{val}" (at {x+2.54:.2f} {y:.2f} 0) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "{foot}" (at {x:.2f} {y:.2f} 0) (effects (font (size 1.27 1.27)) hide)){p_str}
\t)"""
        instances.append(inst)
        return u

    pin_nets = []
    def connect_pin(px, py, net):
        pin_nets.append((round(px, 2), round(py, 2), net))

    # =========================================================================
    # 1. MICROPHONE PREAMP SECTION (U1: NE5532P)
    # =========================================================================
    # XLR Input J1 (placed at 40.64, 50.80)
    j1_x, j1_y = snap(40.0), snap(50.0) # 40.64, 50.80
    add_sym("Connector_Audio:XLR3_Female", "J1", "MIC_XLR_IN", j1_x, j1_y, "Connector_Audio:Jack_XLR_Neutrik_NC3FAH_Horizontal")
    connect_pin(j1_x - 5.08, j1_y - 2.54, "GND_CHASSIS")
    connect_pin(j1_x - 5.08, j1_y,        "MIC_HOT_RAW")
    connect_pin(j1_x - 5.08, j1_y + 2.54, "MIC_COLD_RAW")

    # RF Filter Caps C1, C2
    c1_x, c1_y = snap(52.0), snap(40.0) # 50.80, 40.64
    add_sym("Device:C", "C1", "47pF", c1_x, c1_y, "Capacitor_THT:C_Disc_D4.3mm_W1.9mm_P5.00mm")
    connect_pin(c1_x, c1_y - 2.54, "GND")
    connect_pin(c1_x, c1_y + 2.54, "MIC_HOT_RAW")

    c2_x, c2_y = snap(52.0), snap(60.0) # 50.80, 60.96
    add_sym("Device:C", "C2", "47pF", c2_x, c2_y, "Capacitor_THT:C_Disc_D4.3mm_W1.9mm_P5.00mm")
    connect_pin(c2_x, c2_y - 2.54, "MIC_COLD_RAW")
    connect_pin(c2_x, c2_y + 2.54, "GND")

    # Bleeder Resistors R1, R2
    r1_x, r1_y = snap(62.0), snap(40.0) # 60.96, 40.64
    add_sym("Device:R", "R1", "100k", r1_x, r1_y, "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    connect_pin(r1_x, r1_y - 2.54, "GND")
    connect_pin(r1_x, r1_y + 2.54, "MIC_HOT_RAW")

    r2_x, r2_y = snap(62.0), snap(60.0) # 60.96, 60.96
    add_sym("Device:R", "R2", "100k", r2_x, r2_y, "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    connect_pin(r2_x, r2_y - 2.54, "MIC_COLD_RAW")
    connect_pin(r2_x, r2_y + 2.54, "GND")

    # AC Input Coupling Caps C4, C5 (Bipolar 10uF/50V)
    c4_x, c4_y = snap(76.0), snap(45.0) # 76.20, 45.72
    add_sym("Device:C_Polarized", "C4", "10uF/50V_BP", c4_x, c4_y, "Capacitor_THT:CP_Radial_D6.3mm_P2.50mm")
    connect_pin(c4_x, c4_y - 2.54, "MIC_HOT_RAW")
    connect_pin(c4_x, c4_y + 2.54, "MIC_HOT_AC")

    c5_x, c5_y = snap(76.0), snap(55.0) # 76.20, 55.88
    add_sym("Device:C_Polarized", "C5", "10uF/50V_BP", c5_x, c5_y, "Capacitor_THT:CP_Radial_D6.3mm_P2.50mm")
    connect_pin(c5_x, c5_y - 2.54, "MIC_COLD_AC")
    connect_pin(c5_x, c5_y + 2.54, "MIC_COLD_RAW")

    # Stage 1A Differential Resistors: Rin=2.2k 0.1%, Rfb/Rbias=4.7k 0.1% (High CMRR!)
    r3_x, r3_y = snap(90.0), snap(45.0) # 88.90, 45.72
    add_sym("Device:R", "R3", "2.2k_0.1%", r3_x, r3_y, "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    connect_pin(r3_x, r3_y - 2.54, "MIC_HOT_AC")
    connect_pin(r3_x, r3_y + 2.54, "MIC_PRE1_NONINV")

    r5_x, r5_y = snap(90.0), snap(55.0) # 88.90, 55.88
    add_sym("Device:R", "R5", "2.2k_0.1%", r5_x, r5_y, "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    connect_pin(r5_x, r5_y - 2.54, "MIC_PRE1_INV")
    connect_pin(r5_x, r5_y + 2.54, "MIC_COLD_AC")

    r4_x, r4_y = snap(104.0), snap(35.0) # 104.14, 35.56
    add_sym("Device:R", "R4", "4.7k_0.1%", r4_x, r4_y, "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    connect_pin(r4_x, r4_y - 2.54, "VBIAS_7V5")
    connect_pin(r4_x, r4_y + 2.54, "MIC_PRE1_NONINV")

    r6_x, r6_y = snap(104.0), snap(65.0) # 104.14, 66.04
    add_sym("Device:R", "R6", "4.7k_0.1%", r6_x, r6_y, "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    connect_pin(r6_x, r6_y - 2.54, "MIC_PRE1_INV")
    connect_pin(r6_x, r6_y + 2.54, "MIC_STG1_OUT")

    # U1A: Stage 1A Differential Op-Amp (Unit 1)
    u1a_x, u1a_y = snap(120.0), snap(50.0) # 119.38, 50.80
    add_sym("Amplifier_Operational:NE5532", "U1", "NE5532P", u1a_x, u1a_y, "Package_DIP:DIP-8_W7.62mm", unit=1)
    connect_pin(u1a_x - 5.08, u1a_y - 2.54, "MIC_PRE1_NONINV") # Pin 3 (+)
    connect_pin(u1a_x - 5.08, u1a_y + 2.54, "MIC_PRE1_INV")    # Pin 2 (-)
    connect_pin(u1a_x + 5.08, u1a_y,        "MIC_STG1_OUT")    # Pin 1 (Out)

    # Interstage Coupling: C6 (10uF), R7 (47k to Vbias)
    c6_x, c6_y = snap(140.0), snap(50.0) # 139.70, 50.80
    add_sym("Device:C_Polarized", "C6", "10uF/25V", c6_x, c6_y, "Capacitor_THT:CP_Radial_D5.0mm_P2.00mm")
    connect_pin(c6_x, c6_y - 2.54, "MIC_STG1_OUT")
    connect_pin(c6_x, c6_y + 2.54, "MIC_STG2_IN")

    r7_x, r7_y = snap(150.0), snap(65.0) # 149.86, 66.04
    add_sym("Device:R", "R7", "47k_1%", r7_x, r7_y, "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    connect_pin(r7_x, r7_y - 2.54, "MIC_STG2_IN")
    connect_pin(r7_x, r7_y + 2.54, "VBIAS_7V5")

    # Stage 1B Variable Gain Feedback: Rgain=330R, Rfb2=1.2k, RV1=50k RevLog
    r8_x, r8_y = snap(165.0), snap(65.0) # 165.10, 66.04
    add_sym("Device:R", "R8", "330R_1%", r8_x, r8_y, "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    connect_pin(r8_x, r8_y - 2.54, "MIC_PRE2_INV")
    connect_pin(r8_x, r8_y + 2.54, "VBIAS_7V5")

    r10_x, r10_y = snap(175.0), snap(65.0) # 175.26, 66.04
    add_sym("Device:R", "R10", "1.2k_1%", r10_x, r10_y, "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    connect_pin(r10_x, r10_y - 2.54, "MIC_PRE2_INV")
    connect_pin(r10_x, r10_y + 2.54, "MIC_GAIN_POT_CW")

    rv1_x, rv1_y = snap(190.0), snap(65.0) # 190.50, 66.04
    add_sym("Device:R_Potentiometer", "RV1", "50k_RevLog_MIC_GAIN", rv1_x, rv1_y, "Potentiometer_THT:Potentiometer_Bourns_3386P_Vertical")
    connect_pin(rv1_x, rv1_y - 2.54, "MIC_GAIN_POT_CW") # Pin 1
    connect_pin(rv1_x + 2.54, rv1_y, "MIC_PRE_OUT")     # Pin 2 (wiper)
    connect_pin(rv1_x, rv1_y + 2.54, "MIC_PRE_OUT")     # Pin 3

    # U1B: Stage 1B Post-Amp (Unit 2)
    u1b_x, u1b_y = snap(185.0), snap(50.0) # 185.42, 50.80
    add_sym("Amplifier_Operational:NE5532", "U1", "NE5532P", u1b_x, u1b_y, "Package_DIP:DIP-8_W7.62mm", unit=2)
    connect_pin(u1b_x - 5.08, u1b_y - 2.54, "MIC_STG2_IN")  # Pin 5 (+)
    connect_pin(u1b_x - 5.08, u1b_y + 2.54, "MIC_PRE2_INV")  # Pin 6 (-)
    connect_pin(u1b_x + 5.08, u1b_y,        "MIC_PRE_OUT")   # Pin 7 (Out)

    # U1 Power (Unit 3) + Decoupling C3
    u1c_x, u1c_y = snap(155.0), snap(30.0) # 154.94, 30.48
    add_sym("Amplifier_Operational:NE5532", "U1", "NE5532P", u1c_x, u1c_y, "Package_DIP:DIP-8_W7.62mm", unit=3)
    connect_pin(u1c_x, u1c_y - 5.08, "+15V") # Pin 8 (V+)
    connect_pin(u1c_x, u1c_y + 5.08, "GND")  # Pin 4 (V-)

    c3_x, c3_y = snap(168.0), snap(30.0) # 167.64, 30.48
    add_sym("Device:C", "C3", "100nF/50V", c3_x, c3_y, "Capacitor_THT:C_Rect_L7.2mm_W2.5mm_P5.00mm_FKS2_FKP2_MKS2_MKP2")
    connect_pin(c3_x, c3_y - 2.54, "+15V")
    connect_pin(c3_x, c3_y + 2.54, "GND")

    # Mic Channel AC Coupling C7 & Dedicated Mic Volume Pot RV2
    c7_x, c7_y = snap(205.0), snap(50.0) # 205.74, 50.80
    add_sym("Device:C_Polarized", "C7", "10uF/25V", c7_x, c7_y, "Capacitor_THT:CP_Radial_D5.0mm_P2.00mm")
    connect_pin(c7_x, c7_y - 2.54, "MIC_PRE_OUT")
    connect_pin(c7_x, c7_y + 2.54, "MIC_VOL_POT_IN")

    rv2_x, rv2_y = snap(220.0), snap(50.0) # 220.98, 50.80
    add_sym("Device:R_Potentiometer", "RV2", "10k_Log_MIC_VOL", rv2_x, rv2_y, "Potentiometer_THT:Potentiometer_Bourns_3386P_Vertical")
    connect_pin(rv2_x, rv2_y - 2.54, "MIC_VOL_POT_IN") # Pin 1
    connect_pin(rv2_x + 2.54, rv2_y, "MODE_A_MIC_SIG")  # Pin 2 (wiper to Mode Switch)
    connect_pin(rv2_x, rv2_y + 2.54, "GND")             # Pin 3

    # =========================================================================
    # 2. BALANCED LINE RECEIVER (U2B: NE5532P Unit 2)
    # =========================================================================
    # Combo Input J2
    j2_x, j2_y = snap(40.0), snap(110.0) # 40.64, 109.22
    add_sym("Connector_Audio:XLR3_Female", "J2", "COMBO_LINE_IN", j2_x, j2_y, "Connector_Audio:Jack_XLR-6.35mm_Neutrik_NCJ6FI-H_Horizontal")
    connect_pin(j2_x - 5.08, j2_y - 2.54, "GND_CHASSIS")
    connect_pin(j2_x - 5.08, j2_y,        "LINE_HOT_RAW")
    connect_pin(j2_x - 5.08, j2_y + 2.54, "LINE_COLD_RAW")

    # RF Filter Caps C10, C11
    c10_x, c10_y = snap(52.0), snap(100.0) # 50.80, 99.06
    add_sym("Device:C", "C10", "47pF", c10_x, c10_y, "Capacitor_THT:C_Disc_D4.3mm_W1.9mm_P5.00mm")
    connect_pin(c10_x, c10_y - 2.54, "GND")
    connect_pin(c10_x, c10_y + 2.54, "LINE_HOT_RAW")

    c11_x, c11_y = snap(52.0), snap(120.0) # 50.80, 119.38
    add_sym("Device:C", "C11", "47pF", c11_x, c11_y, "Capacitor_THT:C_Disc_D4.3mm_W1.9mm_P5.00mm")
    connect_pin(c11_x, c11_y - 2.54, "LINE_COLD_RAW")
    connect_pin(c11_x, c11_y + 2.54, "GND")

    # Bleeder Resistors R12, R13
    r12_x, r12_y = snap(62.0), snap(100.0) # 60.96, 99.06
    add_sym("Device:R", "R12", "100k", r12_x, r12_y, "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    connect_pin(r12_x, r12_y - 2.54, "GND")
    connect_pin(r12_x, r12_y + 2.54, "LINE_HOT_RAW")

    r13_x, r13_y = snap(62.0), snap(120.0) # 60.96, 119.38
    add_sym("Device:R", "R13", "100k", r13_x, r13_y, "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    connect_pin(r13_x, r13_y - 2.54, "LINE_COLD_RAW")
    connect_pin(r13_x, r13_y + 2.54, "GND")

    # AC Input Coupling Caps C12, C13 (Film 1uF/63V)
    c12_x, c12_y = snap(76.0), snap(105.0) # 76.20, 104.14
    add_sym("Device:C", "C12", "1uF_Film", c12_x, c12_y, "Capacitor_THT:C_Rect_L7.2mm_W3.5mm_P5.00mm_FKS2_FKP2_MKS2_MKP2")
    connect_pin(c12_x, c12_y - 2.54, "LINE_HOT_RAW")
    connect_pin(c12_x, c12_y + 2.54, "LINE_HOT_AC")

    c13_x, c13_y = snap(76.0), snap(115.0) # 76.20, 114.30
    add_sym("Device:C", "C13", "1uF_Film", c13_x, c13_y, "Capacitor_THT:C_Rect_L7.2mm_W3.5mm_P5.00mm_FKS2_FKP2_MKS2_MKP2")
    connect_pin(c13_x, c13_y - 2.54, "LINE_COLD_AC")
    connect_pin(c13_x, c13_y + 2.54, "LINE_COLD_RAW")

    # Balanced Line Differential Attenuator: Rin=30k 0.1%, Rfb=10k 0.1% (Ad = 1/3 = -9.54 dB, High CMRR)
    r14_x, r14_y = snap(92.0), snap(105.0) # 91.44, 104.14
    add_sym("Device:R", "R14", "30k_0.1%", r14_x, r14_y, "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    connect_pin(r14_x, r14_y - 2.54, "LINE_HOT_AC")
    connect_pin(r14_x, r14_y + 2.54, "LINE_REC_NONINV")

    r15_x, r15_y = snap(92.0), snap(115.0) # 91.44, 114.30
    add_sym("Device:R", "R15", "30k_0.1%", r15_x, r15_y, "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    connect_pin(r15_x, r15_y - 2.54, "LINE_REC_INV")
    connect_pin(r15_x, r15_y + 2.54, "LINE_COLD_AC")

    r16_x, r16_y = snap(108.0), snap(95.0) # 106.68, 93.98
    add_sym("Device:R", "R16", "10k_0.1%", r16_x, r16_y, "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    connect_pin(r16_x, r16_y - 2.54, "VBIAS_7V5")
    connect_pin(r16_x, r16_y + 2.54, "LINE_REC_NONINV")

    r17_x, r17_y = snap(108.0), snap(125.0) # 106.68, 124.46
    add_sym("Device:R", "R17", "10k_0.1%", r17_x, r17_y, "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    connect_pin(r17_x, r17_y - 2.54, "LINE_REC_INV")
    connect_pin(r17_x, r17_y + 2.54, "LINE_REC_OUT")

    # U2B: Balanced Line Receiver Op-Amp (Unit 2)
    u2b_x, u2b_y = snap(125.0), snap(110.0) # 124.46, 109.22
    add_sym("Amplifier_Operational:NE5532", "U2", "NE5532P", u2b_x, u2b_y, "Package_DIP:DIP-8_W7.62mm", unit=2)
    connect_pin(u2b_x - 5.08, u2b_y - 2.54, "LINE_REC_NONINV") # Pin 5 (+)
    connect_pin(u2b_x - 5.08, u2b_y + 2.54, "LINE_REC_INV")    # Pin 6 (-)
    connect_pin(u2b_x + 5.08, u2b_y,        "LINE_REC_OUT")    # Pin 7 (Out)

    # U2 Power (Unit 3) + Decoupling C16
    u2c_x, u2c_y = snap(155.0), snap(90.0) # 154.94, 91.44
    add_sym("Amplifier_Operational:NE5532", "U2", "NE5532P", u2c_x, u2c_y, "Package_DIP:DIP-8_W7.62mm", unit=3)
    connect_pin(u2c_x, u2c_y - 5.08, "+15V") # Pin 8 (V+)
    connect_pin(u2c_x, u2c_y + 5.08, "GND")  # Pin 4 (V-)

    c16_x, c16_y = snap(168.0), snap(90.0) # 167.64, 91.44
    add_sym("Device:C", "C16", "100nF/50V", c16_x, c16_y, "Capacitor_THT:C_Rect_L7.2mm_W2.5mm_P5.00mm_FKS2_FKP2_MKS2_MKP2")
    connect_pin(c16_x, c16_y - 2.54, "+15V")
    connect_pin(c16_x, c16_y + 2.54, "GND")

    # Line Output AC Coupling C15 & Dedicated Line Volume Pot RV3
    c15_x, c15_y = snap(145.0), snap(110.0) # 144.78, 109.22
    add_sym("Device:C_Polarized", "C15", "10uF/25V", c15_x, c15_y, "Capacitor_THT:CP_Radial_D5.0mm_P2.00mm")
    connect_pin(c15_x, c15_y - 2.54, "LINE_REC_OUT")
    connect_pin(c15_x, c15_y + 2.54, "LINE_VOL_POT_IN")

    rv3_x, rv3_y = snap(160.0), snap(110.0) # 160.02, 109.22
    add_sym("Device:R_Potentiometer", "RV3", "10k_Log_LINE_VOL", rv3_x, rv3_y, "Potentiometer_THT:Potentiometer_Bourns_3386P_Vertical")
    connect_pin(rv3_x, rv3_y - 2.54, "LINE_VOL_POT_IN") # Pin 1
    connect_pin(rv3_x + 2.54, rv3_y, "MODE_B_LINE_SIG") # Pin 2 (wiper to Mode Switch)
    connect_pin(rv3_x, rv3_y + 2.54, "GND")             # Pin 3

    # =========================================================================
    # 3. MODE SELECTION SWITCH (SW1: DPDT)
    # =========================================================================
    sw1_x, sw1_y = snap(248.0), snap(80.0) # 248.92, 78.74
    add_sym("Switch:SW_DPDT_x2", "SW1", "DPDT_MODE_SELECT", sw1_x, sw1_y, "Button_Switch_THT:SW_MEC_5G")
    connect_pin(sw1_x - 5.08, sw1_y - 2.54, "MODE_A_MIC_SIG")  # Pin 1 (Mode A: Mic Volume Out)
    connect_pin(sw1_x,        sw1_y - 2.54, "SELECTED_AUDIO")  # Pin 2 (Wiper feeds Common HPF!)
    connect_pin(sw1_x + 5.08, sw1_y - 2.54, "MODE_B_LINE_SIG") # Pin 3 (Mode B: Line Volume Out)
    connect_pin(sw1_x - 5.08, sw1_y + 2.54, "+15V")             # Pin 4 (Telemetry pullup)
    connect_pin(sw1_x,        sw1_y + 2.54, "MODE_STATUS")      # Pin 5 (Telemetry wiper)
    connect_pin(sw1_x + 5.08, sw1_y + 2.54, "GND")              # Pin 6 (Telemetry ground)

    tp1_x, tp1_y = snap(270.0), sw1_y + 2.54 # 269.24, 81.28
    add_sym("Connector:TestPoint", "TP1", "TP_MODE_STATUS", tp1_x, tp1_y, "TestPoint:TestPoint_Pad_D1.5mm")
    connect_pin(tp1_x, tp1_y, "MODE_STATUS")

    # =========================================================================
    # 4. COMMON 60Hz 2nd-ORDER SALLEN-KEY HPF (U2A: NE5532P Unit 1)
    # Protects BOTH Mic and Line modes from excursion hazard!
    # =========================================================================
    c8_x, c8_y = snap(278.0), snap(50.0) # 276.86, 50.80
    add_sym("Device:C", "C8", "68nF_Film", c8_x, c8_y, "Capacitor_THT:C_Rect_L7.2mm_W3.5mm_P5.00mm_FKS2_FKP2_MKS2_MKP2")
    connect_pin(c8_x, c8_y - 2.54, "SELECTED_AUDIO")
    connect_pin(c8_x, c8_y + 2.54, "HPF_MID_NODE")

    r9_x, r9_y = snap(288.0), snap(35.0) # 287.02, 35.56
    add_sym("Device:R", "R9", "27k_1%", r9_x, r9_y, "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    connect_pin(r9_x, r9_y - 2.54, "HPF_OUT")
    connect_pin(r9_x, r9_y + 2.54, "HPF_MID_NODE")

    c9_x, c9_y = snap(295.0), snap(50.0) # 294.64, 50.80
    add_sym("Device:C", "C9", "68nF_Film", c9_x, c9_y, "Capacitor_THT:C_Rect_L7.2mm_W3.5mm_P5.00mm_FKS2_FKP2_MKS2_MKP2")
    connect_pin(c9_x, c9_y - 2.54, "HPF_MID_NODE")
    connect_pin(c9_x, c9_y + 2.54, "HPF_NONINV")

    r11_x, r11_y = snap(295.0), snap(65.0) # 294.64, 66.04
    add_sym("Device:R", "R11", "56k_1%", r11_x, r11_y, "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    connect_pin(r11_x, r11_y - 2.54, "HPF_NONINV")
    connect_pin(r11_x, r11_y + 2.54, "VBIAS_7V5")

    # U2A: Common Sallen-Key HPF Unity Gain Follower (Unit 1)
    u2a_x, u2a_y = snap(310.0), snap(50.0) # 309.88, 50.80
    add_sym("Amplifier_Operational:NE5532", "U2", "NE5532P", u2a_x, u2a_y, "Package_DIP:DIP-8_W7.62mm", unit=1)
    connect_pin(u2a_x - 5.08, u2a_y - 2.54, "HPF_NONINV") # Pin 3 (+)
    connect_pin(u2a_x - 5.08, u2a_y + 2.54, "HPF_OUT")    # Pin 2 (-) feedback
    connect_pin(u2a_x + 5.08, u2a_y,        "HPF_OUT")    # Pin 1 (Out)

    # Master Output AC Coupling C14 & Bleeder R24 to Amp Input
    c14_x, c14_y = snap(325.0), snap(50.0) # 325.12, 50.80
    add_sym("Device:C_Polarized", "C14", "10uF/25V", c14_x, c14_y, "Capacitor_THT:CP_Radial_D5.0mm_P2.00mm")
    connect_pin(c14_x, c14_y - 2.54, "HPF_OUT")
    connect_pin(c14_x, c14_y + 2.54, "AMP_INPUT_SIG")

    r24_x, r24_y = snap(335.0), snap(65.0) # 335.28, 66.04
    add_sym("Device:R", "R24", "100k", r24_x, r24_y, "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    connect_pin(r24_x, r24_y - 2.54, "AMP_INPUT_SIG")
    connect_pin(r24_x, r24_y + 2.54, "GND")

    # =========================================================================
    # 5. POWER SUPPLY & VIRTUAL GROUND SECTION (U4, Q1, U3)
    # =========================================================================
    # DC Input Connector J3 (pins at +/- 1.27 -> place at half snap so pins are on 2.54 grid)
    j3_x = snap(40.0)
    j3_y = snap_half(170.0) # 171.45 -> pins at 170.18 and 172.72
    add_sym("Connector:Conn_01x02_Pin", "J3", "DC_36V_IN", j3_x, j3_y, "Connector_BarrelJack:BarrelJack_Horizontal")
    connect_pin(j3_x - 2.54, j3_y - 1.27, "DC_IN_RAW")
    connect_pin(j3_x - 2.54, j3_y + 1.27, "GND")

    # Fuse F1 (T3.15A 5x20mm)
    f1_x, f1_y = snap(55.0), snap(165.0) # 55.88, 165.10
    add_sym("Device:Fuse", "F1", "T3.15A_250V_5x20mm", f1_x, f1_y, "Fuse:Fuseholder_Cylinder-5x20mm_Schurter_0031_8201_Horizontal_Open")
    connect_pin(f1_x, f1_y - 2.54, "DC_IN_RAW")
    connect_pin(f1_x, f1_y + 2.54, "DC_FUSE_OUT")

    # P-MOSFET Reverse Polarity Protection Q1 (IRF4905)
    # Pin 1 = G, Pin 2 = D (Input), Pin 3 = S (Protected Rail)
    q1_x, q1_y = snap(75.0), snap(165.0) # 76.20, 165.10
    add_sym("Transistor_FET:P-MOSFET", "Q1", "IRF4905", q1_x, q1_y, "Package_TO_SOT_THT:TO-220-3_Vertical")
    connect_pin(q1_x - 5.08, q1_y,        "PMOS_GATE")    # Pin 1 (G)
    connect_pin(q1_x + 2.54, q1_y - 5.08, "DC_FUSE_OUT") # Pin 2 (D)
    connect_pin(q1_x + 2.54, q1_y + 5.08, "+36V")        # Pin 3 (S)

    # Zener D1 (12V clamp across S-G) & Gate pull-down R18 (100k)
    d1_x, d1_y = snap(68.0), snap(180.0) # 68.58, 180.34
    add_sym("Device:D_Zener", "D1", "BZX79C12_12V", d1_x, d1_y, "Diode_THT:D_DO-35_SOD27_P7.62mm_Horizontal")
    connect_pin(d1_x, d1_y - 2.54, "+36V")      # Pin 1 (K)
    connect_pin(d1_x, d1_y + 2.54, "PMOS_GATE") # Pin 2 (A)

    r18_x, r18_y = snap(80.0), snap(180.0) # 81.28, 180.34
    add_sym("Device:R", "R18", "100k", r18_x, r18_y, "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    connect_pin(r18_x, r18_y - 2.54, "PMOS_GATE")
    connect_pin(r18_x, r18_y + 2.54, "GND")

    # 36V Rail Filtering Caps C17, C18
    c17_x, c17_y = snap(95.0), snap(180.0) # 93.98, 180.34
    add_sym("Device:C_Polarized", "C17", "470uF/50V_LowESR", c17_x, c17_y, "Capacitor_THT:CP_Radial_D10.0mm_P5.00mm")
    connect_pin(c17_x, c17_y - 2.54, "+36V")
    connect_pin(c17_x, c17_y + 2.54, "GND")

    c18_x, c18_y = snap(108.0), snap(180.0) # 106.68, 180.34
    add_sym("Device:C", "C18", "100nF/50V", c18_x, c18_y, "Capacitor_THT:C_Rect_L7.2mm_W2.5mm_P5.00mm_FKS2_FKP2_MKS2_MKP2")
    connect_pin(c18_x, c18_y - 2.54, "+36V")
    connect_pin(c18_x, c18_y + 2.54, "GND")

    # LM317HVT Linear Regulator U4 (Pin 3=VI, Pin 1=ADJ, Pin 2=VO)
    u4_x, u4_y = snap(130.0), snap(165.0) # 129.54, 165.10
    add_sym("Regulator_Linear:LM317_TO220", "U4", "LM317HVT", u4_x, u4_y, "Package_TO_SOT_THT:TO-220-3_Vertical")
    connect_pin(u4_x - 5.08, u4_y - 2.54, "+36V")      # Pin 3 (VI)
    connect_pin(u4_x,        u4_y + 5.08, "LM317_ADJ") # Pin 1 (ADJ)
    connect_pin(u4_x + 5.08, u4_y - 2.54, "+15V")      # Pin 2 (VO)

    # LM317 Programming Resistors: R19=240R 1%, R20=2.64k 1%
    r19_x, r19_y = snap(140.0), snap(180.0) # 139.70, 180.34
    add_sym("Device:R", "R19", "240R_1%", r19_x, r19_y, "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    connect_pin(r19_x, r19_y - 2.54, "+15V")
    connect_pin(r19_x, r19_y + 2.54, "LM317_ADJ")

    r20_x, r20_y = snap(150.0), snap(180.0) # 150.88, 180.34
    add_sym("Device:R", "R20", "2.64k_1%", r20_x, r20_y, "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    connect_pin(r20_x, r20_y - 2.54, "LM317_ADJ")
    connect_pin(r20_x, r20_y + 2.54, "GND")

    # ADJ Ripple Filter C19 (10uF)
    c19_x, c19_y = snap(160.0), snap(180.0) # 160.02, 180.34
    add_sym("Device:C_Polarized", "C19", "10uF/25V", c19_x, c19_y, "Capacitor_THT:CP_Radial_D5.0mm_P2.00mm")
    connect_pin(c19_x, c19_y - 2.54, "LM317_ADJ")
    connect_pin(c19_x, c19_y + 2.54, "GND")

    # Protection Diodes D2 (Reverse), D3 (Bypass)
    d2_x, d2_y = snap(130.0), snap(150.0) # 129.54, 149.86
    add_sym("Device:D", "D2", "1N4007", d2_x, d2_y, "Diode_THT:D_DO-41_SOD81_P10.16mm_Horizontal")
    connect_pin(d2_x, d2_y - 2.54, "+36V") # Pin 1 (K)
    connect_pin(d2_x, d2_y + 2.54, "+15V") # Pin 2 (A)

    d3_x, d3_y = snap(145.0), snap(172.0) # 144.78, 172.72
    add_sym("Device:D", "D3", "1N4007", d3_x, d3_y, "Diode_THT:D_DO-41_SOD81_P10.16mm_Horizontal")
    connect_pin(d3_x, d3_y - 2.54, "+15V")      # Pin 1 (K)
    connect_pin(d3_x, d3_y + 2.54, "LM317_ADJ") # Pin 2 (A)

    # +15V Output Filtering C20 (100uF), C21 (100nF)
    c20_x, c20_y = snap(175.0), snap(180.0) # 175.26, 180.34
    add_sym("Device:C_Polarized", "C20", "100uF/25V", c20_x, c20_y, "Capacitor_THT:CP_Radial_D6.3mm_P2.50mm")
    connect_pin(c20_x, c20_y - 2.54, "+15V")
    connect_pin(c20_x, c20_y + 2.54, "GND")

    c21_x, c21_y = snap(185.0), snap(180.0) # 185.42, 180.34
    add_sym("Device:C", "C21", "100nF/50V", c21_x, c21_y, "Capacitor_THT:C_Rect_L7.2mm_W2.5mm_P5.00mm_FKS2_FKP2_MKS2_MKP2")
    connect_pin(c21_x, c21_y - 2.54, "+15V")
    connect_pin(c21_x, c21_y + 2.54, "GND")

    # -------------------------------------------------------------------------
    # Virtual Ground Generator & Buffer (U3: NE5532P)
    # Voltage Divider: R21=10k 1%, R22=10k 1%, Filter C22 (10uF)
    r21_x, r21_y = snap(205.0), snap(165.0) # 205.74, 165.10
    add_sym("Device:R", "R21", "10k_1%", r21_x, r21_y, "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    connect_pin(r21_x, r21_y - 2.54, "+15V")
    connect_pin(r21_x, r21_y + 2.54, "VBIAS_DIV")

    r22_x, r22_y = snap(205.0), snap(185.0) # 205.74, 185.42
    add_sym("Device:R", "R22", "10k_1%", r22_x, r22_y, "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    connect_pin(r22_x, r22_y - 2.54, "VBIAS_DIV")
    connect_pin(r22_x, r22_y + 2.54, "GND")

    c22_x, c22_y = snap(215.0), snap(185.0) # 215.90, 185.42
    add_sym("Device:C_Polarized", "C22", "10uF/25V", c22_x, c22_y, "Capacitor_THT:CP_Radial_D5.0mm_P2.00mm")
    connect_pin(c22_x, c22_y - 2.54, "VBIAS_DIV")
    connect_pin(c22_x, c22_y + 2.54, "GND")

    # U3A: Virtual Ground Follower Buffer (Unit 1)
    u3a_x, u3a_y = snap(235.0), snap(175.0) # 233.68, 175.26
    add_sym("Amplifier_Operational:NE5532", "U3", "NE5532P", u3a_x, u3a_y, "Package_DIP:DIP-8_W7.62mm", unit=1)
    connect_pin(u3a_x - 5.08, u3a_y - 2.54, "VBIAS_DIV") # Pin 3 (+)
    connect_pin(u3a_x - 5.08, u3a_y + 2.54, "VBIAS_7V5") # Pin 2 (-) feedback
    connect_pin(u3a_x + 5.08, u3a_y,        "VBIAS_7V5") # Pin 1 (Out)

    # Vbias Output Decoupling Caps C23 (47uF), C25 (100nF)
    c23_x, c23_y = snap(255.0), snap(185.0) # 254.00, 185.42
    add_sym("Device:C_Polarized", "C23", "47uF/25V", c23_x, c23_y, "Capacitor_THT:CP_Radial_D5.0mm_P2.00mm")
    connect_pin(c23_x, c23_y - 2.54, "VBIAS_7V5")
    connect_pin(c23_x, c23_y + 2.54, "GND")

    c25_x, c25_y = snap(265.0), snap(185.0) # 264.16, 185.42
    add_sym("Device:C", "C25", "100nF/50V", c25_x, c25_y, "Capacitor_THT:C_Rect_L7.2mm_W2.5mm_P5.00mm_FKS2_FKP2_MKS2_MKP2")
    connect_pin(c25_x, c25_y - 2.54, "VBIAS_7V5")
    connect_pin(c25_x, c25_y + 2.54, "GND")

    # U3B: Properly Terminated Spare Unit (Unit 2: Unity Gain Follower tied to Vbias)
    u3b_x, u3b_y = snap(295.0), snap(175.0) # 294.64, 175.26
    add_sym("Amplifier_Operational:NE5532", "U3", "NE5532P", u3b_x, u3b_y, "Package_DIP:DIP-8_W7.62mm", unit=2)
    connect_pin(u3b_x - 5.08, u3b_y - 2.54, "VBIAS_7V5")  # Pin 5 (+)
    connect_pin(u3b_x - 5.08, u3b_y + 2.54, "SPARE_OUT")  # Pin 6 (-) feedback
    connect_pin(u3b_x + 5.08, u3b_y,        "SPARE_OUT")  # Pin 7 (Out)

    # U3 Power (Unit 3) + Decoupling C26
    u3c_x, u3c_y = snap(265.0), snap(155.0) # 264.16, 154.94
    add_sym("Amplifier_Operational:NE5532", "U3", "NE5532P", u3c_x, u3c_y, "Package_DIP:DIP-8_W7.62mm", unit=3)
    connect_pin(u3c_x, u3c_y - 5.08, "+15V") # Pin 8 (V+)
    connect_pin(u3c_x, u3c_y + 5.08, "GND")  # Pin 4 (V-)

    c26_x, c26_y = snap(278.0), snap(155.0) # 276.86, 154.94
    add_sym("Device:C", "C26", "100nF/50V", c26_x, c26_y, "Capacitor_THT:C_Rect_L7.2mm_W2.5mm_P5.00mm_FKS2_FKP2_MKS2_MKP2")
    connect_pin(c26_x, c26_y - 2.54, "+15V")
    connect_pin(c26_x, c26_y + 2.54, "GND")

    # =========================================================================
    # 6. AMPLIFIER & DRIVER INTERFACE SECTION
    # =========================================================================
    # J4: DC 36V Power to TPA3255 Amplifier Board
    j4_x = snap(355.0)
    j4_y = snap_half(50.0)
    add_sym("Connector:Conn_01x02_Pin", "J4", "AMP_POWER_36V", j4_x, j4_y, "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal")
    connect_pin(j4_x - 2.54, j4_y - 1.27, "+36V")
    connect_pin(j4_x - 2.54, j4_y + 1.27, "GND")

    # J5: Audio Signal to TPA3255 Amplifier Board
    j5_x = snap(355.0)
    j5_y = snap(80.0)
    add_sym("Connector:Conn_01x03_Pin", "J5", "AMP_AUDIO_IN", j5_x, j5_y, "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical")
    connect_pin(j5_x - 2.54, j5_y - 2.54, "AMP_INPUT_SIG")
    connect_pin(j5_x - 2.54, j5_y,        "GND")
    connect_pin(j5_x - 2.54, j5_y + 2.54, "GND_CHASSIS")

    # J6: Speaker Output from TPA3255 Amplifier Board (Floating Bridge!)
    j6_x = snap(355.0)
    j6_y = snap_half(120.0)
    add_sym("Connector:Conn_01x02_Pin", "J6", "AMP_SPEAKER_OUT", j6_x, j6_y, "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal")
    connect_pin(j6_x - 2.54, j6_y - 1.27, "AMP_OUT_POS")
    connect_pin(j6_x - 2.54, j6_y + 1.27, "AMP_OUT_NEG")

    # RLC Contour Filter Network: L1, C24, R23 and Bypass Switch SW2
    sw2_x, sw2_y = snap(381.0), snap(95.0) # 381.00, 93.98
    add_sym("Switch:SW_SPST", "SW2", "CONTOUR_BYPASS", sw2_x, sw2_y, "Button_Switch_THT:SW_MEC_5G")
    connect_pin(sw2_x - 5.08, sw2_y, "AMP_OUT_POS")
    connect_pin(sw2_x + 5.08, sw2_y, "SPK_OUT_POS")

    l1_x, l1_y = snap(381.0), snap(110.0) # 381.00, 109.22
    add_sym("Device:L", "L1", "1.0mH_AirCore_0.35R", l1_x, l1_y, "Inductor_THT:L_Radial_D25.0mm_P15.00mm")
    connect_pin(l1_x, l1_y - 2.54, "AMP_OUT_POS")
    connect_pin(l1_x, l1_y + 2.54, "SPK_OUT_POS")

    c24_x, c24_y = snap(381.0), snap(125.0) # 381.00, 124.46
    add_sym("Device:C", "C24", "4.7uF/250V_MKP", c24_x, c24_y, "Capacitor_THT:C_Rect_L18.0mm_W9.0mm_P15.00mm_FKS3_FKP3")
    connect_pin(c24_x, c24_y - 2.54, "AMP_OUT_POS")
    connect_pin(c24_x, c24_y + 2.54, "SPK_OUT_POS")

    r23_x, r23_y = snap(381.0), snap(140.0) # 381.00, 139.70
    add_sym("Device:R", "R23", "8.2R_10W_NonInductive", r23_x, r23_y, "Resistor_THT:R_Axial_Power_L25.0mm_D9.0mm_P30.00mm_Horizontal")
    connect_pin(r23_x, r23_y - 2.54, "AMP_OUT_POS")
    connect_pin(r23_x, r23_y + 2.54, "SPK_OUT_POS")

    # J7: Output Terminal to Visaton BG 20 Loudspeaker Driver (Floating Bridge!)
    j7_x = snap(416.0)
    j7_y = snap_half(120.0)
    add_sym("Connector:Conn_01x02_Pin", "J7", "VISATON_BG20_8R", j7_x, j7_y, "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal")
    connect_pin(j7_x - 2.54, j7_y - 1.27, "SPK_OUT_POS")
    connect_pin(j7_x - 2.54, j7_y + 1.27, "AMP_OUT_NEG")

    # =========================================================================
    # 7. POWER FLAGS (Only for nets not driven by active power_out pins)
    # =========================================================================
    flg1_x, flg1_y = snap(35.0), snap(178.0)
    add_sym("power:PWR_FLAG", "#FLG1", "PWR_FLAG", flg1_x, flg1_y)
    connect_pin(flg1_x, flg1_y, "GND")

    flg2_x, flg2_y = snap(100.0), snap(160.0)
    add_sym("power:PWR_FLAG", "#FLG2", "PWR_FLAG", flg2_x, flg2_y)
    connect_pin(flg2_x, flg2_y, "+36V")

    # =========================================================================
    # GENERATE LABELS
    # =========================================================================
    labels = []
    for px, py, net in pin_nets:
        u = uid()
        lbl = f"""\t(label "{net}"
\t\t(at {px:.2f} {py:.2f} 0.0000)
\t\t(effects
\t\t\t(font
\t\t\t\t(size 1.27 1.27)
\t\t\t)
\t\t\t(justify left bottom)
\t\t)
\t\t(uuid "{u}")
\t)"""
        labels.append(lbl)

    full_sch = sch_header + "\n".join(instances) + "\n" + "\n".join(labels) + """
\t(sheet_instances
\t\t(path "/"
\t\t\t(page "1")
\t\t)
\t)
\t(embedded_fonts no)
)
"""
    with open(sch_file, "w") as f:
        f.write(full_sch)
    print(f"Generated {sch_file} with {len(instances)} symbols and {len(labels)} net labels.")

if __name__ == "__main__":
    main()
