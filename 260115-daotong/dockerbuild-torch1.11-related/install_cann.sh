#!/bin/bash

CANN_TOOKIT="Ascend-cann-toolkit_*_linux-*.run"
CANN_KERNELS="Ascend-cann-kernels-*_*_linux*.run"

chmod +x *.run
yes | ./${CANN_TOOKIT} --install --quiet
toolkit_status=$?
if [ ${toolkit_status} -eq 0 ]; then
    echo "install toolkit successfully"
else
    echo "install toolkit failed with status ${toolkit_status}"
fi

yes | ./${CANN_KERNELS} --install --quiet
kernels_status=$?
if [ ${kernels_status} -eq 0 ]; then
    echo "install kernels successfully"
else
    echo "install kernels failed with status ${kernels_status}"
fi