from fastapi import FastAPI, Path, Query
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

students = {
    1: {"name": "John", "age": 20},
    2: {"name": "Jane", "age": 22},
    3: {"name": "Doe", "age": 21}
}

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
