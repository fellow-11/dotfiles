#!/bin/bash

rm -f ~/.local/state/wireplumber/default-nodes
systemctl --user restart wireplumber

sleep 1

wpctl set-default 115

sleep 1

systemctl --user restart wireplumber
