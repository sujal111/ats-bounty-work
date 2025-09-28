from fastapi import FastAPI
from app.routes import datasets, goldens, test_cases, evaluate

app = FastAPI(title="LLMSec Framework MVP", version="0.1.0")

# Register routes
app.include_router(datasets.router)
app.include_router(goldens.router)
app.include_router(test_cases.router)
app.include_router(evaluate.router)
