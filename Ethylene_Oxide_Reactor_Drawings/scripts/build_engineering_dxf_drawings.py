"""
R-201 Ethylene Oxide Packed-Bed Tubular Reactor
Standard Engineering 2D DXF Drawing Generator (ASME BPVC / TEMA Class R)
Lead Process & Mechanical Engineer: Sourish Senapati (Roll: 002310301035)
Department of Chemical Engineering, Jadavpur University
"""

import os
import math
import numpy as np
import ezdxf
from ezdxf import colors
from ezdxf.enums import TextEntityAlignment

def setup_layers(doc):
    layers = [
        ("TITLE_BLOCK", colors.WHITE, "CONTINUOUS"),
        ("EQUIPMENT", colors.CYAN, "CONTINUOUS"),
        ("VESSEL_SHELL", colors.CYAN, "CONTINUOUS"),
        ("TUBES", colors.LIGHT_GRAY, "CONTINUOUS"),
        ("BAFFLES", colors.YELLOW, "CONTINUOUS"),
        ("NOZZLES", colors.GREEN, "CONTINUOUS"),
        ("CENTERLINE", colors.RED, "CENTER"),
        ("DIMENSIONS", colors.MAGENTA, "CONTINUOUS"),
        ("TEXT", colors.WHITE, "CONTINUOUS"),
        ("HATCH", colors.GRAY, "CONTINUOUS"),
        ("INSTRUMENTS", colors.YELLOW, "CONTINUOUS"),
        ("PIPING", colors.GREEN, "CONTINUOUS"),
    ]
    for name, col, linetype in layers:
        if name not in doc.layers:
            layer = doc.layers.add(name, color=col)
            if linetype in doc.linetypes:
                layer.linetype = linetype

def draw_title_block(msp, dwg_no, dwg_title, sheet_str="1 OF 1", rev="REV 0"):
    # Outer Border A1 standard (841 x 594 mm)
    msp.add_lwpolyline([(0, 0), (841, 0), (841, 594), (0, 594), (0, 0)], dxfattribs={"layer": "TITLE_BLOCK", "lineweight": 50})
    msp.add_lwpolyline([(10, 10), (831, 10), (831, 584), (10, 584), (10, 10)], dxfattribs={"layer": "TITLE_BLOCK", "lineweight": 25})
    
    # Title Box in Bottom Right (600, 10) to (831, 110)
    bx0, by0 = 530, 10
    bx1, by1 = 831, 110
    msp.add_lwpolyline([(bx0, by0), (bx1, by0), (bx1, by1), (bx0, by1), (bx0, by0)], dxfattribs={"layer": "TITLE_BLOCK", "lineweight": 35})
    msp.add_line((bx0, by0 + 75), (bx1, by0 + 75), dxfattribs={"layer": "TITLE_BLOCK"})
    msp.add_line((bx0, by0 + 50), (bx1, by0 + 50), dxfattribs={"layer": "TITLE_BLOCK"})
    msp.add_line((bx0, by0 + 25), (bx1, by0 + 25), dxfattribs={"layer": "TITLE_BLOCK"})
    msp.add_line((bx0 + 150, by0), (bx0 + 150, by0 + 50), dxfattribs={"layer": "TITLE_BLOCK"})
    
    # Academic and Project Details
    msp.add_text("JADAVPUR UNIVERSITY - DEPARTMENT OF CHEMICAL ENGINEERING",
                 dxfattribs={"layer": "TEXT", "height": 4.5}).set_placement((bx0 + 10, by0 + 85))
    msp.add_text("ETHYLENE OXIDE PACKED-BED TUBULAR REACTOR (R-201)",
                 dxfattribs={"layer": "TEXT", "height": 3.5}).set_placement((bx0 + 10, by0 + 78))
    
    msp.add_text(f"TITLE: {dwg_title}", dxfattribs={"layer": "TEXT", "height": 4.0}).set_placement((bx0 + 10, by0 + 58))
    msp.add_text(f"DWG NO: {dwg_no}", dxfattribs={"layer": "TEXT", "height": 3.8}).set_placement((bx0 + 10, by0 + 35))
    msp.add_text(f"LEAD ENGINEER: SOURISH SENAPATI (ROLL: 002310301035)", dxfattribs={"layer": "TEXT", "height": 3.0}).set_placement((bx0 + 10, by0 + 15))
    msp.add_text(f"REV: {rev}  |  SHEET: {sheet_str}", dxfattribs={"layer": "TEXT", "height": 3.2}).set_placement((bx0 + 160, by0 + 35))
    msp.add_text("DESIGN CODE: ASME SEC VIII DIV 1 / TEMA R", dxfattribs={"layer": "TEXT", "height": 2.8}).set_placement((bx0 + 160, by0 + 15))

def generate_elevation_dxf(out_path):
    print("Generating R201_Elevation_Cross_Section.dxf...")
    doc = ezdxf.new("R2010")
    msp = doc.modelspace()
    setup_layers(doc)
    
    draw_title_block(msp, "DWG-R201-MEC-001", "GENERAL ARRANGEMENT & ELEVATION CROSS SECTION", "1 OF 3")
    
    # Scale: Draw vessel at center of page (approx 400 mm tall on paper, scale 1:25)
    # True dimensions (mm):
    # Shell ID = 2133.6 mm, OD = 2190.75 mm (ts = 28.575 mm)
    # L_shell = 9144 mm
    # Head depth = 533.4 mm (2:1 ellipsoidal)
    # Skirt height = 2438.4 mm
    # Total vessel height = 9144 + 2*533.4 + 2438.4 = 12649.2 mm
    # Scale factor S = 0.035 (12649.2 * 0.035 = 442.7 mm tall on drawing)
    S = 0.035
    cx = 320.0
    cy_base = 50.0  # Ground base ring center
    
    # Coordinates in mm on drawing
    r_in = (2133.6 / 2.0) * S
    r_out = (2190.75 / 2.0) * S
    h_skirt = 2438.4 * S
    h_shell = 9144.0 * S
    h_head = 533.4 * S
    t_ts = 95.25 * S
    
    y_skirt_bot = cy_base
    y_skirt_top = y_skirt_bot + h_skirt
    y_shell_bot = y_skirt_top
    y_shell_top = y_shell_bot + h_shell
    y_head_top = y_shell_top + h_head
    y_head_bot = y_shell_bot - h_head
    
    # Centerline
    msp.add_line((cx, cy_base - 20), (cx, y_head_top + 40), dxfattribs={"layer": "CENTERLINE"})
    
    # 1. Base Ring & Skirt
    r_base = (2597.15 / 2.0) * S
    t_base = 38.1 * S
    msp.add_lwpolyline([(cx - r_base, y_skirt_bot), (cx + r_base, y_skirt_bot),
                        (cx + r_base, y_skirt_bot + t_base), (cx - r_base, y_skirt_bot + t_base),
                        (cx - r_base, y_skirt_bot)], dxfattribs={"layer": "EQUIPMENT", "lineweight": 35})
    # Skirt walls
    msp.add_line((cx - r_out, y_skirt_bot + t_base), (cx - r_out, y_skirt_top), dxfattribs={"layer": "EQUIPMENT", "lineweight": 30})
    msp.add_line((cx + r_out, y_skirt_bot + t_base), (cx + r_out, y_skirt_top), dxfattribs={"layer": "EQUIPMENT", "lineweight": 30})
    # Skirt access manway (DN600)
    mw_y = y_skirt_bot + h_skirt * 0.45
    msp.add_circle((cx, mw_y), radius=600.0 * S / 2.0, dxfattribs={"layer": "EQUIPMENT"})
    msp.add_text("DN600 SKIRT MANWAY", dxfattribs={"layer": "TEXT", "height": 2.2}).set_placement((cx - 18, mw_y - 15))
    
    # 2. Reactor Shell Walls (Left side exterior, Right side cross section)
    msp.add_line((cx - r_out, y_shell_bot), (cx - r_out, y_shell_top), dxfattribs={"layer": "VESSEL_SHELL", "lineweight": 35})
    msp.add_line((cx - r_in, y_shell_bot), (cx - r_in, y_shell_top), dxfattribs={"layer": "VESSEL_SHELL", "lineweight": 20})
    msp.add_line((cx + r_out, y_shell_bot), (cx + r_out, y_shell_top), dxfattribs={"layer": "VESSEL_SHELL", "lineweight": 35})
    msp.add_line((cx + r_in, y_shell_bot), (cx + r_in, y_shell_top), dxfattribs={"layer": "VESSEL_SHELL", "lineweight": 20})
    
    # 3. Tubesheets (Upper & Lower)
    msp.add_lwpolyline([(cx - r_in, y_shell_top - t_ts), (cx + r_in, y_shell_top - t_ts),
                        (cx + r_in, y_shell_top), (cx - r_in, y_shell_top),
                        (cx - r_in, y_shell_top - t_ts)], dxfattribs={"layer": "EQUIPMENT", "lineweight": 30})
    msp.add_lwpolyline([(cx - r_in, y_shell_bot), (cx + r_in, y_shell_bot),
                        (cx + r_in, y_shell_bot + t_ts), (cx - r_in, y_shell_bot + t_ts),
                        (cx - r_in, y_shell_bot)], dxfattribs={"layer": "EQUIPMENT", "lineweight": 30})
    
    # 4. Tubes (Right half bundle cross-section)
    y_tube_bot = y_shell_bot + t_ts
    y_tube_top = y_shell_top - t_ts
    for i in range(1, 16):
        tx = cx + (i / 16.0) * (r_in - 5)
        msp.add_line((tx, y_tube_bot), (tx, y_tube_top), dxfattribs={"layer": "TUBES", "lineweight": 13})
    
    # 5. Segmental Baffles (9 Baffles)
    for b_idx in range(1, 10):
        by = y_shell_bot + (b_idx / 10.0) * h_shell
        if b_idx % 2 == 1:
            # Cut on right
            msp.add_line((cx - r_in, by), (cx + r_in * 0.4, by), dxfattribs={"layer": "BAFFLES", "lineweight": 30})
        else:
            # Cut on left
            msp.add_line((cx - r_in * 0.4, by), (cx + r_in, by), dxfattribs={"layer": "BAFFLES", "lineweight": 30})
            
    # 6. Heads (Top and Bottom 2:1 Ellipsoidal)
    # Spline / Polyline for heads
    t_vals = np.linspace(-np.pi/2, np.pi/2, 30)
    top_pts = [(cx + r_out * np.cos(t), y_shell_top + h_head * np.sin(t)) for t in t_vals if np.sin(t) >= 0]
    top_pts_rev = [(cx + r_in * np.cos(t), y_shell_top + (h_head - 28.575*S) * np.sin(t)) for t in reversed(t_vals) if np.sin(t) >= 0]
    msp.add_lwpolyline(top_pts, dxfattribs={"layer": "VESSEL_SHELL", "lineweight": 35})
    
    bot_pts = [(cx + r_out * np.cos(t), y_shell_bot - h_head * np.sin(t)) for t in t_vals if np.sin(t) >= 0]
    msp.add_lwpolyline(bot_pts, dxfattribs={"layer": "VESSEL_SHELL", "lineweight": 35})
    
    # 7. Nozzles N1 - N5
    # N1: Process Gas Inlet 16"
    rn1 = (406.4 / 2.0) * S
    msp.add_lwpolyline([(cx - rn1, y_head_top), (cx - rn1, y_head_top + 18),
                        (cx - rn1 * 1.5, y_head_top + 18), (cx - rn1 * 1.5, y_head_top + 22),
                        (cx + rn1 * 1.5, y_head_top + 22), (cx + rn1 * 1.5, y_head_top + 18),
                        (cx + rn1, y_head_top + 18), (cx + rn1, y_head_top)],
                       dxfattribs={"layer": "NOZZLES", "lineweight": 30})
    msp.add_text("N1: 16\" FEED GAS INLET (300# WNRF)", dxfattribs={"layer": "TEXT", "height": 2.5}).set_placement((cx + 15, y_head_top + 20))
    
    # N2: Product Gas Outlet 16"
    msp.add_lwpolyline([(cx - rn1, y_head_bot), (cx - rn1, y_head_bot - 18),
                        (cx - rn1 * 1.5, y_head_bot - 18), (cx - rn1 * 1.5, y_head_bot - 22),
                        (cx + rn1 * 1.5, y_head_bot - 22), (cx + rn1 * 1.5, y_head_bot - 18),
                        (cx + rn1, y_head_bot - 18), (cx + rn1, y_head_bot)],
                       dxfattribs={"layer": "NOZZLES", "lineweight": 30})
    msp.add_text("N2: 16\" PRODUCT OUTLET (300# WNRF)", dxfattribs={"layer": "TEXT", "height": 2.5}).set_placement((cx + 15, y_head_bot - 25))
    
    # N3: Dowtherm A Inlet 10" (Z = 0.85m)
    rn3 = (273.05 / 2.0) * S
    yn3 = y_shell_bot + 850.0 * S
    msp.add_lwpolyline([(cx + r_out, yn3 - rn3), (cx + r_out + 14, yn3 - rn3),
                        (cx + r_out + 14, yn3 - rn3 * 1.5), (cx + r_out + 17, yn3 - rn3 * 1.5),
                        (cx + r_out + 17, yn3 + rn3 * 1.5), (cx + r_out + 14, yn3 + rn3 * 1.5),
                        (cx + r_out + 14, yn3 + rn3), (cx + r_out, yn3 + rn3)],
                       dxfattribs={"layer": "NOZZLES", "lineweight": 30})
    msp.add_text("N3: 10\" COOLANT INLET (300#)", dxfattribs={"layer": "TEXT", "height": 2.2}).set_placement((cx + r_out + 20, yn3))
    
    # N4: Dowtherm A Outlet 10" (Z = 8.30m)
    yn4 = y_shell_bot + 8300.0 * S
    msp.add_lwpolyline([(cx - r_out, yn4 - rn3), (cx - r_out - 14, yn4 - rn3),
                        (cx - r_out - 14, yn4 - rn3 * 1.5), (cx - r_out - 17, yn4 - rn3 * 1.5),
                        (cx - r_out - 17, yn4 + rn3 * 1.5), (cx - r_out - 14, yn4 + rn3 * 1.5),
                        (cx - r_out - 14, yn4 + rn3), (cx - r_out, yn4 + rn3)],
                       dxfattribs={"layer": "NOZZLES", "lineweight": 30})
    msp.add_text("N4: 10\" COOLANT OUTLET (300#)", dxfattribs={"layer": "TEXT", "height": 2.2}).set_placement((cx - r_out - 75, yn4))
    
    # 8. Engineering Dimensions
    # Height dimension
    dim_x = cx - r_out - 45
    msp.add_line((dim_x, y_shell_bot), (dim_x, y_shell_top), dxfattribs={"layer": "DIMENSIONS"})
    msp.add_line((dim_x - 5, y_shell_bot), (dim_x + 5, y_shell_bot), dxfattribs={"layer": "DIMENSIONS"})
    msp.add_line((dim_x - 5, y_shell_top), (dim_x + 5, y_shell_top), dxfattribs={"layer": "DIMENSIONS"})
    msp.add_text("TUBE LENGTH = 9,144 mm (30.0 ft)", dxfattribs={"layer": "TEXT", "height": 3.0, "rotation": 90}).set_placement((dim_x - 8, y_shell_bot + h_shell * 0.35))
    
    # Diameter dimension
    dim_y = y_shell_top + 15
    msp.add_line((cx - r_in, dim_y), (cx + r_in, dim_y), dxfattribs={"layer": "DIMENSIONS"})
    msp.add_line((cx - r_in, dim_y - 3), (cx - r_in, dim_y + 3), dxfattribs={"layer": "DIMENSIONS"})
    msp.add_line((cx + r_in, dim_y - 3), (cx + r_in, dim_y + 3), dxfattribs={"layer": "DIMENSIONS"})
    msp.add_text("SHELL ID = 2,133.6 mm (84.0 in)", dxfattribs={"layer": "TEXT", "height": 2.8}).set_placement((cx - 35, dim_y + 3))

    doc.saveas(out_path)
    print(f"[SUCCESS] Exported Elevation DXF: {out_path}")

def generate_tubesheet_dxf(out_path):
    print("Generating R201_Tubesheet_Drilling_Pattern.dxf...")
    doc = ezdxf.new("R2010")
    msp = doc.modelspace()
    setup_layers(doc)
    
    draw_title_block(msp, "DWG-R201-MEC-002", "TUBESHEET DRILLING PATTERN & TUBE LAYOUT", "2 OF 3")
    
    # Scale: Tubesheet 84.0" (2133.6 mm) drawn at S = 0.18 (dia ~ 384 mm on A1 page)
    S = 0.18
    cx, cy = 280.0, 300.0
    
    r_shell = (2133.6 / 2.0) * S
    r_otl = (2063.75 / 2.0) * S
    r_bolt = (2387.6 / 2.0) * S
    r_ts_out = (2500.0 / 2.0) * S
    
    # Centerlines
    msp.add_line((cx - r_ts_out - 15, cy), (cx + r_ts_out + 15, cy), dxfattribs={"layer": "CENTERLINE"})
    msp.add_line((cx, cy - r_ts_out - 15), (cx, cy + r_ts_out + 15), dxfattribs={"layer": "CENTERLINE"})
    
    # Outer tubesheet perimeter & OTL circle
    msp.add_circle((cx, cy), radius=r_ts_out, dxfattribs={"layer": "EQUIPMENT", "lineweight": 35})
    msp.add_circle((cx, cy), radius=r_shell, dxfattribs={"layer": "VESSEL_SHELL", "lineweight": 25})
    msp.add_circle((cx, cy), radius=r_otl, dxfattribs={"layer": "CENTERLINE", "lineweight": 18})
    
    # Tubes: 1,021 tubes on triangular pitch Pt = 60.325 mm * S
    Pt = 60.325 * S
    r_hole = (48.5 / 2.0) * S
    
    tube_count = 0
    n_rows = 24
    for row in range(-n_rows, n_rows + 1):
        y = cy + row * Pt * (math.sqrt(3) / 2.0)
        x_offset = (row % 2) * (Pt / 2.0)
        for col in range(-n_rows, n_rows + 1):
            x = cx + col * Pt + x_offset
            dist = math.hypot(x - cx, y - cy)
            if dist + r_hole <= r_otl:
                msp.add_circle((x, y), radius=r_hole, dxfattribs={"layer": "TUBES", "lineweight": 13})
                tube_count += 1
                
    # Tie rods (6x)
    r_tierod = r_otl * 0.75
    for i in range(6):
        ang = 2 * math.pi * i / 6 + math.pi / 6
        tx = cx + r_tierod * math.cos(ang)
        ty = cy + r_tierod * math.sin(ang)
        msp.add_circle((tx, ty), radius=19.0 * S / 2.0, dxfattribs={"layer": "EQUIPMENT", "lineweight": 35})
        msp.add_text(f"TR-{i+1}", dxfattribs={"layer": "TEXT", "height": 2.0}).set_placement((tx + 2, ty + 2))
        
    # Tubesheet Schedule & Drilling Table in Top Right
    tx0, ty0 = 550, 480
    msp.add_lwpolyline([(tx0, ty0), (tx0 + 260, ty0), (tx0 + 260, ty0 - 240), (tx0, ty0 - 240), (tx0, ty0)],
                       dxfattribs={"layer": "TITLE_BLOCK", "lineweight": 30})
    msp.add_text("TUBESHEET FABRICATION SCHEDULE", dxfattribs={"layer": "TEXT", "height": 4.0}).set_placement((tx0 + 10, ty0 - 15))
    msp.add_line((tx0, ty0 - 22), (tx0 + 260, ty0 - 22), dxfattribs={"layer": "TITLE_BLOCK"})
    
    sched_items = [
        ("Nominal Shell Inside Dia (Ds):", "84.0 in (2,133.6 mm)"),
        ("Outer Tube Limit (OTL):", "81.25 in (2,063.75 mm)"),
        ("Tubesheet Thickness (t_ts):", "3.75 in (95.25 mm) Forged SA-266"),
        ("Total Tube Holes:", f"{tube_count} Tubes (1021 Specified)"),
        ("Tube Pitch Pattern:", "2.375 in (60.325 mm) 30 deg Triangular"),
        ("Tube Outside Diameter (Do):", "1.900 in (48.26 mm) - 1.5\" Sch 80"),
        ("Tube Wall Thickness (tw):", "0.200 in (5.08 mm) Seamless TP304"),
        ("Hole Drilling Diameter:", "48.51 mm (+0.10 / -0.00 mm)"),
        ("Tube-to-Tubesheet Joint:", "Expanded + Seal Welded (ASME UW-20)"),
        ("Groove Detail:", "2 Grooves, 3.2 mm W x 0.4 mm D"),
        ("Tie Rods & Spacers:", "6x Dia 19 mm SA-240 304 with Spacers"),
        ("Baffle Cut:", "20% Segmental Cut (Alternating)")
    ]
    
    for idx, (lbl, val) in enumerate(sched_items):
        y_pos = ty0 - 38 - idx * 16
        msp.add_text(lbl, dxfattribs={"layer": "TEXT", "height": 2.8}).set_placement((tx0 + 8, y_pos))
        msp.add_text(val, dxfattribs={"layer": "TEXT", "height": 2.8}).set_placement((tx0 + 140, y_pos))

    doc.saveas(out_path)
    print(f"[SUCCESS] Exported Tubesheet DXF: {out_path} ({tube_count} tubes drawn)")

def generate_pid_dxf(out_path):
    print("Generating R201_Piping_PID_Flowsheet.dxf...")
    doc = ezdxf.new("R2010")
    msp = doc.modelspace()
    setup_layers(doc)
    
    draw_title_block(msp, "DWG-R201-PID-001", "PROCESS PIPING & INSTRUMENTATION DIAGRAM (P&ID)", "3 OF 3")
    
    # Draw Reactor R-201 at center
    rx, ry = 280, 280
    rw, rh = 50, 160
    msp.add_lwpolyline([(rx - rw/2, ry - rh/2), (rx + rw/2, ry - rh/2),
                        (rx + rw/2, ry + rh/2), (rx - rw/2, ry + rh/2),
                        (rx - rw/2, ry - rh/2)], dxfattribs={"layer": "EQUIPMENT", "lineweight": 40})
    # Heads
    msp.add_arc((rx, ry + rh/2), radius=rw/2, start_angle=0, end_angle=180, dxfattribs={"layer": "EQUIPMENT", "lineweight": 40})
    msp.add_arc((rx, ry - rh/2), radius=rw/2, start_angle=180, end_angle=360, dxfattribs={"layer": "EQUIPMENT", "lineweight": 40})
    msp.add_text("R-201", dxfattribs={"layer": "TEXT", "height": 5.0}).set_placement((rx - 15, ry + 10))
    msp.add_text("ETHYLENE OXIDE", dxfattribs={"layer": "TEXT", "height": 2.5}).set_placement((rx - 20, ry - 5))
    msp.add_text("TUBULAR REACTOR", dxfattribs={"layer": "TEXT", "height": 2.5}).set_placement((rx - 22, ry - 15))
    
    # Process Feed Line L-201
    msp.add_line((80, ry + rh/2 + 60), (rx, ry + rh/2 + 60), dxfattribs={"layer": "PIPING", "lineweight": 35})
    msp.add_line((rx, ry + rh/2 + 60), (rx, ry + rh/2 + 25), dxfattribs={"layer": "PIPING", "lineweight": 35})
    msp.add_text("LINE L-201: 16\"-CS-300#-ETHYLENE/AIR FEED", dxfattribs={"layer": "TEXT", "height": 2.8}).set_placement((90, ry + rh/2 + 65))
    
    # Control Valve FCV-201 on feed line
    fcv_x = 160
    fcv_y = ry + rh/2 + 60
    msp.add_lwpolyline([(fcv_x - 8, fcv_y - 6), (fcv_x + 8, fcv_y + 6), (fcv_x + 8, fcv_y - 6),
                        (fcv_x - 8, fcv_y + 6), (fcv_x - 8, fcv_y - 6)], dxfattribs={"layer": "INSTRUMENTS"})
    msp.add_text("FCV-201", dxfattribs={"layer": "TEXT", "height": 2.2}).set_placement((fcv_x - 8, fcv_y + 10))
    
    # Product Line L-202
    msp.add_line((rx, ry - rh/2 - 25), (rx, ry - rh/2 - 60), dxfattribs={"layer": "PIPING", "lineweight": 35})
    msp.add_line((rx, ry - rh/2 - 60), (450, ry - rh/2 - 60), dxfattribs={"layer": "PIPING", "lineweight": 35})
    msp.add_text("LINE L-202: 16\"-CS-300#-PRODUCT GAS TO ABSORBER", dxfattribs={"layer": "TEXT", "height": 2.8}).set_placement((290, ry - rh/2 - 55))
    
    # Dowtherm Coolant Loop E-201 & P-201
    # Coolant In L-203 (Low)
    msp.add_line((rx + rw/2, ry - rh/2 + 20), (rx + rw/2 + 80, ry - rh/2 + 20), dxfattribs={"layer": "PIPING", "lineweight": 30})
    msp.add_text("L-203: 10\" DOWTHERM IN (420 GPM)", dxfattribs={"layer": "TEXT", "height": 2.2}).set_placement((rx + rw/2 + 10, ry - rh/2 + 25))
    
    # Coolant Out L-204 (High)
    msp.add_line((rx - rw/2, ry + rh/2 - 20), (rx - rw/2 - 80, ry + rh/2 - 20), dxfattribs={"layer": "PIPING", "lineweight": 30})
    msp.add_text("L-204: 10\" DOWTHERM OUT (17.26 MW)", dxfattribs={"layer": "TEXT", "height": 2.2}).set_placement((rx - rw/2 - 75, ry + rh/2 - 15))
    
    # Safety PSV-201 on Top Channel
    msp.add_line((rx, ry + rh/2 + 25), (rx + 40, ry + rh/2 + 25), dxfattribs={"layer": "PIPING", "lineweight": 25})
    msp.add_text("PSV-201A/B", dxfattribs={"layer": "TEXT", "height": 2.5}).set_placement((rx + 45, ry + rh/2 + 25))
    
    # Instrument Balloons (ISA-5.1)
    # FIT-201
    msp.add_circle((fcv_x, fcv_y + 30), radius=9, dxfattribs={"layer": "INSTRUMENTS"})
    msp.add_line((fcv_x - 9, fcv_y + 30), (fcv_x + 9, fcv_y + 30), dxfattribs={"layer": "INSTRUMENTS"})
    msp.add_text("FIT", dxfattribs={"layer": "TEXT", "height": 2.5}).set_placement((fcv_x - 4, fcv_y + 33))
    msp.add_text("201", dxfattribs={"layer": "TEXT", "height": 2.5}).set_placement((fcv_x - 4, fcv_y + 23))
    msp.add_line((fcv_x, fcv_y + 6), (fcv_x, fcv_y + 21), dxfattribs={"layer": "INSTRUMENTS", "linetype": "DASHED"})
    
    # Multipoint Temperature TIT-201 (10 Zones)
    msp.add_circle((rx + rw/2 + 30, ry + 20), radius=9, dxfattribs={"layer": "INSTRUMENTS"})
    msp.add_line((rx + rw/2 + 21, ry + 20), (rx + rw/2 + 39, ry + 20), dxfattribs={"layer": "INSTRUMENTS"})
    msp.add_text("TIT", dxfattribs={"layer": "TEXT", "height": 2.5}).set_placement((rx + rw/2 + 26, ry + 23))
    msp.add_text("201", dxfattribs={"layer": "TEXT", "height": 2.5}).set_placement((rx + rw/2 + 26, ry + 13))
    msp.add_text("10-ZONE THERMOWELL", dxfattribs={"layer": "TEXT", "height": 2.0}).set_placement((rx + rw/2 + 42, ry + 18))

    doc.saveas(out_path)
    print(f"[SUCCESS] Exported P&ID DXF: {out_path}")

def main():
    dxf_dir = r"d:\GAMES\zercxes\CAD_Engineering_Drawings\Ethylene_Oxide_Reactor_Drawings\cad\dxf"
    os.makedirs(dxf_dir, exist_ok=True)
    
    print("=" * 70)
    print("GENERATING ASME / TEMA STANDARDS-COMPLIANT DXF DRAWINGS")
    print("=" * 70)
    
    p1 = os.path.join(dxf_dir, "R201_Elevation_Cross_Section.dxf")
    generate_elevation_dxf(p1)
    
    p2 = os.path.join(dxf_dir, "R201_Tubesheet_Drilling_Pattern.dxf")
    generate_tubesheet_dxf(p2)
    
    p3 = os.path.join(dxf_dir, "R201_Piping_PID_Flowsheet.dxf")
    generate_pid_dxf(p3)
    
    print("=" * 70)
    print("[ALL DXF DRAWINGS GENERATED SUCCESSFULLY]")

if __name__ == '__main__':
    main()
