#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(
    cd "$(dirname "${BASH_SOURCE[0]}")"
    pwd
)"

ROOT_DIR="$(
    cd "${SCRIPT_DIR}/../.."
    pwd
)"

ALEMBIC_INI="${ROOT_DIR}/alembic.ini"

if [[ ! -f "${ALEMBIC_INI}" ]]; then
    echo "找不到 Alembic 配置文件：${ALEMBIC_INI}"
    exit 1
fi

cd "${ROOT_DIR}"

echo "检查数据库迁移版本..."

uv run alembic \
    -c "${ALEMBIC_INI}" \
    current \
    --check-heads

echo
echo "数据库迁移版本检查通过。"

echo
echo "检查数据库结构是否与 ORM Model 一致..."

uv run alembic \
    -c "${ALEMBIC_INI}" \
    check

echo
echo "数据库更新检查全部通过："
echo "  1. 数据库已处于最新 Alembic 版本"
echo "  2. 数据库结构与 ORM Model 一致"