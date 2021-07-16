#!/bin/bash
cd `dirname $0`
echo "0" > storage/disabled
/usr/local/bin/tmux kill-session -t TestSachiBot