import customtkinter as ctk
from automation import run_automation
import threading

# ==========================================
# App Settings
# ==========================================

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Kassenbuch Automation")
app.geometry("700x650")
app.resizable(False, False)

# ==========================================
# Header
# ==========================================

header = ctk.CTkFrame(app, fg_color="transparent")
header.pack(fill="x", pady=20)

title = ctk.CTkLabel(
    header,
    text="Kassenbuch Automation",
    font=("Segoe UI", 28, "bold")
)
title.pack()

subtitle = ctk.CTkLabel(
    header,
    text="Restaurant Financial Report Generator",
    font=("Segoe UI", 15)
)
subtitle.pack()

version = ctk.CTkLabel(
    header,
    text="Version 1.1",
    font=("Segoe UI", 12)
)
version.pack()

# ==========================================
# Month Selection
# ==========================================

month_frame = ctk.CTkFrame(app)
month_frame.pack(fill="x", padx=20, pady=10)

ctk.CTkLabel(
    month_frame,
    text="Select Month",
    font=("Segoe UI", 16, "bold")
).pack(pady=(10, 5))

months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

month_menu = ctk.CTkOptionMenu(
    month_frame,
    values=months,
    width=220
)
month_menu.pack(pady=(0, 10))

month_menu.set("January")

# ==========================================
# Status
# ==========================================

status_frame = ctk.CTkFrame(app)
status_frame.pack(fill="x", padx=20, pady=10)

ctk.CTkLabel(
    status_frame,
    text="Automation Status",
    font=("Segoe UI", 16, "bold")
).pack(pady=10)

steps = [
    "POS Export",
    "NEXI Export",
    "Lieferando Bank",
    "Lieferando Cash",
    "Lieferando Tips",
    "Uber Export",
    "Generate Kassenbuch"
]

status_labels = {}

for step in steps:
    label = ctk.CTkLabel(
        status_frame,
        text=f"⚪ {step}",
        anchor="w"
    )
    label.pack(fill="x", padx=20)
    status_labels[step] = label

# ==========================================
# Progress
# ==========================================

progress_frame = ctk.CTkFrame(app)
progress_frame.pack(fill="x", padx=20, pady=10)

ctk.CTkLabel(
    progress_frame,
    text="Progress",
    font=("Segoe UI", 16, "bold")
).pack(pady=(10, 5))

progress = ctk.CTkProgressBar(progress_frame)
progress.pack(fill="x", padx=20)

progress.set(0)

# ==========================================
# Footer
# ==========================================

status = ctk.CTkLabel(
    app,
    text="Status: Ready"
)
status.pack(pady=10)

# ==========================================
# Functions
# ==========================================

def update_progress(value):
    app.after(0, lambda: progress.set(value))


def update_status(step):

    def gui_update():

        status.configure(text=f"Status: Running {step}...")

        for name, label in status_labels.items():

            current = label.cget("text")

            if name == step:
                label.configure(text=f"🟡 {name}")

            elif current.startswith("🟡"):
                label.configure(text=f"🟢 {name}")

    app.after(0, gui_update)


def start_automation():

    # Reset progress
    app.after(0, lambda: progress.set(0))

    # Reset status indicators
    for name, label in status_labels.items():
        app.after(
            0,
            lambda l=label, n=name: l.configure(text=f"⚪ {n}")
        )

    start_btn.configure(state="disabled")

    selected_month = month_menu.get()

    def worker():

        try:

            run_automation(
                selected_month,
                progress_callback=update_progress,
                status_callback=update_status
            )

            app.after(
                0,
                lambda: status.configure(
                    text="✅ Automation Completed Successfully!"
                )
            )

        except Exception as e:

            app.after(
                0,
                lambda: status.configure(
                    text=f"❌ {e}"
                )
            )

        finally:

            app.after(
                0,
                lambda: start_btn.configure(state="normal")
            )

    threading.Thread(target=worker, daemon=True).start()


# ==========================================
# Button
# ==========================================

start_btn = ctk.CTkButton(
    app,
    text="Start Automation",
    width=300,
    height=45,
    font=("Segoe UI", 16, "bold"),
    command=start_automation
)

start_btn.pack(pady=(15, 10))

# ==========================================
# Start GUI
# ==========================================

app.mainloop()