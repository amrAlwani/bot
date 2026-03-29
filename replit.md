# BMQA Telegram Bot

## Project Overview
A Python Telegram bot (R3D Bot) built with `python-telegram-bot==21.0.1`. It provides group management, media downloading, games, custom filters/ranks, and other Telegram group utilities. The bot is written in Arabic/English and targets Arabic-speaking Telegram communities.

## Project Structure
```
bmqa/
├── main.py              # Main bot entry point, registers all handlers
├── config.py            # Configuration: Redis/DummyRedis, TOKEN, OWNER_ID, DB setup
├── information.py       # Fallback token info
├── requirements.txt     # Python dependencies
├── clean.py             # Cleanup utilities
├── convert_plugins.py   # Plugin conversion helpers
├── helpers/             # Helper modules
│   ├── Ranks.py         # Rank/permission system
│   ├── utils.py         # General utilities
│   ├── games.py         # Game helpers
│   ├── memes.py         # Meme helpers
│   ├── quran.py         # Quran data
│   ├── persianData.py   # Persian data
│   └── get_create.py    # Get/create helpers
└── Plugins/             # Feature plugins
    ├── all.py           # Core commands
    ├── welcome_and_rules.py
    ├── fun.py
    ├── games.py
    ├── downloader.py    # Media download (YouTube, etc.)
    ├── mute_and_gban.py
    ├── set_ranks.py / get_ranks.py / del_ranks.py / customRank.py
    ├── customCommad.py / customFilter.py / globalFilters.py
    ├── custom_plugin.py
    ├── group_update.py
    ├── id.py
    ├── sarhni.py
    ├── whisper.py
    ├── replace.py
    └── private&sudos.py
```

## Configuration & Environment Variables
- `BOT_TOKEN` - Telegram bot token (required, set as secret)
- `OWNER_ID` - Bot owner's Telegram user ID (default: 7264011066)
- `BOT_NAME` / `NAME` - Bot display name

## Dependencies
- `python-telegram-bot==21.0.1` - Telegram Bot API framework
- `redis` / `DummyRedis` (fallback) - Session/state storage
- `kvsqlite` - SQLite-backed key-value store (ytdb, sounddb, wsdb)
- `yt-dlp` - YouTube/media downloading
- `pydub`, `mutagen`, `SpeechRecognition`, `gTTS` - Audio processing
- `shazamio` - Music recognition
- `akinator` - Akinator game API
- `Pillow` - Image processing

## Workflow
- **Start application**: `cd bmqa && python main.py` (console output)
- No web frontend — pure Telegram bot

## Notes
- Redis is optional; falls back to in-memory `DummyRedis` if Redis is not available
- The bot requires a valid `BOT_TOKEN` to connect to Telegram
- If a conflict error appears, another bot instance with the same token is running elsewhere
