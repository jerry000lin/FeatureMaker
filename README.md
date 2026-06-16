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

## 数据库变更

每次修改 `models/` 里的代码后，更新数据库操作：

1. 修改 ORM Model 后，执行 `bash bin/db/1-make-migration.sh "<message>"` 调用 alembic 生成 `apps/backend/alembic/versions/<id>_<message>.py`
2. 检查生成的 `apps/backend/alembic/versions/<id>_<message>.py`
3. 执行 `bash bin/db/2-build-sql.sh` 生成 `apps/backend/dist/sql/<date>_<idx>_upgrade_base_to_<id>.sql`
4. 打开 SQL，再检查一次
5. 手动在数据库执行
6. 执行 `bash bin/db/3-check.sh`