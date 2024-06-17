from pydantic import BaseModel
from datetime import datetime

# Define Pydantic model
class TaskModel(BaseModel):
    run_id: int
    date : datetime
    status : str
    error :str
    started_at : datetime
    finished_at :  datetime
    failed_at : datetime

    class Config:
        from_attributes = True

class legitimateSellerModel(BaseModel):
    id:int
    site: str
    ssp_domain_name : str
    publisher_id : str
    seller_relationship :str
    run_id : str

    class Config:
        from_attributes = True