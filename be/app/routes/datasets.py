from fastapi import APIRouter
from app.models.dataset import EvaluationDataset
from app.services.storage import DATASETS

router = APIRouter(prefix="/datasets", tags=["Datasets"])

@router.post("/", response_model=EvaluationDataset)
async def create_dataset(dataset: EvaluationDataset):
    DATASETS[dataset.id] = dataset
    return dataset

@router.get("/", response_model=list[EvaluationDataset])
async def list_datasets():
    return list(DATASETS.values())

@router.get("/{dataset_id}", response_model=EvaluationDataset)
async def get_dataset(dataset_id: str):
    return DATASETS.get(dataset_id)
