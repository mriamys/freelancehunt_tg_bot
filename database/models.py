from sqlalchemy import Column, Integer, BigInteger, DateTime, String
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class SentProject(Base):
    __tablename__ = "sent_projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(BigInteger, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
