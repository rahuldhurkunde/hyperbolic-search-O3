#!/bin/bash

## inputs 
bankfile=$1 

subbank_dir='subbanks_bank_mm099'

mkdir $subbank_dir

pycbc_hdf5_splitbank \
    --bank-file $bankfile \
    --output-prefix splitbank \
    --mchirp-sort \
    --templates-per-bank 100 \

mv splitbank* subbanks_bank_mm099/
