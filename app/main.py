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
    await ctx.connect(auto_subscribe=AutoSubscribe.SUBSCRIBE_ALL)

    # 2. Initialize LLM and Avatar
    # Ensure create_llm() is configured with a system prompt that enforces brevity
    llm = create_llm()
    avatar = create_avatar()

    # 3. Configure the Session for stable turn-taking
    # Increased endpointing delay prevents the agent from cutting in too quickly
    session = AgentSession(
        llm=llm,
        video_sampler=VoiceActivityVideoSampler(speaking_fps=0, silent_fps=0),
        preemptive_generation=False,
        min_endpointing_delay=1.5,  # Wait 1.5s of silence before replying
        max_endpointing_delay=5.0,
    )

    # 4. Initialize Avatar and Session
    # The avatar provides the visual/audio output for the LLM's responses
    await avatar.start(session, room=ctx.room)
    
    # We pass the system instructions here to control Gemini's behavior
    # Added instructions to enforce one-sentence replies to stop the "run-on" sentences
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

    # 5. Initial Greeting
    session.generate_reply(instructions="Give a very brief 1-sentence greeting.")
    
    # 6. Maintain Connection
    await keep_alive(ctx)

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))