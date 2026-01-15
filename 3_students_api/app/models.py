from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Group(Base):
    """
    Модель группы студентов.
    """
    __tablename__ = "groups"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    
    # Связь с таблицей студентов
    students = relationship("Student", back_populates="group")

class Student(Base):
    """
    Модель студента.
    """
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    age = Column(Integer)
    
    # Внешний ключ для связи с группой
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    
    # Связь с таблицей групп
    group = relationship("Group", back_populates="students")