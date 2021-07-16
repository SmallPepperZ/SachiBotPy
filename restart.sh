#!/bin/bash
cd "$(dirname "$0")"
/usr/local/bin/tmux kill-session -t SachiBotTest
./run.sh