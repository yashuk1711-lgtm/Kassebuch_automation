import customtkinter as ctk
from automation import run_automation
import config
import updater
from version import VERSION
import threading
import sys

# ==========================================
# App Settings
# ==========================================

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Kassenbuch Automation")
app.geometry("700x780")
app.minsize(700, 600)
app.resizable(False, True)

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

version_label = ctk.CTkLabel(
    header,
    text=f"Version {VERSION}",
    font=("Segoe UI", 12)
)
version_label.pack()

update_status_label = ctk.CTkLabel(
    header,
    text="",
    font=("Segoe UI", 12),
    text_color="#4caf50"
)
update_status_label.pack()

update_btn = ctk.CTkButton(
    header,
    text="Check for Updates",
    width=180,
    height=28,
    fg_color="#555555",
    command=lambda: check_for_updates()
)
update_btn.pack(pady=(5, 0))

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
# Starting Balance (only needed for the very
# first month, or if no previous month's
# Kassenbuch exists yet)
# ==========================================

balance_frame = ctk.CTkFrame(app)
balance_frame.pack(fill="x", padx=20, pady=10)

ctk.CTkLabel(
    balance_frame,
    text="Starting Balance (only needed if no previous month exists)",
    font=("Segoe UI", 13)
).pack(pady=(10, 5))

balance_entry = ctk.CTkEntry(
    balance_frame,
    placeholder_text="e.g. 42876.01",
    width=220
)
balance_entry.pack(pady=(0, 10))

# ==========================================
# Manual Expenses (Metro, lidl, rent, salary,
# private withdrawals, etc.) - entered by hand
# per month, saved to Data/Manual/
# ==========================================


def _normalize_expense_date(text):

    parts = [p for p in text.strip().split(".") if p]

    if len(parts) < 2:
        raise ValueError('Date must look like "05.02."')

    day, month = int(parts[0]), int(parts[1])

    return f"{day:02d}.{month:02d}."


def _manual_expenses_file(month_lower):
    return config.MANUAL_FOLDER / f"{month_lower}_manual_expenses.csv"


def _load_manual_expenses(month_lower):

    path = _manual_expenses_file(month_lower)

    if not path.exists():
        return []

    rows = []

    with open(path, "r", encoding="utf-8-sig") as f:

        for i, line in enumerate(f):

            if i == 0:
                continue  # header

            line = line.strip()

            if not line:
                continue

            date, description, amount = line.split(";")
            rows.append((date, description, amount))

    return rows


def _save_manual_expenses(month_lower, rows):

    config.MANUAL_FOLDER.mkdir(parents=True, exist_ok=True)

    path = _manual_expenses_file(month_lower)

    with open(path, "w", encoding="utf-8-sig") as f:

        f.write("date;description;amount\n")

        for date, description, amount in rows:
            f.write(f"{date};{description};{amount}\n")


def open_manual_expenses_window():

    month_lower = month_menu.get().lower()

    win = ctk.CTkToplevel(app)
    win.title(f"Manual Expenses - {month_menu.get()}")
    win.geometry("480x520")
    win.grab_set()

    expenses = _load_manual_expenses(month_lower)

    ctk.CTkLabel(
        win,
        text=f"Manual Expenses for {month_menu.get()}",
        font=("Segoe UI", 16, "bold")
    ).pack(pady=(15, 10))

    entry_frame = ctk.CTkFrame(win, fg_color="transparent")
    entry_frame.pack(fill="x", padx=20)

    date_entry = ctk.CTkEntry(entry_frame, placeholder_text="Date (05.02.)", width=110)
    date_entry.grid(row=0, column=0, padx=5, pady=5)

    desc_entry = ctk.CTkEntry(entry_frame, placeholder_text="Description (Metro)", width=180)
    desc_entry.grid(row=0, column=1, padx=5, pady=5)

    amount_entry = ctk.CTkEntry(entry_frame, placeholder_text="Amount (756,19)", width=110)
    amount_entry.grid(row=0, column=2, padx=5, pady=5)

    list_box = ctk.CTkTextbox(win, width=440, height=280)
    list_box.pack(padx=20, pady=10)

    error_label = ctk.CTkLabel(win, text="", text_color="#e05252")
    error_label.pack()

    def refresh_list():

        list_box.configure(state="normal")
        list_box.delete("1.0", "end")

        for date, description, amount in expenses:
            list_box.insert("end", f"{date}  {description}  {amount}\n")

        list_box.configure(state="disabled")

    def add_expense():

        error_label.configure(text="")

        try:
            date = _normalize_expense_date(date_entry.get())
        except ValueError:
            error_label.configure(text='Date must look like "05.02."')
            return

        description = desc_entry.get().strip()

        if not description:
            error_label.configure(text="Description is required.")
            return

        amount_text = amount_entry.get().strip()

        try:
            float(amount_text.replace(".", "").replace(",", "."))
        except ValueError:
            error_label.configure(text="Amount must be a number.")
            return

        expenses.append((date, description, amount_text))
        refresh_list()

        date_entry.delete(0, "end")
        desc_entry.delete(0, "end")
        amount_entry.delete(0, "end")
        date_entry.focus()

    def remove_last():

        if expenses:
            expenses.pop()
            refresh_list()

    def save_and_close():

        _save_manual_expenses(month_lower, expenses)
        win.destroy()

    button_frame = ctk.CTkFrame(win, fg_color="transparent")
    button_frame.pack(pady=(0, 10))

    ctk.CTkButton(
        button_frame, text="Add Expense", width=120, command=add_expense
    ).grid(row=0, column=0, padx=5)

    ctk.CTkButton(
        button_frame, text="Remove Last", width=120,
        fg_color="#555555", command=remove_last
    ).grid(row=0, column=1, padx=5)

    ctk.CTkButton(
        win, text="Save & Close", width=200, command=save_and_close
    ).pack(pady=(5, 15))

    refresh_list()


manual_expenses_btn = ctk.CTkButton(
    balance_frame,
    text="Manual Expenses...",
    width=220,
    fg_color="#555555",
    command=open_manual_expenses_window
)
manual_expenses_btn.pack(pady=(0, 10))

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

_pending_update = {}


def check_for_updates():

    update_btn.configure(state="disabled", text="Checking...")
    update_status_label.configure(text="", text_color="#4caf50")

    def worker():

        result = updater.check_for_update()

        def show_result():

            if result is None:
                update_status_label.configure(
                    text="You're up to date.", text_color="#4caf50"
                )
                update_btn.configure(state="normal", text="Check for Updates")

            elif "error" in result:
                update_status_label.configure(
                    text=f"Update check failed: {result['error']}",
                    text_color="#e05252"
                )
                update_btn.configure(state="normal", text="Check for Updates")

            else:
                _pending_update["download_url"] = result["download_url"]
                update_status_label.configure(
                    text=f"Update {result['version']} is available!",
                    text_color="#4caf50"
                )
                update_btn.configure(
                    state="normal",
                    text="Install Update",
                    command=confirm_install_update
                )

        app.after(0, show_result)

    threading.Thread(target=worker, daemon=True).start()


def confirm_install_update():

    dialog = ctk.CTkToplevel(app)
    dialog.title("Install Update")
    dialog.geometry("360x160")
    dialog.grab_set()

    ctk.CTkLabel(
        dialog,
        text="The app will close and restart\nto finish installing the update.",
        font=("Segoe UI", 13)
    ).pack(pady=(25, 15))

    button_row = ctk.CTkFrame(dialog, fg_color="transparent")
    button_row.pack()

    def do_install():

        dialog.destroy()
        updater.apply_update(_pending_update["download_url"])
        app.destroy()
        sys.exit(0)

    ctk.CTkButton(
        button_row, text="Install & Restart", width=140, command=do_install
    ).grid(row=0, column=0, padx=8)

    ctk.CTkButton(
        button_row, text="Cancel", width=100, fg_color="#555555",
        command=dialog.destroy
    ).grid(row=0, column=1, padx=8)


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

    # Reset step indicators
    for name, label in status_labels.items():
        app.after(
            0,
            lambda l=label, n=name: l.configure(text=f"⚪ {n}")
        )

    selected_month = month_menu.get()
    balance_text = balance_entry.get().strip()

    manual_balance = None

    if balance_text:

        try:
            manual_balance = float(balance_text.replace(",", "."))
        except ValueError:
            status.configure(text="❌ Starting balance must be a number.")
            return

    start_btn.configure(state="disabled")

    def worker():

        try:

            run_automation(
                selected_month,
                manual_balance,
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

            error_message = str(e)

            app.after(
                0,
                lambda: status.configure(
                    text=f"❌ {error_message}"
                )
            )

        finally:

            app.after(
                0,
                lambda: start_btn.configure(state="normal")
            )

    threading.Thread(
        target=worker,
        daemon=True
    ).start()


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