from fastapi import APIRouter
from app.models.test_case import LLMTestCase
from app.services.storage import DATASETS

router = APIRouter(prefix="/testcases", tags=["TestCases"])

@router.post("/{dataset_id}", response_model=LLMTestCase)
async def add_test_case(dataset_id: str, test_case: LLMTestCase):
    dataset = DATASETS.get(dataset_id)
    dataset.test_cases.append(test_case)
    return test_case

@router.get("/{dataset_id}", response_model=list[LLMTestCase])
async def list_test_cases(dataset_id: str):
    dataset = DATASETS.get(dataset_id)
    return dataset.test_cases
