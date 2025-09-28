from typing import List, Optional, Dict
from pydantic import BaseModel

class ToolCall(BaseModel):
    name: str
    args: Dict

class LLMTestCase(BaseModel):
    id: Optional[str] = None
    input: str
    actual_output: Optional[str] = None
    retrieval_context: Optional[List[str]] = None
    tools_called: Optional[List[ToolCall]] = None

    # Security additions
    attack_type: Optional[str] = None
    security_flags: Optional[List[str]] = None

    expected_output: Optional[str] = None
    context: Optional[List[str]] = None
    expected_tools: Optional[List[ToolCall]] = None

    name: Optional[str] = None
