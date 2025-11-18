一、AIS-Bench 性能测试脚本说明
#合成数据集性能测试脚本
auto_synthetic.sh

1.概述
这是一个用于对 xxx 模型进行自动化性能测试的 Bash 脚本。该脚本通过修改配置文件参数，自动运行多个不同配置的性能测试，并记录测试结果。

2.主要功能
自动化配置和运行多个性能测试场景
支持不同的并发度、输入输出长度和请求速率组合
自动生成详细的测试日志


3.文件结构-举例
text
.
├── auto_synthetic.sh            # 主测试脚本
├── output_log_qwen3-8B/         # 日志文件目录（自动创建）
└── outputs/                     # 测试输出目录（自动创建）

4.前置要求
系统要求
Linux 环境

Bash shell
已配置模型推理服务且可访问xxx模型服务，推理正常
已安装 AIS-Bench 测试工具


依赖配置-举例
AIS-Bench 安装路径：/usr/local/lib/python3.11/site-packages/ais_bench/
模型服务运行在：x.x.x.x:1025  
模型路径：/data/Qwen3-8B/

5.配置参数说明
基本参数
bash
model="qwen3-8B"                    # 测试的模型名称，需要与mindie配置文件中一致
path="/data/Qwen3-8B/"              # 模型路径
host_ip="x.x.x.x"                   # 模型服务IP地址
host_port="1025"                    # 模型服务端口
log_dir="output_log_${model}"       # 日志目录
配置文件路径
bash
config_file="/usr/local/lib/python3.11/site-packages/ais_bench/benchmark/configs/models/tgi_api/tgi_stream_api_general.py"
synthetic_config="/usr/local/lib/python3.11/site-packages/ais_bench/datasets/synthetic/synthetic_config.py"

测试参数组合（用户自定义）
脚本测试以下参数组合：

并发度 (Concurrency)
1, 16, 32, 64, 128, 256

输入长度 (Input Length)
1024 tokens

2048 tokens

输出长度 (Output Length)
256, 512, 1024, 2048 tokens

请求速率 (Request Rate)
1 或 4 请求/秒


6.脚本执行流程
初始化设置
创建日志目录
备份原始配置文件
固定参数配置
设置模型路径
配置服务地址和端口
循环测试所有组合
动态更新配置参数
修改合成数据集配置
执行性能测试
保存测试结果

关键配置修改
主配置文件修改 (tgi_stream_api_general.py)
batch_size: 设置并发度

request_rate: 设置请求速率

max_out_len: 设置最大输出长度

path: 模型路径

host_ip 和 host_port: 服务地址

合成数据集配置修改 (synthetic_config.py)
RequestCount: 请求总数（并发度 × 4）

InputLen: 输入序列长度

OutputLen: 输出序列长度

RequestSize: 请求大小

Method: 设置为 "uniform" 确保固定长度


7.使用方法
a. 准备工作
确保：
AIS-Bench 已正确安装
模型服务正常运行
有足够的磁盘空间存储日志

b. 修改配置（根据实际情况修改）
根据实际情况修改脚本开头的配置参数：

bash
model="your-model-name"
path="/your/model/path/"
host_ip="your-server-ip"

c. 运行脚本
bash
chmod +x benchmark_script.sh
./benchmark_script.sh
d. 监控执行
脚本会显示当前测试进度：

text
运行测试: concurrency=1, input=1024, output=1024
运行测试: concurrency=16, input=1024, output=1024
...
输出结果
日志文件
位置：output_log_qwen3-8B/

命名格式：output_${concurrency}_${input}_${output}_${rate}.log

测试结果
位置：outputs/ 目录下的各个子目录

命名格式：${model}_${concurrency}_${input}_${output}_${rate}



二、测试数据汇总脚本说明
#数据提取汇总脚本
model_perf_multi_api_summary.py
#此脚本主要是汇总测试数据使用
# --inputs_dir ./outputs \              #ais_bench测试结果保存的路径，作为汇总脚本的输入
  --output_dir ./outputs/csv \          #汇总文件保存目录
  --merged_file 123test.csv \           #汇总csv文件名
  --model_name qwen3-8B \               #模型名称，与mindie配置文件中modelName必须一致
  --api_dirs tgi-stream-api-general \   #ais_bench测试命令使用的api 如：tgi-stream-api-general、vllm-api-stream-chat
  --data_prefix syntheticdataset        #ais_bench测试数据集名称 如：syntheticdataset、gsm8kdataset
#使用命令如下：
python3 model_perf_multi_api_summary.py \
  --inputs_dir ./outputs \
  --output_dir ./outputs/csv \
  --merged_file 123test.csv \
  --model_name qwen3-8B \
  --api_dirs tgi-stream-api-general \
  --data_prefix syntheticdataset
