import asyncio

async def keep_alive(ctx):
    shutdown = asyncio.Future()

    @ctx.room.on("disconnected")
    def on_disconnect(reason):
        if not shutdown.done():
            shutdown.set_result(None)

    await shutdown
