"""
Session management for storing PKCE verifiers and state.
Supports both in-memory and Redis storage.
"""

import json
import logging
import secrets
import time
from typing import Optional, Dict, Any

try:
    import redis.asyncio as aioredis

    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

from .config import Settings

logger = logging.getLogger(__name__)


class SessionStore:
    """Abstract base for session storage."""

    async def set(self, key: str, value: Dict[str, Any], expire: int) -> None:
        """Store a value with expiration."""
        raise NotImplementedError

    async def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Retrieve a value."""
        raise NotImplementedError

    async def delete(self, key: str) -> None:
        """Delete a value."""
        raise NotImplementedError


class InMemorySessionStore(SessionStore):
    """In-memory session storage (development only)."""

    # Class-level shared store to persist across instances
    _shared_store: Dict[str, Dict[str, Any]] = {}

    def __init__(self):
        # Use class-level store instead of instance-level
        pass

    async def set(self, key: str, value: Dict[str, Any], expire: int) -> None:
        """Store value in memory (expiration not implemented)."""
        InMemorySessionStore._shared_store[key] = value
        logger.debug(
            f"Stored session {key} in memory. Total sessions: {len(InMemorySessionStore._shared_store)}"
        )

    async def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Get value from memory."""
        result = InMemorySessionStore._shared_store.get(key)
        logger.debug(
            f"Retrieved session {key}: {'Found' if result else 'Not found'}. Total sessions: {len(InMemorySessionStore._shared_store)}"
        )
        return result

    async def delete(self, key: str) -> None:
        """Delete value from memory."""
        InMemorySessionStore._shared_store.pop(key, None)


class RedisSessionStore(SessionStore):
    """Redis-based session storage (production)."""

    def __init__(self, redis_url: str):
        if not REDIS_AVAILABLE:
            raise ImportError(
                "Redis not available. Install with: pip install redis[hiredis]"
            )
        self.redis_url = redis_url
        self._redis: Optional[aioredis.Redis] = None

    async def _get_redis(self) -> aioredis.Redis:
        """Get or create Redis connection."""
        if self._redis is None:
            self._redis = await aioredis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=True,
            )
        return self._redis

    async def set(self, key: str, value: Dict[str, Any], expire: int) -> None:
        """Store value in Redis with expiration."""
        redis = await self._get_redis()
        await redis.setex(key, expire, json.dumps(value))

    async def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Get value from Redis."""
        redis = await self._get_redis()
        value = await redis.get(key)
        if value:
            return json.loads(value)
        return None

    async def delete(self, key: str) -> None:
        """Delete value from Redis."""
        redis = await self._get_redis()
        await redis.delete(key)

    async def close(self) -> None:
        """Close Redis connection."""
        if self._redis:
            await self._redis.close()


class SessionManager:
    """Manage authentication sessions with PKCE and state."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.store: SessionStore
        if settings.redis_enabled and settings.redis_url:
            self.store = RedisSessionStore(settings.redis_url)
            logger.info("Using Redis session storage")
        else:
            self.store = InMemorySessionStore()
            logger.info(
                "Using in-memory session storage (not recommended for production)"
            )

    def generate_state(self) -> str:
        """Generate a random state for CSRF protection."""
        return secrets.token_urlsafe(32)

    def generate_nonce(self) -> str:
        """Generate a random nonce for ID token validation."""
        return secrets.token_urlsafe(32)

    async def create_session(
        self,
        state: str,
        code_verifier: Optional[str] = None,
        nonce: Optional[str] = None,
        redirect_uri: Optional[str] = None,
    ) -> None:
        """
        Create a new session.

        Args:
            state: State parameter for CSRF protection
            code_verifier: PKCE code verifier
            nonce: Nonce for ID token validation
            redirect_uri: Original redirect URI
        """
        session_data: Dict[str, Any] = {
            "created_at": int(time.time()),
        }
        if code_verifier:
            session_data["code_verifier"] = code_verifier
        if nonce:
            session_data["nonce"] = nonce
        if redirect_uri:
            session_data["redirect_uri"] = redirect_uri

        await self.store.set(
            f"session:{state}",
            session_data,
            expire=self.settings.session_max_age,
        )

    async def get_session(self, state: str) -> Optional[Dict[str, Any]]:
        """
        Get session data by state.

        Args:
            state: State parameter

        Returns:
            Session data or None if not found
        """
        return await self.store.get(f"session:{state}")

    async def delete_session(self, state: str) -> None:
        """
        Delete session by state.

        Args:
            state: State parameter
        """
        await self.store.delete(f"session:{state}")

    async def close(self) -> None:
        """Close session store connections."""
        if isinstance(self.store, RedisSessionStore):
            await self.store.close()
