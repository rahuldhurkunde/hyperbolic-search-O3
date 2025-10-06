# Steps to do ff study

1/ Generate injection.hdf (name could be different) using gen_inj.sh. It takes config_inj.ini (make sure all the prior settings are fine)
2/ Split the bank using splitbank.sh to speed-up the match calculations ; make sure that all the subbanks are saved in a folder called subbanks_bank_mm099 
3/ run make_dagfiles.py to generate *sub and *dag files that will perform match calculations
4/ submit the dag file by condor_submit_dag bank_dag
