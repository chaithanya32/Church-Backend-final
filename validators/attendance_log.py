from pydantic import BaseModel, constr
from enum import Enum
from datetime import datetime

class StatusEnum(str, Enum):
    present = "present"
    absent = "absent"

class AttendanceLogCreate(BaseModel):
    status: StatusEnum

class AttendanceLogOut(BaseModel):
    id: int
    user_id: int
    status: str
    timestamp: datetime

    class Config:
        orm_mode = True


class AttendanceCodeInput(BaseModel):
    code: constr(min_length=6, max_length=6)