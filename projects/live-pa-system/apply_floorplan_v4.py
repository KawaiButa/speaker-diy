import re, uuid

pcb_file = "projects/live-pa-system/live-pa-system.kicad_pcb"

with open(pcb_file, "r") as f:
    content = f.read()

BOARD_W = 180.0
BOARD_H = 110.0

# 3-Tier Layout:
# Tier 1 (Top, Y: 10 to 42): Connectors & Input Filters
# Tier 2 (Middle, Y: 46 to 78): ICs, Regulators, Passive Filter networks
# Tier 3 (Bottom, Y: 80 to 106): Pots, Switches, Internal headers & Terminals

placements = {
    # Corner Mounting Holes (M3)
    "H1": (5.0, 5.0, 0),
    "H2": (175.0, 5.0, 0),
    "H3": (175.0, 105.0, 0),
    "H4": (5.0, 105.0, 0),

    # =========================================================================
    # ZONE 1: MIC PREAMP (X: 10 to 52)
    # =========================================================================
    # Tier 1: Input Connector & RF Filter
    "J1":  (22.0, 24.0, 0),    # Neutrik NC3FAH XLR Female (body X: 15 to 38, Y: 15 to 41)
    "C1":  (42.0, 14.0, 0),    # Clear of J1 courtyard
    "R1":  (42.0, 20.0, 0),
    "C2":  (42.0, 26.0, 0),
    "R2":  (42.0, 32.0, 0),
    # Tier 2: Preamp Circuitry
    "C4":  (14.0, 48.0, 0),    # 10uF BP input cap
    "C5":  (24.0, 48.0, 0),    # 10uF BP input cap
    "R3":  (34.0, 46.0, 0),    # 2.2k 0.1%
    "R5":  (34.0, 52.0, 0),    # 2.2k 0.1%
    "R4":  (46.0, 46.0, 0),    # 4.7k 0.1%
    "R6":  (46.0, 52.0, 0),    # 4.7k 0.1%
    "U1":  (28.0, 64.0, 0),    # NE5532P (DIP-8)
    "C3":  (40.0, 64.0, 90),   # 100nF decoupling
    "C6":  (14.0, 76.0, 0),    # 10uF interstage
    "R7":  (24.0, 76.0, 0),    # 47k to Vbias
    "R8":  (36.0, 74.0, 0),    # 330R
    "R10": (36.0, 80.0, 0),    # 1.2k
    # Tier 3: Pots & Controls
    "RV1": (16.0, 92.0, 0),    # Mic Gain Pot
    "C7":  (28.0, 92.0, 0),    # 10uF post-gain
    "RV2": (40.0, 92.0, 0),    # Mic Volume Pot

    # =========================================================================
    # ZONE 2: LINE RECEIVER & COMMON HPF (X: 56 to 104)
    # =========================================================================
    # Tier 1: Combo Input & RF Filter
    "J2":  (74.0, 24.0, 0),    # Neutrik NCJ6FI-H (body X: 65 to 100, Y: 16 to 44)
    "C10": (104.0, 14.0, 0),   # Clear of J2 courtyard
    "R12": (104.0, 20.0, 0),
    "C11": (104.0, 26.0, 0),
    "R13": (104.0, 32.0, 0),
    # Tier 2: Line Receiver & HPF Active Core
    "C12": (58.0, 48.0, 0),    # 1uF film input cap
    "C13": (68.0, 48.0, 0),    # 1uF film input cap
    "R14": (78.0, 46.0, 0),    # 30k 0.1%
    "R15": (78.0, 52.0, 0),    # 30k 0.1%
    "R16": (90.0, 46.0, 0),    # 10k 0.1%
    "R17": (90.0, 52.0, 0),    # 10k 0.1%
    "U2":  (72.0, 64.0, 0),    # NE5532P (Line Rec + HPF)
    "C16": (84.0, 64.0, 90),   # 100nF decoupling
    "C8":  (62.0, 76.0, 0),    # HPF 68nF
    "R9":  (72.0, 74.0, 0),    # HPF 27k
    "C9":  (84.0, 74.0, 0),    # HPF 68nF
    "R11": (72.0, 80.0, 0),    # HPF 56k
    "C15": (56.0, 86.0, 0),    # 10uF post-line
    # Tier 3: Controls & Audio Out
    "RV3": (56.0, 96.0, 0),    # Line Volume Pot
    "SW1": (72.0, 96.0, 0),    # Mode Select DPDT
    "TP1": (82.0, 96.0, 0),    # Mode Status TP
    "C14": (92.0, 88.0, 0),    # 10uF HPF Out
    "R24": (92.0, 96.0, 0),    # 100k bleeder
    "J5":  (104.0, 96.0, 0),   # AMP_AUDIO_IN (3-pin header)

    # =========================================================================
    # ZONE 3: VIRTUAL GROUND GENERATOR (X: 110 to 128)
    # =========================================================================
    "R21": (112.0, 22.0, 0),
    "R22": (112.0, 28.0, 0),
    "C22": (122.0, 25.0, 0),
    "U3":  (116.0, 50.0, 0),
    "C26": (128.0, 50.0, 90),
    "C23": (112.0, 66.0, 0),
    "C25": (122.0, 66.0, 0),

    # =========================================================================
    # ZONE 4: POWER SUPPLY & REGULATION (X: 132 to 175, Y: 6 to 62)
    # =========================================================================
    "J3":  (136.0, 16.0, -90), # DC 36V In (barrel jack)
    "F1":  (154.0, 16.0, 0),   # 5x20 Fuse (body X: 141 to 167)
    "J4":  (130.0, 6.0, 180),  # DC 36V Out terminal to TPA3255
    "Q1":  (136.0, 30.0, 0),   # IRF4905 TO-220
    "D1":  (146.0, 27.0, 0),   # 12V Zener
    "R18": (146.0, 33.0, 0),   # 100k Gate pull-down
    "C17": (166.0, 27.0, 0),   # 470uF 50V Low-ESR
    "C18": (166.0, 36.0, 0),   # 100nF 50V
    "U4":  (136.0, 46.0, 0),   # LM317HVT TO-220
    "D2":  (146.0, 42.0, 0),   # 1N4007 reverse
    "D3":  (146.0, 48.0, 0),   # 1N4007 cadj
    "R19": (160.0, 42.0, 0),   # 240R
    "R20": (160.0, 48.0, 0),   # 2.64k
    "C19": (170.0, 45.0, 0),   # 10uF Cadj
    "C20": (136.0, 58.0, 0),   # 100uF +15V bulk
    "C21": (146.0, 58.0, 0),   # 100nF +15V HF

    # =========================================================================
    # ZONE 5: PASSIVE RLC CONTOUR & SPEAKER (X: 130 to 175, Y: 68 to 105)
    # Strictly isolated from Signal GND & Chassis GND!
    # =========================================================================
    "J6":  (132.0, 72.0, 180), # Speaker In from TPA3255 PBTL
    "L1":  (152.0, 72.0, 0),   # 1.0mH Air Core Inductor (Vishay IHB-3, 28mm dia)
    "SW2": (132.0, 86.0, 0),   # Contour Bypass Slide Switch
    "J7":  (168.0, 84.0, 180), # Speaker Out to Visaton BG 20
    "C24": (146.0, 92.0, 0),   # 4.7uF MKP Capacitor
    "R23": (126.0, 100.0, 0),  # 8.2R 10W Power Resistor
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

print("Applied 3-tier non-colliding layout v4.")
