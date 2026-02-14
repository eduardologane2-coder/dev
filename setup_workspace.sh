#!/usr/bin/env bash
set -e

mkdir -p /srv/dev/workspace
cd /srv/dev/workspace

if [ ! -d ".git" ]; then
  git init
  git config user.name "Dev Bot"
  git config user.email "dev@local"
fi

echo "Workspace pronto em /srv/dev/workspace"
