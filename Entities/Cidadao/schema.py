from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Cidadao(Base):
    __tablename__ = "cidadao"

    contacto = Column(String(13), primary_key=True, unique=True, nullable=False)
    nome = Column(String(50), primary_key=False, unique=False, nullable=False)
    rgpd = Column(Boolean, primary_key=False, unique=False, nullable=False, default=False)
