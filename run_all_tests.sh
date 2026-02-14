#!/usr/bin/env bash
set -e

echo "=== RUNNING DEV TEST SUITE ==="

python3 -m pytest -q tests || exit 1

echo "=== ALL TESTS PASSED ==="
