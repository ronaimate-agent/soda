"""
Utility functions and helpers for Soda application.
"""
import json
import logging
from pathlib import Path
from typing import Optional

from sqlalchemy import select as sa_select

from .database import GlobalSetting, async_session

logger = logging.getLogger("soda.utils")


async def get_setting(key: str, default: str = "") -> str:
    """Get a setting value from the database."""
    async with async_session() as session:
        result = await session.execute(
            sa_select(GlobalSetting).where(GlobalSetting.key == key)
        )
        setting = result.scalar_one_or_none()
        return setting.value if setting and setting.value else default


async def get_opencode_api_key() -> str:
    """Get OpenCode API key from settings."""
    return await get_setting("opencode_api_key", "")


def write_opencode_auth(api_key: str, provider: Optional[str] = None, model: Optional[str] = None) -> bool:
    """
    Write OpenCode authentication file.
    
    Args:
        api_key: API key for OpenCode
        provider: Optional provider name
        model: Optional model name
        
    Returns:
        True if auth file was written, False if no API key provided
    """
    if not api_key:
        logger.debug("No API key provided, skipping auth file write")
        return False
    
    auth_path = Path("/root/.opencode/auth.json")
    auth_path.parent.mkdir(parents=True, exist_ok=True)
    
    auth_data = {
        "api_key": api_key,
        "provider": provider or "openai",
        "model": model or "gpt-4"
    }
    
    try:
        with open(auth_path, 'w') as f:
            json.dump(auth_data, f, indent=2)
        logger.info(f"OpenCode auth file written to {auth_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to write OpenCode auth file: {e}")
        return False
