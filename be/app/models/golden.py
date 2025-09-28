from typing import List, Optional, Dict
from pydantic import BaseModel
from .test_case import ToolCall

class Golden(BaseModel):
    id: Optional[str] = None
    input: str
    expected_output: Optional[str] = None
    context: Optional[List[str]] = None
    expected_tools: Optional[List[ToolCall]] = None
    additional_metadata: Optional[Dict] = None
    comments: Optional[str] = None
    custom_column_key_values: Optional[Dict[str, str]] = None

    # Security-specific metadata
    risk_profile: Optional[str] = None
