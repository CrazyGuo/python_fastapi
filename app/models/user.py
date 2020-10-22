from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class AppUsers(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(20), index=True)
    email = Column(String(30), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_available = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
