if [ -z "$1" ]; then
  echo "Error: No chunk number provided."
  echo "Usage: $0 <chunk_no>"
  exit 1
fi

WORKFLOWNAME=gw
CHUNKNUMBER=$1
DESCRIPTION='initial'

OUTPUTDIR="runs/chunk_${CHUNKNUMBER}_${DESCRIPTION}"

export GWDATAFIND_SERVER='datafind.gw-openscience.org'

echo "Output dir: $OUTPUTDIR"
echo "gwdatafind server: $GWDATAFIND_SERVER"

PYCBC_COMMAND="pycbc_make_offline_search_workflow \\
	--workflow-name $WORKFLOWNAME \\
	--output-dir $OUTPUTDIR \\
	--config-overrides \\
		results_page:output-path:\"/home/${USER}/public_html/hyperbolic_search/testing/a${CHUNKNUMBER}_${DESCRIPTION}\" \\
	--submit-now \\
	--config-file \\
		data_O3b.ini \\
		analysis.ini \\
		chunk-specific/injections_$CHUNKNUMBER.ini \\
		executables.ini \\
		plotting.ini \\
		../times/gps_times_$CHUNKNUMBER.ini"

echo $PYCBC_COMMAND	
eval "$PYCBC_COMMAND"
