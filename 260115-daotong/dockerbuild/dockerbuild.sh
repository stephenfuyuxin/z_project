#!/bin/bash

docker build \
--build-arg no_proxy=127.0.0.1,localhost,local,.local,172.17.0.1 \
--build-arg DEVICE=910b \
--build-arg ARCH=aarch64 \
--build-arg CANN_VERSION=8.3.RC2 \
--build-arg PYTHON_VERSION=3.11.6 \
--build-arg PY_VERSION=311 \
--build-arg TORCH_VERSION=2.7.1 \
-t fuyuxin-sam3-ubuntu2204:4 \
--target sam3 .
