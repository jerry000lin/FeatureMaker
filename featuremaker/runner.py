# 核心执行函数
import yaml
import pandas as pd
from featuremaker.mock_provider import generate_customer_label
import os

def run_workflow(workflow_path:str) -> str:
    # 读取 workflow.yaml
    with open(workflow_path, 'r') as stream:
        config = yaml.safe_load(stream)
    
    # 从 dataset.path 读取 CSV
    dataset_path = config['dataset']['path']
    
    # 逐行调用 generate_customer_label
    df = pd.read_csv(dataset_path)
    # 追加 llm_label / llm_reason
    df[['llm_label', 'llm_reason']] = df.apply(generate_customer_label, axis=1, result_type='expand')

    # 写到 output.path
    output_path = config['output']['path']
    os.path.dirname(output_path)  # 确保目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    df.to_csv(output_path, index=False)

    # 返回 output path
    return output_path