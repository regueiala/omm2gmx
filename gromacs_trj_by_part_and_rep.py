import mdtraj as md
import numpy as np
import re 
import glob

for i in range (11,63):
    
    trajs = glob.glob(f"/media/reguei/c02a5532-51e3-4193-b4cf-68db361f6ae6/alaa_MD/pthrp_100ns/pthrp_only_rep{i}/*prod*.dcd")
    trajs.sort(key=lambda x: int(re.search(r'part_(\d+)', x).group(1)) if re.search(r'part_(\d+)', x) else 0)
    print(trajs)
    print(f"Processing trajectory for rep {i}...")
    traj = md.load(trajs, top="step5_input.parm7")
    #traj= traj[0::10] ( if you want)

    # sanitize box vectors
    bv = traj.unitcell_vectors.copy()

    bv[0]
    bv[np.abs(bv) < 1e-5] = 0.0

    traj.unitcell_vectors = bv
    print(f"Saving trajectory for rep {i}...")
    traj.save_xtc(f"pthrp_trj_gromacs_rep{i}.xtc")
