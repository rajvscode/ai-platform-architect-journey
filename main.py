from fastapi import FastAPI
from api.routes import router
from core.limiter import limiter
from rag import initialize_index

app = FastAPI()

app.state.limiter = limiter
app.include_router(router)

@app.on_event("startup")
def startup_event():
    print("Initializing vector index...")
    initialize_index()
    print("Vector index ready")