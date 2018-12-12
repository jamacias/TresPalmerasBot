#!/bin/bash
while true; do
    if ! pgrep -xf "python3 ./telegram_bots/trespalmerasbot.py" > /dev/null; then
        # echo "Starting the process. Sleeping for 5 seconds..."
        nohup python3 ./telegram_bots/trespalmerasbot.py &
        sleep 5
    else
        # echo "Process is running. Sleeping for 2 minutes..."
        sleep 2m
    fi
done
