import re, uuid

pcb_file = "projects/live-pa-system/live-pa-system.kicad_pcb"

with open(pcb_file, "r") as f:
    content = f.read()

# Board dimensions
BOARD_W = 160.0
BOARD_H = 100.0

# 1. New Component Placements (x, y, rot)
# Origin (0,0) is top-left
placements = {
    # Corner Mounting Holes (M3)
    "H1": (5.0, 5.0, 0),
    "H2": (155.0, 5.0, 0),
    "H3": (155.0, 95.0, 0),
    "H4": (5.0, 95.0, 0),

    # =========================================================================
    # ZONE 1: MIC PREAMP SECTION (Far Left, X: 10 to 45 mm)
    # =========================================================================
    "J1":  (16.0, 22.0, 0),    # Neutrik NC3FAH XLR Female (faces top edge)
    "C1":  (32.0, 14.0, 0),    # 47pF RF filter Hot
    "R1":  (32.0, 19.0, 0),    # 100k bleeder Hot
    "C2":  (32.0, 25.0, 0),    # 47pF RF filter Cold
    "R2":  (32.0, 30.0, 0),    # 100k bleeder Cold
    "C4":  (16.0, 42.0, 0),    # 10uF BP input coupling Hot
    "C5":  (24.0, 42.0, 0),    # 10uF BP input coupling Cold
    "R3":  (34.0, 38.0, 0),    # 2.2k 0.1% Rin Hot
    "R5":  (34.0, 44.0, 0),    # 2.2k 0.1% Rin Cold
    "R4":  (44.0, 38.0, 0),    # 4.7k 0.1% Rbias to Vbias
    "R6":  (44.0, 44.0, 0),    # 4.7k 0.1% Rfb
    "U1":  (28.0, 56.0, 0),    # NE5532P (Mic Preamp Stage 1A & Stage 2B)
    "C3":  (38.0, 56.0, 90),   # 100nF decoupling
    "C6":  (16.0, 68.0, 0),    # 10uF interstage coupling
    "R7":  (24.0, 68.0, 0),    # 47k to Vbias
    "R8":  (32.0, 68.0, 0),    # 330R gain resistor
    "R10": (40.0, 68.0, 0),    # 1.2k gain resistor
    "RV1": (16.0, 84.0, 0),    # 50k RevLog Mic Gain Pot
    "C7":  (28.0, 84.0, 0),    # 10uF output coupling
    "RV2": (40.0, 84.0, 0),    # 10k Log Mic Volume Pot

    # =========================================================================
    # ZONE 2: LINE RECEIVER & COMMON HPF (Center-Left, X: 50 to 90 mm)
    # =========================================================================
    "J2":  (62.0, 22.0, 0),    # Neutrik NCJ6FI-H Combo Jack
    "C10": (80.0, 14.0, 0),    # 47pF RF filter Hot
    "R12": (80.0, 19.0, 0),    # 100k bleeder Hot
    "C11": (80.0, 25.0, 0),    # 47pF RF filter Cold
    "R13": (80.0, 30.0, 0),    # 100k bleeder Cold
    "C12": (56.0, 42.0, 0),    # 1uF film input coupling Hot
    "C13": (66.0, 42.0, 0),    # 1uF film input coupling Cold
    "R14": (78.0, 38.0, 0),    # 30k 0.1% Rin Hot
    "R15": (78.0, 44.0, 0),    # 30k 0.1% Rin Cold
    "R16": (88.0, 38.0, 0),    # 10k 0.1% Rbias to Vbias
    "R17": (88.0, 44.0, 0),    # 10k 0.1% Rfb
    "U2":  (72.0, 56.0, 0),    # NE5532P (Line Rec U2B + HPF U2A)
    "C16": (82.0, 56.0, 90),   # 100nF decoupling
    "C15": (56.0, 68.0, 0),    # 10uF post-line coupling
    "RV3": (56.0, 84.0, 0),    # 10k Log Line Volume Pot
    "SW1": (72.0, 84.0, 0),    # DPDT Mode Select Switch
    "TP1": (80.0, 84.0, 0),    # Mode Status Test Point
    "C8":  (66.0, 68.0, 0),    # HPF C8 68nF Film
    "R9":  (74.0, 68.0, 0),    # HPF R9 27k 1%
    "C9":  (82.0, 68.0, 0),    # HPF C9 68nF Film
    "R11": (90.0, 68.0, 0),    # HPF R11 56k 1% to Vbias
    "C14": (70.0, 93.0, 0),    # 10uF Master Output Coupling
    "R24": (78.0, 93.0, 0),    # 100k Amp Bleeder
    "J5":  (88.0, 93.0, 0),    # AMP_AUDIO_IN (3-pin header to TPA3255)

    # =========================================================================
    # ZONE 3: VIRTUAL GROUND GENERATOR (Center-Right, X: 94 to 116 mm)
    # =========================================================================
    "R21": (98.0, 22.0, 0),    # 10k divider top (+15V to Div)
    "R22": (98.0, 28.0, 0),    # 10k divider bottom (Div to GND)
    "C22": (106.0, 25.0, 0),   # 10uF divider bypass
    "U3":  (104.0, 48.0, 0),   # NE5532P (Vbias buffer + terminated spare)
    "C26": (114.0, 48.0, 90),  # 100nF decoupling
    "C23": (98.0, 62.0, 0),    # 47uF Vbias bulk filter
    "C25": (106.0, 62.0, 0),   # 100nF Vbias HF bypass

    # =========================================================================
    # ZONE 4: POWER SUPPLY & +15V REGULATION (Top Right, X: 118 to 155 mm)
    # =========================================================================
    "J3":  (120.0, 16.0, -90), # DC 36V Barrel Jack
    "F1":  (140.0, 16.0, 0),   # 5x20mm Fuseholder (T3.15A)
    "Q1":  (122.0, 30.0, 0),   # IRF4905 P-MOSFET (TO-220)
    "D1":  (132.0, 27.0, 0),   # 12V Zener (BZX79C12)
    "R18": (132.0, 33.0, 0),   # 100k Gate pull-down
    "C17": (146.0, 27.0, 0),   # 470uF 50V Low-ESR Bulk
    "C18": (146.0, 36.0, 0),   # 100nF 50V HF Ceramic
    "J4":  (118.0, 6.0, 180),  # 2-pin DC 36V terminal to TPA3255
    "U4":  (122.0, 45.0, 0),   # LM317HVT Linear Regulator (TO-220)
    "D2":  (132.0, 42.0, 0),   # 1N4007 Reverse Protection
    "D3":  (132.0, 48.0, 0),   # 1N4007 Cadj Bypass
    "R19": (140.0, 42.0, 0),   # 240R 1% Program resistor
    "R20": (140.0, 48.0, 0),   # 2.64k 1% Program resistor
    "C19": (148.0, 45.0, 0),   # 10uF Cadj ripple bypass
    "C20": (122.0, 58.0, 0),   # 100uF +15V output bulk
    "C21": (130.0, 58.0, 0),   # 100nF +15V HF bypass

    # =========================================================================
    # ZONE 5: PASSIVE RLC CONTOUR FILTER & SPEAKER (Bottom Right, X: 118 to 155 mm)
    # Strictly isolated from Signal GND & Chassis GND!
    # =========================================================================
    "J6":  (120.0, 72.0, 180), # Speaker In from TPA3255 PBTL (2-pin terminal)
    "SW2": (120.0, 86.0, 0),   # Contour Bypass Slide Switch
    "L1":  (142.0, 72.0, 0),   # 1.0mH Air Core Inductor (Vishay IHB-3, 28mm dia)
    "C24": (140.0, 90.0, 0),   # 4.7uF MKP Capacitor
    "R23": (122.0, 96.0, 0),   # 8.2R 10W Non-Inductive Power Resistor
    "J7":  (152.0, 88.0, 180), # Output to Visaton BG 20 Driver (2-pin terminal)
}

# 2. Update each footprint position in content
def update_fp(match):
    fp_text = match.group(0)
    ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', fp_text)
    if not ref_m:
        return fp_text
    ref = ref_m.group(1)
    if ref in placements:
        x, y, rot = placements[ref]
        # Replace (at X Y [ROT])
        if rot == 0:
            at_new = f"(at {x:.2f} {y:.2f})"
        else:
            at_new = f"(at {x:.2f} {y:.2f} {rot})"
        fp_text = re.sub(r'\(at\s+[\d\.\-]+\s+[\d\.\-]+(?:\s+[\d\.\-]+)?\)', at_new, fp_text, count=1)
    return fp_text

content = re.sub(r'\t\(footprint\s+"[^"]+".*?\n\t\)', update_fp, content, flags=re.DOTALL)

# 3. Update Edge.Cuts lines
edge_cuts_str = f"""\t(gr_line
\t\t(start 0 0)
\t\t(end {BOARD_W} 0)
\t\t(stroke
\t\t\t(width 0.15)
\t\t\t(type default)
\t\t)
\t\t(layer "Edge.Cuts")
\t\t(uuid "{uuid.uuid4()}")
\t)
\t(gr_line
\t\t(start {BOARD_W} 0)
\t\t(end {BOARD_W} {BOARD_H})
\t\t(stroke
\t\t\t(width 0.15)
\t\t\t(type default)
\t\t)
\t\t(layer "Edge.Cuts")
\t\t(uuid "{uuid.uuid4()}")
\t)
\t(gr_line
\t\t(start {BOARD_W} {BOARD_H})
\t\t(end 0 {BOARD_H})
\t\t(stroke
\t\t\t(width 0.15)
\t\t\t(type default)
\t\t)
\t\t(layer "Edge.Cuts")
\t\t(uuid "{uuid.uuid4()}")
\t)
\t(gr_line
\t\t(start 0 {BOARD_H})
\t\t(end 0 0)
\t\t(stroke
\t\t\t(width 0.15)
\t\t\t(type default)
\t\t)
\t\t(layer "Edge.Cuts")
\t\t(uuid "{uuid.uuid4()}")
\t)"""

# Remove existing Edge.Cuts gr_line elements
content = re.sub(r'\t\(gr_line\s+\(start\s+[\d\.\-]+\s+[\d\.\-]+\)\s+\(end\s+[\d\.\-]+\s+[\d\.\-]+\)\s+\(stroke\s+\(width\s+[\d\.\-]+\)\s+\(type\s+\w+\)\s*\)\s+\(layer\s+"Edge\.Cuts"\)\s+\(uuid\s+"[^"]+"\)\s*\)', '', content)

# 4. Update mounting hole keepouts for (5,5), (155,5), (155,95), (5,95)
# Remove old keepouts
content = re.sub(r'\t\(zone\s+\(layers\s+"F\.Cu"\s+"B\.Cu"\).*?\(keepout.*?\(polygon\s+\(pts.*?\n\t\)', '', content, flags=re.DOTALL)

def make_hole_keepout(hx, hy):
    r = 3.2
    return f"""\t(zone
\t\t(layers "F.Cu" "B.Cu")
\t\t(uuid "{uuid.uuid4()}")
\t\t(hatch edge 0.5)
\t\t(connect_pads (clearance 0))
\t\t(min_thickness 0.25)
\t\t(keepout (tracks not_allowed) (vias not_allowed) (pads allowed) (copperpour not_allowed) (footprints allowed))
\t\t(placement (enabled no) (sheetname ""))
\t\t(fill (thermal_gap 0.5) (thermal_bridge_width 0.5) (island_removal_mode 0))
\t\t(polygon
\t\t\t(pts (xy {hx-r:.2f} {hy-r:.2f}) (xy {hx+r:.2f} {hy-r:.2f}) (xy {hx+r:.2f} {hy+r:.2f}) (xy {hx-r:.2f} {hy+r:.2f}))
\t\t)
\t)"""

keepouts = "\n".join([make_hole_keepout(5.0, 5.0), make_hole_keepout(155.0, 5.0), make_hole_keepout(155.0, 95.0), make_hole_keepout(5.0, 95.0)])

# 5. Add informative silkscreen text labels for functional zones
def make_silk_text(txt, tx, ty, size=1.5):
    return f"""\t(gr_text "{txt}"
\t\t(at {tx:.2f} {ty:.2f} 0)
\t\t(layer "F.SilkS")
\t\t(uuid "{uuid.uuid4()}")
\t\t(effects
\t\t\t(font (size {size} {size}) (thickness 0.2))
\t\t\t(justify left)
\t\t)
\t)"""

silk_labels = "\n".join([
    make_silk_text("LIVE-PA MONITOR ANALOG & POWER BOARD v2.1", 10.0, 6.0, 1.8),
    make_silk_text("ZONE 1: MIC PREAMP", 12.0, 36.0, 1.2),
    make_silk_text("ZONE 2: LINE & 60Hz HPF", 55.0, 36.0, 1.2),
    make_silk_text("ZONE 3: VBIAS 7.5V", 96.0, 15.0, 1.2),
    make_silk_text("ZONE 4: POWER & +15V REG", 120.0, 3.0, 1.2),
    make_silk_text("ZONE 5: RLC CONTOUR (FLOATING PBTL)", 116.0, 66.0, 1.2),
    make_silk_text("MIC GAIN", 12.0, 90.0, 1.0),
    make_silk_text("MIC VOL", 36.0, 90.0, 1.0),
    make_silk_text("LINE VOL", 52.0, 90.0, 1.0),
    make_silk_text("MODE SEL", 70.0, 90.0, 1.0),
    make_silk_text("AMP SIG OUT", 84.0, 97.0, 1.0),
    make_silk_text("AMP 36V OUT", 112.0, 2.0, 1.0),
    make_silk_text("AMP SPK IN", 116.0, 78.0, 1.0),
    make_silk_text("BG20 SPK OUT", 146.0, 94.0, 1.0),
])

# Insert before final closing paren
closing_idx = content.rfind(")")
new_content = content[:closing_idx] + "\n" + edge_cuts_str + "\n" + keepouts + "\n" + silk_labels + "\n)\n"

with open(pcb_file, "w") as f:
    f.write(new_content)

print(f"Successfully applied organized 5-zone floorplan to {pcb_file} ({BOARD_W}mm x {BOARD_H}mm).")
