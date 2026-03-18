from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Bens_E_Servicos(Base):
    __tablename__ = "bens_e_servico"

    tipo_bem_servico = Column(String(100), primary_key=True, unique=True, nullable=False)
