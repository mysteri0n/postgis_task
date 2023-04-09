from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DOUBLE_PRECISION, VARCHAR
from geoalchemy2 import Geometry


Base = declarative_base()


class Fields(Base):
    __tablename__ = 'fields'

    ogc_fid = Column(Integer, primary_key=True)
    id = Column(Integer)
    crop = Column(VARCHAR)
    productivity = Column(DOUBLE_PRECISION)
    area_ha = Column(VARCHAR)
    history = Column(VARCHAR)
    region = Column(VARCHAR)
    score = Column(VARCHAR)
    wkb_geometry = Column(Geometry('POLYGON'))

    def __repr__(self) -> str:
        return f"Field(id={self.id!r}, crop={self.crop}, area={self.area_ha!r})"
