import asyncio
import logging
from os.path import exists

from pyrogram import Client, compose
from pyrogram_patch import patch
import aiosqlite

from app.config import Config
from app.middlewares import ConnectDB
from app.db import Database

async def main():
    app1 = Client(
        name=Config.APP_NAME1,
        api_id=Config.API_ID1,
        api_hash=Config.API_HASH1,
        plugins=dict(root='plugins' if exists('plugins') else 'app/plugins')
    )

    app2 = Client(
        name=Config.APP_NAME2,
        api_id=Config.API_ID2,
        api_hash=Config.API_HASH2,
        plugins=dict(root='plugins' if exists('plugins') else 'app/plugins')
    )

    patch_manager1 = patch(app=app1)
    patch_manager2 = patch(app=app2)

    patch_manager1.include_middleware(ConnectDB(db_name=app1.name))
    patch_manager2.include_middleware(ConnectDB(db_name=app2.name))

    for app in (app1, app2):
        async with aiosqlite.connect(f'app/db/{app.name}.db') as temp_conn:
            db = Database(conn=temp_conn)
            await db.create_tables()

    await compose([app1, app2])


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
