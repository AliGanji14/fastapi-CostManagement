from core.database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    description = Column(String(50), nullable=False)
    amount = Column(Float, nullable=False)

    user = relationship("UserModel", back_populates="expenses")
