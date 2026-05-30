import time
from tkinter import *
from tkinter import ttk


class AdvancedClockApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Time Hub")
        self.root.geometry("650x450")
        self.root.resizable(False, False)

        # Application Configurations & States
        self.is_24_hour = False
        self.current_theme = "cyan"

        # Stopwatch State Variables
        self.stopwatch_running = False
        self.stopwatch_start_time = 0.0
        self.stopwatch_elapsed_time = 0.0

        # Time Zone Offsets (relative to GMT/UTC in hours)
        self.timezones = {
            "Local Time": None,
            "GMT / UTC": 0,
            "New York (EST/EDT)": -4,  # Approximate Daylight/Standard mix
            "London (BST/GMT)": 1,
            "Mumbai (IST)": 5.5,
            "Tokyo (JST)": 9,
        }

        # Color Themes Dictionary
        self.themes = {
            "red": {"bg": "#110000", "fg": "#ff3333", "btn": "#330000"},
            "cyan": {"bg": "#001111", "fg": "#00ffff", "btn": "#003333"},
            "dark": {"bg": "#1e1e1e", "fg": "#ffffff", "btn": "#444444"},
        }

        # Main Setup
        self.root.configure(background=self.themes[self.current_theme]["bg"])
        self.create_widgets()
        self.update_clock()

    def create_widgets(self):
        colors = self.themes[self.current_theme]

        # --- Top Options Panel ---
        self.control_frame = Frame(self.root, bg=colors["bg"])
        self.control_frame.pack(fill=X, padx=10, pady=10)

        # Format Toggle Button
        self.format_btn = Button(
            self.control_frame,
            text="Switch to 24H",
            font=("Arial", 10, "bold"),
            bg=colors["btn"],
            fg=colors["fg"],
            command=self.toggle_format,
            relief=FLAT,
        )
        self.format_btn.pack(side=LEFT, padx=5)

        # Theme Selector Button
        self.theme_btn = Button(
            self.control_frame,
            text="Change Theme",
            font=("Arial", 10, "bold"),
            bg=colors["btn"],
            fg=colors["fg"],
            command=self.rotate_theme,
            relief=FLAT,
        )
        self.theme_btn.pack(side=LEFT, padx=5)

        # Timezone Label & Dropdown Combo
        self.tz_label = Label(
            self.control_frame,
            text="Zone:",
            font=("Arial", 10, "bold"),
            bg=colors["bg"],
            fg=colors["fg"],
        )
        self.tz_label.pack(side=LEFT, padx=(15, 5))

        self.tz_selection = StringVar()
        self.tz_dropdown = ttk.Combobox(
            self.control_frame,
            textvariable=self.tz_selection,
            state="readonly",
            width=18,
        )
        self.tz_dropdown["values"] = list(self.timezones.keys())
        self.tz_dropdown.current(0)  # Default to Local Time
        self.tz_dropdown.pack(side=LEFT, padx=5)

        # --- Display Panel ---
        # Date Display Label
        self.date_label = Label(
            self.root,
            font=("Arial", 18, "bold"),
            bg=colors["bg"],
            fg=colors["fg"],
        )
        self.date_label.pack(pady=(15, 0))

        # Main Time Digit Display Label
        self.digi_clock = Label(
            self.root, font=("Courier", 65, "bold"), bg=colors["bg"], fg=colors["fg"]
        )
        self.digi_clock.pack(pady=10)

        # Divider Line
        self.divider = Frame(self.root, height=2, bd=0, bg=colors["btn"])
        self.divider.pack(fill=X, padx=30, pady=10)

        # --- Bottom Panel: Stopwatch ---
        self.sw_title = Label(
            self.root,
            text="STOPWATCH",
            font=("Arial", 12, "bold"),
            bg=colors["bg"],
            fg=colors["fg"],
        )
        self.sw_title.pack()

        self.sw_display = Label(
            self.root,
            text="00:00:00.00",
            font=("Courier", 28, "bold"),
            bg=colors["bg"],
            fg=colors["fg"],
        )
        self.sw_display.pack(pady=5)

        self.sw_btn_frame = Frame(self.root, bg=colors["bg"])
        self.sw_btn_frame.pack(pady=5)

        self.start_sw_btn = Button(
            self.sw_btn_frame,
            text="Start",
            font=("Arial", 10, "bold"),
            width=8,
            bg=colors["btn"],
            fg=colors["fg"],
            command=self.start_stopwatch,
        )
        self.start_sw_btn.pack(side=LEFT, padx=5)

        self.pause_sw_btn = Button(
            self.sw_btn_frame,
            text="Pause",
            font=("Arial", 10, "bold"),
            width=8,
            bg=colors["btn"],
            fg=colors["fg"],
            command=self.pause_stopwatch,
        )
        self.pause_sw_btn.pack(side=LEFT, padx=5)

        self.reset_sw_btn = Button(
            self.sw_btn_frame,
            text="Reset",
            font=("Arial", 10, "bold"),
            width=8,
            bg=colors["btn"],
            fg=colors["fg"],
            command=self.reset_stopwatch,
        )
        self.reset_sw_btn.pack(side=LEFT, padx=5)

    def update_clock(self):
        """Continuously pulls system or timezone accurate strings."""
        selected_zone = self.tz_selection.get()
        offset = self.timezones[selected_zone]

        if offset is None:
            # Use Local System Settings
            current_struct = time.localtime()
        else:
            # Shift system time directly to UTC target window
            utc_timestamp = time.time() + (time.timezone if time.daylight == 0 else time.altzone)
            target_timestamp = utc_timestamp + (offset * 3600)
            current_struct = time.gmtime(target_timestamp)

        # Generate custom formatting configurations
        time_mask = "%H:%M:%S" if self.is_24_hour else "%I:%M:%S %p"
        date_mask = "%A, %B %d, %Y"

        display_time = time.strftime(time_mask, current_struct)
        display_date = time.strftime(date_mask, current_struct)

        # Write text variations to Tkinter UI elements
        self.digi_clock.config(text=display_time)
        self.date_label.config(text=display_date.upper())

        # Recurse background checks safely every 200ms
        self.root.after(200, self.update_clock)

    def toggle_format(self):
        self.is_24_hour = not self.is_24_hour
        self.format_btn.config(
            text="Switch to 12H" if self.is_24_hour else "Switch to 24H"
        )

    def rotate_theme(self):
        theme_order = ["cyan", "red", "dark"]
        next_index = (theme_order.index(self.current_theme) + 1) % len(
            theme_order
        )
        self.current_theme = theme_order[next_index]
        colors = self.themes[self.current_theme]

        # Repaint UI Background components
        self.root.configure(background=colors["bg"])
        self.control_frame.configure(background=colors["bg"])
        self.sw_btn_frame.configure(background=colors["bg"])

        # Repaint Interactive Widgets
        widget_list = [
            self.format_btn,
            self.theme_btn,
            self.start_sw_btn,
            self.pause_sw_btn,
            self.reset_sw_btn,
        ]
        for btn in widget_list:
            btn.config(bg=colors["btn"], fg=colors["fg"])

        # Repaint Static Labels
        self.tz_label.config(bg=colors["bg"], fg=colors["fg"])
        self.date_label.config(bg=colors["bg"], fg=colors["fg"])
        self.digi_clock.config(bg=colors["bg"], fg=colors["fg"])
        self.sw_title.config(bg=colors["bg"], fg=colors["fg"])
        self.sw_display.config(bg=colors["bg"], fg=colors["fg"])
        self.divider.config(bg=colors["btn"])

    # --- Stopwatch Sub-Systems ---
    def start_stopwatch(self):
        if not self.stopwatch_running:
            self.stopwatch_running = True
            self.stopwatch_start_time = time.time() - self.stopwatch_elapsed_time
            self.update_stopwatch()

    def pause_stopwatch(self):
        if self.stopwatch_running:
            self.stopwatch_running = False
            self.stopwatch_elapsed_time = (
                time.time() - self.stopwatch_start_time
            )

    def reset_stopwatch(self):
        self.stopwatch_running = False
        self.stopwatch_elapsed_time = 0.0
        self.sw_display.config(text="00:00:00.00")

    def update_stopwatch(self):
        if self.stopwatch_running:
            current_elapsed = time.time() - self.stopwatch_start_time

            # Math calculations for base periods
            hours = int(current_elapsed // 3600)
            minutes = int((current_elapsed % 3600) // 60)
            seconds = int(current_elapsed % 60)
            centiseconds = int((current_elapsed % 1) * 100)

            time_string = f"{hours:02d}:{minutes:02d}:{seconds:02d}.{centiseconds:02d}"
            self.sw_display.config(text=time_string)

            # High refresh rate for stopwatch decimals (every 30ms)
            self.root.after(30, self.update_stopwatch)


if __name__ == "__main__":
    window = Tk()
    app = AdvancedClockApp(window)
    window.mainloop()