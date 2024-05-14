from sqlalchemy import Column, Integer, LargeBinary
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ResizedImage(Base):
    __tablename__ = 'resized_images'
    id = Column(Integer, primary_key=True, index=True)
    depth = Column(Integer, index=True)
    pixel_values = Column(LargeBinary)
