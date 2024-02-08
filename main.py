import asyncio
import logging
from os.path import exists

from pyrogram import Client, idle
from pyrogram_patch import patch
import aiosqlite

from app.config import Config
from app.middlewares import ConnectDB
from app.db import Database

async def main():
    app = Client(
        name=Config.APP_NAME,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        plugins=dict(root='plugins' if exists('plugins') else 'app/plugins')
    )

    patch_manager = patch(app=app)
    patch_manager.include_middleware(ConnectDB(db_name="app1_db"))

    await app.start()

    async with aiosqlite.connect('app/db/app1_db.db') as temp_conn:
        db = Database(conn=temp_conn)
        await db.create_tables()

    await idle()
    await app.stop(block=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
