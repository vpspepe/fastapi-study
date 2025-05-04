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
def get_student(student_id: int = Path(..., title="Student ID", description="ID do estudante a ser recuperado")):
    """
    Recupera as informações de um estudante pelo seu ID.

    Args:
        student_id (int): O ID do estudante a ser recuperado. Este é um parâmetro de caminho obrigatório.

    Retorna:
        dict: Um dicionário contendo as informações do estudante, se encontrado.
              Se o estudante não for encontrado, retorna um dicionário com uma mensagem de erro.
    """
    try:
        student = students[student_id]
    except KeyError:
        return {"error": "Estudante não encontrado"}
    return student


@app.get("/get-student-by-name")
def get_student_by_name(name: Optional[str] = Query(None, title="Name", description="Nome do estudante a ser recuperado")):
    """
    Recupera as informações de um estudante pelo seu nome.

    Args:
        name (str): O nome do estudante a ser recuperado. Este é um parâmetro de consulta obrigatório.

    Retorna:
        dict: Um dicionário contendo as informações do estudante, se encontrado.
              Se o estudante não for encontrado, retorna um dicionário com uma mensagem de erro.
    """
    for student_id, student in students.items():
        if student["name"] == name:
            return {student_id: student}
    return {"error": "Estudante não encontrado"}



@app.get("/get-all-students")
def get_all_students():
    return students

@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: Student):
    """
    Cria um novo estudante com o ID e as informações fornecidas.

    Args:
        student_id (int): O ID do estudante a ser criado. Este é um parâmetro de caminho obrigatório.
        student (Student): As informações do estudante a ser criado. Este é um parâmetro de corpo obrigatório.

    Retorna:
        dict: Um dicionário contendo as informações do estudante criado.
              Se o ID do estudante já existir, retorna um dicionário com uma mensagem de erro.
    """
    if student_id in students:
        return {"error": "ID do estudante já existe"}
    students[student_id] = student.dict()
    return students[student_id]


@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    """
    Atualiza as informações de um estudante existente pelo seu ID.

    Args:
        student_id (int): O ID do estudante a ser atualizado. Este é um parâmetro de caminho obrigatório.
        student (UpdateStudent): As informações atualizadas do estudante. Este é um parâmetro de corpo obrigatório.

    Retorna:
        dict: Um dicionário contendo as informações atualizadas do estudante.
              Se o ID do estudante não existir, retorna um dicionário com uma mensagem de erro.
    """
    if student_id not in students:
        return {"error": "Estudante não encontrado"}
    
    existing_student = students[student_id]
    updated_data = student.dict(exclude_unset=True)
    existing_student.update(updated_data)
    students[student_id] = existing_student
    return students[student_id]

@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    """
    Exclui um estudante pelo seu ID.

    Args:
        student_id (int): O ID do estudante a ser excluído. Este é um parâmetro de caminho obrigatório.

    Retorna:
        dict: Um dicionário contendo uma mensagem de sucesso se o estudante foi excluído.
              Se o ID do estudante não existir, retorna um dicionário com uma mensagem de erro.
    """
    if student_id not in students:
        return {"error": "Estudante não encontrado"}
    
    del students[student_id]
    return {"message": "Estudante excluído com sucesso"}