from dotenv import load_dotenv
from os import environ as env

from corded import CordedClient, GatewayEvent, Route
from loguru import logger

from .db import Database

load_dotenv()

bot = CordedClient(env["TOKEN"], intents=515)
db = Database()

@bot.on("message_create")
async def on_message_create(event: GatewayEvent) -> None:
    if event.d["type"] == 7:
        message = int(event.d["id"])
        channel = int(event.d["channel_id"])
        guild = int(event.d["guild_id"])
        member = int(event.d["author"]["id"])

        await db.member_join(message, channel, guild, member)

@bot.on("guild_member_remove")
async def on_member_leave(event: GatewayEvent) -> None:
    guild = int(event.d["guild_id"])
    member = int(event.d["user"]["id"])

    msg = await db.get_join_message(guild, member)

    if not msg:
        return

    logger.info(f"Removing join message for {member} in guild {guild}")

    route = Route("/channels/{channel_id}/messages/{message_id}", message_id=msg[0], channel_id=msg[1])

    await bot.http.request("DELETE", route, expect="response")


if __name__ == "__main__":
    bot.loop.run_until_complete(db.ainit())

    logger.info("Starting the bot...")

    bot.start()
