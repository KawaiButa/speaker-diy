import re, math

# Coordinates for 160mm x 100mm floorplan
# Zone 1: Mic Preamp (X: 10 to 45, Y: 10 to 90)
# Zone 2: Line Receiver & HPF (X: 50 to 85, Y: 10 to 90)
# Zone 3: Virtual Ground & Mode Select (X: 90 to 115, Y: 10 to 90)
# Zone 4: Power Supply (+36V In, Reg) (X: 120 to 155, Y: 10 to 55)
# Zone 5: Speaker / RLC Filter (X: 120 to 155, Y: 55 to 90)

placements = {
    # Mounting holes
    "H1": (5.0, 5.0, 0),
    "H2": (155.0, 5.0, 0),
    "H3": (155.0, 95.0, 0),
    "H4": (5.0, 95.0, 0),

    # --- ZONE 1: MIC PREAMP (Far Left) ---
    "J1": (16.0, 20.0, 0),     # XLR female (facing edge)
    "C1": (32.0, 14.0, 0),
    "R1": (32.0, 19.0, 0),
    "C2": (32.0, 25.0, 0),
    "R2": (32.0, 30.0, 0),
    "C4": (14.0, 42.0, 0),     # 10uF BP input cap
    "C5": (22.0, 42.0, 0),     # 10uF BP input cap
    "R3": (32.0, 38.0, 0),     # 2.2k 0.1%
    "R5": (32.0, 44.0, 0),     # 2.2k 0.1%
    "R4": (40.0, 38.0, 0),     # 4.7k 0.1%
    "R6": (40.0, 44.0, 0),     # 4.7k 0.1%
    "U1": (28.0, 56.0, 0),     # NE5532P (DIP-8)
    "C3": (38.0, 56.0, 90),    # 100nF decoupling
    "C6": (16.0, 68.0, 0),     # 10uF interstage
    "R7": (24.0, 68.0, 0),     # 47k
    "R8": (32.0, 68.0, 0),     # 330R
    "R10": (40.0, 68.0, 0),    # 1.2k
    "RV1": (16.0, 82.0, 0),    # Mic Gain Pot
    "C7": (28.0, 82.0, 0),     # 10uF post-gain
    "RV2": (40.0, 82.0, 0),    # Mic Volume Pot

    # --- ZONE 2: LINE RECEIVER & COMMON HPF (Center-Left) ---
    "J2": (60.0, 22.0, 0),     # Combo XLR/TRS Jack
    "C10": (76.0, 14.0, 0),    # RF cap
    "R12": (76.0, 19.0, 0),    # Bleeder
    "C11": (76.0, 25.0, 0),    # RF cap
    "R13": (76.0, 30.0, 0),    # Bleeder
    "C12": (55.0, 42.0, 0),    # 1uF film input cap
    "C13": (65.0, 42.0, 0),    # 1uF film input cap
    "R14": (76.0, 38.0, 0),    # 30k 0.1%
    "R15": (76.0, 44.0, 0),    # 30k 0.1%
    "R16": (84.0, 38.0, 0),    # 10k 0.1%
    "R17": (84.0, 44.0, 0),    # 10k 0.1%
    "U2": (70.0, 56.0, 0),     # NE5532P (Line Rec + HPF)
    "C16": (80.0, 56.0, 90),   # 100nF decoupling
    "C15": (58.0, 68.0, 0),    # 10uF post-line
    "RV3": (58.0, 82.0, 0),    # Line Volume Pot
    "SW1": (74.0, 82.0, 0),    # DPDT Mode Select Switch
    "TP1": (82.0, 82.0, 0),    # Mode status test point
    "C8": (68.0, 68.0, 0),     # HPF 68nF
    "R9": (76.0, 68.0, 0),     # HPF 27k
    "C9": (84.0, 68.0, 0),     # HPF 68nF
    "R11": (92.0, 68.0, 0),    # HPF 56k
    "C14": (74.0, 92.0, 0),    # HPF output 10uF
    "R24": (82.0, 92.0, 0),    # 100k bleeder
    "J5": (92.0, 92.0, 0),     # AMP_AUDIO_IN (3-pin header to TPA3255)

    # --- ZONE 3: VIRTUAL GROUND GENERATOR (Center-Right) ---
    "R21": (96.0, 25.0, 0),    # 10k divider top
    "R22": (96.0, 32.0, 0),    # 10k divider bottom
    "C22": (104.0, 28.0, 0),   # 10uF divider filter
    "U3": (102.0, 50.0, 0),    # NE5532P (Vbias buffer + spare)
    "C26": (112.0, 50.0, 90),  # 100nF decoupling
    "C23": (96.0, 62.0, 0),    # 47uF Vbias bulk
    "C25": (104.0, 62.0, 0),   # 100nF Vbias HF bypass

    # --- ZONE 4: POWER SUPPLY & REGULATION (Top Right) ---
    "J3": (120.0, 15.0, -90),  # DC 36V Barrel Jack
    "F1": (138.0, 15.0, 0),    # 5x20mm Fuseholder
    "Q1": (124.0, 30.0, 0),    # IRF4905 TO-220
    "D1": (134.0, 27.0, 0),    # 12V Zener
    "R18": (134.0, 33.0, 0),   # 100k gate pull-down
    "C17": (148.0, 25.0, 0),   # 470uF 50V Low-ESR
    "C18": (148.0, 35.0, 0),   # 100nF 50V
    "J4": (115.0, 8.0, 180),   # DC 36V terminal to TPA3255
    "U4": (124.0, 45.0, 0),    # LM317HVT TO-220
    "D2": (134.0, 42.0, 0),    # 1N4007 reverse diode
    "D3": (134.0, 48.0, 0),    # 1N4007 cadj diode
    "R19": (142.0, 42.0, 0),   # 240R
    "R20": (142.0, 48.0, 0),   # 2.64k
    "C19": (150.0, 44.0, 0),   # 10uF Cadj
    "C20": (124.0, 58.0, 0),   # 100uF +15V output
    "C21": (132.0, 58.0, 0),   # 100nF +15V HF

    # --- ZONE 5: PASSIVE RLC CONTOUR FILTER & SPEAKER (Bottom Right) ---
    # Isolated from signal GND!
    "J6": (118.0, 75.0, 180),  # Speaker In from TPA3255 PBTL (2-pin terminal)
    "SW2": (118.0, 88.0, 0),   # Contour bypass slide switch
    "L1": (142.0, 75.0, 0),    # 1.0mH air core inductor (28mm dia)
    "C24": (140.0, 92.0, 0),   # 4.7uF MKP capacitor
    "R23": (124.0, 96.0, 0),   # 8.2R 10W power resistor
    "J7": (152.0, 88.0, 180),  # Output to Visaton BG 20 (2-pin terminal)
}

print(f"Total placed components: {len(placements)}")
