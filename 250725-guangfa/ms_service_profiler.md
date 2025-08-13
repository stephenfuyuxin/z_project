# 配置 ms_service_profilling 环境变量
多机场景，在主节点上，拉起 mindie 服务化之前，先配置 profilling 所需环境变量（该环境变脸只需要在主节点上配置即可），
```shell
export SERVICE_PROF_CONFIG_PATH=/the/path/of/ms_service_profiler_config.json
```
实际配置如下，
```shell
export SERVICE_PROF_CONFIG_PATH=/data/fuyuxin/ms_service_profiler_config.json
```
若需要取消环境变量配置，则
```shell
unset ERVICE_PROF_CONFIG_PATH
```

# 配置 ms_service_profiler_config.json 文件
配置参数如下，
- enable：表示日志采集启停，可以动态配置；
- prof_dir：表示 profiling 存放路径，根据实际情况先创建所需目录；
- acl_task_time：表示采集算子信息（保存文件非常大，平时建议不开）；
- timelimit：表示采集时间；

配置示例，
```shell
# vim /the/path/of/ms_service_profiler_config.json
```
```json
{
    "enable": 0,
    "prof_dir": "/the/path/of/profile",
    "host_system_usage_freq": -1,
    "npu_memory_usage_freq": -1,
    "acl_task_time": 1,
    "timelimit": 4
}
```

实际配置如下，
先创建日志收集 profile 目录，取消对算子信息的采集（删掉）， 采集时间可自定义设置（4->8），
```json
{
    "enable": 0,
    "prof_dir": "/data/fuyuxin/profile",
    "host_system_usage_freq": -1,
    "npu_memory_usage_freq": -1,
    "timelimit": 8
}
```

# 操作方法
- 配置 ERVICE_PROF_CONFIG_PATH 环境变量，拉起 mindie 服务化；
- 创建 profiling 存放路径，编辑 ms_service_profiler_config.json 文件，参数 enable 先设置为0，待 benchmark 性能测试拉起之后，在中间阶段再 enable 设置为1，采集中间数据；

# 采集完数据处理
参考配置如下，
```shell
source /usr/local/Ascend/ascend-toolkit/set_env.sh
python3 -m ms_service_profiler.parse --input-path=(数据落盘的 prof_dir 绝对路径) --output-path=(生成文件路径，不添加默认在当前文件夹下生成 output 文件夹)
```

实际执行如下，
```shell
python3 -m ms_service_profiler.parse --input-path=/data/fuyuxin/profile --output-path=/data/fuyuxin/output
```

# FAQ

## 执行采集完数据处理，报错，报错信息为 profile 目录为空，但 profile 中已采集到数据
先确定 toolkit 下 compiler 版本，
```shell
compiler# pwd
/usr/local/Ascend/ascend-toolkit/8.2.T2/compiler

compiler# cat version.info
Version=7.8.T5.0.B028
version_dir=8.2.T2
timestamp=20250603_154703350
required_opp_abi_version=">=6.3, <=7.8"
required_package_amct_acl_version="7.8"
required_package_aoe_version="7.8"
required_package_fwkplugin_version="7.8"
required_package_nca_version="7.8"
required_package_ncs_version="7.8"
required_package_opp_version="7.8"
required_package_opp_kernel_version=">=7.6, <=7.8"
required_package_runtime_version="7.8"
required_package_toolkit_version="7.8"
```
该问题会通过版本解决，后续版本使用应没有该问题，

问题现象，
```shell
fuyuxin]# python3 -m ms_service_profiler.parse --input-path=/data/fuyuxin/profile --output-path=/data/fuyuxin/output
2025-07-30 14:20:46,326 - 55100 - msServiceProfiler - INFO - Start to parse.
2025-07-30 14:20:46,342 - 55100 - msServiceProfiler - INFO - Read origin db /data/fuyuxin/profile is empty, please check.
```

处理方法，

需要修改脚本，修改如下，绝对路径：/usr/local/Ascend/ascend-toolkit/8.2.T2/tools/msserviceprofiler/python/ms_service_profiler/parse.py
```shell
# cd /usr/local/Ascend/ascend-toolkit/8.2.T2/tools/msserviceprofiler/python/ms_service_profiler
# cp parse.py parse.py.org

# vim parse.py
311 def check_sub_profiler_path(input_path):
312     # 判断子目录是否有PROF文件夹 如果有则走原来解析逻辑返回True 如果没有尝试走mspti返回False
313     #root_path_deepth = len(input_path.split(os.path.sep))
314     #for _, dirs, _ in os.walk(input_path, topdown=True):
315     #    for name in dirs:
316     #        subdir = os.path.join(input_path, name)
317     #        cur_path_deepth = len(subdir.split(os.path.sep))
318     #        if (cur_path_deepth - root_path_deepth == 1) and ('PROF_' in dirs):
319     #            return True
320     #        else:
321     #            continue
322     #return False
323     return True
```
