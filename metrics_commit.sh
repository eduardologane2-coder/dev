#!/usr/bin/env bash
set -e
cd /srv/dev

git add metrics_engine.py metrics_report_handler.py metrics.json || true
git commit -m "feat(metrics): sistema completo de métricas operacionais" || true
git log --oneline -3
