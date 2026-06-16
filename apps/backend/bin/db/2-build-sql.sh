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
OUT_DIR="${ROOT_DIR}/dist/sql"

if [[ ! -f "${ALEMBIC_INI}" ]]; then
    echo "找不到配置文件：${ALEMBIC_INI}"
    exit 1
fi

if [[ ! -d "${VERSIONS_DIR}" ]]; then
    echo "找不到迁移目录：${VERSIONS_DIR}"
    exit 1
fi

cd "${ROOT_DIR}"

mkdir -p "${OUT_DIR}"

echo "项目目录：${ROOT_DIR}"
echo "检查 migration Python 文件语法..."

uv run python -m compileall \
    -q \
    "${VERSIONS_DIR}"

echo "读取最新 migration 版本信息..."

REVISION_INFO="$(
    uv run python - "${ALEMBIC_INI}" <<'PY'
import sys

from alembic.config import Config
from alembic.script import ScriptDirectory


alembic_ini = sys.argv[1]

config = Config(alembic_ini)
scripts = ScriptDirectory.from_config(config)

heads = scripts.get_heads()

if len(heads) != 1:
    raise SystemExit(
        f"要求只有一个 Alembic head，当前发现：{heads}"
    )

to_revision = heads[0]
migration = scripts.get_revision(to_revision)
from_revision = migration.down_revision

if isinstance(from_revision, tuple):
    raise SystemExit(
        "最新 migration 是合并迁移，无法自动确定单一起始版本"
    )

print(from_revision or "base")
print(to_revision)
PY
)"

FROM_REV="$(
    printf '%s\n' "${REVISION_INFO}" |
    sed -n '1p'
)"

TO_REV="$(
    printf '%s\n' "${REVISION_INFO}" |
    sed -n '2p'
)"

DATE_PREFIX="$(date +%Y%m%d)"

LAST_INDEX="$(
    find "${OUT_DIR}" \
        -maxdepth 1 \
        -type f \
        -name "${DATE_PREFIX}_[0-9][0-9][0-9]_*.sql" \
        -printf "%f\n" |
    sed -E "s/^${DATE_PREFIX}_([0-9]{3})_.*/\1/" |
    sort -n |
    tail -n 1
)"

if [[ -z "${LAST_INDEX}" ]]; then
    NEXT_INDEX=1
else
    NEXT_INDEX=$((10#${LAST_INDEX} + 1))
fi

INDEX_PREFIX="$(
    printf "%03d" "${NEXT_INDEX}"
)"

FILE_PREFIX="${DATE_PREFIX}_${INDEX_PREFIX}"

OUT_FILE="${OUT_DIR}/${FILE_PREFIX}_upgrade_${FROM_REV}_to_${TO_REV}.sql"
TMP_FILE="${OUT_FILE}.tmp"

trap 'rm -f "${TMP_FILE}"' EXIT

echo "生成 SQL：${FROM_REV} -> ${TO_REV}"

uv run alembic \
    -c "${ALEMBIC_INI}" \
    upgrade \
    "${FROM_REV}:${TO_REV}" \
    --sql \
    > "${TMP_FILE}"

if [[ ! -s "${TMP_FILE}" ]]; then
    echo "生成的 SQL 文件为空"
    exit 1
fi

{
    echo "-- Alembic 离线迁移 SQL"
    echo "-- 执行前数据库版本：${FROM_REV}"
    echo "-- 执行后数据库版本：${TO_REV}"
    echo
    cat "${TMP_FILE}"
} > "${OUT_FILE}"

rm -f "${TMP_FILE}"
trap - EXIT

echo
echo "SQL 生成成功："
echo "  ${OUT_FILE}"
echo
echo "执行前，请确认数据库当前版本为：${FROM_REV}"
echo "检查 SQL 后，再手动执行。"