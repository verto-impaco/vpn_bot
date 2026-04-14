from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from database.models import Base

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL is None:
    raise ValueError("Переменная окружения DATABASE_URL не установлена")

engine = create_engine(DATABASE_URL, echo=False)

# Фабрика сессий
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def init_db():
    """Создаёт таблицы, если их нет"""
    Base.metadata.create_all(bind=engine)


def get_session():
    """Возвращает новую сессию"""
    return SessionLocal()
