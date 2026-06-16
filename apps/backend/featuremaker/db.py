from collections.abc import Generator

from fastapi.params import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from featuremaker.config import get_settings
from typing import Annotated


settings = get_settings()

engine = create_engine(settings.database_url, pool_pre_ping=True)



class Base(DeclarativeBase):
    pass


SessionFactory = sessionmaker(
    bind=engine,
    expire_on_commit=False,
)

def get_session() -> Generator[Session, None, None]:
    with SessionFactory() as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]