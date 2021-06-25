#!/bin/bash
cd `dirname $0`
echo "0" > storage/disabled
tmux kill-session -t SachiBot