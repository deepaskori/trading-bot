#!/bin/bash

start_time="16:05:00"
end_time="16:06:00"

while true; do
    current_time=$(date +%H:%M:%S)
    current_day=$(date +%u)
    if [[ "$current_day" -le 5 && "$current_time" > "$start_time" ]]; then
        break
    fi
    sleep 1
done

while true; do
    current_time=$(date +%H:%M:%S)
    current_day=$(date +%u)
    if [[ "$current_day" -le 5 && "$current_time" > "$start_time" && "$current_time" < "$end_time" ]]; then
        python -u BuySell.py
    fi
    sleep 1
done
