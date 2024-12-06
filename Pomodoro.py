import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import ttkbootstrap as ttk
import time
import threading
from docx import Document
import os



class Task:
    def __init__(self, parent, tasks, task_no, task_name=None, time=15):
        self.parent = parent
        self.tasks = tasks
        self.task_no = task_no
        self.task_name = task_name
        self.time = time
        self.time_remaining = time * 60
        self.timer_running = False
        self.pdf_process = None
        self.pdf_path = ''
        self.create_widgets()

    def create_widgets(self):

        self.frame = ttk.Frame(self.parent, padding=10, relief="ridge")
        self.frame.pack(fill="x", pady=5)


        self.task_label = ttk.Label(self.frame, text=self.task_no, font=("Helvetica", 16))
        self.task_label.grid(row=0, column=0,padx=5, sticky="w")

        self.timer_label = ttk.Label(self.frame, text="15:00", font=("Helvetica", 16), bootstyle="info")
        self.timer_label.grid(row=0, column=1)

        self.task_entry = ttk.Entry(self.frame, font=("Helvetica", 16), width=10)
        self.task_entry.grid(row=0, column=2, padx=10)


        self.timer_var = tk.StringVar()
        self.timer_var.trace_add("write", self.on_timer_entry_change)  # Monitor changes
        self.timer_entry = ttk.Entry(self.frame, textvariable=self.timer_var, font=("Helvetica", 16), width=5)
        self.timer_entry.grid(row=0, column=3, padx=100)


        self.start_button = ttk.Button(self.frame, text="Start", command=self.start_timer, bootstyle="success")
        self.start_button.grid(row=1, column=0, padx=5, pady=15, sticky="w")


        self.reset_button = ttk.Button(self.frame, text="Reset", command=self.reset_timer , bootstyle='info')
        self.reset_button.grid(row=1, column=1, padx=5, pady=5, sticky="w")


        self.delete_time = ttk.Button(self.frame, text="Delete", command=self.delete_timer, bootstyle="danger")
        self.delete_time.grid(row=1, column=2,padx=5, pady=5, sticky="w")


        self.open_pdf_button = ttk.Button(self.frame, text="Open PDF", command=self.open_pdf, bootstyle="info")
        self.open_pdf_button.grid(row=1, column=3,padx=5, pady=5, sticky="w")

    def on_timer_entry_change(self, *args):
        if self.timer_var.get().strip():
            self.confirm_time()

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            threading.Thread(target=self.run_timer, daemon=True).start()

    def reset_timer(self):
        self.timer_running = False
        self.time_remaining = 15 * 60
        self.update_timer_label()

    def delete_timer(self):
        self.frame.destroy()
        self.tasks.remove(self)

    def run_timer(self):
        while self.time_remaining > 0 and self.timer_running:
            mins, secs = divmod(self.time_remaining, 60)
            self.timer_label.config(text=f"{mins:02}:{secs:02}")
            time.sleep(1)
            self.time_remaining -= 1

        if self.time_remaining == 0:
            self.timer_running = False
            self.task_name = self.task_entry.get()
            self.timer_label.config(text="00:00")
            messagebox.showinfo("Time's Up!", f"Time's up for task: {self.task_name}")
            self.close_pdf()
            self.open_word_file()

    def confirm_time(self):
        try:
            self.time_remaining = int(self.timer_var.get()) * 60
            self.update_timer_label()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")

    def update_timer_label(self):
        mins, secs = divmod(self.time_remaining, 60)
        self.timer_label.config(text=f"{mins:02}:{secs:02}")

    def open_pdf(self):
        self.pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if self.pdf_path:
            try:
                os.startfile(self.pdf_path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open PDF: {e}")

    def close_pdf(self):
        if self.pdf_process:
            self.pdf_process.terminate()
            self.pdf_process = None

    def open_word_file(self):
        if self.task_entry.get() != '':
            self.task_name = self.task_entry.get()
        else:
            self.task_name = self.pdf_path
        doc = Document()
        doc.add_heading(f"{self.task_no}")

        doc.add_paragraph(f"Task Name: {self.task_name}")

        doc_file = f"{self.task_name.replace(" ", '')}.docx"
        doc.save(doc_file)
        try:
            os.startfile(doc_file)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Word file: {e}")


class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("600x400")

        # Task container
        self.task_container = ttk.Frame(self.root)
        self.task_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Add Task Button
        self.add_task_button = ttk.Button(self.root, text="Add New Task", command=self.add_task , bootstyle="info")
        self.add_task_button.pack(side="right", padx=10, pady=10)
        self.temp = 1
        self.tasks = []

    def add_task(self):
        task_no = f"Task {self.temp}"
        self.temp += 1
        new_task = Task(self.task_container, self.tasks, task_no)
        self.tasks.append(new_task)
        print(self.tasks)


if __name__ == "__main__":
    root = ttk.Window("Pomodoro Timer", "superhero")
    app = PomodoroApp(root)
    root.mainloop()
