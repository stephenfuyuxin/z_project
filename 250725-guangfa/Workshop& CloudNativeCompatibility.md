# Workshop

## 整理安排
基于 MindIE 推理全流程，安排如下，
| Index | Items |
| ----- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Day1  | OS 安装及 NPU 驱动源码编译所需依赖 <br> 容器化方案及版本配套关系与开源获取方法 <br> Docker 离线安装部署及修改工作目录 <br> MindIE 容器化镜像构建工程               | 
| Day2  | NPU 驱动固件安装与升级 <br> 参数面网络方案配置及检查 <br> MindIE 镜像申请与导入、环境变量设置、推理服务化参数 config.json 调整及优化 <br> 基于服务化的性能&精度验证 |
| Day3  | MindCluster（包含 Ascend-docker-runtime, Ascend-device-plugin） <br> MindIE 推理全流程的本地化改造 <br> 监控方案对比（Nvidia DCGM Exporter 与 NPU Exporter） |                                        |  

### 参考链接
Atlas 服务器 openEuler 22.03 LTS 操作系统 安装指南 (Arm) 09：https://support.huawei.com/enterprise/zh/doc/EDOC1100258040

NPU 驱动源码编译安装所需依赖：https://www.hiascend.com/document/detail/zh/canncommercial/82RC1/softwareinst/instg/instg_0051.html?Mode=PmIns&InstallType=local&OS=Debian&Software=cannToolKit

MindIE 安装说明->安装方案：https://www.hiascend.com/document/detail/zh/mindie/21RC1/envdeployment/instg/mindie_instg_0001.html

Ascend HDK, CANN, PTA, MindIE, MindCluster 版本配套关系以及开源社区版本获取方法（商发版需要申请），

Ascend HDK：https://www.hiascend.com/hardware/firmware-drivers/community?product=4&model=32&cann=8.2.RC1&driver=Ascend+HDK+25.2.0

Ascend CANN, PTA, MindIE, MindCluster：https://www.hiascend.com/developer/download/community/result?module=ie+pt+cann&product=4&model=32

Docker-ce 离线安装版本确认：https://download.docker.com/linux/static/stable/

Docker-ce 修改工作目录：https://cloud.tencent.com/developer/information/%E5%A6%82%E4%BD%95%E6%9B%B4%E6%94%B9docker%E7%9A%84%E7%9B%AE%E5%BD%95-album

MindIE 容器化镜像构建工程（aarch64, dockerfile, openEuler）：https://gitee.com/ascend/ascend-docker-image/blob/dev/mindie/aarch64/Dockerfile.openEuler

MindIE 商发版镜像申请：https://www.hiascend.com/developer/ascendhub/detail/af85b724a7e5469ebd7ea13c3439d48f

NPU 驱动固件安装与升级：https://www.hiascend.com/document/detail/zh/canncommercial/82RC1/softwareinst/instg/instg_0005.html?Mode=PmIns&InstallType=local&OS=Debian&Software=cannToolKit

参数面组网方案：https://support.huawei.com/enterprise/zh/doc/EDOC1100372014?idPath=23710424%257C251366513%257C22892968%257C258915651

参数面网络配置及检查：https://support.huawei.com/enterprise/zh/doc/EDOC1100493984/d8e72e25?idPath=23710424|251366513|254884019|261408772|252764743

MindIE 容器部署方案：https://www.hiascend.com/document/detail/zh/mindie/21RC1/envdeployment/instg/mindie_instg_0022.html

MindIE 多机推理部署方案（ranktable.json）：https://www.hiascend.com/document/detail/zh/mindie/21RC1/envdeployment/instg/mindie_instg_0027.html

MindIE-Service 服务化配置参数说明：https://www.hiascend.com/document/detail/zh/mindie/21RC1/mindieservice/servicedev/mindie_service0285.html

MindCluster 集群调度组件：https://www.hiascend.com/document/detail/zh/mindcluster/71RC1/clustersched/dlug/mxdlug_201.html

Ascend-Docker-Runtime：https://www.hiascend.com/document/detail/zh/mindcluster/71RC1/clustersched/dlug/mxdlug_003.html

Ascend-Device-Plugin：https://www.hiascend.com/document/detail/zh/mindcluster/71RC1/clustersched/dlug/mxdlug_005.html

Nvidia DCGM Exporter：https://blog.csdn.net/Franklin7B/article/details/145585589

NPU-Exporter：https://www.hiascend.com/document/detail/zh/mindcluster/71RC1/clustersched/dlug/mxdlug_004.html

### docker 离线部署方案
安装部署 docker-ce 离线包
- step1：下载 docker-ce 离线包

先通过官方下载链接确认宿主机架构及想要部署的 docker-ce 版本，链接如下，

https://download.docker.com/linux/static/stable/

通过链接下载指定架构/版本的离线包，

举例，aarch64 宿主机下载 docker-ce 版本 24.0.5 离线包，
```shell
wget -c https://download.docker.com/linux/static/stable/aarch64/docker-24.0.5.tgz
```

- step2：下载离线安装工具

链接如下，

https://github.com/Jrohy/docker-install/

- step3：将下载好的离线包放置到离线工具根目录下，如 `/root/setup/docker` ，

- step4：执行安装操作，
```shell
# cd /root/setup/docker
# chmod +x install.sh
# ./install.sh -f docker-24.0.5.tgz
```

### docker 工作目录修改
适用于全新/已安装 docker-ce 环境，默认工作目录为`/var/lib/docker/`，修改为`/path/to/new/docker`，

若 `/etc/docker/daemon.json` 文件或路径不存在，则通过手动创建，
```shell
# systemctl stop docker
# mkdir -p /path/to/new/docker
# rsync -aqxP /var/lib/docker/ /path/to/new/docker/
# vim /etc/docker/daemon.json
{
  "data-root": "/path/to/new/docker"
}
# systemctl start docker
```

### 参数面网络配置检查
基本网络状态设置、检查
- Item1：物理状态检查，
```shell
for i in {0..7}; do hccn_tool -i $i -lldp -g | grep Ifname; done
```

- Item2：链路状态检查，
```shell
for i in {0..7}; do hccn_tool -i $i -link -g ; done
```

- Item3：健康状态检查，
```shell
for i in {0..7}; do hccn_tool -i $i -net_health -g ; done
```

- Item4：参数面网卡IP地址及子网掩码设置，
```shell
hccn_tool -i 0 -ip -s address 10.248.138.216 netmask 255.255.255.0
hccn_tool -i 1 -ip -s address 10.248.138.217 netmask 255.255.255.0
hccn_tool -i 2 -ip -s address 10.248.138.218 netmask 255.255.255.0
hccn_tool -i 3 -ip -s address 10.248.138.219 netmask 255.255.255.0
hccn_tool -i 4 -ip -s address 10.248.138.220 netmask 255.255.255.0
hccn_tool -i 5 -ip -s address 10.248.138.221 netmask 255.255.255.0
hccn_tool -i 6 -ip -s address 10.248.138.222 netmask 255.255.255.0
hccn_tool -i 7 -ip -s address 10.248.138.223 netmask 255.255.255.0
```

- Item5：参数面网卡默认网关设置
```shell
hccn_tool -i 0 -gateway -s gateway 10.248.138.3
hccn_tool -i 1 -gateway -s gateway 10.248.138.3
hccn_tool -i 2 -gateway -s gateway 10.248.138.3
hccn_tool -i 3 -gateway -s gateway 10.248.138.3
hccn_tool -i 4 -gateway -s gateway 10.248.138.3
hccn_tool -i 5 -gateway -s gateway 10.248.138.3
hccn_tool -i 6 -gateway -s gateway 10.248.138.3
hccn_tool -i 7 -gateway -s gateway 10.248.138.3
```

- Item6：网关配置状态，
```shell
for i in {0..7}; do hccn_tool -i $i -gateway -g ; done
```

- Item7：交换网络IP状态侦测 -> 网关
```shell
for i in {0..7}; do hccn_tool -i $i -netdetect -g ; done
```

- Item8：参数面NPU卡IP检查，
```shell
for i in {0..7};do hccn_tool -i $i -ip -g; done
```

- Item9：检测NPU底层TLS行为一致性，
```shell
for i in {0..7}; do hccn_tool -i $i -tls -g ; done | grep switch
```

- Item10：NPU底层tls校验行为置0操作，
```shell
for i in {0..7};do hccn_tool -i $i -tls -s enable 0; done
```

- Item11：检测机器间互联情况，
```shell
# card_idx: 本机的第几张卡
# ip_address: npu卡的ip address
hccn_tool -i [card_idx] -ping -g address [ip_address]
```
根据参数面地址分布，使用循环方式检查互联情况，
```shell
for j in {0..7}; 
    do for i in {22..29};
        do hccn_tool -i ${j} -ping -g address 10.20.0.${i}; 
    done;
done
```

### MindIE 多机环境 ranktable.json 配置
根据参数面配置，编辑 ranktable.json 文件，ranktable.json 文件权限需要设置为640，
```shell
touch ranktable.json
chmod 640 ranktable.json
vim ranktable.json
```

ranktable.json 配置举例（以双机环境为例）
```json
{
    "version": "1.0",
    "server_count": "2",
    "server_list": [
        {
            "server_id": "Master节点IP地址",
            "container_ip": "Master节点容器IP地址",
            "device": [
                { "device_id": "0", "device_ip": "10.20.0.2", "rank_id": "0" }, 
                { "device_id": "1", "device_ip": "10.20.0.3", "rank_id": "1" },
                { "device_id": "2", "device_ip": "10.20.0.4", "rank_id": "2" },
                { "device_id": "3", "device_ip": "10.20.0.5", "rank_id": "3" },
                { "device_id": "4", "device_ip": "10.20.0.6", "rank_id": "4" },
                { "device_id": "5", "device_ip": "10.20.0.7", "rank_id": "5" },
                { "device_id": "6", "device_ip": "10.20.0.8", "rank_id": "6" },
                { "device_id": "7", "device_ip": "10.20.0.9", "rank_id": "7" }
            ]
        },
        {
            "server_id": "Slave节点IP地址",
            "container_ip": "Slave节点容器IP地址",
            "device": [
                { "device_id": "0", "device_ip": "10.20.0.10", "rank_id": "8" },
                { "device_id": "1", "device_ip": "10.20.0.11", "rank_id": "9" },
                { "device_id": "2", "device_ip": "10.20.0.12", "rank_id": "10" },
                { "device_id": "3", "device_ip": "10.20.0.13", "rank_id": "11" },
                { "device_id": "4", "device_ip": "10.20.0.14", "rank_id": "12" },
                { "device_id": "5", "device_ip": "10.20.0.15", "rank_id": "13" },
                { "device_id": "6", "device_ip": "10.20.0.16", "rank_id": "14" },
                { "device_id": "7", "device_ip": "10.20.0.17", "rank_id": "15" }
            ]
        }
    ],
    "status": "completed"
}
```

## docker run 开箱即用方案1
run.sh，这里
- `--network` 和 `--ipc` 使用 `host`；
- 通过 `--device` 本地持久化 npu 相关资源给容器占用；
- 取消使用 `--privileged` 特权模式；

```shell
#!/bin/bash
IMAGE='docker2.gf.com.cn/aims2/ascendhub/mindie:2.1.RC1-800I-A2-py311-openeuler24.03-lts-arm64'
docker run -it --rm --name deepseek-r1-test \
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
    -v /etc/localtime:/etc/localtime:ro \
    -v /usr/local/sbin/npu-smi:/usr/local/sbin/npu-smi \
    -v /var/log/npu/slog/:/var/log/npu/slog \
    -v /usr/local/Ascend/driver:/usr/local/Ascend/driver \
    -v /usr/local/Ascend/add-ons/:/usr/local/Ascend/add-ons/ \
    -v /var/log/npu/conf/slog/slog.conf:/var/log/npu/conf/slog/slog.conf \
    -v /etc/hccn.conf:/etc/hccn.conf \
    -v /usr/local/Ascend/firmware:/usr/local/Ascend/firmware \
    -v /usr/local/sbin/:/usr/local/sbin/ \
    -v /data:/data \
    -v /root/deepseek-r1-start/r1-config.json:/usr/local/Ascend/mindie/latest/mindie-service/conf/config.json \
    -v /root/deepseek-r1-start/ranktable.json:/etc/mindie_ranktable.json:ro \
    -e PYTORCH_NPU_ALLOC_CONF=expandable_segments:True \
    -e NPU_MEMORY_FRACTION=0.97 \
    -e ATB_WORKSPACE_MEM_ALLOC_ALG_TYPE=3 \
    -e ATB_WORKSPACE_MEM_ALLOC_GLOBAL=1 \
    -e OMP_NUM_THREADS=10 \
    -e HCCL_DETERMINISTIC=false \
    -e HCCL_OP_EXPANSION_MODE="AIV" \
    -e ATB_LLM_HCCL_ENABLE=1 \
    -e ATB_LLM_COMM_BACKEND="hccl" \
    -e INF_NAN_MODE_ENABLE=1 \
    -e TASK_QUEUE_ENABLE=2 \
    -e CPU_AFFINITY_CONF=1 \
    -e ASCEND_LAUNCH_BLOCKING="" \
    -e ATB_LAYER_INTERNAL_TENSOR_REUSE=1 \
    -e ATB_OPENATION_EXECUTE_ASYNC=1 \
    -e ATB_CONVERT_NCHW_TO_ND=1 \
    -e MINDIE_ASYNC_SCHEDULING_ENABLE=1 \
    -e ATB_CONTEXT_WORKSPACE_SIZE=0 \
    -e ATB_LAUNCH_KERNEL_WITH_TILING=1 \
    -e ATB_LLM_ENABLE_AUTO_TRANSPOSE=0 \
    -e HCCL_CONNECT_TIMEOUT=7200 \
    -e HCCL_EXEC_TIMEOUT=0 \
    -e HCCL_RDMA_PCIE_DIRECT_POST_NOSTRICT=TRUE \
    -e MIES_CONTAINER_IP=10.129.155.203 \
    -e RANK_TABLE_FILE=/etc/mindie_ranktable.json \
    --workdir /usr/local/Ascend/mindie/latest/mindie-service/bin \
    --ipc=host \
    --network=host \
    ${IMAGE} \
    /usr/local/Ascend/mindie/latest/mindie-service/bin/mindieservice_daemon
```

## docker run 开箱即用方案2
run.sh，这里
- `--network` 和 `--ipc` 使用 `host`；
- 通过 ascend-docker-runtime 将 `-–device` 替换为通过 `ASCEND_VISIBLE_DEVICES` 控制 NPU 数量，并删除相应应 `-v` 操作；
- 取消使用 `--privileged` 特权模式；

ASCEND_VISIBLE_DEVICES 环境变量的使用方法：https://www.hiascend.com/document/detail/zh/mindcluster/71RC1/clustersched/dlug/dlruntime_ug_004.html
- `ASCEND_VISIBLE_DEVICES=0` 表示将0号设备（/dev/davinci0）挂载入容器中
- `ASCEND_VISIBLE_DEVICES=1,3` 表示将1、3号设备挂载入容器中
- `ASCEND_VISIBLE_DEVICES=0-2` 表示将0号至2号设备（包含0号和2号）挂载入容器中，效果同 ASCEND_VISIBLE_DEVICES=0,1,2
- `ASCEND_VISIBLE_DEVICES=0-2,4` 表示将0号至2号以及4号设备挂载入容器，效果同 ASCEND_VISIBLE_DEVICES=0,1,2,4

```shell
#!/bin/bash
IMAGE='docker2.gf.com.cn/aims2/ascendhub/mindie:2.1.RC1-800I-A2-py311-openeuler24.03-lts-arm64'
docker run -it --rm --name deepseek-r1-test \
    --shm-size 500g \
    -e ASCEND_VISIBLE_DEVICES=0-7 \
    -v /etc/localtime:/etc/localtime:ro \
    -v /data:/data \
    -v /root/deepseek-r1-start/r1-config.json:/usr/local/Ascend/mindie/latest/mindie-service/conf/config.json \
    -v /root/deepseek-r1-start/ranktable.json:/etc/mindie_ranktable.json:ro \
    -e PYTORCH_NPU_ALLOC_CONF=expandable_segments:True \
    -e NPU_MEMORY_FRACTION=0.97 \
    -e ATB_WORKSPACE_MEM_ALLOC_ALG_TYPE=3 \
    -e ATB_WORKSPACE_MEM_ALLOC_GLOBAL=1 \
    -e OMP_NUM_THREADS=10 \
    -e HCCL_DETERMINISTIC=false \
    -e HCCL_OP_EXPANSION_MODE="AIV" \
    -e ATB_LLM_HCCL_ENABLE=1 \
    -e ATB_LLM_COMM_BACKEND="hccl" \
    -e INF_NAN_MODE_ENABLE=1 \
    -e TASK_QUEUE_ENABLE=2 \
    -e CPU_AFFINITY_CONF=1 \
    -e ASCEND_LAUNCH_BLOCKING="" \
    -e ATB_LAYER_INTERNAL_TENSOR_REUSE=1 \
    -e ATB_OPENATION_EXECUTE_ASYNC=1 \
    -e ATB_CONVERT_NCHW_TO_ND=1 \
    -e MINDIE_ASYNC_SCHEDULING_ENABLE=1 \
    -e ATB_CONTEXT_WORKSPACE_SIZE=0 \
    -e ATB_LAUNCH_KERNEL_WITH_TILING=1 \
    -e ATB_LLM_ENABLE_AUTO_TRANSPOSE=0 \
    -e HCCL_CONNECT_TIMEOUT=7200 \
    -e HCCL_EXEC_TIMEOUT=0 \
    -e HCCL_RDMA_PCIE_DIRECT_POST_NOSTRICT=TRUE \
    -e MIES_CONTAINER_IP=10.129.155.203 \
    -e RANK_TABLE_FILE=/etc/mindie_ranktable.json \
    --workdir /usr/local/Ascend/mindie/latest/mindie-service/bin \
    --ipc=host \
    --network=host \
    ${IMAGE} \
    /usr/local/Ascend/mindie/latest/mindie-service/bin/mindieservice_daemon
```

## docker run 开箱即用方案3
开箱即用方案3即非主机网络开箱即用方案，本质上仍然是启动容器之后，根据实际环境设置环境变量之后，再启动推理服务化方式，并不能达到主机网络开箱即用方案2 **启动即服务** 的方式；

run.sh，这里
- `--network` 取消 host 设置，通过端口映射，通过 `-p` 将 MindIE 相关端口进行暴露；
- `--ipc` 取消 host 设置，通过 `--shm-size 500g` 进行指定；
- 通过 ascend-docker-runtime 将 `-–device` 替换为通过 `ASCEND_VISIBLE_DEVICES` 控制 NPU 数量，并删除相应应 `-v` 操作；
- 取消使用 `--privileged` 特权模式；

```shell
#!/bin/bash
IMAGE='docker2.gf.com.cn/aims2/ascendhub/mindie:2.1.RC1-800I-A2-py311-openeuler24.03-lts-arm64'
docker run -itd --name deepseek-r1-test \
    --shm-size 500g \
    -e ASCEND_VISIBLE_DEVICES=0-7 \
    -v /etc/localtime:/etc/localtime:ro \
    -v /data:/data \
    -v /root/deepseek-r1-start/r1-config.json:/usr/local/Ascend/mindie/latest/mindie-service/conf/config.json \
    -v /root/deepseek-r1-start/ranktable.json:/etc/mindie_ranktable.json:ro \
    -e PYTORCH_NPU_ALLOC_CONF=expandable_segments:True \
    -e NPU_MEMORY_FRACTION=0.97 \
    -e ATB_WORKSPACE_MEM_ALLOC_ALG_TYPE=3 \
    -e ATB_WORKSPACE_MEM_ALLOC_GLOBAL=1 \
    -e OMP_NUM_THREADS=10 \
    -e HCCL_DETERMINISTIC=false \
    -e HCCL_OP_EXPANSION_MODE="AIV" \
    -e ATB_LLM_HCCL_ENABLE=1 \
    -e ATB_LLM_COMM_BACKEND="hccl" \
    -e INF_NAN_MODE_ENABLE=1 \
    -e TASK_QUEUE_ENABLE=2 \
    -e CPU_AFFINITY_CONF=1 \
    -e ASCEND_LAUNCH_BLOCKING="" \
    -e ATB_LAYER_INTERNAL_TENSOR_REUSE=1 \
    -e ATB_OPENATION_EXECUTE_ASYNC=1 \
    -e ATB_CONVERT_NCHW_TO_ND=1 \
    -e MINDIE_ASYNC_SCHEDULING_ENABLE=1 \
    -e ATB_CONTEXT_WORKSPACE_SIZE=0 \
    -e ATB_LAUNCH_KERNEL_WITH_TILING=1 \
    -e ATB_LLM_ENABLE_AUTO_TRANSPOSE=0 \
    -e HCCL_CONNECT_TIMEOUT=7200 \
    -e HCCL_EXEC_TIMEOUT=0 \
    -e HCCL_RDMA_PCIE_DIRECT_POST_NOSTRICT=TRUE \
    --workdir /usr/local/Ascend/mindie/latest/mindie-service/bin \
    -p xxxx:xxxx
    ${IMAGE} \
    /bin/bash
```

对于非主机网络的场景，`MIES_CONTAINER_IP` 需要配置为 `container` 的 IP，由于容器启动前无法预知，只能通过启动脚本动态配置进行变通。ranktable.json 相关的环境变量同理，
```shell
export MIES_CONTAINER_IP=10.129.155.202
export RANK_TABLE_FILE=/etc/mindie_ranktable.json
```
非主机网络，端口映射场景，上述环境变量需要先启动容器后再单独设置并使能之后，再启动 MindIE 推理服务化，否则服务化启动失败；

### --network 主机网络 or 端口映射
容器方案在生产环境不得使用主机网络的原因，客户只考虑端口映射的方式，从几个方面说明，

#### 端口冲突与隔离性
- 主机网络：容器直接使用宿主机IP和端口，所有容器共享同一网络命名空间；

    风险：若多个容器监听同一端口（如80/443），会直接冲突，需人工协调端口分配，运维复杂度指数级上升；

    案例：微服务架构中，10个Web服务需映射到宿主机不同端口（如8080-8089），管理困难；

- 端口映射：每个容器拥有独立的虚拟网络栈，通过宿主机端口转发到容器端口（如-p 8080:80），避免冲突，天然隔离；

#### 安全性与攻击面控制
- 主机网络：容器进程可访问宿主机所有网络接口（包括localhost），绕过防火墙规则；

    风险：若容器被入侵，攻击者可直接扫描宿主机上的其他服务（如数据库、SSH）；

    案例：2019年某云厂商因容器使用主机网络，导致攻击者通过容器访问宿主机Redis未授权端口；

- 端口映射：仅暴露显式指定的端口（如-p 80:80），其他端口默认隔离，缩小攻击面；

#### 可扩展性与编排系统兼容性
- 主机网络：无法在Kubernetes、Swarm等编排系统中直接使用（K8s默认禁止hostNetwork，除非显式声明）；

    原因：编排系统依赖服务发现（如K8s Service、Ingress），需通过端口映射或CNI插件动态分配端口；

    案例：K8s中部署100个Nginx实例，若用主机网络，需手动分配100个不同宿主机端口，无法通过Service负载均衡；

- 端口映射：与编排系统的服务抽象天然兼容（如K8s的ClusterIP+NodePort），支持水平扩展；

#### 可观测性与故障排查
- 主机网络：容器网络流量与宿主机混杂，难以区分容器间通信，导致监控和故障排查困难；

    问题：tcpdump抓包时需过滤大量宿主机流量，无法直观定位某个容器的异常连接；

- 端口映射：每个容器网络隔离，可独立抓包、监控端口流量（如docker logs结合端口映射日志）；

#### 合规与审计需求
- 主机网络：直接暴露宿主机网络栈，违反等保2.0等合规要求（需网络分区分域）；

    案例：金融行业要求容器必须运行在隔离的虚拟网络中，禁止直接使用主机网络；

- 端口映射：满足合规性，通过显式端口暴露+防火墙规则实现精细控制；

### --ipc 进程间通信 共享 or 独占
默认情况下，Docker 会给每个容器创建一个独立的 IPC 命名空间，因此容器内的 /dev/shm 默认只有 64MB，且与其他容器隔离；

如果只是为了扩大 /dev/shm，可以用 `--shm-size` 而不是 `--ipc host` 方式

结论：
- 生产环境慎用 --ipc host，除非明确需要与宿主机共享 IPC 命名空间。
- 更推荐 --shm-size 来扩大共享内存，同时保持隔离性。

## CloudNativeCompatibility
其他内容及云原生平台适配

### 讨论 vllm-ascend sglang-ascend 实现方式
vllm 提供已适配 ascend 的镜像，sglang 提供基于 ascend 的实践指导，并提供 dockerfile 镜像工程构建举例，

vllm-ascend images：https://quay.io/repository/ascend/vllm-ascend?tab=tags

SGLang on Ascend NPUs：https://docs.sglang.ai/platforms/ascend_npu.html#method-2-using-docker

### 是否支持结构化输出
nvidia-smi 支持 --query-gpu=xxx --format=xxx 这种 csv, json  原生的结构化输出方式。npu-smi info 仅支持纯文本表格格式，需要通过额外手段（如正则表达式、Python脚本或pandas）进行解析和结构化处理。

以下为 nvidia-smi 结构化输出示例，
- 查询当前系统中所有 GPU 的 UUID 和名称
- 输出格式为 CSV，不显示表头（noheader），不显示单位（nounits），只输出纯数据，方便脚本或程序解析

```shell
[root@gd-alo-nodel ~]# nvidia-smi
Tue Aug 19 10:59:10 2025
+---------------------------------------------------------------------------------------+
| NVIDIA-SMI 535.161.08              Driver Version: 535.161.08     CUDA Version: 12.2  |
|-----------------------------------------+----------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |         Memory-Usage | GPU-Util  Compute M. |
|                                         |                      |               MIG M. |
|=========================================+======================+======================|
|   0  NVIDIA A10                    Off  | 00000000:31:00.0 Off |                    0 |
|  0%   77C    P0             84W / 150W  |  1048MiB / 23028MiB  |      0%      Default |
|                                         |                      |                  N/A |
+-----------------------------------------+----------------------+----------------------+
|   1  NVIDIA A10                    Off  | 00000000:98:00.0 Off |                    0 |
|  0%   35C    P8             15W / 150W  |     0MiB / 23028MiB  |      0%      Default |
|                                         |                      |                  N/A |
+-----------------------------------------+----------------------+----------------------+

+---------------------------------------------------------------------------------------+
| Processes:                                                                            |
|  GPU   GI   CI        PID   Type   Process name                          GPU Memory   |
|        ID   ID                                                           Usage        |
|=======================================================================================|
|    0   N/A  N/A      7461      C   /opt/conda/bin/python                   1040MiB    |
+---------------------------------------------------------------------------------------+

[root@gd-alo-nodel ~]# nvidia-smi --query-gpu=gpu_uuid,name --format=csv,noheader,nounits
GPU-78bf0df8-e7c2-5872-1941-77f20247485e, NVIDIA A10
GPU-f6de7733-951f-5ee3-97b4-f0288118e31c, NVIDIA A10
[root@gd-alo-nodel ~]#
```

### 平台监控能力
监控能力，Nvidia DCGM Exporter（Data Center GPU Manager），NV 原厂监控组件，轻量化部署（一条命令完成安装），数据采集、整合、分析图表等，可独立运作，可结合第三方开源监控组件，

csdn：https://blog.csdn.net/Franklin7B/article/details/145585589

对应昇腾为 NPU Exporter，更像一个采集器，无法独立运作，需要结合第三方开源监控组件，Prometheus 或 Telegraf，通过 api 完成北向对接之后使用

组件介绍：https://www.hiascend.com/document/detail/zh/mindcluster/71RC1/clustersched/dlug/mxdlug_004.html

资源监测：https://www.hiascend.com/document/detail/zh/mindcluster/71RC1/clustersched/dlug/mxdlug_015.html

资源监测特性指南：https://www.hiascend.com/document/detail/zh/mindcluster/71RC1/clustersched/dlug/mxdlug_monit_001.html

NPU Exporter 昇腾镜像仓库：https://www.hiascend.com/developer/ascendhub/detail/1b1a8c3cc1ff4710bdb0222514a8a7a3

```shell
#!/bin/bash
IMAGE=docker2.gf.com.cn/aims2/ascendhub/npu-exporter:v7.1.RC1
docker run -d \
  --name npu-exporter \
  --privileged \
  --user 0:0 \
  --read-only \
  --restart unless-stopped \
  -p 8082:8082 \
  -v /var/log/mindx-dl/npu-exporter:/var/log/mindx-dl/npu-exporter \
  -v /etc/localtime:/etc/localtime:ro \
  -v /usr/local/Ascend/driver:/usr/local/Ascend/driver:ro \
  -v /usr/local/dcmi:/usr/local/dcmi:ro \
  -v /sys:/sys:ro \
  -v /var/run/docker:/var/run/docker:ro \
  -v /run/containerd:/run/containerd:ro \
  -v /tmp:/tmp \
  "${IMAGE}" \
  /bin/bash -c "umask 027; npu-exporter -port=8082 -ip=0.0.0.0 -updateTime=5 -logFile=/var/log/mindx-dl/npu-exporter/npu-exporter.log -logLevel=0 -containerMode=docker"
```
在 grafana 上 可以找到 ascend 面板，链接如下，

https://grafana.com/grafana/dashboards/20592-ascend-npu-exporter/

对昇腾AI处理器资源各种数据信息的实时监测，可实时获取昇腾AI处理器利用率、温度、电压、内存，以及昇腾AI处理器在容器中的分配状况等信息，实现资源的实时监测。支持对虚拟NPU（vNPU）的AI Core利用率、vNPU总内存和vNPU使用中内存进行监测，
大部分指标都有，通过左下角看起来昇腾是把DDR内存和HBM分成了两个不同的指标，根据卡的类型，可能有所差异，






