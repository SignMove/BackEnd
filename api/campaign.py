from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from database import get_session
from datetime import datetime
from model.campaign import Campaign

router = APIRouter()

@router.post("/campaign/create")
async def campaign_create(campaign: Campaign, session: Session = Depends(get_session)):
    try:
        campaign.created_at = datetime.now()
        # todo: image

        session.add(campaign)
        session.commit()
        session.refresh(campaign)

        return {"finish": True}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
