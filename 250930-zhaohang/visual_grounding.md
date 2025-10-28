# 基础配置
ascend 300i pro(24G), mindie, qwen2.5-vl-3b-instruct

# 参考链接
拿 Qwen3-VL cookbooks 中有关 Object Grounding 为例：

https://github.com/QwenLM/Qwen3-VL/blob/main/cookbooks/2d_grounding.ipynb

# mindie config.json
部分配置，还是32k(16k+16k)的配置基本不变
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
没有设置环境变量，仅验证功能，

# 推理服务化验证
目前 Qwen2.5-VL-3B 的 bbox 输出默认只包含坐标和类别标签，但可以通过设计 Prompt 或后处理，让模型把“标注内容”也一起打印出来，

Qwen2.5-VL 系列支持视觉定位（Visual Grounding），
- bbox和label，可以输出 bbox 坐标和类别标签；
- 结构化输出，默认输出格式是 JSON，包含 label 和 bbox；

可以在输入 Prompt 中明确要求模型不仅输出坐标，还要输出该区域的文字或描述，示例 Prompt 如下，

请识别图中所有文字区域，并用 bbox 标出位置，同时输出每个框内的文字内容，
```json
[{"bbox": [x1, y1, x2, y2], "text": "框内文字"}]
```
这种方式在 OCR 或文档理解任务中有效，尤其适用于 Qwen2.5-VL 的多语言 OCR 能力。或者结合 OCR 模型（Qwen-OCR）进行推理结果处理，拿到 bbox 坐标之后对裁剪区域进行二次识别，

测试方法如下，通过提示词强制要求标注图片中的数字并打印，
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
          "text": "Please locate all numbers in this image, read out the exact digit string inside each bounding box, and return a JSON list like [{\"bbox_2d\": [x1,y1,x2,y2], \"digits\": \"0\"}, ...]."
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "https://s18.mogucdn.com/b7/pic/150314/1h38m0_ie2wimrumqzgkztfmyytambqhayde_800x1200.jpg_880x999.jpg"
          }
        }
      ]
    }
  ]
}'
```
结果如下，这里是经过调整之后的 JSON 输出，
```json
{
  "id": "endpoint_common_26",
  "object": "chat.completion",
  "created": 1760428782,
  "model": "qwen2point5-vl-3b",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "```json\n[{\"bbox_2d\": [300, 670, 435, 829], \"digits\": \"13\"}]\n```"
      },
      "logprobs": null,
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 1317,
    "completion_tokens": 41,
    "total_tokens": 1358,
    "batch_size": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "queue_wait_time": [5122, 37, 21, 17, 16, 16, 16, 16, 17, 17, 16, 16, 17, 16, 15, 17, 15, 15, 16, 16, 15, 15, 15, 15, 17, 15, 16, 15, 16, 15, 15, 15, 16, 16, 16, 16, 16, 15, 15, 16, 15]
  },
  "prefill_time": 1025,
  "decode_time_arr": [45, 44, 44, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 44, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43]
}
```
