from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from database import conn
from contextlib import asynccontextmanager

from api import user
from api import campaign
from api import news

@asynccontextmanager
async def lifespan(app: FastAPI):
    conn()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(user.router)
app.include_router(campaign.router)
app.include_router(news.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
	import uvicorn
	uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
