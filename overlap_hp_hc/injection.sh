#!/bin/sh
pycbc_create_injections --verbose \
        --config-files injection_vmax.ini \
        --ninjections 200000 \
        --output-file injection_vmax.hdf \
        --variable-params-section variable_params \
        --static-params-section static_params \
        --dist-section prior \
        --force
