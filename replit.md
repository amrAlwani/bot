# Workspace — Two Telegram Bot Projects

---

## Project 1: BMQA / R3D Bot (`bmqa/`)

A feature-rich Arabic-language Telegram group-management bot.

### Configuration
- `BOT_TOKEN` — Telegram bot token (secret)
- `OWNER_ID` — Bot owner's Telegram ID (default: 7264011066)

### Dependencies
- `python-telegram-bot==21.0.1`, `redis` (DummyRedis fallback), `kvsqlite`
- `yt-dlp`, `pydub`, `mutagen`, `SpeechRecognition`, `gTTS`, `shazamio`, `Pillow`, `akinator`

### Workflow
`cd bmqa && python main.py`

### Key fixes applied
- Lazy Redis init in `config.py` (no blocking ping at import time)
- Fixed 9+ missing `await` on async PTB calls in `Plugins/all.py`
- Fixed `r.set()` missing value arg (line 388)
- Fixed deprecated `asyncio.get_event_loop()` in `private_sudos.py`

---

## Project 2: MenuBuilder Bot (`menubuilder/`)

A **bot factory** — users add their own bot tokens and build fully-featured menu bots with no coding.

### Architecture
- **Main bot** — management interface for bot owners
- **Child bots** — user-configured bots running as asyncio tasks in the same process

### Setup
```
cp menubuilder/.env.example menubuilder/.env
# Fill in MAIN_BOT_TOKEN and MAIN_BOT_ADMIN
cd menubuilder && pip install -r requirements.txt
python main.py
```

### Environment Variables (`.env`)
| Variable | Description | Default |
|---|---|---|
| `MAIN_BOT_TOKEN` | Token of the main management bot | required |
| `MAIN_BOT_ADMIN` | Telegram ID of the platform admin | required |
| `DB_PATH` | SQLite database file path | `menubuilder.db` |
| `MAX_BOTS_PER_USER` | Max bots per user | `5` |
| `MAIL_DELAY` | Delay (seconds) between broadcast messages | `0.05` |

### Project Structure
```
menubuilder/
├── main.py                  # Entry point — starts main bot + restores child bots
├── config.py                # Env var loader
├── .env.example             # Example environment file
├── requirements.txt         # aiosqlite, python-telegram-bot>=21, python-dotenv
├── models/
│   └── database.py          # SQLite schema (14 tables), init_db, setting_get/set
├── utils/
│   ├── keyboards.py         # All InlineKeyboardMarkup builders
│   ├── macros.py            # Process {name} {balance} {id} {ref_link} etc.
│   └── bot_runner.py        # Start/stop/track child bot Application instances
└── handlers/
    ├── start.py             # /start, home panel, help, my_stats
    ├── bot_manager.py       # Add bot (token), list, start/stop, delete
    ├── menu_builder.py      # Create/edit menus and buttons (text, url, submenu)
    ├── broadcast.py         # Mailing to all bot users (text + media)
    ├── settings.py          # Maintenance mode, captcha, welcome text, referral bonus
    ├── shop.py              # eShop — categories, products, cart, orders (admin side)
    └── child_bot.py         # Child bot logic: /start, menu nav, shop, captcha, referrals
```

### Features
| Feature | Description |
|---|---|
| Multi-bot management | Add unlimited bots via BotFather token |
| Menu builder | Create menus with text-reply, URL, and submenu buttons |
| Broadcast/mailing | Send text & media to all users with stats |
| Referral system | Auto-track referrals, award configurable bonus |
| User balance | Virtual balance per user per bot |
| eShop | Categories → Products → Cart → Orders |
| Admin panel | Add/remove bot admins |
| Maintenance mode | Block non-admins with custom message |
| Captcha | Math-question verification on /start |
| Welcome message | Custom welcome with macro variables |
| Statistics | Users, orders, mailings, referrals |
| Macros | {name} {username} {id} {balance} {users} {ref_link} |

### Database Schema (SQLite)
`managed_bots`, `bot_admins`, `bot_users`, `menus`, `menu_buttons`, `bot_commands`,
`bot_settings`, `shop_categories`, `shop_products`, `cart_items`, `orders`,
`mailing_history`, `referrals`
