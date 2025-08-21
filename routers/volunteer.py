from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.volunteer import Volunteer
from models.user import User
from utilities.database import get_db
from utilities.auth import get_current_user

router = APIRouter(prefix="/volunteers", tags=["Volunteers"])

@router.post("/")
def create_volunteer(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Optional: Check if current user is admin or superuser

    # Check if user is already a volunteer
    existing = db.query(Volunteer).filter(Volunteer.user_id == user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="User is already a volunteer")

    new_volunteer = Volunteer(user_id=user_id)
    db.add(new_volunteer)
    db.commit()
    db.refresh(new_volunteer)
    return {"msg": "Volunteer created", "volunteer_id": new_volunteer.id}

@router.get("/me")
def check_if_volunteer(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    volunteer = db.query(Volunteer).filter(Volunteer.user_id == current_user.id).first()
    if not volunteer:
        raise HTTPException(status_code=403, detail="Not a valid volunteer")
    return {"id": volunteer.id, "name": current_user.name}


@router.get("/")
def get_all_volunteers(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Optional: Restrict to admins
    volunteers = db.query(Volunteer).all()
    return [
        {
            "volunteer_id": v.id,
            "user_id": v.user_id
        } for v in volunteers
    ]

def verify_volunteer(user: User, db: Session):
    volunteer = db.query(Volunteer).filter(Volunteer.user_id == user.id).first()
    if not volunteer:
        raise HTTPException(status_code=403, detail="Access denied. Not a volunteer.")
    return volunteer

@router.get("/dashboard")
def volunteer_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify if user is a volunteer
    verify_volunteer(current_user, db)
    
    # Return data for volunteer dashboard
    return {"message": f"Welcome, {current_user.name}. This is the volunteer dashboard."}

@router.delete("/{volunteer_id}")
def delete_volunteer(volunteer_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    volunteer = db.query(Volunteer).filter(Volunteer.id == volunteer_id).first()
    if not volunteer:
        raise HTTPException(status_code=404, detail="Volunteer not found")

    db.delete(volunteer)
    db.commit()
    return {"msg": "Volunteer removed"}
