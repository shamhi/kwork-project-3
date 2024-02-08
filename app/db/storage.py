import aiosqlite

from app.utils import scripts


class Database:
    def __init__(self, conn: aiosqlite.Connection):
        self.db: aiosqlite.Connection = conn

    async def create_tables(self):
        await self.db.execute(sql="""CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tg_id BIGINT,
                    username VARCHAR(32),
                    firstname VARCHAR(64),
                    messages_count BIGINT)""")

        await self.db.execute(sql="""CREATE TABLE IF NOT EXISTS history(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data TEXT,
                    tg_id BIGINT,
                    FOREIGN KEY(tg_id) REFERENCES users(tg_id))""")
        await self.db.commit()

    async def add_history_messages(self, tg_id: int, history: list[dict[str, str]]):
        await self.db.execute(sql="UPDATE history SET data=? WHERE tg_id=?", parameters=(history, tg_id,))
        await self.db.commit()

    async def get_history_messages(self, tg_id: int):
        data = await self.db.execute(sql="SELECT data FROM history WHERE tg_id=?", parameters=(tg_id,))
        history = await data.fetchone()

        try: return scripts.get_loaded_data(history[0]) or []
        except: return scripts.get_loaded_data(history) or []

    async def check_user(self, tg_id: int):
        user = await self.db.execute(sql="SELECT id FROM users WHERE tg_id=?", parameters=(tg_id,))
        data = await user.fetchone()

        return False if not data else True

    async def register_user(self, tg_id: int, username: str, firstname: str):
        if not await self.check_user(tg_id=tg_id):
            await self.db.execute(sql="INSERT INTO users(tg_id, username, firstname, messages_count) VALUES(?, ?, ?, ?)",
                                  parameters=(tg_id, username, firstname, 0))
            await self.db.execute(sql="INSERT INTO history(tg_id) VALUES(?)", parameters=(tg_id,))
            await self.db.commit()

    async def add_message(self, tg_id: int):
        await self.db.execute(sql="UPDATE users SET messages_count=messages_count+1 WHERE tg_id=?",
                              parameters=(tg_id,))
        await self.db.commit()
