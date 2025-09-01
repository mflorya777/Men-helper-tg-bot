#!/usr/bin/env bash


export $(grep -v '^#' "$1" | xargs -d '\n')
