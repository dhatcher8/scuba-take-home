from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class TestModelOne(Base):
    __tablename__ = "test_model_one"

    id = Column(Integer, primary_key=True, index=True)
    test_string_one = Column(String)
    test_bool_one = Column(Boolean, default=True)

class TestModelTwo(Base):
    __tablename__ = "test_model_two"

    id = Column(Integer, primary_key=True, index=True)
    test_string_one = Column(String)
    test_bool_one = Column(Boolean, default=True)

    test_one_partner_id = Column(Integer, ForeignKey("users.id"))