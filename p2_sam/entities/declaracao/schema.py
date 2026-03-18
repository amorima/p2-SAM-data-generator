from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Declaracao(Base):
    __tablename__ = "declaracao"

    declaracao_id = Column(String(250), primary_key=True, unique=True, nullable=False)
    doacao_id = Column(String(250), ForeignKey("doacao.id_doacao", ondelete=CASCADE), unique=True, nullable=False)