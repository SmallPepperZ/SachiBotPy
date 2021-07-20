#!/bin/bash
cd "$(dirname "$0")"
/usr/local/bin/tmux kill-session -t="$(basename "$(dirname "$0")")"
./run.sh