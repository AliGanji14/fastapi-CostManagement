from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Float,ForeignKey
from sqlalchemy.orm import relationship

from config import settings

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False}
)

Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    description = Column(String(50), nullable=False)
    amount = Column(Float, nullable=False)

    user = relationship("UserModel", back_populates="expenses")

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()



