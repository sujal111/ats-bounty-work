from fastapi import APIRouter
from app.models.golden import Golden
from app.services.storage import DATASETS

router = APIRouter(prefix="/goldens", tags=["Goldens"])

@router.post("/{dataset_id}", response_model=Golden)
async def add_golden(dataset_id: str, golden: Golden):
    dataset = DATASETS.get(dataset_id)
    dataset.goldens.append(golden)
    return golden

@router.get("/{dataset_id}", response_model=list[Golden])
async def list_goldens(dataset_id: str):
    dataset = DATASETS.get(dataset_id)
    return dataset.goldens
