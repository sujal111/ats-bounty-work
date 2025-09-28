from typing import Dict
from pydantic import BaseModel

class MetricResult(BaseModel):
    name: str
    score: float
    passed: bool
    details: Dict
