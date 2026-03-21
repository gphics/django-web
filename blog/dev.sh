#!/bin/bash

# INSTRUCTIONAL messages
echo "CUSTOM DJANGO RUNNER "
echo "This script is responsible for running the django server "
echo "@params ::"
echo " \$1 ---> keyword == db. make migrations and migrate alone"
echo " \$1 ---> keyword == all. perform db ops and runserver"
echo " No param ---> Run server"

function db_processor(){
	#  "PERFORMING DB OPs"
	python manage.py makemigrations
	python manage.py migrate
}

function run_server(){
	PORT=8000

	# checking if port is busy
	port_status=$(sudo lsof -i :$PORT)

	# killing port if it's busy
	if [[ -n $port_status ]]
	then
		echo "KILLING THE BUSY PORT"
		sudo fuser -k "$PORT"/tcp
	fi

	# running the server
	echo "RUNNING THE SERVER AT PORT $PORT"
	python manage.py runserver $PORT

}

function activate_env(){
	
	if [[ -z $VIRTUAL_ENV ]]
	then
		echo "ACTIVATING VIRTUAL ENVIRONMENT"
		source ../env/bin/activate
		
	else
		echo "VIRTUAL ENVIRONMENT ALREADY ACTIVATED"
	fi

}

# activating the env
activate_env

if [[ $1 = "db" ]]
then
	db_processor
elif [[ $1 = "all" ]]
then
	db_processor
	run_server
elif [[ -n $1 ]]
then
	echo "param $1 not identified"
else
	run_server
fi

