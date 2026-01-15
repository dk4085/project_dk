from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas
from ..database import get_db

router = APIRouter()

# Эндпоинты для студентов
@router.post("/students/", response_model=schemas.Student, tags=["Студенты"])
def create_student_endpoint(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    """
    Создать нового студента.
    """
    return crud.create_student(db=db, student=student)

@router.get("/students/{student_id}", response_model=schemas.Student, tags=["Студенты"])
def read_student(student_id: int, db: Session = Depends(get_db)):
    """
    Получить информацию о студенте по его ID.
    """
    db_student = crud.get_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Студент не найден")
    return db_student

@router.get("/students/", response_model=List[schemas.Student], tags=["Студенты"])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получить список студентов.
    """
    students = crud.get_students(db, skip=skip, limit=limit)
    return students

@router.delete("/students/{student_id}", response_model=schemas.Student, tags=["Студенты"])
def delete_student_endpoint(student_id: int, db: Session = Depends(get_db)):
    """
    Удалить студента.
    """
    db_student = crud.delete_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Студент не найден")
    return db_student

# Эндпоинты для групп
@router.post("/groups/", response_model=schemas.Group, tags=["Группы"])
def create_group_endpoint(group: schemas.GroupCreate, db: Session = Depends(get_db)):
    """
    Создать новую группу.
    """
    return crud.create_group(db=db, group=group)

@router.get("/groups/{group_id}", response_model=schemas.GroupWithStudents, tags=["Группы"])
def read_group(group_id: int, db: Session = Depends(get_db)):
    """
    Получить информацию о группе по ее ID.
    """
    db_group = crud.get_group(db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Группа не найден")
    return db_group

@router.get("/groups/", response_model=List[schemas.Group], tags=["Группы"])
def read_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получить список групп.
    """
    groups = crud.get_groups(db, skip=skip, limit=limit)
    return groups

@router.delete("/groups/{group_id}", response_model=schemas.Group, tags=["Группы"])
def delete_group_endpoint(group_id: int, db: Session = Depends(get_db)):
    """
    Удалить группу.
    """
    db_group = crud.delete_group(db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Группа не найден")
    return db_group

@router.get("/groups/{group_id}/students", response_model=List[schemas.Student], tags=["Группы"])
def read_students_in_group(group_id: int, db: Session = Depends(get_db)):
    """
    Получить всех студентов в группе.
    """
    # Проверяем существование группы
    group = crud.get_group(db, group_id=group_id)
    if group is None:
        raise HTTPException(status_code=404, detail="Группа не найден")
    
    return crud.get_students_in_group(db, group_id=group_id)

# Эндпоинты для операций со студентами и группами
@router.post("/groups/{group_id}/students/{student_id}", response_model=schemas.Student, tags=["Операции"])
def add_student_to_group_endpoint(group_id: int, student_id: int, db: Session = Depends(get_db)):
    """
    Добавить студента в группу.
    """
    db_student = crud.add_student_to_group(db, student_id=student_id, group_id=group_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Студент или группа не найден")
    return db_student

@router.delete("/students/{student_id}/group", response_model=schemas.Student, tags=["Операции"])
def remove_student_from_group_endpoint(student_id: int, db: Session = Depends(get_db)):
    """
    Удалить студента из группы.
    """
    db_student = crud.remove_student_from_group(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Студент не найден")
    return db_student

@router.put("/students/{student_id}/transfer", response_model=schemas.Student, tags=["Операции"])
def transfer_student_endpoint(
    student_id: int, 
    transfer_data: schemas.TransferStudent,
    db: Session = Depends(get_db)
):
    """
    Перевести студента из группы A в группу B.
    """
    db_student = crud.transfer_student(
        db, 
        student_id=student_id,
        from_group_id=transfer_data.from_group_id,
        to_group_id=transfer_data.to_group_id
    )
    if db_student is None:
        raise HTTPException(
            status_code=404, 
            detail="Студент или группы не найдены, либо студент не состоит в указанной группе"
        )
    return db_student