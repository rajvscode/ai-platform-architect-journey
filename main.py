from fastapi import FastAPI
from api.routes import router
from core.limiter import limiter

app = FastAPI()

app.state.limiter = limiter
app.include_router(router)