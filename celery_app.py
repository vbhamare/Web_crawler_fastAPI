from celery_config import celery
import celery_part

if __name__ == "__main__":
    celery.start()