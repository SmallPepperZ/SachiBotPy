#!/bin/bash
cd "$(dirname "$0")"
/usr/local/bin/tmux kill-session -t SachiBot
./run.sh