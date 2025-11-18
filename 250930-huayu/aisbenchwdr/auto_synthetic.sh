#!/bin/bash

# 配置参数
model="llama"
path="/data/DeepSeek-R1-Distill-Llama-70B/"
host_ip="127.0.0.1"
host_port="1025"
log_dir="output_log_${model}"
config_file="/usr/local/lib/python3.11/site-packages/ais_bench/benchmark/configs/models/tgi_api/tgi_stream_api_general.py"
synthetic_config="/usr/local/lib/python3.11/site-packages/ais_bench/datasets/synthetic/synthetic_config.py"

# 创建日志目录
mkdir -p "$log_dir"

# 备份原始文件
cp "$synthetic_config" "${synthetic_config}.bak"

# 初始化配置文件固定参数
sed -i "8s|.*|         path=\"${path}\",|" "$config_file"
sed -i "11s|.*|        host_ip = \"${host_ip}\",|" "$config_file"
sed -i "12s|.*|        host_port = ${host_port},|" "$config_file"

# 定义参数组合：concurrency input_leq output_leq request_rate
declare -a combinations=(
"1 1024 1024 1"
"8 1024 1024 1"
"16 1024 1024 1"
"32 1024 1024 1"
"64 1024 1024 1"
"128 1024 1024 1"
"256 1024 1024 1"
"512 1024 1024 1"
"1024 1024 1024 1"
)

# 循环处理每个组合
for combo in "${combinations[@]}"; do
    # 解析组合参数
    read concurrency input_leq output_leq request_rate <<< "$combo"
    max_lines=$(( concurrency * 2 ))

    # 更新配置文件动态参数
    sed -i "14s|.*|        batch_size = ${concurrency},|" "$config_file"
    sed -i "9s|.*|         request_rate = ${request_rate},|" "$config_file"
    sed -i "13s|.*|        max_out_len = ${output_leq},|" "$config_file"

    # 合成数据集修改
    # 修改 RequestCount
    awk -v max_lines="$max_lines" 'NR==28{$0="    \"RequestCount\":" max_lines ","} {print}' "$synthetic_config" > "${synthetic_config}.tmp" && mv "${synthetic_config}.tmp" "$synthetic_config"
    # 修改 InputLen
    awk -v input="$input_leq" 'NR==33{$0="            \"Params\": {\"MinValue\": " input ", \"MaxValue\":" input "}"} {print}' "$synthetic_config" > "${synthetic_config}.tmp" && mv "${synthetic_config}.tmp" "$synthetic_config"
    # 修改 OutputLen
    awk -v output="$output_leq" 'NR==37{$0="            \"Params\": {\"MinValue\": " output ", \"MaxValue\":" output "}"} {print}' "$synthetic_config" > "${synthetic_config}.tmp" && mv "${synthetic_config}.tmp" "$synthetic_config"
    # 修改 RequestSize
    awk -v input="$input_leq" 'NR==41{$0="        \"RequestSize\": " input " # 每条请求的长度，即每条请求中token id的个数，应与模型侧配置文件中的 input_seq_len 一致"} {print}' "$synthetic_config" > "${synthetic_config}.tmp" && mv "${synthetic_config}.tmp" "$synthetic_config"
    # 将 InputLen 和 OutputLen 的 Method 改为 uniform
    awk 'NR==32 {$0="            \"Method\": \"uniform\","} {print}' "$synthetic_config" > "${synthetic_config}.tmp" && mv "${synthetic_config}.tmp" "$synthetic_config"

    awk 'NR==36 {$0="            \"Method\": \"uniform\","} {print}' "$synthetic_config" > "${synthetic_config}.tmp" && mv "${synthetic_config}.tmp" "$synthetic_config"
    # 修改 Type
    awk 'NR==27{$0="        \"Type\": \"string\",  # [tokenid/string]，生成的随机数据集类型，支持固定长度的随机tokenid，和随机长度的string，两种类型的数据集"} {print}' "$synthetic_config" > "${synthetic_config}.tmp" && mv "${synthetic_config}.tmp" "$synthetic_config"
    
    # 执行基准测试
    echo "运行测试: concurrency=$concurrency, input=$input_leq, output=$output_leq"
    output_dir="outputs/${model}_${concurrency}_${input_leq}_${output_leq}_${request_rate}"
    log_file="${log_dir}/output_${concurrency}_${input_leq}_${output_leq}_${request_rate}.log"

    # 创建输出目录
    mkdir -p "$output_dir"

    ais_bench --models tgi_stream_api_general \
        --datasets synthetic_gen \
        --debug \
        --mode perf \
        -w "$output_dir" \
        --num-prompts "$max_lines"  2>&1 | tee "$log_file"

    echo "完成测试，日志: $log_file"

    sleep 20
done

echo "所有测试完成!

