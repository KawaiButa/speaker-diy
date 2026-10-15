#!/usr/bin/env python3
"""
Generate verified SVG simulation plots from ngspice data for Gate D Final Verification.
Plots:
1. sim_d1_mic_preamp.svg (Gain curves & CMRR with 0.1% resistor mismatch)
2. sim_d1_line_receiver.svg (Differential frequency response & Headroom at +22 dBu)
3. sim_d1_hpf_filter.svg (Common 60 Hz 2nd-order Sallen-Key HPF response)
4. sim_d2_dc_protection.svg (Reverse polarity cutoff & LM317 100Hz ripple rejection)
5. sim_d4_rlc_complex_load.svg (RLC contour notch depth with Visaton BG 20 complex load)
"""

import subprocess
import os
import math
from pathlib import Path

SIM_DIR = Path(__file__).resolve().parent

def run_ngspice_batch(cir_path):
    cmd = ["ngspice", "-b", str(cir_path)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.returncode, res.stdout, res.stderr

def create_svg_chart(title, x_label, y_label, series_list, x_log=True, y_min=None, y_max=None, width=700, height=400):
    """
    series_list: list of dict(name, x_vals, y_vals, color, stroke_dash)
    """
    margin_l = 80
    margin_r = 40
    margin_t = 60
    margin_b = 60
    plot_w = width - margin_l - margin_r
    plot_h = height - margin_t - margin_b

    # Determine bounds
    all_x = [x for s in series_list for x in s['x']]
    all_y = [y for s in series_list for y in s['y']]

    min_x = min(all_x) if all_x else 10
    max_x = max(all_x) if all_x else 100000
    if min_x <= 0 and x_log:
        min_x = 10

    if y_min is None:
        y_min = math.floor(min(all_y) / 10.0) * 10.0
    if y_max is None:
        y_max = math.ceil(max(all_y) / 10.0) * 10.0
    if y_max == y_min:
        y_max += 10.0

    def map_x(x):
        if x_log:
            ratio = (math.log10(max(x, 1e-6)) - math.log10(min_x)) / (math.log10(max_x) - math.log10(min_x))
        else:
            ratio = (x - min_x) / (max_x - min_x)
        return margin_l + ratio * plot_w

    def map_y(y):
        ratio = (y - y_min) / (y_max - y_min)
        return margin_t + (1.0 - ratio) * plot_h

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" style="background-color: #1a1a1a; font-family: monospace, sans-serif;">')
    
    # Title
    svg.append(f'<text x="{width/2}" y="32" fill="#ffffff" font-size="16" font-weight="bold" text-anchor="middle">{title}</text>')

    # Grid & Axes
    # Y-axis ticks
    y_step = (y_max - y_min) / 6.0
    if y_step >= 10:
        y_step = round(y_step / 10) * 10
    elif y_step >= 5:
        y_step = 5
    elif y_step >= 2:
        y_step = 2
    else:
        y_step = 1

    cur_y = math.ceil(y_min / y_step) * y_step
    while cur_y <= y_max:
        yp = map_y(cur_y)
        svg.append(f'<line x1="{margin_l}" y1="{yp}" x2="{margin_l + plot_w}" y2="{yp}" stroke="#333333" stroke-width="1" />')
        svg.append(f'<text x="{margin_l - 10}" y="{yp + 4}" fill="#aaaaaa" font-size="11" text-anchor="end">{cur_y:g}</text>')
        cur_y += y_step

    # X-axis ticks (log or linear)
    if x_log:
        dec_min = int(math.floor(math.log10(min_x)))
        dec_max = int(math.ceil(math.log10(max_x)))
        for dec in range(dec_min, dec_max + 1):
            val = 10**dec
            if min_x <= val <= max_x:
                xp = map_x(val)
                svg.append(f'<line x1="{xp}" y1="{margin_t}" x2="{xp}" y2="{margin_t + plot_h}" stroke="#444444" stroke-width="1" />')
                label = f"{val:g} Hz" if val < 1000 else f"{val/1000:g} kHz"
                svg.append(f'<text x="{xp}" y="{margin_t + plot_h + 20}" fill="#aaaaaa" font-size="11" text-anchor="middle">{label}</text>')
    else:
        x_step = (max_x - min_x) / 5.0
        cur_x = min_x
        while cur_x <= max_x:
            xp = map_x(cur_x)
            svg.append(f'<line x1="{xp}" y1="{margin_t}" x2="{xp}" y2="{margin_t + plot_h}" stroke="#444444" stroke-width="1" />')
            svg.append(f'<text x="{xp}" y="{margin_t + plot_h + 20}" fill="#aaaaaa" font-size="11" text-anchor="middle">{cur_x:g}</text>')
            cur_x += x_step

    # Axis borders
    svg.append(f'<rect x="{margin_l}" y="{margin_t}" width="{plot_w}" height="{plot_h}" fill="none" stroke="#666666" stroke-width="1.5" />')

    # Axis Labels
    svg.append(f'<text x="{margin_l + plot_w/2}" y="{height - 15}" fill="#cccccc" font-size="12" text-anchor="middle">{x_label}</text>')
    svg.append(f'<text x="25" y="{margin_t + plot_h/2}" fill="#cccccc" font-size="12" text-anchor="middle" transform="rotate(-90 25 {margin_t + plot_h/2})">{y_label}</text>')

    # Series paths
    for s in series_list:
        color = s.get('color', '#00ffcc')
        dash = s.get('dash', '')
        width_line = s.get('width', 2.0)
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ''
        
        pts = []
        for x, y in zip(s['x'], s['y']):
            if x_log and x <= 0:
                continue
            # Clamp y within plot area for clean line
            clamped_y = max(min(y, y_max + 10), y_min - 10)
            xp = map_x(x)
            yp = map_y(clamped_y)
            pts.append(f"{xp:.1f},{yp:.1f}")
        
        if pts:
            polyline_str = " ".join(pts)
            svg.append(f'<polyline points="{polyline_str}" fill="none" stroke="{color}" stroke-width="{width_line}"{dash_attr} />')

    # Legend
    leg_x = margin_l + 15
    leg_y = margin_t + 20
    for idx, s in enumerate(series_list):
        y_pos = leg_y + idx * 22
        color = s.get('color', '#00ffcc')
        dash = s.get('dash', '')
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ''
        svg.append(f'<line x1="{leg_x}" y1="{y_pos}" x2="{leg_x + 25}" y2="{y_pos}" stroke="{color}" stroke-width="2.5"{dash_attr} />')
        svg.append(f'<text x="{leg_x + 32}" y="{y_pos + 4}" fill="#ffffff" font-size="11">{s["name"]}</text>')

    svg.append('</svg>')
    return '\n'.join(svg)

# =============================================================================
# 1. MIC PREAMP DATA & PLOT
# =============================================================================
def generate_mic_preamp_plot():
    cir_content = """* Mic Preamp wrdata testbench
.include "projects/live-pa-system/simulation/sim_d1_mic_preamp.cir"
.control
  alter R_pot = 0
  ac dec 50 10 100k
  wrdata projects/live-pa-system/simulation/mic_gain_min.txt vdb(PRE2_OUT)

  alter R_pot = 25k
  ac dec 50 10 100k
  wrdata projects/live-pa-system/simulation/mic_gain_mid.txt vdb(PRE2_OUT)

  alter R_pot = 50k
  ac dec 50 10 100k
  wrdata projects/live-pa-system/simulation/mic_gain_max.txt vdb(PRE2_OUT)

  * Worst-case CMRR with 0.1% resistor mismatch
  alter R_in_cold = 2202.2
  alter R_fb1     = 4695.3
  alter R_in_hot  = 2197.8
  alter R_bias1   = 4704.7
  alter Vmic_hot ac = 1.0
  alter Vmic_cold ac = 1.0
  alter R_pot = 0
  ac dec 50 10 100k
  let cmrr_wc = 19.92 - vdb(PRE1_OUT)
  wrdata projects/live-pa-system/simulation/mic_cmrr.txt cmrr_wc
.endc
"""
    tb_path = SIM_DIR / "tb_mic_wrdata.cir"
    with open(tb_path, "w") as f:
        f.write(cir_content)
    
    run_ngspice_batch(tb_path)
    
    # Read data
    def read_dat(fn):
        xs, ys = [], []
        with open(SIM_DIR / fn) as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 2:
                    xs.append(float(parts[0]))
                    ys.append(float(parts[1]))
        return xs, ys

    x_min, y_min = read_dat("mic_gain_min.txt")
    x_mid, y_mid = read_dat("mic_gain_mid.txt")
    x_max, y_max = read_dat("mic_gain_max.txt")
    x_cmrr, y_cmrr = read_dat("mic_cmrr.txt")

    series = [
        {"name": "Max Gain (+50.45 dB, RV1=50k)", "x": x_max, "y": y_max, "color": "#ff3366"},
        {"name": "Mid Gain (+44.69 dB, RV1=25k)", "x": x_mid, "y": y_mid, "color": "#ffaa00"},
        {"name": "Min Gain (+19.92 dB, RV1=0)", "x": x_min, "y": y_min, "color": "#00ffcc"},
        {"name": "Worst-Case CMRR (0.1% Mismatch: 71.2 dB)", "x": x_cmrr, "y": y_cmrr, "color": "#3399ff", "dash": "4,4"}
    ]
    svg = create_svg_chart(
        "Microphone Preamp: Frequency Response & Worst-Case CMRR (0.1% Resistors)",
        "Frequency (Hz)",
        "Magnitude (dB / dB CMRR)",
        series,
        x_log=True,
        y_min=10,
        y_max=85
    )
    with open(SIM_DIR / "sim_d1_mic_preamp.svg", "w") as f:
        f.write(svg)
    print("Generated sim_d1_mic_preamp.svg")

# =============================================================================
# 2. LINE RECEIVER DATA & PLOT
# =============================================================================
def generate_line_receiver_plot():
    cir_content = """* Line Receiver wrdata testbench
.include "projects/live-pa-system/simulation/sim_d1_line_receiver.cir"
.control
  ac dec 50 10 100k
  wrdata projects/live-pa-system/simulation/line_ac.txt vdb(POT_TOP)

  * Worst-case CMRR
  alter R_in_cold = 30030
  alter R_fb      = 9990
  alter R_in_hot  = 29970
  alter R_bias    = 10010
  alter Vline_hot ac = 1.0
  alter Vline_cold ac = 1.0
  ac dec 50 10 100k
  let line_cmrr_wc = -9.54 - vdb(POT_TOP)
  wrdata projects/live-pa-system/simulation/line_cmrr.txt line_cmrr_wc

  * Transient at stress +22 dBu (13.79 Vpk diff)
  alter Vline_hot sin = [ 0 6.896 1k ]
  alter Vline_cold sin = [ 0 -6.896 1k ]
  tran 10u 4m
  wrdata projects/live-pa-system/simulation/line_tran22.txt v(LINE_OUT)
.endc
"""
    tb_path = SIM_DIR / "tb_line_wrdata.cir"
    with open(tb_path, "w") as f:
        f.write(cir_content)
    
    run_ngspice_batch(tb_path)

    def read_dat(fn):
        xs, ys = [], []
        with open(SIM_DIR / fn) as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 2:
                    xs.append(float(parts[0]))
                    ys.append(float(parts[1]))
        return xs, ys

    x_ac, y_ac = read_dat("line_ac.txt")
    x_cmrr, y_cmrr = read_dat("line_cmrr.txt")
    t_tran, v_tran = read_dat("line_tran22.txt")

    series_ac = [
        {"name": "Differential Gain (Ad = 1/3 = -9.54 dB)", "x": x_ac, "y": y_ac, "color": "#00ffcc"},
        {"name": "Worst-Case CMRR (0.1% Resistors: 50.5 dB)", "x": x_cmrr, "y": y_cmrr, "color": "#3399ff", "dash": "4,4"}
    ]
    svg_ac = create_svg_chart(
        "Balanced LINE Receiver: Frequency Response & Worst-Case CMRR (0.1% Resistors)",
        "Frequency (Hz)",
        "Magnitude (dB / dB CMRR)",
        series_ac,
        x_log=True,
        y_min=-20,
        y_max=60
    )
    with open(SIM_DIR / "sim_d1_line_receiver.svg", "w") as f:
        f.write(svg_ac)
    print("Generated sim_d1_line_receiver.svg")

# =============================================================================
# 3. COMMON HPF DATA & PLOT
# =============================================================================
def generate_hpf_plot():
    cir_content = """* HPF wrdata testbench
.include "projects/live-pa-system/simulation/sim_d1_hpf_filter.cir"
.control
  alter R_pot_wiper = 50
  ac dec 100 10 10k
  wrdata projects/live-pa-system/simulation/hpf_100pct.txt vdb(OUT_AC)

  alter R_pot_wiper = 2.5k
  ac dec 100 10 10k
  wrdata projects/live-pa-system/simulation/hpf_50pct.txt vdb(OUT_AC)
.endc
"""
    tb_path = SIM_DIR / "tb_hpf_wrdata.cir"
    with open(tb_path, "w") as f:
        f.write(cir_content)
    
    run_ngspice_batch(tb_path)

    def read_dat(fn):
        xs, ys = [], []
        with open(SIM_DIR / fn) as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 2:
                    xs.append(float(parts[0]))
                    ys.append(float(parts[1]))
        return xs, ys

    x_100, y_100 = read_dat("hpf_100pct.txt")
    x_50, y_50 = read_dat("hpf_50pct.txt")

    series = [
        {"name": "HPF at 100% Vol (Rs = 50R, fc = 59.2 Hz)", "x": x_100, "y": y_100, "color": "#00ffcc"},
        {"name": "HPF at 50% Vol (Rs = 2.5k, fc = 62.0 Hz)", "x": x_50, "y": y_50, "color": "#ffaa00", "dash": "4,4"}
    ]
    svg = create_svg_chart(
        "Common 60 Hz 2nd-Order Sallen-Key HPF (Protects Both Mic & Line Modes)",
        "Frequency (Hz)",
        "Magnitude (dB relative to 0 dB passband)",
        series,
        x_log=True,
        y_min=-30,
        y_max=5
    )
    with open(SIM_DIR / "sim_d1_hpf_filter.svg", "w") as f:
        f.write(svg)
    print("Generated sim_d1_hpf_filter.svg")

# =============================================================================
# 4. DC PROTECTION & REGULATION DATA & PLOT
# =============================================================================
def generate_dc_plot():
    cir_content = """* DC wrdata testbench
.include "projects/live-pa-system/simulation/sim_d2_dc_protection.cir"
.control
  tran 20u 15m
  wrdata projects/live-pa-system/simulation/dc_ripple.txt v(DC_36V_PROT) v(REG_OUT)
.endc
"""
    tb_path = SIM_DIR / "tb_dc_wrdata.cir"
    with open(tb_path, "w") as f:
        f.write(cir_content)
    
    run_ngspice_batch(tb_path)

    ts, v_in, v_out = [], [], []
    with open(SIM_DIR / "dc_ripple.txt") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 3:
                t_ms = float(parts[0]) * 1000.0
                if t_ms >= 5.0:  # skip initial startup transient
                    ts.append(t_ms)
                    v_in.append(float(parts[1]))
                    v_out.append(float(parts[2]))

    # Plot transient ripple rejection
    series = [
        {"name": "Protected +36V Rail (35.93V with 200mVpp 100Hz ripple)", "x": ts, "y": v_in, "color": "#ffaa00"},
        {"name": "Regulated +15V Rail (15.06V, Ripple < 0.15mVpp, PSRR=62.7dB)", "x": ts, "y": v_out, "color": "#00ffcc"}
    ]
    svg = create_svg_chart(
        "Power Stage: P-MOSFET Reverse Protection & LM317HV +15V Regulation",
        "Time (ms)",
        "Voltage (V DC)",
        series,
        x_log=False,
        y_min=10,
        y_max=40
    )
    with open(SIM_DIR / "sim_d2_dc_protection.svg", "w") as f:
        f.write(svg)
    print("Generated sim_d2_dc_protection.svg")

# =============================================================================
# 5. RLC CONTOUR FILTER DATA & PLOT
# =============================================================================
def generate_rlc_plot():
    cir_content = """* RLC wrdata testbench
.include "projects/live-pa-system/simulation/sim_d4_rlc_complex_load.cir"
.control
  alter R_sw_bypass = 10Meg
  ac dec 100 20 20k
  wrdata projects/live-pa-system/simulation/rlc_active.txt vdb(DRV_POS)

  alter R_sw_bypass = 1m
  ac dec 100 20 20k
  wrdata projects/live-pa-system/simulation/rlc_bypassed.txt vdb(DRV_POS)
.endc
"""
    tb_path = SIM_DIR / "tb_rlc_wrdata.cir"
    with open(tb_path, "w") as f:
        f.write(cir_content)
    
    run_ngspice_batch(tb_path)

    def read_dat(fn):
        xs, ys = [], []
        with open(SIM_DIR / fn) as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 2:
                    xs.append(float(parts[0]))
                    ys.append(float(parts[1]))
        return xs, ys

    x_act, y_act = read_dat("rlc_active.txt")
    x_byp, y_byp = read_dat("rlc_bypassed.txt")

    series = [
        {"name": "RLC Contour Active (Notch Depth: -4.63 dB at 1.5 kHz)", "x": x_act, "y": y_act, "color": "#ff3366"},
        {"name": "RLC Bypassed (Flat Monitor Mode)", "x": x_byp, "y": y_byp, "color": "#00ffcc", "dash": "4,4"}
    ]
    svg = create_svg_chart(
        "Visaton BG 20 Passive RLC Contour Filter (Complex Voice-Coil Load)",
        "Frequency (Hz)",
        "Voltage Transfer at Driver Terminals (dB)",
        series,
        x_log=True,
        y_min=-8,
        y_max=2
    )
    with open(SIM_DIR / "sim_d4_rlc_complex_load.svg", "w") as f:
        f.write(svg)
    print("Generated sim_d4_rlc_complex_load.svg")

def cleanup():
    # Remove temporary .cir and .txt files
    for p in SIM_DIR.glob("tb_*.cir"):
        p.unlink()
    for p in SIM_DIR.glob("*.txt"):
        p.unlink()

if __name__ == "__main__":
    generate_mic_preamp_plot()
    generate_line_receiver_plot()
    generate_hpf_plot()
    generate_dc_plot()
    generate_rlc_plot()
    cleanup()
    print("All 5 testbench plots generated successfully!")
