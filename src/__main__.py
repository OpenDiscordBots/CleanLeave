from asyncio import run
from dotenv import load_dotenv
from os import environ as env

from bauxite import HTTPClient, GatewayClient, Route
from loguru import logger

from .db import Database

load_dotenv()

http = HTTPClient(env["TOKEN"])
db = Database()

async def on_message_create(data: dict) -> None:
    if data["type"] == 7:
        message = int(data["id"])
        channel = int(data["channel_id"])
        guild = int(data["guild_id"])
        member = int(data["author"]["id"])

        await db.member_join(message, channel, guild, member)

async def on_member_leave(data: dict) -> None:
    guild = int(data["guild_id"])
    member = int(data["user"]["id"])

    msg = await db.get_join_message(guild, member)

    if not msg:
        return

    logger.info(f"Removing join message for {member} in guild {guild}")

    route = Route("DELETE", "/channels/{channel_id}/messages/{message_id}", message_id=msg[0], channel_id=msg[1])

    await http.request(route)

async def dispatch(_shard, _direction, data: dict) -> None:
    if not (t := data.get("t")):
        return

    if t == "MESSAGE_CREATE":
        await on_message_create(data)
        return

    if t == "GUILD_MEMBER_REMOVE":
        await on_member_leave(data)
        return

async def main() -> None:
    await db.ainit()

    gateway = GatewayClient(http, 515, callbacks=[dispatch])

    await gateway.spawn_shards()


if __name__ == "__main__":
    logger.info("Starting the bot...")

    run(main())
