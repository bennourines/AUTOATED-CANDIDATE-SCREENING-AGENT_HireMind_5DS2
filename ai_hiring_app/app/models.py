# In app/models.py
from sqlalchemy import Column, Integer, String, Text, ARRAY, ForeignKey
from .database import Base

class User(Base): # Keeping this
    __tablename__ = "users"; id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False); role = Column(String, nullable=False)

class Job(Base): # REMOVING hiring_manager_id
    __tablename__ = "jobs"; id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True); description = Column(Text)
    required_skills = Column(ARRAY(String))

class Candidate(Base): # Unchanged
    __tablename__ = "candidates"; id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True); email = Column(String, index=True, nullable=True)
    skills = Column(ARRAY(String), nullable=True); raw_text = Column(Text, nullable=True)
    job_id = Column(Integer, ForeignKey("jobs.id")); status = Column(String, default="new", index=True)