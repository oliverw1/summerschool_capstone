#!/usr/bin/env bash

SUMMER_CAPSTONE_VERSION=$(git describe --tags --always --first-parent --abbrev=7 --dirty=.dirty)
jq -n --arg summer_capstone_version "$SUMMER_CAPSTONE_VERSION" '{"summer_capstone_version":$summer_capstone_version}'
