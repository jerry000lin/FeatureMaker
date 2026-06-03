# FeatureMaker

FeatureMaker 是一个面向表数据的数据加工与 LLM Agents 编排平台。

## 开发环境运行

```sh
cd apps/backend

# 安装后端运行依赖和开发依赖
poetry install --with dev

# 运行后端测试
poetry run python -m pytest

# 启动 FastAPI 开发服务
poetry run uvicorn featuremaker.main:app --reload
```
