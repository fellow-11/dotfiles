#!/bin/sh
LOG="/var/log/t2-suspend-fix.log"
log() { echo "[$(date '+%Y_%m_%d-%H:%M:%S')][resume] $*" >> "$LOG" 2>/dev/null || true; }

log "Starting resume..."
/usr/bin/modprobe apple_bce 2>/dev/null || true
log "Loaded apple_bce"
sleep 1

if [ ! -e /sys/bus/pci/devices/0000:04:00.3/driver ]; then
    echo "0000:04:00.3" > /sys/bus/pci/drivers/aaudio/bind 2>/dev/null || true
    log "Rebound audio PCI device"
fi

/usr/bin/modprobe apple_gmux 2>/dev/null || true
log "Loaded apple_gmux"
/usr/local/bin/t2-drm-display.sh off
log "DRM display off"
/usr/local/bin/t2-drm-display.sh on
log "DRM display on"

for dev in 00:14.0 09:00.0 7f:00.0; do
    if [ ! -e /sys/bus/pci/devices/0000:$dev/driver ]; then
        echo "0000:$dev" > /sys/bus/pci/drivers/xhci_hcd/bind 2>/dev/null || true
        log "Rebound xhci_hcd $dev"
    fi
done

for mod in appletbdrm hid_appletb_kbd hid_appletb_bl; do
    /usr/bin/modprobe "$mod" 2>/dev/null || true
    log "Loaded $mod"
done

sleep 2
systemctl restart tiny-dfr 2>/dev/null || true
log "Restarted tiny-dfr"

/usr/bin/brightnessctl -sd :white:kbd_backlight set 10% -q 2>/dev/null || true
/usr/bin/brightnessctl -d gmux_backlight set 10% -q 2>/dev/null || true

log "Resume complete"
