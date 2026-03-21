#!bin/bash

# This shell file is responsible for creating the base(dummy) data for the project

echo "CREATING DUMMY DATA"
(   


    # activating the environment
    source ../../env/bin/activate
    # creating the dummy data
    python utils/dummy_data/action.py
)