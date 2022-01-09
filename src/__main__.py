from datetime import datetime
from json import dumps
from os import environ as env

from disnake import Client, Message, MessageType, Intents, Member
from disnake.http import Route
from dotenv import load_dotenv
from loguru import logger
from libodb import APIClient

load_dotenv()

intents = Intents.none()
intents.guilds = True
intents.guild_messages = True
intents.members = True

client = Client(intents=intents)
api = APIClient(env["API_TOKEN"], kv_ns="cleanleave")

@client.event
async def on_message(message: Message) -> None:
    if message.type != MessageType.new_member:
        return

    assert message.guild

    if message.author.current_timeout and message.author.current_timeout > datetime.utcnow():
        await message.delete()
        return

    await api.kv_set(f"{message.guild.id}.{message.author.id}", dumps({
        "message": message.id,
        "channel": message.channel.id
    }))

@client.event
async def on_member_remove(member: Member) -> None:
    try:
        msg = await api.kv_get(f"{member.guild.id}.{member.id}")
    except Exception as e:
        logger.error(e)
        return

    if not msg:
        return

    logger.info(f"Removing join message for {member.id} in guild {member.guild.id}: {type(msg)}")

    route = Route("DELETE", "/channels/{channel_id}/messages/{message_id}", message_id=msg["message"], channel_id=msg["channel"])

    await client.http.request(route)


if __name__ == "__main__":
    logger.info("Starting the bot...")

    client.run(env["TOKEN"])
