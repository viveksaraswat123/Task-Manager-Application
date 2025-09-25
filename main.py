import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# Database setup
conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    priority TEXT DEFAULT 'Medium',
    due_date TEXT,
    status TEXT DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

# Functions
def add_task():
    task = entry_task.get().strip()
    priority = combo_priority.get()
    due_date = entry_due.get().strip()

    if task == "":
        messagebox.showwarning("Warning", "Task cannot be empty!")
        return

    cursor.execute("INSERT INTO tasks (title, priority, due_date) VALUES (?, ?, ?)",
                   (task, priority, due_date))
    conn.commit()
    entry_task.delete(0, tk.END)
    entry_due.delete(0, tk.END)
    load_tasks()

def delete_task():
    try:
        selected = tree.selection()[0]
        task_id = tree.item(selected)['values'][0]
        cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
        load_tasks()
    except:
        messagebox.showwarning("Warning", "Please select a task to delete.")

def mark_completed():
    try:
        selected = tree.selection()[0]
        task_id = tree.item(selected)['values'][0]
        cursor.execute("UPDATE tasks SET status='Completed' WHERE id=?", (task_id,))
        conn.commit()
        load_tasks()
    except:
        messagebox.showwarning("Warning", "Please select a task to mark completed.")

def search_tasks():
    keyword = entry_search.get().strip().lower()
    tree.delete(*tree.get_children())
    cursor.execute("SELECT * FROM tasks WHERE LOWER(title) LIKE ?", ('%' + keyword + '%',))
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)

def load_tasks():
    tree.delete(*tree.get_children())
    cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)

# UI Setup
root = tk.Tk()
root.title("📋 Advanced Task Manager")
root.geometry("750x500")
root.resizable(False, False)

# Input Frame
frame_top = tk.Frame(root, pady=10)
frame_top.pack()

tk.Label(frame_top, text="Task:").grid(row=0, column=0, padx=5)
entry_task = tk.Entry(frame_top, width=40)
entry_task.grid(row=0, column=1, padx=5)

tk.Label(frame_top, text="Priority:").grid(row=0, column=2, padx=5)
combo_priority = ttk.Combobox(frame_top, values=["High", "Medium", "Low"], width=7)
combo_priority.grid(row=0, column=3, padx=5)
combo_priority.set("Medium")

tk.Label(frame_top, text="Due Date (YYYY-MM-DD):").grid(row=0, column=4, padx=5)
entry_due = tk.Entry(frame_top, width=12)
entry_due.grid(row=0, column=5, padx=5)

btn_add = tk.Button(frame_top, text="➕ Add Task", command=add_task, bg="#4CAF50", fg="white")
btn_add.grid(row=0, column=6, padx=5)

# Search Frame
frame_search = tk.Frame(root, pady=5)
frame_search.pack()
tk.Label(frame_search, text="🔍 Search:").pack(side=tk.LEFT, padx=5)
entry_search = tk.Entry(frame_search, width=30)
entry_search.pack(side=tk.LEFT, padx=5)
btn_search = tk.Button(frame_search, text="Search", command=search_tasks)
btn_search.pack(side=tk.LEFT, padx=5)
btn_show_all = tk.Button(frame_search, text="Show All", command=load_tasks)
btn_show_all.pack(side=tk.LEFT, padx=5)

# Task Table
cols = ("ID", "Title", "Priority", "Due Date", "Status", "Created At")
tree = ttk.Treeview(root, columns=cols, show="headings", height=15)
for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=120 if col != "Title" else 220)
tree.pack(pady=10)

# Action Buttons
frame_actions = tk.Frame(root, pady=10)
frame_actions.pack()

btn_complete = tk.Button(frame_actions, text="✔ Mark Completed", command=mark_completed, bg="#2196F3", fg="white")
btn_complete.grid(row=0, column=0, padx=10)

btn_delete = tk.Button(frame_actions, text="🗑 Delete Task", command=delete_task, bg="#f44336", fg="white")
btn_delete.grid(row=0, column=1, padx=10)

# Load tasks on startup
load_tasks()

root.mainloop()
