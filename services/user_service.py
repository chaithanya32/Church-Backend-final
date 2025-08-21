from sqlalchemy.orm import Session
from models.user import User
from validators.user import UserRegister, UserLogin
from utilities.auth import hash_password, verify_password, create_access_token


def register_user(db: Session, user_data: UserRegister):
    # Check if email is already registered
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise ValueError("Email already registered.")

    # Hash the password
    hashed_pw = hash_password(user_data.password)

    # Create new user
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hashed_pw,
        id_number=user_data.id_number,
        batch=user_data.batch,
        branch=user_data.branch,
        phone_number=user_data.phone_number,
        gender=user_data.gender,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"msg": "User registered successfully."}


def login_user(db: Session, login_data: UserLogin):
    user = db.query(User).filter(User.email == login_data.email).first()

    if not user or not verify_password(login_data.password, user.password_hash):
        raise ValueError("Invalid credentials.")

    access_token = create_access_token(user_id=user.id)
    return {"access_token": access_token, "token_type": "bearer"}
