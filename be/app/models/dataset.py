from typing import List
from pydantic import BaseModel
from .golden import Golden
from .test_case import LLMTestCase

class EvaluationDataset(BaseModel):
    id: str
    name: str
    type: str   # "single-turn" or "multi-turn"
    goldens: List[Golden] = []
    test_cases: List[LLMTestCase] = []

    def add_test_case(self, test_case: LLMTestCase):
        self.test_cases.append(test_case)
