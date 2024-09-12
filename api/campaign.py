from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select, or_, desc
from database import get_session
from datetime import datetime
from typing import Optional
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
async def campaign_get_list(limit: int, region: str, req: Optional[str | int] = Query(None), session: Session = Depends(get_session)):
    try:
        campaign_list = []

        if req != None:
            if isinstance(req, int):
                statement = select(Campaign).where(Campaign.owner == req)
            else:
                statement = select(Campaign).where(or_(
                    Campaign.owner.ilike(f'%{req}%'),
                    Campaign.title.ilike(f'%{req}%'),
                    Campaign.content.ilike(f'%{req}%'),
                ))
        
        else:
            # todo: region
            statement = select(Campaign)
        
        campaigns = session.exec(statement.order_by(desc(Campaign.created_at)).limit(limit)).all()
        campaign_list.append(campaigns)

        return campaign_list
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/campaign", tags=["Campaign"])
async def campaign_set(campaign: Campaign, upload_images: Optional[list[str]] = Query(None), session: Session = Depends(get_session)):
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

            await delete_files(existing_campaign.images)
            if upload_images:
                existing_campaign.images = await upload_files(upload_images)
            
            session.add(existing_campaign)
            updated = True
        else:
            campaign.created_at = datetime.now()
            if upload_images:
                campaign.images = await upload_files(upload_images)

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
