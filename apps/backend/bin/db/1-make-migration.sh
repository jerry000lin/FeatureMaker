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
VERSIONS_DIR="${ROOT_DIR}/alembic/versions"

if [[ $# -eq 0 ]]; then
    echo "用法："
    echo "  bash bin/db/1-make-migration.sh \"迁移说明\""
    exit 1
fi

if [[ ! -f "${ALEMBIC_INI}" ]]; then
    echo "找不到配置文件：${ALEMBIC_INI}"
    exit 1
fi

if [[ ! -d "${VERSIONS_DIR}" ]]; then
    echo "找不到迁移目录：${VERSIONS_DIR}"
    exit 1
fi

cd "${ROOT_DIR}"

MESSAGE="$*"

echo "项目目录：${ROOT_DIR}"
echo "开始生成 migration..."

uv run alembic \
    -c "${ALEMBIC_INI}" \
    revision \
    --autogenerate \
    -m "${MESSAGE}"

LATEST_FILE="$(
    find "${VERSIONS_DIR}" \
        -maxdepth 1 \
        -type f \
        -name "*.py" \
        ! -name "__init__.py" \
        -printf "%T@ %p\n" |
    sort -nr |
    head -n 1 |
    cut -d " " -f 2-
)"

if [[ -z "${LATEST_FILE}" ]]; then
    echo "没有找到生成的 migration 文件"
    exit 1
fi

echo
echo "检查 migration Python 语法..."

uv run python -m py_compile "${LATEST_FILE}"

echo
echo "生成成功："
echo "  ${LATEST_FILE}"
echo
echo "请人工检查 upgrade() 和 downgrade()。"