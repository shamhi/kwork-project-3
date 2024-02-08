from typing import Any, Union

from pyrogram import Client
from pyrogram.types import Update
from pyrogram_patch.middlewares.middleware_types import OnMessageMiddleware
from pyrogram_patch.middlewares import PatchHelper
import aiosqlite


class ConnectDB(OnMessageMiddleware):
    def __init__(self, db_name: str):
        self.db_name = db_name

    async def __call__(
            self,
            update: Update,
            client: Union[Client, Any],
            patch_helper: PatchHelper
    ):

        conn = await aiosqlite.connect(f"app/db/{self.db_name}.db")
        return patch_helper.data.update(conn=conn)
