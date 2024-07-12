import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os

class TodoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced To-Do List")
        self.root.geometry("400x350")
        self.root.configure(bg="#f0f0f0")  # Set window background color
        self.filename = 'tasks.json'
        self.tasks = self.load_tasks()

        self.create_widgets()
        self.load_listbox()

    def create_widgets(self):
        self.frame = tk.Frame(self.root, bg="#d9d9d9")
        self.frame.pack(pady=10)

        self.listbox = tk.Listbox(self.frame, width=50, height=10, selectmode=tk.SINGLE, bg="#ffffff", fg="#000000")
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical")
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox.config(yscrollcommand=self.scrollbar.set)

        self.entry_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.entry_frame.pack(pady=5)

        self.entry = tk.Entry(self.entry_frame, width=30, bg="#ffffff", fg="#000000")
        self.entry.pack(side=tk.LEFT, padx=5)

        self.add_button = tk.Button(self.entry_frame, text="Add Task", command=self.add_task, bg="#4caf50", fg="#ffffff",width=10, height=1)
        self.add_button.pack(side=tk.LEFT)

        self.update_button = tk.Button(self.root, text="Update Task", command=self.update_task, bg="#2196f3", fg="#ffffff",width=10, height=1)
        self.update_button.pack(pady=5)

        self.done_button = tk.Button(self.root, text="Mark as Done", command=self.mark_as_done, bg="#ffeb3b", fg="#000000",width=10, height=1)
        self.done_button.pack(pady=5)

        self.delete_button = tk.Button(self.root, text="Delete Task", command=self.delete_task, bg="#f44336", fg="#ffffff",width=10, height=1)
        self.delete_button.pack(pady=5)

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                return json.load(f)
        return []

    def save_tasks(self):
        with open(self.filename, 'w') as f:
            json.dump(self.tasks, f, indent=4)

    def load_listbox(self):
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "Done" if task["completed"] else "Not done"
            self.listbox.insert(tk.END, f"{task['task']} [{status}]")

    def add_task(self):
        task = self.entry.get()
        if task:
            self.tasks.append({"task": task, "completed": False})
            self.save_tasks()
            self.load_listbox()
            self.entry.delete(0, tk.END)

    def update_task(self):
        selected = self.listbox.curselection()
        if selected:
            index = selected[0]
            task = self.tasks[index]
            new_task = simpledialog.askstring("Update Task", "Enter new task:", initialvalue=task["task"])
            if new_task is not None:
                self.tasks[index]["task"] = new_task
                self.save_tasks()
                self.load_listbox()

    def mark_as_done(self):
        selected = self.listbox.curselection()
        if selected:
            index = selected[0]
            self.tasks[index]["completed"] = True
            self.save_tasks()
            self.load_listbox()

    def delete_task(self):
        selected = self.listbox.curselection()
        if selected:
            index = selected[0]
            del self.tasks[index]
            self.save_tasks()
            self.load_listbox()

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoListApp(root)
    root.mainloop()
