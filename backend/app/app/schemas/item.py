from pydantic import BaseModel

from .user import User  # noqa: F401


# Shared properties
class ItemBase(BaseModel):
    title: str = None
    description: str = None
    devices:str = None
    is_active: int = None
    ticketType:str = None
    externalId: int = None
    tenant:str = None
    region:str = None
    requestType:str = None
    category1:str = None
    category2:str = None
    category3:str = None
    vlan:str = None
    vrf:str = None



# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str


# Properties to receive on item update
class ItemUpdate(ItemBase):
    pass


# Properties shared by models stored in DB
class ItemInDBBase(ItemBase):
    id: int
    title: str
    devices: str
    owner_id: int
    ticketType: str
    externalId: int
    tenant: str
    region: str
    requestType: str
    category1: str
    category2: str
    category3: str
    vlan: str
    vrf: str

    class Config:
        orm_mode = True


# Properties to return to client
class Item(ItemInDBBase):
    pass


# Properties properties stored in DB
class ItemInDB(ItemInDBBase):
    pass
