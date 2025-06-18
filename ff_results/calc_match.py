import csv
import h5py as h
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

logging.info('Reading the original bank file: bank_org.hdf')
bank_org = h.File('bank_org.hdf', 'r')

logging.info('Reading the injection file: injections.hdf')
injection = h.File('injections_20000.hdf', 'r')
 
# Define the waveform approximant and other settings
approximant = 'Hyperbolic15PNhphc'
buffer_len = 8
sample_rate = 2048
df = 1.0 / buffer_len
tlen = buffer_len * sample_rate
flen = tlen // 2 + 1
f_low = 20.0

# Load the PSD file
logging.info("Loading PSD file")
psd_filename = 'O4_psd.txt'
psd = pycbc.psd.from_txt(psd_filename, flen, df, f_low, is_asd_file=False)

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
        eccentricity=injection['alpha2'][random_index],
        vmax=injection['alpha'][random_index],
        duration=injection.attrs['alpha1']
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
        'spin1z': injection['spin1z'][random_index],
        'spin2z': injection['spin2z'][random_index],
        'match': best_match
    }

    results_list.append(injection_result)

# Save results to a CSV file
output_file = f"match_results_injections_20000.csv"
df = pd.DataFrame(results_list)
df.to_csv(output_file, index=False)
logging.info(f"Results saved to file: {output_file}")