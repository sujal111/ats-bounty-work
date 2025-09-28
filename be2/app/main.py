# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from typing import List, Optional, Dict, Any
# from jinja2 import Template

# # -------------------------------
# # App init
# # -------------------------------
# app = FastAPI(title="LLM Evaluation Framework", version="0.2.0")

# # -------------------------------
# # Mock LLM App (RAG style pipeline)
# # -------------------------------
# def retriever(query: str) -> List[str]:
#     return ["retrieved", "context", "chunks"]

# def generator(query: str, context: List[str]) -> str:
#     return f"Answer to '{query}' using context {context}"

# def llm_app(query: str) -> str:
#     return generator(query, retriever(query))

# # -------------------------------
# # Dataset + Schema
# # -------------------------------
# class Golden(BaseModel):
#     id: str
#     input: str
#     expected_output: str

# class Dataset(BaseModel):
#     alias: str
#     goldens: List[Golden] = []

# DATASETS = {}

# # -------------------------------
# # Test Case & Metrics
# # -------------------------------
# class TestCase(BaseModel):
#     id: str
#     input: str
#     expected_output: str
#     actual_output: Optional[str] = None
#     passed: Optional[bool] = None
#     score: Optional[float] = None

# def simple_exact_match(expected: str, actual: str) -> (bool, float):
#     return (expected.strip() == actual.strip(), float(expected.strip() == actual.strip()))

# # -------------------------------
# # Prompt Versioning
# # -------------------------------
# class PromptVersion(BaseModel):
#     version: str
#     content: str   # raw text or messages
#     type: str      # "text" or "messages"

# class Prompt(BaseModel):
#     alias: str
#     versions: Dict[str, PromptVersion] = {}  # keyed by version string

# PROMPTS: Dict[str, Prompt] = {}

# class PromptRequest(BaseModel):
#     alias: str
#     version: str
#     type: str
#     content: str

# class PromptRenderRequest(BaseModel):
#     alias: str
#     version: Optional[str] = None
#     variables: Dict[str, Any] = {}

# def render_prompt(content: str, variables: dict) -> str:
#     template = Template(content)
#     return template.render(**variables)

# def add_prompt_version(alias: str, version: str, content: str, type_: str) -> Prompt:
#     if alias not in PROMPTS:
#         PROMPTS[alias] = Prompt(alias=alias, versions={})
#     PROMPTS[alias].versions[version] = PromptVersion(version=version, content=content, type=type_)
#     return PROMPTS[alias]

# def get_prompt_version(alias: str, version: Optional[str] = None) -> PromptVersion:
#     if alias not in PROMPTS:
#         raise ValueError("Prompt alias not found")
#     if not version:
#         versions = sorted(PROMPTS[alias].versions.keys())
#         version = versions[-1]  # latest version
#     return PROMPTS[alias].versions[version]

# # -------------------------------
# # Dataset Endpoints
# # -------------------------------
# @app.post("/dataset/create")
# def create_dataset(dataset: Dataset):
#     if dataset.alias in DATASETS:
#         raise HTTPException(status_code=400, detail="Dataset alias already exists")
#     DATASETS[dataset.alias] = dataset
#     return {"message": "Dataset created", "alias": dataset.alias}

# @app.get("/dataset/{alias}")
# def get_dataset(alias: str):
#     if alias not in DATASETS:
#         raise HTTPException(status_code=404, detail="Dataset not found")
#     return DATASETS[alias]

# @app.post("/evaluate/{alias}")
# def evaluate_dataset(alias: str, prompt_alias: Optional[str] = None, prompt_version: Optional[str] = None, variables: Optional[Dict[str, Any]] = {}):
#     if alias not in DATASETS:
#         raise HTTPException(status_code=404, detail="Dataset not found")

#     dataset = DATASETS[alias]
#     results = []

#     for golden in dataset.goldens:
#         query = golden.input
#         # Apply prompt versioning if provided
#         if prompt_alias:
#             try:
#                 pv = get_prompt_version(prompt_alias, prompt_version)
#                 query = render_prompt(pv.content, {**variables, "user_input": query})
#             except Exception as e:
#                 raise HTTPException(status_code=400, detail=f"Prompt error: {str(e)}")
#         actual = llm_app(query)
#         passed, score = simple_exact_match(golden.expected_output, actual)
#         test_case = TestCase(
#             id=golden.id,
#             input=query,
#             expected_output=golden.expected_output,
#             actual_output=actual,
#             passed=passed,
#             score=score
#         )
#         results.append(test_case)

#     pass_rate = sum(1 for r in results if r.passed) / len(results) if results else 0
#     return {
#         "alias": alias,
#         "results": results,
#         "summary": {
#             "total_cases": len(results),
#             "pass_rate": pass_rate
#         }
#     }

# # -------------------------------
# # Prompt Endpoints
# # -------------------------------
# @app.post("/prompts/create-version")
# def create_prompt_version(req: PromptRequest):
#     try:
#         prompt = add_prompt_version(req.alias, req.version, req.content, req.type)
#         return {"message": "Prompt version created", "alias": req.alias, "version": req.version}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @app.post("/prompts/render")
# def render_prompt_version(req: PromptRenderRequest):
#     try:
#         pv = get_prompt_version(req.alias, req.version)
#         rendered = render_prompt(pv.content, req.variables)
#         return {"alias": req.alias, "version": pv.version, "rendered_prompt": rendered}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @app.get("/prompts/{alias}")
# def get_prompt(alias: str):
#     if alias not in PROMPTS:
#         raise HTTPException(status_code=404, detail="Prompt not found")
#     return PROMPTS[alias]


from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from jinja2 import Template

# -------------------------------
# App init
# -------------------------------
app = FastAPI(title="LLM Evaluation Framework", version="0.3.0")

# -------------------------------
# JWT / Auth Config
# -------------------------------
SECRET_KEY = "YOUR_SECRET_KEY_HERE"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# -------------------------------
# Mock DB for Users
# -------------------------------
USERS_DB = {}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None or username not in USERS_DB:
            raise HTTPException(status_code=401, detail="Invalid authentication")
        return USERS_DB[username]
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication")

# -------------------------------
# Auth Models & Routes
# -------------------------------
class User(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

@app.post("/register")
def register(user: User):
    if user.username in USERS_DB:
        raise HTTPException(status_code=400, detail="Username already exists")
    USERS_DB[user.username] = {
        "username": user.username,
        "hashed_password": get_password_hash(user.password)
    }
    return {"message": "User registered successfully"}

@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = USERS_DB.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

# -------------------------------
# Mock LLM App (RAG style pipeline)
# -------------------------------
def retriever(query: str) -> List[str]:
    return ["retrieved", "context", "chunks"]

def generator(query: str, context: List[str]) -> str:
    return f"Answer to '{query}' using context {context}"

def llm_app(query: str) -> str:
    return generator(query, retriever(query))

# -------------------------------
# Dataset + Schema
# -------------------------------
class Golden(BaseModel):
    id: str
    input: str
    expected_output: str

class Dataset(BaseModel):
    alias: str
    goldens: List[Golden] = []

DATASETS: Dict[str, Dataset] = {}

# -------------------------------
# Test Case & Metrics
# -------------------------------
class TestCase(BaseModel):
    id: str
    input: str
    expected_output: str
    actual_output: Optional[str] = None
    passed: Optional[bool] = None
    score: Optional[float] = None

def simple_exact_match(expected: str, actual: str) -> (bool, float):
    return (expected.strip() == actual.strip(), float(expected.strip() == actual.strip()))

# -------------------------------
# Prompt Versioning
# -------------------------------
class PromptVersion(BaseModel):
    version: str
    content: str
    type: str   # "text" or "messages"

class Prompt(BaseModel):
    alias: str
    versions: Dict[str, PromptVersion] = {}

PROMPTS: Dict[str, Prompt] = {}

class PromptRequest(BaseModel):
    alias: str
    version: str
    type: str
    content: str

class PromptRenderRequest(BaseModel):
    alias: str
    version: Optional[str] = None
    variables: Dict[str, Any] = {}

def render_prompt(content: str, variables: dict) -> str:
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
        versions = sorted(PROMPTS[alias].versions.keys())
        version = versions[-1]  # latest version
    return PROMPTS[alias].versions[version]

# -------------------------------
# Protected Dataset Endpoints
# -------------------------------
@app.post("/dataset/create")
def create_dataset(dataset: Dataset, current_user: dict = Depends(get_current_user)):
    if dataset.alias in DATASETS:
        raise HTTPException(status_code=400, detail="Dataset alias already exists")
    DATASETS[dataset.alias] = dataset
    return {"message": "Dataset created", "alias": dataset.alias}

@app.get("/dataset/{alias}")
def get_dataset(alias: str, current_user: dict = Depends(get_current_user)):
    if alias not in DATASETS:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return DATASETS[alias]

@app.post("/evaluate/{alias}")
def evaluate_dataset(
    alias: str,
    prompt_alias: Optional[str] = None,
    prompt_version: Optional[str] = None,
    variables: Optional[Dict[str, Any]] = {},
    current_user: dict = Depends(get_current_user)
):
    if alias not in DATASETS:
        raise HTTPException(status_code=404, detail="Dataset not found")

    dataset = DATASETS[alias]
    results = []

    for golden in dataset.goldens:
        query = golden.input
        # Apply prompt versioning if provided
        if prompt_alias:
            try:
                pv = get_prompt_version(prompt_alias, prompt_version)
                query = render_prompt(pv.content, {**variables, "user_input": query})
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Prompt error: {str(e)}")
        actual = llm_app(query)
        passed, score = simple_exact_match(golden.expected_output, actual)
        test_case = TestCase(
            id=golden.id,
            input=query,
            expected_output=golden.expected_output,
            actual_output=actual,
            passed=passed,
            score=score
        )
        results.append(test_case)

    pass_rate = sum(1 for r in results if r.passed) / len(results) if results else 0
    return {
        "alias": alias,
        "results": results,
        "summary": {
            "total_cases": len(results),
            "pass_rate": pass_rate
        }
    }

# -------------------------------
# Protected Prompt Endpoints
# -------------------------------
@app.post("/prompts/create-version")
def create_prompt_version(req: PromptRequest, current_user: dict = Depends(get_current_user)):
    try:
        prompt = add_prompt_version(req.alias, req.version, req.content, req.type)
        return {"message": "Prompt version created", "alias": req.alias, "version": req.version}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/prompts/render")
def render_prompt_version(req: PromptRenderRequest, current_user: dict = Depends(get_current_user)):
    try:
        pv = get_prompt_version(req.alias, req.version)
        rendered = render_prompt(pv.content, req.variables)
        return {"alias": req.alias, "version": pv.version, "rendered_prompt": rendered}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/prompts/{alias}")
def get_prompt(alias: str, current_user: dict = Depends(get_current_user)):
    if alias not in PROMPTS:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return PROMPTS[alias]
