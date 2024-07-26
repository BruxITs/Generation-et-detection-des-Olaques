from pydantic import BaseModel

class LicensePlateBase(BaseModel):
    filename: str
    detected: bool

class LicensePlateCreate(LicensePlateBase):
    pass

class LicensePlate(LicensePlateBase):
    id: int

    class Config:
        orm_mode = True
