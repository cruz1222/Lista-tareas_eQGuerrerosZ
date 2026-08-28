import tkinter as tk
from tkinter import messagebox


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista de Tareas")
        self.root.geometry("560x560")
        self.root.resizable(False, False)

        self.tasks = []

        self.main = tk.Frame(root)
        self.main.pack(fill="both", expand=True, padx=20, pady=20)

        title = tk.Label(
            self.main,
            text="Lista de Tareas",
            font=("Arial", 20, "bold"),
            anchor="center",
            justify="center",
        )
        title.pack(pady=(0, 15), fill="x")

        self.task_var = tk.StringVar()
        entry_frame = tk.Frame(self.main)
        entry_frame.pack(pady=10)

        self.entry = tk.Entry(
            entry_frame,
            textvariable=self.task_var,
            width=35,
            font=("Arial", 12),
            justify="center",
        )
        self.entry.grid(row=0, column=0, padx=6)
        self.entry.bind("<Return>", lambda event: self.add_task())

        add_btn = tk.Button(entry_frame, text="Agregar", width=12, command=self.add_task)
        add_btn.grid(row=0, column=1, padx=6)

        list_frame = tk.Frame(self.main)
        list_frame.pack(pady=10, fill="both", expand=True)

        self.listbox = tk.Listbox(
            list_frame,
            font=("Arial", 12),
            width=46,
            height=14,
            justify="center",
            selectmode="browse",
        )
        self.listbox.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(list_frame, command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

        btn_frame = tk.Frame(self.main)
        btn_frame.pack(pady=10)

        buttons = [
            ("Completada", self.toggle_done, 0, 0),
            ("Editar", self.edit_task, 0, 1),
            ("Eliminar", self.delete_task, 0, 2),
            ("Mostrar todo", self.refresh_list, 1, 0),
            ("Pendientes", self.show_pending, 1, 1),
            ("Terminadas", self.show_completed, 1, 2),
        ]

        for text, command, row, col in buttons:
            tk.Button(btn_frame, text=text, width=14, command=command).grid(
                row=row, column=col, padx=6, pady=6
            )

        self.status_var = tk.StringVar(value="Agrega una tarea para empezar.")
        status = tk.Label(
            self.main,
            textvariable=self.status_var,
            anchor="center",
            justify="center",
            font=("Arial", 11),
        )
        status.pack(fill="x", padx=10, pady=(10, 0))

    def add_task(self):
        task = self.task_var.get().strip()
        if not task:
            messagebox.showwarning("Aviso", "Escribe una tarea primero.")
            return
        self.tasks.append({"text": task, "done": False})
        self.task_var.set("")
        self.refresh_list()
        self.status_var.set("Tarea agregada.")

    def selected_index(self):
        selection = self.listbox.curselection()
        if not selection:
            return None
        return selection[0]

    def refresh_list(self, tasks=None):
        self.listbox.delete(0, tk.END)
        data = self.tasks if tasks is None else tasks
        for i, task in enumerate(data, start=1):
            mark = "✓" if task["done"] else " "
            self.listbox.insert(tk.END, f"{i}. [{mark}] {task['text']}")
        self.status_var.set(f"Total de tareas: {len(self.tasks)}")

    def toggle_done(self):
        idx = self.selected_index()
        if idx is None:
            messagebox.showinfo("Selecciona", "Elige una tarea de la lista.")
            return
        self.tasks[idx]["done"] = not self.tasks[idx]["done"]
        self.refresh_list()
        self.status_var.set("Estado de tarea actualizado.")

    def edit_task(self):
        idx = self.selected_index()
        if idx is None:
            messagebox.showinfo("Selecciona", "Elige una tarea de la lista.")
            return
        new_text = self.task_var.get().strip()
        if not new_text:
            messagebox.showwarning("Aviso", "Escribe el nuevo texto en la caja superior.")
            return
        self.tasks[idx]["text"] = new_text
        self.task_var.set("")
        self.refresh_list()
        self.status_var.set("Tarea editada.")

    def delete_task(self):
        idx = self.selected_index()
        if idx is None:
            messagebox.showinfo("Selecciona", "Elige una tarea de la lista.")
            return
        del self.tasks[idx]
        self.refresh_list()
        self.status_var.set("Tarea eliminada.")

    def show_pending(self):
        pending = [t for t in self.tasks if not t["done"]]
        self.refresh_list(pending)
        self.status_var.set("Mostrando tareas pendientes.")

    def show_completed(self):
        completed = [t for t in self.tasks if t["done"]]
        self.refresh_list(completed)
        self.status_var.set("Mostrando tareas terminadas.")


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
