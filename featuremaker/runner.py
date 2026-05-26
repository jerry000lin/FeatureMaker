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
    # df[['llm_label', 'llm_reason']] = df.apply(generate_customer_label, axis=1, result_type='expand')
    results = []
    for index, row in df.iterrows():
        try:
            label_info = generate_customer_label(row)
            results.append({
                'llm_label': label_info['llm_label'],
                'llm_reason': label_info['llm_reason'],
                '_featuremaker_status': 'success',
                '_featuremaker_error_message': ''
            })
        except Exception as e:
            results.append({
                'llm_label': '',
                'llm_reason': '',
                '_featuremaker_status': 'failed',
                '_featuremaker_error_message': str(e)
            })
    pd_results = pd.DataFrame(results)
    df_concat = pd.concat([df, pd_results], axis=1)
    # 写到 output.path
    output_path = config['output']['path']
    os.path.dirname(output_path)  # 确保目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    df_concat.to_csv(output_path, index=False)

    # 返回 output path
    return output_path