#!bin/bash
PORT=9090


# function for activating the python env
function activate_env(){
    if [[ -z $VIRTUAL_ENV ]]
    then
        echo "ACTIVATING ENV"
        source ../env/bin/activate
    fi
}
# function for running the server
function run_server(){
    is_port_busy=$(sudo lsof -t -i :$PORT)

    if [[ -n is_port_busy ]]
    then
        echo "KILLING THE BUSY PORT"
        sudo fuser -k $PORT/tcp
        
    fi

    # running the server
    echo "STARTING THE SERVR"
    python manage.py runserver "$PORT"
    # python manage.py runserver "$PORT" & pkill -f 'celery worker' & celery -A core worker -l info
        

}

# function for making db migrations
function make_migrations(){
    python manage.py makemigrations
    python manage.py migrate

}

activate_env

make_migrations

run_server