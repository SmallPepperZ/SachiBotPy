#!/bin/bash

cd "$(dirname "$0")"

dirname="$(basename "$PWD")"

if ! which /usr/local/bin/tmux >/dev/null
then
	echo "tmux is not installed"
	exit 1
elif ! /usr/local/bin/tmux has-session -t=$dirname &> /dev/null
then
	cd "$(dirname "$0")"
	source ./venv/bin/activate
	/usr/local/bin/tmux new-session -d -s $dirname ./venv/bin/python ./bot.py &> logs/SachiBot.info.log
	/usr/local/bin/tmux pipe-pane -t $dirname "tee -a $PWD/logs/SachiBot.{debug,info}.log"
else
	echo "3.3" >> $HOME/.tmp/test
	exit 2
fi