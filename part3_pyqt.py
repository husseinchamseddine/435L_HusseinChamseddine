"""
PyQt5 School Management System.

This module implements a graphical school management system using PyQt5.
It supports management of students, instructors, courses, course
registration, searching, editing, deleting, saving, loading, and CSV export.
"""

import sys
import csv

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QTabWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QFileDialog,
    QInputDialog,
    QGroupBox,
    QAbstractItemView
)

from part1_oop import Student, Instructor, Course, save_data, load_data


class SchoolManagementSystem(QMainWindow):
    """
    Main window for the School Management System.

    The application provides PyQt5 interfaces for managing students,
    instructors, courses, registrations, and stored records.
    """

    def __init__(self):
        """Initialize the School Management System window and application data."""

        super().__init__()

        self.students = []
        self.instructors = []
        self.courses = []

        self.setWindowTitle("School Management System")
        self.resize(950, 650)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.create_student_tab()
        self.create_instructor_tab()
        self.create_course_tab()
        self.create_records_tab()

    def create_student_tab(self):
        """Create the student management and course registration interface."""

        self.student_tab = QWidget()
        self.tabs.addTab(self.student_tab, "Students")

        layout = QVBoxLayout()

        form = QFormLayout()

        self.student_name = QLineEdit()
        self.student_age = QLineEdit()
        self.student_email = QLineEdit()
        self.student_id = QLineEdit()

        form.addRow("Name:", self.student_name)
        form.addRow("Age:", self.student_age)
        form.addRow("Email:", self.student_email)
        form.addRow("Student ID:", self.student_id)

        add_button = QPushButton("Add Student")
        add_button.clicked.connect(self.add_student)

        layout.addLayout(form)
        layout.addWidget(add_button)

        registration_group = QGroupBox("Course Registration")
        registration_layout = QFormLayout()

        self.registration_student = QComboBox()
        self.registration_course = QComboBox()

        registration_layout.addRow(
            "Student:",
            self.registration_student
        )

        registration_layout.addRow(
            "Course:",
            self.registration_course
        )

        register_button = QPushButton("Register Student")
        register_button.clicked.connect(self.register_student)

        registration_layout.addRow(register_button)

        registration_group.setLayout(registration_layout)

        layout.addWidget(registration_group)
        layout.addStretch()

        self.student_tab.setLayout(layout)

    def create_instructor_tab(self):
        """Create the instructor management and course assignment interface."""

        self.instructor_tab = QWidget()
        self.tabs.addTab(self.instructor_tab, "Instructors")

        layout = QVBoxLayout()

        form = QFormLayout()

        self.instructor_name = QLineEdit()
        self.instructor_age = QLineEdit()
        self.instructor_email = QLineEdit()
        self.instructor_id = QLineEdit()

        form.addRow("Name:", self.instructor_name)
        form.addRow("Age:", self.instructor_age)
        form.addRow("Email:", self.instructor_email)
        form.addRow("Instructor ID:", self.instructor_id)

        add_button = QPushButton("Add Instructor")
        add_button.clicked.connect(self.add_instructor)

        layout.addLayout(form)
        layout.addWidget(add_button)

        assignment_group = QGroupBox("Course Assignment")
        assignment_layout = QFormLayout()

        self.assignment_instructor = QComboBox()
        self.assignment_course = QComboBox()

        assignment_layout.addRow(
            "Instructor:",
            self.assignment_instructor
        )

        assignment_layout.addRow(
            "Course:",
            self.assignment_course
        )

        assign_button = QPushButton("Assign Course")
        assign_button.clicked.connect(self.assign_course)

        assignment_layout.addRow(assign_button)

        assignment_group.setLayout(assignment_layout)

        layout.addWidget(assignment_group)
        layout.addStretch()

        self.instructor_tab.setLayout(layout)

    def create_course_tab(self):
        """Create the course management interface."""

        self.course_tab = QWidget()
        self.tabs.addTab(self.course_tab, "Courses")

        layout = QVBoxLayout()

        form = QFormLayout()

        self.course_id = QLineEdit()
        self.course_name = QLineEdit()

        form.addRow("Course ID:", self.course_id)
        form.addRow("Course Name:", self.course_name)

        add_button = QPushButton("Add Course")
        add_button.clicked.connect(self.add_course)

        layout.addLayout(form)
        layout.addWidget(add_button)
        layout.addStretch()

        self.course_tab.setLayout(layout)

    def create_records_tab(self):
        """Create the records table, search controls, and record actions."""

        self.records_tab = QWidget()
        self.tabs.addTab(self.records_tab, "Records")

        layout = QVBoxLayout()

        search_layout = QHBoxLayout()

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText(
            "Search by name, ID, or course"
        )

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_records)

        show_all_button = QPushButton("Show All")
        show_all_button.clicked.connect(self.show_all_records)

        search_layout.addWidget(self.search_box)
        search_layout.addWidget(search_button)
        search_layout.addWidget(show_all_button)

        layout.addLayout(search_layout)

        self.records_table = QTableWidget()
        self.records_table.setColumnCount(4)

        self.records_table.setHorizontalHeaderLabels(
            ["Type", "ID", "Name", "Details"]
        )

        self.records_table.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        self.records_table.setSelectionMode(
            QAbstractItemView.SingleSelection
        )

        self.records_table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        self.records_table.setColumnWidth(0, 110)
        self.records_table.setColumnWidth(1, 140)
        self.records_table.setColumnWidth(2, 220)
        self.records_table.setColumnWidth(3, 350)

        layout.addWidget(self.records_table)

        buttons = QHBoxLayout()

        edit_button = QPushButton("Edit Selected")
        edit_button.clicked.connect(self.edit_record)

        delete_button = QPushButton("Delete Selected")
        delete_button.clicked.connect(self.delete_record)

        save_button = QPushButton("Save Data")
        save_button.clicked.connect(self.save_records)

        load_button = QPushButton("Load Data")
        load_button.clicked.connect(self.load_records)

        export_button = QPushButton("Export CSV")
        export_button.clicked.connect(self.export_csv)

        buttons.addWidget(edit_button)
        buttons.addWidget(delete_button)
        buttons.addWidget(save_button)
        buttons.addWidget(load_button)
        buttons.addWidget(export_button)

        layout.addLayout(buttons)

        self.records_tab.setLayout(layout)

    def refresh_dropdowns(self):
        """Refresh student, instructor, and course dropdown values."""

        self.registration_student.clear()
        self.registration_course.clear()
        self.assignment_instructor.clear()
        self.assignment_course.clear()

        self.registration_student.addItem(
            "Select Student",
            None
        )

        self.registration_course.addItem(
            "Select Course",
            None
        )

        self.assignment_instructor.addItem(
            "Select Instructor",
            None
        )

        self.assignment_course.addItem(
            "Select Course",
            None
        )

        for student in self.students:
            self.registration_student.addItem(
                f"{student.student_id} - {student.name}",
                student
            )

        for instructor in self.instructors:
            self.assignment_instructor.addItem(
                f"{instructor.instructor_id} - {instructor.name}",
                instructor
            )

        for course in self.courses:
            text = f"{course.course_id} - {course.course_name}"

            self.registration_course.addItem(
                text,
                course
            )

            self.assignment_course.addItem(
                text,
                course
            )

    def add_student(self):
        """Validate input and add a new student."""

        try:
            name = self.student_name.text().strip()
            email = self.student_email.text().strip()
            student_id = self.student_id.text().strip()

            if (
                name == ""
                or self.student_age.text().strip() == ""
                or email == ""
                or student_id == ""
            ):
                QMessageBox.warning(
                    self,
                    "Error",
                    "Please fill in all fields."
                )
                return

            age = int(self.student_age.text())

            if any(
                student.student_id == student_id
                for student in self.students
            ):
                QMessageBox.warning(
                    self,
                    "Error",
                    "Student ID already exists."
                )
                return

            student = Student(
                name,
                age,
                email,
                student_id
            )

            self.students.append(student)

            self.student_name.clear()
            self.student_age.clear()
            self.student_email.clear()
            self.student_id.clear()

            self.refresh_dropdowns()
            self.refresh_records()

            QMessageBox.information(
                self,
                "Success",
                "Student added successfully!"
            )

        except ValueError as error:
            QMessageBox.warning(
                self,
                "Invalid Input",
                str(error)
            )

    def add_instructor(self):
        """Validate input and add a new instructor."""

        try:
            name = self.instructor_name.text().strip()
            email = self.instructor_email.text().strip()
            instructor_id = self.instructor_id.text().strip()

            if (
                name == ""
                or self.instructor_age.text().strip() == ""
                or email == ""
                or instructor_id == ""
            ):
                QMessageBox.warning(
                    self,
                    "Error",
                    "Please fill in all fields."
                )
                return

            age = int(self.instructor_age.text())

            if any(
                instructor.instructor_id == instructor_id
                for instructor in self.instructors
            ):
                QMessageBox.warning(
                    self,
                    "Error",
                    "Instructor ID already exists."
                )
                return

            instructor = Instructor(
                name,
                age,
                email,
                instructor_id
            )

            self.instructors.append(instructor)

            self.instructor_name.clear()
            self.instructor_age.clear()
            self.instructor_email.clear()
            self.instructor_id.clear()

            self.refresh_dropdowns()
            self.refresh_records()

            QMessageBox.information(
                self,
                "Success",
                "Instructor added successfully!"
            )

        except ValueError as error:
            QMessageBox.warning(
                self,
                "Invalid Input",
                str(error)
            )

    def add_course(self):
        """Create and add a new course."""

        course_id = self.course_id.text().strip()
        course_name = self.course_name.text().strip()

        if course_id == "" or course_name == "":
            QMessageBox.warning(
                self,
                "Error",
                "Please fill in all course fields."
            )
            return

        if any(
            course.course_id == course_id
            for course in self.courses
        ):
            QMessageBox.warning(
                self,
                "Error",
                "Course ID already exists."
            )
            return

        course = Course(
            course_id,
            course_name
        )

        self.courses.append(course)

        self.course_id.clear()
        self.course_name.clear()

        self.refresh_dropdowns()
        self.refresh_records()

        QMessageBox.information(
            self,
            "Success",
            "Course added successfully!"
        )

    def register_student(self):
        """Register the selected student in the selected course."""

        student = self.registration_student.currentData()
        course = self.registration_course.currentData()

        if student is None or course is None:
            QMessageBox.warning(
                self,
                "Error",
                "Please select a student and course."
            )
            return

        if course in student.registered_courses:
            QMessageBox.warning(
                self,
                "Error",
                "Student is already registered in this course."
            )
            return

        student.register_course(course)
        course.add_student(student)

        self.refresh_records()

        QMessageBox.information(
            self,
            "Success",
            "Student registered successfully!"
        )

    def assign_course(self):
        """Assign the selected course to the selected instructor."""

        instructor = self.assignment_instructor.currentData()
        course = self.assignment_course.currentData()

        if instructor is None or course is None:
            QMessageBox.warning(
                self,
                "Error",
                "Please select an instructor and course."
            )
            return

        if course.instructor is instructor:
            QMessageBox.warning(
                self,
                "Error",
                "This course is already assigned to this instructor."
            )
            return

        if course.instructor is not None:
            old_instructor = course.instructor

            if course in old_instructor.assigned_courses:
                old_instructor.assigned_courses.remove(course)

        course.instructor = instructor

        if course not in instructor.assigned_courses:
            instructor.assign_course(course)

        self.refresh_records()

        QMessageBox.information(
            self,
            "Success",
            "Course assigned successfully!"
        )

    def refresh_records(self, search_text=""):
        """
        Refresh the records table.

        :param search_text: Optional text used to filter displayed records.
        :type search_text: str
        """

        self.records_table.setRowCount(0)

        search_text = search_text.lower()

        records = []

        for student in self.students:
            courses = ", ".join(
                course.course_id
                for course in student.registered_courses
            )

            records.append(
                (
                    "Student",
                    student.student_id,
                    student.name,
                    f"Courses: {courses if courses else 'None'}"
                )
            )

        for instructor in self.instructors:
            courses = ", ".join(
                course.course_id
                for course in instructor.assigned_courses
            )

            records.append(
                (
                    "Instructor",
                    instructor.instructor_id,
                    instructor.name,
                    f"Courses: {courses if courses else 'None'}"
                )
            )

        for course in self.courses:
            instructor_name = (
                course.instructor.name
                if course.instructor is not None
                else "None"
            )

            records.append(
                (
                    "Course",
                    course.course_id,
                    course.course_name,
                    f"Instructor: {instructor_name}"
                )
            )

        for record in records:
            combined = " ".join(record).lower()

            if search_text == "" or search_text in combined:
                row = self.records_table.rowCount()

                self.records_table.insertRow(row)

                for column, value in enumerate(record):
                    self.records_table.setItem(
                        row,
                        column,
                        QTableWidgetItem(value)
                    )

    def search_records(self):
        """Search records using the text entered by the user."""

        self.refresh_records(
            self.search_box.text().strip()
        )

    def show_all_records(self):
        """Clear the search filter and display all records."""

        self.search_box.clear()
        self.refresh_records()

    def edit_record(self):
        """Edit the currently selected record."""

        row = self.records_table.currentRow()

        if row < 0:
            QMessageBox.warning(
                self,
                "Error",
                "Please select a record."
            )
            return

        record_type = self.records_table.item(row, 0).text()
        record_id = self.records_table.item(row, 1).text()

        if record_type == "Student":
            student = next(
                (
                    student
                    for student in self.students
                    if student.student_id == record_id
                ),
                None
            )

            if student is None:
                return

            name, ok = QInputDialog.getText(
                self,
                "Edit Student",
                "Name:",
                text=student.name
            )

            if not ok:
                return

            age, ok = QInputDialog.getInt(
                self,
                "Edit Student",
                "Age:",
                student.age,
                0,
                150
            )

            if not ok:
                return

            email, ok = QInputDialog.getText(
                self,
                "Edit Student",
                "Email:",
                text=student._email
            )

            if not ok:
                return

            student_id, ok = QInputDialog.getText(
                self,
                "Edit Student",
                "Student ID:",
                text=student.student_id
            )

            if not ok:
                return

            if (
                name.strip() == ""
                or email.strip() == ""
                or student_id.strip() == ""
            ):
                QMessageBox.warning(
                    self,
                    "Error",
                    "Fields cannot be empty."
                )
                return

            if not student.valid_email(email):
                QMessageBox.warning(
                    self,
                    "Error",
                    "Invalid email format."
                )
                return

            if any(
                other is not student
                and other.student_id == student_id
                for other in self.students
            ):
                QMessageBox.warning(
                    self,
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
                (
                    instructor
                    for instructor in self.instructors
                    if instructor.instructor_id == record_id
                ),
                None
            )

            if instructor is None:
                return

            name, ok = QInputDialog.getText(
                self,
                "Edit Instructor",
                "Name:",
                text=instructor.name
            )

            if not ok:
                return

            age, ok = QInputDialog.getInt(
                self,
                "Edit Instructor",
                "Age:",
                instructor.age,
                0,
                150
            )

            if not ok:
                return

            email, ok = QInputDialog.getText(
                self,
                "Edit Instructor",
                "Email:",
                text=instructor._email
            )

            if not ok:
                return

            instructor_id, ok = QInputDialog.getText(
                self,
                "Edit Instructor",
                "Instructor ID:",
                text=instructor.instructor_id
            )

            if not ok:
                return

            if (
                name.strip() == ""
                or email.strip() == ""
                or instructor_id.strip() == ""
            ):
                QMessageBox.warning(
                    self,
                    "Error",
                    "Fields cannot be empty."
                )
                return

            if not instructor.valid_email(email):
                QMessageBox.warning(
                    self,
                    "Error",
                    "Invalid email format."
                )
                return

            if any(
                other is not instructor
                and other.instructor_id == instructor_id
                for other in self.instructors
            ):
                QMessageBox.warning(
                    self,
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
                (
                    course
                    for course in self.courses
                    if course.course_id == record_id
                ),
                None
            )

            if course is None:
                return

            course_id, ok = QInputDialog.getText(
                self,
                "Edit Course",
                "Course ID:",
                text=course.course_id
            )

            if not ok:
                return

            course_name, ok = QInputDialog.getText(
                self,
                "Edit Course",
                "Course Name:",
                text=course.course_name
            )

            if not ok:
                return

            if (
                course_id.strip() == ""
                or course_name.strip() == ""
            ):
                QMessageBox.warning(
                    self,
                    "Error",
                    "Fields cannot be empty."
                )
                return

            if any(
                other is not course
                and other.course_id == course_id
                for other in self.courses
            ):
                QMessageBox.warning(
                    self,
                    "Error",
                    "Course ID already exists."
                )
                return

            course.course_id = course_id
            course.course_name = course_name

        self.refresh_dropdowns()
        self.refresh_records()

        QMessageBox.information(
            self,
            "Success",
            "Record updated successfully!"
        )

    def delete_record(self):
        """Delete the currently selected record."""

        row = self.records_table.currentRow()

        if row < 0:
            QMessageBox.warning(
                self,
                "Error",
                "Please select a record."
            )
            return

        record_type = self.records_table.item(row, 0).text()
        record_id = self.records_table.item(row, 1).text()

        confirm = QMessageBox.question(
            self,
            "Delete Record",
            "Are you sure you want to delete this record?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm != QMessageBox.Yes:
            return

        if record_type == "Student":
            student = next(
                (
                    student
                    for student in self.students
                    if student.student_id == record_id
                ),
                None
            )

            if student:
                for course in list(student.registered_courses):
                    if student in course.enrolled_students:
                        course.enrolled_students.remove(student)

                self.students.remove(student)

        elif record_type == "Instructor":
            instructor = next(
                (
                    instructor
                    for instructor in self.instructors
                    if instructor.instructor_id == record_id
                ),
                None
            )

            if instructor:
                for course in list(instructor.assigned_courses):
                    course.instructor = None

                self.instructors.remove(instructor)

        elif record_type == "Course":
            course = next(
                (
                    course
                    for course in self.courses
                    if course.course_id == record_id
                ),
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

                self.courses.remove(course)

        self.refresh_dropdowns()
        self.refresh_records()

        QMessageBox.information(
            self,
            "Success",
            "Record deleted successfully!"
        )

    def save_records(self):
        """Save application records to a JSON file."""

        try:
            save_data(
                self.students,
                self.instructors,
                self.courses,
                "school_data_pyqt.json"
            )

            QMessageBox.information(
                self,
                "Success",
                "Data saved successfully!"
            )

        except Exception as error:
            QMessageBox.warning(
                self,
                "Error",
                str(error)
            )

    def load_records(self):
        """Load previously saved application records."""

        try:
            data = load_data(
                "school_data_pyqt.json"
            )

            self.students.clear()
            self.instructors.clear()
            self.courses.clear()

            instructor_map = {}
            student_map = {}
            course_map = {}

            for item in data.get("instructors", []):
                instructor = Instructor(
                    item["name"],
                    item["age"],
                    item["email"],
                    item["instructor_id"]
                )

                self.instructors.append(instructor)

                instructor_map[
                    instructor.instructor_id
                ] = instructor

            for item in data.get("students", []):
                student = Student(
                    item["name"],
                    item["age"],
                    item["email"],
                    item["student_id"]
                )

                self.students.append(student)

                student_map[
                    student.student_id
                ] = student

            for item in data.get("courses", []):
                instructor = instructor_map.get(
                    item.get("instructor")
                )

                course = Course(
                    item["course_id"],
                    item["course_name"],
                    instructor
                )

                self.courses.append(course)

                course_map[
                    course.course_id
                ] = course

                if instructor is not None:
                    instructor.assigned_courses.append(
                        course
                    )

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
                        student.registered_courses.append(
                            course
                        )

                        if student not in course.enrolled_students:
                            course.enrolled_students.append(
                                student
                            )

            self.refresh_dropdowns()
            self.refresh_records()

            QMessageBox.information(
                self,
                "Success",
                "Data loaded successfully!"
            )

        except FileNotFoundError:
            QMessageBox.warning(
                self,
                "Error",
                "No saved data file was found."
            )

        except Exception as error:
            QMessageBox.warning(
                self,
                "Error",
                str(error)
            )

    def export_csv(self):
        """Export the displayed records to a CSV file."""

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export CSV",
            "school_records.csv",
            "CSV Files (*.csv)"
        )

        if filename == "":
            return

        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow(
                ["Type", "ID", "Name", "Details"]
            )

            for row in range(
                self.records_table.rowCount()
            ):
                writer.writerow(
                    [
                        self.records_table.item(
                            row,
                            column
                        ).text()
                        for column in range(4)
                    ]
                )

        QMessageBox.information(
            self,
            "Success",
            "CSV exported successfully!"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = SchoolManagementSystem()
    window.show()

    sys.exit(app.exec_())