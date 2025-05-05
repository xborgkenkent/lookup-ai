from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

router = APIRouter(tags=["main"])

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initial route
@router.get("/")
async def root():
    return {"message": "Welcome to the Restaurant Search API!"}

app.include_router(router)