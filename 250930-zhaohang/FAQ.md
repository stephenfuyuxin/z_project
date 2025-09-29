# 300i pro (24G) 两卡 MindIE 启动 Qwen2.5-VL-7B 报错信息

## 环境信息
- npu型号：300i pro (24G)
- 驱动：25.2.0
- 固件：7.7.0.6.236
- MindIE：swr.cn-south-1.myhuaweicloud.com/ascendhub/mindie:2.1.RC2-300I-Duo-py311-openeuler24.03-lts
- 模型：Qwen2.5-VL-7B-Instruct

## 服务化 config.json 配置信息
部分配置，
```json
    "ServerConfig" :
    {
        "ipAddress" : "127.0.0.1",
        "managementIpAddress" : "127.0.0.2",
        "port" : 1025,
        "managementPort" : 1026,
        "httpsEnabled" : false,
        "interCommTLSEnabled" : false,
        "tokenTimeout" : 3600,
        "e2eTimeout" : 3600,
    },
    "BackendConfig" : {
        "npuDeviceIds" : [[0,1]],
        "multiNodesInferEnabled" : false,
        "interNodeTLSEnabled" : false,
        "ModelDeployConfig" :
        {
            "maxSeqLen" : 4096,
            "maxInputTokenLen" : 2048,
            "ModelConfig" : [
                {
                    "modelName" : "qwen2point5-vl-7b",
                    "modelWeightPath" : "/the/path/of/Qwen2point5-VL-7B-Instruct",
                    "worldSize" : 2,
                    "cpuMemSize" : 5,
                    "npuMemSize" : -1,
                    "backendType" : "atb",
                    "trustRemoteCode" : false
                }
            ]
        },
        "ScheduleConfig" :
        {
            "maxPrefillBatchSize" : 50,
            "maxPrefillTokens" : 2048,
            "maxBatchSize" : 200,
            "maxIterTimes" : 2048,
        }
    }
```

## 环境变量设置
```shell
export ASDOPS_LOG_LEVEL=ERROR
export ASDOPS_LOG_TO_STDOUT=1
```

## 报错信息
开启日志打印之后，启动服务化报错回显，
```shell
[xxxx-xx-xx xx:xx:xx.910257] [error] [57624] [hccl_runner.cpp:169] AllReduceHcclRunner:0 HcclGetRootInfo fail, error:1, rank:0
[xxxx-xx-xx xx:xx:xx.911043] [error] [57624] [comm_pool.h:42] CommPool commCreateFunc fail
[xxxx-xx-xx xx:xx:xx.911054] [error] [57624] [hccl_runner.cpp:72] AllReduceHcclRunner:0 get hccl comm fail by rank:0
[xxxx-xx-xx xx:xx:xx.911913] [error] [57624] [hccl_runner.cpp:169] AllReduceHcclRunner:0 HcclGetRootInfo fail, error:1, rank:0
[xxxx-xx-xx xx:xx:xx.911979] [error] [57624] [comm_pool.h:42] CommPool commCreateFunc fail
[xxxx-xx-xx xx:xx:xx.911989] [error] [57624] [hccl_runner.cpp:72] AllReduceHcclRunner:0 get hccl comm fail by rank:0
[xxxx-xx-xx xx:xx:xx.930050] [error] [57624] [hccl_runner.cpp:169] AllReduceHcclRunner:0 HcclGetRootInfo fail, error:1, rank:0
[xxxx-xx-xx xx:xx:xx.930171] [error] [57624] [comm_pool.h:42] CommPool commCreateFunc fail
[xxxx-xx-xx xx:xx:xx.930181] [error] [57624] [hccl_runner.cpp:72] AllReduceHcclRunner:0 get hccl comm fail by rank:0
[xxxx-xx-xx xx:xx:xx.930527] [error] [58010] [all_reduce_hccl_runner.cpp:38] hcclComm is null, rank: 0
[xxxx-xx-xx xx:xx:xx.930577] [error] [58010] [runner.cpp:132] AllReduceHcclRunner_2_0_4_1:1 Execute Failed. st: 28
[xxxx-xx-xx xx:xx:xx.930593] [error] [58010] [graph_runner.cpp:976] LinearRowParallelNoAddRunner_2_0_4:0  node[1] execute fail, runner name:AllReduceHcclRunner
[xxxx-xx-xx xx:xx:xx.930606] [error] [58010] [runner.cpp:132] LinearRowParallelNoAddRunner_2_0_4:1 Execute Failed. st: 28
[xxxx-xx-xx xx:xx:xx.930613] [error] [58010] [graph_runner.cpp:976] AttentionRunner_2_0:0  node[4] execute fail, runner name:LinearRowParallelNoAddRunner
[xxxx-xx-xx xx:xx:xx.930622] [error] [58010] [runner.cpp:132] AttentionRunner_2_0:1 Execute Failed. st: 28
[xxxx-xx-xx xx:xx:xx.930627] [error] [58010] [graph_runner.cpp:976] Prefill_layerRunner_2:0  node[0] execute fail, runner name:AttentionRunner
[xxxx-xx-xx xx:xx:xx.930634] [error] [58010] [runner.cpp:132] Prefill_layerRunner_2:1 Execute Failed. st: 28
[xxxx-xx-xx xx:xx:xx.930639] [error] [58010] [operation_base.cpp:1023] Prefill_layer_2 execute Prefill_layerRunner fail
[xxxx-xx-xx xx:xx:xx.930645] [error] [58010] [operation_base.cpp:1100] Prefill_layer_2 Launch fail, error code: 28
[xxxx-xx-xx xx:xx:xx.930979] [error] [57624] [hccl_runner.cpp:169] AllReduceHcclRunner:0 HcclGetRootInfo fail, error:1, rank:0
[xxxx-xx-xx xx:xx:xx.931041] [error] [57624] [comm_pool.h:42] CommPool commCreateFunc fail
[xxxx-xx-xx xx:xx:xx.931050] [error] [57624] [hccl_runner.cpp:72] AllReduceHcclRunner:0 get hccl comm fail by rank:0**
```
