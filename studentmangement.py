import tkinter as tk
from tkinter import ttk, messagebox
import pickle
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Student:
    def __init__(self, id, name, student_class, marks):
        self.id = id
        self.name = name
        self.student_class = student_class
        self.marks = marks
        self.total = sum(marks)
        self.avg = self.total / len(marks)
        self.grade = self.calculate_grade()

    def calculate_grade(self):
        if self.avg >= 90:
            return 'A'
        elif self.avg >= 80:
            return 'B'
        elif self.avg >= 70:
            return 'C'
        elif self.avg >= 60:
            return 'D'
        else:
            return 'F'

    def update_marks(self, marks):
        self.marks = marks
        self.total = sum(marks)
        self.avg = self.total / len(marks)
        self.grade = self.calculate_grade()

    def to_tuple(self):
        return (self.id, self.name, self.student_class, *self.marks, self.total, f"{self.avg:.2f}", self.grade)


class CRUDOperations:
    def __init__(self):
        self.students = []

    def create_student(self, id, name, student_class, marks):
        for student in self.students:
            if student.id == id:
                return "Student ID already exists!"
        self.students.append(Student(id, name, student_class, marks))
        return "Student created successfully."

    def read_student(self, id):
        for student in self.students:
            if student.id == id:
                return student.to_tuple()
        return None

    def read_students(self):
        return [student.to_tuple() for student in self.students]

    def update_student(self, id, new_name, new_marks):
        for student in self.students:
            if student.id == id:
                student.name = new_name
                student.update_marks(new_marks)
                return "Student updated successfully."
        return "Student not found."

    def delete_student(self, id):
        for student in self.students:
            if student.id == id:
                self.students.remove(student)
                return "Student deleted successfully."
        return "Student not found."

    def save_data(self):
        with open("students_data.pkl", "wb") as file:
            pickle.dump(self.students, file)

    def load_data(self):
        try:
            with open("students_data.pkl", "rb") as file:
                self.students = pickle.load(file)
        except FileNotFoundError:
            pass


# Initialize CRUD operations
crud = CRUDOperations()
crud.load_data()  # Load data from file at startup

# GUI Setup
root = tk.Tk()
root.title("Pitesh Education Academy Class 1st to 8th (H.M. & E.M.)")
root.geometry("1000x700")
root.config(bg="#2f2f2f")

# Header Frame
header_frame = tk.Frame(root, bg="#333333", pady=15)
header_frame.pack(fill="x")

header_label = tk.Label(
    header_frame,
    text="Pitesh Education Academy Class 1st to 8th (H.M. & E.M.)",
    font=("Arial", 24, "bold"),
    bg="#333333",
    fg="#32cd32"
)
header_label.pack()

# Input Frame
input_frame = tk.Frame(root, padx=10, pady=10, bg="#444444")
input_frame.pack(side=tk.LEFT, fill="y")

# Fields
fields = ["ID", "Name", "Class", "Marks ENG", "Marks MATHS", "Marks SCIENCE", "Marks HINDI", "Marks DRAWING",
          "Marks COMPUTER"]
entries = []

for i, field in enumerate(fields):
    tk.Label(input_frame, text=field + ":", font=("Arial", 14), bg="#444444", fg="white").grid(row=i, column=0, padx=10,
                                                                                               pady=5, sticky="e")
    entry = tk.Entry(input_frame, font=("Arial", 14), bg="#666666", fg="white")
    entry.grid(row=i, column=1, padx=10, pady=5)
    entries.append(entry)

# Buttons
button_frame = tk.Frame(input_frame, bg="#444444")
button_frame.grid(row=len(fields), column=0, columnspan=2, pady=15)


def create_student():
    try:
        id = int(entries[0].get())
        name = entries[1].get()
        student_class = entries[2].get()
        marks = [int(entries[i].get()) for i in range(3, 9)]
        message = crud.create_student(id, name, student_class, marks)
        messagebox.showinfo("Result", message)
        update_table()
        update_chart()
        clear_entries()
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter valid data.")


def update_student_func():
    try:
        id = int(entries[0].get())
        new_name = entries[1].get()
        new_marks = [int(entries[i].get()) for i in range(3, 9)]
        message = crud.update_student(id, new_name, new_marks)
        messagebox.showinfo("Result", message)
        update_table()
        update_chart()
        clear_entries()
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter valid data.")


def delete_student():
    try:
        id = int(entries[0].get())
        message = crud.delete_student(id)
        messagebox.showinfo("Result", message)
        update_table()
        update_chart()
        clear_entries()
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter a valid ID.")


def clear_entries():
    for entry in entries:
        entry.delete(0, tk.END)


def read_student():
    try:
        id = int(entries[0].get())
        student_data = crud.read_student(id)
        if student_data:
            details = f"ID: {student_data[0]}\nName: {student_data[1]}\nClass: {student_data[2]}\n" \
                      f"ENG: {student_data[3]}\nMATHS: {student_data[4]}\nSCIENCE: {student_data[5]}\n" \
                      f"HINDI: {student_data[6]}\nDRAWING: {student_data[7]}\nCOMPUTER: {student_data[8]}\n" \
                      f"Total: {student_data[9]}\nAverage: {student_data[10]}\nGrade: {student_data[11]}"
            messagebox.showinfo("Student Details", details)
        else:
            messagebox.showinfo("Result", "Student not found.")
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter a valid ID.")


def update_table():
    for i in tree.get_children():
        tree.delete(i)
    for student in crud.read_students():
        tree.insert("", "end", values=student)


def update_chart():
    # Clear previous chart if any
    for widget in chart_frame.winfo_children():
        widget.destroy()

    # Extract data from students' tuples returned by read_students
    ids = [str(student[0]) for student in crud.read_students()]
    totals = [student[9] for student in crud.read_students()]

    if len(ids) > 0:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(ids, totals, color='#32cd32')
        ax.set_title("Student Performance", fontsize=16, color="white")
        ax.set_xlabel("Student ID", fontsize=12, color="white")
        ax.set_ylabel("Total Marks", fontsize=12, color="white")
        ax.tick_params(axis='x', colors="white")
        ax.tick_params(axis='y', colors="white")

        for label in ax.get_xticklabels():
            label.set_rotation(45)

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


# Buttons in the button_frame
tk.Button(button_frame, text="Create", font=("Arial", 12), bg="#32cd32", fg="white", command=create_student).grid(row=0,
                                                                                                                  column=0,
                                                                                                                  padx=5)
tk.Button(button_frame, text="Read", font=("Arial", 12), bg="#1e90ff", fg="white", command=read_student).grid(row=1,
                                                                                                              column=0,
                                                                                                              padx=5)
tk.Button(button_frame, text="Update", font=("Arial", 12), bg="#ffa500", fg="white", command=update_student_func).grid(row=2,
                                                                                                                  column=0,
                                                                                                                  padx=5)
tk.Button(button_frame, text="Delete", font=("Arial", 12), bg="#dc143c", fg="white", command=delete_student).grid(row=3,
                                                                                                                  column=0,
                                                                                                                  padx=5)

# Table Frame (Positioned in the upper portion)
table_frame = tk.Frame(root, bg="#333333", padx=10, pady=10)
table_frame.pack(side=tk.TOP, fill="both", expand=True)

columns = (
    "ID", "Name", "Class", "ENG", "MATHS", "SCIENCE", "HINDI", "DRAWING", "COMPUTER", "Total", "Average", "Grade")
tree = ttk.Treeview(table_frame, columns=columns, show="headings", style="Dark.Treeview")
tree.pack(fill="both", expand=True)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor=tk.CENTER, width=120)

scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
scrollbar.pack(side="right", fill="y")
tree.config(yscrollcommand=scrollbar.set)

# Define dark theme style for Treeview
style = ttk.Style()
style.configure("Dark.Treeview", background="#444444", foreground="white", fieldbackground="#444444")
style.map("Dark.Treeview", background=[("selected", "#1e90ff")])

# Student Performance Chart Frame (Initially empty)
chart_frame = tk.Frame(root, bg="#333333", padx=10, pady=10)
chart_frame.pack(side=tk.BOTTOM, fill="both", expand=True)

# Binding the double-click event on the Treeview to read student details
tree.bind("<Double-1>", lambda event: read_student())

update_table()
update_chart()

root.mainloop()


