#!/usr/bin/env sh


until nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  >&2 echo "Waiting for postgres..."
  sleep 1
done

until nc -z "$REDIS_HOST" "$REDIS_PORT"; do
  >&2 echo "Waiting for redis..."
  sleep 1
done

alembic upgrade head

exec "$@"
