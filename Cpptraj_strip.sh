#!/bin/sh

# create output directory in parent
mkdir -p ../centered_stripped_trajs

for traj in *.dcd; do
  base=$(basename "$traj" .dcd)

  cpptraj << EOF
parm ../step5_input.parm7
trajin $traj 1 last 10
strip :WAT,Cl-,Na+,PA,PC,OL outprefix stripped
trajout ../centered_stripped_trajs/${base}_stripped.dcd
EOF
done

strip.sh (END)

