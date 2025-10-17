# In app/models.py
from sqlalchemy import Column, Integer, String, Text, ARRAY, ForeignKey
from sqlalchemy.orm import relationship # Import relationship
from database import Base

class Candidate(Base):
    __tablename__ = "candidates"; id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True); email = Column(String, index=True, nullable=True)
    skills = Column(ARRAY(String), nullable=True); raw_text = Column(Text, nullable=True)
    job_id = Column(Integer, ForeignKey("jobs.id")); status = Column(String, default="new", index=True)
class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True) # Link to company
    company = relationship("Company")

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    required_skills = Column(ARRAY(String))
    company_id = Column(Integer, ForeignKey("companies.id")) # Link to company
    company = relationship("Company")
    hiring_manager_id = Column(Integer, ForeignKey("users.id"), nullable=True)