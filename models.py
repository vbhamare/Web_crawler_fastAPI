from pydantic import BaseModel
from sqlalchemy import Date, ForeignKey, create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base,sessionmaker,relationship
import uuid 
from datetime import datetime

engine = create_engine('postgresql://postgres:12345@localhost:5432/webcrawlerdb')
Session = sessionmaker(aucommit=False ,autoflush=False,bind=engine)

class TaskStatus():
    SCHEDULED = 'SCHEDULED'
    STARTED = 'STARTED'
    FAILED = 'FAILED'
    FINISHED = 'FINISHED'

# Create SQLAlchemy base
Base = declarative_base()

# Define SQLAlchemy model
class Task(Base):
    __tablename__ = 'tasks'

    run_id = Column(String, primary_key=True,default=lambda:str(uuid.uuid4()))
    date = Column(Date)
    status = Column(String)
    error = Column(String)
    started_at = Column(Date)
    finished_at = Column(Date)
    failed_at = Column(Date)
    legitimate_sellers = relationship("LegitimateSeller", back_populates="tasks")

class LegitimateSeller(Base):
    __tablename__ = 'legitimate_sellers'
    
    id = Column(Integer, primary_key=True,autoincrement=True)
    site = Column(String(100))
    ssp_domain_name = Column(String(200))
    publisher_id = Column(String(200))
    seller_relationship = Column(String(50))
    date = Column(Date)
    run_id = Column(String(30), ForeignKey('tasks.run_id'))

    # Define a relationship with the Task model if needed
    tasks = relationship("Task", back_populates="legitimate_sellers")
    



def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()