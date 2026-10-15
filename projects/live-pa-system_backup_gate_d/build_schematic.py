#!/usr/bin/env python3
"""
Generate complete KiCad 10 schematic for DIY Active Stage Monitor
Project: live-pa-system.kicad_sch
With complete net labels on all pins for 100% clean ERC.
"""

import uuid
import sys

def uid():
    return str(uuid.uuid4())

def main():
    sch_file = "projects/live-pa-system/live-pa-system.kicad_sch"
    
    sch_header = f"""(kicad_sch
	(version 20250114)
	(generator "eeschema")
	(generator_version "10.0")
	(uuid "{uid()}")
	(paper "A3")
	(title_block
		(title "DIY Active Stage Monitor - Analog Front-End & Filter")
		(date "2026-10-14")
		(rev "1.0")
		(company "DIY Audio Labs")
		(comment 1 "Gate D Engineering Schematic: Visaton BG 20 + TPA3255 PBTL")
		(comment 2 "Mode A: Mic Preamp + 60Hz 2nd HPF | Mode B: Balanced LINE -6dB")
		(comment 3 "DC 36V in with P-MOSFET reverse prot, LM317HV +15V reg & RLC contour")
	)
	(lib_symbols
		(symbol "Device:C"
			(pin passive line (at 0 2.54 270) (length 2.54)
				(name "~" (effects (font (size 1.27 1.27))))
				(number "1" (effects (font (size 1.27 1.27))))
			)
			(pin passive line (at 0 -2.54 90) (length 2.54)
				(name "~" (effects (font (size 1.27 1.27))))
				(number "2" (effects (font (size 1.27 1.27))))
			)
			(property "Reference" "C" (at 2.54 1.27 0) (effects (font (size 1.27 1.27))))
			(property "Value" "C" (at 2.54 -1.27 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
		)
		(symbol "Device:C_Polarized"
			(pin passive line (at 0 2.54 270) (length 2.54)
				(name "~" (effects (font (size 1.27 1.27))))
				(number "1" (effects (font (size 1.27 1.27))))
			)
			(pin passive line (at 0 -2.54 90) (length 2.54)
				(name "~" (effects (font (size 1.27 1.27))))
				(number "2" (effects (font (size 1.27 1.27))))
			)
			(property "Reference" "C" (at 2.54 1.27 0) (effects (font (size 1.27 1.27))))
			(property "Value" "C_Polarized" (at 2.54 -1.27 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
		)
		(symbol "Device:R"
			(pin passive line (at 0 2.54 270) (length 2.54)
				(name "~" (effects (font (size 1.27 1.27))))
				(number "1" (effects (font (size 1.27 1.27))))
			)
			(pin passive line (at 0 -2.54 90) (length 2.54)
				(name "~" (effects (font (size 1.27 1.27))))
				(number "2" (effects (font (size 1.27 1.27))))
			)
			(property "Reference" "R" (at 2.032 0 90) (effects (font (size 1.27 1.27))))
			(property "Value" "R" (at -2.032 0 90) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
		)
		(symbol "Device:R_Potentiometer"
			(pin passive line (at 0 2.54 270) (length 2.54)
				(name "1" (effects (font (size 1.27 1.27))))
				(number "1" (effects (font (size 1.27 1.27))))
			)
			(pin passive line (at 2.54 0 180) (length 2.54)
				(name "2" (effects (font (size 1.27 1.27))))
				(number "2" (effects (font (size 1.27 1.27))))
			)
			(pin passive line (at 0 -2.54 90) (length 2.54)
				(name "3" (effects (font (size 1.27 1.27))))
				(number "3" (effects (font (size 1.27 1.27))))
			)
			(property "Reference" "RV" (at 2.54 2.54 0) (effects (font (size 1.27 1.27))))
			(property "Value" "R_Potentiometer" (at 2.54 -2.54 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
		)
		(symbol "Device:L"
			(pin passive line (at 0 2.54 270) (length 2.54)
				(name "~" (effects (font (size 1.27 1.27))))
				(number "1" (effects (font (size 1.27 1.27))))
			)
			(pin passive line (at 0 -2.54 90) (length 2.54)
				(name "~" (effects (font (size 1.27 1.27))))
				(number "2" (effects (font (size 1.27 1.27))))
			)
			(property "Reference" "L" (at 2.032 0 90) (effects (font (size 1.27 1.27))))
			(property "Value" "L" (at -2.032 0 90) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
		)
		(symbol "Device:D_Zener"
			(pin passive line (at 0 2.54 270) (length 2.54)
				(name "K" (effects (font (size 1.27 1.27))))
				(number "1" (effects (font (size 1.27 1.27))))
			)
			(pin passive line (at 0 -2.54 90) (length 2.54)
				(name "A" (effects (font (size 1.27 1.27))))
				(number "2" (effects (font (size 1.27 1.27))))
			)
			(property "Reference" "D" (at 2.54 0 0) (effects (font (size 1.27 1.27))))
			(property "Value" "D_Zener" (at 2.54 -2.0 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
		)
		(symbol "Device:D"
			(pin passive line (at 0 2.54 270) (length 2.54)
				(name "K" (effects (font (size 1.27 1.27))))
				(number "1" (effects (font (size 1.27 1.27))))
			)
			(pin passive line (at 0 -2.54 90) (length 2.54)
				(name "A" (effects (font (size 1.27 1.27))))
				(number "2" (effects (font (size 1.27 1.27))))
			)
			(property "Reference" "D" (at 2.54 0 0) (effects (font (size 1.27 1.27))))
			(property "Value" "D" (at 2.54 -2.0 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
		)
		(symbol "Device:Fuse"
			(pin passive line (at 0 2.54 270) (length 2.54)
				(name "~" (effects (font (size 1.27 1.27))))
				(number "1" (effects (font (size 1.27 1.27))))
			)
			(pin passive line (at 0 -2.54 90) (length 2.54)
				(name "~" (effects (font (size 1.27 1.27))))
				(number "2" (effects (font (size 1.27 1.27))))
			)
			(property "Reference" "F" (at 2.032 0 90) (effects (font (size 1.27 1.27))))
			(property "Value" "Fuse" (at -2.032 0 90) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
		)
		(symbol "Switch:SW_SPST"
			(pin passive line (at -5.08 0 0) (length 2.54)
				(name "1" (effects (font (size 1.27 1.27))))
				(number "1" (effects (font (size 1.27 1.27))))
			)
			(pin passive line (at 5.08 0 180) (length 2.54)
				(name "2" (effects (font (size 1.27 1.27))))
				(number "2" (effects (font (size 1.27 1.27))))
			)
			(property "Reference" "SW" (at 0 2.54 0) (effects (font (size 1.27 1.27))))
			(property "Value" "SW_SPST" (at 0 -2.54 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
		)
		(symbol "Switch:SW_DPDT_x2"
			(pin passive line (at -5.08 2.54 0) (length 2.54)
				(name "A" (effects (font (size 1.27 1.27))))
				(number "1" (effects (font (size 1.27 1.27))))
			)
			(pin passive line (at 0 2.54 270) (length 2.54)
				(name "B" (effects (font (size 1.27 1.27))))
				(number "2" (effects (font (size 1.27 1.27))))
			)
			(pin passive line (at 5.08 2.54 180) (length 2.54)
				(name "C" (effects (font (size 1.27 1.27))))
				(number "3" (effects (font (size 1.27 1.27))))
			)
			(pin passive line (at -5.08 -2.54 0) (length 2.54)
				(name "D" (effects (font (size 1.27 1.27))))
				(number "4" (effects (font (size 1.27 1.27))))
			)
			(pin passive line (at 0 -2.54 90) (length 2.54)
				(name "E" (effects (font (size 1.27 1.27))))
				(number "5" (effects (font (size 1.27 1.27))))
			)
			(pin passive line (at 5.08 -2.54 180) (length 2.54)
				(name "F" (effects (font (size 1.27 1.27))))
				(number "6" (effects (font (size 1.27 1.27))))
			)
			(property "Reference" "SW" (at 0 5.08 0) (effects (font (size 1.27 1.27))))
			(property "Value" "SW_DPDT" (at 0 -5.08 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
		)
		(symbol "Connector:Conn_01x02_Pin"
			(pin passive line (at -2.54 1.27 0) (length 2.54)
				(name "Pin_1" (effects (font (size 1.27 1.27))))
				(number "1" (effects (font (size 1.27 1.27))))
			)
			(pin passive line (at -2.54 -1.27 0) (length 2.54)
				(name "Pin_2" (effects (font (size 1.27 1.27))))
				(number "2" (effects (font (size 1.27 1.27))))
			)
			(property "Reference" "J" (at 0 3.81 0) (effects (font (size 1.27 1.27))))
			(property "Value" "Conn_01x02" (at 0 -3.81 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
		)
		(symbol "Connector:Conn_01x03_Pin"
			(pin passive line (at -2.54 2.54 0) (length 2.54)
				(name "Pin_1" (effects (font (size 1.27 1.27))))
				(number "1" (effects (font (size 1.27 1.27))))
			)
			(pin passive line (at -2.54 0 0) (length 2.54)
				(name "Pin_2" (effects (font (size 1.27 1.27))))
				(number "2" (effects (font (size 1.27 1.27))))
			)
			(pin passive line (at -2.54 -2.54 0) (length 2.54)
				(name "Pin_3" (effects (font (size 1.27 1.27))))
				(number "3" (effects (font (size 1.27 1.27))))
			)
			(property "Reference" "J" (at 0 5.08 0) (effects (font (size 1.27 1.27))))
			(property "Value" "Conn_01x03" (at 0 -5.08 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
		)
		(symbol "Connector_Audio:XLR3_Female"
			(pin passive line (at -5.08 2.54 0) (length 2.54)
				(name "1" (effects (font (size 1.27 1.27))))
				(number "1" (effects (font (size 1.27 1.27))))
			)
			(pin passive line (at -5.08 0 0) (length 2.54)
				(name "2" (effects (font (size 1.27 1.27))))
				(number "2" (effects (font (size 1.27 1.27))))
			)
			(pin passive line (at -5.08 -2.54 0) (length 2.54)
				(name "3" (effects (font (size 1.27 1.27))))
				(number "3" (effects (font (size 1.27 1.27))))
			)
			(property "Reference" "J" (at 0 5.08 0) (effects (font (size 1.27 1.27))))
			(property "Value" "XLR3_Female" (at 0 -5.08 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
		)
		(symbol "Amplifier_Operational:NE5532"
			(pin input line (at -5.08 2.54 0) (length 2.54)
				(name "+" (effects (font (size 1.27 1.27))))
				(number "3" (effects (font (size 1.27 1.27))))
			)
			(pin input line (at -5.08 -2.54 0) (length 2.54)
				(name "-" (effects (font (size 1.27 1.27))))
				(number "2" (effects (font (size 1.27 1.27))))
			)
			(pin output line (at 5.08 0 180) (length 2.54)
				(name "~" (effects (font (size 1.27 1.27))))
				(number "1" (effects (font (size 1.27 1.27))))
			)
			(pin power_in line (at 0 5.08 270) (length 2.54)
				(name "V+" (effects (font (size 1.27 1.27))))
				(number "8" (effects (font (size 1.27 1.27))))
			)
			(pin power_in line (at 0 -5.08 90) (length 2.54)
				(name "V-" (effects (font (size 1.27 1.27))))
				(number "4" (effects (font (size 1.27 1.27))))
			)
			(property "Reference" "U" (at 2.54 5.08 0) (effects (font (size 1.27 1.27))))
			(property "Value" "NE5532" (at 2.54 -5.08 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "Package_DIP:DIP-8_W7.62mm" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
		)
		(symbol "Regulator_Linear:LM317_TO220"
			(pin input line (at -5.08 2.54 0) (length 2.54)
				(name "VI" (effects (font (size 1.27 1.27))))
				(number "3" (effects (font (size 1.27 1.27))))
			)
			(pin input line (at 0 -5.08 90) (length 2.54)
				(name "ADJ" (effects (font (size 1.27 1.27))))
				(number "1" (effects (font (size 1.27 1.27))))
			)
			(pin power_out line (at 5.08 2.54 180) (length 2.54)
				(name "VO" (effects (font (size 1.27 1.27))))
				(number "2" (effects (font (size 1.27 1.27))))
			)
			(property "Reference" "U" (at 0 5.08 0) (effects (font (size 1.27 1.27))))
			(property "Value" "LM317HV" (at 0 -7.62 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "Package_TO_SOT_THT:TO-220-3_Vertical" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
		)
		(symbol "Transistor_FET:P-MOSFET"
			(pin input line (at -5.08 0 0) (length 2.54)
				(name "G" (effects (font (size 1.27 1.27))))
				(number "1" (effects (font (size 1.27 1.27))))
			)
			(pin passive line (at 2.54 5.08 270) (length 2.54)
				(name "D" (effects (font (size 1.27 1.27))))
				(number "2" (effects (font (size 1.27 1.27))))
			)
			(pin passive line (at 2.54 -5.08 90) (length 2.54)
				(name "S" (effects (font (size 1.27 1.27))))
				(number "3" (effects (font (size 1.27 1.27))))
			)
			(property "Reference" "Q" (at 5.08 2.54 0) (effects (font (size 1.27 1.27))))
			(property "Value" "IRF4905" (at 5.08 -2.54 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "Package_TO_SOT_THT:TO-220-3_Vertical" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
		)
		(symbol "power:PWR_FLAG"
			(pin power_out line (at 0 0 90) (length 0)
				(name "~" (effects (font (size 1.27 1.27))))
				(number "1" (effects (font (size 1.27 1.27))))
			)
			(property "Reference" "#FLG" (at 0 1.905 0) (effects (font (size 1.27 1.27)) hide))
			(property "Value" "PWR_FLAG" (at 0 3.81 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
		)
		(symbol "Connector:TestPoint"
			(pin passive line (at 0 0 0) (length 0)
				(name "1" (effects (font (size 1.27 1.27))))
				(number "1" (effects (font (size 1.27 1.27))))
			)
			(property "Reference" "TP" (at 0 2.54 0) (effects (font (size 1.27 1.27))))
			(property "Value" "TestPoint" (at 0 -2.54 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "TestPoint:TestPoint_Pad_D1.5mm" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
		)
	)
"""

    instances = []
    def add_sym(lib_id, ref, val, x, y, foot="", unit=1, props=None):
        u = uid()
        p_str = ""
        if props:
            for pk, pv in props.items():
                p_str += f'\n\t\t(property "{pk}" "{pv}" (at {x} {y} 0) (effects (font (size 1.27 1.27))))'
        inst = f"""\t(symbol
\t\t(lib_id "{lib_id}")
\t\t(at {x} {y} 0)
\t\t(unit {unit})
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(dnp no)
\t\t(uuid "{u}")
\t\t(property "Reference" "{ref}" (at {x+2.54} {y-2.54} 0) (effects (font (size 1.27 1.27))))
\t\t(property "Value" "{val}" (at {x+2.54} {y} 0) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "{foot}" (at {x} {y} 0) (effects (font (size 1.27 1.27)) hide)){p_str}
\t)"""
        instances.append(inst)
        return u

    # Place Symbols
    add_sym("Connector_Audio:XLR3_Female", "J1", "MIC_XLR_IN", 40.0, 50.0, "Connector_Audio:Neutrik_NC3FAAH2_Horizontal")
    add_sym("Device:C", "C1", "47pF", 55.0, 40.0, "Capacitor_THT:C_Disc_D4.3mm_W1.9mm_P5.00mm")
    add_sym("Device:C", "C2", "47pF", 55.0, 60.0, "Capacitor_THT:C_Disc_D4.3mm_W1.9mm_P5.00mm")
    add_sym("Device:R", "R1", "100k", 65.0, 40.0, "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    add_sym("Device:R", "R2", "100k", 65.0, 60.0, "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    add_sym("Device:C_Polarized", "C4", "10uF/50V_BP", 80.0, 45.0, "Capacitor_THT:CP_Radial_D6.3mm_P2.50mm")
    add_sym("Device:C_Polarized", "C5", "10uF/50V_BP", 80.0, 55.0, "Capacitor_THT:CP_Radial_D6.3mm_P2.50mm")
    add_sym("Device:R", "R3", "10k_1%", 95.0, 45.0, "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    add_sym("Device:R", "R5", "10k_1%", 95.0, 55.0, "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    add_sym("Device:R", "R4", "100k_1%", 110.0, 35.0, "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    add_sym("Device:R", "R6", "100k_1%", 110.0, 65.0, "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    add_sym("Device:R_Potentiometer", "RV1", "50k_RevLog_MIC_GAIN", 125.0, 65.0, "Potentiometer_THT:Potentiometer_Bourns_3386P_Vertical")
    add_sym("Amplifier_Operational:NE5532", "U1", "NE5532P", 125.0, 50.0, "Package_DIP:DIP-8_W7.62mm", unit=1)
    add_sym("Device:C_Polarized", "C6", "10uF/25V", 145.0, 50.0, "Capacitor_THT:CP_Radial_D5.0mm_P2.00mm")
    add_sym("Device:C", "C7", "68nF_Film", 160.0, 50.0, "Capacitor_THT:C_Rect_L7.2mm_W3.5mm_P5.00mm_FKS2_FKP2_MKS2_MKP2")
    add_sym("Device:C", "C8", "68nF_Film", 175.0, 50.0, "Capacitor_THT:C_Rect_L7.2mm_W3.5mm_P5.00mm_FKS2_FKP2_MKS2_MKP2")
    add_sym("Device:R", "R8", "27k_1%", 170.0, 35.0, "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    add_sym("Device:R", "R9", "56k_1%", 175.0, 65.0, "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    add_sym("Amplifier_Operational:NE5532", "U1", "NE5532P", 195.0, 50.0, "Package_DIP:DIP-8_W7.62mm", unit=2)
    add_sym("Device:C_Polarized", "C9", "10uF/25V", 215.0, 50.0, "Capacitor_THT:CP_Radial_D5.0mm_P2.00mm")
    add_sym("Device:R_Potentiometer", "RV2", "10k_Log_MIC_VOL", 230.0, 50.0, "Potentiometer_THT:Potentiometer_Bourns_3386P_Vertical")

    # Line input
    add_sym("Connector_Audio:XLR3_Female", "J2", "COMBO_LINE_IN", 40.0, 110.0, "Connector_Audio:Neutrik_NCJ6FI-V_Horizontal")
    add_sym("Device:C", "C10", "47pF", 55.0, 100.0, "Capacitor_THT:C_Disc_D4.3mm_W1.9mm_P5.00mm")
    add_sym("Device:C", "C11", "47pF", 55.0, 120.0, "Capacitor_THT:C_Disc_D4.3mm_W1.9mm_P5.00mm")
    add_sym("Device:C", "C12", "1uF_Film", 75.0, 105.0, "Capacitor_THT:C_Rect_L7.2mm_W3.5mm_P5.00mm_FKS2_FKP2_MKS2_MKP2")
    add_sym("Device:C", "C13", "1uF_Film", 75.0, 115.0, "Capacitor_THT:C_Rect_L7.2mm_W3.5mm_P5.00mm_FKS2_FKP2_MKS2_MKP2")
    add_sym("Device:R", "R12", "20k_1%", 95.0, 105.0, "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    add_sym("Device:R", "R14", "20k_1%", 95.0, 115.0, "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    add_sym("Device:R", "R13", "10k_1%", 115.0, 95.0, "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    add_sym("Device:R", "R15", "10k_1%", 115.0, 125.0, "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    add_sym("Amplifier_Operational:NE5532", "U2", "NE5532P", 130.0, 110.0, "Package_DIP:DIP-8_W7.62mm", unit=1)
    add_sym("Device:C_Polarized", "C14", "10uF/25V", 150.0, 110.0, "Capacitor_THT:CP_Radial_D5.0mm_P2.00mm")
    add_sym("Device:R_Potentiometer", "RV3", "10k_Log_LINE_VOL", 165.0, 110.0, "Potentiometer_THT:Potentiometer_Bourns_3386P_Vertical")

    # Mode switch
    add_sym("Switch:SW_DPDT_x2", "SW1", "DPDT_MODE_SELECT", 260.0, 80.0, "Button_Switch_THT:SW_MEC_5G")

    # DC power circuit
    add_sym("Connector:Conn_01x02_Pin", "J3", "DC_36V_IN", 40.0, 170.0, "Connector_BarrelJack:BarrelJack_Horizontal")
    add_sym("Device:Fuse", "F1", "T3.15A_250V_5x20mm", 60.0, 165.0, "Fuse:Fuseholder_Cylinder-5x20mm_Schurter_0031_8201_Horizontal_Open")
    add_sym("Transistor_FET:P-MOSFET", "Q1", "IRF4905", 85.0, 165.0, "Package_TO_SOT_THT:TO-220-3_Vertical")
    add_sym("Device:D_Zener", "D1", "BZX79C12_12V", 80.0, 180.0, "Diode_THT:D_DO-35_SOD27_P7.62mm_Horizontal")
    add_sym("Device:R", "R16", "100k", 95.0, 180.0, "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    add_sym("Device:C_Polarized", "C15", "470uF/50V_LowESR", 110.0, 180.0, "Capacitor_THT:CP_Radial_D10.0mm_P5.00mm")
    add_sym("Device:C", "C16", "100nF/50V", 120.0, 180.0, "Capacitor_THT:C_Rect_L7.2mm_W2.5mm_P5.00mm_FKS2_FKP2_MKS2_MKP2")
    add_sym("Regulator_Linear:LM317_TO220", "U3", "LM317HVT", 145.0, 165.0, "Package_TO_SOT_THT:TO-220-3_Vertical")
    add_sym("Device:R", "R17", "240R_1%", 150.0, 180.0, "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    add_sym("Device:R", "R18", "2.64k_1%", 160.0, 180.0, "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    add_sym("Device:C_Polarized", "C17", "10uF/25V", 170.0, 180.0, "Capacitor_THT:CP_Radial_D5.0mm_P2.00mm")
    add_sym("Device:D", "D2", "1N4007", 145.0, 150.0, "Diode_THT:D_DO-41_SOD81_P10.16mm_Horizontal")
    add_sym("Device:D", "D3", "1N4007", 155.0, 172.0, "Diode_THT:D_DO-41_SOD81_P10.16mm_Horizontal")
    add_sym("Device:C_Polarized", "C18", "100uF/25V", 185.0, 180.0, "Capacitor_THT:CP_Radial_D6.3mm_P2.50mm")
    add_sym("Device:C", "C19", "100nF/50V", 195.0, 180.0, "Capacitor_THT:C_Rect_L7.2mm_W2.5mm_P5.00mm_FKS2_FKP2_MKS2_MKP2")
    add_sym("Device:R", "R19", "10k_1%", 215.0, 165.0, "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    add_sym("Device:R", "R20", "10k_1%", 215.0, 185.0, "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    add_sym("Device:C_Polarized", "C20", "47uF/25V", 225.0, 185.0, "Capacitor_THT:CP_Radial_D5.0mm_P2.00mm")
    add_sym("Amplifier_Operational:NE5532", "U2", "NE5532P", 245.0, 175.0, "Package_DIP:DIP-8_W7.62mm", unit=2)
    add_sym("Device:C", "C21", "100nF/50V", 260.0, 185.0, "Capacitor_THT:C_Rect_L7.2mm_W2.5mm_P5.00mm_FKS2_FKP2_MKS2_MKP2")

    # Amp & Driver interface
    add_sym("Connector:Conn_01x02_Pin", "J4", "AMP_POWER_36V", 310.0, 50.0, "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal")
    add_sym("Connector:Conn_01x03_Pin", "J5", "AMP_AUDIO_IN", 310.0, 80.0, "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical")
    add_sym("Connector:Conn_01x02_Pin", "J6", "AMP_SPEAKER_OUT", 310.0, 120.0, "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal")
    add_sym("Device:L", "L1", "1.0mH_AirCore_0.35R", 340.0, 110.0, "Inductor_THT:L_Radial_D25.0mm_P15.00mm")
    add_sym("Device:C", "C24", "4.7uF/250V_MKP", 340.0, 125.0, "Capacitor_THT:C_Rect_L18.0mm_W9.0mm_P15.00mm_FKS3_FKP3")
    add_sym("Device:R", "R21", "8.2R_10W_NonInductive", 340.0, 140.0, "Resistor_THT:R_Axial_Power_L25.0mm_D9.0mm_P30.00mm_Horizontal")
    add_sym("Switch:SW_SPST", "SW2", "CONTOUR_BYPASS", 340.0, 95.0, "Button_Switch_THT:SW_MEC_5G")
    add_sym("Connector:Conn_01x02_Pin", "J7", "VISATON_BG20_8R", 380.0, 120.0, "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal")

    # Power flags & Test Points
    add_sym("power:PWR_FLAG", "#FLG2", "PWR_FLAG", 125.0, 58.0)
    add_sym("Connector:TestPoint", "TP1", "TP_MODE_STATUS", 280.0, 80.0, "TestPoint:TestPoint_Pad_D1.5mm")

    # Net connections map: (pin_x, pin_y, net_name)
    pin_nets = [
        # Power flags & TP1
        (125.0, 58.0, "GND"),
        (280.0, 80.0, "MODE_STATUS"),
        # J1
        (34.92, 47.46, "GND_CHASSIS"),
        (34.92, 50.0,  "MIC_HOT_RAW"),
        (34.92, 52.54, "MIC_COLD_RAW"),
        # C1
        (55.0, 37.46, "GND"),
        (55.0, 42.54, "MIC_HOT_RAW"),
        # C2
        (55.0, 57.46, "MIC_COLD_RAW"),
        (55.0, 62.54, "GND"),
        # R1
        (65.0, 37.46, "GND"),
        (65.0, 42.54, "MIC_HOT_RAW"),
        # R2
        (65.0, 57.46, "MIC_COLD_RAW"),
        (65.0, 62.54, "GND"),
        # C4
        (80.0, 42.46, "MIC_HOT_RAW"),
        (80.0, 47.54, "MIC_HOT_DC"),
        # C5
        (80.0, 52.46, "MIC_COLD_DC"),
        (80.0, 57.54, "MIC_COLD_RAW"),
        # R3
        (95.0, 42.46, "MIC_HOT_DC"),
        (95.0, 47.54, "MIC_PRE_NONINV"),
        # R5
        (95.0, 52.46, "MIC_PRE_INV"),
        (95.0, 57.54, "MIC_COLD_DC"),
        # R4
        (110.0, 32.46, "VBIAS_7V5"),
        (110.0, 37.54, "MIC_PRE_NONINV"),
        # R6
        (110.0, 62.46, "MIC_PRE_INV"),
        (110.0, 67.54, "MIC_GAIN_POT"),
        # RV1
        (125.0, 62.46, "MIC_GAIN_POT"),
        (127.54, 65.0, "MIC_PRE_OUT"),
        (125.0, 67.54, "MIC_PRE_OUT"),
        # U1A
        (119.92, 47.46, "MIC_PRE_NONINV"),
        (119.92, 52.54, "MIC_PRE_INV"),
        (130.08, 50.0,  "MIC_PRE_OUT"),
        (125.0, 44.92,  "+15V"),
        (125.0, 55.08,  "GND"),
        # C6
        (145.0, 47.46, "MIC_PRE_OUT"),
        (145.0, 52.54, "HPF_STAGE_IN"),
        # C7
        (160.0, 47.46, "HPF_STAGE_IN"),
        (160.0, 52.54, "HPF_MID_NODE"),
        # R8
        (170.0, 32.46, "HPF_OUT"),
        (170.0, 37.54, "HPF_MID_NODE"),
        # C8
        (175.0, 47.46, "HPF_MID_NODE"),
        (175.0, 52.54, "HPF_NONINV"),
        # R9
        (175.0, 62.46, "HPF_NONINV"),
        (175.0, 67.54, "VBIAS_7V5"),
        # U1B
        (189.92, 47.46, "HPF_NONINV"),
        (189.92, 52.54, "HPF_OUT"),
        (200.08, 50.0,  "HPF_OUT"),
        (195.0, 44.92,  "+15V"),
        (195.0, 55.08,  "GND"),
        # C9
        (215.0, 47.46, "HPF_OUT"),
        (215.0, 52.54, "MIC_VOL_POT_IN"),
        # RV2
        (230.0, 47.46, "MIC_VOL_POT_IN"),
        (232.54, 50.0, "MODE_A_MIC_SIG"),
        (230.0, 52.54, "GND"),

        # J2
        (34.92, 107.46, "GND_CHASSIS"),
        (34.92, 110.0,  "LINE_HOT_RAW"),
        (34.92, 112.54, "LINE_COLD_RAW"),
        # C10
        (55.0, 97.46,  "GND"),
        (55.0, 102.54, "LINE_HOT_RAW"),
        # C11
        (55.0, 117.46, "LINE_COLD_RAW"),
        (55.0, 122.54, "GND"),
        # C12
        (75.0, 102.46, "LINE_HOT_RAW"),
        (75.0, 107.54, "LINE_HOT_DC"),
        # C13
        (75.0, 112.46, "LINE_COLD_DC"),
        (75.0, 117.54, "LINE_COLD_RAW"),
        # R12
        (95.0, 102.46, "LINE_COLD_DC"),
        (95.0, 107.54, "LINE_REC_INV"),
        # R14
        (95.0, 112.46, "LINE_REC_NONINV"),
        (95.0, 117.54, "LINE_HOT_DC"),
        # R13
        (115.0, 92.46, "LINE_REC_OUT"),
        (115.0, 97.54, "LINE_REC_INV"),
        # R15
        (115.0, 122.46, "LINE_REC_NONINV"),
        (115.0, 127.54, "VBIAS_7V5"),
        # U2A
        (124.92, 107.46, "LINE_REC_NONINV"),
        (124.92, 112.54, "LINE_REC_INV"),
        (135.08, 110.0,  "LINE_REC_OUT"),
        (130.0, 104.92,  "+15V"),
        (130.0, 115.08,  "GND"),
        # C14
        (150.0, 107.46, "LINE_REC_OUT"),
        (150.0, 112.54, "LINE_VOL_POT_IN"),
        # RV3
        (165.0, 107.46, "LINE_VOL_POT_IN"),
        (167.54, 110.0, "MODE_B_LINE_SIG"),
        (165.0, 112.54, "GND"),

        # SW1
        (254.92, 77.46, "MODE_A_MIC_SIG"),
        (260.0, 77.46,  "AMP_INPUT_SIG"),
        (265.08, 77.46, "MODE_B_LINE_SIG"),
        (254.92, 82.54, "GND"),
        (260.0, 82.54,  "MODE_STATUS"),
        (265.08, 82.54, "VBIAS_7V5"),

        # J3
        (37.46, 168.73, "DC_IN_RAW"),
        (37.46, 171.27, "GND"),
        # F1
        (60.0, 162.46, "DC_IN_RAW"),
        (60.0, 167.54, "DC_FUSED"),
        # Q1
        (79.92, 165.0,  "PMOS_GATE"),
        (87.54, 159.92, "DC_FUSED"),
        (87.54, 170.08, "+36V"),
        # D1
        (80.0, 177.46, "+36V"),
        (80.0, 182.54, "PMOS_GATE"),
        # R16
        (95.0, 177.46, "PMOS_GATE"),
        (95.0, 182.54, "GND"),
        # C15
        (110.0, 177.46, "+36V"),
        (110.0, 182.54, "GND"),
        # C16
        (120.0, 177.46, "+36V"),
        (120.0, 182.54, "GND"),
        # U3
        (139.92, 162.46, "+36V"),
        (145.0, 170.08,  "LM317_ADJ"),
        (150.08, 162.46, "+15V"),
        # D2
        (145.0, 147.46, "+36V"),
        (145.0, 152.54, "+15V"),
        # D3
        (155.0, 169.46, "+15V"),
        (155.0, 174.54, "LM317_ADJ"),
        # R17
        (150.0, 177.46, "+15V"),
        (150.0, 182.54, "LM317_ADJ"),
        # R18
        (160.0, 177.46, "LM317_ADJ"),
        (160.0, 182.54, "GND"),
        # C17
        (170.0, 177.46, "LM317_ADJ"),
        (170.0, 182.54, "GND"),
        # C18
        (185.0, 177.46, "+15V"),
        (185.0, 182.54, "GND"),
        # C19
        (195.0, 177.46, "+15V"),
        (195.0, 182.54, "GND"),
        # R19
        (215.0, 162.46, "+15V"),
        (215.0, 167.54, "VBIAS_DIV"),
        # R20
        (215.0, 182.46, "VBIAS_DIV"),
        (215.0, 187.54, "GND"),
        # C20
        (225.0, 182.46, "VBIAS_DIV"),
        (225.0, 187.54, "GND"),
        # U2B
        (239.92, 172.46, "VBIAS_DIV"),
        (239.92, 177.54, "VBIAS_7V5"),
        (250.08, 175.0,  "VBIAS_7V5"),
        (245.0, 169.92,  "+15V"),
        (245.0, 180.08,  "GND"),
        # C21
        (260.0, 182.46, "VBIAS_7V5"),
        (260.0, 187.54, "GND"),

        # J4
        (307.46, 48.73, "+36V"),
        (307.46, 51.27, "GND"),
        # J5
        (307.46, 77.46, "AMP_INPUT_SIG"),
        (307.46, 80.0,  "GND"),
        (307.46, 82.54, "GND_CHASSIS"),
        # J6
        (307.46, 118.73, "AMP_OUT_POS"),
        (307.46, 121.27, "AMP_OUT_NEG"),
        # SW2
        (334.92, 95.0, "AMP_OUT_POS"),
        (345.08, 95.0, "SPK_OUT_POS"),
        # L1
        (340.0, 107.46, "AMP_OUT_POS"),
        (340.0, 112.54, "SPK_OUT_POS"),
        # C24
        (340.0, 122.46, "AMP_OUT_POS"),
        (340.0, 127.54, "SPK_OUT_POS"),
        # R21
        (340.0, 137.46, "AMP_OUT_POS"),
        (340.0, 142.54, "SPK_OUT_POS"),
        # J7
        (377.46, 118.73, "SPK_OUT_POS"),
        (377.46, 121.27, "AMP_OUT_NEG")
    ]

    labels = []
    for px, py, net in pin_nets:
        u = uid()
        lbl = f"""\t(label "{net}"
\t\t(at {px} {py} 0.0000)
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
	(sheet_instances
		(path "/"
			(page "1")
		)
	)
	(embedded_fonts no)
)
"""
    with open(sch_file, "w") as f:
        f.write(full_sch)
    print(f"Generated {sch_file} with {len(instances)} symbols and {len(labels)} net labels.")

if __name__ == "__main__":
    main()
