# 环境信息
- npu型号：300i pro (24G)
- 驱动：25.2.0
- 固件：7.7.0.6.236
- MindIE：swr.cn-south-1.myhuaweicloud.com/ascendhub/mindie:2.1.RC2-300I-Duo-py311-openeuler24.03-lts
- 模型：Qwen2.5-VL-3B-Instruct
从参数量更小的3B模型，这样单卡能运行起来

# 服务化 config.json 配置信息
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
        "npuDeviceIds" : [[0]],
        "multiNodesInferEnabled" : false,
        "interNodeTLSEnabled" : false,
        "ModelDeployConfig" :
        {
            "maxSeqLen" : 32768,
            "maxInputTokenLen" : 16384,
            "ModelConfig" : [
                {
                    "modelName" : "qwen2point5-vl-3b",
                    "modelWeightPath" : "/the/path/of/Qwen2point5-VL-3B-Instruct",
                    "worldSize" : 1,
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
            "maxPrefillTokens" : 16384,
            "maxBatchSize" : 200,
            "maxIterTimes" : 16384,
        }
    }
```

# 环境变量设置
写 `~/.bashrc` 然后 `source` 永久生效，
```shell
export PYTORCH_NPU_ALLOC_CONF=expandable_segments:True
export NPU_MEMORY_FRACTION=0.91
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
```
其中，`NPU_MEMORY_FRACTION`超过0.91，在32k(16k+16k)这种配置条件下，接收请求之后会出现`Segmentation fault (core dumped)`

# 测试方法
调用推理服务化的api请求，不带相关参数，不带推理后处理参数，
```shell
curl http://127.0.0.1:1025/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
  "model": "qwen2point5-vl-3b",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "请用中文详细描述这张图片的内容。"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "https://vpic-cover.puui.qpic.cn/m3543j2c1k1/m3543j2c1k1_1710906090_hz.jpg"
          }
        }
      ]
    }
  ]
}'
```

# 结果记录
32k(16k+16k) 推理服务化，全量环境变量设置（NPU_MEMORY_FRACTION=0.91），1280*720 图片分辨率，进行图片理解推理，
```json
{"id":"endpoint_common_0","object":"chat.completion","created":1759126165,"model":"qwen2point5-vl-3b","choices":[{"index":0,"message":{"role":"assistant","content":"这张图片展示了一幅美丽的自然景观，主要由山脉、湖泊和植被组成。画面中可以看到几座高耸的山峰，其中一座山峰特别突出，形状独特，像是一个尖锐的锥体，被称为“米尔福德角”。这座山峰被茂密的绿色植被覆盖，显得非常壮观。\n\n前景是一片广阔的湖泊，湖水清澈见底，反射出周围的景色。湖边有一些岩石和树木，增加了画面的层次感。远处的山脉延伸到天际线，天空晴朗，蓝天白云，给人一种宁静而开阔的感觉。\n\n整体来看，这幅图片展现了新西兰南岛米尔福德角地区的自然美景，是一个非常适合旅游和摄影的地方。","tool_calls":null},"logprobs":null,"finish_reason":"stop"}],"usage":{"prompt_tokens":1226,"completion_tokens":145,"total_tokens":1371,"batch_size":[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],"queue_wait_time":[5116,5204,78,46,49,88,60,58,56,40,56,58,63,51,33,45,53,53,42,43,26,23,18,20,17,18,17,18,18,19,19,22,41,34,50,49,42,40,36,23,24,20,31,45,38,47,24,20,20,20,18,18,18,17,21,39,27,31,34,45,46,48,38,45,57,66,57,65,59,61,66,63,57,49,46,28,22,29,57,54,58,45,36,54,55,49,63,50,49,48,38,32,23,19,46,53,43,38,34,40,37,38,32,30,23,23,18,19,20,23,36,45,70,54,43,45,35,22,25,24,37,42,46,35,32,24,19,21,17,20,17,20,58,59,64,65,57,67,62,69,56,57,50,31,22]},"prefill_time":1138,"decode_time_arr":[47,45,45,45,44,44,46,45,45,45,44,44,44,44,44,44,44,44,44,43,44,43,44,44,43,44,44,44,43,44,44,44,44,44,44,44,44,43,43,44,44,44,45,44,44,43,43,44,44,44,44,44,44,44,45,45,44,44,44,44,44,45,44,44,45,45,44,45,44,44,44,44,44,44,44,44,44,45,44,44,44,44,44,45,44,43,44,43,43,43,43,46,44,43,43,44,44,43,44,44,44,44,43,43,43,43,43,43,44,45,44,43,44,44,44,45,44,43,44,44,44,45,44,43,43,43,43,44,43,44,44,44,44,44,43,44,44,44,44,44,43,44,43,44]}
```
| 指标项           | 数值          |
| ---------------- | ------------- |
| 输入token数      | 1226          |
| 输出token数      | 145           |
| 总token数        | 1371          |
| 填充时间         | 1.14 秒        |
| 总解码时间       | 6.42 秒        |
| 总响应时间       | 7.56 秒        |
| 平均解码时间     | 44.3 ms/token  |
| Token生成速率    | 22.6 tokens/s |
| 平均队列等待时间  | 45.4 ms       |
| 最大队列等待时间  | 5204 ms       |
| 最小队列等待时间  | 17 ms         |

# 注意事项
- dtype 类型，300i pro，mindie 仅支持fp16（默认开源权重下 config.json 中dtype为 bf16 类型）；
- 图片类型， 仅支持 .jpg .jpeg .png 三种；

