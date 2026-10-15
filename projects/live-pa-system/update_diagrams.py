#!/usr/bin/env python3
"""
Regenerate updated perfboard diagrams:
Board B: 5x7 cm (Power Conditioning & +7.5V Virtual Ground Buffer U3)
Board A: 7x9 cm (Audio Front-End: U1 Mic Preamp, U2 Line Rec & HPF)
Board C: 5x7 cm (Passive RLC Contour Filter)
System Wiring Diagram
"""

import os

output_dir = "projects/live-pa-system"
os.makedirs(output_dir, exist_ok=True)
pitch = 28
mx, my = 80, 80

# -------------------------------------------------------------------------
# BOARD B: 5 x 7 cm (Power Conditioning & +7.5V Bias Reference Buffer U3)
# -------------------------------------------------------------------------
cols_b = [chr(65 + i) for i in range(18)] # A to R
rows_b = list(range(1, 25)) # 1 to 24
w_b = mx * 2 + (len(cols_b) - 1) * pitch
h_b = my * 2 + (len(rows_b) - 1) * pitch

def cb(col_str, row_int):
    ci = ord(col_str.upper()) - 65
    ri = row_int - 1
    return mx + ci * pitch, my + ri * pitch

svg_b = []
svg_b.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w_b} {h_b}" width="{w_b}" height="{h_b}">')
svg_b.append('''<defs>
<style>
  .board-bg { fill: #1a2a3a; stroke: #0d1b2a; stroke-width: 4; }
  .grid-lbl { font-family: "Courier New", monospace; font-size: 13px; font-weight: bold; fill: #48cae4; text-anchor: middle; dominant-baseline: middle; }
  .pad-copper { fill: #d4a373; stroke: #b07d4f; stroke-width: 0.5; }
  .pad-hole { fill: #1a2a3a; }
  .mtg-hole { fill: #2b2b2b; stroke: #cccccc; stroke-width: 2; }
  .comp-label { font-family: Arial, sans-serif; font-size: 10.5px; font-weight: bold; fill: #ffffff; text-anchor: middle; dominant-baseline: middle; }
  .sub-label { font-family: Arial, sans-serif; font-size: 8.5px; fill: #e9ecef; text-anchor: middle; dominant-baseline: middle; }
  .val-label { font-family: "Courier New", monospace; font-size: 9px; font-weight: bold; fill: #ffea00; text-anchor: middle; dominant-baseline: middle; }
  .sec-title { font-family: Arial, sans-serif; font-size: 12px; font-weight: bold; fill: #00b4d8; text-anchor: middle; }
</style>
</defs>''')

svg_b.append(f'<rect x="{mx - 30}" y="{my - 30}" width="{(len(cols_b)-1)*pitch + 60}" height="{(len(rows_b)-1)*pitch + 60}" rx="14" class="board-bg"/>')
svg_b.append(f'<text x="{w_b/2}" y="30" font-family="Arial, sans-serif" font-size="16" font-weight="bold" fill="#ffffff" text-anchor="middle">BOARD B: POWER CONDITIONING &amp; BIAS BUFFER (5 × 7 cm PERFBOARD)</text>')
svg_b.append(f'<text x="{w_b/2}" y="50" font-family="Arial, sans-serif" font-size="11" fill="#aaccbb" text-anchor="middle">IRF4905 Reverse Protection | LM317HVT +15V Reg | U3 NE5532P +7.5V Active Buffer</text>')

# Coordinate labels
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

# Section dividers
zx1, _ = cb("G", 1); zx2, _ = cb("H", 1)
svg_b.append(f'<line x1="{(zx1+zx2)/2}" y1="{my - 20}" x2="{(zx1+zx2)/2}" y2="{h_b - my + 20}" stroke="#0077b6" stroke-dasharray="5 3" stroke-width="1.5"/>')
zx3, _ = cb("L", 1); zx4, _ = cb("M", 1)
svg_b.append(f'<line x1="{(zx3+zx4)/2}" y1="{my - 20}" x2="{(zx3+zx4)/2}" y2="{h_b - my + 20}" stroke="#0077b6" stroke-dasharray="5 3" stroke-width="1.5"/>')

svg_b.append(f'<text x="{mx + 2.5*pitch}" y="{my - 22}" class="sec-title">PROTECTION &amp; +36V</text>')
svg_b.append(f'<text x="{mx + 9*pitch}" y="{my - 22}" class="sec-title">+15V REGULATOR</text>')
svg_b.append(f'<text x="{mx + 14.5*pitch}" y="{my - 22}" class="sec-title">+7.5V VBIAS BUFFER</text>')

# Top Terminals
# TB_DC_IN at B2-C2
x1, y1 = cb("B", 2); x2, _ = cb("C", 2)
svg_b.append(f'<rect x="{x1 - 10}" y="{y1 - 12}" width="{pitch + 20}" height="24" fill="#b7094c" stroke="#ff4d6d" stroke-width="2" rx="3"/>')
svg_b.append(f'<text x="{(x1+x2)/2}" y="{y1 - 1}" class="comp-label">DC_IN</text>')
svg_b.append(f'<text x="{(x1+x2)/2}" y="{y1 + 8}" class="sub-label">1:+36V 2:GND</text>')

# TB_AMP_PWR at E2-F2
x1, y1 = cb("E", 2); x2, _ = cb("F", 2)
svg_b.append(f'<rect x="{x1 - 10}" y="{y1 - 12}" width="{pitch + 20}" height="24" fill="#b7094c" stroke="#ff4d6d" stroke-width="2" rx="3"/>')
svg_b.append(f'<text x="{(x1+x2)/2}" y="{y1 - 1}" class="comp-label">AMP_PWR</text>')
svg_b.append(f'<text x="{(x1+x2)/2}" y="{y1 + 8}" class="sub-label">1:+36V 2:GND</text>')

# Q1: IRF4905 TO-220 at B6-D6
xq, yq = cb("C", 6)
svg_b.append(f'<rect x="{xq - pitch - 6}" y="{yq - 14}" width="{2*pitch + 12}" height="24" fill="#333333" stroke="#e0e0e0" stroke-width="1.8" rx="3"/>')
svg_b.append(f'<rect x="{xq - pitch - 4}" y="{yq - 12}" width="{2*pitch + 8}" height="6" fill="#cccccc"/>')
svg_b.append(f'<text x="{xq}" y="{yq + 3}" class="comp-label">Q1: IRF4905</text>')
svg_b.append(f'<text x="{xq}" y="{yq + 18}" class="val-label">1:G(B6) 2:D(C6) 3:S(D6)</text>')

# R18 & D1
x1, y1 = cb("B", 8); x2, y2 = cb("D", 8)
svg_b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#d4a373" stroke-width="2"/>')
svg_b.append(f'<rect x="{(x1+x2)/2 - 8}" y="{y1 - 4}" width="16" height="8" fill="#faedcd" stroke="#bc6c25" rx="2"/>')
svg_b.append(f'<text x="{(x1+x2)/2}" y="{y1 - 7}" font-family="Arial" font-size="8" font-weight="bold" fill="#ffffff" text-anchor="middle">R18: 100k</text>')

x1, y1 = cb("B", 9); x2, y2 = cb("D", 9)
svg_b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#e63946" stroke-width="2"/>')
svg_b.append(f'<rect x="{(x1+x2)/2 - 7}" y="{y1 - 4}" width="14" height="8" fill="#e63946" stroke="#ffb703" rx="2"/>')
svg_b.append(f'<text x="{(x1+x2)/2}" y="{y1 + 10}" font-family="Arial" font-size="8" font-weight="bold" fill="#ffd166" text-anchor="middle">D1: BZX79C12</text>')

# Bulk Caps C17, C18
x_c17, y_c17 = cb("D", 13)
svg_b.append(f'<circle cx="{x_c17}" cy="{y_c17}" r="14" fill="#023e8a" stroke="#48cae4" stroke-width="2"/>')
svg_b.append(f'<text x="{x_c17}" y="{y_c17 - 3}" class="comp-label">C17</text>')
svg_b.append(f'<text x="{x_c17}" y="{y_c17 + 8}" class="val-label">470uF/50V</text>')

x1, y1 = cb("B", 13); x2, y2 = cb("C", 13)
svg_b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#e63946" stroke-width="2"/>')
svg_b.append(f'<rect x="{(x1+x2)/2 - 6}" y="{y1 - 4}" width="12" height="8" fill="#e63946" stroke="#ffb703" rx="2"/>')
svg_b.append(f'<text x="{(x1+x2)/2}" y="{y1 - 7}" font-family="Arial" font-size="8" font-weight="bold" fill="#ffd166" text-anchor="middle">C18: 100nF</text>')

# U4: LM317HVT TO-220 at I10-K10
xu, yu = cb("J", 9)
svg_b.append(f'<rect x="{xu - pitch - 12}" y="{yu - 22}" width="{2*pitch + 24}" height="14" fill="#6c757d" stroke="#adb5bd" stroke-width="1.5" rx="2"/>')
svg_b.append(f'<text x="{xu}" y="{yu - 14}" font-family="Arial" font-size="7.5" fill="#ffffff" text-anchor="middle">HEATSINK (FLOATING TAB!)</text>')
svg_b.append(f'<rect x="{xu - pitch - 6}" y="{yu - 10}" width="{2*pitch + 12}" height="24" fill="#222222" stroke="#e0e0e0" stroke-width="1.8" rx="3"/>')
svg_b.append(f'<text x="{xu}" y="{yu + 3}" class="comp-label">U4: LM317HVT</text>')
svg_b.append(f'<text x="{xu}" y="{yu + 17}" class="val-label">1:ADJ(I) 2:OUT(J) 3:IN(K)</text>')

# D2 Protection Diode across U4
x1, y1 = cb("J", 6); x2, y2 = cb("K", 6)
svg_b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#222222" stroke-width="2.5"/>')
svg_b.append(f'<rect x="{(x1+x2)/2 - 7}" y="{y1 - 4}" width="14" height="8" fill="#222222" stroke="#ffffff" rx="1"/>')
svg_b.append(f'<text x="{(x1+x2)/2}" y="{y1 - 6}" font-family="Arial" font-size="8" font-weight="bold" fill="#ffffff" text-anchor="middle">D2: 1N4007</text>')

# R19 & R20 & C19 & D3
x1, y1 = cb("I", 13); x2, y2 = cb("J", 13)
svg_b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#d4a373" stroke-width="2"/>')
svg_b.append(f'<rect x="{(x1+x2)/2 - 7}" y="{y1 - 4}" width="14" height="8" fill="#faedcd" stroke="#bc6c25" rx="2"/>')
svg_b.append(f'<text x="{(x1+x2)/2}" y="{y1 - 6}" font-family="Arial" font-size="8" font-weight="bold" fill="#ffffff" text-anchor="middle">R19: 240R</text>')

x1, y1 = cb("H", 15); x2, y2 = cb("I", 15)
svg_b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#d4a373" stroke-width="2"/>')
svg_b.append(f'<rect x="{(x1+x2)/2 - 8}" y="{y1 - 4}" width="16" height="8" fill="#faedcd" stroke="#bc6c25" rx="2"/>')
svg_b.append(f'<text x="{(x1+x2)/2}" y="{y1 - 6}" font-family="Arial" font-size="8" font-weight="bold" fill="#ffffff" text-anchor="middle">R20: 2.64k</text>')

x1, y1 = cb("H", 17); x2, y2 = cb("I", 17)
svg_b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#0077b6" stroke-width="2"/>')
svg_b.append(f'<circle cx="{(x1+x2)/2}" cy="{y1}" r="6" fill="#023e8a" stroke="#48cae4" stroke-width="1.2"/>')
svg_b.append(f'<text x="{(x1+x2)/2}" y="{y1 + 10}" font-family="Arial" font-size="8" font-weight="bold" fill="#90e0ef" text-anchor="middle">C19: 10uF</text>')

x1, y1 = cb("H", 13); x2, y2 = cb("I", 13)
svg_b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#222222" stroke-width="2"/>')
svg_b.append(f'<rect x="{(x1+x2)/2 - 7}" y="{y1 - 4}" width="14" height="8" fill="#222222" stroke="#ffffff" rx="1"/>')
svg_b.append(f'<text x="{(x1+x2)/2}" y="{y1 - 6}" font-family="Arial" font-size="8" font-weight="bold" fill="#ffffff" text-anchor="middle">D3: 1N4007</text>')

# Output caps C20, C21
x1, y1 = cb("J", 15); x2, y2 = cb("K", 15)
svg_b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#0077b6" stroke-width="2"/>')
svg_b.append(f'<circle cx="{(x1+x2)/2}" cy="{y1}" r="7" fill="#023e8a" stroke="#48cae4" stroke-width="1.5"/>')
svg_b.append(f'<text x="{(x1+x2)/2}" y="{y1 - 9}" font-family="Arial" font-size="8" font-weight="bold" fill="#90e0ef" text-anchor="middle">C20: 100uF</text>')

x1, y1 = cb("J", 17); x2, y2 = cb("K", 17)
svg_b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#e63946" stroke-width="2"/>')
svg_b.append(f'<rect x="{(x1+x2)/2 - 6}" y="{y1 - 4}" width="12" height="8" fill="#e63946" stroke="#ffb703" rx="2"/>')
svg_b.append(f'<text x="{(x1+x2)/2}" y="{y1 + 10}" font-family="Arial" font-size="8" font-weight="bold" fill="#ffd166" text-anchor="middle">C21: 100nF</text>')

# RIGHT SECTION: +7.5V Virtual Ground (R21, R22, C22, U3, C23, C25, C26)
x1, y1 = cb("N", 5); x2, y2 = cb("P", 5)
svg_b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#d4a373" stroke-width="2"/>')
svg_b.append(f'<rect x="{(x1+x2)/2 - 8}" y="{y1 - 4}" width="16" height="8" fill="#faedcd" stroke="#bc6c25" rx="2"/>')
svg_b.append(f'<text x="{(x1+x2)/2}" y="{y1 - 6}" font-family="Arial" font-size="8" font-weight="bold" fill="#ffffff" text-anchor="middle">R21: 10k 1%</text>')

x1, y1 = cb("N", 7); x2, y2 = cb("P", 7)
svg_b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#d4a373" stroke-width="2"/>')
svg_b.append(f'<rect x="{(x1+x2)/2 - 8}" y="{y1 - 4}" width="16" height="8" fill="#faedcd" stroke="#bc6c25" rx="2"/>')
svg_b.append(f'<text x="{(x1+x2)/2}" y="{y1 - 6}" font-family="Arial" font-size="8" font-weight="bold" fill="#ffffff" text-anchor="middle">R22: 10k 1%</text>')

x1, y1 = cb("N", 9); x2, y2 = cb("P", 9)
svg_b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#0077b6" stroke-width="2"/>')
svg_b.append(f'<circle cx="{(x1+x2)/2}" cy="{y1}" r="6" fill="#023e8a" stroke="#48cae4" stroke-width="1.2"/>')
svg_b.append(f'<text x="{(x1+x2)/2}" y="{y1 + 10}" font-family="Arial" font-size="8" font-weight="bold" fill="#90e0ef" text-anchor="middle">C22: 10uF</text>')

# U3 DIP-8 Socket at N12-Q15
x1, y1 = cb("N", 12); x2, y2 = cb("Q", 15)
bx = min(x1, x2) - 10; by = y1 - 10
bw = abs(x2 - x1) + 20; bh = abs(y2 - y1) + 20
svg_b.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="#1b1b1b" stroke="#e0e0e0" stroke-width="2" rx="4"/>')
svg_b.append(f'<path d="M {bx + bw/2 - 8} {by} A 8 8 0 0 0 {bx + bw/2 + 8} {by}" fill="#1a2a3a" stroke="#e0e0e0" stroke-width="1.5"/>')
svg_b.append(f'<text x="{bx + bw/2}" y="{by + bh/2 - 5}" class="comp-label">U3: NE5532P</text>')
svg_b.append(f'<text x="{bx + bw/2}" y="{by + bh/2 + 7}" class="val-label">VBIAS BUFFER</text>')
for idx in range(4):
    px, py = cb("N", 12 + idx)
    svg_b.append(f'<circle cx="{px}" cy="{py}" r="5" fill="#ffd166" stroke="#333333"/>')
    svg_b.append(f'<text x="{px}" y="{py}" font-family="Arial" font-size="7" font-weight="bold" fill="#000" text-anchor="middle" dominant-baseline="middle">{idx+1}</text>')
    px, py = cb("Q", 12 + idx)
    svg_b.append(f'<circle cx="{px}" cy="{py}" r="5" fill="#ffd166" stroke="#333333"/>')
    svg_b.append(f'<text x="{px}" y="{py}" font-family="Arial" font-size="7" font-weight="bold" fill="#000" text-anchor="middle" dominant-baseline="middle">{8-idx}</text>')

# C26, C23, C25
x1, y1 = cb("N", 17); x2, y2 = cb("Q", 17)
svg_b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#e63946" stroke-width="2"/>')
svg_b.append(f'<rect x="{(x1+x2)/2 - 6}" y="{y1 - 4}" width="12" height="8" fill="#e63946" stroke="#ffb703" rx="2"/>')
svg_b.append(f'<text x="{(x1+x2)/2}" y="{y1 - 6}" font-family="Arial" font-size="8" font-weight="bold" fill="#ffd166" text-anchor="middle">C26: 100nF</text>')

x1, y1 = cb("N", 19); x2, y2 = cb("P", 19)
svg_b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#0077b6" stroke-width="2"/>')
svg_b.append(f'<circle cx="{(x1+x2)/2}" cy="{y1}" r="6.5" fill="#023e8a" stroke="#48cae4" stroke-width="1.2"/>')
svg_b.append(f'<text x="{(x1+x2)/2}" y="{y1 + 10}" font-family="Arial" font-size="8" font-weight="bold" fill="#90e0ef" text-anchor="middle">C23: 47uF</text>')

x1, y1 = cb("N", 21); x2, y2 = cb("P", 21)
svg_b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#e63946" stroke-width="2"/>')
svg_b.append(f'<rect x="{(x1+x2)/2 - 6}" y="{y1 - 4}" width="12" height="8" fill="#e63946" stroke="#ffb703" rx="2"/>')
svg_b.append(f'<text x="{(x1+x2)/2}" y="{y1 - 6}" font-family="Arial" font-size="8" font-weight="bold" fill="#ffd166" text-anchor="middle">C25: 100nF</text>')

# TB_PWR_OUT at N23-Q23 (4-Pin Terminal Block)
x1, y1 = cb("N", 23); x2, _ = cb("Q", 23)
svg_b.append(f'<rect x="{x1 - 10}" y="{y1 - 12}" width="{3*pitch + 20}" height="24" fill="#7209b7" stroke="#b5179e" stroke-width="2" rx="3"/>')
svg_b.append(f'<text x="{(x1+x2)/2}" y="{y1 - 1}" class="comp-label">POWER OUT TO BOARD A</text>')
svg_b.append(f'<text x="{(x1+x2)/2}" y="{y1 + 8}" class="sub-label">1:+15V  2:GND  3:VBIAS(7.5V)  4:SHIELD</text>')

svg_b.append('</svg>')
with open(f"{output_dir}/gate-e-board-b-assembly.svg", "w") as f:
    f.write("\n".join(svg_b))
print("Updated gate-e-board-b-assembly.svg")


# -------------------------------------------------------------------------
# BOARD A: 7 x 9 cm (Audio Analog Front-End: U1 Mic, U2 Line & HPF)
# -------------------------------------------------------------------------
cols_a = [chr(65 + i) for i in range(26)] # A to Z
rows_a = list(range(1, 32)) # 1 to 31
w_a = mx * 2 + (len(cols_a) - 1) * pitch
h_a = my * 2 + (len(rows_a) - 1) * pitch

def ca(col_str, row_int):
    ci = ord(col_str.upper()) - 65
    ri = row_int - 1
    return mx + ci * pitch, my + ri * pitch

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
</style>
</defs>''')

svg_a.append(f'<rect x="{mx - 30}" y="{my - 30}" width="{(len(cols_a)-1)*pitch + 60}" height="{(len(rows_a)-1)*pitch + 60}" rx="14" class="board-bg"/>')
svg_a.append(f'<text x="{w_a/2}" y="32" font-family="Arial, sans-serif" font-size="18" font-weight="bold" fill="#ffffff" text-anchor="middle">BOARD A: AUDIO ANALOG FRONT-END (7 × 9 cm UNIVERSAL PERFBOARD)</text>')
svg_a.append(f'<text x="{w_a/2}" y="52" font-family="Arial, sans-serif" font-size="12" fill="#aaccbb" text-anchor="middle">2.54 mm Pitch (26 Cols A–Z × 31 Rows 1–31) | U1 Mic Preamp (+20..+50dB) | U2 Line Receiver &amp; 60Hz HPF</text>')

# Coordinate headers
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

# Zone divider down the middle (between L and M)
zx1, _ = ca("L", 1); zx2, _ = ca("M", 1)
svg_a.append(f'<line x1="{(zx1+zx2)/2}" y1="{my - 22}" x2="{(zx1+zx2)/2}" y2="{h_a - my + 22}" stroke="#38b000" stroke-dasharray="6 4" stroke-width="2"/>')

svg_a.append(f'<text x="{mx + 5.5*pitch}" y="{my - 22}" class="zone-title">ZONE 1: MIC PREAMP (U1)</text>')
svg_a.append(f'<text x="{mx + 18*pitch}" y="{my - 22}" class="zone-title">ZONE 2: LINE RECEIVER &amp; COMMON 60Hz HPF (U2)</text>')

# Helper functions
def draw_term_block(col_start, col_end, row, label, sublabel, color="#2d6a4f", stroke="#52b788"):
    x1, y = ca(col_start, row)
    x2, _ = ca(col_end, row)
    bx = min(x1, x2) - 12; by = y - 14
    bw = abs(x2 - x1) + 24; bh = 28
    svg_a.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="{color}" stroke="{stroke}" stroke-width="2" rx="4"/>')
    svg_a.append(f'<text x="{bx + bw/2}" y="{by + 10}" class="comp-label">{label}</text>')
    svg_a.append(f'<text x="{bx + bw/2}" y="{by + 21}" class="sub-label">{sublabel}</text>')

def draw_dip8(col_l, col_r, row_start, ref, val):
    x1, y1 = ca(col_l, row_start); x2, y2 = ca(col_r, row_start + 3)
    bx = min(x1, x2) - 10; by = y1 - 10
    bw = abs(x2 - x1) + 20; bh = abs(y2 - y1) + 20
    svg_a.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="#1b1b1b" stroke="#e0e0e0" stroke-width="2" rx="5"/>')
    svg_a.append(f'<path d="M {bx + bw/2 - 8} {by} A 8 8 0 0 0 {bx + bw/2 + 8} {by}" fill="#132a13" stroke="#e0e0e0" stroke-width="1.5"/>')
    svg_a.append(f'<text x="{bx + bw/2}" y="{by + bh/2 - 6}" class="comp-label">{ref} (DIP-8)</text>')
    svg_a.append(f'<text x="{bx + bw/2}" y="{by + bh/2 + 8}" class="val-label">{val}</text>')
    for idx in range(4):
        px, py = ca(col_l, row_start + idx)
        svg_a.append(f'<circle cx="{px}" cy="{py}" r="6" fill="#ffd166" stroke="#333333"/>')
        svg_a.append(f'<text x="{px}" y="{py}" font-family="Arial" font-size="8" font-weight="bold" fill="#000" text-anchor="middle" dominant-baseline="middle">{idx+1}</text>')
        px, py = ca(col_r, row_start + idx)
        svg_a.append(f'<circle cx="{px}" cy="{py}" r="6" fill="#ffd166" stroke="#333333"/>')
        svg_a.append(f'<text x="{px}" y="{py}" font-family="Arial" font-size="8" font-weight="bold" fill="#000" text-anchor="middle" dominant-baseline="middle">{8-idx}</text>')

def draw_res(c1, r1, c2, r2, ref, val):
    x1, y1 = ca(c1, r1); x2, y2 = ca(c2, r2)
    mx_p, my_p = (x1 + x2)/2, (y1 + y2)/2
    svg_a.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#d4a373" stroke-width="2.5"/>')
    if x1 == x2:
        svg_a.append(f'<rect x="{mx_p - 5}" y="{my_p - 10}" width="10" height="20" fill="#faedcd" stroke="#bc6c25" rx="3"/>')
        svg_a.append(f'<text x="{mx_p - 8}" y="{my_p}" font-family="Arial" font-size="8.5" font-weight="bold" fill="#ffffff" text-anchor="end" dominant-baseline="middle">{ref}: {val}</text>')
    else:
        svg_a.append(f'<rect x="{mx_p - 10}" y="{my_p - 5}" width="20" height="10" fill="#faedcd" stroke="#bc6c25" rx="3"/>')
        svg_a.append(f'<text x="{mx_p}" y="{my_p - 8}" font-family="Arial" font-size="8.5" font-weight="bold" fill="#ffffff" text-anchor="middle">{ref}: {val}</text>')

def draw_cap(c1, r1, c2, r2, ref, val, is_elec=False):
    x1, y1 = ca(c1, r1); x2, y2 = ca(c2, r2)
    mx_p, my_p = (x1 + x2)/2, (y1 + y2)/2
    if is_elec:
        svg_a.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#0077b6" stroke-width="2.5"/>')
        svg_a.append(f'<circle cx="{mx_p}" cy="{my_p}" r="7.5" fill="#023e8a" stroke="#48cae4" stroke-width="1.8"/>')
        svg_a.append(f'<text x="{mx_p}" y="{my_p - 10}" font-family="Arial" font-size="8" font-weight="bold" fill="#90e0ef" text-anchor="middle">{ref}: {val}</text>')
    else:
        svg_a.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#e63946" stroke-width="2.5"/>')
        svg_a.append(f'<rect x="{mx_p - 8}" y="{my_p - 5}" width="16" height="10" fill="#e63946" stroke="#ffb703" rx="2"/>')
        svg_a.append(f'<text x="{mx_p}" y="{my_p - 8}" font-family="Arial" font-size="8" font-weight="bold" fill="#ffd166" text-anchor="middle">{ref}: {val}</text>')

def draw_pot_3pin(col_c, row, ref, val, func):
    x, y = ca(col_c, row)
    bw, bh = 2.4 * pitch, 28
    svg_a.append(f'<rect x="{x - bw/2}" y="{y - bh/2}" width="{bw}" height="{bh}" fill="#0077b6" stroke="#90e0ef" stroke-width="1.8" rx="4"/>')
    svg_a.append(f'<circle cx="{x}" cy="{y}" r="5" fill="#ffffff" stroke="#000000"/>')
    svg_a.append(f'<text x="{x}" y="{y - 18}" class="comp-label">{ref}: {val}</text>')
    svg_a.append(f'<text x="{x}" y="{y + 22}" class="val-label">[{func}]</text>')

# Terminal Blocks
draw_term_block("B", "D", 2, "TB_MIC IN", "1:GND  2:HOT(+)  3:COLD(-)")
draw_term_block("N", "P", 2, "TB_LINE IN", "1/S:GND  2/T:HOT  3/R:COLD")
draw_term_block("W", "Y", 2, "TB_PWR IN", "1:+15V  2:GND  3:VBIAS", color="#7209b7", stroke="#b5179e")
draw_term_block("R", "T", 30, "TB_AUDIO OUT", "1:SIG  2:GND  3:SHIELD")

# IC Sockets
draw_dip8("E", "H", 12, "U1", "MIC PREAMP")
draw_dip8("Q", "T", 12, "U2", "LINE & HPF")

# Potentiometers
draw_pot_3pin("C", 27, "RV1", "50k RevLog", "MIC GAIN")
draw_pot_3pin("G", 27, "RV2", "10k Log", "MIC VOL")
draw_pot_3pin("N", 27, "RV3", "10k Log", "LINE VOL")

# SW1 Mode Switch
x_sw, y_sw = ca("U", 27)
svg_a.append(f'<rect x="{x_sw - 28}" y="{y_sw - 16}" width="56" height="32" fill="#4a4e69" stroke="#9a8c98" stroke-width="1.8" rx="4"/>')
svg_a.append(f'<rect x="{x_sw - 8}" y="{y_sw - 12}" width="16" height="24" fill="#f2e9e4" stroke="#222222" rx="2"/>')
svg_a.append(f'<text x="{x_sw}" y="{y_sw - 20}" class="comp-label">SW1 (DPDT)</text>')
svg_a.append(f'<text x="{x_sw}" y="{y_sw + 24}" class="val-label">VOCAL / MONITOR</text>')

# Mic Components
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

# Line Components
draw_cap("N", 4, "O", 4, "C10", "47pF")
draw_cap("N", 5, "O", 5, "C11", "47pF")
draw_res("M", 6, "O", 6, "R12", "100k")
draw_res("M", 7, "O", 7, "R13", "100k")
draw_cap("M", 9, "O", 9, "C12", "1uF Film")
draw_cap("M", 10, "O", 10, "C13", "1uF Film")
draw_res("M", 11, "O", 11, "R14", "30k 0.1%")
draw_res("P", 11, "Q", 11, "R15", "30k 0.1%")
draw_res("P", 13, "R", 13, "R16", "10k 0.1%")
draw_res("P", 14, "R", 14, "R17", "10k 0.1%")
draw_cap("Q", 16, "T", 16, "C16", "100nF")
draw_cap("R", 18, "S", 18, "C15", "10uF", is_elec=True)

# HPF Components
draw_cap("S", 19, "U", 19, "C8", "68nF Film")
draw_cap("S", 20, "U", 20, "C9", "68nF Film")
draw_res("S", 21, "U", 21, "R9", "27k 1%")
draw_res("S", 22, "U", 22, "R11", "56k 1%")
draw_cap("R", 24, "T", 24, "C14", "10uF", is_elec=True)
draw_res("R", 25, "T", 25, "R24", "100k")

# Test Point TP1
x_tp, y_tp = ca("V", 24)
svg_a.append(f'<circle cx="{x_tp}" cy="{y_tp}" r="6" fill="#ffb703" stroke="#ffffff" stroke-width="1.5"/>')
svg_a.append(f'<text x="{x_tp}" y="{y_tp}" font-family="Arial" font-size="7" font-weight="bold" fill="#000000" text-anchor="middle" dominant-baseline="middle">TP1</text>')
svg_a.append(f'<text x="{x_tp + 10}" y="{y_tp}" font-family="Arial" font-size="8" font-weight="bold" fill="#ffb703" text-anchor="start" dominant-baseline="middle">HPF OUT</text>')

svg_a.append('</svg>')
with open(f"{output_dir}/gate-e-board-a-assembly.svg", "w") as f:
    f.write("\n".join(svg_a))
print("Updated gate-e-board-a-assembly.svg")
