from sqlalchemy.orm import Session
from . import models, schemas

# CRUD операции для студентов
def get_student(db: Session, student_id: int):
    """
    Получить студента по ID.
    
    Args:
        db: Сессия базы данных
        student_id: ID студента
        
    Returns:
        Объект студента или None
    """
    return db.query(models.Student).filter(models.Student.id == student_id).first()

def get_students(db: Session, skip: int = 0, limit: int = 100):
    """
    Получить список студентов.
    
    Args:
        db: Сессия базы данных
        skip: Количество записей для пропуска
        limit: Максимальное количество записей
        
    Returns:
        Список студентов
    """
    return db.query(models.Student).offset(skip).limit(limit).all()

def create_student(db: Session, student: schemas.StudentCreate):
    """
    Создать нового студента.
    
    Args:
        db: Сессия базы данных
        student: Данные студента
        
    Returns:
        Созданный студент
    """
    db_student = models.Student(
        first_name=student.first_name,
        last_name=student.last_name,
        age=student.age,
        group_id=student.group_id
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def update_student(db: Session, student_id: int, student_update: schemas.StudentUpdate):
    """
    Обновить данные студента.
    
    Args:
        db: Сессия базы данных
        student_id: ID студента
        student_update: Новые данные студента
        
    Returns:
        Обновленный студент или None
    """
    db_student = get_student(db, student_id)
    if db_student:
        update_data = student_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_student, key, value)
        db.commit()
        db.refresh(db_student)
    return db_student

def delete_student(db: Session, student_id: int):
    """
    Удалить студента.
    
    Args:
        db: Сессия базы данных
        student_id: ID студента
        
    Returns:
        Удаленный студент или None
    """
    db_student = get_student(db, student_id)
    if db_student:
        db.delete(db_student)
        db.commit()
    return db_student

# CRUD операции для групп
def get_group(db: Session, group_id: int):
    """
    Получить группу по ID.
    
    Args:
        db: Сессия базы данных
        group_id: ID группы
        
    Returns:
        Объект группы или None
    """
    return db.query(models.Group).filter(models.Group.id == group_id).first()

def get_groups(db: Session, skip: int = 0, limit: int = 100):
    """
    Получить список групп.
    
    Args:
        db: Сессия базы данных
        skip: Количество записей для пропуска
        limit: Максимальное количество записей
        
    Returns:
        Список групп
    """
    return db.query(models.Group).offset(skip).limit(limit).all()

def create_group(db: Session, group: schemas.GroupCreate):
    """
    Создать новую группу.
    
    Args:
        db: Сессия базы данных
        group: Данные группы
        
    Returns:
        Созданная группа
    """
    db_group = models.Group(name=group.name)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def delete_group(db: Session, group_id: int):
    """
    Удалить группу.
    
    Args:
        db: Сессия базы данных
        group_id: ID группы
        
    Returns:
        Удаленная группа или None
    """
    db_group = get_group(db, group_id)
    if db_group:
        # Удаляем связь со студентами (обнуляем group_id)
        for student in db_group.students:
            student.group_id = None
        db.delete(db_group)
        db.commit()
    return db_group

def get_students_in_group(db: Session, group_id: int):
    """
    Получить всех студентов в группе.
    
    Args:
        db: Сессия базы данных
        group_id: ID группы
        
    Returns:
        Список студентов в группе
    """
    group = get_group(db, group_id)
    return group.students if group else []

def add_student_to_group(db: Session, student_id: int, group_id: int):
    """
    Добавить студента в группу.
    
    Args:
        db: Сессия базы данных
        student_id: ID студента
        group_id: ID группы
        
    Returns:
        Обновленный студент или None
    """
    student = get_student(db, student_id)
    group = get_group(db, group_id)
    
    if student and group:
        student.group_id = group_id
        db.commit()
        db.refresh(student)
    
    return student

def remove_student_from_group(db: Session, student_id: int):
    """
    Удалить студента из группы.
    
    Args:
        db: Сессия базы данных
        student_id: ID студента
        
    Returns:
        Обновленный студент или None
    """
    student = get_student(db, student_id)
    if student:
        student.group_id = None
        db.commit()
        db.refresh(student)
    return student

def transfer_student(db: Session, student_id: int, from_group_id: int, to_group_id: int):
    """
    Перевести студента из одной группы в другую.
    
    Args:
        db: Сессия базы данных
        student_id: ID студента
        from_group_id: ID исходной группы
        to_group_id: ID целевой группы
        
    Returns:
        Обновленный студент или None
    """
    student = get_student(db, student_id)
    from_group = get_group(db, from_group_id)
    to_group = get_group(db, to_group_id)
    
    if student and from_group and to_group and student.group_id == from_group_id:
        student.group_id = to_group_id
        db.commit()
        db.refresh(student)
    
    return student