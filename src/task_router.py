from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_db
from src.security import get_current_user
from src.models import User
from src.schemas import TaskCreate, TaskResponse
from src.crud import create_task, get_user_tasks_by_id


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=list[TaskResponse])
async def get_tasks(current_user: User = Depends(get_current_user),
                    db: AsyncSession = Depends(get_async_db)):
    result = await get_user_tasks_by_id(current_user.id, db)
    return result


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_new_task(new_task: TaskCreate, current_user: User = Depends(get_current_user),
                      db: AsyncSession = Depends(get_async_db)):
    result = await create_task(new_task, current_user.id, db)
    return result






