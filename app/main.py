import asyncio
import os
from livekit.agents import (
    Agent,
    AgentSession,
    AutoSubscribe,
    JobContext,
    WorkerOptions,
    cli,
)
from livekit.agents.voice import VoiceActivityVideoSampler, room_io
from app.llm.gemini import create_llm
from app.avatar.anam_avatar import create_avatar
from app.avatar.persona import SYSTEM_INSTRUCTIONS
from app.utils.safety import keep_alive

async def entrypoint(ctx: JobContext):
    # 1. Connect and subscribe to all tracks
    # Using the standard connection method from your main entrypoint
    await ctx.connect(auto_subscribe=AutoSubscribe.SUBSCRIBE_ALL)

    # 2. Initialize LLM and Avatar
    # Ensure create_llm() uses your NEW Gemini API key from environment variables
    llm = create_llm()
    avatar = create_avatar()

    # 3. Configure the Session for stable sync between Gemini and Anam
    # Increased endpointing delays prevent the "marking playout as done arbitrarily" errors
    session = AgentSession(
        llm=llm,
        video_sampler=VoiceActivityVideoSampler(speaking_fps=0, silent_fps=0),
        preemptive_generation=False,
        min_endpointing_delay=2.0,  # Increased to 2s to allow Avatar buffer to sync
        max_endpointing_delay=5.0,
    )

    # 4. Initialize Avatar and Session
    # The avatar provides the visual/audio output for the LLM's responses
    await avatar.start(session, room=ctx.room)
    
    # 5. Production Instructions
    # Added strict rules to enforce one-sentence replies to stop the "run-on" sentences
    production_instructions = (
        f"{SYSTEM_INSTRUCTIONS}\n"
        "STRICT RULE: Reply in only ONE or TWO short sentences. "
        "Do not speak long paragraphs. Wait for the user to reply."
    )

    await session.start(
        agent=Agent(instructions=production_instructions),
        room=ctx.room,
        room_input_options=room_io.RoomInputOptions(video_enabled=True),
    )

    # 6. Initial Greeting
    # Triggers a brief greeting once the session is live
    session.generate_reply(instructions="Give a very brief 1-sentence greeting.")
    
    # 7. Maintain Connection
    # Uses the utility to keep the process alive while the user is connected
    await keep_alive(ctx)

if __name__ == "__main__":
    # Required for the LiveKit CLI to start the worker correctly
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
