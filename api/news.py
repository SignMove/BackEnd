from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select, and_, desc
from database import get_session
from datetime import datetime
from feedparser import parse
from bs4 import BeautifulSoup
from requests import get
from model.news import News
from api.util import delete_files
from model.dto import Comment

router = APIRouter()

@router.put("/news", tags=["News"])
async def news_fetch(session: Session = Depends(get_session)):
    try:
        rss_url = 'https://www.mk.co.kr/rss/30200030/'
        feed = parse(rss_url)
        cnt = 0

        for entry in feed.entries:
            news = News()
            res = get(entry.link)
            soup = BeautifulSoup(res.content, 'html.parser')

            post_content = []
            paragraphs = soup.find_all('p', refid=True)
            
            for paragraph in paragraphs:
                post_content.append(paragraph.get_text(strip=True))
            
            time_area = soup.find('div', class_='time_area')
            if time_area:
                dt_tags = time_area.find_all('dl', class_='registration')
                for dt_tag in dt_tags:
                    dt_text = dt_tag.find('dt').get_text(strip=True)
                    if "입력" in dt_text:
                        created_at = dt_tag.find('dd').get_text(strip=True)
                        break
            
            image = soup.find('img')
            date_format = "%Y-%m-%d %H:%M:%S"

            news.created_at = datetime.strptime(created_at, date_format)
            news.image = image['src'] if image else ''
            news.title = entry.title
            news.content = '\n'.join(post_content)

            statement = select(News).where(and_(
                News.created_at == news.created_at,
                News.title == news.title
            ))
            existing_news = session.exec(statement).first()

            if not existing_news:
                session.add(news)
                cnt += 1
        
        session.commit()

        return {"fetched": cnt}
    
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/news/detail", tags=["News"])
async def news_get_detail(id: int, session: Session = Depends(get_session)):
    try:
        statement = select(News).where(News.id == id)
        news = session.exec(statement).first()

        if news:
            return {"news": news}
        else:
            raise HTTPException(status_code=404, detail="News not found")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/news/list", tags=["News"])
async def news_get_list(limit: int, session: Session = Depends(get_session)):
    try:
        statement = select(News).order_by(desc(News.created_at)).limit(limit)
        news = session.exec(statement).all()

        if news:
            return {"news": news}
        else:
            raise HTTPException(status_code=404, detail="News not found")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/news", tags=["News"])
async def news_del(id: int, session: Session = Depends(get_session)):
    try:
        statement = select(News).where(News.id == id)
        news = session.exec(statement).first()
        
        if news:
            session.delete(news)
            session.commit()
            return {"updated": True}
        else:
            return {"updated": False}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/news/comment", tags=["News"])
async def news_comment_add(id: int, comment: Comment, session: Session = Depends(get_session)):
    try:
        statement = select(News).where(News.id == id)
        news = session.exec(statement).first()

        if news:
            news.comment_add(comment)
            session.add(news)
            session.commit()

            return {"updated": True}
        else:
            return {"updated": False}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/news/comment", tags=["News"])
async def news_comment_del(id: int, comment_id: int, session: Session = Depends(get_session)):
    try:
        statement = select(News).where(News.id == id)
        news = session.exec(statement).first()

        if news:
            news.comment_del(comment_id)
            session.add(news)
            session.commit()

            return {"updated": True}
        else:
            return {"updated": False}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
