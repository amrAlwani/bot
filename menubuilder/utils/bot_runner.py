"""
Manages running child bots as asyncio tasks.
Each child bot runs its own Application instance within the same event loop.
"""
import asyncio
import logging
from typing import Dict, Optional
from telegram.ext import Application

logger = logging.getLogger(__name__)

_running_bots: Dict[str, Application] = {}


async def start_child_bot(token: str, build_app_func) -> bool:
    """Start a child bot. Returns True if started successfully."""
    if token in _running_bots:
        logger.info(f"Bot {token[:20]}... is already running")
        return True
    try:
        app = await build_app_func(token)
        await app.initialize()
        await app.start()
        await app.updater.start_polling(drop_pending_updates=True)
        _running_bots[token] = app
        logger.info(f"✅ Child bot started: {token[:20]}...")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to start child bot {token[:20]}...: {e}")
        return False


async def stop_child_bot(token: str) -> bool:
    """Stop a running child bot. Returns True if stopped successfully."""
    app = _running_bots.pop(token, None)
    if not app:
        return False
    try:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()
        logger.info(f"⏹️ Child bot stopped: {token[:20]}...")
        return True
    except Exception as e:
        logger.error(f"❌ Error stopping child bot {token[:20]}...: {e}")
        return False


def is_running(token: str) -> bool:
    return token in _running_bots


def get_running_tokens() -> list:
    return list(_running_bots.keys())


async def stop_all():
    """Stop all running child bots."""
    tokens = list(_running_bots.keys())
    for token in tokens:
        await stop_child_bot(token)
