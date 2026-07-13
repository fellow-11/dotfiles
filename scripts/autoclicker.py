#!/usr/bin/env python3
"""
autoclicker.py — GTK4 settings GUI for the autoclicker daemon.

This window does NOT click anything itself. It only reads/writes
~/.config/autoclicker/config.json. The actual clicking is done by
autoclicker-toggle.py, which is toggled independently (e.g. via a
system-wide Hyprland F6 keybind) and works with the GUI closed.

Theming: loads ~/.config/autoclicker/gui-config.css if present (rendered by
sync-theme from ~/.config/theme/templates/autoclicker-gui-config.css, or
hand-edited directly). This one file holds ALL visual settings -- colors,
font-size/scale, spacing, borders. Falls back to default GTK styling if
missing.

Requires: python-gobject, gtk4
"""

import os
import json
import subprocess

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio, GLib, Gdk

DATA_DIR = os.path.expanduser("~/.config/autoclicker")
CONFIG_PATH = os.path.join(DATA_DIR, "config.json")
PID_PATH = os.path.join(DATA_DIR, "daemon.pid")
THEME_CSS_PATH = os.path.expanduser("~/.config/autoclicker/gui-config.css")

DEFAULT_CONFIG = {
    # click behavior
    "interval_ms": 100,
    "random_offset_ms": 40,
    "random_offset_enabled": False,
    "button": "Left",
    "double_click": False,
    "repeat_mode": "until_stopped",   # "count" or "until_stopped"
    "repeat_count": 1,
    "use_fixed_pos": False,
    "pos_x": 0,
    "pos_y": 0,
    # customization
    "hotkey": "F6",                   # informational label only; actual bind lives in hyprland.lua
    "pick_countdown_secs": 3,
    "click_jitter_px": 0,             # random +-px cursor wiggle before each click (0 = off)
    "start_delay_secs": 0,            # delay before first click after toggling on
    "notify_on_toggle": True,         # send a notification via notify-send on start/stop
    "compact_mode": False,            # hides hint text / tightens spacing
    "always_on_top": False,
}


def load_config():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(CONFIG_PATH):
        save_config(DEFAULT_CONFIG)
        return dict(DEFAULT_CONFIG)
    with open(CONFIG_PATH) as f:
        cfg = json.load(f)
    merged = dict(DEFAULT_CONFIG)
    merged.update(cfg)
    return merged


def save_config(cfg):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2)


def daemon_running():
    if not os.path.exists(PID_PATH):
        return False
    try:
        with open(PID_PATH) as f:
            pid = int(f.read().strip())
        os.kill(pid, 0)
        return True
    except (OSError, ValueError):
        return False


def hypr_cursorpos():
    try:
        out = subprocess.run(["hyprctl", "cursorpos", "-j"],
                              capture_output=True, text=True, check=True)
        data = json.loads(out.stdout)
        return int(data["x"]), int(data["y"])
    except Exception:
        return None


def load_theme_css():
    provider = Gtk.CssProvider()
    if os.path.exists(THEME_CSS_PATH):
        try:
            provider.load_from_path(THEME_CSS_PATH)
        except GLib.Error:
            return
        display = Gdk.Display.get_default()
        Gtk.StyleContext.add_provider_for_display(
            display, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )


def spin(minv, maxv, value, step=1, width_chars=4):
    s = Gtk.SpinButton.new_with_range(minv, maxv, step)
    s.set_value(value)
    s.set_width_chars(width_chars)
    s.set_max_width_chars(width_chars)
    return s


def frame(label_text):
    fr = Gtk.Frame()
    lbl = Gtk.Label(label=f"  {label_text}  ")
    fr.set_label_widget(lbl)
    inner = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
    inner.add_css_class("autoclicker-frame-inner")
    fr.set_child(inner)
    return fr, inner


class AutoclickerWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title="Autoclicker Settings")
        self.add_css_class("autoclicker-window")
        self.set_resizable(False)
        self.cfg = load_config()
        self._suppress_save = True

        if self.cfg.get("always_on_top"):
            self.set_decorated(True)  # Wayland: real always-on-top needs compositor rule

        scroller = Gtk.ScrolledWindow()
        scroller.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroller.set_propagate_natural_height(True)
        scroller.set_propagate_natural_width(True)
        scroller.set_max_content_height(820)  # cap: scrolls only past this
        self.set_child(scroller)

        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        root.add_css_class("autoclicker-root")
        scroller.set_child(root)

        # ---- status banner ----
        self.status_label = Gtk.Label()
        self.status_label.add_css_class("autoclicker-status")
        root.append(self.status_label)
        self.note = Gtk.Label(
            label=f"Settings save automatically. Toggle clicking with "
                  f"{self.cfg['hotkey']} system-wide — this window doesn't need to stay open.")
        self.note.add_css_class("dim-label")
        self.note.set_wrap(True)
        self.note.set_max_width_chars(50)
        self.note.set_halign(Gtk.Align.START)
        root.append(self.note)

        # ---- Click interval ----
        fr, box = frame("Click interval")
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        total_ms = self.cfg["interval_ms"]
        h, rem = divmod(total_ms, 3600000)
        m, rem = divmod(rem, 60000)
        s, ms = divmod(rem, 1000)
        self.hours = spin(0, 999, h)
        self.mins = spin(0, 59, m)
        self.secs = spin(0, 59, s)
        self.ms = spin(0, 999, ms)
        for w, lbl in [(self.hours, "hours"), (self.mins, "mins"),
                       (self.secs, "secs"), (self.ms, "milliseconds")]:
            row.append(w)
            row.append(Gtk.Label(label=lbl))
            w.connect("value-changed", self.on_change)
        box.append(row)

        offset_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.random_offset_chk = Gtk.CheckButton(label="Random offset +-")
        self.random_offset_chk.set_active(self.cfg["random_offset_enabled"])
        self.random_offset_chk.connect("toggled", self.on_change)
        self.offset_ms = spin(0, 5000, self.cfg["random_offset_ms"])
        self.offset_ms.connect("value-changed", self.on_change)
        offset_row.append(self.random_offset_chk)
        offset_row.append(self.offset_ms)
        offset_row.append(Gtk.Label(label="milliseconds"))
        box.append(offset_row)
        root.append(fr)

        # ---- Click options + repeat ----
        mid = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        mid.set_homogeneous(True)

        opt_fr, opt_box = frame("Click options")
        btn_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        btn_row.append(Gtk.Label(label="Mouse button:"))
        self.button_dd = Gtk.DropDown.new_from_strings(["Left", "Right", "Middle"])
        self.button_dd.set_selected(["Left", "Right", "Middle"].index(self.cfg["button"]))
        self.button_dd.connect("notify::selected", self.on_change)
        btn_row.append(self.button_dd)
        opt_box.append(btn_row)

        type_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        type_row.append(Gtk.Label(label="Click type:"))
        self.type_dd = Gtk.DropDown.new_from_strings(["Single", "Double"])
        self.type_dd.set_selected(1 if self.cfg["double_click"] else 0)
        self.type_dd.connect("notify::selected", self.on_change)
        type_row.append(self.type_dd)
        opt_box.append(type_row)
        mid.append(opt_fr)

        rep_fr, rep_box = frame("Click repeat")
        self.repeat_n_radio = Gtk.CheckButton(label="Repeat")
        self.repeat_until_radio = Gtk.CheckButton(label="Repeat until stopped")
        self.repeat_until_radio.set_group(self.repeat_n_radio)
        if self.cfg["repeat_mode"] == "until_stopped":
            self.repeat_until_radio.set_active(True)
        else:
            self.repeat_n_radio.set_active(True)
        self.repeat_n_radio.connect("toggled", self.on_change)
        n_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        n_row.append(self.repeat_n_radio)
        self.repeat_count = spin(1, 999999, self.cfg["repeat_count"], width_chars=6)
        self.repeat_count.connect("value-changed", self.on_change)
        n_row.append(self.repeat_count)
        n_row.append(Gtk.Label(label="times"))
        rep_box.append(n_row)
        rep_box.append(self.repeat_until_radio)
        mid.append(rep_fr)
        root.append(mid)

        # ---- Cursor position ----
        pos_fr, pos_box = frame("Cursor position")
        pos_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.current_loc_radio = Gtk.CheckButton(label="Current location")
        self.fixed_loc_radio = Gtk.CheckButton()
        self.fixed_loc_radio.set_group(self.current_loc_radio)
        if self.cfg["use_fixed_pos"]:
            self.fixed_loc_radio.set_active(True)
        else:
            self.current_loc_radio.set_active(True)
        self.fixed_loc_radio.connect("toggled", self.on_change)
        pick_btn = Gtk.Button(label="Pick location")
        pick_btn.connect("clicked", self.on_pick_location)
        self.x_spin = spin(0, 20000, self.cfg["pos_x"], width_chars=5)
        self.y_spin = spin(0, 20000, self.cfg["pos_y"], width_chars=5)
        self.x_spin.connect("value-changed", self.on_change)
        self.y_spin.connect("value-changed", self.on_change)

        pos_row.append(self.current_loc_radio)
        pos_row.append(self.fixed_loc_radio)
        pos_row.append(pick_btn)
        pos_row.append(Gtk.Label(label="X"))
        pos_row.append(self.x_spin)
        pos_row.append(Gtk.Label(label="Y"))
        pos_row.append(self.y_spin)
        pos_box.append(pos_row)
        root.append(pos_fr)

        # ---- Advanced / customization (collapsed by default) ----
        adv_expander = Gtk.Expander(label="Advanced")
        adv_expander.set_expanded(False)
        adv_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        adv_box.add_css_class("autoclicker-frame-inner")

        jitter_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        jitter_row.append(Gtk.Label(label="Click jitter +-"))
        self.jitter_spin = spin(0, 200, self.cfg["click_jitter_px"])
        self.jitter_spin.connect("value-changed", self.on_change)
        jitter_row.append(self.jitter_spin)
        jitter_px_label = Gtk.Label(label="px")
        jitter_px_label.set_tooltip_text("Randomizes cursor position slightly before each click")
        jitter_row.append(jitter_px_label)
        adv_box.append(jitter_row)

        delay_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        delay_row.append(Gtk.Label(label="Start delay"))
        self.delay_spin = spin(0, 60, self.cfg["start_delay_secs"])
        self.delay_spin.connect("value-changed", self.on_change)
        delay_row.append(self.delay_spin)
        delay_row.append(Gtk.Label(label="seconds before first click"))
        adv_box.append(delay_row)

        countdown_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        countdown_row.append(Gtk.Label(label="Pick-location countdown"))
        self.countdown_spin = spin(0, 10, self.cfg["pick_countdown_secs"])
        self.countdown_spin.connect("value-changed", self.on_change)
        countdown_row.append(self.countdown_spin)
        countdown_row.append(Gtk.Label(label="seconds"))
        adv_box.append(countdown_row)

        self.notify_chk = Gtk.CheckButton(label="Notify on start/stop (notify-send)")
        self.notify_chk.set_active(self.cfg["notify_on_toggle"])
        self.notify_chk.connect("toggled", self.on_change)
        adv_box.append(self.notify_chk)

        self.compact_chk = Gtk.CheckButton(label="Compact mode")
        self.compact_chk.set_active(self.cfg["compact_mode"])
        self.compact_chk.connect("toggled", self.on_compact_toggle)
        adv_box.append(self.compact_chk)

        adv_expander.set_child(adv_box)
        root.append(adv_expander)

        # ---- manual start/stop buttons ----
        action_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        action_row.set_homogeneous(True)
        self.start_btn = Gtk.Button()
        self.start_btn.add_css_class("suggested-action")
        self.start_btn.connect("clicked", self.on_start_clicked)
        self.stop_btn = Gtk.Button(label="Stop")
        self.stop_btn.add_css_class("destructive-action")
        self.stop_btn.connect("clicked", self.on_stop_clicked)
        action_row.append(self.start_btn)
        action_row.append(self.stop_btn)
        root.append(action_row)

        reload_btn = Gtk.Button(label="Reload theme")
        reload_btn.connect("clicked", lambda _b: load_theme_css())
        root.append(reload_btn)

        self._suppress_save = False
        load_theme_css()
        self.apply_compact(self.cfg["compact_mode"])
        self.refresh_status()
        GLib.timeout_add_seconds(1, self.poll_status)

    def apply_compact(self, compact):
        self.note.set_visible(not compact)

    def on_compact_toggle(self, chk):
        self.apply_compact(chk.get_active())
        self.on_change()

    def refresh_status(self):
        running = daemon_running()
        self.status_label.set_label("● Clicking" if running else "○ Idle")
        self.status_label.remove_css_class("status-running")
        self.status_label.remove_css_class("status-idle")
        self.status_label.add_css_class("status-running" if running else "status-idle")
        self.start_btn.set_label(f"Start ({self.cfg['hotkey']})")
        self.start_btn.set_sensitive(not running)
        self.stop_btn.set_sensitive(running)

    def poll_status(self):
        self.refresh_status()
        return True

    def on_start_clicked(self, _btn):
        subprocess.run(["autoclicker-toggle.py", "--start"], check=False)
        self.refresh_status()

    def on_stop_clicked(self, _btn):
        subprocess.run(["autoclicker-toggle.py", "--stop"], check=False)
        self.refresh_status()

    def on_pick_location(self, btn):
        btn.set_sensitive(False)
        secs = int(self.countdown_spin.get_value())

        def countdown(n):
            if n <= 0:
                pos = hypr_cursorpos()
                if pos:
                    self.x_spin.set_value(pos[0])
                    self.y_spin.set_value(pos[1])
                    self.fixed_loc_radio.set_active(True)
                btn.set_sensitive(True)
                self.refresh_status()
                return False
            self.status_label.set_label(f"Picking location in {n}...")
            GLib.timeout_add_seconds(1, countdown, n - 1)
            return False

        if secs <= 0:
            countdown(0)
        else:
            self.status_label.set_label(f"Picking location in {secs}...")
            GLib.timeout_add_seconds(1, countdown, secs - 1)

    def on_change(self, *_args):
        if self._suppress_save:
            return
        cfg = {
            "interval_ms": int(
                (self.hours.get_value() * 3600 + self.mins.get_value() * 60 +
                 self.secs.get_value()) * 1000 + self.ms.get_value()
            ),
            "random_offset_ms": int(self.offset_ms.get_value()),
            "random_offset_enabled": self.random_offset_chk.get_active(),
            "button": ["Left", "Right", "Middle"][self.button_dd.get_selected()],
            "double_click": self.type_dd.get_selected() == 1,
            "repeat_mode": "count" if self.repeat_n_radio.get_active() else "until_stopped",
            "repeat_count": int(self.repeat_count.get_value()),
            "use_fixed_pos": self.fixed_loc_radio.get_active(),
            "pos_x": int(self.x_spin.get_value()),
            "pos_y": int(self.y_spin.get_value()),
            "hotkey": self.cfg["hotkey"],
            "pick_countdown_secs": int(self.countdown_spin.get_value()),
            "click_jitter_px": int(self.jitter_spin.get_value()),
            "start_delay_secs": int(self.delay_spin.get_value()),
            "notify_on_toggle": self.notify_chk.get_active(),
            "compact_mode": self.compact_chk.get_active(),
            "always_on_top": self.cfg["always_on_top"],
        }
        self.cfg = cfg
        save_config(cfg)


class AutoclickerApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="dev.felix.autoclicker")

    def do_activate(self):
        win = AutoclickerWindow(self)
        win.present()


if __name__ == "__main__":
    import sys
    app = AutoclickerApp()
    sys.exit(app.run(sys.argv))
