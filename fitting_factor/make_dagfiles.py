import numpy as np
import os
import glob
from glue.pipeline import CondorDAGJob, CondorDAGNode, CondorDAG, CondorJob
 
# BASEDIR
RUNDIR = os.getcwd()+'/'

psd = f"{RUNDIR}O4_psd.txt" 
injection = f"{RUNDIR}injections_20000.hdf"
outputmatch = f"{RUNDIR}match_out_20000inj/"

os.makedirs(f"{RUNDIR}logs", exist_ok=True)

arglist = ['--bank-file',
           '--injection-file',
           '--psd-file',
           '--output-file'
          ]

outputfile = '$(outputfile)'
bank = '$(bank)'
psd_file = psd
injection_file = injection

argvars = [bank,
            injection_file,
            psd_file,
            outputfile
          ]

# Define the Condor job
djob = CondorDAGJob('vanilla', f'{RUNDIR}calc_match_parallel.py')
djob.add_condor_cmd('getenv', 'True')
djob.add_condor_cmd('should_transfer_files', 'YES')
djob.add_condor_cmd('when_to_transfer_output', 'ON_EXIT')
djob.add_condor_cmd('request_memory','1GB')

djob.set_sub_file(f'{RUNDIR}bank.sub')

d = CondorDAG(f'{RUNDIR}bank_toplog')
d.set_dag_file(f'{RUNDIR}bank_dag')


for al, av in zip(arglist, argvars):
    djob.add_arg(f'{al} {av}')
 
def write_node(index):
    node = djob.create_node()
    outf = outputmatch+f"match_{index}.csv"
    node.add_macro('bank', RUNDIR+f'subbanks_bank_mm099/splitbank{index}.hdf') 
    node.add_macro('outputfile', outf) 
    d.add_node(node)

    djob.set_log_file('logs/bank_log_'+'.$(Cluster).$(Process).log')
    djob.set_stderr_file('logs/bank_error_'+'.$(Cluster).$(Process).err')
    djob.set_stdout_file('logs/bank_out_'+'.$(Cluster).$(Process).out')


for i in range(100):  # Assuming 100 sub-banks named splitbank0.hdf to splitbank99.hdf
    write_node(i)


d.write_sub_files()
d.write_dag()
