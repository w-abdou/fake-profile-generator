import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from faker import Faker
import json
import csv
from decimal import Decimal
from datetime import date
import pyperclip

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        elif isinstance(o, date):
            return o.isoformat()
        return super().default(o)

def generate_fake_profile(selected_fields, fake_instance):
    profile = fake_instance.profile()
    return {field: profile[field] for field in selected_fields if field in profile}

def save_profiles_as_json(profiles, file_path):
    with open(file_path, 'w') as f:
        json.dump(profiles, f, indent=4, cls=CustomJSONEncoder)

def save_profiles_as_csv(profiles, file_path):
    with open(file_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=profiles[0].keys())
        writer.writeheader()
        writer.writerows(profiles)

def generate_and_save():
    try:
        num = int(entry_number.get())
        if num <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid positive number.")
        return

    selected_fields = [field for field, var in field_vars.items() if var.get()]
    if not selected_fields:
        messagebox.showwarning("No Fields Selected", "Please select at least one field to include.")
        return

    local_fake = Faker()
    Faker.seed(0)
    local_fake.seed_instance(0)

    profiles = [generate_fake_profile(selected_fields, local_fake) for _ in range(num)]
    preview_text.delete("1.0", tk.END)
    for i, profile in enumerate(profiles, start=1):
        preview_text.insert(tk.END, f"🧑 Profile {i}:\n", "bold")
        for key, value in profile.items():
            preview_text.insert(tk.END, f"• {key.capitalize()}: {value}\n")
        preview_text.insert(tk.END, "\n")

    filetype = file_format.get()
    ext = 'json' if filetype == 'json' else 'csv'
    filetypes = [('JSON files', '*.json')] if ext == 'json' else [('CSV files', '*.csv')]

    file_path = filedialog.asksaveasfilename(defaultextension=f".{ext}", filetypes=filetypes)
    if not file_path:
        return

    try:
        if ext == 'json':
            save_profiles_as_json(profiles, file_path)
        else:
            save_profiles_as_csv(profiles, file_path)
        messagebox.showinfo("Success", f"Saved {num} profiles to {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save file:\n{e}")

def copy_to_clipboard():
    content = preview_text.get("1.0", tk.END)
    pyperclip.copy(content)
    messagebox.showinfo("Copied", "Preview content copied to clipboard.")

def search_profiles():
    preview_text.tag_remove("highlight", "1.0", tk.END)
    keyword = search_entry.get().strip()
    if keyword:
        idx = "1.0"
        while True:
            idx = preview_text.search(keyword, idx, nocase=1, stopindex=tk.END)
            if not idx:
                break
            end_idx = f"{idx}+{len(keyword)}c"
            preview_text.tag_add("highlight", idx, end_idx)
            idx = end_idx
        preview_text.tag_config("highlight", background="yellow", foreground="black")

def toggle_dark_mode():
    is_dark = dark_mode_var.get()
    bg, fg = ("#2E2E2E", "#FAFAFA") if is_dark else ("#FFFFFF", "black")
    preview_text.configure(bg=bg, fg=fg, insertbackground=fg)
    root.configure(bg=bg)
    for widget in root.winfo_children():
        try:
            widget.configure(bg=bg, fg=fg)
        except:
            pass

def update_statistics():
    text = preview_text.get("1.0", tk.END)
    total = text.count("Profile")
    males = text.count(" M")
    females = text.count(" F")
    stats_label.config(text=f"📊 Total: {total} | 👨 Males: {males} | 👩 Females: {females}")

# Initialize root
root = tk.Tk()
root.title("Fake Profile Generator")
root.geometry("950x780")
root.configure(bg="#FFFFFF")

style = ttk.Style()
style.theme_use('clam')

# Top frame
frame_top = tk.Frame(root, bg="#FFFFFF")
frame_top.pack(pady=10)

tk.Label(frame_top, text="👥 Number of Profiles:", bg="#FFFFFF", fg="black", font=("Arial", 11)).grid(row=0, column=0, padx=5)
entry_number = tk.Entry(frame_top, width=8)
entry_number.grid(row=0, column=1, padx=5)

file_format = tk.StringVar(value='json')
tk.Radiobutton(frame_top, text="💾 JSON", variable=file_format, value='json', bg="#FFFFFF", fg="black").grid(row=0, column=2)
tk.Radiobutton(frame_top, text="📄 CSV", variable=file_format, value='csv', bg="#FFFFFF", fg="black").grid(row=0, column=3)

# Field selection
field_frame = tk.LabelFrame(root, text="🛠 Select Fields", padx=10, pady=5, bg="#FFFFFF", fg="black", font=("Arial", 10, "bold"))
field_frame.pack(pady=10, fill='x')

all_fields = ["name", "username", "sex", "address", "mail", "birthdate", "job", "company"]
field_vars = {field: tk.BooleanVar(value=True) for field in all_fields}
for i, field in enumerate(all_fields):
    tk.Checkbutton(field_frame, text=field.capitalize(), variable=field_vars[field], bg="#FFFFFF", fg="black").grid(row=i//4, column=i%4, sticky='w', padx=10, pady=3)

# Buttons
button_frame = tk.Frame(root, bg="#FFFFFF")
button_frame.pack(pady=10)

tk.Button(button_frame, text="🚀 Generate & Save", command=generate_and_save, bg="#4CAF50", fg="black", width=18).grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="📋 Copy Preview", command=copy_to_clipboard, bg="#2196F3", fg="black", width=18).grid(row=0, column=1, padx=10)

dark_mode_var = tk.BooleanVar()
tk.Checkbutton(button_frame, text="🌙 Dark Mode", variable=dark_mode_var, command=toggle_dark_mode, bg="#FFFFFF", fg="black").grid(row=0, column=2, padx=10)

# Preview text area
tk.Label(root, text="📝 Preview (editable):", bg="#FFFFFF", fg="black", font=("Arial", 10, "bold")).pack()
preview_text = tk.Text(root, height=20, wrap=tk.WORD, font=("Consolas", 10), bg="white", fg="black")
preview_text.tag_configure("bold", font=("Consolas", 10, "bold"))
preview_text.pack(fill='both', padx=20, pady=5, expand=True)

# Bottom frame
bottom_frame = tk.Frame(root, bg="#FFFFFF")
bottom_frame.pack(pady=10)

tk.Label(bottom_frame, text="🔍 Search Preview:", bg="#FFFFFF", fg="black").grid(row=0, column=0, padx=5)
search_entry = tk.Entry(bottom_frame, width=20)
search_entry.grid(row=0, column=1, padx=5)
tk.Button(bottom_frame, text="Search", command=search_profiles, bg="#FFC107", fg="black").grid(row=0, column=2, padx=5)
tk.Button(bottom_frame, text="📊 Stats", command=update_statistics, bg="#FFC107", fg="black").grid(row=0, column=3, padx=5)

stats_label = tk.Label(bottom_frame, text="", bg="#FFFFFF", fg="black")
stats_label.grid(row=0, column=4, padx=10)

root.mainloop()
