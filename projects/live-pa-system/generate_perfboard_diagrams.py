#!/usr/bin/env python3
"""
Generate Scaled Component-Placement and Wiring Diagrams for Universal Prototyping Boards
Board A: 7x9 cm (26 Columns A-Z x 31 Rows 1-31) - Audio Analog Front-End
Board B: 5x7 cm (18 Columns A-R x 24 Rows 1-24) - Power Conditioning (+15V Reg, IRF4905)
Board C: 5x7 cm (18 Columns A-R x 24 Rows 1-24) - Passive RLC Speaker Filter
System Wiring Diagram: Interconnecting Board A, B, C, TPA3255 Amp, PSU, Connectors & BG 20
"""

import os

def generate_svgs():
    output_dir = "projects/live-pa-system"
    os.makedirs(output_dir, exist_ok=True)

    # =========================================================================
    # BOARD A: 7 x 9 cm Audio Analog Front-End
    # =========================================================================
    cols_a = [chr(65 + i) for i in range(26)] # A to Z
    rows_a = list(range(1, 32)) # 1 to 31
    pitch = 28 # pixels per 2.54mm pitch
    mx, my = 80, 80
    w_a = mx * 2 + (len(cols_a) - 1) * pitch
    h_a = my * 2 + (len(rows_a) - 1) * pitch

    svg_a = []
    svg_a.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w_a} {h_a}" width="{w_a}" height="{h_a}">')
    svg_a.append('''<defs>
<style>
  .board-bg { fill: #132a13; stroke: #081c08; stroke-width: 4; }
  .grid-lbl { font-family: "Courier New", monospace; font-size: 13px; font-weight: bold; fill: #70e000; text-anchor: middle; dominant-baseline: middle; }
  .pad-copper { fill: #d4a373; stroke: #b07d4f; stroke-width: 0.5; }
  .pad-hole { fill: #132a13; }
  .mtg-hole { fill: #2b2b2b; stroke: #cccccc; stroke-width: 2; }
  .comp-label { font-family: Arial, sans-serif; font-size: 11px; font-weight: bold; fill: #ffffff; text-anchor: middle; dominant-baseline: middle; }
  .sub-label { font-family: Arial, sans-serif; font-size: 9px; fill: #e9ecef; text-anchor: middle; dominant-baseline: middle; }
  .val-label { font-family: "Courier New", monospace; font-size: 9.5px; font-weight: bold; fill: #ffea00; text-anchor: middle; dominant-baseline: middle; }
  .zone-title { font-family: Arial, sans-serif; font-size: 14px; font-weight: bold; fill: #38b000; text-anchor: middle; }
  .wire-track { stroke-linecap: round; stroke-linejoin: round; fill: none; }
</style>
</defs>''')

    # Background
    svg_a.append(f'<rect x="{mx - 30}" y="{my - 30}" width="{(len(cols_a)-1)*pitch + 60}" height="{(len(rows_a)-1)*pitch + 60}" rx="14" class="board-bg"/>')
    svg_a.append(f'<text x="{w_a/2}" y="32" font-family="Arial, sans-serif" font-size="18" font-weight="bold" fill="#ffffff" text-anchor="middle">BOARD A: AUDIO ANALOG FRONT-END (7 × 9 cm UNIVERSAL PERFBOARD)</text>')
    svg_a.append(f'<text x="{w_a/2}" y="52" font-family="Arial, sans-serif" font-size="12" fill="#aaccbb" text-anchor="middle">Standard 2.54 mm Pitch (26 Columns A–Z × 31 Rows 1–31) | 3× NE5532P DIP-8 Sockets | Isolated Pads</text>')

    def ca(col_str, row_int):
        ci = ord(col_str.upper()) - 65
        ri = row_int - 1
        return mx + ci * pitch, my + ri * pitch

    # Coordinates headers
    for i, col in enumerate(cols_a):
        x = mx + i * pitch
        svg_a.append(f'<text x="{x}" y="{my - 14}" class="grid-lbl">{col}</text>')
        svg_a.append(f'<text x="{x}" y="{h_a - my + 16}" class="grid-lbl">{col}</text>')
    for j, row in enumerate(rows_a):
        y = my + j * pitch
        svg_a.append(f'<text x="{mx - 18}" y="{y}" class="grid-lbl">{row}</text>')
        svg_a.append(f'<text x="{w_a - mx + 18}" y="{y}" class="grid-lbl">{row}</text>')

    # Pads
    for i in range(len(cols_a)):
        for j in range(len(rows_a)):
            x = mx + i * pitch
            y = my + j * pitch
            if (i in (0, len(cols_a)-1)) and (j in (0, len(rows_a)-1)):
                svg_a.append(f'<circle cx="{x}" cy="{y}" r="8" class="mtg-hole"/>')
                svg_a.append(f'<circle cx="{x}" cy="{y}" r="4.5" fill="#132a13"/>')
            else:
                svg_a.append(f'<circle cx="{x}" cy="{y}" r="4.5" class="pad-copper"/>')
                svg_a.append(f'<circle cx="{x}" cy="{y}" r="1.8" class="pad-hole"/>')

    # Zone dividers
    zx1, _ = ca("I", 1); zx2, _ = ca("J", 1)
    svg_a.append(f'<line x1="{(zx1+zx2)/2}" y1="{my - 22}" x2="{(zx1+zx2)/2}" y2="{h_a - my + 22}" stroke="#38b000" stroke-dasharray="6 4" stroke-width="1.8"/>')
    zx3, _ = ca("R", 1); zx4, _ = ca("S", 1)
    svg_a.append(f'<line x1="{(zx3+zx4)/2}" y1="{my - 22}" x2="{(zx3+zx4)/2}" y2="{h_a - my + 22}" stroke="#38b000" stroke-dasharray="6 4" stroke-width="1.8"/>')

    # Zone Headings
    svg_a.append(f'<text x="{mx + 3.8*pitch}" y="{my - 22}" class="zone-title">ZONE 1: MIC PREAMP</text>')
    svg_a.append(f'<text x="{mx + 13.5*pitch}" y="{my - 22}" class="zone-title">ZONE 2: LINE &amp; 60Hz HPF</text>')
    svg_a.append(f'<text x="{mx + 22*pitch}" y="{my - 22}" class="zone-title">ZONE 3: VBIAS (+7.5V)</text>')

    # Terminal block drawing helper
    def draw_term_block(col_start, col_end, row, label, sublabel, color="#2d6a4f", stroke="#52b788"):
        x1, y = ca(col_start, row)
        x2, _ = ca(col_end, row)
        bx = min(x1, x2) - 12
        by = y - 14
        bw = abs(x2 - x1) + 24
        bh = 28
        svg_a.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="{color}" stroke="{stroke}" stroke-width="2" rx="4"/>')
        svg_a.append(f'<text x="{bx + bw/2}" y="{by + 10}" class="comp-label">{label}</text>')
        svg_a.append(f'<text x="{bx + bw/2}" y="{by + 21}" class="sub-label">{sublabel}</text>')

    # Top terminals
    draw_term_block("B", "D", 2, "TB_MIC IN", "1:GND  2:HOT(+)  3:COLD(-)")
    draw_term_block("M", "O", 2, "TB_LINE IN", "1/S:GND  2/T:HOT  3/R:COLD")
    draw_term_block("W", "Y", 2, "TB_PWR IN", "1:+15V  2:GND  3:VBIAS", color="#7209b7", stroke="#b5179e")

    # Bottom terminals
    draw_term_block("N", "P", 30, "TB_AUDIO OUT", "1:SIG  2:GND  3:SHIELD")

    # DIP-8 Socket drawing helper
    def draw_dip8_sock(col_l, col_r, row_start, ref, val):
        x1, y1 = ca(col_l, row_start)
        x2, y2 = ca(col_r, row_start + 3)
        bx = min(x1, x2) - 10
        by = y1 - 10
        bw = abs(x2 - x1) + 20
        bh = abs(y2 - y1) + 20
        svg_a.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="#1b1b1b" stroke="#e0e0e0" stroke-width="2" rx="5"/>')
        # Notch at top
        svg_a.append(f'<path d="M {bx + bw/2 - 8} {by} A 8 8 0 0 0 {bx + bw/2 + 8} {by}" fill="#132a13" stroke="#e0e0e0" stroke-width="1.5"/>')
        svg_a.append(f'<text x="{bx + bw/2}" y="{by + bh/2 - 6}" class="comp-label">{ref} (DIP-8)</text>')
        svg_a.append(f'<text x="{bx + bw/2}" y="{by + bh/2 + 8}" class="val-label">{val}</text>')
        # Pin circles & numbers
        for idx in range(4):
            # Left pins 1-4
            px, py = ca(col_l, row_start + idx)
            svg_a.append(f'<circle cx="{px}" cy="{py}" r="6" fill="#ffd166" stroke="#333333" stroke-width="1"/>')
            svg_a.append(f'<text x="{px}" y="{py}" font-family="Arial" font-size="8" font-weight="bold" fill="#000000" text-anchor="middle" dominant-baseline="middle">{idx+1}</text>')
            # Right pins 8-5
            px, py = ca(col_r, row_start + idx)
            svg_a.append(f'<circle cx="{px}" cy="{py}" r="6" fill="#ffd166" stroke="#333333" stroke-width="1"/>')
            svg_a.append(f'<text x="{px}" y="{py}" font-family="Arial" font-size="8" font-weight="bold" fill="#000000" text-anchor="middle" dominant-baseline="middle">{8-idx}</text>')

    draw_dip8_sock("E", "H", 12, "U1", "NE5532P")
    draw_dip8_sock("M", "P", 12, "U2", "NE5532P")
    draw_dip8_sock("V", "Y", 12, "U3", "NE5532P")

    # Potentiometers
    def draw_pot_3pin(col_c, row, ref, val, func):
        x, y = ca(col_c, row)
        bw, bh = 2.4 * pitch, 28
        svg_a.append(f'<rect x="{x - bw/2}" y="{y - bh/2}" width="{bw}" height="{bh}" fill="#0077b6" stroke="#90e0ef" stroke-width="1.8" rx="4"/>')
        svg_a.append(f'<circle cx="{x}" cy="{y}" r="5" fill="#ffffff" stroke="#000000"/>')
        svg_a.append(f'<text x="{x}" y="{y - 18}" class="comp-label">{ref}: {val}</text>')
        svg_a.append(f'<text x="{x}" y="{y + 22}" class="val-label">[{func}]</text>')

    draw_pot_3pin("C", 27, "RV1", "50k RevLog", "MIC GAIN")
    draw_pot_3pin("G", 27, "RV2", "10k Log", "MIC VOL")
    draw_pot_3pin("L", 27, "RV3", "10k Log", "LINE VOL")

    # Switch SW1 (Mode Select)
    x_sw, y_sw = ca("Q", 27)
    svg_a.append(f'<rect x="{x_sw - 28}" y="{y_sw - 16}" width="56" height="32" fill="#4a4e69" stroke="#9a8c98" stroke-width="1.8" rx="4"/>')
    svg_a.append(f'<rect x="{x_sw - 8}" y="{y_sw - 12}" width="16" height="24" fill="#f2e9e4" stroke="#222222" rx="2"/>')
    svg_a.append(f'<text x="{x_sw}" y="{y_sw - 20}" class="comp-label">SW1 (DPDT)</text>')
    svg_a.append(f'<text x="{x_sw}" y="{y_sw + 24}" class="val-label">VOCAL / MONITOR</text>')

    # Resistor drawer
    def draw_res(c1, r1, c2, r2, ref, val):
        x1, y1 = ca(c1, r1); x2, y2 = ca(c2, r2)
        mx_p, my_p = (x1 + x2)/2, (y1 + y2)/2
        svg_a.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#d4a373" stroke-width="2.5"/>')
        if x1 == x2: # vertical
            svg_a.append(f'<rect x="{mx_p - 5}" y="{my_p - 10}" width="10" height="20" fill="#faedcd" stroke="#bc6c25" stroke-width="1.2" rx="3"/>')
            svg_a.append(f'<text x="{mx_p + 10}" y="{my_p}" font-family="Arial" font-size="8.5" font-weight="bold" fill="#ffffff" text-anchor="start" dominant-baseline="middle">{ref}: {val}</text>')
        else: # horizontal
            svg_a.append(f'<rect x="{mx_p - 10}" y="{my_p - 5}" width="20" height="10" fill="#faedcd" stroke="#bc6c25" stroke-width="1.2" rx="3"/>')
            svg_a.append(f'<text x="{mx_p}" y="{my_p - 8}" font-family="Arial" font-size="8.5" font-weight="bold" fill="#ffffff" text-anchor="middle">{ref}: {val}</text>')

    # Capacitor drawer
    def draw_cap(c1, r1, c2, r2, ref, val, is_elec=False):
        x1, y1 = ca(c1, r1); x2, y2 = ca(c2, r2)
        mx_p, my_p = (x1 + x2)/2, (y1 + y2)/2
        svg_a.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#48cae4" stroke-width="2.2"/>')
        if is_elec:
            svg_a.append(f'<circle cx="{mx_p}" cy="{my_p}" r="8" fill="#023e8a" stroke="#48cae4" stroke-width="1.5"/>')
            svg_a.append(f'<line x1="{mx_p - 4}" y1="{my_p}" x2="{mx_p + 4}" y2="{my_p}" stroke="#ffffff" stroke-width="1.2"/>')
            svg_a.append(f'<line x1="{mx_p}" y1="{my_p - 4}" x2="{mx_p}" y2="{my_p + 4}" stroke="#ffffff" stroke-width="1.2"/>')
            svg_a.append(f'<text x="{mx_p + 11}" y="{my_p}" font-family="Arial" font-size="8.5" font-weight="bold" fill="#90e0ef" text-anchor="start" dominant-baseline="middle">{ref}: {val}</text>')
        else:
            svg_a.append(f'<rect x="{mx_p - 8}" y="{my_p - 5}" width="16" height="10" fill="#e63946" stroke="#ffb703" stroke-width="1.2" rx="2"/>')
            svg_a.append(f'<text x="{mx_p}" y="{my_p + 10}" font-family="Arial" font-size="8.5" font-weight="bold" fill="#ffd166" text-anchor="middle">{ref}: {val}</text>')

    # Zone 1 Components
    draw_cap("C", 4, "D", 4, "C1", "47pF")
    draw_cap("C", 5, "D", 5, "C2", "47pF")
    draw_res("B", 6, "D", 6, "R1", "100k")
    draw_res("B", 7, "D", 7, "R2", "100k")
    draw_cap("B", 9, "D", 9, "C4", "10uF BP", is_elec=True)
    draw_cap("B", 10, "D", 10, "C5", "10uF BP", is_elec=True)
    draw_res("B", 11, "D", 11, "R3", "2.2k 0.1%")
    draw_res("F", 11, "G", 11, "R4", "4.7k 0.1%")
    draw_res("B", 13, "D", 13, "R5", "2.2k 0.1%")
    draw_res("B", 14, "D", 14, "R6", "4.7k 0.1%")
    draw_cap("E", 16, "H", 16, "C3", "100nF")
    draw_cap("E", 18, "F", 18, "C6", "10uF", is_elec=True)
    draw_res("F", 19, "G", 19, "R10", "1.2k")
    draw_res("F", 20, "G", 20, "R8", "330R")
    draw_res("F", 21, "G", 21, "R7", "47k")
    draw_cap("G", 23, "H", 23, "C7", "10uF", is_elec=True)

    # Zone 2 Components
    draw_cap("L", 4, "M", 4, "C10", "47pF")
    draw_cap("L", 5, "M", 5, "C11", "47pF")
    draw_res("K", 6, "M", 6, "R12", "100k")
    draw_res("K", 7, "M", 7, "R13", "100k")
    draw_cap("K", 9, "M", 9, "C12", "1uF Film")
    draw_cap("K", 10, "M", 10, "C13", "1uF Film")
    draw_res("K", 11, "M", 11, "R14", "30k 0.1%")
    draw_res("O", 11, "P", 11, "R15", "30k 0.1%")
    draw_res("K", 13, "M", 13, "R16", "10k 0.1%")
    draw_res("K", 14, "M", 14, "R17", "10k 0.1%")
    draw_cap("M", 16, "P", 16, "C16", "100nF")
    draw_cap("N", 18, "O", 18, "C15", "10uF", is_elec=True)
    draw_cap("O", 19, "Q", 19, "C8", "68nF Film")
    draw_cap("O", 20, "Q", 20, "C9", "68nF Film")
    draw_res("O", 21, "Q", 21, "R9", "27k 1%")
    draw_res("O", 22, "Q", 22, "R11", "56k 1%")
    draw_cap("N", 24, "P", 24, "C14", "10uF", is_elec=True)
    draw_res("N", 25, "P", 25, "R24", "100k")

    # Test point TP1
    x_tp, y_tp = ca("R", 24)
    svg_a.append(f'<circle cx="{x_tp}" cy="{y_tp}" r="6" fill="#ffb703" stroke="#ffffff" stroke-width="1.5"/>')
    svg_a.append(f'<text x="{x_tp}" y="{y_tp}" font-family="Arial" font-size="7" font-weight="bold" fill="#000000" text-anchor="middle" dominant-baseline="middle">TP1</text>')
    svg_a.append(f'<text x="{x_tp + 10}" y="{y_tp}" font-family="Arial" font-size="8" font-weight="bold" fill="#ffb703" text-anchor="start" dominant-baseline="middle">HPF OUT</text>')

    # Zone 3 Components
    draw_res("U", 6, "W", 6, "R21", "10k 1%")
    draw_res("U", 8, "W", 8, "R22", "10k 1%")
    draw_cap("U", 10, "W", 10, "C22", "10uF", is_elec=True)
    draw_cap("V", 16, "Y", 16, "C26", "100nF")
    draw_cap("V", 19, "X", 19, "C23", "47uF", is_elec=True)
    draw_cap("V", 21, "X", 21, "C25", "100nF")

    svg_a.append('</svg>')
    with open(f"{output_dir}/gate-e-board-a-assembly.svg", "w") as f:
        f.write("\n".join(svg_a))
    print("Generated gate-e-board-a-assembly.svg")


    # =========================================================================
    # BOARD B: 5 x 7 cm Low-Voltage Power Conditioning
    # =========================================================================
    cols_b = [chr(65 + i) for i in range(18)] # A to R
    rows_b = list(range(1, 25)) # 1 to 24
    w_b = mx * 2 + (len(cols_b) - 1) * pitch
    h_b = my * 2 + (len(rows_b) - 1) * pitch

    svg_b = []
    svg_b.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w_b} {h_b}" width="{w_b}" height="{h_b}">')
    svg_b.append('''<defs>
<style>
  .board-bg { fill: #1a2a3a; stroke: #0d1b2a; stroke-width: 4; }
  .grid-lbl { font-family: "Courier New", monospace; font-size: 13px; font-weight: bold; fill: #48cae4; text-anchor: middle; dominant-baseline: middle; }
  .pad-copper { fill: #d4a373; stroke: #b07d4f; stroke-width: 0.5; }
  .pad-hole { fill: #1a2a3a; }
  .mtg-hole { fill: #2b2b2b; stroke: #cccccc; stroke-width: 2; }
  .comp-label { font-family: Arial, sans-serif; font-size: 11px; font-weight: bold; fill: #ffffff; text-anchor: middle; dominant-baseline: middle; }
  .sub-label { font-family: Arial, sans-serif; font-size: 9px; fill: #e9ecef; text-anchor: middle; dominant-baseline: middle; }
  .val-label { font-family: "Courier New", monospace; font-size: 9.5px; font-weight: bold; fill: #ffea00; text-anchor: middle; dominant-baseline: middle; }
</style>
</defs>''')

    svg_b.append(f'<rect x="{mx - 30}" y="{my - 30}" width="{(len(cols_b)-1)*pitch + 60}" height="{(len(rows_b)-1)*pitch + 60}" rx="14" class="board-bg"/>')
    svg_b.append(f'<text x="{w_b/2}" y="32" font-family="Arial, sans-serif" font-size="17" font-weight="bold" fill="#ffffff" text-anchor="middle">BOARD B: POWER CONDITIONING &amp; +15V REG (5 × 7 cm PERFBOARD)</text>')
    svg_b.append(f'<text x="{w_b/2}" y="52" font-family="Arial, sans-serif" font-size="11.5" fill="#aaccbb" text-anchor="middle">IRF4905 Reverse Polarity P-FET | LM317HVT Linear Regulator | High-Current Direct Wiring</text>')

    def cb(col_str, row_int):
        ci = ord(col_str.upper()) - 65
        ri = row_int - 1
        return mx + ci * pitch, my + ri * pitch

    # Coordinates
    for i, col in enumerate(cols_b):
        x = mx + i * pitch
        svg_b.append(f'<text x="{x}" y="{my - 14}" class="grid-lbl">{col}</text>')
        svg_b.append(f'<text x="{x}" y="{h_b - my + 16}" class="grid-lbl">{col}</text>')
    for j, row in enumerate(rows_b):
        y = my + j * pitch
        svg_b.append(f'<text x="{mx - 18}" y="{y}" class="grid-lbl">{row}</text>')
        svg_b.append(f'<text x="{w_b - mx + 18}" y="{y}" class="grid-lbl">{row}</text>')

    # Pads
    for i in range(len(cols_b)):
        for j in range(len(rows_b)):
            x = mx + i * pitch
            y = my + j * pitch
            if (i in (0, len(cols_b)-1)) and (j in (0, len(rows_b)-1)):
                svg_b.append(f'<circle cx="{x}" cy="{y}" r="8" class="mtg-hole"/>')
                svg_b.append(f'<circle cx="{x}" cy="{y}" r="4.5" fill="#1a2a3a"/>')
            else:
                svg_b.append(f'<circle cx="{x}" cy="{y}" r="4.5" class="pad-copper"/>')
                svg_b.append(f'<circle cx="{x}" cy="{y}" r="1.8" class="pad-hole"/>')

    # Top Terminal Blocks
    # TB_DC_IN at B2-C2
    x1, y1 = cb("B", 2); x2, _ = cb("C", 2)
    svg_b.append(f'<rect x="{x1 - 10}" y="{y1 - 12}" width="{pitch + 20}" height="24" fill="#b7094c" stroke="#ff4d6d" stroke-width="2" rx="3"/>')
    svg_b.append(f'<text x="{(x1+x2)/2}" y="{y1 - 1}" class="comp-label">DC_IN</text>')
    svg_b.append(f'<text x="{(x1+x2)/2}" y="{y1 + 8}" class="sub-label">1:+36V 2:GND</text>')

    # TB_AMP_PWR at F2-G2
    x1, y1 = cb("F", 2); x2, _ = cb("G", 2)
    svg_b.append(f'<rect x="{x1 - 10}" y="{y1 - 12}" width="{pitch + 20}" height="24" fill="#b7094c" stroke="#ff4d6d" stroke-width="2" rx="3"/>')
    svg_b.append(f'<text x="{(x1+x2)/2}" y="{y1 - 1}" class="comp-label">TO AMP</text>')
    svg_b.append(f'<text x="{(x1+x2)/2}" y="{y1 + 8}" class="sub-label">1:+36V 2:GND</text>')

    # Q1: IRF4905 TO-220
    xq, yq = cb("C", 6)
    svg_b.append(f'<rect x="{xq - pitch - 6}" y="{yq - 14}" width="{2*pitch + 12}" height="24" fill="#333333" stroke="#e0e0e0" stroke-width="1.8" rx="3"/>')
    svg_b.append(f'<rect x="{xq - pitch - 4}" y="{yq - 12}" width="{2*pitch + 8}" height="6" fill="#cccccc"/>') # Tab
    svg_b.append(f'<text x="{xq}" y="{yq + 3}" class="comp-label">Q1: IRF4905 (P-FET)</text>')
    svg_b.append(f'<text x="{xq}" y="{yq + 18}" class="val-label">1:G(B6) 2:D(C6) 3:S(D6)</text>')

    # R18 & D1 around Q1
    x1, y1 = cb("B", 8); x2, y2 = cb("D", 8)
    svg_b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#d4a373" stroke-width="2"/>')
    svg_b.append(f'<rect x="{(x1+x2)/2 - 8}" y="{y1 - 4}" width="16" height="8" fill="#faedcd" stroke="#bc6c25" rx="2"/>')
    svg_b.append(f'<text x="{(x1+x2)/2}" y="{y1 - 7}" font-family="Arial" font-size="8" font-weight="bold" fill="#ffffff" text-anchor="middle">R18: 100k</text>')

    x1, y1 = cb("B", 9); x2, y2 = cb("D", 9)
    svg_b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#e63946" stroke-width="2"/>')
    svg_b.append(f'<rect x="{(x1+x2)/2 - 7}" y="{y1 - 4}" width="14" height="8" fill="#e63946" stroke="#ffb703" rx="2"/>')
    svg_b.append(f'<text x="{(x1+x2)/2}" y="{y1 + 10}" font-family="Arial" font-size="8" font-weight="bold" fill="#ffd166" text-anchor="middle">D1: BZX79C12 (12V)</text>')

    # Bulk Caps C17, C18
    x_c17, y_c17 = cb("D", 12)
    svg_b.append(f'<circle cx="{x_c17}" cy="{y_c17}" r="14" fill="#023e8a" stroke="#48cae4" stroke-width="2"/>')
    svg_b.append(f'<text x="{x_c17}" y="{y_c17 - 3}" class="comp-label">C17</text>')
    svg_b.append(f'<text x="{x_c17}" y="{y_c17 + 8}" class="val-label">470uF/50V</text>')

    x1, y1 = cb("B", 12); x2, y2 = cb("C", 12)
    svg_b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#e63946" stroke-width="2"/>')
    svg_b.append(f'<rect x="{(x1+x2)/2 - 6}" y="{y1 - 4}" width="12" height="8" fill="#e63946" stroke="#ffb703" rx="2"/>')
    svg_b.append(f'<text x="{(x1+x2)/2}" y="{y1 - 7}" font-family="Arial" font-size="8" font-weight="bold" fill="#ffd166" text-anchor="middle">C18: 100nF</text>')

    # U4: LM317HVT TO-220
    xu, yu = cb("L", 10)
    # Heatsink
    svg_b.append(f'<rect x="{xu - pitch - 12}" y="{yu - 22}" width="{2*pitch + 24}" height="14" fill="#6c757d" stroke="#adb5bd" stroke-width="1.5" rx="2"/>')
    svg_b.append(f'<text x="{xu}" y="{yu - 14}" font-family="Arial" font-size="8" fill="#ffffff" text-anchor="middle">ALUMINUM HEATSINK (&lt;=20 C/W)</text>')
    svg_b.append(f'<rect x="{xu - pitch - 6}" y="{yu - 10}" width="{2*pitch + 12}" height="24" fill="#222222" stroke="#e0e0e0" stroke-width="1.8" rx="3"/>')
    svg_b.append(f'<text x="{xu}" y="{yu + 3}" class="comp-label">U4: LM317HVT</text>')
    svg_b.append(f'<text x="{xu}" y="{yu + 18}" class="val-label">1:ADJ(K10) 2:VOUT(L10) 3:VIN(M10)</text>')
    svg_b.append(f'<text x="{xu}" y="{yu + 28}" font-family="Arial" font-size="7.5" font-weight="bold" fill="#ff4d6d" text-anchor="middle">TAB = +15V (NOT GND!)</text>')

    # D2 Protection Diode across U4
    x1, y1 = cb("L", 7); x2, y2 = cb("M", 7)
    svg_b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#222222" stroke-width="2.5"/>')
    svg_b.append(f'<rect x="{(x1+x2)/2 - 7}" y="{y1 - 4}" width="14" height="8" fill="#222222" stroke="#ffffff" rx="1"/>')
    svg_b.append(f'<text x="{(x1+x2)/2}" y="{y1 - 6}" font-family="Arial" font-size="8" font-weight="bold" fill="#ffffff" text-anchor="middle">D2: 1N4007</text>')

    # R19 & R20 & C19 & D3
    x1, y1 = cb("K", 14); x2, y2 = cb("L", 14)
    svg_b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#d4a373" stroke-width="2"/>')
    svg_b.append(f'<rect x="{(x1+x2)/2 - 7}" y="{y1 - 4}" width="14" height="8" fill="#faedcd" stroke="#bc6c25" rx="2"/>')
    svg_b.append(f'<text x="{(x1+x2)/2}" y="{y1 - 6}" font-family="Arial" font-size="8" font-weight="bold" fill="#ffffff" text-anchor="middle">R19: 240R</text>')

    x1, y1 = cb("I", 16); x2, y2 = cb("K", 16)
    svg_b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#d4a373" stroke-width="2"/>')
    svg_b.append(f'<rect x="{(x1+x2)/2 - 8}" y="{y1 - 4}" width="16" height="8" fill="#faedcd" stroke="#bc6c25" rx="2"/>')
    svg_b.append(f'<text x="{(x1+x2)/2}" y="{y1 - 6}" font-family="Arial" font-size="8" font-weight="bold" fill="#ffffff" text-anchor="middle">R20: 2.64k</text>')

    x1, y1 = cb("I", 18); x2, y2 = cb("K", 18)
    svg_b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#0077b6" stroke-width="2"/>')
    svg_b.append(f'<circle cx="{(x1+x2)/2}" cy="{y1}" r="6" fill="#023e8a" stroke="#48cae4" stroke-width="1.2"/>')
    svg_b.append(f'<text x="{(x1+x2)/2}" y="{y1 + 10}" font-family="Arial" font-size="8" font-weight="bold" fill="#90e0ef" text-anchor="middle">C19: 10uF</text>')

    # D3
    x1, y1 = cb("I", 14); x2, y2 = cb("K", 14)
    svg_b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#222222" stroke-width="2"/>')
    svg_b.append(f'<rect x="{(x1+x2)/2 - 7}" y="{y1 - 4}" width="14" height="8" fill="#222222" stroke="#ffffff" rx="1"/>')
    svg_b.append(f'<text x="{(x1+x2)/2}" y="{y1 - 6}" font-family="Arial" font-size="8" font-weight="bold" fill="#ffffff" text-anchor="middle">D3: 1N4007</text>')

    # Output caps C20, C21
    x1, y1 = cb("N", 16); x2, y2 = cb("P", 16)
    svg_b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#0077b6" stroke-width="2"/>')
    svg_b.append(f'<circle cx="{(x1+x2)/2}" cy="{y1}" r="7" fill="#023e8a" stroke="#48cae4" stroke-width="1.5"/>')
    svg_b.append(f'<text x="{(x1+x2)/2}" y="{y1 - 9}" font-family="Arial" font-size="8" font-weight="bold" fill="#90e0ef" text-anchor="middle">C20: 100uF</text>')

    x1, y1 = cb("N", 18); x2, y2 = cb("P", 18)
    svg_b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#e63946" stroke-width="2"/>')
    svg_b.append(f'<rect x="{(x1+x2)/2 - 6}" y="{y1 - 4}" width="12" height="8" fill="#e63946" stroke="#ffb703" rx="2"/>')
    svg_b.append(f'<text x="{(x1+x2)/2}" y="{y1 + 10}" font-family="Arial" font-size="8" font-weight="bold" fill="#ffd166" text-anchor="middle">C21: 100nF</text>')

    # TB_PWR_OUT at N22-P22
    x1, y1 = cb("N", 22); x2, _ = cb("P", 22)
    svg_b.append(f'<rect x="{x1 - 10}" y="{y1 - 12}" width="{2*pitch + 20}" height="24" fill="#7209b7" stroke="#b5179e" stroke-width="2" rx="3"/>')
    svg_b.append(f'<text x="{(x1+x2)/2}" y="{y1 - 1}" class="comp-label">TO BOARD A</text>')
    svg_b.append(f'<text x="{(x1+x2)/2}" y="{y1 + 8}" class="sub-label">1:+15V  2:GND  3:SHIELD</text>')

    svg_b.append('</svg>')
    with open(f"{output_dir}/gate-e-board-b-assembly.svg", "w") as f:
        f.write("\n".join(svg_b))
    print("Generated gate-e-board-b-assembly.svg")


    # =========================================================================
    # BOARD C: 5 x 7 cm Passive RLC Contour Filter Board
    # =========================================================================
    svg_c = []
    svg_c.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w_b} {h_b}" width="{w_b}" height="{h_b}">')
    svg_c.append('''<defs>
<style>
  .board-bg { fill: #2c1919; stroke: #190c0c; stroke-width: 4; }
  .grid-lbl { font-family: "Courier New", monospace; font-size: 13px; font-weight: bold; fill: #ff9e00; text-anchor: middle; dominant-baseline: middle; }
  .pad-copper { fill: #d4a373; stroke: #b07d4f; stroke-width: 0.5; }
  .pad-hole { fill: #2c1919; }
  .mtg-hole { fill: #2b2b2b; stroke: #cccccc; stroke-width: 2; }
  .comp-label { font-family: Arial, sans-serif; font-size: 11px; font-weight: bold; fill: #ffffff; text-anchor: middle; dominant-baseline: middle; }
  .sub-label { font-family: Arial, sans-serif; font-size: 9px; fill: #e9ecef; text-anchor: middle; dominant-baseline: middle; }
  .val-label { font-family: "Courier New", monospace; font-size: 10px; font-weight: bold; fill: #ffea00; text-anchor: middle; dominant-baseline: middle; }
</style>
</defs>''')

    svg_c.append(f'<rect x="{mx - 30}" y="{my - 30}" width="{(len(cols_b)-1)*pitch + 60}" height="{(len(rows_b)-1)*pitch + 60}" rx="14" class="board-bg"/>')
    svg_c.append(f'<text x="{w_b/2}" y="32" font-family="Arial, sans-serif" font-size="17" font-weight="bold" fill="#ffffff" text-anchor="middle">BOARD C: PASSIVE RLC CONTOUR FILTER (5 × 7 cm PERFBOARD)</text>')
    svg_c.append(f'<text x="{w_b/2}" y="52" font-family="Arial, sans-serif" font-size="11.5" fill="#f4a261" text-anchor="middle">Floating PBTL Class-D Audio Drive (18 AWG Wire) | Strictly Isolated from GND</text>')

    # Coordinates
    for i, col in enumerate(cols_b):
        x = mx + i * pitch
        svg_c.append(f'<text x="{x}" y="{my - 14}" class="grid-lbl">{col}</text>')
        svg_c.append(f'<text x="{x}" y="{h_b - my + 16}" class="grid-lbl">{col}</text>')
    for j, row in enumerate(rows_b):
        y = my + j * pitch
        svg_c.append(f'<text x="{mx - 18}" y="{y}" class="grid-lbl">{row}</text>')
        svg_c.append(f'<text x="{w_b - mx + 18}" y="{y}" class="grid-lbl">{row}</text>')

    # Pads
    for i in range(len(cols_b)):
        for j in range(len(rows_b)):
            x = mx + i * pitch
            y = my + j * pitch
            if (i in (0, len(cols_b)-1)) and (j in (0, len(rows_b)-1)):
                svg_c.append(f'<circle cx="{x}" cy="{y}" r="8" class="mtg-hole"/>')
                svg_c.append(f'<circle cx="{x}" cy="{y}" r="4.5" fill="#2c1919"/>')
            else:
                svg_c.append(f'<circle cx="{x}" cy="{y}" r="4.5" class="pad-copper"/>')
                svg_c.append(f'<circle cx="{x}" cy="{y}" r="1.8" class="pad-hole"/>')

    # Terminals
    # TB_SPK_IN at B2-C2
    x1, y1 = cb("B", 2); x2, _ = cb("C", 2)
    svg_c.append(f'<rect x="{x1 - 10}" y="{y1 - 12}" width="{pitch + 20}" height="24" fill="#d90429" stroke="#ef233c" stroke-width="2" rx="3"/>')
    svg_c.append(f'<text x="{(x1+x2)/2}" y="{y1 - 1}" class="comp-label">AMP PBTL IN</text>')
    svg_c.append(f'<text x="{(x1+x2)/2}" y="{y1 + 8}" class="sub-label">1:(+) 2:(-)</text>')

    # SW2 Contour Bypass Switch at B8-C8
    x_sw2, y_sw2 = cb("B", 8)
    svg_c.append(f'<rect x="{x_sw2 - 12}" y="{y_sw2 - 14}" width="34" height="28" fill="#4a4e69" stroke="#9a8c98" stroke-width="1.8" rx="3"/>')
    svg_c.append(f'<rect x="{x_sw2 - 4}" y="{y_sw2 - 10}" width="8" height="20" fill="#f2e9e4" rx="2"/>')
    svg_c.append(f'<text x="{x_sw2 + 25}" y="{y_sw2 - 4}" font-family="Arial" font-size="9" font-weight="bold" fill="#ffffff" text-anchor="start">SW2 (SPST)</text>')
    svg_c.append(f'<text x="{x_sw2 + 25}" y="{y_sw2 + 8}" font-family="Arial" font-size="8" fill="#ffb703" text-anchor="start">RLC ON / BYPASS</text>')

    # L1: 1.0mH Air Core Choke (Large circle in center)
    x_l1, y_l1 = cb("K", 11)
    svg_c.append(f'<circle cx="{x_l1}" cy="{y_l1}" r="38" fill="#582f0e" stroke="#ddb892" stroke-width="3"/>')
    svg_c.append(f'<circle cx="{x_l1}" cy="{y_l1}" r="12" fill="#2c1919" stroke="#ddb892" stroke-width="1.5"/>')
    svg_c.append(f'<text x="{x_l1}" y="{y_l1 - 4}" class="comp-label">L1: 1.0 mH</text>')
    svg_c.append(f'<text x="{x_l1}" y="{y_l1 + 8}" class="val-label">AIR CORE (0.35R)</text>')
    # Zip-tie holes
    x_zt1, y_zt1 = cb("I", 11); x_zt2, y_zt2 = cb("M", 11)
    svg_c.append(f'<line x1="{x_zt1}" y1="{y_zt1-35}" x2="{x_zt1}" y2="{y_zt1+35}" stroke="#ffffff" stroke-width="3" stroke-dasharray="8 4" opacity="0.6"/>')
    svg_c.append(f'<text x="{x_l1}" y="{y_l1 + 26}" font-family="Arial" font-size="7.5" fill="#e9ecef" text-anchor="middle">NYLON ZIP-TIE MOUNT</text>')

    # C24: 4.7uF/250V MKP Film Capacitor
    x1, y1 = cb("E", 17); x2, y2 = cb("I", 17)
    svg_c.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#e63946" stroke-width="3"/>')
    svg_c.append(f'<rect x="{(x1+x2)/2 - 24}" y="{y1 - 10}" width="48" height="20" fill="#e63946" stroke="#ffb703" stroke-width="1.8" rx="3"/>')
    svg_c.append(f'<text x="{(x1+x2)/2}" y="{y1 - 1}" class="comp-label">C24: 4.7 uF / 250V</text>')
    svg_c.append(f'<text x="{(x1+x2)/2}" y="{y1 + 8}" class="val-label">MKP AUDIO FILM</text>')

    # R23: 8.2 Ohm / 10W Power Resistor (Ceramic / Wirewound)
    x1, y1 = cb("E", 21); x2, y2 = cb("M", 21)
    svg_c.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#e9ecef" stroke-width="3.5"/>')
    svg_c.append(f'<rect x="{(x1+x2)/2 - 36}" y="{y1 - 10}" width="72" height="20" fill="#f8f9fa" stroke="#495057" stroke-width="2" rx="3"/>')
    svg_c.append(f'<text x="{(x1+x2)/2}" y="{y1 - 1}" font-family="Arial" font-size="10" font-weight="bold" fill="#212529" text-anchor="middle">R23: 8.2 Ω / 10W</text>')
    svg_c.append(f'<text x="{(x1+x2)/2}" y="{y1 + 8}" font-family="Arial" font-size="8" font-weight="bold" fill="#495057" text-anchor="middle">NON-INDUCTIVE POWER RESISTOR</text>')

    # TB_SPK_OUT at B23-C23
    x1, y1 = cb("B", 23); x2, _ = cb("C", 23)
    svg_c.append(f'<rect x="{x1 - 10}" y="{y1 - 12}" width="{pitch + 20}" height="24" fill="#d90429" stroke="#ef233c" stroke-width="2" rx="3"/>')
    svg_c.append(f'<text x="{(x1+x2)/2}" y="{y1 - 1}" class="comp-label">TO BG 20</text>')
    svg_c.append(f'<text x="{(x1+x2)/2}" y="{y1 + 8}" class="sub-label">1:(+) 2:(-)</text>')

    # Floating Bus Warning
    svg_c.append(f'<rect x="{mx + 5}" y="{h_b - my - 16}" width="{w_b - 2*mx - 10}" height="28" fill="#5c0000" stroke="#ff4d6d" stroke-width="1.5" rx="3"/>')
    svg_c.append(f'<text x="{w_b/2}" y="{h_b - my - 5}" font-family="Arial" font-size="9" font-weight="bold" fill="#ffffff" text-anchor="middle">WARNING: BOTH SPEAKER RAILS FLOAT AT +18V DC HALF-SUPPLY</text>')
    svg_c.append(f'<text x="{w_b/2}" y="{h_b - my + 6}" font-family="Arial" font-size="8" fill="#ffd166" text-anchor="middle">NEVER CONNECT EITHER TERMINAL TO CHASSIS OR SIGNAL GROUND!</text>')

    svg_c.append('</svg>')
    with open(f"{output_dir}/gate-e-board-c-assembly.svg", "w") as f:
        f.write("\n".join(svg_c))
    print("Generated gate-e-board-c-assembly.svg")


    # =========================================================================
    # SYSTEM WIRING DIAGRAM: Interconnection Architecture
    # =========================================================================
    sw_w, sw_h = 1100, 750
    svg_s = []
    svg_s.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {sw_w} {sw_h}" width="{sw_w}" height="{sw_h}">')
    svg_s.append('''<defs>
<style>
  .sys-bg { fill: #0b0f19; }
  .blk-bg { fill: #1a2238; stroke: #4cc9f0; stroke-width: 2; rx: 8; }
  .blk-hdr { font-family: Arial, sans-serif; font-size: 14px; font-weight: bold; fill: #4cc9f0; }
  .blk-desc { font-family: Arial, sans-serif; font-size: 10px; fill: #e0e1dd; }
  .term-box { fill: #2b2d42; stroke: #8d99ae; stroke-width: 1.2; rx: 3; }
  .term-txt { font-family: "Courier New", monospace; font-size: 9.5px; fill: #ffffff; }
  .wire-hi-pwr { stroke: #e63946; stroke-width: 4; fill: none; stroke-linecap: round; }
  .wire-hi-gnd { stroke: #000000; stroke-width: 4; fill: none; stroke-linecap: round; }
  .wire-spk-pos { stroke: #f77f00; stroke-width: 3.5; fill: none; stroke-linecap: round; }
  .wire-spk-neg { stroke: #0077b6; stroke-width: 3.5; fill: none; stroke-linecap: round; }
  .wire-sig { stroke: #2a9d8f; stroke-width: 2.5; fill: none; stroke-linecap: round; }
  .wire-vbias { stroke: #7209b7; stroke-width: 2; fill: none; stroke-linecap: round; }
</style>
</defs>''')

    svg_s.append(f'<rect width="{sw_w}" height="{sw_h}" class="sys-bg"/>')
    svg_s.append(f'<text x="{sw_w/2}" y="32" font-family="Arial, sans-serif" font-size="20" font-weight="bold" fill="#ffffff" text-anchor="middle">DIY ACTIVE STAGE MONITOR — GATE E COMPLETE SYSTEM WIRING</text>')
    svg_s.append(f'<text x="{sw_w/2}" y="52" font-family="Arial, sans-serif" font-size="12" fill="#aaccbb" text-anchor="middle">Point-to-Point Cable Interconnect: External PSU, Board A, Board B, Board C, TPA3255 Amp &amp; Visaton BG 20</text>')

    # Block 1: External PSU & Panel Power
    svg_s.append('<rect x="40" y="80" width="180" height="140" class="blk-bg"/>')
    svg_s.append('<text x="55" y="105" class="blk-hdr">DC POWER INPUT</text>')
    svg_s.append('<text x="55" y="125" class="blk-desc">External 36V 5A Adapter</text>')
    svg_s.append('<text x="55" y="145" class="blk-desc">J3: 5.5x2.1mm DC Jack</text>')
    svg_s.append('<text x="55" y="165" class="blk-desc">F1: 5x20mm 3.15A Fuse</text>')
    svg_s.append('<text x="55" y="195" class="blk-desc" fill="#f77f00">18 AWG Heavy Wire</text>')

    # Block 2: Board B (Power Conditioning)
    svg_s.append('<rect x="280" y="80" width="220" height="200" class="blk-bg"/>')
    svg_s.append('<text x="295" y="105" class="blk-hdr">BOARD B (5 × 7 cm)</text>')
    svg_s.append('<text x="295" y="125" class="blk-desc">Power Conditioning</text>')
    svg_s.append('<text x="295" y="145" class="blk-desc">• IRF4905 Reverse Protection</text>')
    svg_s.append('<text x="295" y="165" class="blk-desc">• LM317HVT +15V Regulator</text>')
    svg_s.append('<text x="295" y="185" class="blk-desc">• 470uF Reservoir / 100uF Out</text>')
    svg_s.append('<text x="295" y="215" class="blk-desc" fill="#7209b7">Outputs: +15V, GND, +36V</text>')

    # Block 3: TPA3255 Amplifier Module
    svg_s.append('<rect x="580" y="80" width="230" height="200" class="blk-bg"/>')
    svg_s.append('<text x="595" y="105" class="blk-hdr">TPA3255 AMPLIFIER</text>')
    svg_s.append('<text x="595" y="125" class="blk-desc">Wuzhi ZK-3002 PBTL Mono</text>')
    svg_s.append('<text x="595" y="145" class="blk-desc">• 36V DC Power Terminal</text>')
    svg_s.append('<text x="595" y="165" class="blk-desc">• 3-Pin Single-Ended Audio In</text>')
    svg_s.append('<text x="595" y="185" class="blk-desc">• Floating PBTL Speaker Out</text>')
    svg_s.append('<text x="595" y="215" class="blk-desc" fill="#ff4d6d">Half-Supply +18V DC Offset</text>')

    # Block 4: Board A (Analog Front-End)
    svg_s.append('<rect x="280" y="340" width="340" height="260" class="blk-bg"/>')
    svg_s.append('<text x="295" y="365" class="blk-hdr">BOARD A: ANALOG AUDIO (7 × 9 cm)</text>')
    svg_s.append('<text x="295" y="385" class="blk-desc">3x NE5532P High-Performance Audio Op-Amps</text>')
    svg_s.append('<text x="295" y="410" class="blk-desc">• U1: Mic Preamp (+20 to +54 dB Gain)</text>')
    svg_s.append('<text x="295" y="430" class="blk-desc">• U2A: Balanced LINE Diff Receiver (0 dB)</text>')
    svg_s.append('<text x="295" y="450" class="blk-desc">• SW1: Mode Switch (Vocal / Console)</text>')
    svg_s.append('<text x="295" y="470" class="blk-desc">• U2B: 60Hz 2nd-Order Sallen-Key HPF</text>')
    svg_s.append('<text x="295" y="490" class="blk-desc">• U3A: Virtual Ground Follower (+7.5V)</text>')
    svg_s.append('<text x="295" y="520" class="blk-desc" fill="#2a9d8f">Controls: RV1 (Gain), RV2 (MicVol), RV3 (LineVol)</text>')

    # Block 5: Inputs (Mic & Line)
    svg_s.append('<rect x="40" y="340" width="180" height="260" class="blk-bg"/>')
    svg_s.append('<text x="55" y="365" class="blk-hdr">PANEL INPUTS</text>')
    svg_s.append('<text x="55" y="395" class="blk-desc">J1: Neutrik NC3FD XLR-F</text>')
    svg_s.append('<text x="55" y="415" class="blk-desc">Pin 1: GND / Shield</text>')
    svg_s.append('<text x="55" y="430" class="blk-desc">Pin 2: HOT (+)</text>')
    svg_s.append('<text x="55" y="445" class="blk-desc">Pin 3: COLD (-)</text>')
    svg_s.append('<text x="55" y="480" class="blk-desc">J2: Neutrik NCJ6FI Combo</text>')
    svg_s.append('<text x="55" y="500" class="blk-desc">XLR / 6.35mm TRS</text>')
    svg_s.append('<text x="55" y="515" class="blk-desc">Tied 1/S: GND, 2/T: HOT</text>')
    svg_s.append('<text x="55" y="530" class="blk-desc">3/R: COLD (-)</text>')

    # Block 6: Board C (RLC Filter)
    svg_s.append('<rect x="870" y="80" width="190" height="240" class="blk-bg"/>')
    svg_s.append('<text x="885" y="105" class="blk-hdr">BOARD C (5 × 7 cm)</text>')
    svg_s.append('<text x="885" y="125" class="blk-desc">Passive RLC Contour</text>')
    svg_s.append('<text x="885" y="150" class="blk-desc">• L1: 1.0 mH Air Choke</text>')
    svg_s.append('<text x="885" y="170" class="blk-desc">• R23: 8.2 Ω 10W Resistor</text>')
    svg_s.append('<text x="885" y="190" class="blk-desc">• C24: 4.7 uF MKP Cap</text>')
    svg_s.append('<text x="885" y="210" class="blk-desc">• SW2: Bypass Switch</text>')
    svg_s.append('<text x="885" y="240" class="blk-desc" fill="#f77f00">18 AWG Speaker Tracks</text>')

    # Block 7: Visaton BG 20
    svg_s.append('<rect x="870" y="380" width="190" height="150" class="blk-bg"/>')
    svg_s.append('<text x="885" y="405" class="blk-hdr">VISATON BG 20</text>')
    svg_s.append('<text x="885" y="425" class="blk-desc">8" Full-Range (8 Ω)</text>')
    svg_s.append('<text x="885" y="445" class="blk-desc">25 L Vented Stage Wedge</text>')
    svg_s.append('<text x="885" y="465" class="blk-desc">10 W RMS Operating Limit</text>')
    svg_s.append('<text x="885" y="495" class="blk-desc" fill="#e63946">Peak Current: 3.6 A</text>')

    # WIRES & CONNECTIONS
    # 1. Power DC: PSU -> Board B
    svg_s.append('<path d="M 220 120 L 280 120" class="wire-hi-pwr"/>')
    svg_s.append('<path d="M 220 150 L 280 150" class="wire-hi-gnd"/>')

    # 2. Power DC: Board B -> TPA3255
    svg_s.append('<path d="M 500 120 L 580 120" class="wire-hi-pwr"/>')
    svg_s.append('<path d="M 500 150 L 580 150" class="wire-hi-gnd"/>')

    # 3. Regulated Power: Board B -> Board A (+15V, GND)
    svg_s.append('<path d="M 390 280 L 390 340" class="wire-hi-pwr" stroke-width="2.5"/>')
    svg_s.append('<path d="M 410 280 L 410 340" class="wire-hi-gnd" stroke-width="2.5"/>')

    # 4. Audio Inputs: Panel -> Board A
    svg_s.append('<path d="M 220 420 L 280 420" class="wire-sig"/>')
    svg_s.append('<path d="M 220 510 L 280 510" class="wire-sig"/>')

    # 5. Audio Output: Board A -> TPA3255
    svg_s.append('<path d="M 620 440 L 700 440 L 700 280" class="wire-sig"/>')

    # 6. Speaker Out: TPA3255 -> Board C
    svg_s.append('<path d="M 810 140 L 870 140" class="wire-spk-pos"/>')
    svg_s.append('<path d="M 810 170 L 870 170" class="wire-spk-neg"/>')

    # 7. Filter Out: Board C -> Visaton BG 20
    svg_s.append('<path d="M 940 320 L 940 380" class="wire-spk-pos"/>')
    svg_s.append('<path d="M 980 320 L 980 380" class="wire-spk-neg"/>')

    # Legend at bottom
    svg_s.append('<rect x="40" y="640" width="1020" height="70" fill="#141b2d" stroke="#3a405a" rx="6"/>')
    svg_s.append('<text x="60" y="665" font-family="Arial" font-size="11" font-weight="bold" fill="#ffffff">WIRING COLOR CODE &amp; WIRE SPECIFICATIONS:</text>')
    
    # Legend items
    svg_s.append('<line x1="60" y1="685" x2="90" y2="685" class="wire-hi-pwr"/>')
    svg_s.append('<text x="100" y="688" font-family="Arial" font-size="10" fill="#ffffff">+36V High-Current (18 AWG Red Silicone)</text>')

    svg_s.append('<line x1="330" y1="685" x2="360" y2="685" class="wire-hi-gnd"/>')
    svg_s.append('<text x="370" y="688" font-family="Arial" font-size="10" fill="#ffffff">DC Power Ground Return (18 AWG Black Silicone)</text>')

    svg_s.append('<line x1="650" y1="685" x2="680" y2="685" class="wire-spk-pos"/>')
    svg_s.append('<text x="690" y="688" font-family="Arial" font-size="10" fill="#ffffff">PBTL Speaker (+) (18 AWG Orange/Red - FLOATING)</text>')

    svg_s.append('<line x1="60" y1="702" x2="90" y2="702" class="wire-sig"/>')
    svg_s.append('<text x="100" y="705" font-family="Arial" font-size="10" fill="#ffffff">Analog Audio Signals (Shielded Twisted Pair / 24 AWG)</text>')

    svg_s.append('<line x1="330" y1="702" x2="360" y2="702" class="wire-spk-neg"/>')
    svg_s.append('<text x="370" y="705" font-family="Arial" font-size="10" fill="#ffffff">PBTL Speaker (-) (18 AWG Blue - FLOATING)</text>')

    svg_s.append('<line x1="650" y1="702" x2="680" y2="702" class="wire-vbias"/>')
    svg_s.append('<text x="690" y="705" font-family="Arial" font-size="10" fill="#ffffff">+15V &amp; Virtual Ground (24 AWG Hookup Wire)</text>')

    svg_s.append('</svg>')
    with open(f"{output_dir}/gate-e-system-wiring-diagram.svg", "w") as f:
        f.write("\n".join(svg_s))
    print("Generated gate-e-system-wiring-diagram.svg")

if __name__ == "__main__":
    generate_svgs()
    print("All prototyping SVG diagrams generated successfully.")
