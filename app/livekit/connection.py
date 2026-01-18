import asyncio
from livekit.agents import JobContext, AutoSubscribe
from app.config import LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET

async def connect_room(ctx: JobContext):
    await asyncio.wait_for(
        ctx.connect(
            url=LIVEKIT_URL,
            api_key=LIVEKIT_API_KEY,
            api_secret=LIVEKIT_API_SECRET,
            auto_subscribe=AutoSubscribe.SUBSCRIBE_ALL,
        ),
        timeout=10
    )
