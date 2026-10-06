import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from part1_oop import Student, Instructor, Course, save_data, load_data

students = []
instructors = []
courses = []

def refresh_instructor_dropdown():
    instructor_dropdown["values"] = [
        f"{instructor.instructor_id} - {instructor.name}"
        for instructor in instructors
    ]

def refresh_registration_dropdowns():
    student_registration_dropdown["values"] = [
        f"{student.student_id} - {student.name}"
        for student in students
    ]

    course_registration_dropdown["values"] = [
        f"{course.course_id} - {course.course_name}"
        for course in courses
    ]

def add_student():
    try:
        name = student_name_entry.get()
        age = int(student_age_entry.get())
        email = student_email_entry.get()
        student_id = student_id_entry.get()

        if name == "" or email == "" or student_id == "":
            messagebox.showerror(
                "Error",
                "Please fill in all fields."
            )
            return

        student = Student(
            name,
            age,
            email,
            student_id
        )

        students.append(student)
        
        refresh_registration_dropdowns()
        refresh_records()
        messagebox.showinfo(
            "Success",
            "Student added successfully!"
        )

        student_name_entry.delete(0, tk.END)
        student_age_entry.delete(0, tk.END)
        student_email_entry.delete(0, tk.END)
        student_id_entry.delete(0, tk.END)

    except ValueError as error:
        messagebox.showerror(
            "Invalid Input",
            str(error)
        )

def add_instructor():
    try:
        name = instructor_name_entry.get()
        age = int(instructor_age_entry.get())
        email = instructor_email_entry.get()
        instructor_id = instructor_id_entry.get()

        if name == "" or email == "" or instructor_id == "":
            messagebox.showerror(
                "Error",
                "Please fill in all fields."
            )
            return

        instructor = Instructor(
            name,
            age,
            email,
            instructor_id
        )

        instructors.append(instructor)
        refresh_instructor_dropdown()
        refresh_records()
        messagebox.showinfo(
            "Success",
            "Instructor added successfully!"
        )

        instructor_name_entry.delete(0, tk.END)
        instructor_age_entry.delete(0, tk.END)
        instructor_email_entry.delete(0, tk.END)
        instructor_id_entry.delete(0, tk.END)

    except ValueError as error:
        messagebox.showerror(
            "Invalid Input",
            str(error)
        )

def add_course():
    course_id = course_id_entry.get()
    course_name = course_name_entry.get()
    selected_instructor = instructor_dropdown.get()

    if course_id == "" or course_name == "":
        messagebox.showerror(
            "Error",
            "Please fill in all course fields."
        )
        return

    instructor = None

    if selected_instructor != "":
        instructor_id = selected_instructor.split(" - ")[0]

        for inst in instructors:
            if inst.instructor_id == instructor_id:
                instructor = inst
                break

    course = Course(
        course_id,
        course_name,
        instructor
    )

    courses.append(course)

    if instructor is not None:
        instructor.assign_course(course)

    refresh_registration_dropdowns()
    refresh_records()
    messagebox.showinfo(
        "Success",
        "Course added successfully!"
    )

    course_id_entry.delete(0, tk.END)
    course_name_entry.delete(0, tk.END)
    instructor_dropdown.set("")

def register_student():
    selected_student = student_registration_dropdown.get()
    selected_course = course_registration_dropdown.get()

    if selected_student == "" or selected_course == "":
        messagebox.showerror(
            "Error",
            "Please select both a student and a course."
        )
        return

    student_id = selected_student.split(" - ")[0]
    course_id = selected_course.split(" - ")[0]

    student = None
    course = None

    for s in students:
        if s.student_id == student_id:
            student = s
            break

    for c in courses:
        if c.course_id == course_id:
            course = c
            break

    if course in student.registered_courses:
        messagebox.showerror(
            "Error",
            "Student is already registered in this course."
        )
        return

    student.register_course(course)
    course.add_student(student)
    refresh_records()
    
    messagebox.showinfo(
        "Success",
        "Student registered successfully!"
    )

    student_registration_dropdown.set("")
    course_registration_dropdown.set("")

def refresh_records(search_text=""):
    # Clear the current table
    for item in records_tree.get_children():
        records_tree.delete(item)

    search_text = search_text.lower()

    # Students
    for student in students:
        course_names = ", ".join(
            course.course_id for course in student.registered_courses
        )

        values = (
            "Student",
            student.student_id,
            student.name,
            f"Courses: {course_names if course_names else 'None'}"
        )

        if search_text == "" or search_text in " ".join(values).lower():
            records_tree.insert("", tk.END, values=values)

    # Instructors
    for instructor in instructors:
        course_names = ", ".join(
            course.course_id for course in instructor.assigned_courses
        )

        values = (
            "Instructor",
            instructor.instructor_id,
            instructor.name,
            f"Courses: {course_names if course_names else 'None'}"
        )

        if search_text == "" or search_text in " ".join(values).lower():
            records_tree.insert("", tk.END, values=values)

    # Courses
    for course in courses:
        instructor_name = (
            course.instructor.name
            if course.instructor is not None
            else "None"
        )

        values = (
            "Course",
            course.course_id,
            course.course_name,
            f"Instructor: {instructor_name}"
        )

        if search_text == "" or search_text in " ".join(values).lower():
            records_tree.insert("", tk.END, values=values)

def search_records():
    search_text = search_entry.get()
    refresh_records(search_text)


def show_all_records():
    search_entry.delete(0, tk.END)
    refresh_records()

def delete_record():
    selected = records_tree.selection()

    if not selected:
        messagebox.showerror("Error", "Please select a record.")
        return

    values = records_tree.item(selected[0], "values")
    record_type = values[0]
    record_id = values[1]

    confirm = messagebox.askyesno(
        "Delete Record",
        "Are you sure you want to delete this record?"
    )

    if not confirm:
        return

    if record_type == "Student":
        student = next(
            (s for s in students if s.student_id == record_id),
            None
        )

        if student:
            for course in list(student.registered_courses):
                if student in course.enrolled_students:
                    course.enrolled_students.remove(student)

            students.remove(student)

    elif record_type == "Instructor":
        instructor = next(
            (i for i in instructors if i.instructor_id == record_id),
            None
        )

        if instructor:
            for course in list(instructor.assigned_courses):
                course.instructor = None

            instructors.remove(instructor)

    elif record_type == "Course":
        course = next(
            (c for c in courses if c.course_id == record_id),
            None
        )

        if course:
            for student in list(course.enrolled_students):
                if course in student.registered_courses:
                    student.registered_courses.remove(course)

            if (
                course.instructor is not None
                and course in course.instructor.assigned_courses
            ):
                course.instructor.assigned_courses.remove(course)

            courses.remove(course)

    refresh_instructor_dropdown()
    refresh_registration_dropdowns()
    refresh_records()

    messagebox.showinfo(
        "Success",
        "Record deleted successfully!"
    )


def edit_record():
    selected = records_tree.selection()

    if not selected:
        messagebox.showerror("Error", "Please select a record.")
        return

    values = records_tree.item(selected[0], "values")
    record_type = values[0]
    record_id = values[1]

    if record_type == "Student":
        student = next(
            (s for s in students if s.student_id == record_id),
            None
        )

        if student is None:
            return

        name = simpledialog.askstring(
            "Edit Student",
            "Name:",
            initialvalue=student.name
        )

        if name is None:
            return

        age = simpledialog.askinteger(
            "Edit Student",
            "Age:",
            initialvalue=student.age,
            minvalue=0
        )

        if age is None:
            return

        email = simpledialog.askstring(
            "Edit Student",
            "Email:",
            initialvalue=student._email
        )

        if email is None:
            return

        student_id = simpledialog.askstring(
            "Edit Student",
            "Student ID:",
            initialvalue=student.student_id
        )

        if student_id is None:
            return

        if name == "" or email == "" or student_id == "":
            messagebox.showerror(
                "Error",
                "Fields cannot be empty."
            )
            return

        if not student.valid_email(email):
            messagebox.showerror(
                "Error",
                "Invalid email format."
            )
            return

        if any(
            s is not student and s.student_id == student_id
            for s in students
        ):
            messagebox.showerror(
                "Error",
                "Student ID already exists."
            )
            return

        student.name = name
        student.age = age
        student._email = email
        student.student_id = student_id

    elif record_type == "Instructor":
        instructor = next(
            (i for i in instructors if i.instructor_id == record_id),
            None
        )

        if instructor is None:
            return

        name = simpledialog.askstring(
            "Edit Instructor",
            "Name:",
            initialvalue=instructor.name
        )

        if name is None:
            return

        age = simpledialog.askinteger(
            "Edit Instructor",
            "Age:",
            initialvalue=instructor.age,
            minvalue=0
        )

        if age is None:
            return

        email = simpledialog.askstring(
            "Edit Instructor",
            "Email:",
            initialvalue=instructor._email
        )

        if email is None:
            return

        instructor_id = simpledialog.askstring(
            "Edit Instructor",
            "Instructor ID:",
            initialvalue=instructor.instructor_id
        )

        if instructor_id is None:
            return

        if name == "" or email == "" or instructor_id == "":
            messagebox.showerror(
                "Error",
                "Fields cannot be empty."
            )
            return

        if not instructor.valid_email(email):
            messagebox.showerror(
                "Error",
                "Invalid email format."
            )
            return

        if any(
            i is not instructor
            and i.instructor_id == instructor_id
            for i in instructors
        ):
            messagebox.showerror(
                "Error",
                "Instructor ID already exists."
            )
            return

        instructor.name = name
        instructor.age = age
        instructor._email = email
        instructor.instructor_id = instructor_id

    elif record_type == "Course":
        course = next(
            (c for c in courses if c.course_id == record_id),
            None
        )

        if course is None:
            return

        course_id = simpledialog.askstring(
            "Edit Course",
            "Course ID:",
            initialvalue=course.course_id
        )

        if course_id is None:
            return

        course_name = simpledialog.askstring(
            "Edit Course",
            "Course Name:",
            initialvalue=course.course_name
        )

        if course_name is None:
            return

        current_instructor_id = ""

        if course.instructor is not None:
            current_instructor_id = course.instructor.instructor_id

        instructor_id = simpledialog.askstring(
            "Edit Course",
            "Instructor ID (leave blank for none):",
            initialvalue=current_instructor_id
        )

        if instructor_id is None:
            return

        if course_id == "" or course_name == "":
            messagebox.showerror(
                "Error",
                "Course ID and name cannot be empty."
            )
            return

        if any(
            c is not course and c.course_id == course_id
            for c in courses
        ):
            messagebox.showerror(
                "Error",
                "Course ID already exists."
            )
            return

        new_instructor = None

        if instructor_id != "":
            new_instructor = next(
                (
                    i for i in instructors
                    if i.instructor_id == instructor_id
                ),
                None
            )

            if new_instructor is None:
                messagebox.showerror(
                    "Error",
                    "Instructor ID not found."
                )
                return

        if (
            course.instructor is not None
            and course in course.instructor.assigned_courses
        ):
            course.instructor.assigned_courses.remove(course)

        course.course_id = course_id
        course.course_name = course_name
        course.instructor = new_instructor

        if (
            new_instructor is not None
            and course not in new_instructor.assigned_courses
        ):
            new_instructor.assigned_courses.append(course)

    refresh_instructor_dropdown()
    refresh_registration_dropdowns()
    refresh_records()

    messagebox.showinfo(
        "Success",
        "Record updated successfully!"
    )


def save_records():
    try:
        save_data(
            students,
            instructors,
            courses,
            "school_data.json"
        )

        messagebox.showinfo(
            "Success",
            "Data saved successfully!"
        )

    except Exception as error:
        messagebox.showerror(
            "Error",
            str(error)
        )


def load_records():
    try:
        data = load_data("school_data.json")

        students.clear()
        instructors.clear()
        courses.clear()

        instructor_map = {}

        for item in data.get("instructors", []):
            instructor = Instructor(
                item["name"],
                item["age"],
                item["email"],
                item["instructor_id"]
            )

            instructors.append(instructor)
            instructor_map[instructor.instructor_id] = instructor

        student_map = {}

        for item in data.get("students", []):
            student = Student(
                item["name"],
                item["age"],
                item["email"],
                item["student_id"]
            )

            students.append(student)
            student_map[student.student_id] = student

        course_map = {}

        for item in data.get("courses", []):
            instructor = instructor_map.get(
                item.get("instructor")
            )

            course = Course(
                item["course_id"],
                item["course_name"],
                instructor
            )

            courses.append(course)
            course_map[course.course_id] = course

            if instructor is not None:
                instructor.assigned_courses.append(course)

        for item in data.get("students", []):
            student = student_map.get(
                item["student_id"]
            )

            for course_id in item.get(
                "registered_courses",
                []
            ):
                course = course_map.get(course_id)

                if course is not None:
                    student.registered_courses.append(course)

                    if student not in course.enrolled_students:
                        course.enrolled_students.append(student)

        refresh_instructor_dropdown()
        refresh_registration_dropdowns()
        refresh_records()

        messagebox.showinfo(
            "Success",
            "Data loaded successfully!"
        )

    except FileNotFoundError:
        messagebox.showerror(
            "Error",
            "No saved data file was found."
        )

    except Exception as error:
        messagebox.showerror(
            "Error",
            str(error)
        )

root = tk.Tk()
root.title("School Management System")
root.geometry("800x600")


title_label = tk.Label(
    root,
    text="School Management System",
    font=("Arial", 22, "bold")
)

title_label.pack(pady=15)


notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=10)


student_tab = ttk.Frame(notebook)
notebook.add(student_tab, text="Students")

student_form = ttk.Frame(student_tab)
student_form.pack(pady=20)

registration_frame = ttk.LabelFrame(
    student_tab,
    text="Course Registration"
)

registration_frame.pack(
    pady=20,
    padx=20,
    fill="x"
)


# Student dropdown
ttk.Label(
    registration_frame,
    text="Student:"
).grid(
    row=0,
    column=0,
    padx=10,
    pady=10,
    sticky="w"
)

student_registration_dropdown = ttk.Combobox(
    registration_frame,
    width=30,
    state="readonly"
)

student_registration_dropdown.grid(
    row=0,
    column=1,
    padx=10,
    pady=10
)


# Course dropdown
ttk.Label(
    registration_frame,
    text="Course:"
).grid(
    row=1,
    column=0,
    padx=10,
    pady=10,
    sticky="w"
)

course_registration_dropdown = ttk.Combobox(
    registration_frame,
    width=30,
    state="readonly"
)

course_registration_dropdown.grid(
    row=1,
    column=1,
    padx=10,
    pady=10
)


# Register button
register_button = ttk.Button(
    registration_frame,
    text="Register Student",
    command=register_student
)

register_button.grid(
    row=2,
    column=0,
    columnspan=2,
    pady=15
)

# Name
ttk.Label(
    student_form,
    text="Name:"
).grid(row=0, column=0, padx=10, pady=10, sticky="w")

student_name_entry = ttk.Entry(
    student_form,
    width=30
)
student_name_entry.grid(
    row=0,
    column=1,
    padx=10,
    pady=10
)


# Age
ttk.Label(
    student_form,
    text="Age:"
).grid(row=1, column=0, padx=10, pady=10, sticky="w")

student_age_entry = ttk.Entry(
    student_form,
    width=30
)
student_age_entry.grid(
    row=1,
    column=1,
    padx=10,
    pady=10
)


# Email
ttk.Label(
    student_form,
    text="Email:"
).grid(row=2, column=0, padx=10, pady=10, sticky="w")

student_email_entry = ttk.Entry(
    student_form,
    width=30
)
student_email_entry.grid(
    row=2,
    column=1,
    padx=10,
    pady=10
)


# Student ID
ttk.Label(
    student_form,
    text="Student ID:"
).grid(row=3, column=0, padx=10, pady=10, sticky="w")

student_id_entry = ttk.Entry(
    student_form,
    width=30
)
student_id_entry.grid(
    row=3,
    column=1,
    padx=10,
    pady=10
)


# Add Student button
add_student_button = ttk.Button(
    student_form,
    text="Add Student",
    command=add_student
)

add_student_button.grid(
    row=4,
    column=0,
    columnspan=2,
    pady=15
)

instructor_tab = ttk.Frame(notebook)
notebook.add(instructor_tab, text="Instructors")

instructor_form = ttk.Frame(instructor_tab)
instructor_form.pack(pady=20)


# Name
ttk.Label(
    instructor_form,
    text="Name:"
).grid(row=0, column=0, padx=10, pady=10, sticky="w")

instructor_name_entry = ttk.Entry(
    instructor_form,
    width=30
)
instructor_name_entry.grid(
    row=0,
    column=1,
    padx=10,
    pady=10
)


# Age
ttk.Label(
    instructor_form,
    text="Age:"
).grid(row=1, column=0, padx=10, pady=10, sticky="w")

instructor_age_entry = ttk.Entry(
    instructor_form,
    width=30
)
instructor_age_entry.grid(
    row=1,
    column=1,
    padx=10,
    pady=10
)


# Email
ttk.Label(
    instructor_form,
    text="Email:"
).grid(row=2, column=0, padx=10, pady=10, sticky="w")

instructor_email_entry = ttk.Entry(
    instructor_form,
    width=30
)
instructor_email_entry.grid(
    row=2,
    column=1,
    padx=10,
    pady=10
)


# Instructor ID
ttk.Label(
    instructor_form,
    text="Instructor ID:"
).grid(row=3, column=0, padx=10, pady=10, sticky="w")

instructor_id_entry = ttk.Entry(
    instructor_form,
    width=30
)
instructor_id_entry.grid(
    row=3,
    column=1,
    padx=10,
    pady=10
)


# Add Instructor button
add_instructor_button = ttk.Button(
    instructor_form,
    text="Add Instructor",
    command=add_instructor
)

add_instructor_button.grid(
    row=4,
    column=0,
    columnspan=2,
    pady=15
)

course_tab = ttk.Frame(notebook)
notebook.add(course_tab, text="Courses")

course_form = ttk.Frame(course_tab)
course_form.pack(pady=20)


# Course ID
ttk.Label(
    course_form,
    text="Course ID:"
).grid(
    row=0,
    column=0,
    padx=10,
    pady=10,
    sticky="w"
)

course_id_entry = ttk.Entry(
    course_form,
    width=30
)

course_id_entry.grid(
    row=0,
    column=1,
    padx=10,
    pady=10
)


# Course Name
ttk.Label(
    course_form,
    text="Course Name:"
).grid(
    row=1,
    column=0,
    padx=10,
    pady=10,
    sticky="w"
)

course_name_entry = ttk.Entry(
    course_form,
    width=30
)

course_name_entry.grid(
    row=1,
    column=1,
    padx=10,
    pady=10
)


# Instructor dropdown
ttk.Label(
    course_form,
    text="Instructor:"
).grid(
    row=2,
    column=0,
    padx=10,
    pady=10,
    sticky="w"
)

instructor_dropdown = ttk.Combobox(
    course_form,
    width=27,
    state="readonly"
)

instructor_dropdown.grid(
    row=2,
    column=1,
    padx=10,
    pady=10
)


# Add Course button
add_course_button = ttk.Button(
    course_form,
    text="Add Course",
    command=add_course
)

add_course_button.grid(
    row=3,
    column=0,
    columnspan=2,
    pady=15
)

records_tab = ttk.Frame(notebook)
notebook.add(records_tab, text="Records")

# Search area
search_frame = ttk.Frame(records_tab)
search_frame.pack(pady=10)


ttk.Label(
    search_frame,
    text="Search:"
).grid(
    row=0,
    column=0,
    padx=5
)


search_entry = ttk.Entry(
    search_frame,
    width=30
)

search_entry.grid(
    row=0,
    column=1,
    padx=5
)


search_button = ttk.Button(
    search_frame,
    text="Search",
    command=search_records
)

search_button.grid(
    row=0,
    column=2,
    padx=5
)


show_all_button = ttk.Button(
    search_frame,
    text="Show All",
    command=show_all_records
)

show_all_button.grid(
    row=0,
    column=3,
    padx=5
)

# Records table
columns = (
    "type",
    "id",
    "name",
    "details"
)

records_tree = ttk.Treeview(
    records_tab,
    columns=columns,
    show="headings",
    height=15
)


records_tree.heading(
    "type",
    text="Type"
)

records_tree.heading(
    "id",
    text="ID"
)

records_tree.heading(
    "name",
    text="Name"
)

records_tree.heading(
    "details",
    text="Details"
)


records_tree.column(
    "type",
    width=100
)

records_tree.column(
    "id",
    width=120
)

records_tree.column(
    "name",
    width=180
)

records_tree.column(
    "details",
    width=300
)


records_tree.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)

record_buttons = ttk.Frame(records_tab)
record_buttons.pack(pady=10)


edit_button = ttk.Button(
    record_buttons,
    text="Edit Selected",
    command=edit_record
)

edit_button.grid(
    row=0,
    column=0,
    padx=5
)


delete_button = ttk.Button(
    record_buttons,
    text="Delete Selected",
    command=delete_record
)

delete_button.grid(
    row=0,
    column=1,
    padx=5
)


save_button = ttk.Button(
    record_buttons,
    text="Save Data",
    command=save_records
)

save_button.grid(
    row=0,
    column=2,
    padx=5
)


load_button = ttk.Button(
    record_buttons,
    text="Load Data",
    command=load_records
)

load_button.grid(
    row=0,
    column=3,
    padx=5
)



root.mainloop()