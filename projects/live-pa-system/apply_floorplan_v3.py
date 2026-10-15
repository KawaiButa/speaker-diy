import re, uuid

pcb_file = "projects/live-pa-system/live-pa-system.kicad_pcb"

with open(pcb_file, "r") as f:
    content = f.read()

BOARD_W = 180.0
BOARD_H = 110.0

placements = {
    # Corner Mounting Holes (M3)
    "H1": (5.0, 5.0, 0),
    "H2": (175.0, 5.0, 0),
    "H3": (175.0, 105.0, 0),
    "H4": (5.0, 105.0, 0),

    # --- ZONE 1: MIC PREAMP (Far Left) ---
    "J1":  (20.0, 24.0, 0),
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
    "J2":  (70.0, 24.0, 0),
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
    "C9":  (92.0, 70.0, 0),
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
    "F1":  (148.0, 16.0, 0),    # shifted left from 156
    "Q1":  (136.0, 30.0, 0),
    "D1":  (146.0, 27.0, 0),
    "R18": (146.0, 33.0, 0),
    "C17": (166.0, 27.0, 0),
    "C18": (166.0, 36.0, 0),
    "J4":  (130.0, 6.0, 180),
    "U4":  (136.0, 46.0, 0),
    "D2":  (146.0, 42.0, 0),
    "D3":  (146.0, 48.0, 0),
    "R19": (162.0, 42.0, 0),    # shifted from 156 to 162
    "R20": (162.0, 48.0, 0),    # shifted from 156 to 162
    "C19": (172.0, 45.0, 0),
    "C20": (136.0, 58.0, 0),
    "C21": (146.0, 58.0, 0),

    # --- ZONE 5: PASSIVE RLC CONTOUR FILTER & SPEAKER (Bottom Right) ---
    "J6":  (130.0, 72.0, 180),
    "SW2": (130.0, 86.0, 0),
    "L1":  (145.0, 72.0, 0),
    "C24": (144.0, 92.0, 0),
    "R23": (124.0, 100.0, 0),
    "J7":  (168.0, 80.0, 180),   # shifted to y=80
}

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

with open(pcb_file, "w") as f:
    f.write(content)

print("Updated placement v3.")
