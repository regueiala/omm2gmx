# gromacs_centering_from_openmm

Utilities and workflow for converting and centering OpenMM trajectories with GROMACS.

---

## Overview

This repository provides a workflow to:

- Generate `.gro` and `.tpr` files from OpenMM outputs
- Convert OpenMM `.dcd` trajectories into GROMACS-compatible `.xtc`
- Correct periodic boundary condition (PBC) artifacts
- Center the trajectory around a residue or the system center of mass
- Visualize the final trajectory in VMD

---

# Workflow

## 1. Generate `.gro` and `.tpr` files

Run the `paremd` script to generate `.gro` and `.top` files from:

- `system.xml`
- `*.parm7`

Then generate the `.tpr` file with GROMACS:

```bash
gmx grompp -f file.mdp -c structure.gro -p topology.top -o system.tpr
```

---

## 2. Convert the trajectory (`.dcd` → `.xtc`)

Modify and run:

```bash
python3 gromacs.py
```

This converts the OpenMM trajectory into a GROMACS-compatible `.xtc` trajectory.

> **Important**
>
> OpenMM and GROMACS use slightly different box matrix conventions.
>
> OpenMM may contain extremely small floating-point values (e.g. `1e-16`)
> where GROMACS expects exact zeros. These values must be corrected before
> conversion.

---

## 3. Create an index file

Generate the index file:

```bash
gmx make_ndx -f structure.gro -o index.ndx
```

Inside the interactive prompt:

```text
r RESID
```

### Recommendation

For better centering:

1. Compute the system center of mass
2. Select the residue closest to the center

Use:

```bash
python3 center_of_mass.py
```

to identify the best residue.

---

## 4. Remove periodic boundary jumps

```bash
gmx trjconv \
    -s system.tpr \
    -f trj_gromacs.xtc \
    -o trj_nojump.xtc \
    -pbc nojump
```

---

## 5. Center the trajectory

```bash
gmx trjconv \
    -s system.tpr \
    -f trj_nojump.xtc \
    -o trj_center.xtc \
    -pbc mol \
    -center \
    -ur compact \
    -n index.ndx
```

When prompted, select:

1. The centering group (your residue)
2. The output group (`System`)

Example:

```text
21 0
```

---

## 6. Visualize the trajectory

Always load the topology together with the trajectory:

```bash
vmd topology.parm7 trj_center.xtc
```
