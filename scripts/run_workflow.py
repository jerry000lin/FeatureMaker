# 执行入口
from featuremaker.runner import run_workflow
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python run_workflow.py <workflow.yaml>")
        sys.exit(1)

    workflow_path = sys.argv[1]
    output_path = run_workflow(workflow_path)
    print(f'Workflow completed. Output saved to: {output_path}')

if __name__ == "__main__":
    main()