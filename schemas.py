from pydantic import BaseModel,Field
from datetime import datetime,timezone
import uuid
from typing import Optional

# Define Pydantic model
class TaskModel(BaseModel):
    run_id: str = Field(default_factory=lambda:str(uuid.uuid4()))
    date : datetime=Field(default_factory=datetime.utcnow)
    status : str
    error :Optional[str]=None
    started_at : Optional[datetime]=None
    finished_at :  Optional[datetime]=None
    failed_at : Optional[datetime]=None

    class Config:
        from_attributes = True

class LegitimateSellerModel(BaseModel):
    id:int
    site: str
    ssp_domain_name : str
    publisher_id : str
    seller_relationship :str
    date:datetime=Field(default_factory=datetime.utcnow)
    run_id : str

    class Config:
        from_attributes = True