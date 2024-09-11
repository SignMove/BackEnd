from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from database import get_session
from datetime import datetime
from model.campaign import Campaign
from api.util import upload_files, delete_files

router = APIRouter()

@router.get("/campaign/detail", tags=["Campaign"])
async def campaign_get_detail(id: int, session: Session = Depends(get_session)):
    try:
        statement = select(Campaign).where(Campaign.id == id)
        campaign = session.exec(statement).first()

        if campaign:
            return {"campaign": campaign}
        else:
            raise HTTPException(status_code=404, detail="Campaign not found")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/campaign/list", tags=["Campaign"])
async def campaign_get_list(region: str, keyword: str | None, owner: int | None, session: Session = Depends(get_session)):
    try:
        campaign_list = []

        if owner:
            statement = select(Campaign).where(Campaign.owner == owner)
            campaigns = session.exec(statement).all()
            campaign_list.append(campaigns)
        
        if keyword:
            pass
        
        # todo: region neighbor, keyword recommend

        return campaign_list
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/campaign", tags=["Campaign"])
async def campaign_set(campaign: Campaign, session: Session = Depends(get_session)):
    try:
        statement = select(Campaign).where(
            Campaign.owner == campaign.owner,
            Campaign.created_at == campaign.created_at
        )
        existing_campaign = session.exec(statement).first()

        if existing_campaign:
            existing_campaign.title = campaign.title
            existing_campaign.goal = campaign.goal
            existing_campaign.content = campaign.content
            existing_campaign.region = campaign.region

            delete_files(existing_campaign.images)
            if campaign.upload_images:
                existing_campaign.images = upload_files(campaign.upload_images)
            
            session.add(existing_campaign)
            updated = True
        else:
            campaign.created_at = datetime.now()
            if campaign.upload_images:
                campaign.images = upload_files(campaign.upload_images)

            session.add(campaign)
            updated = False
        
        session.commit()

        return {"updated": updated}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/campaign", tags=["Campaign"])
async def campaign_del(id: int, session: Session = Depends(get_session)):
    try:
        statement = select(Campaign).where(Campaign.id == id)
        campaign = session.exec(statement).first()
        
        if campaign:
            session.delete(campaign)
            session.commit()
            return {"updated": True}
        else:
            return {"updated": False}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
