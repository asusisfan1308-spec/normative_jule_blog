#!/bin/sh
set -e

# 1) PostgreSQL tayyor bo'lguncha kutish
if [ -n "$DB_HOST" ]; then
  echo "[entrypoint] PostgreSQL kutilmoqda: ${DB_HOST}:${DB_PORT:-5432}"
  python - <<'PY'
import os, socket, sys, time

host = os.environ["DB_HOST"]
port = int(os.environ.get("DB_PORT", "5432"))

for _ in range(60):
    try:
        socket.create_connection((host, port), timeout=2).close()
        print("[entrypoint] PostgreSQL tayyor")
        sys.exit(0)
    except OSError:
        time.sleep(1)

print("[entrypoint] XATO: PostgreSQL ga ulanib bo'lmadi")
sys.exit(1)
PY
fi

# 2) Migratsiyalar
if [ "${RUN_MIGRATIONS:-1}" = "1" ]; then
  echo "[entrypoint] migrate"
  python manage.py migrate --noinput
fi

# 3) Static fayllarni nginx o'qiydigan volume ga yig'ish
if [ "${RUN_COLLECTSTATIC:-1}" = "1" ]; then
  echo "[entrypoint] collectstatic"
  python manage.py collectstatic --noinput
fi

# 4) Asosiy buyruqni (gunicorn) ishga tushirish
echo "[entrypoint] ishga tushirilmoqda: $*"
exec "$@"
