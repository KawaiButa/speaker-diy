import re

pcb_file = "projects/live-pa-system/live-pa-system.kicad_pcb"

with open(pcb_file, "r") as f:
    content = f.read()

shifts = {
    # Move C25 and C23 cleanly
    "C25": (112.0, 78.0, 0),
    "C23": (112.0, 70.0, 0),
    # Move L1 and J7
    "L1":  (144.0, 66.0, 0),
    "J7":  (170.0, 84.0, 180),
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

print("Applied v7 shifts.")
