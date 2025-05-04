from fastapi import FastAPI, Path, Query
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

students = {
    1: {"name": "John", "age": 20, "enrolled": True},
    2: {"name": "Jane", "age": 22, "enrolled": False},
    3: {"name": "Doe", "age": 21, "enrolled": True},
    4: {"name": "Alice", "age": 23, "enrolled": True},
    5: {"name": "Bob", "age": 24, "enrolled": False},
    6: {"name": "Charlie", "age": 25, "enrolled": True},
}

class Student(BaseModel):
    name: str
    age: int
    enrolled: bool

class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    enrolled: Optional[bool] = None


@app.get("/")
def index():
    return {"name": "FastAPI", "version": "0.1"}

@app.get("/get-student/{student_id}")
def get_student(student_id: int = Path(..., title="Student ID", description="ID of the student to retrieve",)):
    """
    Retrieve a student's information by their ID.

    Args:
        student_id (int): The ID of the student to retrieve. This is a required path parameter.

    Returns:
        dict: A dictionary containing the student's information if found.
              If the student is not found, returns a dictionary with an error message.
    """
    try:
        student = students[student_id]
    except KeyError:
        return {"error": "Student not found"}
    return student


@app.get("/get-student-by-name")
def get_student_by_name(name: Optional[str] = Query(None, title="Name", description="Name of the student to retrieve")):
    """
    Retrieve a student's information by their name.

    Args:
        name (str): The name of the student to retrieve. This is a required query parameter.

    Returns:
        dict: A dictionary containing the student's information if found.
              If the student is not found, returns a dictionary with an error message.
    """
    for student_id, student in students.items():
        if student["name"] == name:
            return {student_id: student}
    return {"error": "Student not found"}



@app.get("/get-all-students")
def get_all_students():
    return students

@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: Student):
    """
    Create a new student with the given ID and information.

    Args:
        student_id (int): The ID of the student to create. This is a required path parameter.
        student (Student): The information of the student to create. This is a required body parameter.

    Returns:
        dict: A dictionary containing the created student's information.
              If the student ID already exists, returns a dictionary with an error message.
    """
    if student_id in students:
        return {"error": "Student ID already exists"}
    students[student_id] = student.dict()
    return students[student_id]


@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    """
    Update an existing student's information by their ID.

    Args:
        student_id (int): The ID of the student to update. This is a required path parameter.
        student (UpdateStudent): The updated information of the student. This is a required body parameter.

    Returns:
        dict: A dictionary containing the updated student's information.
              If the student ID does not exist, returns a dictionary with an error message.
    """
    if student_id not in students:
        return {"error": "Student not found"}
    
    existing_student = students[student_id]
    updated_data = student.dict(exclude_unset=True)
    existing_student.update(updated_data)
    students[student_id] = existing_student
    return students[student_id]