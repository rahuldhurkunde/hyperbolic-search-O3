import h5py
import sys
import numpy as np
from pycbc.filter.matchedfilter import overlap
from pycbc.psd import aLIGOZeroDetHighPower
import pycbc.waveform
from pycbc.filter.matchedfilter import match
from pycbc.filter.matchedfilter import compute_max_snr_over_sky_loc_stat_no_phase

# sys reads the command line arguements
injfile = sys.argv[1]   # e.g. injection.hdf
start   = int(sys.argv[2]) #e.g. 0
end     = int(sys.argv[3]) #e.g. 1000
outfile = sys.argv[4] #e.g. inj.hdf for 0 to 100 injections out of 100k total injections

f_low = 15

with h5py.File(injfile, "r") as f:
    # Load only a chunk
    total = len(f["mass1"])
    idx = np.arange(start, min(end, total))
    # lists to hold results
    m1s, m2s, s1_a, s2_a, s1_az, s2_az, s1_p, s2_p, eccs, vmaxs, coa_p, ovs, m_list, m_filter_list = [], [], [], [], [], [], [], [], [], [], [], [], [], []
    for i in idx:
        m1 = f["mass1"][i]
        m2 = f["mass2"][i]
        spin1_a = f["spin1_a"][i]
        spin2_a = f["spin2_a"][i]
        spin1_azimuthal = f["spin1_azimuthal"][i]
        spin2_azimuthal = f["spin2_azimuthal"][i]
        spin1_polar = f["spin1_polar"][i]
        spin2_polar = f["spin2_polar"][i]
        ecc = f["eccentricity"][i]
        vmax = f["alpha"][i]
        coa_phase = f["coa_phase"][i]

        hp, hc = pycbc.waveform.get_td_waveform(
            approximant="Hyperbolic15PNhphc",
            mass1=m1, mass2=m2, spin1_a=spin1_a, spin2_a=spin2_a,
            spin1_azimuthal=spin1_azimuthal, spin2_azimuthal=spin2_azimuthal, spin1_polar=spin1_polar, spin2_polar=spin2_polar,
            eccentricity=ecc, alpha=vmax, coa_phase=coa_phase,
            f_lower=15, delta_t=1/4096, alpha1 = 8
        )
       # Resize the waveforms to the same length
        tlen = max(len(hp), len(hc))
        hp.resize(tlen)
        hc.resize(tlen)
        
        # Generate the aLIGO ZDHP PSD
        delta_f = 1.0 / hp.duration
        flen = tlen//2 + 1
        psd = aLIGOZeroDetHighPower(flen, delta_f, f_low)

    # calculate overlap between hp and hc
        ov = overlap(hp, hc, psd=psd, low_frequency_cutoff=f_low, normalized=True)
        Re_ov = np.real(overlap(hp, hc, psd=psd, low_frequency_cutoff=f_low, normalized=True))
        m, i = match(hp, hc, psd=psd, low_frequency_cutoff=f_low)
        #norm_hp = np.sqrt(np.vdot(hp.numpy(), hp.numpy()).real)
        #norm_hc = np.sqrt(np.vdot(hc.numpy(), hc.numpy()).real)
        #m_filter = compute_max_snr_over_sky_loc_stat_no_phase(hp, hc, hphccorr=Re_ov, hpnorm=norm_hp, hcnorm=norm_hc)

        
       # collect results
        m1s.append(m1)
        m2s.append(m2)
        s1_a.append(spin1_a)
        s2_a.append(spin2_a)
        s1_az.append(spin1_azimuthal)
        s2_az.append(spin2_azimuthal)
        s1_p.append(spin1_polar)
        s2_p.append(spin2_polar)
        eccs.append(ecc)
        vmaxs.append(vmax)
        coa_p.append(coa_phase)
        ovs.append(ov)
        m_list.append(m)
        #m_filter_list.append(m_filter)
# Save results
with h5py.File(outfile, "w") as f_out:
    f_out.create_dataset("mass1", data=np.array(m1s))
    f_out.create_dataset("mass2", data=np.array(m2s))
    f_out.create_dataset("spin1_a", data=np.array(s1_a))
    f_out.create_dataset("spin2_a", data=np.array(s2_a))
    f_out.create_dataset("spin1_azimuthal", data=np.array(s1_az))
    f_out.create_dataset("spin2_azimuthal", data=np.array(s2_az))
    f_out.create_dataset("spin1_polar", data=np.array(s1_p))
    f_out.create_dataset("spin2_polar", data=np.array(s2_p))
    f_out.create_dataset("eccentricity", data=np.array(eccs))
    f_out.create_dataset("vmax", data=np.array(vmaxs))
    f_out.create_dataset("coa_phase", data=np.array(coa_p))
    f_out.create_dataset("overlap", data=np.array(ovs))
    f_out.create_dataset("match", data=np.array(m_list))
    #f_out.create_dataset("match_max_Pol", data=np.array(m_filter_list))
