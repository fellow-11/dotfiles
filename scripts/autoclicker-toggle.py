#!/usr/bin/env python3
"""
autoclicker-daemon.py — background clicker for Hyprland/Wayland (T2 CachyOS)

Reads settings from ~/.config/autoclicker/config.json (created with
defaults on first run if missing) and clicks in the background. Has no GUI
dependency at all -- meant to be called by a system-wide Hyprland keybind.

Usage:
  autoclicker-daemon.py --toggle   # start if stopped, stop if running
  autoclicker-daemon.py --start
  autoclicker-daemon.py --stop
  autoclicker-daemon.py --status

State:
  PID file:    ~/.config/autoclicker/daemon.pid
  Config file: ~/.config/autoclicker/config.json
"""

import sys
import os
import json
import random
import signal
import subprocess
import time

DATA_DIR = os.path.expanduser("~/.config/autoclicker")
CONFIG_PATH = os.path.join(DATA_DIR, "config.json")
PID_PATH = os.path.join(DATA_DIR, "daemon.pid")

DEFAULT_CONFIG = {
    "interval_ms": 100,
    "random_offset_ms": 40,
    "random_offset_enabled": False,
    "button": "Left",          # Left / Right / Middle
    "double_click": False,
    "repeat_mode": "until_stopped",  # "count" or "until_stopped"
    "repeat_count": 1,
    "use_fixed_pos": False,
    "pos_x": 0,
    "pos_y": 0,
    "hotkey": "F6",
    "pick_countdown_secs": 3,
    "click_jitter_px": 0,
    "start_delay_secs": 0,
    "notify_on_toggle": True,
    "compact_mode": False,
    "always_on_top": False,
}

BUTTON_CODES = {"Left": "0xC0", "Right": "0xC1", "Middle": "0xC2"}


def ensure_config():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)
        return dict(DEFAULT_CONFIG)
    with open(CONFIG_PATH) as f:
        cfg = json.load(f)
    # backfill any missing keys from defaults (safe upgrades)
    merged = dict(DEFAULT_CONFIG)
    merged.update(cfg)
    return merged


def ydotool_click(button):
    subprocess.run(["ydotool", "click", BUTTON_CODES[button]], check=False)


def hypr_movecursor(x, y):
    subprocess.run(["hyprctl", "dispatch", f"hl.dsp.movecursor({x}, {y})"], check=False)


def notify(title, body):
    subprocess.run(["notify-send", title, body], check=False)


def read_pid():
    if not os.path.exists(PID_PATH):
        return None
    try:
        with open(PID_PATH) as f:
            pid = int(f.read().strip())
        os.kill(pid, 0)  # check alive
        return pid
    except (OSError, ValueError):
        try:
            os.remove(PID_PATH)
        except OSError:
            pass
        return None


def start_daemon():
    if read_pid():
        print("already running")
        return
    pid = os.fork()
    if pid > 0:
        return  # parent returns immediately
    # child: detach and run the click loop
    os.setsid()
    with open(PID_PATH, "w") as f:
        f.write(str(os.getpid()))
    run_click_loop()
    sys.exit(0)


def stop_daemon():
    pid = read_pid()
    if not pid:
        print("not running")
        return
    try:
        os.kill(pid, signal.SIGTERM)
    except OSError:
        pass
    try:
        os.remove(PID_PATH)
    except OSError:
        pass


def run_click_loop():
    cfg = ensure_config()
    interval = cfg["interval_ms"]
    offset = cfg["random_offset_ms"] if cfg["random_offset_enabled"] else 0
    button = cfg["button"]
    double = cfg["double_click"]
    repeat_mode = cfg["repeat_mode"]
    repeat_count = cfg["repeat_count"]
    use_fixed = cfg["use_fixed_pos"]
    pos_xy = (cfg["pos_x"], cfg["pos_y"]) if use_fixed else None
    jitter = cfg.get("click_jitter_px", 0)
    start_delay = cfg.get("start_delay_secs", 0)
    notify_toggle = cfg.get("notify_on_toggle", True)

    def handle_term(signum, frame):
        subprocess.run(["ydotool", "click", "0x80"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)

        if notify_toggle:
            notify("Autoclicker", "Stopped")
        sys.exit(0)

    signal.signal(signal.SIGTERM, handle_term)

    if notify_toggle:
        notify("Autoclicker", "Started")

    if start_delay > 0:
        time.sleep(start_delay)

    count = 0
    while True:
        if use_fixed and pos_xy:
            x, y = pos_xy
            if jitter > 0:
                x += random.randint(-jitter, jitter)
                y += random.randint(-jitter, jitter)
            hypr_movecursor(x, y)
        elif jitter > 0:
            pos = None
            try:
                out = subprocess.run(["hyprctl", "cursorpos", "-j"],
                                      capture_output=True, text=True, check=True)
                data = json.loads(out.stdout)
                pos = (int(data["x"]), int(data["y"]))
            except Exception:
                pos = None
            if pos:
                x = pos[0] + random.randint(-jitter, jitter)
                y = pos[1] + random.randint(-jitter, jitter)
                hypr_movecursor(x, y)
        ydotool_click(button)
        if double:
            time.sleep(0.05)
            ydotool_click(button)
        count += 1
        if repeat_mode == "count" and count >= repeat_count:
            break
        wait = interval
        if offset > 0:
            wait += random.uniform(-offset, offset)
        time.sleep(max(wait, 1) / 1000.0)

    if notify_toggle:
        notify("Autoclicker", "Finished")
    try:
        os.remove(PID_PATH)
    except OSError:
        pass


def main():
    ensure_config()
    args = sys.argv[1:]
    if "--status" in args:
        pid = read_pid()
        print(f"running (pid {pid})" if pid else "stopped")
    elif "--start" in args:
        start_daemon()
    elif "--stop" in args:
        stop_daemon()
    elif "--toggle" in args:
        if read_pid():
            stop_daemon()
        else:
            start_daemon()
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
