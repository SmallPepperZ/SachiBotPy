#!/bin/bash
if ! which /usr/local/bin/tmux >/dev/null
then
	echo "tmux is not installed"
	exit 0
elif ! /usr/local/bin/tmux has-session -t SachiBot &> /dev/null
then
	echo "1" > storage/disabled
	cd `dirname $0`
	source ./venv/bin/activate
	/usr/local/bin/tmux new-session -d -s SachiBot python3 "./bot.py" &> logs/SachiBot.info.log
else
	echo "3.3" >> /Users/zachy/.tmp/test
	exit 0
fi