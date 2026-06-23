#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(
    cd "$(dirname "${BASH_SOURCE[0]}")"
    pwd
)"

BACKEND_DIR="$(
    cd "${SCRIPT_DIR}/../.."
    pwd
)"

REPO_DIR="$(
    cd "${BACKEND_DIR}/../.."
    pwd
)"

COMPOSE_FILE="${REPO_DIR}/docker-compose.yml"

if [[ ! -f "${COMPOSE_FILE}" ]]; then
    echo "找不到 docker-compose.yml：${COMPOSE_FILE}"
    exit 1
fi

cd "${REPO_DIR}"

echo "将重置 FeatureMaker 本地 PostgreSQL 数据库 schema。"
echo
echo "目标："
echo "  compose: ${COMPOSE_FILE}"
echo "  service: postgres"
echo "  database: featuremaker"
echo "  user: featuremaker"
echo
echo "该操作会删除 featuremaker 数据库 public schema 下的所有表、视图和 Alembic 版本记录。"
echo "不会删除 Docker volume。"
echo

docker compose exec postgres \
    psql \
    -U featuremaker \
    -d featuremaker \
    -v ON_ERROR_STOP=1 \
    -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public; GRANT ALL ON SCHEMA public TO featuremaker;"

echo
echo "数据库 schema 已重置。"
echo
echo "下一步通常执行："
echo "  cd ${BACKEND_DIR}"
echo "  uv run alembic upgrade head"
