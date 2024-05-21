#!/bin/bash

start_time="09:30:00"

while true; do
    current_time=$(date +%H:%M:%S)
    current_day=$(date +%u) 
    if [[ "$current_day" -le 5 && "$current_time" > "$start_time" ]]; then
        break
    fi
    sleep 1
done

while true; do
    python -u WebSocket.py &

    echo $! > /tmp/websocket_pid

    end_time="16:00:00"
    while true; do
        current_time=$(date +%H:%M:%S)
        current_day=$(date +%u) 
        if [[ "$current_day" -le 5 && "$current_time" > "$end_time" ]]; then
            if [ -f "/tmp/websocket_pid" ]; then
                script_pid=$(cat /tmp/websocket_pid)
                kill -9 "$script_pid"
                rm /tmp/websocket_pid
            fi
            break
        fi
        sleep 1
    done

    sleep_seconds=$((86400 - $(date +%s -d "09:30:00")))
    sleep $sleep_seconds
done
