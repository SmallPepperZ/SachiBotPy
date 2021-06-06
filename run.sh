#!/bin/bash
if ! which tmux >/dev/null; then
	echo "tmux is not installed"
	exit 0
else
	cd `dirname $0`
	source ./venv/bin/activate
	tmux new-session -d -s SachiBot python3 "./bot.py"
fi