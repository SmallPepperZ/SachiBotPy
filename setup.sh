#!/bin/bash
echo 'Setting up virtual environment...'
if [[ -d venv ]]; then
  echo "A virtual environment is already setup. You can run:\n\n	python3 -m pip install -r requirements.txt\n\nto install dependencies"
else
  echo "Beginning setup"
  echo "Creating virtual environment at ./venv"
  python3 -m venv venv
  source venv/bin/activate
  echo "Installing dependencies"
  python3 -m pip install -r requirements.txt
  echo "Setup complete!"
fi
echo
echo "------------------------"
echo
echo 'Creating config files'
echo
echo -n "Would you like to follow the automatic configuration setup (y/n)? "
read -n 1 AUTO_CONFIG
if [[ $AUTO_CONFIG == "y" || $AUTO_CONFIG == "Y" ]]; then
	echo -n 'What is your bot token? '
	read -s BOT_TOKEN
	echo

	echo -n 'What is your github api token? '
	read -s GITHUB_TOKEN
	echo

	echo -n 'What prefix do you want to use? '
	read BOT_PREFIX

	echo -n 'What channel do you want to use to log errors in? '
	read ERROR_CHANNEL

	echo -n 'What github gist do you want to log tracebacks to? '
	read TRACEBACK_GIST

	echo -n 'What text would you like to remove from tracebacks before uploading (optional)? '
	read PATH_TO_HIDE

fi
if [ -e ./storage/config.json ]; then
	echo "Config.json already exists, skipping"
else
	echo """
	{
		\"discordtoken\": \"$BOT_TOKEN\",
		\"githubtoken\": \"$GITHUB_TOKEN\",
		\"prefix\": \"$BOT_PREFIX\",
		\"errorchannel\": \"$ERROR_CHANNEL\",
		\"githubgist\": \"$TRACEBACK_GIST\",
		\"pathtohide\": \"$PATH_TO_HIDE\",
		\"embedcolor\": \"0x2F3136\",
		\"errornum\": \"0\",
		\"enabledguilds\": [],
		\"status\": [
			[
				\"watching\",
				3
			],
			\"people try and set me up\",
			[
				\"online\",
				\"online\"
			]
		]
	}
	""" > ./storage/config.json
fi