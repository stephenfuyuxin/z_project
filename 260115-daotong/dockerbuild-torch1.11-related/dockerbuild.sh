#!/bin/bash

docker build \
--build-arg no_proxy=127.0.0.1,localhost,local,.local,172.17.0.1 \
--build-arg DEVICE=910b \
--build-arg ARCH=aarch64 \
--build-arg CANN_VERSION=8.0.RC2 \
--build-arg PYTHON_VERSION=3.10.12 \
--build-arg PY_VERSION=310 \
--build-arg TORCH_VERSION=1.11.0 \
-t fuyuxin-transfer-ubuntu2204:1 \
--target aisbench .
