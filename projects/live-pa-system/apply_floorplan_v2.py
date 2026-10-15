import re, uuid

pcb_file = "projects/live-pa-system/live-pa-system.kicad_pcb"

with open(pcb_file, "r") as f:
    content = f.read()

# Board dimensions: 180mm x 110mm
BOARD_W = 180.0
BOARD_H = 110.0

placements = {
    # Corner Mounting Holes (M3)
    "H1": (5.0, 5.0, 0),
    "H2": (175.0, 5.0, 0),
    "H3": (175.0, 105.0, 0),
    "H4": (5.0, 105.0, 0),

    # --- ZONE 1: MIC PREAMP (Far Left) ---
    "J1":  (20.0, 24.0, 0),    # Neutrik NC3FAH XLR Female
    "C1":  (36.0, 14.0, 0),
    "R1":  (36.0, 20.0, 0),
    "C2":  (36.0, 26.0, 0),
    "R2":  (36.0, 32.0, 0),
    "C4":  (16.0, 44.0, 0),
    "C5":  (26.0, 44.0, 0),
    "R3":  (36.0, 38.0, 0),
    "R5":  (36.0, 44.0, 0),
    "R4":  (48.0, 38.0, 0),
    "R6":  (48.0, 44.0, 0),
    "U1":  (30.0, 58.0, 0),
    "C3":  (44.0, 58.0, 90),
    "C6":  (16.0, 72.0, 0),
    "R7":  (26.0, 72.0, 0),
    "R8":  (38.0, 70.0, 0),
    "R10": (38.0, 76.0, 0),
    "RV1": (16.0, 90.0, 0),
    "C7":  (28.0, 90.0, 0),
    "RV2": (40.0, 90.0, 0),

    # --- ZONE 2: LINE RECEIVER & COMMON HPF (Center-Left) ---
    "J2":  (70.0, 24.0, 0),    # Neutrik NCJ6FI-H Combo Jack
    "C10": (90.0, 14.0, 0),
    "R12": (90.0, 20.0, 0),
    "C11": (90.0, 26.0, 0),
    "R13": (90.0, 32.0, 0),
    "C12": (60.0, 44.0, 0),
    "C13": (72.0, 44.0, 0),
    "R14": (84.0, 38.0, 0),
    "R15": (84.0, 44.0, 0),
    "R16": (96.0, 38.0, 0),
    "R17": (96.0, 44.0, 0),
    "U2":  (76.0, 58.0, 0),
    "C16": (90.0, 58.0, 90),
    "C15": (60.0, 72.0, 0),
    "RV3": (60.0, 90.0, 0),
    "SW1": (76.0, 90.0, 0),
    "TP1": (86.0, 90.0, 0),
    "C8":  (70.0, 70.0, 0),
    "R9":  (80.0, 70.0, 0),
    "C9":  (90.0, 70.0, 0),
    "R11": (80.0, 76.0, 0),
    "C14": (72.0, 100.0, 0),
    "R24": (82.0, 100.0, 0),
    "J5":  (92.0, 100.0, 0),

    # --- ZONE 3: VIRTUAL GROUND GENERATOR (Center-Right) ---
    "R21": (106.0, 22.0, 0),
    "R22": (106.0, 28.0, 0),
    "C22": (118.0, 25.0, 0),
    "U3":  (110.0, 50.0, 0),
    "C26": (124.0, 50.0, 90),
    "C23": (106.0, 68.0, 0),
    "C25": (118.0, 68.0, 0),

    # --- ZONE 4: POWER SUPPLY & REGULATION (Top Right) ---
    "J3":  (136.0, 16.0, -90),
    "F1":  (156.0, 16.0, 0),
    "Q1":  (136.0, 30.0, 0),
    "D1":  (146.0, 27.0, 0),
    "R18": (146.0, 33.0, 0),
    "C17": (164.0, 27.0, 0),
    "C18": (164.0, 36.0, 0),
    "J4":  (130.0, 6.0, 180),
    "U4":  (136.0, 46.0, 0),
    "D2":  (146.0, 42.0, 0),
    "D3":  (146.0, 48.0, 0),
    "R19": (156.0, 42.0, 0),
    "R20": (156.0, 48.0, 0),
    "C19": (168.0, 45.0, 0),
    "C20": (136.0, 58.0, 0),
    "C21": (146.0, 58.0, 0),

    # --- ZONE 5: PASSIVE RLC CONTOUR FILTER & SPEAKER (Bottom Right) ---
    "J6":  (132.0, 72.0, 180),
    "SW2": (132.0, 86.0, 0),
    "L1":  (150.0, 72.0, 0),
    "C24": (148.0, 92.0, 0),
    "R23": (130.0, 100.0, 0),
    "J7":  (168.0, 92.0, 180),
}

# Update footprints in file
def update_fp(match):
    fp_text = match.group(0)
    ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', fp_text)
    if not ref_m:
        return fp_text
    ref = ref_m.group(1)
    if ref in placements:
        x, y, rot = placements[ref]
        if rot == 0:
            at_new = f"(at {x:.2f} {y:.2f})"
        else:
            at_new = f"(at {x:.2f} {y:.2f} {rot})"
        fp_text = re.sub(r'\(at\s+[\d\.\-]+\s+[\d\.\-]+(?:\s+[\d\.\-]+)?\)', at_new, fp_text, count=1)
    return fp_text

content = re.sub(r'\t\(footprint\s+"[^"]+".*?\n\t\)', update_fp, content, flags=re.DOTALL)

# Remove old Edge.Cuts
content = re.sub(r'\t\(gr_line\s+\(start\s+[\d\.\-]+\s+[\d\.\-]+\)\s+\(end\s+[\d\.\-]+\s+[\d\.\-]+\)\s+\(stroke\s+\(width\s+[\d\.\-]+\)\s+\(type\s+\w+\)\s*\)\s+\(layer\s+"Edge\.Cuts"\)\s+\(uuid\s+"[^"]+"\)\s*\)', '', content)

edge_cuts_str = f"""\t(gr_line
\t\t(start 0 0)
\t\t(end {BOARD_W} 0)
\t\t(stroke (width 0.15) (type default))
\t\t(layer "Edge.Cuts")
\t\t(uuid "{uuid.uuid4()}")
\t)
\t(gr_line
\t\t(start {BOARD_W} 0)
\t\t(end {BOARD_W} {BOARD_H})
\t\t(stroke (width 0.15) (type default))
\t\t(layer "Edge.Cuts")
\t\t(uuid "{uuid.uuid4()}")
\t)
\t(gr_line
\t\t(start {BOARD_W} {BOARD_H})
\t\t(end 0 {BOARD_H})
\t\t(stroke (width 0.15) (type default))
\t\t(layer "Edge.Cuts")
\t\t(uuid "{uuid.uuid4()}")
\t)
\t(gr_line
\t\t(start 0 {BOARD_H})
\t\t(end 0 0)
\t\t(stroke (width 0.15) (type default))
\t\t(layer "Edge.Cuts")
\t\t(uuid "{uuid.uuid4()}")
\t)"""

# Remove old keepouts
content = re.sub(r'\t\(zone\s+\(layers\s+"F\.Cu"\s+"B\.Cu"\).*?\(keepout.*?\(polygon\s+\(pts.*?\n\t\)', '', content, flags=re.DOTALL)

def make_hole_keepout(hx, hy):
    r = 3.5
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

keepouts = "\n".join([make_hole_keepout(5.0, 5.0), make_hole_keepout(175.0, 5.0), make_hole_keepout(175.0, 105.0), make_hole_keepout(5.0, 105.0)])

# Silkscreen text
# Remove old gr_text
content = re.sub(r'\t\(gr_text\s+"[^"]+".*?\(layer\s+"F\.SilkS"\).*?\n\t\)', '', content, flags=re.DOTALL)

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
    make_silk_text("ZONE 2: LINE & 60Hz HPF", 62.0, 36.0, 1.2),
    make_silk_text("ZONE 3: VBIAS 7.5V", 104.0, 15.0, 1.2),
    make_silk_text("ZONE 4: POWER & +15V REG", 136.0, 3.0, 1.2),
    make_silk_text("ZONE 5: RLC CONTOUR (FLOATING PBTL)", 128.0, 65.0, 1.2),
    make_silk_text("MIC GAIN", 12.0, 98.0, 1.0),
    make_silk_text("MIC VOL", 36.0, 98.0, 1.0),
    make_silk_text("LINE VOL", 56.0, 98.0, 1.0),
    make_silk_text("MODE SEL", 74.0, 98.0, 1.0),
    make_silk_text("AMP SIG OUT", 88.0, 106.0, 1.0),
    make_silk_text("AMP 36V OUT", 126.0, 2.0, 1.0),
    make_silk_text("AMP SPK IN", 126.0, 78.0, 1.0),
    make_silk_text("BG20 SPK OUT", 162.0, 98.0, 1.0),
])

closing_idx = content.rfind(")")
new_content = content[:closing_idx] + "\n" + edge_cuts_str + "\n" + keepouts + "\n" + silk_labels + "\n)\n"

with open(pcb_file, "w") as f:
    f.write(new_content)

print(f"Successfully generated clean 5-zone floorplan ({BOARD_W}mm x {BOARD_H}mm).")
