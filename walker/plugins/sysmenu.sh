#!/bin/bash

# --- MENU DATA STRUCTURES ---

main_menu() {
    echo "Apps"
    echo "Learning..."
    echo "Capture..."
    echo "Toggle..."
    echo "Style..."
    echo "Setup..."
    echo "Configs..."
    echo "Install..."
    echo "Remove..."
    echo "Update..."
    echo "About"
    echo "System..."
}

submenu_learning() {
    echo "Learning -> Keybindings"
    echo "Learning -> CachyOS Wiki"
    echo "Learning -> Hyprland Wiki"
    echo "Learning -> Arch Wiki"
    echo "Learning -> Neovim Docs"
    echo "Learning -> Bash Manuals"
    echo "<- Back to Main Menu"
}

submenu_capture() {
    echo "Capture -> Screenshot"
    echo "Capture -> Screen Recording"
    echo "Capture -> Color Picker"
    echo "Capture -> OCR Text Extraction"
    echo "<- Back to Main Menu"
}

submenu_toggle() {
    echo "Toggle -> Waybar Top Bar"
    echo "Toggle -> Screen Shader"
    echo "Toggle -> Idle Timeout"
    echo "<- Back to Main Menu"
}

submenu_style() {
    echo "Style -> Theme Selector"
    echo "Style -> Font Style"
    echo "Style -> Desktop Wallpaper"
    echo "<- Back to Main Menu"
}

submenu_setup() {
    echo "Setup -> Audio TUI Configuration"
    echo "Setup -> Wi-Fi Manager"
    echo "Setup -> Bluetooth Devices"
    echo "Setup -> Monitor Layout & Scaling"
    echo "Setup -> Keybindings Config"
    echo "Setup -> Input Layout & Repeat Rate"
    echo "Setup -> Mouse & Touchpad Sensitivity"
    echo "Setup -> Fingerprint Sensor Setup"
    echo "Setup -> Default Apps (Editor/Browser/Terminal)"
    echo "<- Back to Main Menu"
}

submenu_configs() {
    echo "Configs -> Hyprland Settings"
    echo "Configs -> Hypridle Setup"
    echo "Configs -> Hyprlock Screen"
    echo "Configs -> Walker Launcher"
    echo "Configs -> Waybar Customization"
    echo "Configs -> Mako Notifications"
    echo "Configs -> SwayOSD Volume Overlay"
    echo "<- Back to Main Menu"
}

submenu_install() {
    echo "Install -> Package"
    echo "Install -> AUR"
    echo "Install -> Web Apps & PWAs"
    echo "<- Back to Main Menu"
}

submenu_remove() {
    echo "Remove -> Package"
    echo "Remove -> AUR"
    echo "Remove -> Web Apps & PWAs"
    echo "<- Back to Main Menu"
}

submenu_update() {
    echo "Update -> Omarchy"
    echo "Update -> System Packages"
    echo "<- Back to Main Menu"
}

submenu_system() {
    echo "System -> Lock Screen"
    echo "System -> Log Out"
    echo "System -> Suspend"
    echo "System -> Reboot"
    echo "System -> Power Off"
    echo "<- Back to Main Menu"
}

# --- RUNTIME EXECUTION ---

if [ -z "$1" ]; then
    main_menu
else
    case "$1" in
        # --- SUBMENU TRIGGERS ---
        "Learning...")     SELECTION=$(submenu_learning | walker --dmenu) && $0 "$SELECTION" ;;
        "Capture...")      SELECTION=$(submenu_capture | walker --dmenu)  && $0 "$SELECTION" ;;
        "Toggle...")       SELECTION=$(submenu_toggle | walker --dmenu)   && $0 "$SELECTION" ;;
        "Style...")        SELECTION=$(submenu_style | walker --dmenu)    && $0 "$SELECTION" ;;
        "Setup...")        SELECTION=$(submenu_setup | walker --dmenu)    && $0 "$SELECTION" ;;
        "Configs...")      SELECTION=$(submenu_configs | walker --dmenu)  && $0 "$SELECTION" ;;
        "Install...")      SELECTION=$(submenu_install | walker --dmenu)  && $0 "$SELECTION" ;;
        "Remove...")       SELECTION=$(submenu_remove | walker --dmenu)   && $0 "$SELECTION" ;;
        "Update...")       SELECTION=$(submenu_update | walker --dmenu)   && $0 "$SELECTION" ;;
        "System...")       SELECTION=$(submenu_system | walker --dmenu)   && $0 "$SELECTION" ;;
        "<- Back to Main Menu") SELECTION=$(main_menu | walker --dmenu)   && $0 "$SELECTION" ;;

        # --- CORE ACTIONS ---
        "Apps")
            walker --modules applications
            ;;

        # Learning Actions
        "Learning -> Keybindings")
            alacritty -e sh -c "echo '=== SYSTEM KEYBINDINGS ===' && hyprctl binds | grep -E 'modmask|key|dispatcher|arg' | awk '{print \$0}' && echo '' && read -p 'Press Enter to close...'"
            ;;
        "Learning -> CachyOS Wiki")    xdg-open "https://wiki.cachyos.org/" ;;
        "Learning -> Hyprland Wiki")   xdg-open "https://wiki.hyprland.org/" ;;
        "Learning -> Arch Wiki")       xdg-open "https://wiki.archlinux.org/" ;;
        "Learning -> Neovim Docs")     alacritty -e nvim +h ;;
        "Learning -> Bash Manuals")    alacritty -e man bash ;;

        # Capture Actions
        "Capture -> Screenshot")      grimblast copysave area ;;
        "Capture -> Color Picker")    hyprpicker -a ;;
        "Capture -> Screen Recording"|"Capture -> OCR Text Extraction")
            notify-send "Menu" "Action coming soon!" ;;

        # Toggle Actions
        "Toggle -> Waybar Top Bar")  pkill -USR1 waybar || waybar & disown ;;
        "Toggle -> Screen Shader"|"Toggle -> Idle Timeout")
            notify-send "Toggle" "Action coming soon!" ;;

        # Configs Quick-Open Actions
        "Configs -> Hyprland Settings")  kate ~/.config/hypr/hyprland.lua ;;
        "Configs -> Waybar Customization") kate ~/.config/waybar/config.jsonc ;;
        "Configs -> Walker Launcher")    kate ~/.config/walker/config.toml ;;

        # Setup Quick-Open Actions
        "Setup -> Wi-Fi Manager")       alacritty -e nmtui ;;
        "Setup -> Bluetooth Devices")   alacritty -e bluetuith || blueman-manager ;;
        "Setup -> Audio TUI Configuration") alacritty -e pulsemixer || alacritty -e ncmcpp ;;
        "Setup -> Keybindings Config")  kate ~/.config/hypr/hyprland.lua ;;

        # System Actions
        "System -> Lock Screen")     hyprlock ;;
        "System -> Log Out")         hyprctl dispatch exit ;;
        "System -> Suspend")         systemctl suspend ;;
        "System -> Reboot")          systemctl reboot ;;
        "System -> Power Off")       systemctl poweroff ;;

        # Fallback
        "About"|*)
            if [ ! -z "$1" ] && [ "$1" != "<- Back to Main Menu" ]; then
                notify-send "System Menu" "Shortcut selected: $1"
            fi
            ;;
    esac
fi
