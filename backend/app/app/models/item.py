from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Item(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    devices = Column(String, index=True)
    is_active = Column(Integer, index=True)
    ticketType = Column(String)
    externalId	= Column(Integer, index=True)
    tenant = Column(String, index=True)
    region = Column(String, index=True)
    requestType = Column(String, index=True)
    category1 = Column(String, index=True)
    category2 = Column(String, index=True)
    category3 = Column(String, index=True)
    vlan = Column(String, index=True)
    vrf = Column(String, index=True)
    owner = relationship("User", back_populates="items")
    owner_id = Column(Integer, ForeignKey("user.id"))
