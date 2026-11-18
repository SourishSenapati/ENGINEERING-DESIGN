"""
R-201 Ethylene Oxide Packed-Bed Tubular Reactor
Native SolidWorks 2025 Parametric CAD Modeling & Assembly Automation
ASME BPVC Section VIII Division 1 / TEMA Class R
Lead Process & Mechanical Engineer: Sourish Senapati (Roll: 002310301035)
Department of Chemical Engineering, Jadavpur University
"""

import os
import sys
import math
import shutil
import pythoncom
import win32com.client

# SolidWorks Constants
swDocPART = 1
swDocASSEMBLY = 2
swDocDRAWING = 3

swSaveAsCurrentVersion = 0
swSaveAsCopy = 2

# Directory paths
BASE_DIR = r"d:\GAMES\zercxes\CAD_Engineering_Drawings\Ethylene_Oxide_Reactor_Drawings"
SLDPRT_DIR = os.path.join(BASE_DIR, "cad", "sldprt")
SLDASM_DIR = os.path.join(BASE_DIR, "cad", "sldasm")
STEP_DIR = os.path.join(BASE_DIR, "cad", "step")

PART_TEMPLATE = r"C:\ProgramData\SolidWorks\SOLIDWORKS 2025\templates\Part.PRTDOT"
ASM_TEMPLATE = r"C:\ProgramData\SolidWorks\SOLIDWORKS 2025\templates\Assembly.ASMDOT"

def connect_solidworks():
    print("Connecting to SolidWorks COM Application...")
    sw = win32com.client.Dispatch("SldWorks.Application")
    sw.Visible = False
    print(f"Connected to SolidWorks version {sw.RevisionNumber}")
    return sw

def build_pressure_shell(sw):
    print("Modeling R201_Vessel_Pressure_Shell.SLDPRT...")
    model = sw.NewDocument(PART_TEMPLATE, 0, 0, 0)
    
    # Select Top Plane
    model.Extension.SelectByID2("Top Plane", "PLANE", 0, 0, 0, False, 0, pythoncom.Nothing, 0)
    model.SketchManager.InsertSketch(True)
    
    # Outer & Inner Circles for Cylindrical Shell
    # Ds = 84.0 in ID = 2.1336 m, ts = 1.125 in = 0.028575 m -> Ro = 1.095375 m, Ri = 1.0668 m
    Ro = 1.095375
    Ri = 1.0668
    L_shell = 9.144  # 30.0 ft
    
    model.SketchManager.CreateCircleByRadius(0, 0, 0, Ro)
    model.SketchManager.CreateCircleByRadius(0, 0, 0, Ri)
    
    # Extrude shell cylinder
    model.FeatureManager.FeatureExtrusion3(
        True, False, False, 0, 0, L_shell, 0.01,
        False, False, False, False, 0, 0, False, False, False, False,
        True, True, True, 0, 0, False
    )
    
    # Top Head Revolve / Dome
    H_head = 0.5334  # 21.0 in
    # Select Front Plane to sketch head cross section
    model.Extension.SelectByID2("Front Plane", "PLANE", 0, 0, 0, False, 0, pythoncom.Nothing, 0)
    model.SketchManager.InsertSketch(True)
    
    # Construct 2:1 ellipsoidal head profile
    # Centerline for revolution
    model.SketchManager.CreateCenterLine(0, L_shell, 0, 0, L_shell + H_head + 0.1, 0)
    # Head dome arc & straight flange
    model.SketchManager.CreateLine(Ri, L_shell - 0.05, 0, Ri, L_shell, 0)
    model.SketchManager.CreateLine(Ro, L_shell - 0.05, 0, Ro, L_shell, 0)
    model.SketchManager.CreateLine(Ri, L_shell - 0.05, 0, Ro, L_shell - 0.05, 0)
    # 3-point arc for outer and inner ellipse
    model.SketchManager.Create3PointArc(Ro, L_shell, 0, 0, L_shell + H_head + 0.028575, 0, Ro * 0.7, L_shell + H_head * 0.75, 0)
    model.SketchManager.Create3PointArc(Ri, L_shell, 0, 0, L_shell + H_head, 0, Ri * 0.7, L_shell + H_head * 0.72, 0)
    model.SketchManager.CreateLine(0, L_shell + H_head, 0, 0, L_shell + H_head + 0.028575, 0)
    
    model.FeatureManager.FeatureRevolve2(
        True, True, False, False, False, False, 0, 0,
        2 * math.pi, 0, False, False, 0.01, 0.01, 0, 0, 0, True, True, True
    )
    
    # Set Material (Carbon Steel SA-516 Gr 70)
    model.SetMaterialPropertyName2("Default", "SOLIDWORKS Materials", "Carbon Steel Sheet (SS)")
    
    save_path = os.path.join(SLDPRT_DIR, "R201_Vessel_Pressure_Shell.SLDPRT")
    model.SaveAs3(save_path, swSaveAsCurrentVersion, swSaveAsCopy)
    sw.CloseDoc(model.GetTitle)
    print(f"[SUCCESS] Saved {save_path}")
    return save_path

def build_tubesheet(sw):
    print("Modeling R201_Tubesheets_Pair.SLDPRT...")
    model = sw.NewDocument(PART_TEMPLATE, 0, 0, 0)
    
    model.Extension.SelectByID2("Top Plane", "PLANE", 0, 0, 0, False, 0, pythoncom.Nothing, 0)
    model.SketchManager.InsertSketch(True)
    
    # Tubesheet Disc: Dia = 84.0 in (Ri = 1.0668 m), Thickness = 3.75 in = 0.09525 m
    R_ts = 1.0668
    t_ts = 0.09525
    model.SketchManager.CreateCircleByRadius(0, 0, 0, R_ts)
    
    # Extrude Tubesheet Disc
    model.FeatureManager.FeatureExtrusion3(
        True, False, False, 0, 0, t_ts, 0.01,
        False, False, False, False, 0, 0, False, False, False, False,
        True, True, True, 0, 0, False
    )
    
    # Cut representative tube holes
    model.Extension.SelectByID2("", "FACE", 0, 0, t_ts, False, 0, pythoncom.Nothing, 0)
    model.SketchManager.InsertSketch(True)
    
    # Triangular pitch tube holes
    Pt = 0.060325  # 2.375 in
    r_hole = 0.0485 / 2.0
    otl = 2.06375 / 2.0
    
    holes_cut = 0
    for row in range(-6, 7):
        y = row * Pt * (math.sqrt(3) / 2.0)
        x_offset = (row % 2) * (Pt / 2.0)
        for col in range(-6, 7):
            x = col * Pt + x_offset
            if math.hypot(x, y) + r_hole <= otl * 0.4:  # Cut central representative cluster
                model.SketchManager.CreateCircleByRadius(x, y, 0, r_hole)
                holes_cut += 1
                
    # Extrude Cut through all
    model.FeatureManager.FeatureCut3(
        True, False, False, 1, 0, t_ts * 1.1, 0.01,
        False, False, False, False, 0, 0, False, False, False, False, False,
        True, True, True, True, False, 0, 0, False
    )
    
    model.SetMaterialPropertyName2("Default", "SOLIDWORKS Materials", "Forged Steel")
    save_path = os.path.join(SLDPRT_DIR, "R201_Tubesheets_Pair.SLDPRT")
    model.SaveAs3(save_path, swSaveAsCurrentVersion, swSaveAsCopy)
    sw.CloseDoc(model.GetTitle)
    print(f"[SUCCESS] Saved {save_path} ({holes_cut} holes extruded)")
    return save_path

def build_catalyst_tube(sw):
    print("Modeling R201_Schedule80_Catalyst_Tube.SLDPRT...")
    model = sw.NewDocument(PART_TEMPLATE, 0, 0, 0)
    
    model.Extension.SelectByID2("Top Plane", "PLANE", 0, 0, 0, False, 0, pythoncom.Nothing, 0)
    model.SketchManager.InsertSketch(True)
    
    # 1.5-in Schedule 80: OD = 1.900 in (0.04826 m), ID = 1.500 in (0.03810 m)
    Ro_t = 0.04826 / 2.0
    Ri_t = 0.03810 / 2.0
    L_tube = 9.144  # 30.0 ft
    
    model.SketchManager.CreateCircleByRadius(0, 0, 0, Ro_t)
    model.SketchManager.CreateCircleByRadius(0, 0, 0, Ri_t)
    
    model.FeatureManager.FeatureExtrusion3(
        True, False, False, 0, 0, L_tube, 0.01,
        False, False, False, False, 0, 0, False, False, False, False,
        True, True, True, 0, 0, False
    )
    
    model.SetMaterialPropertyName2("Default", "SOLIDWORKS Materials", "AISI 304")
    save_path = os.path.join(SLDPRT_DIR, "R201_Schedule80_Catalyst_Tube.SLDPRT")
    model.SaveAs3(save_path, swSaveAsCurrentVersion, swSaveAsCopy)
    sw.CloseDoc(model.GetTitle)
    print(f"[SUCCESS] Saved {save_path}")
    return save_path

def build_segmental_baffle(sw):
    print("Modeling R201_Transverse_Segmental_Baffle.SLDPRT...")
    model = sw.NewDocument(PART_TEMPLATE, 0, 0, 0)
    
    model.Extension.SelectByID2("Top Plane", "PLANE", 0, 0, 0, False, 0, pythoncom.Nothing, 0)
    model.SketchManager.InsertSketch(True)
    
    # Baffle diameter = 83.5 in = 2.1209 m (radius = 1.06045 m)
    # 20% cut height: chord at y = 0.6 * R
    R_b = 1.06045
    t_b = 0.0127  # 0.50 in
    y_cut = 0.6 * R_b
    x_cut = math.sqrt(R_b**2 - y_cut**2)
    
    # Arc and Chord line
    model.SketchManager.CreateLine(-x_cut, y_cut, 0, x_cut, y_cut, 0)
    model.SketchManager.Create3PointArc(-x_cut, y_cut, 0, x_cut, y_cut, 0, 0, -R_b, 0)
    
    # Extrude Baffle Plate
    model.FeatureManager.FeatureExtrusion3(
        True, False, False, 0, 0, t_b, 0.01,
        False, False, False, False, 0, 0, False, False, False, False,
        True, True, True, 0, 0, False
    )
    
    model.SetMaterialPropertyName2("Default", "SOLIDWORKS Materials", "Carbon Steel Sheet (SS)")
    save_path = os.path.join(SLDPRT_DIR, "R201_Transverse_Segmental_Baffle.SLDPRT")
    model.SaveAs3(save_path, swSaveAsCurrentVersion, swSaveAsCopy)
    sw.CloseDoc(model.GetTitle)
    print(f"[SUCCESS] Saved {save_path}")
    return save_path

def build_skirt_support(sw):
    print("Modeling R201_Skirt_Support_BaseRing.SLDPRT...")
    model = sw.NewDocument(PART_TEMPLATE, 0, 0, 0)
    
    model.Extension.SelectByID2("Top Plane", "PLANE", 0, 0, 0, False, 0, pythoncom.Nothing, 0)
    model.SketchManager.InsertSketch(True)
    
    # Skirt OD = 86.25 in (radius 1.095375 m), thickness = 0.75 in (0.01905 m), height = 8.0 ft = 2.4384 m
    R_sk_out = 1.095375
    R_sk_in = R_sk_out - 0.01905
    H_skirt = 2.4384
    
    model.SketchManager.CreateCircleByRadius(0, 0, 0, R_sk_out)
    model.SketchManager.CreateCircleByRadius(0, 0, 0, R_sk_in)
    
    model.FeatureManager.FeatureExtrusion3(
        True, False, False, 0, 0, H_skirt, 0.01,
        False, False, False, False, 0, 0, False, False, False, False,
        True, True, True, 0, 0, False
    )
    
    # Base Ring Flange at bottom
    model.Extension.SelectByID2("Top Plane", "PLANE", 0, 0, 0, False, 0, pythoncom.Nothing, 0)
    model.SketchManager.InsertSketch(True)
    
    R_base_out = 2.59715 / 2.0  # 102.25 in
    t_base = 0.0381             # 1.50 in
    model.SketchManager.CreateCircleByRadius(0, 0, 0, R_base_out)
    model.SketchManager.CreateCircleByRadius(0, 0, 0, R_sk_in)
    
    model.FeatureManager.FeatureExtrusion3(
        True, False, False, 0, 0, t_base, 0.01,
        False, False, False, False, 0, 0, False, False, False, False,
        True, True, True, 0, 0, False
    )
    
    model.SetMaterialPropertyName2("Default", "SOLIDWORKS Materials", "ASTM A36 Steel")
    save_path = os.path.join(SLDPRT_DIR, "R201_Skirt_Support_BaseRing.SLDPRT")
    model.SaveAs3(save_path, swSaveAsCurrentVersion, swSaveAsCopy)
    sw.CloseDoc(model.GetTitle)
    print(f"[SUCCESS] Saved {save_path}")
    return save_path

def build_nozzle_assembly(sw):
    print("Modeling R201_Nozzle_Flange_Subassembly.SLDPRT...")
    model = sw.NewDocument(PART_TEMPLATE, 0, 0, 0)
    
    model.Extension.SelectByID2("Top Plane", "PLANE", 0, 0, 0, False, 0, pythoncom.Nothing, 0)
    model.SketchManager.InsertSketch(True)
    
    # 16" NPS Sch 40: OD = 16.0 in (0.4064 m), ID = 15.0 in (0.381 m)
    r_pipe_out = 0.4064 / 2.0
    r_pipe_in = 0.3810 / 2.0
    l_neck = 0.450
    
    model.SketchManager.CreateCircleByRadius(0, 0, 0, r_pipe_out)
    model.SketchManager.CreateCircleByRadius(0, 0, 0, r_pipe_in)
    
    model.FeatureManager.FeatureExtrusion3(
        True, False, False, 0, 0, l_neck, 0.01,
        False, False, False, False, 0, 0, False, False, False, False,
        True, True, True, 0, 0, False
    )
    
    # 300# WNRF Flange: OD = 25.5 in (0.6477 m), Thickness = 3.5 in (0.0889 m)
    model.Extension.SelectByID2("", "FACE", 0, 0, l_neck, False, 0, pythoncom.Nothing, 0)
    model.SketchManager.InsertSketch(True)
    
    r_flange = 0.6477 / 2.0
    model.SketchManager.CreateCircleByRadius(0, 0, 0, r_flange)
    model.SketchManager.CreateCircleByRadius(0, 0, 0, r_pipe_in)
    
    # Bolt holes (20x holes on 22.5 in = 0.5715 m BCD)
    bc_r = 0.5715 / 2.0
    for i in range(20):
        ang = 2 * math.pi * i / 20
        model.SketchManager.CreateCircleByRadius(bc_r * math.cos(ang), bc_r * math.sin(ang), 0, 0.0175)
        
    model.FeatureManager.FeatureExtrusion3(
        True, False, False, 0, 0, 0.0889, 0.01,
        False, False, False, False, 0, 0, False, False, False, False,
        True, True, True, 0, 0, False
    )
    
    model.SetMaterialPropertyName2("Default", "SOLIDWORKS Materials", "Forged Steel")
    save_path = os.path.join(SLDPRT_DIR, "R201_Nozzle_Flange_Subassembly.SLDPRT")
    model.SaveAs3(save_path, swSaveAsCurrentVersion, swSaveAsCopy)
    sw.CloseDoc(model.GetTitle)
    print(f"[SUCCESS] Saved {save_path}")
    return save_path

def build_master_assembly(sw, part_paths):
    print("Building R201_Ethylene_Oxide_Reactor_Master.SLDASM...")
    asm = sw.NewDocument(ASM_TEMPLATE, 0, 0, 0)
    
    # Insert Primary Shell
    shell_path = part_paths["shell"]
    c1 = asm.AddComponent5(shell_path, 0, "", False, "", 0, 0, 0)
    print("Inserted shell component into master assembly.")
    
    # Insert Tubesheet (Upper at Z = 9.144m, Lower at Z = 0m)
    ts_path = part_paths["tubesheet"]
    asm.AddComponent5(ts_path, 0, "", False, "", 0, 0, 9.144 - 0.09525)
    asm.AddComponent5(ts_path, 0, "", False, "", 0, 0, 0.0)
    print("Inserted pair of tubesheets.")
    
    # Insert Tubes (Bundle Array)
    tube_path = part_paths["tube"]
    Pt = 0.060325
    for i in range(-2, 3):
        for j in range(-2, 3):
            tx = i * Pt
            ty = j * Pt * (math.sqrt(3) / 2.0)
            if math.hypot(tx, ty) < 0.3:
                asm.AddComponent5(tube_path, 0, "", False, "", tx, ty, 0.09525)
    print("Inserted representative catalyst tube cluster.")
    
    # Insert Baffle
    baffle_path = part_paths["baffle"]
    for b_idx in range(1, 10):
        bz = b_idx * (9.144 / 10.0)
        asm.AddComponent5(baffle_path, 0, "", False, "", 0, 0, bz)
    print("Inserted 9 segmental baffles.")
    
    # Insert Skirt Support
    skirt_path = part_paths["skirt"]
    asm.AddComponent5(skirt_path, 0, "", False, "", 0, 0, -2.4384)
    print("Inserted skirt support & base ring.")
    
    # Insert Nozzles (N1 Top, N2 Bottom)
    nozzle_path = part_paths["nozzle"]
    asm.AddComponent5(nozzle_path, 0, "", False, "", 0, 0, 9.144 + 0.5334)
    print("Inserted process gas nozzle.")
    
    # Save Native Assembly (.SLDASM)
    asm_save_path = os.path.join(SLDASM_DIR, "R201_Ethylene_Oxide_Reactor_Master.SLDASM")
    asm.SaveAs3(asm_save_path, swSaveAsCurrentVersion, swSaveAsCopy)
    print(f"[SUCCESS] Saved Master Assembly: {asm_save_path}")
    
    # Export Standard STEP AP214 (.step)
    step_save_path = os.path.join(STEP_DIR, "R201_Ethylene_Oxide_Reactor_Assembly.step")
    asm.SaveAs3(step_save_path, swSaveAsCurrentVersion, swSaveAsCopy)
    print(f"[SUCCESS] Exported STEP AP214 Exchange Model: {step_save_path}")
    
    sw.CloseDoc(asm.GetTitle)
    return asm_save_path, step_save_path

def sync_to_pedd():
    print("Synchronizing SolidWorks Models to PEDD directories...")
    dest_bases = [
        r"D:\user\SOURISH SENAPATI\Downloads\pedd\cad",
        r"D:\Downloads\pedd\cad",
        r"C:\Users\SOURISH SENAPATI\Downloads\pedd\cad"
    ]
    subdirs = ["sldprt", "sldasm", "step"]
    for base in dest_bases:
        for sub in subdirs:
            src = os.path.join(BASE_DIR, "cad", sub)
            dst = os.path.join(base, sub)
            if os.path.exists(src):
                try:
                    os.makedirs(dst, exist_ok=True)
                    for item in os.listdir(src):
                        s_f = os.path.join(src, item)
                        d_f = os.path.join(dst, item)
                        if os.path.isfile(s_f):
                            shutil.copy2(s_f, d_f)
                    print(f"Synced {sub} -> {dst}")
                except Exception as e:
                    print(f"Error syncing to {dst}: {e}")

def main():
    os.makedirs(SLDPRT_DIR, exist_ok=True)
    os.makedirs(SLDASM_DIR, exist_ok=True)
    os.makedirs(STEP_DIR, exist_ok=True)
    
    print("=" * 70)
    print("R-201 ETHYLENE OXIDE PACKED-BED TUBULAR REACTOR")
    print("SOLIDWORKS 2025 PARAMETRIC CAD MODELING & ASSEMBLY GENERATION")
    print("=" * 70)
    
    sw = connect_solidworks()
    try:
        parts = {}
        parts["shell"] = build_pressure_shell(sw)
        parts["tubesheet"] = build_tubesheet(sw)
        parts["tube"] = build_catalyst_tube(sw)
        parts["baffle"] = build_segmental_baffle(sw)
        parts["skirt"] = build_skirt_support(sw)
        parts["nozzle"] = build_nozzle_assembly(sw)
        
        build_master_assembly(sw, parts)
        sync_to_pedd()
        
    finally:
        print("Closing SolidWorks session...")
        try:
            sw.ExitApp()
        except:
            pass
        print("=" * 70)
        print("[SOLIDWORKS AUTOMATION COMPLETE]")

if __name__ == "__main__":
    main()
