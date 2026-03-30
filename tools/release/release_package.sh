#!/bin/sh

# SPDX-FileCopyrightText: 2026 Infineon Technologies AG
#
# SPDX-License-Identifier: MIT

set -e

echo "Preparing release"
cd ../..
rm -rf *.gz
COMMIT_SHA=$(git rev-parse --short HEAD)
echo "$COMMIT_SHA"
tar --exclude='.*' -czf optiga-trust-m-explorer_$COMMIT_SHA.tar.gz *

echo " release package done $PWD/optiga-trust-m-explorer_$COMMIT_SHA.tar.gz "

