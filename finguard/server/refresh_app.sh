#!/bin/bash

# This shell file is for cleaning up the whole apps
    # > delete the __pycache__
    # > delete migrations dir
    # mkdir migrations and touch 

echo "DELETING THE DB"
rm db.sqlite3

echo "DELETING THE __PYCACHE__ DIR"
find -iname "__pycache__" | xargs rm -rf

echo "DELETING THE MIGRATIONS DIR"
find -iname "migrations" | xargs rm -rf

echo "DELETING TOKENS.TXT"
find -iname "tokens.txt" | xargs rm -rf

echo "DELETING THE MODEL STORE"
find -iname "model_store" | xargs rm -rf

django_apps=("account" "transaction" "ml" "media_app")

# looping through the djangoapps
for app in "${django_apps[@]}"
do
    # creating the migration files
    (
    cd "$app"
    # FOR ML APP
    if [[ "$app" == "ml" ]]
    then
        echo "CREATING THE MODEL STORE"
        mkdir model_store
    fi

    mkdir -p migrations && touch migrations/__init__.py
    echo "CREATED THE MIGRATIONS DIR FOR $app app"
    )
done

echo "CREATING THE TOKENS.TXT FILE"
(

    touch utils/dummy_data/tokens.txt
)


