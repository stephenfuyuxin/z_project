# 参考链接
## vllm-ascend 支持 Qwen3-VL
昇腾 0day 支持 Qwen3-VL-30B-A3B 模型适配：https://mp.weixin.qq.com/s/hnQsDl1qlx2F6ElhTd1gDg

## vllm-ascend 支持 Qwen3-Next
Multi-NPU (Qwen3-Next)：https://vllm-ascend.readthedocs.io/zh-cn/latest/tutorials/multi_npu_qwen3_next.html#

# vllm-ascend 支持 Qwen3-VL-30B-A3B
这里采用 vLLM Ascend 镜像的方式，在昇腾上运行 Qwen3-VL-30B-A3B-Instruct 模型，

## 镜像信息
镜像仓：quay.io/ascend/vllm-ascend:v0.11.0rc0

镜像链接：https://quay.io/repository/ascend/vllm-ascend?tab=tags

## docker run 启动
这里，直接贴原链接中的启动命令，实际使用 aispace 加载镜像启动，
```shell
# Update the vllm-ascend image
export IMAGE=quay.io/ascend/vllm-ascend:v0.11.0rc0
docker run --rm \
--name vllm-ascend \
--device /dev/davinci0 \
--device /dev/davinci_manager \
--device /dev/devmm_svm \
--device /dev/hisi_hdc \
-v /usr/local/dcmi:/usr/local/dcmi \
-v /usr/local/bin/npu-smi:/usr/local/bin/npu-smi \
-v /usr/local/Ascend/driver/lib64/:/usr/local/Ascend/driver/lib64/ \
-v /usr/local/Ascend/driver/version.info:/usr/local/Ascend/driver/version.info \
-v /etc/ascend_install.info:/etc/ascend_install.info \
-v /root/.cache:/root/.cache \
-p 8000:8000 \
-e VLLM_USE_MODELSCOPE=True \
-e PYTORCH_NPU_ALLOC_CONF=max_split_size_mb:256 \
-it $IMAGE \
vllm serve Qwen/Qwen3-VL-30B-A3B-Instruct \
--served-model-name qwen3vl \
--dtype bfloat16 \
--max_model_len 16384 \
--max-num-batched-tokens 16384 \
--tensor-parallel-size 2 \
--enable_expert_parallel
```
若是 aispace 启动，则导入镜像和模型权重、创建在线服务（导入/创建过程不表述），启动命令为，
```shell
vllm server /the/path/of/modelweigh --port 8000 --served-model-name qwen3vl --dtype bfloat16 --max_model_len 16384 --max-num-batched-tokens 16384 --tensor-parallel-size 2 --enable_expert_parallel
```
如果使用默认的权重路径，有个默认路径 `/usr/local/serving/models`，可以填充 `/the/path/of/modelweigh` 这段，

## 环境变量设置
这里，直接贴原链接中的环境变量，实际使用 aispace 加载镜像启动，这部分已经通过 dockerfile 固化到自定义镜像中，
```shell
# 从 ModelScope 加载模型来加速下载
export VLLM_USE_MODELSCOPE=True
# 设置 `max_split_size_mb` 来减少内存碎片
export PYTORCH_NPU_ALLOC_CONF=max_split_size_mb:256
```

## 推理服务化
如果推理服务化启动成功，会打印以下信息，
```shell
INFO: Started server process [44610]
INFO: Waiting for application startup.
INFO: Application startup complete.
```

推理服务化启动成功之后，通过提示词来验证功能，通过 `image_url` 的方式需要能连接外网，
```shell
curl http://localhost:8000/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
    "model": "qwen3vl",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://modelscope.oss-cn-beijing.aliyuncs.com/resource/qwen.png"
                    }
                },
                {
                    "type": "text",
                    "text": "What is the text in the illustrate?"
                }
            ]
        }
    ]
}'
```

若推理服务化正常响应，则会在服务端打印如下日志信息，
```shell
INFO: x.x.x.x:x - "POST /v1/chat/completions HTTP/1.1" 200 OK
INFO xx-xx xx:xx:xx [loggers.py:123] Engine 000: Avg prompt throughput: 6.5 tokens/s, Avg generation throughput: 0.7 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 0.0%
INFO xx-xx xx:xx:xx [loggers.py:123] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 0.0 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 0.0%
```

服务端侧会打印推理结果，
```json
{"id":"chatcmpl-7d35682041384faeb147660c93bd13f8","object":"chat.completion","created":1758627832,"model":"qwen3vl","choices":[{"index":0,"message":{"role":"assistant","content":"TONGYI Qwen","refusal":null,"annotations":null,"audio":null,"function_call":null,"tool_calls":[],"reasoning_content":null},"logprobs":null,"finish_reason":"stop","stop_reason":null,"token_ids":null}],"service_tier":null,"system_fingerprint":null,"usage":{"prompt_tokens":65,"total_tokens":72,"completion_tokens":7,"prompt_tokens_details":null},"prompt_logprobs":null,"prompt_token_ids":null,"kv_transfer_params":null}
```

## 附- dockerfile
通过自定义构建，固化额外的环境变量，以及更新原有镜像的 `transformers` 版本，Qwen3-VL 官方要求版本为 4.57.0 且当前仅支持源码方式安装，暂未 release 不支持 .whl 形式，

参考链接：https://modelscope.cn/models/Qwen/Qwen3-VL-30B-A3B-Instruct
```shell
Quickstart
Below, we provide simple examples to show how to use Qwen3-VL with 🤖 ModelScope and 🤗 Transformers.

The code of Qwen3-VL has been in the latest Hugging Face transformers and we advise you to build from source with command:

pip install git+https://github.com/huggingface/transformers
# pip install transformers==4.57.0 # currently, V4.57.0 is not released
```

以下为 dockerfile 文件，
```dockerfile
FROM quay.io/ascend/vllm-ascend:v0.11.0rc0 AS base
LABEL maintainer="fuyuxin"

ENV VLLM_USE_MODELSCOPE=True \
    PYTORCH_NPU_ALLOC_CONF=max_split_size_mb:256

RUN wget -q http://172.17.0.1:3000/transformers-4.57.0.tar.gz -P . && \
    tar -xzvf transformers-4.57.0.tar.gz && \
    cd transformers-4.57.0 && \
    pip install . && \
    pip cache purge && \
    rm -rf ~/.cache/pip && \
    cd .. && \
    rm -rf transformers-4.57.0 transformers-4.57.0.tar.gz
```

# vllm-ascend 支持 Qwen3-Next-80B-A3B
这里采用 vLLM Ascend 镜像的方式，在昇腾上运行 Qwen3-Next-80B-A3B-Instruct 模型，

## 镜像信息
镜像仓：quay.io/ascend/vllm-ascend:v0.11.0rc0

镜像链接：https://quay.io/repository/ascend/vllm-ascend?tab=tags

## docker run 启动
这里，直接贴原链接中的启动命令，实际使用 aispace 加载镜像启动，
```shell
# Update the vllm-ascend image
export IMAGE=quay.io/ascend/vllm-ascend:v0.11.0rc0
docker run --rm \
--shm-size=1g \
--name vllm-ascend-qwen3 \
--device /dev/davinci0 \
--device /dev/davinci1 \
--device /dev/davinci2 \
--device /dev/davinci3 \
--device /dev/davinci_manager \
--device /dev/devmm_svm \
--device /dev/hisi_hdc \
-v /usr/local/dcmi:/usr/local/dcmi \
-v /usr/local/bin/npu-smi:/usr/local/bin/npu-smi \
-v /usr/local/Ascend/driver/lib64/:/usr/local/Ascend/driver/lib64/ \
-v /usr/local/Ascend/driver/version.info:/usr/local/Ascend/driver/version.info \
-v /etc/ascend_install.info:/etc/ascend_install.info \
-v /root/.cache:/root/.cache \
-p 8000:8000 \
-it $IMAGE bash
```
若是 aispace 启动，则导入镜像和模型权重、创建在线服务（导入/创建过程不表述），启动命令为，
```shell
vllm server /the/path/of/modelweigh --port 8000 --served-model-name qwen3next --tensor-parallel-size 4 --max_model_len 4096 --gpu-memory-utilization 0.7 --enforce-eager
```
如果使用默认的权重路径，有个默认路径 `/usr/local/serving/models`，可以填充 `/the/path/of/modelweigh` 这段，另外，当前最大仅支持 <16K 的最大输入输出总长度，所以设置为 14K 比较合理，gpu利用率这个指标 0.9 会 oom，0.8 可以正常拉起，

## 环境变量设置
这里，直接贴原链接中的环境变量，实际使用 aispace 加载镜像启动，这部分已经通过 dockerfile 固化到自定义镜像中，
```shell
# Load model from ModelScope to speed up download
export VLLM_USE_MODELSCOPE=True
```

## 原镜像变更操作
两部分，变更 bisheng 编译器编译的 toolkit 包，以及变更 triton ascend 包，这部分已经通过 dockerfile 固化到自定义镜像中，

### bisheng toolkit
额外环境变量设置固化到镜像中，在 k8s 平台上使用启动为 pod 时不会默认加载 ~/.bashrc 文件，会导致推理响应请求时报错，
```shell
wget https://vllm-ascend.obs.cn-north-4.myhuaweicloud.com/vllm-ascend/Ascend-BiSheng-toolkit_aarch64.run
chmod a+x Ascend-BiSheng-toolkit_aarch64.run
./Ascend-BiSheng-toolkit_aarch64.run --install
source /usr/local/Ascend/8.3.RC1/bisheng_toolkit/set_env.sh
```

### triton ascend
```shell
wget https://vllm-ascend.obs.cn-north-4.myhuaweicloud.com/vllm-ascend/triton_ascend-3.2.0.dev20250914-cp311-cp311-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl
pip install triton_ascend-3.2.0.dev20250914-cp311-cp311-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl
```

## 推理服务化
如果推理服务化启动成功，会打印以下信息，
```shell
INFO: Started server process [44610]
INFO: Waiting for application startup.
INFO: Application startup complete.
```

推理服务化启动成功之后，通过提示词来验证功能，推理后处理参数可加可不加，
```shell
curl http://localhost:8000/v1/chat/completions -H "Content-Type: application/json" -d '{
  "model": "/usr/local/serving/models",
  "messages": [
    {"role": "user", "content": "Who are you?"}
  ],
  "temperature": 0.6,
  "top_p": 0.95,
  "top_k": 20,
  "max_tokens": 32
}'
```

## 附- dockerfile
通过自定义构建，固化额外的环境变量，固化 toolkit 和 triton 的变更，另外将 patch_mamba_config.py 脚本变更也做进去，否则推理服务化拉不起来，参考 README.md 同级目录下的文件，
```dockerfile
FROM quay.io/ascend/vllm-ascend:v0.11.0rc0 AS base
LABEL maintainer="fuyuxin"

ENV VLLM_USE_MODELSCOPE=True

RUN wget -q http://172.17.0.1:3000/Ascend-BiSheng-toolkit_aarch64.run -P . && \
    chmod a+x Ascend-BiSheng-toolkit_aarch64.run && \
    ./Ascend-BiSheng-toolkit_aarch64.run --install && \
    wget -q http://172.17.0.1:3000/env.sh -P . && \
    bash env.sh && \
    wget -q http://172.17.0.1:3000/triton_ascend-3.2.0.dev20250914-cp311-cp311-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl -P . && \
    pip install triton_ascend-3.2.0.dev20250914-cp311-cp311-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl && \
    rm -rf Ascend-BiSheng-toolkit_aarch64.run env.sh triton_ascend-3.2.0.dev20250914-cp311-cp311-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl && \
    pip cache purge && \
    rm -rf ~/.cache/pip && \
    wget -q http://172.17.0.1:3000/patch_mamba_config.py -P . && \
    cd /vllm-workspace/vllm-ascend/vllm_ascend/patch/platform/patch_common/ && \
    cp patch_mamba_config.py patch_mamba_config.py.bak && \
    mv /workspace/patch_mamba_config.py .

ENV PATH="/usr/local/Ascend/8.3.RC1/compiler/bishengir/bin:${PATH}"
```
