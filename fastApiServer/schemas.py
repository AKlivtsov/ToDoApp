from pydantic import BaseModel, EmailStr, field_validator, Field
from typing import Optional


class LoginUser(BaseModel):
    email: EmailStr
    password: str

    @field_validator('email', mode='before')
    def email_validate(cls, to_validate) -> str:
        if not isinstance(to_validate, str):
            raise ValueError("Почта должна быть строкой")
        
        if len(to_validate) < 8 or len(to_validate) > 120:
            raise ValueError("Некорректная длина почты")
        
        return to_validate
    

class RegUser(BaseModel):
    username: str
    email: EmailStr
    password: str
    
    @field_validator('email', mode='before')
    def email_validate(cls, to_validate) -> str:
        if not isinstance(to_validate, str):
            raise ValueError("Почта должна быть строкой")
        
        if len(to_validate) < 8 or len(to_validate) > 120:
            raise ValueError("Некорректная длина почты")
        
        return to_validate
    
    
class Task(BaseModel):
    title: str
    description: str
