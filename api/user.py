from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from database import get_session
from model.user import User

router = APIRouter()

@router.get("/user", tags=["User"])
async def user_get(email: str, session: Session = Depends(get_session)):
    """
    주어진 이메일로 사용자를 조회합니다.

    Args:
        email (str): 조회할 사용자의 이메일 주소.
        session (Session): 데이터베이스 세션.

    Returns:
        dict: 
            - "exists" (bool): 사용자가 존재하는지 여부.
            - "user" (User, optional): 사용자가 존재하는 경우 사용자 객체, 그렇지 않으면 없음.
    """

    try:
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()
        
        if user:
            return {"exists": True, "user": user}
        else:
            return {"exists": False}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/user", tags=["User"])
async def user_set(user: User, session: Session = Depends(get_session)):
    """
    사용자 정보를 추가하거나 기존 사용자 정보를 업데이트합니다.

    Args:
        user (User): 생성하거나 업데이트할 사용자 객체.
        session (Session): 데이터베이스 세션.

    Returns:
        dict: 
            - "updated" (bool): 사용자가 새로 추가되었는지 수정되었는지 여부.
    """

    try:
        statement = select(User).where(User.email == user.email)
        existing_user = session.exec(statement).first()

        if existing_user:
            existing_user.nickname = user.nickname
            existing_user.description = user.description
            existing_user.region = user.region

            session.add(existing_user)
            updated = True
        else:
            session.add(user)
            updated = False
        
        session.commit()
        session.refresh(existing_user if existing_user else user)
        
        return {"updated": updated}
    
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/user", tags=["User"])
async def user_del(email: str, session: Session = Depends(get_session)):
    """
    주어진 이메일로 사용자를 삭제합니다.

    Args:
        email (str): 조회할 사용자의 이메일 주소.
        session (Session): 데이터베이스 세션.

    Returns:
        dict: 
            - "updated" (bool): 사용자가 삭제되었는지 여부.
    """

    try:
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()
        
        if user:
            session.delete(user)
            session.commit()
            return {"updated": True}
        else:
            return {"updated": False}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
