from typing import Dict
from app.models.dataset import EvaluationDataset

# In-memory database
DATASETS: Dict[str, EvaluationDataset] = {}
