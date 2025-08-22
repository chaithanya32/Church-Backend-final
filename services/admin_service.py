from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.admin import Admin
from models.user import User
from validators.admin import AdminCreate

def create_admin(db: Session, admin_in: AdminCreate):
    # find user by email
    user = db.query(User).filter(User.email == admin_in.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # check if already admin
    existing = db.query(Admin).filter(Admin.user_id == user.id).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is already an admin")

    new_admin = Admin(user_id=user.id)
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin

def get_admins(db: Session):
    return db.query(Admin).all()

def delete_admin(db: Session, admin_id: int):
    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")

    db.delete(admin)
    db.commit()
    return {"message": "Admin removed successfully"}
