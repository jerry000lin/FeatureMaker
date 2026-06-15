# FeatureMaker

FeatureMaker 是一个面向表数据的数据加工与 LLM Agents 编排平台。

## 开发环境运行

```bash
cd apps/backend

# 安装并同步依赖
uv sync

# 运行测试
uv run python -m pytest

# 启动开发服务
uv run fastapi dev

# 查看数据库迁移状态
uv run alembic current
```