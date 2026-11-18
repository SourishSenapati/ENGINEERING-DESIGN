"""
R-201 Ethylene Oxide Packed-Bed Tubular Reactor
B-Rep Solid Body Tessellation & Industrial Multi-Material PBR GLB Generator
Lead Process & Mechanical Engineer: Sourish Senapati (Roll: 002310301035)
Department of Chemical Engineering, Jadavpur University
"""

import os
import sys
import numpy as np
import trimesh
import trimesh.visual
import trimesh.visual.material
from shapely.geometry import Polygon, box

def apply_pbr(mesh, color_rgba, metallic=0.75, roughness=0.30):
    """Assign vertex colors and glTF 2.0 PBR material properties."""
    mesh.visual = trimesh.visual.ColorVisuals(mesh=mesh, vertex_colors=color_rgba)
    mesh.visual.material = trimesh.visual.material.PBRMaterial(
        baseColorFactor=color_rgba,
        metallicFactor=metallic,
        roughnessFactor=roughness
    )
    return mesh

def make_pipe(r_in, r_out, height, sections=48):
    """Create watertight cylindrical pipe using annulus extrusion."""
    return trimesh.creation.annulus(r_min=r_in, r_max=r_out, height=height, sections=sections)

def make_half_pipe(r_in, r_out, height, sections=48):
    """Generate exact watertight half cylindrical shell (pi to 2*pi)."""
    thetas = np.linspace(np.pi, 2 * np.pi, sections)
    verts = []
    faces = []
    z0 = -height / 2.0
    z1 = height / 2.0
    N = sections
    
    # 4 rings of vertices
    for th in thetas:
        verts.append([r_out * np.cos(th), r_out * np.sin(th), z0])
    for th in thetas:
        verts.append([r_out * np.cos(th), r_out * np.sin(th), z1])
    for th in thetas:
        verts.append([r_in * np.cos(th), r_in * np.sin(th), z1])
    for th in thetas:
        verts.append([r_in * np.cos(th), r_in * np.sin(th), z0])
        
    for i in range(N - 1):
        faces.append([i, i + 1, N + i + 1])
        faces.append([i, N + i + 1, N + i])
    for i in range(N - 1):
        faces.append([N + i, N + i + 1, 2*N + i + 1])
        faces.append([N + i, 2*N + i + 1, 2*N + i])
    for i in range(N - 1):
        faces.append([2*N + i, 2*N + i + 1, 3*N + i + 1])
        faces.append([2*N + i, 3*N + i + 1, 3*N + i])
    for i in range(N - 1):
        faces.append([3*N + i, 3*N + i + 1, i + 1])
        faces.append([3*N + i, i + 1, i])
        
    # End caps
    faces.append([0, N, 2*N])
    faces.append([0, 2*N, 3*N])
    faces.append([N-1, 4*N-1, 3*N-1])
    faces.append([N-1, 3*N-1, 2*N-1])
    
    mesh = trimesh.Trimesh(vertices=verts, faces=faces, process=True)
    return mesh

def make_half_disk(radius, height, sections=64):
    """Watertight half cylinder disc (y <= 0)."""
    thetas = np.linspace(np.pi, 2 * np.pi, sections)
    pts = list(np.column_stack([radius * np.cos(thetas), radius * np.sin(thetas)]))
    pts.append([-radius, 0.0])
    poly = Polygon(pts)
    return trimesh.creation.extrude_polygon(poly, height=height)

def make_flange_with_bolts(r_flange, r_pipe, t_flange, bolt_circle_r, num_bolts, bolt_r, sections=48, cutaway=False):
    """Watertight flange disc with raised face and 3D bolt studs."""
    if cutaway:
        thetas = np.linspace(np.pi, 2 * np.pi, sections)
        c_out = Polygon(np.column_stack([r_flange * np.cos(thetas), r_flange * np.sin(thetas)]))
        c_in = Polygon(np.column_stack([r_pipe * np.cos(thetas), r_pipe * np.sin(thetas)]))
        ann_pts = list(np.column_stack([r_flange * np.cos(thetas), r_flange * np.sin(thetas)]))
        ann_pts.extend(list(np.column_stack([r_pipe * np.cos(thetas[::-1]), r_pipe * np.sin(thetas[::-1])])))
        poly = Polygon(ann_pts)
        flange = trimesh.creation.extrude_polygon(poly, height=t_flange)
    else:
        flange = trimesh.creation.annulus(r_min=r_pipe, r_max=r_flange, height=t_flange, sections=sections)
    
    # Generate bolt studs
    studs = []
    stud_len = t_flange * 1.3
    stud_r = bolt_r * 0.85
    for i in range(num_bolts):
        theta = 2.0 * np.pi * i / num_bolts
        bx = bolt_circle_r * np.cos(theta)
        by = bolt_circle_r * np.sin(theta)
        if cutaway and by > 0.01:
            continue
        stud = trimesh.creation.cylinder(radius=stud_r, height=stud_len, sections=12)
        stud.apply_translation([bx, by, 0])
        studs.append(stud)
        
    combined = trimesh.util.concatenate([flange] + studs)
    return combined

def make_ellipsoidal_head(r_shell, height, thickness, sections=48, cutaway=False):
    """ASME 2:1 Ellipsoidal Head with uniform thickness and straight flange."""
    Ri = r_shell
    Ro = r_shell + thickness
    Hi = height
    Ho = height + thickness
    
    r_curve = np.linspace(0.0, 1.0, 20)
    z_outer = Ho * np.sqrt(np.maximum(0.0, 1.0 - r_curve**2))
    r_outer = Ro * r_curve
    z_inner = Hi * np.sqrt(np.maximum(0.0, 1.0 - r_curve**2))
    r_inner = Ri * r_curve
    
    linestring = []
    # Start at top center inner (0, Hi)
    for r, z in zip(r_inner, z_inner):
        linestring.append([r, z])
    # Straight flange down
    linestring.append([Ri, -0.05])
    linestring.append([Ro, -0.05])
    # Outer curve back up to apex
    for r, z in zip(reversed(r_outer), reversed(z_outer)):
        linestring.append([r, z])
    # Close profile at apex
    linestring.append([0.0, Hi])
    linestring = np.array(linestring)
    
    if cutaway:
        # Revolve 180 degrees (from 0 to pi), then rotate to align with y <= 0
        half_head = trimesh.creation.revolve(linestring, angle=np.pi, cap=True, sections=sections)
        rot_z = trimesh.transformations.rotation_matrix(np.pi, [0, 0, 1])
        half_head.apply_transform(rot_z)
        return half_head
    else:
        return trimesh.creation.revolve(linestring, sections=sections)

def build_reactor_model(cutaway=False):
    print(f"Building R-201 3D CAD B-Rep Model (Cutaway={cutaway})...")
    
    # Dimensions (meters)
    Ds = 2.1336         # 84.0 in ID
    ts = 0.028575       # 1.125 in (SA-516 Gr 70)
    Rs_in = Ds / 2.0
    Rs_out = Rs_in + ts
    L_shell = 9.144     # 30.0 ft
    H_head = 0.5334     # 21.0 in (2:1 head)
    
    H_skirt = 2.4384    # 8.0 ft
    t_skirt = 0.01905   # 0.75 in
    R_skirt = Rs_out
    
    parts = []
    
    # 1. Shell Body
    if cutaway:
        shell = make_half_pipe(Rs_in, Rs_out, L_shell, sections=64)
    else:
        shell = make_pipe(Rs_in, Rs_out, L_shell, sections=64)
    shell.apply_translation([0, 0, L_shell / 2.0])
    apply_pbr(shell, [42, 54, 69, 255], metallic=0.85, roughness=0.25) # Deep slate midnight steel
    parts.append(shell)
    
    # 2. Skirt Support
    if cutaway:
        skirt = make_half_pipe(R_skirt - t_skirt, R_skirt, H_skirt, sections=48)
    else:
        skirt = make_pipe(R_skirt - t_skirt, R_skirt, H_skirt, sections=48)
    skirt.apply_translation([0, 0, -H_skirt / 2.0])
    apply_pbr(skirt, [33, 37, 41, 255], metallic=0.55, roughness=0.65) # Structural dark iron
    parts.append(skirt)
    
    # Base Ring with 24 Anchor Bolt Assemblies
    R_base_out = R_skirt + 0.2032  # 8.0 in wider
    base_ring = make_flange_with_bolts(
        r_flange=R_base_out,
        r_pipe=R_skirt - t_skirt,
        t_flange=0.0381,
        bolt_circle_r=R_skirt + 0.0984,
        num_bolts=24,
        bolt_r=0.0222,
        sections=48,
        cutaway=cutaway
    )
    base_ring.apply_translation([0, 0, -H_skirt + 0.0381 / 2.0])
    apply_pbr(base_ring, [40, 45, 52, 255], metallic=0.65, roughness=0.50)
    parts.append(base_ring)
    
    # 3. Upper & Lower Tubesheets (Forged SA-266 Cl 2, 3.75 in thick)
    t_ts = 0.09525 # 3.75 in
    if cutaway:
        ts_upper = make_half_disk(radius=Rs_in, height=t_ts, sections=64)
        ts_lower = make_half_disk(radius=Rs_in, height=t_ts, sections=64)
    else:
        ts_upper = trimesh.creation.cylinder(radius=Rs_in, height=t_ts, sections=64)
        ts_lower = trimesh.creation.cylinder(radius=Rs_in, height=t_ts, sections=64)
        
    ts_upper.apply_translation([0, 0, L_shell - t_ts / 2.0])
    apply_pbr(ts_upper, [208, 213, 221, 255], metallic=0.88, roughness=0.22)
    parts.append(ts_upper)
    
    ts_lower.apply_translation([0, 0, t_ts / 2.0])
    apply_pbr(ts_lower, [208, 213, 221, 255], metallic=0.88, roughness=0.22)
    parts.append(ts_lower)
    
    # 4. Schedule 80 Catalyst Tubes (1,021 Tubes, Pt = 2.375 in, Triangular Pitch)
    Pt = 0.060325           # 2.375 in pitch
    r_tube = 0.04826 / 2.0  # 1.900 in OD / 2 = 0.02413 m
    otl = 2.06375 / 2.0     # OTL = 81.25 in / 2 = 1.031875 m
    
    tube_centers = []
    n_rows = 40
    for row in range(-n_rows, n_rows + 1):
        y = row * Pt * (np.sqrt(3) / 2.0)
        x_offset = (row % 2) * (Pt / 2.0)
        for col in range(-n_rows, n_rows + 1):
            x = col * Pt + x_offset
            dist = np.hypot(x, y)
            if dist + r_tube <= otl:
                tube_centers.append((x, y))
                
    print(f"Computed {len(tube_centers)} exact tube coordinates inside OTL {otl*2*39.3701:.2f} in.")
    
    # High fidelity bundle generation
    if cutaway:
        # Render high-density internal bundle (only in y <= 0 to reveal cutaway)
        tubes_to_render = [(tx, ty) for (tx, ty) in tube_centers if ty <= 0.005]
        # To maintain crisp performance with 500+ tubes, take every 2nd tube or full bundle
        tubes_to_render = tubes_to_render[::2]
    else:
        # Exterior view: outer perimeter tubes visible through nozzles/end views
        tubes_to_render = [tc for tc in tube_centers if np.hypot(tc[0], tc[1]) > otl * 0.7][::4]
        
    tube_meshes = []
    L_tube = L_shell - t_ts * 2.0
    for tx, ty in tubes_to_render:
        tube = trimesh.creation.cylinder(radius=r_tube, height=L_tube, sections=12)
        tube.apply_translation([tx, ty, L_shell / 2.0])
        tube_meshes.append(tube)
        
    if tube_meshes:
        combined_tubes = trimesh.util.concatenate(tube_meshes)
        apply_pbr(combined_tubes, [232, 236, 240, 255], metallic=0.95, roughness=0.15) # SA-213 TP304 Stainless
        parts.append(combined_tubes)
        
    # 5. Segmental Baffles (9 Transverse Baffles, 20% Cut, Alternating)
    num_baffles = 9
    baffle_spacing = L_shell / (num_baffles + 1)
    b_thickness = 0.0127 # 0.50 in
    r_baffle = Rs_in - 0.00635
    
    # Circle polygon for baffle
    thetas_b = np.linspace(0, 2 * np.pi, 64, endpoint=False)
    circle_pts = np.column_stack([r_baffle * np.cos(thetas_b), r_baffle * np.sin(thetas_b)])
    circle_poly = Polygon(circle_pts)
    
    for i in range(1, num_baffles + 1):
        bz = i * baffle_spacing
        cut_dir = 1.0 if (i % 2 == 1) else -1.0
        
        # 20% cut: cut box at y > 0.6 * r_baffle or y < -0.6 * r_baffle
        if cut_dir > 0:
            c_box = box(-r_baffle * 1.5, 0.6 * r_baffle, r_baffle * 1.5, r_baffle * 1.5)
        else:
            c_box = box(-r_baffle * 1.5, -r_baffle * 1.5, r_baffle * 1.5, -0.6 * r_baffle)
            
        b_poly = circle_poly.difference(c_box)
        
        if cutaway:
            # Slice in half along y=0
            half_box = box(-r_baffle * 1.5, 0.0, r_baffle * 1.5, r_baffle * 1.5)
            b_poly = b_poly.difference(half_box)
            
        if not b_poly.is_empty:
            b_mesh = trimesh.creation.extrude_polygon(b_poly, height=b_thickness)
            b_mesh.apply_translation([0, 0, bz])
            apply_pbr(b_mesh, [136, 146, 154, 255], metallic=0.70, roughness=0.38)
            parts.append(b_mesh)
            
    # 6. Top & Bottom ASME 2:1 Ellipsoidal Heads
    # Top Head
    head_top = make_ellipsoidal_head(Rs_in, H_head, ts, sections=48, cutaway=cutaway)
    head_top.apply_translation([0, 0, L_shell])
    apply_pbr(head_top, [42, 54, 69, 255], metallic=0.85, roughness=0.25)
    parts.append(head_top)
    
    # Bottom Head (inverted)
    head_bot = make_ellipsoidal_head(Rs_in, H_head, ts, sections=48, cutaway=cutaway)
    rot_x_180 = trimesh.transformations.rotation_matrix(np.pi, [1, 0, 0])
    head_bot.apply_transform(rot_x_180)
    if cutaway:
        rot_z_180 = trimesh.transformations.rotation_matrix(np.pi, [0, 0, 1])
        head_bot.apply_transform(rot_z_180)
    apply_pbr(head_bot, [42, 54, 69, 255], metallic=0.85, roughness=0.25)
    parts.append(head_bot)
    
    # 7. ASME B16.5 Class 300 Flanged Nozzles
    # N1: Feed Gas Inlet 16" (Top Head Apex)
    r_n1 = 0.4064 / 2.0   # 16.0 in OD / 2
    r_n1_in = 0.381 / 2.0 # 15.0 in ID / 2
    l_n1 = 0.500
    n1_pipe = make_pipe(r_n1_in, r_n1, l_n1, sections=36)
    n1_pipe.apply_translation([0, 0, L_shell + H_head + l_n1 / 2.0])
    apply_pbr(n1_pipe, [176, 184, 192, 255], metallic=0.85, roughness=0.25)
    parts.append(n1_pipe)
    
    n1_flange = make_flange_with_bolts(
        r_flange=0.6477 / 2.0,
        r_pipe=r_n1_in,
        t_flange=0.0889,
        bolt_circle_r=0.5715 / 2.0,
        num_bolts=20,
        bolt_r=0.0175,
        sections=36
    )
    n1_flange.apply_translation([0, 0, L_shell + H_head + l_n1 + 0.0889 / 2.0])
    apply_pbr(n1_flange, [190, 198, 206, 255], metallic=0.90, roughness=0.20)
    parts.append(n1_flange)
    
    # N2: Product Gas Outlet 16" (Bottom Head Apex)
    n2_pipe = make_pipe(r_n1_in, r_n1, l_n1, sections=36)
    n2_pipe.apply_translation([0, 0, -H_head - l_n1 / 2.0])
    apply_pbr(n2_pipe, [176, 184, 192, 255], metallic=0.85, roughness=0.25)
    parts.append(n2_pipe)
    
    n2_flange = make_flange_with_bolts(
        r_flange=0.6477 / 2.0,
        r_pipe=r_n1_in,
        t_flange=0.0889,
        bolt_circle_r=0.5715 / 2.0,
        num_bolts=20,
        bolt_r=0.0175,
        sections=36
    )
    n2_flange.apply_translation([0, 0, -H_head - l_n1 - 0.0889 / 2.0])
    apply_pbr(n2_flange, [190, 198, 206, 255], metallic=0.90, roughness=0.20)
    parts.append(n2_flange)
    
    # N3: Dowtherm A Coolant Inlet 10" (Side, Lower Shell Z = 0.85m)
    r_n3 = 0.27305 / 2.0  # 10.75 in OD / 2
    r_n3_in = 0.2545 / 2.0
    l_n3 = 0.450
    rot_y_90 = trimesh.transformations.rotation_matrix(np.pi / 2.0, [0, 1, 0])
    
    n3_pipe = make_pipe(r_n3_in, r_n3, l_n3, sections=32)
    n3_pipe.apply_transform(rot_y_90)
    n3_pipe.apply_translation([Rs_out + l_n3 / 2.0, 0, 0.85])
    apply_pbr(n3_pipe, [0, 137, 123, 255], metallic=0.80, roughness=0.25) # Dowtherm teal
    parts.append(n3_pipe)
    
    n3_flange = make_flange_with_bolts(
        r_flange=0.4445 / 2.0,
        r_pipe=r_n3_in,
        t_flange=0.0635,
        bolt_circle_r=0.38735 / 2.0,
        num_bolts=16,
        bolt_r=0.015,
        sections=32
    )
    n3_flange.apply_transform(rot_y_90)
    n3_flange.apply_translation([Rs_out + l_n3 + 0.0635 / 2.0, 0, 0.85])
    apply_pbr(n3_flange, [190, 198, 206, 255], metallic=0.90, roughness=0.20)
    parts.append(n3_flange)
    
    # N4: Dowtherm A Coolant Outlet 10" (Side, Upper Shell Z = 8.30m, 180 deg opposite)
    n4_pipe = make_pipe(r_n3_in, r_n3, l_n3, sections=32)
    n4_pipe.apply_transform(rot_y_90)
    n4_pipe.apply_translation([-Rs_out - l_n3 / 2.0, 0, 8.30])
    apply_pbr(n4_pipe, [0, 137, 123, 255], metallic=0.80, roughness=0.25)
    parts.append(n4_pipe)
    
    n4_flange = make_flange_with_bolts(
        r_flange=0.4445 / 2.0,
        r_pipe=r_n3_in,
        t_flange=0.0635,
        bolt_circle_r=0.38735 / 2.0,
        num_bolts=16,
        bolt_r=0.015,
        sections=32
    )
    n4_flange.apply_transform(rot_y_90)
    n4_flange.apply_translation([-Rs_out - l_n3 - 0.0635 / 2.0, 0, 8.30])
    apply_pbr(n4_flange, [190, 198, 206, 255], metallic=0.90, roughness=0.20)
    parts.append(n4_flange)
    
    # N5: PSV Relief Valve 4" (OSHA Safety Red on Top Channel)
    r_n5 = 0.1143 / 2.0
    r_n5_in = 0.09718 / 2.0
    l_n5 = 0.400
    rot_x_90 = trimesh.transformations.rotation_matrix(np.pi / 2.0, [1, 0, 0])
    
    n5_pipe = make_pipe(r_n5_in, r_n5, l_n5, sections=24)
    n5_pipe.apply_transform(rot_x_90)
    n5_pipe.apply_translation([0, -Rs_out - l_n5 / 2.0, L_shell + 0.35])
    apply_pbr(n5_pipe, [211, 47, 47, 255], metallic=0.40, roughness=0.30) # OSHA Red
    parts.append(n5_pipe)
    
    n5_flange = make_flange_with_bolts(
        r_flange=0.254 / 2.0,
        r_pipe=r_n5_in,
        t_flange=0.0349,
        bolt_circle_r=0.200 / 2.0,
        num_bolts=8,
        bolt_r=0.011,
        sections=24
    )
    n5_flange.apply_transform(rot_x_90)
    n5_flange.apply_translation([0, -Rs_out - l_n5 - 0.0349 / 2.0, L_shell + 0.35])
    apply_pbr(n5_flange, [211, 47, 47, 255], metallic=0.40, roughness=0.30)
    parts.append(n5_flange)
    
    scene = trimesh.Scene(parts)
    return scene

def main():
    out_dir = r"d:\GAMES\zercxes\CAD_Engineering_Drawings\Ethylene_Oxide_Reactor_Drawings\cad\glb"
    os.makedirs(out_dir, exist_ok=True)
    
    print("=" * 70)
    print("R-201 ETHYLENE OXIDE PACKED-BED TUBULAR REACTOR")
    print("PHYSICALLY BASED RENDERING (PBR) GLB MODEL GENERATION")
    print("=" * 70)
    
    # 1. Full Exterior Assembly
    scene_full = build_reactor_model(cutaway=False)
    glb_path_full = os.path.join(out_dir, "R201_Ethylene_Oxide_Reactor_PBR.glb")
    scene_full.export(glb_path_full)
    size_mb = os.path.getsize(glb_path_full) / (1024 * 1024)
    print(f"[SUCCESS] Exported Master Exterior PBR GLB: {glb_path_full} ({size_mb:.2f} MB)")
    
    # 2. Internal Cutaway Assembly
    scene_cut = build_reactor_model(cutaway=True)
    glb_path_cut = os.path.join(out_dir, "R201_Reactor_Cutaway_Internal_PBR.glb")
    scene_cut.export(glb_path_cut)
    size_mb_cut = os.path.getsize(glb_path_cut) / (1024 * 1024)
    print(f"[SUCCESS] Exported Internal Cutaway PBR GLB: {glb_path_cut} ({size_mb_cut:.2f} MB)")
    print("=" * 70)

if __name__ == '__main__':
    main()
