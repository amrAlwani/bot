import aiosqlite
import json
from config import DB_PATH


async def get_db() -> aiosqlite.Connection:
    conn = await aiosqlite.connect(DB_PATH)
    conn.row_factory = aiosqlite.Row
    await conn.execute("PRAGMA journal_mode=WAL")
    await conn.execute("PRAGMA foreign_keys=ON")
    return conn


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        await db.executescript("""
            CREATE TABLE IF NOT EXISTS managed_bots (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                token       TEXT    UNIQUE NOT NULL,
                bot_id      INTEGER,
                username    TEXT,
                name        TEXT,
                owner_id    INTEGER NOT NULL,
                is_active   INTEGER DEFAULT 0,
                created_at  TEXT    DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS bot_admins (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                bot_token  TEXT    NOT NULL,
                user_id    INTEGER NOT NULL,
                added_at   TEXT    DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(bot_token, user_id)
            );

            CREATE TABLE IF NOT EXISTS bot_users (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                bot_token   TEXT    NOT NULL,
                user_id     INTEGER NOT NULL,
                username    TEXT,
                first_name  TEXT,
                referrer_id INTEGER,
                balance     REAL    DEFAULT 0,
                joined_at   TEXT    DEFAULT CURRENT_TIMESTAMP,
                is_blocked  INTEGER DEFAULT 0,
                UNIQUE(bot_token, user_id)
            );

            CREATE TABLE IF NOT EXISTS menus (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                bot_token   TEXT    NOT NULL,
                menu_key    TEXT    NOT NULL,
                title       TEXT    NOT NULL,
                text        TEXT,
                parent_key  TEXT,
                UNIQUE(bot_token, menu_key)
            );

            CREATE TABLE IF NOT EXISTS menu_buttons (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                bot_token    TEXT    NOT NULL,
                menu_key     TEXT    NOT NULL,
                label        TEXT    NOT NULL,
                btn_type     TEXT    DEFAULT 'callback',
                response     TEXT,
                url          TEXT,
                submenu_key  TEXT,
                position     INTEGER DEFAULT 0,
                per_row      INTEGER DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS bot_commands (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                bot_token TEXT    NOT NULL,
                command   TEXT    NOT NULL,
                response  TEXT,
                UNIQUE(bot_token, command)
            );

            CREATE TABLE IF NOT EXISTS bot_settings (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                bot_token TEXT    NOT NULL,
                key       TEXT    NOT NULL,
                value     TEXT,
                UNIQUE(bot_token, key)
            );

            CREATE TABLE IF NOT EXISTS shop_categories (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                bot_token   TEXT    NOT NULL,
                name        TEXT    NOT NULL,
                description TEXT,
                emoji       TEXT    DEFAULT '📦'
            );

            CREATE TABLE IF NOT EXISTS shop_products (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                bot_token     TEXT    NOT NULL,
                category_id   INTEGER,
                name          TEXT    NOT NULL,
                description   TEXT,
                price         REAL    NOT NULL DEFAULT 0,
                emoji         TEXT    DEFAULT '🛍️',
                is_available  INTEGER DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS cart_items (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                bot_token   TEXT    NOT NULL,
                user_id     INTEGER NOT NULL,
                product_id  INTEGER NOT NULL,
                quantity    INTEGER DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS orders (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                bot_token   TEXT    NOT NULL,
                user_id     INTEGER NOT NULL,
                items_json  TEXT,
                total       REAL,
                status      TEXT    DEFAULT 'pending',
                created_at  TEXT    DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS mailing_history (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                bot_token    TEXT    NOT NULL,
                message_text TEXT,
                sent_count   INTEGER DEFAULT 0,
                fail_count   INTEGER DEFAULT 0,
                created_at   TEXT    DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS referrals (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                bot_token   TEXT    NOT NULL,
                referrer_id INTEGER NOT NULL,
                referred_id INTEGER NOT NULL,
                created_at  TEXT    DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(bot_token, referred_id)
            );
        """)
        await db.commit()


async def setting_get(bot_token: str, key: str, default=None):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT value FROM bot_settings WHERE bot_token=? AND key=?",
            (bot_token, key)
        ) as cur:
            row = await cur.fetchone()
            return row["value"] if row else default


async def setting_set(bot_token: str, key: str, value):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO bot_settings(bot_token,key,value) VALUES(?,?,?) "
            "ON CONFLICT(bot_token,key) DO UPDATE SET value=excluded.value",
            (bot_token, key, str(value) if value is not None else None)
        )
        await db.commit()


async def setting_del(bot_token: str, key: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "DELETE FROM bot_settings WHERE bot_token=? AND key=?",
            (bot_token, key)
        )
        await db.commit()
