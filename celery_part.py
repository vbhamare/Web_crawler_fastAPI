from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Task , LegitimateSeller , TaskStatus
import uuid 
from datetime import datetime
import json
import urllib
from celery_config import celery

engine = create_engine('postgresql://postgres:12345@localhost:5432/webcrawlerdb')
Session = sessionmaker(aucommit=False ,autoflush=False,bind=engine)

# celery = Celery('tasks', broker='redis://localhost:6379/0')
#celery = Celery('tasks', broker='http://127.0.0.1:8000/')

@celery.task(name='scheduler')
def scheduler():
    print('schedular called')
    db = Session()
    try:
        new_task = Task(
            run_id=str(uuid.uuid4()),
            date=datetime.now().date(),
            status=TaskStatus.SCHEDULED
        )
        db.add(new_task)
        db.commit()
        print(f"Scheduled new task with run_id: {new_task.run_id}")
    except Exception as e:
        db.rollback()
        print(f"Failed to schedule new task: {e}")
    finally:
        db.close()

@celery.task(name='executor')
def executor():
    db=  Session()
    try:
        task = db.query(Task).filter_by(status=TaskStatus.SCHEDULED).first()
        if task:
            task.status = TaskStatus.STARTED
            task.started_at = datetime.now()
            db.commit()
            print(f"Started task with run_id: {task.run_id}")

            with open('sites.json') as f:
                sites = json.load(f)["sites"]
                print(f"Processing sites: {sites}")

            for domain in sites:
                url = f"https://{domain}/ads.txt"
                try:
                    with urllib.request.urlopen(url) as response:
                        if response.getcode() == 200:
                            lines = response.read().decode('utf-8').splitlines()
                            print(f"Lines from {domain}: {lines}")
                            lines = [line for line in lines if ',' in line]
                            for line in lines:
                                for index in range(len(lines)):
                                    line = lines[index]
                                    line = line.split(',')
                                    ssp_domain_name = line[0]
                                    publisher_id = line[1]
                                    seller_relationship = line[2]
                                    new_seller = LegitimateSeller(
                                        site=domain,
                                        ssp_domain_name=ssp_domain_name,
                                        publisher_id=publisher_id,
                                        seller_relationship=seller_relationship,
                                        date=datetime.now().date(),
                                        run_id=task.run_id
                                    )
                                    db.add(new_seller)
                except Exception as e:
                    print(f"An error occurred processing {domain}: {e}")

            db.commit()
            task.status = TaskStatus.FINISHED
            task.finished_at = datetime.now()
        else:
            print("No scheduled tasks found.")
    except Exception as e:
        db.rollback()
        print(f"Failed to process task: {e}")
    finally:
        try:
            db.commit()
        except Exception as e:
            print(f"Failed to commit changes to the database: {e}")
        finally:
            db.close()