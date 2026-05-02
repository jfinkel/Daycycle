#!/usr/bin/env python3
"""Settings UI for daycycle-wallpaper."""

from __future__ import annotations

import pathlib
import shlex
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from zoneinfo import ZoneInfo

try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
except ImportError:
    DND_FILES = None
    TkinterDnD = None

CONFIG_PATH = pathlib.Path.home() / ".config" / "daycycle-wallpaper.conf"
SERVICE_PATH = pathlib.Path.home() / ".config" / "systemd" / "user" / "daycycle-wallpaper.service"
TIMER_PATH = pathlib.Path.home() / ".config" / "systemd" / "user" / "daycycle-wallpaper.timer"
SCRIPT_PATH = pathlib.Path.home() / "bin" / "daycycle-wallpaper.sh"

RULES = ["sunrise", "sunset", "noon", "midnight", "clock"]
SLOT_LABELS = [
    "Slot 1",
    "Slot 2",
    "Slot 3",
    "Slot 4",
    "Slot 5",
    "Slot 6",
]

DEFAULTS = {
    "WALLDIR": str(pathlib.Path.home() / "wallpapers" / "daycycle"),
    "CITY_NAME": "Chicago",
    "REGION": "USA",
    "TIMEZONE": "America/Chicago",
    "LATITUDE": "41.93",
    "LONGITUDE": "-87.87",
    "IMAGE_1": str(pathlib.Path.home() / "wallpapers" / "daycycle" / "1-morning.jpg"),
    "IMAGE_2": str(pathlib.Path.home() / "wallpapers" / "daycycle" / "2-late-morning.jpg"),
    "IMAGE_3": str(pathlib.Path.home() / "wallpapers" / "daycycle" / "3-afternoon.jpg"),
    "IMAGE_4": str(pathlib.Path.home() / "wallpapers" / "daycycle" / "4-evening.jpg"),
    "IMAGE_5": str(pathlib.Path.home() / "wallpapers" / "daycycle" / "5-night.jpg"),
    "IMAGE_6": str(pathlib.Path.home() / "wallpapers" / "daycycle" / "6-late-night.jpg"),
    "RULE_1": "sunrise",
    "RULE_2": "sunrise",
    "RULE_3": "noon",
    "RULE_4": "sunset",
    "RULE_5": "sunset",
    "RULE_6": "midnight",
    "OFFSET_MIN_1": "0",
    "OFFSET_MIN_2": "120",
    "OFFSET_MIN_3": "0",
    "OFFSET_MIN_4": "-180",
    "OFFSET_MIN_5": "0",
    "OFFSET_MIN_6": "0",
    "CLOCK_TIME_1": "06:00",
    "CLOCK_TIME_2": "09:00",
    "CLOCK_TIME_3": "12:00",
    "CLOCK_TIME_4": "18:00",
    "CLOCK_TIME_5": "21:00",
    "CLOCK_TIME_6": "00:00",
}

SERVICE_TEXT = """[Unit]
Description=Update wallpaper by sun position

[Service]
Type=oneshot
Environment=DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/%U/bus
ExecStart=%h/bin/daycycle-wallpaper.sh
"""

TIMER_TEXT = """[Unit]
Description=Run daycycle wallpaper updater

[Timer]
OnBootSec=1min
OnUnitActiveSec=15min
Persistent=true

[Install]
WantedBy=timers.target
"""


def parse_config(path: pathlib.Path) -> dict[str, str]:
    values = DEFAULTS.copy()
    if not path.exists():
        return values

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        values[key] = value
    return values


def write_config(path: pathlib.Path, values: dict[str, str]) -> None:
    keys = ["WALLDIR", "CITY_NAME", "REGION", "TIMEZONE", "LATITUDE", "LONGITUDE"]
    for i in range(1, 7):
        keys.extend([f"IMAGE_{i}", f"RULE_{i}", f"OFFSET_MIN_{i}", f"CLOCK_TIME_{i}"])

    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Managed by daycycle-settings.py"]
    for key in keys:
        lines.append(f"{key}={shlex.quote(values[key])}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


class App:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Daycycle Wallpaper Settings")
        self.values = parse_config(CONFIG_PATH)
        self.drop_enabled = TkinterDnD is not None
        self.show_thumbnails = Image is not None and ImageTk is not None
        self.thumbnail_labels: dict[str, tk.Label] = {}  # Store thumbnail label widgets

        outer = ttk.Frame(root, padding=12)
        outer.grid(row=0, column=0, sticky="nsew")

        self.vars: dict[str, tk.StringVar] = {}

        self._add_simple(
            outer,
            0,
            "Wallpaper Folder",
            "WALLDIR",
            browse_command=lambda: self.pick_directory("WALLDIR"),
            browse_text="Browse",
        )
        self._add_simple(outer, 1, "City", "CITY_NAME")
        self._add_simple(outer, 2, "Region/Country", "REGION")
        self._add_simple(outer, 3, "Timezone", "TIMEZONE")
        self._add_simple(outer, 4, "Latitude", "LATITUDE")
        self._add_simple(outer, 5, "Longitude", "LONGITUDE")

        ttk.Label(outer, text="Image Slots", font=("Sans", 10, "bold")).grid(
            row=6, column=0, columnspan=7, sticky="w", pady=(12, 6)
        )
        if self.show_thumbnails:
            ttk.Label(outer, text="Preview").grid(row=7, column=1, sticky="w", padx=(0, 4))
            ttk.Label(outer, text="Image File").grid(row=7, column=2, sticky="w")
        else:
            ttk.Label(outer, text="Image File").grid(row=7, column=1, sticky="w")
        ttk.Label(outer, text="Time Rule").grid(row=7, column=4 if self.show_thumbnails else 3, sticky="w")
        ttk.Label(outer, text="Offset min").grid(row=7, column=5 if self.show_thumbnails else 4, sticky="w")
        ttk.Label(outer, text="Clock HH:MM").grid(row=7, column=6 if self.show_thumbnails else 5, sticky="w")

        start = 8
        for idx, label in enumerate(SLOT_LABELS, start=1):
            row = start + idx - 1
            ttk.Label(outer, text=label).grid(row=row, column=0, sticky="w", padx=(0, 8), pady=4)

            img_key = f"IMAGE_{idx}"
            rule_key = f"RULE_{idx}"
            off_key = f"OFFSET_MIN_{idx}"
            clk_key = f"CLOCK_TIME_{idx}"

            # Add thumbnail display if PIL is available
            if self.show_thumbnails:
                # Create a frame with fixed pixel size to contain the thumbnail
                thumb_frame = tk.Frame(outer, bg="gray20", relief="solid", bd=1)
                thumb_frame.grid(row=row, column=1, sticky="nsew", padx=(0, 4), pady=4)
                # Force frame to fixed size (in pixels via minsize)
                thumb_frame.grid_propagate(False)
                thumb_frame.config(width=120, height=80)
                
                # Create label inside frame without width/height constraints
                thumb_label = tk.Label(thumb_frame, bg="gray20")
                thumb_label.pack(fill="both", expand=True)
                self.thumbnail_labels[img_key] = thumb_label

                img_var = tk.StringVar(value=self.values[img_key])
                self.vars[img_key] = img_var
                img_entry = ttk.Entry(outer, textvariable=img_var, width=25)
                img_entry.grid(row=row, column=2, sticky="w", pady=4)
                # Update thumbnail when image path changes
                img_var.trace_add("write", lambda *args, k=img_key: self._update_thumbnail(k))
                self._update_thumbnail(img_key)  # Load initial thumbnail
                self._enable_drop(img_entry, img_key)
                ttk.Button(outer, text="Browse", command=lambda k=img_key: self.pick_file(k)).grid(
                    row=row, column=3, sticky="w", padx=(6, 0)
                )
                rule_col = 4
                off_col = 5
                clk_col = 6
            else:
                img_var = tk.StringVar(value=self.values[img_key])
                self.vars[img_key] = img_var
                img_entry = ttk.Entry(outer, textvariable=img_var, width=40)
                img_entry.grid(row=row, column=1, columnspan=2, sticky="w", pady=4)
                self._enable_drop(img_entry, img_key)
                ttk.Button(outer, text="Browse", command=lambda k=img_key: self.pick_file(k)).grid(
                    row=row, column=3, sticky="w", padx=(6, 8)
                )
                rule_col = 3
                off_col = 4
                clk_col = 5

            rule_var = tk.StringVar(value=self.values[rule_key])
            self.vars[rule_key] = rule_var
            combo = ttk.Combobox(outer, textvariable=rule_var, width=10, values=RULES, state="readonly")
            combo.grid(row=row, column=rule_col, sticky="w", padx=(0, 8))

            off_var = tk.StringVar(value=self.values[off_key])
            self.vars[off_key] = off_var
            ttk.Entry(outer, textvariable=off_var, width=9).grid(row=row, column=off_col, sticky="w", padx=(0, 8))

            clk_var = tk.StringVar(value=self.values[clk_key])
            self.vars[clk_key] = clk_var
            ttk.Entry(outer, textvariable=clk_var, width=8).grid(row=row, column=clk_col, sticky="w")

        self.remove_cron = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            outer,
            text="Remove old cron entry for this script",
            variable=self.remove_cron,
        ).grid(row=15, column=0, columnspan=4, sticky="w", pady=(10, 8))

        hint = "Drag image files onto slot fields to set paths."
        if not self.drop_enabled:
            hint += " (Install tkinterdnd2 to enable drag-and-drop.)"
        if not self.show_thumbnails:
            hint += " (Install python3-pil.imagetk for thumbnail previews.)"
        ttk.Label(outer, text=hint).grid(row=16, column=0, columnspan=7, sticky="w", pady=(0, 8))

        btns = ttk.Frame(outer)
        btns.grid(row=17, column=0, columnspan=7, sticky="e")
        ttk.Button(btns, text="Save", command=self.save).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(btns, text="Install/Enable Timer", command=self.install_timer).grid(row=0, column=1, padx=(0, 8))
        ttk.Button(btns, text="Run Now", command=self.run_now).grid(row=0, column=2)

    def _enable_drop(self, widget: ttk.Entry, key: str) -> None:
        if not self.drop_enabled or DND_FILES is None:
            return
        try:
            widget.drop_target_register(DND_FILES)
            widget.dnd_bind("<<Drop>>", lambda event, slot=key: self._on_drop(event, slot))
        except Exception:
            # tkinterdnd2 may not be properly initialized, silently fail
            pass

    def _on_drop(self, event, key: str) -> None:
        paths = self.root.tk.splitlist(event.data)
        if not paths:
            return
        dropped = pathlib.Path(paths[0]).expanduser()
        if dropped.is_dir():
            return
        self.vars[key].set(str(dropped))

    def _update_thumbnail(self, key: str) -> None:
        """Load and display thumbnail for the given image key."""
        if not self.show_thumbnails:
            return
        
        label = self.thumbnail_labels.get(key)
        if not label:
            return
        
        img_path = self.vars[key].get().strip()
        if not img_path:
            label.config(image="")
            return
        
        path = pathlib.Path(img_path).expanduser()
        if not path.exists():
            label.config(image="")
            return
        
        try:
            # Load and resize image to fit in thumbnail area
            img = Image.open(path)
            img.thumbnail((120, 80), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img, master=self.root)
            
            # Store reference directly on label to prevent garbage collection
            label._photo_ref = photo
            
            # Display image on label
            label.config(image=photo)
        except Exception:
            # If image fails to load, clear it
            label.config(image="")

    def _add_simple(
        self,
        parent: ttk.Frame,
        row: int,
        label: str,
        key: str,
        browse_command=None,
        browse_text: str = "Browse",
    ) -> None:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", padx=(0, 8), pady=3)
        var = tk.StringVar(value=self.values[key])
        self.vars[key] = var
        ttk.Entry(parent, textvariable=var, width=42).grid(row=row, column=1, columnspan=3, sticky="w", pady=3)
        if browse_command is not None:
            ttk.Button(parent, text=browse_text, command=browse_command).grid(
                row=row, column=4, sticky="w", padx=(6, 0)
            )

    def pick_directory(self, key: str) -> None:
        current = self.vars[key].get().strip()
        initial_dir = current if current else str(pathlib.Path.home())
        selected = filedialog.askdirectory(
            title="Select wallpaper folder",
            initialdir=initial_dir,
            mustexist=True,
        )
        if selected:
            self.vars[key].set(selected)

    def pick_file(self, key: str) -> None:
        current = self.vars[key].get().strip()
        initial_dir = str(pathlib.Path(current).parent) if current else self.vars["WALLDIR"].get().strip()
        selected = filedialog.askopenfilename(
            title="Select wallpaper image",
            initialdir=initial_dir,
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.webp *.bmp"), ("All files", "*.*")],
        )
        if selected:
            self.vars[key].set(selected)

    def _collect(self) -> dict[str, str]:
        data = {k: v.get().strip() for k, v in self.vars.items()}

        for key in ["WALLDIR", "CITY_NAME", "REGION", "TIMEZONE", "LATITUDE", "LONGITUDE"]:
            if not data[key]:
                raise ValueError(f"{key} cannot be empty")

        try:
            float(data["LATITUDE"])
            float(data["LONGITUDE"])
        except ValueError as exc:
            raise ValueError("Latitude and Longitude must be numbers") from exc

        try:
            ZoneInfo(data["TIMEZONE"])
        except Exception as exc:
            raise ValueError("Timezone is invalid") from exc

        for i in range(1, 7):
            img = data[f"IMAGE_{i}"]
            if not img:
                raise ValueError(f"IMAGE_{i} cannot be empty")
            if data[f"RULE_{i}"] not in RULES:
                raise ValueError(f"RULE_{i} must be one of: {', '.join(RULES)}")

            try:
                int(data[f"OFFSET_MIN_{i}"])
            except ValueError as exc:
                raise ValueError(f"OFFSET_MIN_{i} must be an integer") from exc

            clock = data[f"CLOCK_TIME_{i}"]
            if ":" not in clock:
                raise ValueError(f"CLOCK_TIME_{i} must be HH:MM")
            hh, mm = clock.split(":", 1)
            if not (hh.isdigit() and mm.isdigit() and 0 <= int(hh) <= 23 and 0 <= int(mm) <= 59):
                raise ValueError(f"CLOCK_TIME_{i} must be valid HH:MM")

        return data

    def _run(self, cmd: list[str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(cmd, check=False, capture_output=True, text=True)

    def save(self) -> None:
        try:
            data = self._collect()
            write_config(CONFIG_PATH, data)
        except Exception as exc:
            messagebox.showerror("Save Failed", str(exc))
            return
        messagebox.showinfo("Saved", f"Saved settings to\n{CONFIG_PATH}")

    def install_timer(self) -> None:
        try:
            data = self._collect()
            write_config(CONFIG_PATH, data)
        except Exception as exc:
            messagebox.showerror("Install Failed", str(exc))
            return

        SERVICE_PATH.parent.mkdir(parents=True, exist_ok=True)
        SERVICE_PATH.write_text(SERVICE_TEXT, encoding="utf-8")
        TIMER_PATH.write_text(TIMER_TEXT, encoding="utf-8")

        cmds: list[list[str]] = [
            ["systemctl", "--user", "daemon-reload"],
            ["systemctl", "--user", "enable", "--now", "daycycle-wallpaper.timer"],
        ]
        if self.remove_cron.get():
            cmds.append([
                "bash",
                "-lc",
                f"{{ crontab -l 2>/dev/null || true; }} | grep -v '{SCRIPT_PATH}' | crontab -",
            ])

        failures = []
        for cmd in cmds:
            result = self._run(cmd)
            if result.returncode != 0:
                failures.append((cmd, result.stderr.strip()))

        if failures:
            msg = "\n\n".join(f"$ {' '.join(c)}\n{e}" for c, e in failures)
            messagebox.showerror("Install Failed", msg)
            return

        messagebox.showinfo("Installed", "Timer is enabled and will run every 15 minutes.")

    def run_now(self) -> None:
        try:
            data = self._collect()
            write_config(CONFIG_PATH, data)
        except Exception as exc:
            messagebox.showerror("Run Failed", str(exc))
            return

        result = self._run([str(SCRIPT_PATH)])
        if result.returncode == 0:
            messagebox.showinfo("Success", "Wallpaper updated successfully.")
            return

        output = (result.stdout + "\n" + result.stderr).strip()
        messagebox.showerror("Run Failed", output or "Unknown error")


def main() -> None:
    if TkinterDnD is not None:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
