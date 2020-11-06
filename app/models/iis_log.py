from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class IISLog(Base):
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime)
    time = Column(String(20), index=True)
    s_ip = Column(String(20), index=True)
    cs_method = Column(String(10), index=True)
    cs_uri_stem = Column(String(500))
    cs_uri_query = Column(String(500))
    s_port = Column(Integer)
    cs_username = Column(String(20))
    c_ip = Column(String(20), index=True)
    cs_user_agent = Column(String(500))
    sc_status = Column(String(500))
    sc_substatus = Column(Integer)
    sc_win32_status = Column(Integer)
    sc_bytes = Column(Integer)
    cs_bytes = Column(Integer)
    time_taken = Column(Integer, nullable=True)
