# routers/user.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utilities.database import get_db
from models.user import User
from validators.user import UserRegister, UserOut
from utilities.auth import get_current_user, hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from models.volunteer import Volunteer

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserOut)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    if db.query(User).filter_by(email=user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        id_number=user_data.id_number,
        batch=user_data.batch,
        branch=user_data.branch,
        phone_number=user_data.phone_number,
        gender=user_data.gender
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

#login
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
def get_current_user_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    volunteer = db.query(Volunteer).filter(
        Volunteer.user_id == current_user.id
    ).first()

    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "is_volunteer": volunteer is not None
    }

@router.delete("/hard-delete", response_model=dict)
def hard_delete_current_user(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == current_user.id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    db.delete(user)
    db.commit()
    return {"msg": "User deleted permanently."}
