import enum
from sqlalchemy import Date, ForeignKey, Column, Integer, String,DateTime,Enum
from sqlalchemy.orm import declarative_base,relationship
from datetime import datetime
import uuid
from database import Base

class TaskStatus(enum.Enum):
    SCHEDULED = 'SCHEDULED'
    STARTED = 'STARTED'
    FAILED = 'FAILED'
    FINISHED = 'FINISHED'

# Define SQLAlchemy model
class Task(Base):
    __tablename__ = 'tasks'

    run_id = Column(String, primary_key=True,default=lambda:str(uuid.uuid4()))
    date = Column(Date, default=datetime.utcnow().date())
    status = Column(Enum((TaskStatus),default=TaskStatus.SCHEDULED))
    error = Column(String,nullable=True)
    started_at = Column(DateTime,nullable=True)
    finished_at = Column(DateTime,nullable=True)
    failed_at = Column(DateTime,nullable=True)
    legitimate_sellers = relationship("LegitimateSeller", back_populates="tasks")

class LegitimateSeller(Base):
    __tablename__ = 'legitimate_sellers'
    
    id = Column(Integer, primary_key=True,autoincrement=True)
    site = Column(String(100))
    ssp_domain_name = Column(String(200))
    publisher_id = Column(String(200))
    seller_relationship = Column(String(50))
    date = Column(DateTime,default=datetime.utcnow().date())
    run_id = Column(String(200), ForeignKey('tasks.run_id'))

    # Define a relationship with the Task model if needed
    tasks = relationship("Task", back_populates="legitimate_sellers")
    