#!/bin/bash

rm -f ~/.local/state/wireplumber/default-nodes
systemctl --user restart wireplumber
sleep 1

if ! wpctl set-default 37 2>/dev/null; then
    wpctl set-default 38
fi
