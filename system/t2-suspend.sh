#!/bin/sh
LOG="/var/log/t2-suspend-fix.log"
log() { echo "[$(date '+%Y_%m_%d-%H:%M:%S')][suspend] $*" >> "$LOG" 2>/dev/null || true; }

log "Starting suspend sequence..."
systemctl stop tiny-dfr 2>/dev/null || true
/usr/bin/brightnessctl -sd :white:kbd_backlight set 0 -q 2>/dev/null || true

if [ -e /sys/bus/pci/devices/0000:04:00.3/driver ]; then
    echo "0000:04:00.3" > /sys/bus/pci/drivers/aaudio/unbind 2>/dev/null || true
    log "Unbound audio PCI device"
fi

for mod in hid_appletb_bl hid_appletb_kbd appletbdrm; do
    if lsmod | grep -q "^${mod}"; then
        /usr/bin/modprobe -r "$mod" 2>/dev/null || true
        log "Unloaded $mod"
    fi
done

for dev in 09:00.0 7f:00.0 00:14.0; do
    if [ -e /sys/bus/pci/devices/0000:$dev/driver ]; then
        echo "0000:$dev" > /sys/bus/pci/drivers/xhci_hcd/unbind 2>/dev/null || true
        log "Unbound xhci_hcd $dev"
    fi
done

if lsmod | grep -q "^apple_gmux"; then
    /usr/bin/modprobe -r apple_gmux 2>/dev/null || true
    /usr/local/bin/t2-drm-display.sh off
    log "DRM display off"
    log "Unloaded apple_gmux"
fi

if lsmod | grep -q "^apple_bce"; then
    /usr/bin/modprobe -r apple_bce 2>/dev/null || true
    log "Unloaded apple_bce"
fi

log "Suspend complete, ready to sleep"
