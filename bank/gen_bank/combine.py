import h5py, glob, numpy as np

files = sorted(glob.glob("bank99*.hdf"))
keys_to_merge = ['approximant', 'duration', 'eccentricity', 'f_lower', 'mass1', 'mass2', 'spin1_a', 'spin1_azimuthal', 'spin1_polar', 'spin1x', 'spin1y', 'spin1z', 'spin2_a', 'spin2_azimuthal', 'spin2_polar', 'spin2x', 'spin2y', 'spin2z', 'vmax']

with h5py.File("combine_bank99.hdf", "w") as fout:
    grp = fout.create_group("results")

    # initialize lists to collect data
    collected = {k: [] for k in keys_to_merge}

    for f in files:
        with h5py.File(f, "r") as fin:
            for k in keys_to_merge:
                collected[k].append(fin[k][()])  # grab numpy array

    # concatenate and save
    for k in keys_to_merge:
        data = np.concatenate(collected[k])
        grp.create_dataset(k, data=data)
