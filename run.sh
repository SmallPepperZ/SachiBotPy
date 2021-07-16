#!/bin/bash
if ! which /usr/local/bin/tmux >/dev/null
then
	echo "tmux is not installed"
	exit 0
elif ! /usr/local/bin/tmux has-session -t SachiBotTest &> /dev/null
then
	cd `dirname $0`
	source ./venv/bin/activate
	/usr/local/bin/tmux new-session -d -s SachiBotTest python3 "./bot.py" &> logs/SachiBot.info.log
else
	exit 0
fi