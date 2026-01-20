#!/bin/bash

echo "start install torch, wait for a minute..."
pip3 install torch-*.whl --force-reinstall --quiet 2> /dev/null
torch_status=$?
if [ ${torch_status} -eq 0 ]; then
    echo "pip3 install torch successfully"
else
    echo "pip3 install torch failed"
fi

echo "start install torch_npu, wait for a minute..."
pip3 install torch_npu*.whl --quiet 2> /dev/null
torch_npu_status=$?
if [ ${torch_npu_status} -eq 0 ]; then
    echo "pip3 install torch_npu successfully"
else
    echo "pip3 install torch_npu failed"
fi