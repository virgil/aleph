#!/bin/bash


	cd /root/helloflask/
	source venv/bin/activate
	python app.py
	echo "Sleeping for 10sec..."
	sleep 10
	source run_app.sh