import enum
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, ForeignKey, DECIMAL
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class tipoDonativo(enum.Enum):
    MBWAY = "mbway"
    CHEQUE = "cheque"
    MULTIBANCO = "multibanco"

class estadoDoacao(enum.Enum):
    ACEITE = "aceite"
    PENDENTE = "pendente"
    REJEITADO = "rejeitado"


class Doacao(Base):
    __tablename__ = "doacao"

    id_doacao = Column(Integer, primary_key=True, nullable=False, unique=True)
    mecena_nif_nipc = Column(Integer(9), ForeignKey("mecena.nif_nipc", ondelete=CASCADE), nullable=False, unique=True)
    data_emissao = Column(TIMESTAMP(timezone=True), nullable=False)
    valor_transacao = Column(DECIMAL(10,2), nullable=False)
    tipo_donativo = Column(enum(tipoDonativo), nullable=False)
    anonimo = Column(Boolean, nullable=False)
    url_comprovativo = Column(String, nullable=False)
    estado = Column(enum(estadoDoacao), nullable=False)
