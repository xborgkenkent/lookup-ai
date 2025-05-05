from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from routes.fsq_routes import router as restaurant_router

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

# Restaurant router
app.include_router(restaurant_router, prefix="/api", tags=["restaurant"])

# Initial route
@router.get("/")
async def root():
    return {"message": "Welcome to the Restaurant Search API!"}


app.include_router(router)