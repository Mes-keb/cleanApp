import os
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# --- Helper function to hash files ---
def get_file_hash(filepath):
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            buf = f.read(4096)
            while buf:
                hasher.update(buf)
                buf = f.read(4096)
        return hasher.hexdigest()
    except:
        return None  




# --- Main App Class ---
class DuplicateCleanerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Duplicate Cleaner App")
        self.root.geometry("700x500")
        self.root.resizable(False, False)
        self.folder_path = tk.StringVar()
        self.duplicates = {}
        # --- UI Layout ---
        self.setup_ui()
    def setup_ui(self):
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack(fill="x")




        tk.Label(frame, text="Select Folder:", font=('Arial', 12)).pack(side="left")
        tk.Entry(frame, textvariable=self.folder_path, width=50).pack(side="left", padx=5)
        tk.Button(frame, text="Browse", command=self.browse_folder).pack(side="left")
        tk.Button(self.root, text="Scan for Duplicates", command=self.scan_duplicates,
          bg="#83C8D8", fg="white").pack(pady=10)
        # --- Treeview for results ---
        columns = ("#1", "#2")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=15)
        self.tree.heading("#1", text="Duplicate File Path")
        self.tree.heading("#2", text="Size (KB)")
        self.tree.column("#1", width=500)
        self.tree.column("#2", width=100, anchor="center")
        self.tree.pack(padx=10, pady=10)
    tk.Button(self.root, text="Delete Selected", command=self.delete_selected,
          bg="#83C8D8", fg="white").pack(pady=5)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)

    def scan_duplicates(self):
        folder = self.folder_path.get()
        if not folder:
            messagebox.showwarning("warning", "please select a folder first!")
            return

        self.tree.delete(*self.tree.get_children())
        self.duplicates.clear()
        hash_map = {}

        for root_dir, _, files in os.walk(folder):
            for filename in files:
                filepath = os.path.join(root_dir, filename)
                file_hash = get_file_hash(filepath)
                if file_hash:
                    if file_hash in hash_map:
                        self.duplicates[filepath] = hash_map[file_hash]
                    else:
                        hash_map[file_hash] = filepath

        if not self.duplicates:
            messagebox.showinfo("result", "no duplicate files found.")
            return

        # Display Duplicates
        for dup, orig in self.duplicates.items():
            size_kb = os.path.getsize(dup) // 1024
            self.tree.insert("", "end", values=(dup, size_kb))

        messagebox showinfo/"Scan Complete" f"Found {len(self.duplicates)} duplicate files."