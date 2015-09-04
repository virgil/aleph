#!/bin/bash


	cd /root/aleph
	source venv/bin/activate
	heroku local -p 1337
	echo "Sleeping for 10sec..."
	sleep 10
	source run_app.sh
