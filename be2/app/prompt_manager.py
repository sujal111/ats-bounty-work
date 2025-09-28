from typing import Dict, List, Optional
from pydantic import BaseModel
from jinja2 import Template

# -------------------------------
# Models
# -------------------------------
class PromptVersion(BaseModel):
    version: str
    content: str   # raw text or messages
    type: str      # "text" or "messages"

class Prompt(BaseModel):
    alias: str
    versions: Dict[str, PromptVersion] = {}  # keyed by version string

# -------------------------------
# In-memory storage
# -------------------------------
PROMPTS: Dict[str, Prompt] = {}

# -------------------------------
# Helpers
# -------------------------------
def render_prompt(content: str, variables: dict) -> str:
    """Render prompt with Jinja2 variables/logic."""
    template = Template(content)
    return template.render(**variables)

def add_prompt_version(alias: str, version: str, content: str, type_: str) -> Prompt:
    if alias not in PROMPTS:
        PROMPTS[alias] = Prompt(alias=alias, versions={})
    PROMPTS[alias].versions[version] = PromptVersion(version=version, content=content, type=type_)
    return PROMPTS[alias]

def get_prompt_version(alias: str, version: Optional[str] = None) -> PromptVersion:
    if alias not in PROMPTS:
        raise ValueError("Prompt alias not found")
    if not version:
        # return latest version
        versions = sorted(PROMPTS[alias].versions.keys())
        version = versions[-1]
    return PROMPTS[alias].versions[version]
