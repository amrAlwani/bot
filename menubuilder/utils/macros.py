"""
Process macro variables in bot messages.
Available macros:
  {name}      - User's first name
  {username}  - User's @username
  {id}        - User's Telegram ID
  {balance}   - User's balance
  {users}     - Total users count
  {ref_link}  - Referral link
"""
from typing import Optional


def process_macros(
    text: str,
    user=None,
    balance: float = 0.0,
    users_count: int = 0,
    bot_username: str = "",
) -> str:
    if not text:
        return text

    replacements = {
        "{name}": getattr(user, "first_name", "") or "",
        "{username}": (f"@{user.username}" if getattr(user, "username", None) else getattr(user, "first_name", "")) if user else "",
        "{id}": str(getattr(user, "id", "")) if user else "",
        "{balance}": f"{balance:.2f}",
        "{users}": str(users_count),
        "{ref_link}": f"https://t.me/{bot_username}?start=ref_{getattr(user, 'id', '')}" if bot_username and user else "",
    }

    for macro, value in replacements.items():
        text = text.replace(macro, value)

    return text
