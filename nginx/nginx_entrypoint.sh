#!/usr/bin/env sh
set -eu

envsubst '${NGINX_HOST} ${SERVER_NAME} ${SERVER_PORT}' < /etc/nginx/conf.d/site.conf.template > /etc/nginx/conf.d/site.conf
envsubst '${WORKERS_COUNT}' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

exec "$@"