#!/bin/bash

STATE_FILE="/tmp/hypr-gamemode"

if [[ -f "$STATE_FILE" ]]; then
    rm "$STATE_FILE"
    hyprctl dispatch "hl.dsp.submap('reset')"
    systemctl --user start hypridle
    powerprofilesctl set balanced
    notify-send "Gamemode" "Off" -t 2000
else
    touch "$STATE_FILE"
    systemctl --user stop hypridle
    powerprofilesctl set performance
    hyprctl dispatch "hl.dsp.submap('gamemode')"
    notify-send "Gamemode" "On" -t 2000
fi
