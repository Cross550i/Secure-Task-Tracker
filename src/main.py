from fastapi import FastAPI
from src.router import router as auth_router
from src.task_router import router as task_router

app = FastAPI(title="Secure Task Tracker")

app.include_router(auth_router)
app.include_router(task_router)


@app.get("/")
async def welcome():
    return {"message": "Welcome to Secure Task Tracker API"}
