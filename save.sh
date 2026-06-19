#!/bin/bash

DOTFILES="$HOME/dotfiles"

echo "Saving dotfiles..."

# ~/.config dirs
cp -r ~/.config/hypr/* "$DOTFILES/hypr/"
cp -r ~/.config/waybar/* "$DOTFILES/waybar/"
cp -r ~/.config/alacritty/* "$DOTFILES/alacritty/"
cp -r ~/.config/walker/* "$DOTFILES/walker/"
cp -r ~/.config/fish/* "$DOTFILES/fish/"
cp -r ~/.config/theme/* "$DOTFILES/theme/"
cp -r ~/.config/btop/* "$DOTFILES/btop/"
cp -r ~/.config/gtk-3.0/* "$DOTFILES/gtk-3.0/" 2>/dev/null
cp -r ~/.config/gtk-4.0/* "$DOTFILES/gtk-4.0/" 2>/dev/null
cp -r ~/.config/wireplumber/* "$DOTFILES/wireplumber/" 2>/dev/null
cp -r ~/.config/micro/* "$DOTFILES/micro/" 2>/dev/null
cp -r ~/.config/wiremix/* "$DOTFILES/wiremix/" 2>/dev/null
cp -r ~/.config/magicpods/* "$DOTFILES/magicpods/" 2>/dev/null
cp -r ~/.config/mako/* "$DOTFILES/mako/" 2>/dev/null
cp -r ~/.config/swayosd/* "$DOTFILES/swayosd/" 2>/dev/null
cp -r ~/.config/wlogout/* "$DOTFILES/wlogout/" 2>/dev/null

# Shell
cp ~/.zshrc "$DOTFILES/zsh/"

# Scripts
cp -r ~/.local/bin/* "$DOTFILES/scripts/" 2>/dev/null

# System
cp /usr/local/bin/t2-suspend.sh "$DOTFILES/system/"
cp /usr/local/bin/t2-resume.sh "$DOTFILES/system/"
cp /etc/t2-suspend-fix/hardware.conf "$DOTFILES/system/"
sudo cp /boot/limine.conf "$DOTFILES/system/"
sudo chown "$USER:$USER" "$DOTFILES/system/limine.conf"

# Systemd
sudo cp /etc/systemd/sleep.conf "$DOTFILES/systemd/"
sudo cp /etc/systemd/logind.conf "$DOTFILES/systemd/"
sudo cp /etc/systemd/timesyncd.conf "$DOTFILES/systemd/"
sudo cp /etc/systemd/journald.conf "$DOTFILES/systemd/"
sudo cp /etc/systemd/system/t2-suspend.service "$DOTFILES/systemd/"
sudo cp /etc/systemd/system/t2-resume.service "$DOTFILES/systemd/"
sudo cp /etc/systemd/system/t2-fix-kbd-backlight.service "$DOTFILES/systemd/"
sudo chown -R "$USER:$USER" "$DOTFILES/systemd/"

# Wallpapers
cp -r ~/.local/share/wallpapers/custom-wallpapers/* "$DOTFILES/wallpapers/" 2>/dev/null

# README
mkdir "$DOTFILES/screenshots"
cp -r ~/dotfiles-screenshots/* "$DOTFILES/screenshots/"

# Commit and push
cd "$DOTFILES"
git add .
git commit -m "dotfiles update: $(date '+%Y-%m-%d %H:%M')"
git push

echo "Done."
