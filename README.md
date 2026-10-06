# Lab 4 - Git and GitHub

## Hussein Chamseddine

This project contains two graphical implementations of the School Management System developed in Lab 2: one using Tkinter and one using PyQt5.

## Files

- `part1_oop.py` - Contains the Student, Instructor, and Course classes used by both interfaces.
- `part2_tkinter.py` - Implements the School Management System using Tkinter.
- `part3_pyqt.py` - Implements the School Management System using PyQt5.

## How to Run

### Tkinter Version

The Tkinter version provides a graphical interface for managing students, instructors, and courses.

Run the Tkinter application with:

```bash
python3 part2_tkinter.py
```

The Tkinter interface allows the user to:

- Add students, instructors, and courses.
- Register students in courses.
- Assign instructors to courses.
- View and search records.
- Edit and delete records.
- Save and load application data.

### PyQt5 Version

The PyQt5 version provides the same School Management System functionality using the PyQt5 framework.

If PyQt5 is not installed, install it with:

```bash
pip3 install PyQt5
```

Then run the PyQt5 application with:

```bash
python3 part3_pyqt.py
```

The PyQt5 interface allows the user to:

- Add students, instructors, and courses.
- Register students in courses.
- Assign instructors to courses.
- View and search records.
- Edit and delete records.
- Save and load application data.
- Export records to CSV.

## How Tkinter and PyQt Are Used

Tkinter and PyQt5 are used to provide two different graphical user interfaces for the same School Management System.

The Tkinter version uses Python's Tkinter library to create forms, buttons, dropdown menus, and record tables.

The PyQt5 version uses Qt widgets such as `QLineEdit`, `QComboBox`, `QTableWidget`, and `QPushButton` to provide an alternative graphical interface.

Both interfaces use the object-oriented classes defined in `part1_oop.py`.
