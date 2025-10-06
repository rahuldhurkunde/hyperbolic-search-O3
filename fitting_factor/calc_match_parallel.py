#!/usr/bin/env python

import csv
import h5py
import numpy as np
import pandas as pd
import pycbc
from pycbc.psd.read import from_txt
from pycbc.filter import match
import pycbc.waveform
import argparse
import logging
from datetime import datetime
import matplotlib.pyplot as plt

# Configure logging to include timestamps
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Calculate match values for waveforms.")
    parser.add_argument("--bank-file", type=str, required=True, help="Path to the original bank file (HDF format).")
    parser.add_argument("--injection-file", type=str, required=True, help="Path to the injection file (HDF format).")
    parser.add_argument("--psd-file", type=str, required=True, help="Path to the PSD file (TXT format).")
    parser.add_argument("--output-file", type=str, required=True, help="Path to save the output CSV file.")
    return parser.parse_args()

# Parse command-line arguments
args = parse_arguments()
logging.info('Reading the original bank file')
bank_org = h5py.File(args.bank_file,'r')

logging.info('Reading the injection file')
injection =  h5py.File(args.injection_file,'r')

 
# Define the waveform approximant and other settings
approximant = 'Hyperbolic15PNhphc'
buffer_len = 8
sample_rate = 2048
df = 1.0 / buffer_len
tlen = buffer_len * sample_rate
flen = tlen // 2 + 1
f_low = 15.0

# Load the PSD file
logging.info("Loading PSD file")
psd_filename = args.psd_file
psd = pycbc.psd.from_txt(psd_filename, flen, df, f_low, is_asd_file=True)

logging.info('Computing PSD for a fixed duration: 8 s')

# Initialize results list
results_list = []

for random_index in range(len(injection['mass1'])):
    logging.info(f"Processing injection {random_index + 1}/{len(injection['mass1'])}")
    
    injection_waveform, _ = pycbc.waveform.get_fd_waveform(
        approximant=approximant,
        mass1=injection['mass1'][random_index],
        mass2=injection['mass2'][random_index],
        f_lower=f_low,
        delta_f=df,
        spin1x=injection['spin1x'][random_index], spin1y=injection['spin1y'][random_index], spin1z=injection['spin1z'][random_index],
        spin2x=injection['spin2x'][random_index], spin2y=injection['spin2y'][random_index], spin2z=injection['spin2z'][random_index],
        eccentricity=injection['eccentricity'][random_index],
        vmax=injection['vmax'][random_index],
        duration=injection.attrs['duration']
    )

    # Resize waveform to match PSD length
    injection_waveform.resize(len(psd))

    match_values = []

    for i in range(len(bank_org['mass1'])):
        waveform_data, _ = pycbc.waveform.get_fd_waveform(
            mass1=bank_org['mass1'][i],
            mass2=bank_org['mass2'][i],
            approximant=approximant,
            f_lower=f_low,
            delta_f=df,
            spin1x=bank_org['spin1x'][i], spin1y=bank_org['spin1y'][i], spin1z=bank_org['spin1z'][i],
            spin2x=bank_org['spin2x'][i], spin2y=bank_org['spin2y'][i], spin2z=bank_org['spin2z'][i],
            eccentricity=bank_org['eccentricity'][i],
            vmax=bank_org['vmax'][i],
            duration=bank_org['duration'][i]
    )

        waveform_data.resize(len(psd))

        # Compute match
        m, _ = match(waveform_data, injection_waveform, psd=psd, low_frequency_cutoff=f_low)
        match_values.append(m)

        logging.info(f"Template {i + 1}/{len(bank_org['mass1'])}: Match={m:.4f}")

    # Store the best match for this injection
    best_match = max(match_values)
    
    injection_result = {
        'mass1': injection['mass1'][random_index],
        'mass2': injection['mass2'][random_index],
        'spin1x': injection['spin1x'][random_index],
        'spin1y': injection['spin1y'][random_index],
        'spin1z': injection['spin1z'][random_index],
        'spin2x': injection['spin2x'][random_index],
        'spin2y': injection['spin2y'][random_index],
        'spin2z': injection['spin2z'][random_index],
        'spin2z': injection['spin2z'][random_index],
        'eccentricity': injection['eccentricity'][random_index],
        'vmax': injection['vmax'][random_index],
        'match': best_match
    }

    results_list.append(injection_result)

# Save results to a CSV file
output_file = args.output_file
df = pd.DataFrame(results_list)
df.to_csv(output_file, index=False)
logging.info(f"Results saved to file: {output_file}")
