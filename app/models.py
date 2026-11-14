from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Tankstelle(Base):
    __tablename__ = "tankstellen"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str]
    marke: Mapped[str]
    adresse: Mapped[str]
    ort: Mapped[str]
    lat: Mapped[float]
    lng: Mapped[float]

    preise: Mapped[list["Preis"]] = relationship(back_populates="tankstelle")


class Preis(Base):
    __tablename__ = "preise"

    id: Mapped[int] = mapped_column(primary_key=True)
    tankstelle_id: Mapped[str] = mapped_column(ForeignKey("tankstellen.id"), index=True)
    sorte: Mapped[str] = mapped_column(String(6))
    preis: Mapped[float]
    geoeffnet: Mapped[bool]
    zeitpunkt: Mapped[datetime] = mapped_column(index=True)

    tankstelle: Mapped["Tankstelle"] = relationship(back_populates="preise")