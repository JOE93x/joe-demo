from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from config import SessionLocal

router=APIRouter()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users/")

def create_user(name:str,email:str,db:Session=Depends(get_db)):
    existing=db.query((User).filter(User.email==email).first())
    
    if existing:
        raise HTTPException(status_code=400,detail="Email already eists")
    user=User(name=name,email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/users/")
def get_all_users(db: Session=Depends(get_db)):
    return db.query(User).all()

@router.get("/users/{user_id}")
def get_user(user_id: int,db: Session=Depends(get_db)):
    user=db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    return user


@router.delete("/users/{user_id}")
def delete_user(user_id: int,db: Session=Depends(get_db)):
    user=db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    db.delete(user)
    db.commit()