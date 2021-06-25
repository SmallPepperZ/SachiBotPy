#!/bin/bash
if ! which tmux >/dev/null
then
	echo "tmux is not installed"
	exit 0
elif ! tmux has-session -t SachiBot &> /dev/null
then
	echo "1" > storage/disabled
	cd `dirname $0`
	source ./venv/bin/activate
	tmux new-session -d -s SachiBot python3 "./bot.py"
else
	exit 0
fi