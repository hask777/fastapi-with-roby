from sqlalchemy import Boolean, String, Integer, Column
from database import Base

class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(String)
    complete = Column(Boolean, default=False)