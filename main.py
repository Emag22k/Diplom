from fastapi import FastAPI
from routers.admin import admin_router
from routers.user import user_router
from database import engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url='/')

app.include_router(admin_router)
app.include_router(user_router)


