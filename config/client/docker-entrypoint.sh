#!/bin/sh
set -e

# replace ${API_SERVER} in template with runtime env value (or empty)
: "${API_SERVER:=}"
envsubst '${API_SERVER}' < /usr/share/nginx/html/config.template.js > /usr/share/nginx/html/config.js

exec "$@"