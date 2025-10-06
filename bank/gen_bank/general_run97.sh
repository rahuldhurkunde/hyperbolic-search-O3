#!/bin/bash
export OMP_NUM_THREADS=1
/home/lroy02/miniconda3/envs/hyperbolic/bin/pycbc_brute_bank \
--psd-file /home/lroy02/hyperbolic_encounter/template_bank/l1_psd.txt \
--output-file "$2" \
--input-config "$1" \
--approximant Hyperbolic15PNhphc \
--minimal-match 0.97 \
--tolerance 0.1 \
--sample-rate 2048 \
--low-frequency-cutoff 20.0 \
--tau0-start start-value \
--tau0-end end-value \
--tau0-crawl 2 \
--tau0-threshold 0.5 \
--buffer-length 8 \
--nprocesses 32 \
--verbose
