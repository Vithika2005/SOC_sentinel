# enterprise/shared/schemas.py

from pydantic import BaseModel, EmailStr, constr, validator

class UserCreate(BaseModel):
    username: constr(min_length=3)
    email: EmailStr
    password: constr(min_length=8)

    @validator('username')
    def validate_username(cls, v):
        if 'admin' in v:
            raise ValueError('Username cannot contain "admin"')
        return v

class OrderCreate(BaseModel):
    user_id: int
    product: str
    quantity: int
