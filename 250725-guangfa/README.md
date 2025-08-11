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

## MindIE 下 config.json 配置
- 混合并行 MLA 策略按照 dp:tp:moe_ep:moe_tp:sp 配置说明；
- 混合并行 MLA + MTP 配置中涉及 cp 配置策略，按照 dp:tp:moe_ep:moe_tp:sp:cp 配置说明；
- 其他配置参考对应章节；

### MLA 2,8,4,4,1 配置


### MLA 2,8,16,1,8 配置


### MLA 2,8,4,4,1 + 使能 MTP 配置


### MLA 2,8,4,4,1 + 去使能 MTP 配置


### MLA 1,8,16,1,8,2 + 使能 MTP 配置
适用于长序列推理，按照现场配置进行改造使用，

### MLA 1,8,16,1,8,2 + 去使能 MTP 配置
仅把长序列推理的推荐配置去使能 MTP 特性之后，按照现场配置进行改造使用，

## MindIE 下 env 环境变量配置
通过写 `bashrc` 的方式，使环境变量在推理后端永久生效
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

# 性能数据
## MindIE benchmark
以 MindIE 版本，分为三个版本 MindIE 
