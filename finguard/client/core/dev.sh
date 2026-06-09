#!/bin/bash

PORT=5000

is_port_busy=$(sudo lsof -t -i :$PORT 2>/dev/null)

# IF PORT IS BUSY
if [[ -n "$is_port_busy" ]]
then
    echo "KILLING THE SERVER"
    sudo fuser -k $PORT/tcp
fi

echo "RUNNING THE SERVER"    
npm run dev -- --turbo -p $PORT 