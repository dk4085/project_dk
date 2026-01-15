from pydantic import BaseModel
from typing import Optional, List

# Схемы для студента
class StudentBase(BaseModel):
    """Базовая схема студента."""
    first_name: str
    last_name: str
    age: Optional[int] = None
    group_id: Optional[int] = None

class StudentCreate(StudentBase):
    """Схема для создания студента."""
    pass

class StudentUpdate(BaseModel):
    """Схема для обновления студента."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    group_id: Optional[int] = None

class Student(StudentBase):
    """Схема студента с идентификатором."""
    id: int
    
    class Config:
        from_attributes = True

# Схемы для группы
class GroupBase(BaseModel):
    """Базовая схема группы."""
    name: str

class GroupCreate(GroupBase):
    """Схема для создания группы."""
    pass

class Group(GroupBase):
    """Схема группы с идентификатором."""
    id: int
    
    class Config:
        from_attributes = True

class GroupWithStudents(Group):
    """Схема группы со списком студентов."""
    students: List[Student] = []

# Схемы для операций с группами
class AddStudentToGroup(BaseModel):
    """Схема для добавления студента в группу."""
    student_id: int
    group_id: int

class TransferStudent(BaseModel):
    """Схема для перевода студента между группами."""
    student_id: int
    from_group_id: int
    to_group_id: int