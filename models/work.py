from typing import List
from pydantic import BaseModel


class Work(BaseModel):
    title: str
    url: str
    description: str
    tags: List[str]
    location: str
    client_spendings: str
    payment_status: str
    rating: str
    job_type: str
    tier: str
    date: str
