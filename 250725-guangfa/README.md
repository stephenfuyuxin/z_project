# 硬件信息
| 硬件名称 | 配置信息           | 数量 |
| -------- | ------------------ | ---- |
| AI服务器 | Altas 800I A2      | 4    |
| CPU      | Kunpeng 920 48Core | 16   |
| NPU      | Ascend 910B4 64G   | 32   |

## CPU
```shell
# lscpu
Architecture:           aarch64
  CPU op-mode(s):       64-bit
  Byte Order:           Little Endian
CPU(s):                 192
  On-line CPU(s) list:  0-191
Vendor ID:              HiSilicon
  BIOS Vendor ID:       HiSilicon
  Model name:           Kunpeng-920
    BIOS Model name:    HUAWEI Kunpeng 920 5250
    Model:              0
    Thread(s) per core: 1
    Core(s) per socket: 48
    Socket(s):          4
    Stepping:           0x1
    BogoMIPS:           200.00
```

## NPU
```shell
# npu-smi info
+------------------------------------------------------------------------------------------------+
| npu-smi 25.0.rc1.1               Version: 25.0.rc1.1                                           |
+---------------------------+---------------+----------------------------------------------------+
| NPU   Name                | Health        | Power(W)    Temp(C)           Hugepages-Usage(page)|
| Chip                      | Bus-Id        | AICore(%)   Memory-Usage(MB)  HBM-Usage(MB)        |
+===========================+===============+====================================================+
| 0     910B4               | OK            | 105.5       39                0    / 0             |
| 0                         | xxxx:xx:xx.x  | 5           0    / 0          6154 / 65536         |
+===========================+===============+====================================================+
```

# 软件信息
| 软件名称        | 版本信息            |
| --------------- | ------------------- |
| OS              | openEuler 22.03 LTS |
| NPU Deiver      | 25.0.rc1.1          |
| NPU Firmware    | 7.7.0.1.231         |
| CANN            | 8.2.RC1             |
| Python          | 3.11.6              |
| torch           | 2.1.0               |
| torch_npu       | 2.1.0               |
| torchvison      | 0.16.0              |
| MindIE          | 2.1.RC1             |
| mindiebenchmark | 2.1rc1              |
| vLLM            | 0.8.5 / 0.10.1      |

## OS
```shell
# uname -m && cat /etc/*reLease && uname -r
aarch64
openEuler release 22.03 LTS
NAME="openEuler"
VERSION="22.03 LTS"
ID="openEuler"
VERSION_ID="22.03"
PRETTY_NAME="openEuler 22.03 LTS"
ANSI_COLOR="0;31"

openEuler release 22.03 LTS
5.10.0-60.18.0.50.0e2203.aarch64
```

## NPU

### NPU Driver
```shell
/usr/local/Ascend/driver# cat version.info
Version=25.0.rc1.1
ascendhal_version=7.35.23
aicpu_version=1.0
tdt_version=1.0
log_version=1.0
prof_version=2.0
dvppkernels_version=1.1
tsfw_version=1.0
Innerversion=V100R001C21SPC002B220
compatible_version=[V100R001C17],[V100R001C18],[V100R001C19],[V100R001C20],[V100R001C21]
compatible_version_fw=[7.0.0,7.7.99]
package_version=25.0.rc1.1
```

### NPU Firmware
```shell
/usr/local/Ascend/firmware# cat version.info
Version=7.7.0.1.231
firmware_version=1.0
package_version=25.0.rc1.1
compatible_version_drv=[23.0.0,23.0.0.],[24.0,24.0.],[24.1,24.1.],[25.0,25.0.]
```

## CANN
对应 mindie 2.1.RC1 版本，以 mindie:2.1.RC1-800I-A2-py311-openeuler24.03-lts 镜像为例，

### toolkit
```shell
/usr/local/Ascend/ascend-toolkit/latest/toolkit# cat version.info
Version=8.2.0.0.201
version_dir=8.2.RC1
timestamp=20250724_194044950
required_package_amct_acl_version="8.2"
required_package_aoe_version="8.2"
required_package_compiler_version="8.2"
required_package_fwkplugin_version="8.2"
required_package_hccl_version="8.2"
required_package_nca_version="8.2"
required_package_ncs_version="8.2"
required_package_opp_version="8.2"
required_package_opp_kernel_version=">=7.6, <=8.2"
required_package_runtime_version="8.2"

/usr/local/Ascend/ascend-toolkit/latest/aarch64-linux# cat ascend_toolkit_install.info
package_name=Ascend-cann-toolkit
version=8.2.RC1
innerversion=V100R001C22SPC001B231
compatible_version=[V100R001C15],[V100R001C18],[V100R001C19],[V100R001C20],[V100R001C21],[V100R001C23]
arch=aarch64
os=linux
path=/usr/local/Ascend/ascend-toolkit/8.2.RC1/aarch64-linux
```

### kernels
```shell
/usr/local/Ascend/ascend-toolkit/latest/opp_kernel# cat version.info
Version=8.2.0.0.201
version_dir=8.2.RC1
timestamp=20250724_194044950
ops_version=8.2.0.0.201
adk_version=8.2.0.0.201
required_package_amct_acl_version=">=7.6, <=8.2"
required_package_aoe_version=">=7.6, <=8.2"
required_package_compiler_version=">=7.6, <=8.2"
required_package_fwkplugin_version=">=7.6, <=8.2"
required_package_hccl_version=">=7.6, <=8.2"
required_package_nca_version=">=7.6, <=8.2"
required_package_ncs_version=">=7.6, <=8.2"
required_package_opp_version=">=7.6, <=8.2"
required_package_runtime_version=">=7.6, <=8.2"
required_package_toolkit_version=">=7.6, <=8.2"
```

### nnal
```shell
/usr/local/Ascend/nnal/atb/latest# cat version.info
    Ascend-cann-atb : 8.2.RC1
    Ascend-cann-atb Version : 8.2.RC1.B150
    Platform : aarch64
    branch : br_release_cann_8.2.RC1_20251226
    commit id : f10dc20391d8af04c3f8024aca0e0dfa94d2a0a5
```

## MindIE
对应 mindie 2.1.RC1 版本，以 mindie:2.1.RC1-800I-A2-py311-openeuler24.03-lts 镜像为例，
```shell
/usr/local/Ascend/mindie/latest# cat version.info
Ascend-mindie : MindIE 2.1.RC1.B152
mindie-rt: 2.1.RC1.B152
mindie-torch: 2.1.RC1.B152
mindie-service: 2.1.RC1.B152
mindie-llm: 2.1.RC1.B152
mindie-sd:2.1.RC1.B152
Platform : aarch64
```

# 配置信息

## 镜像启动
分为 MindIE Service 推理后端 和 vLLM benchmark 推理前端，

### MindIE Service 推理后端
```shell
# vim mindierun.sh

#!/bin/bash
docker run -itd --ipc=host --net=host -u root --privileged=true \
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
-v /home:/home \
-v /data:/data \
-v /usr/share/zoneinfo/Asia/Shanghai:/etc/localtime \
--name=21rc1_deepseekr1 \
swr.cn-south-1.myhuaweicloud.com/ascendhub/mindie:2.1.RC1-800I-A2-py311-openeuler24.03-lts \
/bin/bash
```

### vLLM benchmark 推理前端
```shell
# vim vllmrun.sh

#!/bin/bash
docker run -itd --ipc=host --net=host --name=vllm \
-v /data:/data \
vllm_arm:v1 \
/bin/bash
```

## MindIE Service 下 config.json 配置
- 混合并行 MLA 策略按照 "dp","tp","moe_ep","moe_tp","sp" 配置说明；
- 混合并行 MLA 涉及 cp 配置策略，按照 "dp","tp","moe_ep","moe_tp","sp","cp" 配置说明；
- 其他配置参考对应章节；

### MLA 2,8,4,4,1 配置
仅列举关键配置项，
- "tokenTimeout"：默认为600，也可配置为3600；
- "e2eTimeout"：默认为600，也可配置未3600；
- "maxSeqLen"：配置为32k，输入输出分别为16k+16k;
- "maxInputTokenLen"/"maxPrefillTokens"：输入为16k；
- "maxPrefillBatchSize"：输入bz，默认为50，设置为与dp保持一致为2；
- "maxIterTimes"：输出为16k；
- "maxBatchSize"：输出bz，默认为200；
- "dp","tp","moe_ep","moe_tp","sp"=2,8,4,4,1；
```json
    "ServerConfig" :
    {
        "ipAddress" : "x.x.x.x",
        "managementIpAddress" : "x.x.x.x",
        "port" : 1025,
        "managementPort" : 1026,
        "httpsEnabled" : false,
        "interCommTLSEnabled" : false,
        "tokenTimeout" : 3600,
        "e2eTimeout" : 3600,
    },
    "BackendConfig" : {
        "npuDeviceIds" : [[0,1,2,3,4,5,6,7]],
        "multiNodesInferEnabled" : true,
        "interNodeTLSEnabled" : false,
        "ModelDeployConfig" :
        {
            "maxSeqLen" : 32768,
            "maxInputTokenLen" : 16384,
            "ModelConfig" : [
                {
                    "modelName" : "external-deepseek-r1-ascend",
                    "modelWeightPath" : "/the/path/of/DeepSeek-R1-bf16-hfd-w8a8",
                    "worldSize" : 8,
                    "dp" : 2,
                    "tp" : 8,
                    "moe_ep" : 4,
                    "moe_tp" : 4,
                    "sp" : 1,
                    "ignore_eos" : true,
                    "models":{"deepseekv2": {"ep_level": 1}}
                }
            ]
        },
        "ScheduleConfig" :
        {
            "maxPrefillBatchSize" : 2,
            "maxPrefillTokens" : 16384,
            "maxBatchSize" : 200,
            "maxIterTimes" : 16384,
        }
    }
```

### MLA 2,8,16,1,8 配置
仅列举关键配置项，
- "tokenTimeout"：默认为600，也可配置为3600；
- "e2eTimeout"：默认为600，也可配置未3600；
- "maxSeqLen"：配置为32k，输入输出分别为16k+16k;
- "maxInputTokenLen"/"maxPrefillTokens"：输入为16k；
- "maxPrefillBatchSize"：输入bz，默认为50，设置为与dp保持一致为2；
- "maxIterTimes"：输出为16k；
- "maxBatchSize"：输出bz，默认为200；
- "dp","tp","moe_ep","moe_tp","sp"=2,8,16,1,8；
```json
    "ServerConfig" :
    {
        "ipAddress" : "x.x.x.x",
        "managementIpAddress" : "x.x.x.x",
        "port" : 1025,
        "managementPort" : 1026,
        "httpsEnabled" : false,
        "interCommTLSEnabled" : false,
        "tokenTimeout" : 3600,
        "e2eTimeout" : 3600,
    },
    "BackendConfig" : {
        "npuDeviceIds" : [[0,1,2,3,4,5,6,7]],
        "multiNodesInferEnabled" : true,
        "interNodeTLSEnabled" : false,
        "ModelDeployConfig" :
        {
            "maxSeqLen" : 32768,
            "maxInputTokenLen" : 16384,
            "ModelConfig" : [
                {
                    "modelName" : "external-deepseek-r1-ascend",
                    "modelWeightPath" : "/the/path/of/DeepSeek-R1-bf16-hfd-w8a8",
                    "worldSize" : 8,
                    "dp" : 2,
                    "tp" : 8,
                    "moe_ep" : 16,
                    "moe_tp" : 1,
                    "sp" : 8,
                    "ignore_eos" : true,
                    "models":{"deepseekv2": {"ep_level": 1}}
                }
            ]
        },
        "ScheduleConfig" :
        {
            "maxPrefillBatchSize" : 2,
            "maxPrefillTokens" : 16384,
            "maxBatchSize" : 200,
            "maxIterTimes" : 16384,
        }
    }
```

### MLA 2,8,4,4,1 + 使能 MTP 配置
仅列举关键配置项，
- "tokenTimeout"：默认为600，也可配置为3600；
- "e2eTimeout"：默认为600，也可配置未3600；
- "maxSeqLen"：带 MTP 配置为16k，输入输出分别为16k+16k;
- "maxInputTokenLen"/"maxPrefillTokens"：输入为16k；
- "maxPrefillBatchSize"：输入bz，默认为50；
- "maxIterTimes"：输出为16k；
- "maxBatchSize"：输出bz，默认为200；
- "dp","tp","moe_ep","moe_tp","sp"=2,8,4,4,1；
- "plugin_params": 用于使能 MTP 特性，"{\"plugin_type\":\"mtp\",\"num_speculative_tokens\": 1}"；
```json
    "ServerConfig" :
    {
        "ipAddress" : "x.x.x.x",
        "managementIpAddress" : "x.x.x.x",
        "port" : 1025,
        "managementPort" : 1026,
        "httpsEnabled" : false,
        "interCommTLSEnabled" : false,
        "tokenTimeout" : 3600,
        "e2eTimeout" : 3600,
    },
    "BackendConfig" : {
        "npuDeviceIds" : [[0,1,2,3,4,5,6,7]],
        "multiNodesInferEnabled" : true,
        "interNodeTLSEnabled" : false,
        "ModelDeployConfig" :
        {
            "maxSeqLen" : 16384,
            "maxInputTokenLen" : 16384,
            "ModelConfig" : [
                {
                    "modelName" : "deepseekr1",
                    "modelWeightPath" : "/the/path/of/DeepSeek-R1-bf16-hfd-w8a8",
                    "worldSize" : 8,
                    "dp" : 2,
                    "tp" : 8,
                    "moe_ep" : 4,
                    "moe_tp" : 4,
                    "sp" : 1,
                    "ignore_eos" : true,
                    "enable_warmup_with_sampling": false,
                    "plugin_params": "{\"plugin_type\":\"mtp\",\"num_speculative_tokens\": 1}",
                    "models": {
                        "deepseekv2": {
                            "enable_mlapo_prefetch": true,
                            "kv_cache_options": {
                                "enable_nz": true
                            }
                        }
                    }
                }
            ]
        },
        "ScheduleConfig" :
        {
            "maxPrefillBatchSize" : 50,
            "maxPrefillTokens" : 16384,
            "maxBatchSize" : 200,
            "maxIterTimes" : 16384,
        }
    }
```

### MLA 2,8,4,4,1 + 去使能 MTP 配置
仅列举关键配置项，
- "tokenTimeout"：默认为600，也可配置为3600；
- "e2eTimeout"：默认为600，也可配置未3600；
- "maxSeqLen"：恢复为不带 MTP 配置为32k，输入输出分别为16k+16k;
- "maxInputTokenLen"/"maxPrefillTokens"：输入为16k；
- "maxPrefillBatchSize"：输入bz，默认为50；
- "maxIterTimes"：输出为16k；
- "maxBatchSize"：输出bz，默认为200；
- "dp","tp","moe_ep","moe_tp","sp"=2,8,4,4,1；
- "plugin_params": 用于使能 MTP 特性，这行删除用于去使能 MTP 特性，"{\"plugin_type\":\"mtp\",\"num_speculative_tokens\": 1}"；
```json
    "ServerConfig" :
    {
        "ipAddress" : "x.x.x.x",
        "managementIpAddress" : "x.x.x.x",
        "port" : 1025,
        "managementPort" : 1026,
        "httpsEnabled" : false,
        "interCommTLSEnabled" : false,
        "tokenTimeout" : 3600,
        "e2eTimeout" : 3600,
    },
    "BackendConfig" : {
        "npuDeviceIds" : [[0,1,2,3,4,5,6,7]],
        "multiNodesInferEnabled" : true,
        "interNodeTLSEnabled" : false,
        "ModelDeployConfig" :
        {
            "maxSeqLen" : 32768,
            "maxInputTokenLen" : 16384,
            "ModelConfig" : [
                {
                    "modelName" : "deepseekr1",
                    "modelWeightPath" : "/the/path/of/DeepSeek-R1-bf16-hfd-w8a8",
                    "worldSize" : 8,
                    "dp" : 2,
                    "tp" : 8,
                    "moe_ep" : 4,
                    "moe_tp" : 4,
                    "sp" : 1,
                    "ignore_eos" : true,
                    "enable_warmup_with_sampling": false,
                    "models": {
                        "deepseekv2": {
                            "enable_mlapo_prefetch": true,
                            "kv_cache_options": {
                                "enable_nz": true
                            }
                        }
                    }
                }
            ]
        },
        "ScheduleConfig" :
        {
            "maxPrefillBatchSize" : 50,
            "maxPrefillTokens" : 16384,
            "maxBatchSize" : 200,
            "maxIterTimes" : 16384,
        }
    }
```

### MLA 1,8,16,1,8,2 适用于长序列推理场景
适用于长序列推理，按照现场配置进行改造使用，仅列举关键配置项，
- "tokenTimeout"：默认为600，也可配置为3600；
- "e2eTimeout"：默认为600，也可配置未3600；
- "maxSeqLen"：非 MTP 特性配置为32k，输入输出分别为16k+16k;
- "maxInputTokenLen"/"maxPrefillTokens"：输入为16k；
- "maxPrefillBatchSize"：输入bz，默认为50；
- "maxIterTimes"：输出为16k；
- "maxBatchSize"：输出bz，默认为200；
- "dp","tp","moe_ep","moe_tp","sp","cp"=1,8,16,4,1；
```json
    "ServerConfig" :
    {
        "ipAddress" : "x.x.x.x",
        "managementIpAddress" : "x.x.x.x",
        "port" : 1025,
        "managementPort" : 1026,
        "httpsEnabled" : false,
        "interCommTLSEnabled" : false,
        "tokenTimeout" : 3600,
        "e2eTimeout" : 3600,
    },
    "BackendConfig" : {
        "npuDeviceIds" : [[0,1,2,3,4,5,6,7]],
        "multiNodesInferEnabled" : true,
        "interNodeTLSEnabled" : false,
        "ModelDeployConfig" :
        {
            "maxSeqLen" : 32768,
            "maxInputTokenLen" : 16384,
            "ModelConfig" : [
                {
                    "modelName" : "dsr1_w8a8_mtp_quant",
                    "modelWeightPath" : "/the/path/of/DeepSeek-R1-bf16-hfd-w8a8",
                    "worldSize" : 8,
                    "dp" : 1,
                    "tp" : 8,
                    "moe_ep" : 16,
                    "moe_tp" : 1,
                    "sp" : 8,
                    "cp" : 2,
                    "ignore_eos" : true,
                    "async_scheduler_wait_time": 120,
                    "kv_trans_timeout": 10,
                    "kv_link_timeout": 1080,
                    "models": {
                        "deepseekv2": {
                            "ep_level": 1,
                            "enable_mlapo_prefetch": true,
                            "topk_scaling_factor": 0.25
                        }
                    }
                }
            ]
        },
        "ScheduleConfig" :
        {
            "maxPrefillBatchSize" : 50,
            "maxPrefillTokens" : 16384,
            "maxBatchSize" : 200,
            "maxIterTimes" : 16384,
        }
    }
```

## MindIE Service 下 env 环境变量配置
通过写 `vim ~/.bashrc` 的方式，使环境变量在推理后端永久生效，
```shell
# vim ~/.bashrc

export PYTORCH_NPU_ALLOC_CONF=expandable_segments:True
export NPU_MEMORY_FRACTION=0.97
export ATB_WORKSPACE_MEM_ALLOC_ALG_TYPE=3
export ATB_WORKSPACE_MEM_ALLOC_GLOBAL=1
export OMP_NUM_THREADS=10
export HCCL_DETERMINISTIC=false
export HCCL_OP_EXPANSION_MODE="AIV"
export ATB_LLM_HCCL_ENABLE=1
export ATB_LLM_COMM_BACKEND="hccl"
export INF_NAN_MODE_ENABLE=1
export TASK_QUEUE_ENABLE=2
export CPU_AFFINITY_CONF=1
unset ASCEND_LAUNCH_BLOCKING
export ATB_LAYER_INTERNAL_TENSOR_REUSE=1
export ATB_OPENATION_EXECUTE_ASYNC=1
export ATB_CONVERT_NCHW_TO_ND=1
export MINDIE_ASYNC_SCHEDULING_ENABLE=1
export ATB_CONTEXT_WORKSPACE_SIZE=0
export ATB_LAUNCH_KERNEL_WITH_TILING=1
export ATB_LLM_ENABLE_AUTO_TRANSPOSE=0
export HCCL_CONNECT_TIMEOUT=7200
export HCCL_EXEC_TIMEOUT=0
export HCCL_RDMA_PCIE_DIRECT_POST_NOSTRICT=TRUE

export MIES_CONTAINER_IP=x.x.x.x
export RANK_TABLE_FILE=/the/path/of/ranktable_2.json

# 以下 4 个环境变量为 mindie 相关日志打印，会影响性能，性能测试需要去使能，
# export MINDIE_LOG_TO_STDOUT=1
# export MINDIE_LOG_TO_FILE=1
# export MINDIE_LOG_LEVEL=info
# export LD_PRELOAD="/usr/lib64/libjemalloc.so.2:$LD_PRELOAD"

# 如果用 mindie benchmark 工具性能测试，下面这个环境变量 MINDIE_LOG_TO_STDOUT 需要使能，
# export MINDIE_LOG_TO_STDOUT="benchmark:1; client:1"
```

## MindIE benchmark 前端配置

### mindiebenchmark
```shell
# pip list | grep mindie
mindie_llm                  2.1rc1
mindiebenchmark             2.1rc1
mindieclient                2.1rc1
mindiesd                    2.1rc1
mindiesimulator             0.0.1
mindietorch                 2.1rc1+torch2.1.0.abi0

# pip show mindiebenchmark
Name: mindiebenchmark
Version: 2.1rc1
Summary: build wheel for mindie benchmark
Home-page:
Author: ascend
Author-email:
License:
Location: /usr/local/lib/python3.11/site-packages
Requires:
Required-by:
```

### mindieclient python config
/usr/local/lib/python3.11/site-packages/mindieclient/python/config/config.json
```shell
# cd /usr/local/lib/python3.11/site-packages/mindieclient/python/config/
# chmod 640 config.json
```

### mindiebenchmark config
/usr/local/lib/python3.11/site-packages/mindiebenchmark/config/config.json
```shell
# cd /usr/local/lib/python3.11/site-packages/mindiebenchmark/config/
# chmod 640 config.json
```

### mindiebenchmark config synthetic_config
/usr/local/lib/python3.11/site-packages/mindiebenchmark/config/synthetic_config.json

配置要求，
- 输入输出分别为4k1k；
- Concurrency:RequestCount 并发数与数据集条目的比例，推荐配置为1:4，现场配置为1:10，根据实际情况进行修改；

```shell
# cd /usr/local/lib/python3.11/site-packages/mindiebenchmark/config/
# chmod 640 synthetic_config.json
# vim synthetic_config.json
{
    "Input":{
        "Method": "uniform",
        "Params": {"MinValue": 4096, "MaxValue": 4096}
    },
    "Output": {
        "Method": "uniform",
        "Params": {"MinValue": 1024, "MaxValue": 1024}
    },
    "RequestCount": 250
}
```

### 开启 mindiebenchmark 日志打屏
如果用 mindiebenchmark 作为性能测试工具，需要设置日志打屏环境变量，
```shell
export MINDIE_LOG_TO_STDOUT="benchmark:1; client:1"
```

### 运行 mindiebenchmark 性能测试

配置项说明如下，
- ModelName 需要与 mindie-service config.json 里的 modelName 一致；
- ModelPath 需要与 mindie-service config.json 里的 modelWeightPath 一致；
- Http 设置为主节点机器的ip（多机场景）以及 port 端口，与 mindie-service config.json 里的一致；
- ManagementHttp 设置为主节点机器的ip（多机场景）以及 managementPort 端口，与 mindie-service config.json 里的一致；

性能测试参考执行如下，
```shell
benchmark \
--SyntheticConfigPath /usr/local/lib/python3.11/site-packages/mindiebenchmark/config/synthetic_config.json \
--DatasetType "synthetic" \
--ModelName xxxxxx \
--ModelPath "/the/path/of/modelweight/" \
--TestType openai \
--Http http://x.x.x.x:xxxx \
--ManagementHttp http://x.x.x.x:xxxx \
--Concurrency 25 \
--TaskKind text \
--Tokenizer True
```

## vLLM benchmark 前端配置
vllm 工具以及 vllm benchmark 代码通过镜像承载，镜像启动为容器之后作为推理前端，直接运行 vllm benchmark 测试套件即可，

配置项说明如下，
- host，设置为主节点机器的ip（多机场景），与 mindie-service config.json 里的一致；
- port，设置为 port 端口，与 mindie-service config.json 里的一致；
- served-model-name，需要与 mindie-service config.json 里的 modelName 一致；
- model，需要与 mindie-service config.json 里的 modelWeightPath 一致；
- max-concurrency:num-prompts，并发数与数据集条目的比例，推荐配置为1:4，现场配置为1:10，根据实际情况进行修改；

在 vllm 源代码根目录下，执行性能测试参考如下，
```shell
python3 benchmarks/benchmark_serving.py \
    --host x.x.x.x \
    --port xxxx \
    --served-model-name "xxxxxx"  \
    --backend "openai-chat" \
    --model "/the/path/of/modelweight" \
    --endpoint "/v1/chat/completions" \
    --dataset-name "random" \
    --num-prompts 20 \
    --random_input_len 4096 \
    --random_output_len 1024 \
    --max-concurrency 5 \
    --ignore_eos
```

# 性能数据
## MindIE benchmark
涉及 MindIE 三个版本 MindIE 2.1.T10.B060, MindIE 2.1.RC1.B092, MindIE 2.1.RC1.B152，以 B060 和 B092 版本为准，

涉及 MindIE benchmark 随 MindIE 版本自带，

### MindIE 2.1.T10.B060
取值方式，
- TTFT(ms)，取 FirstTokenTime 中 average
- TPOT(ms)，取 DecodeTime 中 average

推理后端32k(16k+16k)，MLA 2,8,4,4,1，输入输出4k1k，Concurrency:RequestCount=1:4
| Model      | dp | tp | moe_ep | moe_tp | sp | Model Length | Total Length | Concurrency | RequestCount | TTFT(ms)   | TPOT(ms) |
| ---------- | -- | -- | ------ | ------ | -- | ------------ | ------------ | ----------- | ------------ | ---------- | -------- |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 5           | 20           | 1303.85    | 64.5014  |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 10          | 40           | 2089.775   | 69.2063  |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 15          | 60           | 2866.1333  | 71.6391  |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 20          | 80           | 3624.7625  | 71.4263  |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 25          | 100          | 4382.12    | 74.1949  |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 30          | 120          | 5128.425   | 74.0763  |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 35          | 140          | 3965.4429  | 83.4565  |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 35          | 140          | 3967.2571  | 85.0697  |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 35          | 140          | 3968.6571  | 86.5612  |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 40          | 160          | 10397.1062 | 95.5639  |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 45          | 180          | 21946.1667 | 95.7002  |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 50          | 200          | 35488.635  | 98.4092  |

指标 ttft 在并发35时陡降（连测3次）必现，并发15时 ttft<3s 达成，所有并发在 tpot < 100ms 达成；

推理后端32k(16k+16k)，MLA 2,8,4,4,1，输入输出4k1k，Concurrency:RequestCount=1:10
| Model      | dp | tp | moe_ep | moe_tp | sp | Model Length | Total Length | Concurrency | RequestCount | TTFT(ms)   | TPOT(ms) |
| ---------- | -- | -- | ------ | ------ | -- | ------------ | ------------ | ----------- | ------------ | ---------- | -------- |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 5           | 50           | 1320.48    | 67.464   |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 10          | 100          | 2089.81    | 67.6794  |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 15          | 150          | 2856.8267  | 69.3979  |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 20          | 200          | 3571.425   | 70.3092  |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 25          | 250          | 4363.736   | 71.8698  |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 30          | 300          | 5092.43    | 73.2793  |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 35          | 350          | 2882.6229  | 85.8515  |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 35          | 350          | 2884.7914  | 84.8607  |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 35          | 350          | 2876.3257  | 84.7459  |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 40          | 400          | 10963.6875 | 97.1349  |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 45          | 450          | 23505.9667 | 95.0788  |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 50          | 500          | 36194.582  | 93.898   |

指标 ttft 在并发35时陡降（连测3次）必现，并发15时 ttft<3s 达成，所有并发在 tpot < 100ms 达成；

推理后端32k(16k+16k)，MLA 2,8,16,1,8，输入输出4k1k，Concurrency:RequestCount=1:4
| Model      | dp | tp | moe_ep | moe_tp | sp | Model Length | Total Length | Concurrency | RequestCount | TTFT(ms)   | TPOT(ms) |
| ---------- | -- | -- | ------ | ------ | -- | ------------ | ------------ | ----------- | ------------ | ---------- | -------- |
| ds-r1-int8 | 2  | 8  | 16     | 1      | 8  | 32k(16k+16k) | 5k(4k+1k)    | 5           | 20           | 1437.4     | 89.6589  |
| ds-r1-int8 | 2  | 8  | 16     | 1      | 8  | 32k(16k+16k) | 5k(4k+1k)    | 10          | 40           | 2323.675   | 90.6738  |
| ds-r1-int8 | 2  | 8  | 16     | 1      | 8  | 32k(16k+16k) | 5k(4k+1k)    | 15          | 60           | 3211.3     | 91.6263  |
| ds-r1-int8 | 2  | 8  | 16     | 1      | 8  | 32k(16k+16k) | 5k(4k+1k)    | 20          | 80           | 4079.6375  | 92.9413  |
| ds-r1-int8 | 2  | 8  | 16     | 1      | 8  | 32k(16k+16k) | 5k(4k+1k)    | 25          | 100          | 4952.19    | 93.5295  |
| ds-r1-int8 | 2  | 8  | 16     | 1      | 8  | 32k(16k+16k) | 5k(4k+1k)    | 30          | 120          | 5763.9417  | 97.3635  |
| ds-r1-int8 | 2  | 8  | 16     | 1      | 8  | 32k(16k+16k) | 5k(4k+1k)    | 35          | 140          | 6608.2786  | 99.808   |
| ds-r1-int8 | 2  | 8  | 16     | 1      | 8  | 32k(16k+16k) | 5k(4k+1k)    | 40          | 160          | 7472.325   | 96.8846  |
| ds-r1-int8 | 2  | 8  | 16     | 1      | 8  | 32k(16k+16k) | 5k(4k+1k)    | 45          | 180          | 8333.0444  | 102.4389 |
| ds-r1-int8 | 2  | 8  | 16     | 1      | 8  | 32k(16k+16k) | 5k(4k+1k)    | 50          | 200          | 9166.485   | 104.3129 |

指标 ttft 无陡降问题，相比 MLA 2,8,4,4,1，ttft 在低并发时性能基本持平存在少许劣化，高并发时性能上升趋势平缓具有一定优势；

### MindIE 2.1.RC1.B092
取值方式，
- TTFT(ms)，取 FirstTokenTime 中 average
- TPOT(ms)，取 DecodeTime 中 average

推理后端32k(16k+16k)，MLA 2,8,4,4,1，输入输出4k1k，Concurrency:RequestCount=1:4
| Model      | dp | tp | moe_ep | moe_tp | sp | Model Length | Total Length | Concurrency | RequestCount | TTFT(ms)   | TPOT(ms) |
| ---------- | -- | -- | ------ | ------ | -- | ------------ | ------------ | ----------- | ------------ | ---------- | -------- |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 5           | 20           | 1290.55    | 68.1276  |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 10          | 40           | 2083.525   | 70.1545  |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 15          | 60           | 2819.45    | 69.5495  |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 20          | 80           | 3572.025   | 75.5876  |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 25          | 100          | 4329.04    | 75.4382  |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 30          | 120          | 5105.0667  | 81.4722  |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 35          | 140          | 4110.9643  | 87.2286  |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 40          | 160          | 9974.0188  | 95.2362  |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 45          | 180          | 21718.3056 | 96.5663  |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 50          | 200          | 34309.195  | 94.514   |

指标 ttft 在并发35时仍然存在陡降现象，并发15时 ttft<3s 达成，ttft 整体趋势相比 2.1.T10.B060 有少许提升，所有并发在 tpot < 100ms 达成；

## vLLM benchmark
涉及 MindIE 三个版本 MindIE 2.1.T10.B060, MindIE 2.1.RC1.B092, MindIE 2.1.RC1.B152，以 B152 版本为准，

涉及 vLLM 0.8.5 和 0.10.1 两个版本，

### vLLM 0.8.5 + MindIE 2.1.RC1.B152
取值方式，
- TTFT(ms)，取 Mean TTFT (ms) 值；
- TOPT(ms)，取 Mean TPOT (ms) 值；

推理后端32k(16k+16k)，MLA 2,8,4,4,1，输入输出4k1k，max-concurrency:num-prompts=1:4
| Model      | dp | tp | moe_ep | moe_tp | sp | Model Length | Total Length | Concurrency | RequestCount | TTFT(ms)   | TPOT(ms) |
| ---------- | -- | -- | ------ | ------ | -- | ------------ | ------------ | ----------- | ------------ | ---------- | -------- |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 5           | 20           | 1344.10    | 73.86    |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 10          | 40           | 2122.95    | 74.68    |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 15          | 60           | 2926.62    | 74.60    |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 20          | 80           | 3709.08    | 79.61    |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 25          | 100          | 4548.46    | 80.05    |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 30          | 120          | 5471.30    | 83.06    |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 35          | 140          | 3391.13    | 90.89    |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 40          | 160          | 8442.08    | 103.96   |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 45          | 180          | 20048.14   | 103.50   |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 50          | 200          | 34602.93   | 103.80   |

指标 ttft 在并发35时仍然存在陡降现象，并发15时 ttft 为 2.9s+，ttft<3s 达成，tpot 在高并发时存在 100ms+；

推理后端32k(16k+16k)，MLA 2,8,16,1,8，输入输出4k1k，max-concurrency:num-prompts=1:4
| Model      | dp | tp | moe_ep | moe_tp | sp | Model Length | Total Length | Concurrency | RequestCount | TTFT(ms)   | TPOT(ms) |
| ---------- | -- | -- | ------ | ------ | -- | ------------ | ------------ | ----------- | ------------ | ---------- | -------- |
| ds-r1-int8 | 2  | 8  | 16     | 1      | 8  | 32k(16k+16k) | 5k(4k+1k)    | 5           | 20           | 1574.69    | 88.02    |
| ds-r1-int8 | 2  | 8  | 16     | 1      | 8  | 32k(16k+16k) | 5k(4k+1k)    | 10          | 40           | 2465.63    | 87.59    |
| ds-r1-int8 | 2  | 8  | 16     | 1      | 8  | 32k(16k+16k) | 5k(4k+1k)    | 15          | 60           | 3257.97    | 91.19    |
| ds-r1-int8 | 2  | 8  | 16     | 1      | 8  | 32k(16k+16k) | 5k(4k+1k)    | 20          | 80           | 4142.61    | 94.45    |
| ds-r1-int8 | 2  | 8  | 16     | 1      | 8  | 32k(16k+16k) | 5k(4k+1k)    | 25          | 100          | 5218.33    | 92.80    |
| ds-r1-int8 | 2  | 8  | 16     | 1      | 8  | 32k(16k+16k) | 5k(4k+1k)    | 30          | 120          | 5913.06    | 93.34    |
| ds-r1-int8 | 2  | 8  | 16     | 1      | 8  | 32k(16k+16k) | 5k(4k+1k)    | 35          | 140          | 6866.77    | 97.16    |
| ds-r1-int8 | 2  | 8  | 16     | 1      | 8  | 32k(16k+16k) | 5k(4k+1k)    | 40          | 160          | 7769.33    | 94.79    |
| ds-r1-int8 | 2  | 8  | 16     | 1      | 8  | 32k(16k+16k) | 5k(4k+1k)    | 45          | 180          | 8807.63    | 99.21    |
| ds-r1-int8 | 2  | 8  | 16     | 1      | 8  | 32k(16k+16k) | 5k(4k+1k)    | 50          | 200          | 9673.76    | 103.43   |

指标 ttft 无陡降问题，相比 MLA 2,8,4,4,1，并发15时 ttft 为 3.2s+，tpot 在高并发时存在 100ms+；

推理后端32k(16k+16k)，MLA 2,8,4,4,1，使能 MTP 特性，输入输出4k1k，max-concurrency:num-prompts=1:4
| Model      | dp | tp | moe_ep | moe_tp | sp | Model Length | Total Length | Concurrency | RequestCount | TTFT(ms)   | TPOT(ms) | Median TPOT(ms) |
| ---------- | -- | -- | ------ | ------ | -- | ------------ | ------------ | ----------- | ------------ | ---------- | -------- | --------------- |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 16k(16k+16k) | 5k(4k+1k)    | 5           | 20           | 991.15     | 773.32   | 51.71           |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 16k(16k+16k) | 5k(4k+1k)    | 10          | 40           | 1263.12    | 334.51   | 54.32           |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 16k(16k+16k) | 5k(4k+1k)    | 15          | 60           | 1451.01    | 282.28   | 57.47           |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 16k(16k+16k) | 5k(4k+1k)    | 20          | 80           | 1729.08    | 587.73   | 61.78           |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 16k(16k+16k) | 5k(4k+1k)    | 25          | 100          | 1910.33    | 958.80   | 67.26           |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 16k(16k+16k) | 5k(4k+1k)    | 30          | 120          | 2167.36    | 718.74   | 66.96           |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 16k(16k+16k) | 5k(4k+1k)    | 35          | 140          | 2447.56    | 884.49   | 72.20           |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 16k(16k+16k) | 5k(4k+1k)    | 40          | 160          | 2643.59    | 965.51   | 78.30           |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 16k(16k+16k) | 5k(4k+1k)    | 45          | 180          | 7875.97    | 686.84   | 88.03           |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 16k(16k+16k) | 5k(4k+1k)    | 50          | 200          | 15727.13   | 932.70   | 91.93           |

指标 ttft 无陡降问题，相同 MLA 策略下使能 MTP 特性相比非 MTP特性，ttft 性能提升明显，但 tpot 结果性能存在劣化10倍+，且 mean 相比 median 数据差距较大，不合理；

### vLLM 0.10.1 + MindIE 2.1.RC1.B152
取值方式，
- TTFT(ms)，取 Mean TTFT (ms) 值；
- TOPT(ms)，取 Mean TPOT (ms) 值；

推理后端32k(16k+16k)，MLA 2,8,4,4,1，使能 MTP 特性，输入输出4k1k，max-concurrency:num-prompts=1:4
| Model      | dp | tp | moe_ep | moe_tp | sp | Model Length | Total Length | Concurrency | RequestCount | TTFT(ms)   | TPOT(ms) | Median TPOT(ms) |
| ---------- | -- | -- | ------ | ------ | -- | ------------ | ------------ | ----------- | ------------ | ---------- | -------- | --------------- |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 16k(16k+16k) | 5k(4k+1k)    | 5           | 20           | 990.77     | 50.22    | 52.28           |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 16k(16k+16k) | 5k(4k+1k)    | 10          | 40           | 1212.24    | 382.07   | 54.70           |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 16k(16k+16k) | 5k(4k+1k)    | 15          | 60           | 1405.94    | 896.96   | 58.31           |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 16k(16k+16k) | 5k(4k+1k)    | 20          | 80           | 1638.91    | 1182.88  | 59.59           |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 16k(16k+16k) | 5k(4k+1k)    | 25          | 100          | 1863.76    | 1243.74  | 68.07           |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 16k(16k+16k) | 5k(4k+1k)    | 30          | 120          |    |    |            |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 16k(16k+16k) | 5k(4k+1k)    | 35          | 140          |    |    |            |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 16k(16k+16k) | 5k(4k+1k)    | 40          | 160          |    |    |            |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 16k(16k+16k) | 5k(4k+1k)    | 45          | 180          |    |    |            |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 16k(16k+16k) | 5k(4k+1k)    | 50          | 200          |    |    |            |

使能 MTP 特性下，相同 MLA 2,8,4,4,1 策略，vllm 0.10.1与0.8.5 ttft 性能趋势类似，但 tpot 结果存在正常/不正常结果，且 mean 与 median 之间的差距仍然较大，不合理；

推理后端32k(16k+16k)，MLA 2,8,4,4,1，去使能 MTP 特性，输入输出4k1k，max-concurrency:num-prompts=1:4
| Model      | dp | tp | moe_ep | moe_tp | sp | Model Length | Total Length | Concurrency | RequestCount | TTFT(ms)   | TPOT(ms) | Median TPOT(ms) |
| ---------- | -- | -- | ------ | ------ | -- | ------------ | ------------ | ----------- | ------------ | ---------- | -------- | --------------- |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 5           | 20           | 1394.36    | 72.50    | 72.09           |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 10          | 40           | 2611.01    | 72.76    | 72.53           |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 15          | 60           | 3787.87    | 72.27    | 72.08           |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 20          | 80           | 4623.35    | 79.71    | 80.49           |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 25          | 100          | 5616.94    | 78.05    | 76.65           |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 30          | 120          |    |    |            |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 35          | 140          |    |    |            |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 40          | 160          |    |    |            |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 45          | 180          |    |    |            |
| ds-r1-int8 | 2  | 8  | 4      | 4      | 1  | 32k(16k+16k) | 5k(4k+1k)    | 50          | 200          |    |    |            |

使能 MTP 特性下，仅去使能 MTP 功能，相同 MLA 2,8,4,4,1 策略，ttft 和 tpot 性能趋势类似，无明显提升，且 ttft 存在少许性能劣化；

推理后端32k(16k+16k)，MLA 2,8,4,4,1，去使能 MTP 特性，长序列推理配置，输入输出4k1k，max-concurrency:num-prompts=1:4
| Model      | dp | tp | moe_ep | moe_tp | sp | cp | Model Length | Total Length | Concurrency | RequestCount | TTFT(ms)   | TPOT(ms) | Median TPOT(ms) |
| ---------- | -- | -- | ------ | ------ | -- | -- | ------------ | ------------ | ----------- | ------------ | ---------- | -------- | --------------- |
| ds-r1-int8 | 1  | 8  | 16     | 1      | 8  | 2  | 32k(16k+16k) | 5k(4k+1k)    | 5           | 20           | 1737.15    | 95.70    | 94.70           |
| ds-r1-int8 | 1  | 8  | 16     | 1      | 8  | 2  | 32k(16k+16k) | 5k(4k+1k)    | 10          | 40           | 2960.43    | 97.17    | 97.11           |
| ds-r1-int8 | 1  | 8  | 16     | 1      | 8  | 2  | 32k(16k+16k) | 5k(4k+1k)    | 15          | 60           | 3954.52    | 97.72    | 97.33           |
| ds-r1-int8 | 1  | 8  | 16     | 1      | 8  | 2  | 32k(16k+16k) | 5k(4k+1k)    | 20          | 80           | 5127.07    | 100.60   | 100.32          |
| ds-r1-int8 | 1  | 8  | 16     | 1      | 8  | 2  | 32k(16k+16k) | 5k(4k+1k)    | 25          | 100          | 5834.68    | 105.64   | 105.61          |
| ds-r1-int8 | 1  | 8  | 16     | 1      | 8  | 2  | 32k(16k+16k) | 5k(4k+1k)    | 30          | 120          |    |    |            |
| ds-r1-int8 | 1  | 8  | 16     | 1      | 8  | 2  | 32k(16k+16k) | 5k(4k+1k)    | 35          | 140          |    |    |            |
| ds-r1-int8 | 1  | 8  | 16     | 1      | 8  | 2  | 32k(16k+16k) | 5k(4k+1k)    | 40          | 160          |    |    |            |
| ds-r1-int8 | 1  | 8  | 16     | 1      | 8  | 2  | 32k(16k+16k) | 5k(4k+1k)    | 45          | 180          |    |    |            |
| ds-r1-int8 | 1  | 8  | 16     | 1      | 8  | 2  | 32k(16k+16k) | 5k(4k+1k)    | 50          | 200          |    |    |            |

长序列推理配置，非 MTP 特性，适配 32k(16k+16k) 场景，ttft 和 tpot 性能趋势类似，无明显提升，且 ttft 和 tpot 均存在少许性能劣化；
