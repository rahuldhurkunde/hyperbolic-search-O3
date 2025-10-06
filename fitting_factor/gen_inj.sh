#!/bin/bash

pycbc_create_injections --verbose --ninjections 20000 \
    --seed 1000 --output-file injections_20000.hdf \
    --force --config-files config_inj.ini
