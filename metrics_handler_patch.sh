#!/usr/bin/env bash
set -e

cd /srv/dev

# inserir import
grep -q "import metrics_engine" dev_bot.py || \
sed -i '1i import metrics_engine' dev_bot.py

echo "Metrics import ensured."
