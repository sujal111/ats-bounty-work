from fastapi import APIRouter
from app.models.test_case import LLMTestCase
from app.models.metrics import MetricResult
from app.services.security_checks import detect_prompt_injection, detect_sensitive_leakage

router = APIRouter(prefix="/evaluate", tags=["Evaluation"])

@router.post("/", response_model=list[MetricResult])
async def evaluate_case(test_case: LLMTestCase):
    results = []
    if test_case.input:
        results.append(detect_prompt_injection(test_case.input))
    if test_case.actual_output:
        results.append(detect_sensitive_leakage(test_case.actual_output))
    return results
