from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import declarative_base
# from "../Entidade/schema.py" import entidade

Base = declarative_base()

class Contacto(Base):
    __tablename__ = "contacto"

    contacto = Column(String(45), primary_key=True, unique=True, nullable=False)
    entidade_nif_nipc = Column(String(9), ForeignKey("entidade.nif_nipc", ondelete="CASCADE"), primary_key=False, unique=True, nullable=False,)
    nome_contacto = Column(String(100), primary_key=False, unique=False, nullable=False)
    descricao = Column(String(500), primary_key=False, unique=False, nullable=False)
