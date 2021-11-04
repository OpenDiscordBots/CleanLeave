from os import environ as env
from typing import Optional, Tuple

from asyncpg import create_pool


class Database:
    def __init__(self) -> None:
        self._pool = None

    async def ainit(self) -> None:
        self._pool = await create_pool(dsn=env["PG_URI"])

        await self._pool.execute("""
            CREATE TABLE IF NOT EXISTS JoinMessages (
                id BIGINT PRIMARY KEY,
                channel_id BIGINT NOT NULL,
                guild_id BIGINT NOT NULL,
                member_id BIGINT NOT NULL
            );
        """)

    async def member_join(self, message: int, channel: int, guild: int, member: int) -> None:
        await self._pool.execute("INSERT INTO JoinMessages VALUES ($1, $2, $3, $4);", message, channel, guild, member)

    async def get_join_message(self, guild: int, member: int) -> Optional[Tuple[int, int]]:
        msg = await self._pool.fetchrow("SELECT * FROM JoinMessages WHERE guild_id = $1 AND member_id = $2;", guild, member)

        if not msg:
            return None

        await self._pool.execute("DELETE FROM JoinMessages WHERE guild_id = $1 AND member_id = $2;", guild, member)

        return (msg["id"], msg["channel_id"])
