from fastapi import APIRouter
from livekit import api
from app.config import (
    LIVEKIT_API_KEY,
    LIVEKIT_API_SECRET,
    LIVEKIT_URL
)

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/livekit/token")
def create_token(room: str, identity: str):
    token = api.AccessToken(
        LIVEKIT_API_KEY,
        LIVEKIT_API_SECRET
    ).with_identity(identity).with_grants(
        api.VideoGrants(room_join=True, room=room)
    )
    return {
        "token": token.to_jwt(),
        "url": LIVEKIT_URL
    }
