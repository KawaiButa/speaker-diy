import re

pcb_file = "projects/live-pa-system/live-pa-system.kicad_pcb"

with open(pcb_file, "r") as f:
    content = f.read()

shifts = {
    # 1. Clear C25 from J6
    "C25": (120.0, 58.0, 0),
    # 2. Clear C15 from RV3
    "C15": (48.0, 86.0, 0),
    # 3. Clear R12 from R21
    "R21": (118.0, 16.0, 0),
    "R22": (118.0, 24.0, 0),
    "C22": (126.0, 20.0, 0),
    # 4. Clear R9 and R11 from U2
    "R9":  (74.0, 76.0, 0),
    "R11": (74.0, 82.0, 0),
    "C8":  (64.0, 76.0, 0),
    "C9":  (86.0, 76.0, 0),
    # 5. Clear R8 from U1
    "R8":  (42.0, 74.0, 0),
    "R10": (42.0, 80.0, 0),
    # 6. Clear C21 from L1 coil radius
    "C21": (146.0, 52.0, 0),
    "C20": (136.0, 56.0, 0),
    # 7. Clear J4 from J3
    "J4":  (118.0, 6.0, 180),
    # 8, 9, 10. Clear Zone 5 RLC & Speaker Terminals
    "J6":  (132.0, 72.0, 180),
    "SW2": (132.0, 86.0, 0),
    "L1":  (150.0, 68.0, 0),
    "J7":  (170.0, 68.0, 180),
    "C24": (154.0, 92.0, 0),
    "R23": (124.0, 102.0, 0),
}

def update_fp(match):
    fp_text = match.group(0)
    ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', fp_text)
    if not ref_m:
        return fp_text
    ref = ref_m.group(1)
    if ref in shifts:
        x, y, rot = shifts[ref]
        if rot == 0:
            at_new = f"(at {x:.2f} {y:.2f})"
        else:
            at_new = f"(at {x:.2f} {y:.2f} {rot})"
        fp_text = re.sub(r'\(at\s+[\d\.\-]+\s+[\d\.\-]+(?:\s+[\d\.\-]+)?\)', at_new, fp_text, count=1)
    return fp_text

content = re.sub(r'\t\(footprint\s+"[^"]+".*?\n\t\)', update_fp, content, flags=re.DOTALL)

with open(pcb_file, "w") as f:
    f.write(content)

print("Applied precision clearance adjustments v5.")
