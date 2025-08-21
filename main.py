# main.py
from fastapi import FastAPI
from models import user, attendance_log, email_notification
from utilities.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware


from routers import user
from routers import attendance_log
from routers import email_notification
from routers import password_reset
from routers import volunteer
from routers import attendance_code_in
from routers import attendace_code_out
from routers import email_tasks
from routers import attendancd_temporary

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"msg": "Welcome to the Church App backend"}



# Allow frontend to access backend
origins = [
    "http://localhost:5173",  # Vite frontend
    "http://127.0.0.1:5173"   # optional, sometimes Vite uses this
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # allow these origins
    allow_credentials=True,
    allow_methods=["*"],    # allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],    # allow all headers
)


app.include_router(user.router)
app.include_router(password_reset.router)
app.include_router(volunteer.router)
app.include_router(attendance_code_in.router)
app.include_router(attendace_code_out.router)
app.include_router(attendance_log.router)
app.include_router(attendancd_temporary.router)
app.include_router(email_notification.router)
app.include_router(email_tasks.router)
