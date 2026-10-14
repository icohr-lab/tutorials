#!/bin/bash
# Build survey/nhis-project.zip (the starter project students download in lesson N3).
# Run from the project root: bash survey/starter/make_zip.sh
set -e
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
TMP="$(mktemp -d)"
cp -R "$ROOT/survey/starter/nhis-project" "$TMP/"
mkdir -p "$TMP/nhis-project/data"
cp "$ROOT/data/nhis/nhis2025_adult.csv" "$TMP/nhis-project/data/"
cp "$ROOT/data/nhis/README.md" "$TMP/nhis-project/data/README.md"
rm -f "$TMP/nhis-project/data/nhis_analysis.rds"
(cd "$TMP" && zip -q -r -X nhis-project.zip nhis-project -x '*.DS_Store' '*/.Rproj.user/*' '*.Rhistory')
mv "$TMP/nhis-project.zip" "$ROOT/survey/nhis-project.zip"
rm -rf "$TMP"
echo "Wrote survey/nhis-project.zip"
