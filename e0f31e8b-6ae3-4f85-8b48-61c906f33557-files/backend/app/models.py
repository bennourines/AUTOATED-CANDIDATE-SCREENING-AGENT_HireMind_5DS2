from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    candidates = relationship("Candidate", back_populates="job", cascade="all, delete-orphan")

class Candidate(Base):
    __tablename__ = "candidates"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True, index=True)
    resume_text = Column(Text, nullable=True)
    shortlisted = Column(Boolean, default=False)
    decision = Column(String(50), nullable=True)

    job_id = Column(Integer, ForeignKey("jobs.id"), index=True)
    job = relationship("Job", back_populates="candidates")
