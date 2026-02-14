#!/usr/bin/env bash
set -e
cd /srv/dev

if [ ! -f metrics.json ]; then
cat << 'JSON' > metrics.json
{
  "executions": 0,
  "commits": 0,
  "selfmods": 0,
  "failures": 0,
  "rollbacks": 0,
  "last_update": null
}
JSON
fi

echo "Metrics initialized."
