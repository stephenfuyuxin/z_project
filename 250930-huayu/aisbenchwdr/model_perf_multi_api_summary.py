import os
import csv
import json
import shutil
import pandas as pd
import argparse
from datetime import datetime

def extract_csv_data(csv_path):
    """提取CSV文件中的性能指标数据"""
    csv_data = {
        "InputTokens": None,
        "OutputTokens": None,
        "E2EL": None,
        "TTFT": None,
        "TPOT": None,
        "OutputTokenThroughput_CSV": None
    }
    try:
        with open(csv_path, "r", encoding="utf-8-sig") as f:
            reader = csv.reader(f, delimiter=",", skipinitialspace=True)
            header_found = False
            param_col_idx = -1
            avg_col_idx = -1
            for row_num, row in enumerate(reader, 1):
                if not row:
                    continue
                if not header_found:
                    lower_row = [col.strip().lower() for col in row]
                    if "performance parameters" in lower_row and "average" in lower_row:
                        param_col_idx = lower_row.index("performance parameters")
                        avg_col_idx = lower_row.index("average")
                        header_found = True
                    continue
                if len(row) <= max(param_col_idx, avg_col_idx):
                    continue
                param_name = row[param_col_idx].strip().lower()
                avg_value = row[avg_col_idx].strip()
                if param_name == "inputtokens":
                    csv_data["InputTokens"] = avg_value
                elif param_name == "outputtokens":
                    csv_data["OutputTokens"] = avg_value
                elif param_name == "e2el":
                    csv_data["E2EL"] = avg_value
                elif param_name == "ttft":
                    csv_data["TTFT"] = avg_value
                elif param_name == "tpot":
                    csv_data["TPOT"] = avg_value
                elif param_name == "outputtokenthroughput":
                    csv_data["OutputTokenThroughput_CSV"] = avg_value
    except Exception as e:
        print(f"CSV读取失败[{csv_path}]：{str(e)}")
    return csv_data

def extract_json_data(json_path):
    """提取JSON文件中的性能指标数据"""
    json_data = {
        "Concurrency": None,
        "Max_Concurrency": None,
        "Request_Throughput": None,
        "Total_Token_Throughput": None,
        "OutputTokenThroughput_JSON": None
    }
    try:
        with open(json_path, "r", encoding="utf-8-sig") as f:
            raw_json = json.load(f)
        json_data["Concurrency"] = raw_json.get("Concurrency", {}).get("total")
        json_data["Max_Concurrency"] = raw_json.get("Max Concurrency", {}).get("total")
        json_data["Request_Throughput"] = raw_json.get("Request Throughput", {}).get("total")
        json_data["Total_Token_Throughput"] = raw_json.get("Total Token Throughput", {}).get("total")
        json_data["OutputTokenThroughput_JSON"] = raw_json.get("Output Token Throughput", {}).get("total")
    except Exception as e:
        print(f"JSON读取失败[{json_path}]：{str(e)}")
    return json_data

def is_number(s):
    """判断字符串是否为数字"""
    try:
        float(s)
        return True
    except ValueError:
        return False

def extract_request_rate(ds_dir_name, model_prefix):
    """从目录名中提取请求速率"""
    if not ds_dir_name.startswith(model_prefix + "_"):
        print(f"目录名不匹配：{ds_dir_name}（需以{model_prefix}_开头）")
        return "Unknown"

    dir_parts = ds_dir_name.split("_")
    print(f"目录名分割：{ds_dir_name} -> 分割后：{dir_parts}（共{len(dir_parts)}个部分）")

    if len(dir_parts) != 5:
        print(f"目录名格式异常：{ds_dir_name}（需为{model_prefix}_X_X_X_RequestRate，当前{len(dir_parts)}个部分）")
        return "Unknown"

    request_rate = dir_parts[-1]
    if not is_number(request_rate):
        print(f"request_rate非数字：{request_rate}（目录名：{ds_dir_name}）")
    else:
        print(f"提取request_rate：{request_rate}（来源目录：{ds_dir_name}）")
    return request_rate

def is_valid_timestamp_dir(dir_name):
    """验证目录名是否为合法时间戳（YYYYMMDD_HHMMSS）"""
    if len(dir_name) != 15 or "_" not in dir_name:
        return False
    date_part, time_part = dir_name.split("_")
    try:
        datetime.strptime(date_part, "%Y%m%d")
        datetime.strptime(time_part, "%H%M%S")
        return True
    except ValueError:
        return False

def generate_sub_table(csv_data, json_data, request_rate, output_dir):
    """生成单个场景的子表格"""
    input_token = csv_data["InputTokens"].replace(".0", "") if csv_data["InputTokens"] else "Unknown"
    output_token = csv_data["OutputTokens"].replace(".0", "") if csv_data["OutputTokens"] else "Unknown"
    concurrency = str(json_data["Max_Concurrency"]).replace(".0", "") if json_data["Max_Concurrency"] else "Unknown"

    safe_request_rate = request_rate.replace(".", "_") if request_rate != "Unknown" else "Unknown"

    table_name = (
        f"Table_Input{input_token}_"
        f"Output{output_token}_"
        f"ReqRate{safe_request_rate}_"
        f"Concurrency{concurrency}.csv"
    )

    # 替换文件名中的非法字符
    illegal_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in illegal_chars:
        table_name = table_name.replace(char, "_")

    output_path = os.path.join(output_dir, table_name)

    # 子表格内容
    table_content = [
        ["具体指标", "数值"],
        ["并发数（Concurrency）", json_data["Concurrency"] if json_data["Concurrency"] else "-"],
        ["最大并发数（Max Concurrency）", json_data["Max_Concurrency"] if json_data["Max_Concurrency"] else "-"],
        ["输入Token数", csv_data["InputTokens"] if csv_data["InputTokens"] else "-"],
        ["输出Token数", csv_data["OutputTokens"] if csv_data["OutputTokens"] else "-"],
        ["端到端延迟（E2EL）", csv_data["E2EL"] if csv_data["E2EL"] else "-"],
        ["首词响应时间（TTFT）", csv_data["TTFT"] if csv_data["TTFT"] else "-"],
        ["后续词响应时间（TPOT）", csv_data["TPOT"] if csv_data["TPOT"] else "-"],
        ["请求吞吐量（Request Throughput）", json_data["Request_Throughput"] if json_data["Request_Throughput"] else "-"],
        ["输出Token吞吐量（CSV）", csv_data["OutputTokenThroughput_CSV"] if csv_data["OutputTokenThroughput_CSV"] else "-"],
        ["输出Token吞吐量（JSON）", json_data["OutputTokenThroughput_JSON"] if json_data["OutputTokenThroughput_JSON"] else "-"],
        ["总Token吞吐量（Total Token Throughput）", json_data["Total_Token_Throughput"] if json_data["Total_Token_Throughput"] else "-"],
        ["request_rate", request_rate]
    ]

    try:
        with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerows(table_content)
        print(f"生成子表格：{table_name}")
        return output_path, table_name
    except Exception as e:
        print(f"子表格生成失败：{str(e)}")
        return None, None

def move_sub_table(source_path, source_table_name, output_dir, ds_dir_name, timestamp_dir_name):
    """移动子表格到输出目录"""
    os.makedirs(output_dir, exist_ok=True)

    safe_ds_dir_name = ds_dir_name.replace(".", "_")
    target_filename = f"{safe_ds_dir_name}_{timestamp_dir_name}_{source_table_name}"

    if not target_filename.endswith(".csv"):
        target_filename += ".csv"

    target_path = os.path.join(output_dir, target_filename)

    try:
        shutil.move(source_path, target_path)
        print(f"移动子表格：{source_table_name} -> {target_filename}")
        return output_dir
    except Exception as e:
        print(f"子表格移动失败：{str(e)}")
        return output_dir

def merge_sub_tables(output_dir, merged_filename):
    """合并所有子表格为汇总表格"""
    print(f"开始合并子表格（目录：{output_dir}）")

    sub_tables = [
        f for f in os.listdir(output_dir)
        if "Table_Input" in f and "ReqRate" in f and f.endswith(".csv") and f != merged_filename
    ]

    if not sub_tables:
        print(f"未找到目标子表格")
        return

    print(f"找到{len(sub_tables)}个目标子表格")

    long_df = pd.DataFrame()
    for table in sub_tables:
        table_path = os.path.join(output_dir, table)
        try:
            df = pd.read_csv(table_path, encoding="utf-8-sig")
            scene_name = table.replace(".csv", "").replace("_ReqRate", "ReqRate").replace("ReqRate", "_ReqRate")
            df["测试场景"] = scene_name
            long_df = pd.concat([long_df, df], ignore_index=True)
            print(f"合并成功：{table}")
        except Exception as e:
            print(f"合并失败[{table}]：{str(e)}")
            continue

    if long_df.empty:
        print(f"合并后无有效数据")
        return

    # 转换为宽表
    wide_df = pd.pivot_table(
        data=long_df,
        index="测试场景",
        columns="具体指标",
        values="数值",
        fill_value="-",
        aggfunc="first"
    ).reset_index()

    # 定义列顺序
    desired_col_order = [
        "测试场景",
        "并发数（Concurrency）",
        "最大并发数（Max Concurrency）",
        "输入Token数",
        "输出Token数",
        "端到端延迟（E2EL）",
        "首词响应时间（TTFT）",
        "后续词响应时间（TPOT）",
        "请求吞吐量（Request Throughput）",
        "输出Token吞吐量（CSV）",
        "输出Token吞吐量（JSON）",
        "总Token吞吐量（Total Token Throughput）",
        "request_rate"
    ]

    # 过滤实际存在的列
    actual_cols = [col for col in desired_col_order if col in wide_df.columns]
    wide_df = wide_df[actual_cols]

    merged_output_path = os.path.join(output_dir, merged_filename)
    wide_df.to_csv(merged_output_path, index=False, encoding="utf-8-sig")

    print(f"合并完成！")
    print(f"合并结果：{merged_output_path}（{len(wide_df)}场景 × {len(wide_df.columns)}指标）")

def main():
    parser = argparse.ArgumentParser(description='处理性能测试数据并生成汇总表格')
    # 基础参数
    parser.add_argument('--inputs_dir', default='.', help='输入数据根目录路径，默认为当前目录')
    parser.add_argument('--output_dir', default='./outputs', help='输出目录路径，默认为./outputs')
    parser.add_argument('--merged_file', default='results.csv', help='汇总文件名，默认为results.csv')
    parser.add_argument('--model_name', default='Qwen3-32B', help='模型名前缀，默认为Qwen3-32B')
    
    # 新增：支持多个API目录（逗号分隔）
    parser.add_argument('--api_dirs', default='vllm-api-stream-chat', 
                        help='API测试目录名（多个用逗号分隔，如"vllm-api-stream-chat,tgi-stream-api-general"）')
    # 新增：数据文件前缀（如"syntheticdataset"）
    parser.add_argument('--data_prefix', default='gsm8kdataset', 
                        help='CSV/JSON数据文件的前缀（如"syntheticdataset"）')

    args = parser.parse_args()

    inputs_dir = args.inputs_dir
    output_dir = args.output_dir
    merged_filename = args.merged_file
    model_prefix = args.model_name
    # 解析API目录列表（去重+过滤空字符串）
    api_dirs = list(set([d.strip() for d in args.api_dirs.split(',') if d.strip()]))
    data_prefix = args.data_prefix  # 数据文件前缀

    # 检查输入目录是否存在
    if not os.path.exists(inputs_dir):
        print(f"错误：输入目录不存在 - {inputs_dir}")
        return

    # 获取输入目录的绝对路径
    inputs_dir = os.path.abspath(inputs_dir)
    
    print(f"开始执行脚本，输入目录：{inputs_dir}")
    print(f"输出目录：{output_dir}")
    print(f"汇总文件：{merged_filename}")
    print(f"模型前缀：{model_prefix}")
    print(f"待匹配的API目录：{api_dirs}")
    print(f"数据文件前缀：{data_prefix}")

    processed_count = 0

    # 遍历所有目录查找目标数据
    for dirpath, _, filenames in os.walk(inputs_dir):
        current_dir_name = os.path.basename(dirpath)
        # 匹配指定的API目录（支持多个）
        if current_dir_name not in api_dirs:
            continue

        print(f"找到目标API目录：{dirpath}")

        # 解析目录层级
        perf_dir = os.path.dirname(dirpath)
        timestamp_dir = os.path.dirname(perf_dir)
        ds_dir = os.path.dirname(timestamp_dir)
        ds_dir_name = os.path.basename(ds_dir)
        timestamp_dir_name = os.path.basename(timestamp_dir)

        print(f"目录追溯链：{ds_dir_name} -> {timestamp_dir_name} -> {os.path.basename(perf_dir)} -> {current_dir_name}")

        # 验证上级目录是否为"performances"
        if os.path.basename(perf_dir) != "performances":
            print(f"上级目录异常：{os.path.basename(perf_dir)}（需为performances），跳过")
            continue
        # 验证时间戳目录格式
        if not is_valid_timestamp_dir(timestamp_dir_name):
            print(f"时间戳目录异常：{timestamp_dir_name}（需为YYYYMMDD_HHMMSS），跳过")
            continue
        # 验证模型目录前缀
        if not ds_dir_name.startswith(model_prefix + "_"):
            print(f"模型目录异常：{ds_dir_name}（需以{model_prefix}_开头），跳过")
            continue

        # 构建数据文件路径（使用用户指定的前缀）
        csv_path = os.path.join(dirpath, f"{data_prefix}.csv")
        json_path = os.path.join(dirpath, f"{data_prefix}.json")
        csv_exists = os.path.exists(csv_path)
        json_exists = os.path.exists(json_path)
        print(f"文件检查：CSV={csv_exists}（{csv_path}），JSON={json_exists}（{json_path}）")
        if not csv_exists or not json_exists:
            print(f"缺失文件，跳过")
            continue

        # 提取请求速率
        print(f"开始提取request_rate...")
        request_rate = extract_request_rate(ds_dir_name, model_prefix)

        # 提取CSV和JSON数据
        csv_data = extract_csv_data(csv_path)
        json_data = extract_json_data(json_path)

        # 检查关键数据是否缺失
        missing_keys = []
        if not csv_data["InputTokens"]:
            missing_keys.append("InputTokens")
        if not csv_data["OutputTokens"]:
            missing_keys.append("OutputTokens")
        if not json_data["Max_Concurrency"]:
            missing_keys.append("Max_Concurrency")
        if missing_keys:
            print(f"关键数据缺失：{', '.join(missing_keys)}，跳过")
            continue

        # 生成子表格
        print(f"生成子表格...")
        sub_table_path, sub_table_name = generate_sub_table(csv_data, json_data, request_rate, dirpath)
        if not sub_table_path:
            print(f"子表格生成失败，跳过")
            continue

        # 移动子表格到输出目录
        move_sub_table(sub_table_path, sub_table_name, output_dir, ds_dir_name, timestamp_dir_name)

        processed_count += 1
        print(f"场景处理完成（累计：{processed_count}个）")

    print(f"脚本执行结束：共处理{processed_count}个有效场景")
    if os.path.exists(output_dir) and processed_count > 0:
        merge_sub_tables(output_dir, merged_filename)
    else:
        print("未生成任何子表格")

if __name__ == "__main__":
    main()

