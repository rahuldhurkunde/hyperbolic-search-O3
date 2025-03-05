#!/usr/bin/env python3
import subprocess
import sys
import glob
import shutil
import time

run = sys.argv[1]

if run == 'O1':
    data = 'data/data_O1.ini'
elif run == 'O2' and chunk == '15p':
    data = 'data/data_15p.ini'
elif run == 'O2' and int(chunk) <= 18:
    data = 'data/data_O2_twoifo.ini'
elif run == 'O2' and int(chunk) >= 19:
    data = 'configs/chunk-specific/data_O2.ini'
elif run == 'O3':
    data = 'configs/chunk-specific/{}/data_O3.ini'.format(run)
elif run == 'O3b':
    data = 'configs/chunk-specific/{}/data_O3b.ini'.format(run)
elif run == 'test':
    data = 'data/data_test.ini'


cache = False 

chunk_list = ['1']

for chunk in chunk_list:
	print('Run ', run, 'Chunk', chunk)
	if cache == True:
		cache_file = 'runs/{}/{}/partial_workflow.map'.format(run, chunk)
		print(' \t \t \t CACHE FILE USED ', cache_file, '\n')
		wf_name = 'gwv3'

	elif cache == False:
		print('OG workflow')
		wf_name = 'gw'

	print('CHECK workflow name \t \t ', wf_name, '\n')

	configs = glob.glob("configs/*.ini")
	configs.append("times/gps_times_{}_analysis_{}.ini".format(run, chunk))
	configs.append(data)
	configs.append("configs/chunk-specific/{}/inj_{}_{}.ini".format(run, run, chunk))

	if cache == True:
		outdir = 'runs/{}/{}/{}'.format(run, chunk, wf_name)
	else:
		outdir = 'runs/{}/{}'.format(run, chunk)

	print('Outdir \t', outdir)
	print(configs)

	if cache == True:
		subprocess.run(["pycbc_make_offline_search_workflow",
						"--workflow-name", "{}".format(wf_name),
						"--cache-file", "{}".format(cache_file),
						"--config-overrides", "results_page:output-path:html",
						"--output-dir", "{}".format(outdir),
                                                "--submit-now",
						"--config-files"] + configs,
                                                )
	else:
		subprocess.run(["pycbc_make_offline_search_workflow",
						"--workflow-name", "{}".format(wf_name),
						"--config-overrides", "results_page:output-path:html",
						"--output-dir", "{}".format(outdir),
						"--submit-now",
                                                "--config-files"] + configs,
                                                )
	
	time.sleep(100000)
