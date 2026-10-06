import re
import json

class Person:
    def __init__(self, name, age, email):
        if age < 0:
            raise ValueError("Age cannot be negative.")

        if not self.valid_email(email):
            raise ValueError("Invalid email format.")

        self.name = name
        self.age = age
        self._email = email

    def introduce(self):
        return f"My name is {self.name}, I am {self.age} years old."

    def valid_email(self, email):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email) is not None

class Student(Person):
    def __init__(self, name, age, email, student_id):
        super().__init__(name, age, email)
        self.student_id = student_id
        self.registered_courses = []

    def register_course(self, course):
        self.registered_courses.append(course)


class Instructor(Person):
    def __init__(self, name, age, email, instructor_id):
        super().__init__(name, age, email)
        self.instructor_id = instructor_id
        self.assigned_courses = []

    def assign_course(self, course):
        self.assigned_courses.append(course)


class Course:
    def __init__(self, course_id, course_name, instructor=None):
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        self.enrolled_students = []

    def add_student(self, student):
        self.enrolled_students.append(student)


def save_data(students, instructors, courses, filename="school_data.json"):
    data = {
        "students": [
            {
                "name": student.name,
                "age": student.age,
                "email": student._email,
                "student_id": student.student_id,
                "registered_courses": [
                    course.course_id for course in student.registered_courses
                ]
            }
            for student in students
        ],

        "instructors": [
            {
                "name": instructor.name,
                "age": instructor.age,
                "email": instructor._email,
                "instructor_id": instructor.instructor_id,
                "assigned_courses": [
                    course.course_id for course in instructor.assigned_courses
                ]
            }
            for instructor in instructors
        ],

        "courses": [
            {
                "course_id": course.course_id,
                "course_name": course.course_name,
                "instructor": (
                    course.instructor.instructor_id
                    if course.instructor
                    else None
                ),
                "enrolled_students": [
                    student.student_id for student in course.enrolled_students
                ]
            }
            for course in courses
        ]
    }

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def load_data(filename="school_data.json"):
    with open(filename, "r") as file:
        return json.load(file)

if __name__ == "__main__":  
    student1 = Student(
        "Hussein",
        22,
        "hmc16@mail.edu.lb",
        "202207578"
    )

    instructor1 = Instructor(
        "Hussein 2",
        22,
        "hmc16@mail.edu.lb",
        "XXXX"
    )

    course1 = Course(
        "EECE435L",
        "Software Tools Lab",
        instructor1
    )


    student1.register_course(course1)
    course1.add_student(student1)
    instructor1.assign_course(course1)

    save_data(
        [student1],
        [instructor1],
        [course1]
    )


    loaded_data = load_data()

