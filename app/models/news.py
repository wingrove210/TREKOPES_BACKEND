from database import Base
from sqlalchemy import Column, Integer, String, Text, DateTime

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    image_url = Column(String, nullable=True)
    published_at = Column(DateTime, nullable=True)