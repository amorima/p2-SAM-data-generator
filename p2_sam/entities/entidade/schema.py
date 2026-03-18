from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Entidade(Base):
    __tablename__ = "entidade"

    nif_nipc = Column(String(9), primary_key=True, unique=True, nullable=False)