#!bin/bash

echo "SETTING UP ... "
echo "PARAMETER OPTIONS"
echo "\$1 ---> : run server only"
echo "\$1 ---> all : db migrations and run server"
echo "\$1 ---> db : db migrations only"
echo "\$1 ---> gen : generate the requirements.txt file"



function run_server(){
    PORT=8000

    echo "checking if port is in use"

    is_busy=$(sudo lsof -t -i :$PORT)


    if [[ -z "$is_busy" ]]
    then
        echo "PORT: $PORT is free"
        echo "STARTING THE SERVER AT PORT:$PORT"
        python manage.py runserver $PORT
    else
        echo "PORT: $PORT is busy"
        echo "KILLING PORT:$PORT"
        sudo fuser -k "$PORT"/tcp
        echo "STARTING THE SERVER AT PORT:$PORT"
        python manage.py runserver $PORT
    fi
}

function db_actions(){
    python manage.py makemigrations
    python manage.py migrate
}

function activate_env(){
    if [[ -z $VIRTUAL_ENV ]]
    then
        echo "ACTIVATING THE ENVIRONMENT"
        source ../../env/bin/activate
    else
        echo "ENVIRONMENT IS ALREADY ACTIVE"
    fi
}

function generate_requirements(){
    pip freeze > requirements.txt
}

# env activation
activate_env

if [[ $1 == "all" ]]
then
    db_actions
    run_server
elif [[ $1 == "db" ]]
then
    db_actions
elif [[ $1 == "gen" ]]
then
    generate_requirements
elif [[ -n $1 ]]
then
    echo "$1 not recognized"
else
    run_server
fi