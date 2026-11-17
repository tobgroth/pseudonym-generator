import hashlib
import getpass
from datetime import datetime
import tkinter as tk
import re
from tkinter import ttk, messagebox, simpledialog
from hashlib import pbkdf2_hmac


def validate_input(last_name, first_name, dob, place_of_birth):
    """Validate all input fields"""
    errors = []

    # Validate last name
    if not last_name.strip():
        errors.append("❌ Last name is required.")
    elif not all(c.isalpha() or c.isspace() for c in last_name):
        errors.append("❌ Last name must contain only letters and spaces.")

    # Validate first name
    if not first_name.strip():
        errors.append("❌ First name is required.")
    elif not all(c.isalpha() or c.isspace() for c in first_name):
        errors.append("❌ First name must contain only letters and spaces.")

    # Validate DOB
    if not dob.strip():
        errors.append("❌ Date of birth is required.")
    else:
        # Try both formats
        if '-' in dob:
            parts = dob.split('-')
            if len(parts) != 3:
                errors.append("❌ Invalid date format. Use YYYY-MM-DD.")
            else:
                y, m, d = parts
                if not (y.isdigit() and m.isdigit() and d.isdigit()):
                    errors.append("❌ Date must contain only numbers.")
                elif len(y) != 4 or len(m) != 2 or len(d) != 2:
                    errors.append("❌ Invalid date format. Use YYYY-MM-DD.")
                elif int(m) < 1 or int(m) > 12:
                    errors.append("❌ Month must be 01–12.")
                elif int(d) < 1 or int(d) > 31:
                    errors.append("❌ Day must be 01–31.")
        elif '/' in dob:
            parts = dob.split('/')
            if len(parts) != 3:
                errors.append("❌ Invalid date format. Use YYYY-MM-DD.")
            else:
                d, m, y = parts
                if not (y.isdigit() and m.isdigit() and d.isdigit()):
                    errors.append("❌ Date must contain only numbers.")
                elif len(y) != 4 or len(m) != 2 or len(d) != 2:
                    errors.append("❌ Invalid date format. Use YYYY-MM-DD.")
                elif int(m) < 1 or int(m) > 12:
                    errors.append("❌ Month must be 01–12.")
                elif int(d) < 1 or int(d) > 31:
                    errors.append("❌ Day must be 01–31.")
        else:
            errors.append("❌ Invalid date format. Use YYYY-MM-DD.")

    # Validate place of birth
    if not place_of_birth.strip():
        errors.append("❌ Place of birth is required.")
    elif not all(c.isalpha() or c.isspace() for c in place_of_birth):
        errors.append("❌ Place of birth must contain only letters and spaces.")

    return errors

def generate_verification_code(password):
    """Generate a short 8-char code from password for verification"""
    salt_key = pbkdf2_hmac('sha256', password.encode(), b'verify_salt', 100000)
    combined = password.encode() + salt_key
    hash_obj = hashlib.sha256(combined)
    raw_hash = hash_obj.hexdigest()[:8].upper()
    mapping = {'0': '#', 'O': '+'}
    safe = ''.join(mapping.get(c, c) for c in raw_hash)
    return f"{safe[:4]}-{safe[4:]}"

def generate_base_code(first_name, last_name, place_of_birth, dob):
    """Generate 8-digit base code: HSPR2130"""
    if '-' in dob:
        y, m, d = dob.split('-')
    elif '/' in dob:
        d, m, y = dob.split('/')
    else:
        raise ValueError("Invalid DOB format")
    dob_clean = f"{y}{m}{d}"

    digit_sum = sum(int(c) for c in dob_clean if c.isdigit()) + len(place_of_birth) * 2
    letter_sum = len(first_name) + len(last_name) + int(m) * 2

    try:
        f1 = first_name[0].upper()
        f2 = first_name[-1].upper()
        l1 = last_name[1].upper()
        c1 = place_of_birth[0].upper()
    except IndexError:
        raise ValueError("Name or city too short. Write city/name twice into the field.")

    base = f1 + l1 + str(digit_sum).rjust(2,'0')[:2] + f2 + c1 + str(letter_sum).rjust(2,'0')[:2]
    return base

def format_final_pseudonym(raw_hash):
    """Replace 0 → #, O → +, then format as ABCD-EFGH"""
    mapping = {'0': '#', 'O': '+'}
    safe = ''.join(mapping.get(c, c) for c in raw_hash)
    return f"{safe[:4]}-{safe[4:]}"

def generate_pseudonym_from_base(base_code, label, password):
    """Generate 8-char pseudonym from base + label + password"""
    combined = base_code + label + password
    salt_key = pbkdf2_hmac('sha256', password.encode(), b'salt_for_pseudonym_tool', 100000)
    combined_bytes = combined.encode() + salt_key
    hash_obj = hashlib.sha256(combined_bytes)
    raw_hash = hash_obj.hexdigest()[:8].upper()
    return format_final_pseudonym(raw_hash)

def main_gui(tool_version):
    root = tk.Tk()
    root.title("🔐 " + tool_version)
    root.minsize(900, 600)
    root.resizable(True, True)

    # === Title ===
    #title = tk.Label(root, text=tool_version, font=("Arial", 16, "bold"))
    #title.pack(pady=10)

    # === Main Frame: Two Columns ===
    main_frame = ttk.Frame(root)
    main_frame.pack(pady=10, padx=20, fill="both", expand=True)

    # Configure columns to grow equally
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)
    main_frame.rowconfigure(0, weight=1)

    # === Left Column: Input & Controls ===
    left_frame = ttk.LabelFrame(main_frame, text="Input & Settings", padding=10)
    left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0)


    # === Mode Selection (Inside left_frame) ===
    mode_var = tk.StringVar(value="input")  # default: input mode

    # === Input Mode Fields ===
    input_frame = ttk.LabelFrame(left_frame, text="Raw Input", padding=10)
    input_frame.grid()
    ttk.Radiobutton(input_frame, text="1. Input Mode (Name, DOB, Place)", variable=mode_var, value="input").grid(row=0, column=0, sticky="w", padx=10, pady=5)

    input_fields = [
        ("(First) First Name", "first_name"),
        ("(Last) Last Name", "last_name"),
        ("Date of Birth YYYY-MM-DD", "dob"),
        ("Place of Birth", "place_of_birth")
    ]

    entries_input = {}
    for i, (label_text, key) in enumerate(input_fields):
        label = ttk.Label(input_frame, text=label_text, width=25)
        label.grid(row=i+2, column=0, sticky="w", padx=5, pady=5)  # Start at row 2
        entry = ttk.Entry(input_frame, width=40)
        entry.grid(row=i+2, column=1, sticky="ew", padx=5, pady=5)
        entries_input[key] = entry

    # === Base Code Mode Fields ===
    base_frame = ttk.LabelFrame(left_frame, text="Basecode Input", padding=10)
    base_frame.grid()
    ttk.Radiobutton(base_frame, text="2. Base Code Mode", variable=mode_var, value="base").grid(row=1, column=0, sticky="w", padx=10, pady=5)

    base_label = ttk.Label(base_frame, text="Enter Base Code:", width=35)
    base_entry = ttk.Entry(base_frame, width=40)

    # Place base code fields below input fields
    base_label.grid(row=6, column=0, sticky="w", padx=5, pady=5)
    base_entry.grid(row=6, column=1, sticky="ew", padx=5, pady=5)

    # === Tag Selection ===
    ttk.Label(left_frame, text="Pseudonym Tags (select one or more):").grid(row=7, column=0, sticky="w", pady=(10, 0), padx=10)
    tags = ["_default", "_genetic", "_epigen", "_biosample", "_backup1", "_backup2", "_backup3", "_backup4"]
    tag_vars = {}
    tag_frame = ttk.Frame(left_frame)
    tag_frame.grid(row=8, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))
    for i, tag in enumerate(tags):
        if "backup" in tag:
            var = tk.BooleanVar(value=False)
        else:
            var = tk.BooleanVar(value=True)
        cb = ttk.Checkbutton(tag_frame, text=tag, variable=var)
        cb.grid(row=i//4, column=i%4, sticky="w", padx=5, pady=2)
        tag_vars[tag] = var

    # === Password & Verification ===
    ttk.Label(left_frame, text="Study Password:").grid(row=9, column=0, sticky="w", pady=(10, 0), padx=10)
    password_entry = ttk.Entry(left_frame, width=30, show="*")
    password_entry.grid(row=10, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

    ttk.Label(left_frame, text="Expected Verification Code:").grid(row=11, column=0, sticky="w", pady=(10, 0), padx=10)
    expected_code_entry = ttk.Entry(left_frame, width=30)
    expected_code_entry.grid(row=12, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

    # === Right Column: Output & Buttons ===
    right_frame = ttk.LabelFrame(main_frame, text="Output & Actions", padding=10)
    right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=0)

    # === Output ===
    output_frame = ttk.LabelFrame(right_frame, text="Generated Pseudonym(s)")
    output_frame.pack(fill="both", expand=True, pady=(0, 10))

    output_text = tk.Text(output_frame, height=10, width=50, font=("Courier", 11), wrap="none")
    output_text.pack(pady=5, padx=5, fill="both", expand=True)


    # === Buttons ===
    button_frame = ttk.Frame(right_frame)
    button_frame.pack(fill="x", pady=(5, 0))

    def copy_to_clipboard():
        root.clipboard_clear()
        OUTPUT = output_text.get("1.0", "end-1c")
        OUTPUT = OUTPUT.replace("\n", "\t")
        root.clipboard_append(OUTPUT)
        messagebox.showinfo("Copied", "Pseudonym(s) copied to clipboard!")

    copy_btn = ttk.Button(button_frame, text="📋 Copy to Clipboard", command=copy_to_clipboard)
    copy_btn.pack(side="left", padx=(0, 5))

    def generate():
        mode = mode_var.get()

        if mode == "input":
            last_name = entries_input["last_name"].get().strip()
            first_name = entries_input["first_name"].get().strip()
            dob = entries_input["dob"].get().strip()
            place_of_birth = entries_input["place_of_birth"].get().strip()
            
            errors = validate_input(last_name, first_name, dob, place_of_birth)
            if errors:
                messagebox.showwarning("Input Error", "\n".join(errors))
                return

            try:
                base_code = generate_base_code(first_name, last_name, place_of_birth, dob)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate base code: {e}")
                return

        elif mode == "base":
            base_code = base_entry.get().strip()            
            if not base_code:
                messagebox.showerror("Missing Data", "Please enter a base code.")
                return

            if not re.match(r"^[A-Z0-9]{8}$", base_code):
                messagebox.showerror("Invalid Base Code", "Base code must be 8 alphanumeric characters.")
                return

        # Get selected tags
        selected_tags = [tag for tag, var in tag_vars.items() if var.get()]
        if not selected_tags:
            messagebox.showerror("No Tag", "Please select at least one pseudonym tag.")
            return

        # Verify password and verification code
        password = password_entry.get().strip()

        if not password.strip():
            messagebox.showerror("No Password", "❌ Password is required.")
            return
        elif len(password) < 6:
            messagebox.showerror("Short Password", "❌ Password must be at least 6 characters long.")
            return
        
        expected_code = expected_code_entry.get().strip()
        actual_code = generate_verification_code(password)

        if not expected_code.strip():
            messagebox.showerror("No Verification Code", "❌ Verification Code is required.")
            return

        if expected_code and actual_code != expected_code:
            messagebox.showerror("Verification Failed", f"❌ The verification code does not match with the entered password. This indicates a mistake/typo in either the password or the verification code. Both need to be correct to generate reproducible pseudonyms.\n\nExpected: {expected_code}\nActual: {actual_code}")
            return

        # Generate pseudonyms
        try:
            results = []
            for tag in selected_tags:
                pseudonym = generate_pseudonym_from_base(base_code, tag, password)
                results.append(f"{pseudonym}{tag}")

            output_text.delete("1.0", "end")
            output_text.insert("1.0", f"{base_code}\n")
            output_text.insert("end", "\n".join(results))
            output_text.insert("end", f"\n{actual_code}_verification")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate: {e}")

    generate_btn = ttk.Button(button_frame, text="🚀 Generate Pseudonym(s)", command=generate)
    generate_btn.pack(side="right")

    # Optional: Add scrollbar (if needed)
    # scrollbar = ttk.Scrollbar(output_frame, orient="vertical", command=output_text.yview)
    # scrollbar.pack(side="right", fill="y")
    # output_text.config(yscrollcommand=scrollbar.set)

    # Make left_frame expandable
    left_frame.columnconfigure(1, weight=1)
    right_frame.columnconfigure(0, weight=1)


    # === Help Menu ===
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    help_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="Documentation", command=lambda: show_documentation())

    # === Function to Show Documentation ===
    def show_documentation():
        doc_window = tk.Toplevel(root)
        doc_window.title("📘 Pseudonym Generator - Help & Documentation")
        doc_window.geometry("700x600")
        doc_window.resizable(True, True)
        doc_window.configure(bg="#f0f0f0")

        title = tk.Label(doc_window, text=tool_version, font=("Arial", 16, "bold"), bg="#f0f0f0")
        title.pack(pady=10)

        text_frame = ttk.Frame(doc_window)
        text_frame.pack(fill="both", expand=True, padx=20, pady=10)

        text_widget = tk.Text(text_frame, wrap="word", font=("Arial", 11), bg="#ffffff", fg="#000000")
        text_widget.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        scrollbar.pack(side="right", fill="y")
        text_widget.config(yscrollcommand=scrollbar.set)

        doc_content = f"""
📘 {tool_version} – User Guide

This tool generates secure, anonymized pseudonyms for research participants using two modes:

---

🔧 Mode 1: Input Mode
Enter participant data to generate a base code:
- Last Name
- First Name
- Date of Birth (YYYY-MM-DD or DD/MM/YYYY)
- Place of Birth

The tool generates a base code (e.g., HSPR2130) automatically.

---

🔧 Mode 2: Base Code Mode
Enter an existing base code (8 digits) to generate pseudonyms:
- Use this when you already have a base code from another system
- Enter the same password to regenerate the same pseudonyms

---

🔍 Output Format
- Base Code: 8-digit code (e.g., HSPR2130)
- Pseudonyms: 8-character code with label (e.g., 6TWH-HU#9_sosci)
- Verification Code: 8-character code (e.g., A3F9-#B1C)

---

🛡️ Security & Privacy
- No PII is stored or transmitted.
- Passwords are never saved.
- All hashing is done locally.
- Ambiguous characters (0, O) are replaced with # and +.

---

✅ Best Practices
- Use a different password for each study.
- Never share the password.
- Store raw data securely (encrypted database).
- Use the verification code to double-check data entry.

---

💡 Troubleshooting
- If the tool crashes: Check that all fields are filled.
- If verification fails: Re-enter the password.
- If no output: Check for invalid DOB format.

---

📄 For Research Teams
This tool is GDPR/IRB-compliant. Use it to:
- Anonymize participant data
- Link data across sessions
- Ensure data integrity

For support contact https://github.com/tobgroth.

---
        """.strip()

        text_widget.insert("1.0", doc_content)
        text_widget.config(state="disabled")

        close_btn = ttk.Button(doc_window, text="Close", command=doc_window.destroy)
        close_btn.pack(pady=10)

    # === Run GUI ===
    root.mainloop()

if __name__ == "__main__":
    try:
        tool_version = "PseudonymGenerator v1.0"
        main_gui(tool_version)
    except Exception as e:
        import traceback
        print("Fatal error in GUI:", traceback.format_exc())
        messagebox.showerror("Fatal Error", f"An error occurred: {e}")
