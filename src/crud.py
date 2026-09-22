from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas import UserCreate, TaskCreate
from sqlalchemy import select
from src.models import User, Task
from src.security import get_password_hash


async def get_user_by_email(email: str, db: AsyncSession) -> User | None:
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    db_email = result.scalars().one_or_none()
    return db_email


async def create_user(new_user: UserCreate, db: AsyncSession):
    hash_pwd = get_password_hash(new_user.password)
    db_user = User(email=new_user.email, hashed_password=hash_pwd)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user_tasks_by_id(user_id: int, db: AsyncSession)-> list[Task]:
    stmt = select(Task).where(Task.user_id == user_id)
    result = await db.execute(stmt)
    db_task = result.scalars().all()
    return list(db_task)



async def create_task(new_task: TaskCreate, user_id: int, db: AsyncSession):
    db_task = Task(title=new_task.title, description=new_task.description,
                   user_id=user_id)
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task

