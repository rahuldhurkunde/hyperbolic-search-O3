#!/bin/bash
source ~/miniconda3/etc/profile.d/conda.sh
conda activate hyperbolic



PROC=$1
CHUNK=2000   # number of injections per job
START=$(( PROC * CHUNK ))
END=$(( START + CHUNK ))

python3 run_inj.py injection_vmax.hdf $START $END results_vmax_${PROC}.hdf
