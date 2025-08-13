# 现象
配置 mtp 特性 config.json 之后，启动 mindieservice 服务化拉起失败

# 环境变量
```shell
export MINDIE_LOG_LEVEL=INFO
export MINDIE_LOG_STDOUT=1
```

日志获取完毕之后，需要去使能，影响性能，
```shell
unset MINDIE_LOG_LEVEL
unset MINDIE_LOG_STDOUT
```

# 错误获取与分析
获取报错信息方式，
```shell
grep -rn ERR /root/mindie/log
```

错误关键信息如下，
```shell
/root/mindie/log/debug/mindie-batchscheduler_47502_20250806112052041.log:42:[2025-08-06 11:21:44.006+0800] [47502] [281473508503904] [batchscheduler] [ERROR] [model.py:61] : [Model]   >>> Exception:'model.layers.61.self_attn.q_a_proj.weight'
```

怀疑 mtp 所需 deepseek-r1 的 quant_model_description_w8a8_dynamic.json 和 quant_model_weight_w8a8_dynamic.index.json 文件异常，检查发现，原有文件与所需文件 md5sum 结果不同，因此替换，将原有文件 .bak 后缀，将所需文件放入权重路径，
```shell
[root@localhost DeepSeek-R1-bf16-hfd-w8a8]# md5sum quant_model_description_w8a8_dynamic.json.bak
2248fa8f24bc6b68ec94f013208140cd  quant_model_description_w8a8_dynamic.json.bak
[root@localhost DeepSeek-R1-bf16-hfd-w8a8]# md5sum quant_model_description_w8a8_dynamic.json
c5143d44593f13dd8dc73a6de831313f  quant_model_description_w8a8_dynamic.json
[root@localhost DeepSeek-R1-bf16-hfd-w8a8]# md5sum quant_model_weight_w8a8_dynamic.index.json.bak
ed2618b6c95832bccd8dbb44fd7862f8  quant_model_weight_w8a8_dynamic.index.json.bak
[root@localhost DeepSeek-R1-bf16-hfd-w8a8]# md5sum quant_model_weight_w8a8_dynamic.index.json
34eb4be45d07ac2ebd04508dec9079c5  quant_model_weight_w8a8_dynamic.index.json
```

# 解决方法
将所需 quant_model_description_w8a8_dynamic.json 和 quant_model_weight_w8a8_dynamic.index.json 放入权重路径，对原有的文件进行 .bak 后缀化，

文件获取链接，https://docs.qq.com/sheet/DVkFYbnBDd3JvV0VN?tab=u59jn7

quant_model_description_w8a8_dynamic.json
```shell
https://poc-resource.obs.cn-south-1.myhuaweicloud.com:443/%E6%A8%A1%E5%9E%8B%E6%9D%83%E9%87%8D/deepseek-r1-w8a8-mtp-only/quant_model_description_w8a8_dynamic.json?AccessKeyId=TRRYAVJVC5ETCYNIGOSG&Expires=1776521710&Signature=QXTtYNScot6pfHNSU1Yp8iEpNH4%3D
```
quant_model_weight_w8a8_dynamic.index.json
```shell
https://poc-resource.obs.cn-south-1.myhuaweicloud.com:443/%E6%A8%A1%E5%9E%8B%E6%9D%83%E9%87%8D/deepseek-r1-w8a8-mtp-only/quant_model_weight_w8a8_dynamic.index.json?AccessKeyId=TRRYAVJVC5ETCYNIGOSG&Expires=1776521721&Signature=ruOxBax7opghJJE0JT3inIiGNQ8%3D
```

