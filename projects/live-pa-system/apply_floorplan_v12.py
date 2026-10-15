import re

pcb_file = "projects/live-pa-system/live-pa-system.kicad_pcb"

with open(pcb_file, "r") as f:
    content = f.read()

shifts = {
    # C19 near LM317
    "C19": (132.0, 38.0, 0),
    # RLC Zone
    "L1":  (144.0, 70.0, 0),
    "J6":  (126.0, 70.0, 180),
    "SW2": (126.0, 84.0, 0),
    "J7":  (172.0, 88.0, 180),
    "R23": (118.0, 102.0, 0),
    "C24": (154.0, 102.0, 0),
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

print("Applied v12 shifts.")
