from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, delete
from datetime import datetime, timedelta
from .models import Base, SentProject
from utils.logger import logger

DATABASE_URL = "sqlite+aiosqlite:///./bot_data.db"

engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database initialized")


async def is_project_sent(project_id: int) -> bool:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(SentProject).where(SentProject.project_id == project_id)
        )
        return result.scalar_one_or_none() is not None


async def save_sent_project(project_id: int):
    async with AsyncSessionLocal() as session:
        new_project = SentProject(project_id=project_id)
        session.add(new_project)
        await session.commit()


async def clean_old_projects(days: int = 30):
    cutoff = datetime.utcnow() - timedelta(days=days)
    async with AsyncSessionLocal() as session:
        await session.execute(
            delete(SentProject).where(SentProject.created_at < cutoff)
        )
        await session.commit()
    logger.info(f"Cleaned projects older than {days} days")
