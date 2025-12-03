# Hardware
INTEL(R) XEON(R) GOLD 6530, 32Cores

300IA2 32G(chip 910B4) × 8

DDR5 32G × 32

SATA SSD, 480G × 2

NVMe SSD, 2.0T × 3

# Software
Ubuntu 22.04.2 LTS, 5.15.0-60-generic

docker-ce 24.0.5, swr.cn-south-1.myhuaweicloud.com/ascendhub/mindie:2.1.RC2-800I-A2-py311-openeuler24.03-lts

npu-driver 25.2.2

npu-firmware 7.7.0.10.220

cann 8.2.RC2

mindie 2.1.RC2

# Configurations
乱序版，不按自顶向下排序，

## CPU Performance
查看当前 CPU 调度策略设置（x86 可能更倾向于通过BIOS能效模式，aarch64 一般使用 os 进行调整）
```shell
~# cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
performance
```
要求全部 `performance` 回显，

## Transparent Huge Pages
查看方式，
```shell
~# cat /sys/kernel/mm/transparent_hugepage/enabled
always [madvise] never
```
这里显示 `madvise` 表示按需，修改 `always` 方式，
```shell
~# echo always > /sys/kernel/mm/transparent_hugepage/enabled
~# cat /sys/kernel/mm/transparent_hugepage/enabled
[always] madvise never
```

## docker run
vim dockerrun.sh
```shell
~# docker run -itd --ipc=host --net=host -u root --privileged=true \
--shm-size 500g \
--device=/dev/davinci0 \
--device=/dev/davinci1 \
--device=/dev/davinci2 \
--device=/dev/davinci3 \
--device=/dev/davinci4 \
--device=/dev/davinci5 \
--device=/dev/davinci6 \
--device=/dev/davinci7 \
--device=/dev/davinci_manager \
--device=/dev/devmm_svm \
--device=/dev/hisi_hdc \
-v /usr/local/Ascend/driver:/usr/local/Ascend/driver \
-v /usr/local/Ascend/firmware:/usr/local/Ascend/firmware \
-v /usr/local/Ascend/add-ons/:/usr/local/Ascend/add-ons/ \
-v /usr/local/sbin/npu-smi:/usr/local/sbin/npu-smi \
-v /usr/local/sbin/:/usr/local/sbin/ \
-v /var/log/npu/conf/slog/slog.conf:/var/log/npu/conf/slog/slog.conf \
-v /var/log/npu/slog/:/var/log/npu/slog \
-v /etc/hccn.conf:/etc/hccn.conf \
-v /data:/data \
-v /usr/share/zoneinfo/Asia/Shanghai:/etc/localtime \
--name=21rc2-ds-r1-distill-llama-70b \
swr.cn-south-1.myhuaweicloud.com/ascendhub/mindie:2.1.RC2-800I-A2-py311-openeuler24.03-lts \
/bin/bash
```

## container os
```shell
~# uname -m && cat /etc/*release && uname -r
x86_64
openEuler release 24.03 (LTS)
NAME="openEuler"
VERSION="24.03 (LTS)"
ID="openEuler"
VERSION_ID="24.03"
PRETTY_NAME="openEuler 24.03 (LTS)"
ANSI_COLOR="0;31"

openEuler release 24.03 (LTS)
5.15.0-60-generic
```

## transformers
```shell
~# pip list | grep transformers
transformers                4.51.0

根据版本决定是否要更新，以更高的版本为准，
~# pip install transformers==4.47.0
```

## Jemalloc
Jemalloc动态链接库，若容器内不存在Jemalloc文件，需要安装，
```shell
~# yum install jemalloc
Package jemalloc-5.3.0-1.oe2403.x86_64 is already installed.
~# find / -name *libjemalloc*
/usr/lib64/libjemalloc.so.2
```
拉起服务前，将Jemalloc动态链接库引入环境，执行如下，
```shell
~# export LD_PRELOAD=/usr/lib64/libjemalloc.so.2:$LD_PRELOAD
```

## env
通过写 vim ~/.bashrc 的方式，使环境变量在推理后端永久生效，
```shell
export PYTORCH_NPU_ALLOC_CONF=expandable_segments:True
export NPU_MEMORY_FRACTION=0.95
export ATB_WORKSPACE_MEM_ALLOC_ALG_TYPE=3
export ATB_WORKSPACE_MEM_ALLOC_GLOBAL=1
export OMP_NUM_THREADS=10
export HCCL_DETERMINISTIC=false
unset HCCL_OP_EXPANSION_MODE
unset ATB_LLM_HCCL_ENABLE
# export ATB_LLM_COMM_BACKEND="hccl"
export INF_NAN_MODE_ENABLE=1
export TASK_QUEUE_ENABLE=2
export CPU_AFFINITY_CONF=1
unset ASCEND_LAUNCH_BLOCKING
export ATB_LAYER_INTERNAL_TENSOR_REUSE=1
export ATB_OPERATION_EXECUTE_ASYNC=2
export ATB_CONVERT_NCHW_TO_ND=1
export MINDIE_ASYNC_SCHEDULING_ENABLE=1
export ATB_CONTEXT_WORKSPACE_SIZE=0
export ATB_LAUNCH_KERNEL_WITH_TILING=1
export ATB_LLM_ENABLE_AUTO_TRANSPOSE=0
export HCCL_CONNECT_TIMEOUT=7200
export HCCL_EXEC_TIMEOUT=0
export HCCL_RDMA_PCIE_DIRECT_POST_NOSTRICT=TRUE
export LD_PRELOAD=/usr/lib64/libjemalloc.so.2:$LD_PRELOAD
```

## mindie-service config.json
按照总长输入输出配置4k(2k+2k)启动服务化，
```json
{
    "ServerConfig" :
    {
        "ipAddress" : "127.0.0.1",
        "managementIpAddress" : "127.0.0.2",
        "port" : 1025,
        "managementPort" : 1026,
        "httpsEnabled" : false,
        "interCommTLSEnabled" : false,
        "openAiSupport" : "vllm",
        "tokenTimeout" : 3600,
        "e2eTimeout" : 3600,
    },
    "BackendConfig" :
	{
        "npuDeviceIds" : [[0,1,2,3,4,5,6,7]],
        "multiNodesInferEnabled" : false,
        "interNodeTLSEnabled" : false,
        "ModelDeployConfig" :
        {
            "maxSeqLen" : 4200,
            "maxInputTokenLen" : 2100,
            "truncation" : false,
            "ModelConfig" : [
                {
                    "modelInstanceType" : "Standard",
                    "modelName" : "llama",
                    "modelWeightPath" : "/data/DeepSeek-R1-Distill-Llama-70B",
                    "worldSize" : 8,
                    "cpuMemSize" : 5,
                    "npuMemSize" : -1,
                    "backendType" : "atb",
                    "trustRemoteCode" : true,
                    "async_scheduler_wait_time": 120,
                    "kv_trans_timeout": 10,
                    "kv_link_timeout": 1080,
                    "multi_step": 1,
                    "ignore_eos": true
                }
            ]
        },
        "ScheduleConfig" :
        {
            "maxPrefillBatchSize" : 50,
            "maxPrefillTokens" : 8192,
            "maxBatchSize" : 200,
            "maxIterTimes" : 2100,
        }
    }
}
```

## FAQ - mindie_error_log
默认第一次启服务化，如果不是第一次，则需要先清理删除日志，
- 设置环境变量
```shell
export ASDOPS_LOG_LEVEL=ERROR
export ASDOPS_LOG_TO_STDOUT=1
```

- 拉起服务化

- 抓关键字
```shell
grep -rn ERROR /root/mindie/log
grep -rn ERROR /root/ascend/log
```

- 删除日志
```shell
rm -rf /root/mindie/* && rm -rf /root/ascend/*
```

- 去使能环境变量
```shell
unset ASDOPS_LOG_LEVEL
unset ASDOPS_LOG_TO_STDOUT
```

# Test
mindiebenchmark, aisbench, evalscope

## mindiebenchmark
```shell
benchmark \
--SyntheticConfigPath /usr/local/lib/python3.11/site-packages/mindiebenchmark/config/synthetic_config.json \
--DatasetType "synthetic" \
--ModelName llama \
--ModelPath "/data/DeepSeek-R1-Distill-Llama-70B" \
--TestType openai \
--Http http://127.0.0.1:1025 \
--ManagementHttp http://127.0.0.2:1026 \
--Concurrency 16 \
--TaskKind text \
--Tokenizer True
```

## aisbench
```shell
model="llama"
path="/data/DeepSeek-R1-Distill-Llama-70B/"
host_ip="127.0.0.1"
host_port="1025"
log_dir="output_log_${model}"

# 修改配置文件 -> 修改流式 TGI 接口
config_file="/usr/local/lib/python3.11/site-packages/ais_bench/benchmark/configs/models/tgi_api/tgi_stream_api_general.py"
# 修改数据集 -> 随机数据集、设置数据量、固定输入输出长度
synthetic_config="/usr/local/lib/python3.11/site-packages/ais_bench/datasets/synthetic/synthetic_config.py"

# 启动方式
~# ais_bench --models tgi_stream_api_general --dataset synthetic_gen --debug --mode perf
```

## evalscope
```shell
evalscope perf \
--parallel 1 \
--number  2  \
--model llama \
--url http://127.0.0.1:1025/v1/chat/completions \
--api openai \
--dataset random \
--max-tokens 1024 \
--min-tokens 1024 \
--prefix-length 0 \
--min-prompt-length 1024 \
--max-prompt-length 1024 \
--tokenizer-path /data/DeepSeek-R1-Distill-Llama-70B \
--query-template '{"model": "%m", "messages": [{"role": "user", "content": "%p"}], "user": "evalscope_user_{{RANDOM}}"}' \
--extra-args '{"ignore_eos": true}'
```
