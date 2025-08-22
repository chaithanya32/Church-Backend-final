from utilities.auth import get_current_admin, get_current_user, HTTPException
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utilities.database import get_db
from validators.admin import AdminCreate, AdminOut
from services import admin_service
from typing import List
from models.admin import Admin
from models.user import User

router = APIRouter(prefix="/admins", tags=["Admins"])

@router.post("/", response_model=AdminOut)
def add_admin(admin_in: AdminCreate, db: Session = Depends(get_db)):
    return admin_service.create_admin(db, admin_in)

@router.get("/me")
def get_current_admin(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # check if user is admin
    admin = db.query(Admin).filter(Admin.user_id == current_user.id).first()

    if not admin:
        raise HTTPException(status_code=403, detail="Not an admin")

    return {
        "id": admin.id,                # from admin table
        "user_id": admin.user_id,      # from admin table
        "name": current_user.name,     # from users table
        "email": current_user.email    # from users table (if you want)
    }

@router.get("/", response_model=List[AdminOut])
def list_admins(db: Session = Depends(get_db)):
    return admin_service.get_admins(db)

@router.delete("/{admin_id}")
def remove_admin(admin_id: int, db: Session = Depends(get_db)):
    return admin_service.delete_admin(db, admin_id)
