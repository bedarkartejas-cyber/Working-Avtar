from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    WorkerOptions,
    cli,
)
from livekit.agents.voice import VoiceActivityVideoSampler, room_io

from app.logger import setup_logger
from app.avatar.anam_avatar import create_avatar
from app.llm.gemini import create_llm
from app.livekit.connection import connect_room
from app.utils.safety import keep_alive

logger = setup_logger("avatar-agent")

async def entrypoint(ctx: JobContext):
    logger.info(f"🤖 Agent joining room: {ctx.room.name}")

    await connect_room(ctx)

    llm = create_llm()
    avatar = create_avatar()

    session = AgentSession(
        llm=llm,
        video_sampler=VoiceActivityVideoSampler(
            speaking_fps=0,
            silent_fps=0
        ),
        preemptive_generation=False,
    )

    await avatar.start(session, room=ctx.room)

    await session.start(
        agent=Agent(),
        room=ctx.room,
        room_input_options=room_io.RoomInputOptions(
            video_enabled=True
        ),
    )

    session.generate_reply(
        instructions="Greet the user politely and ask how you can help."
    )

    logger.info("✅ Avatar LIVE")
    await keep_alive(ctx)

if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(entrypoint_fnc=entrypoint)
    )
