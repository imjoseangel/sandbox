from __future__ import annotations

import json
import logging
import threading
from datetime import datetime
from typing import Any

import numpy as np
import redis
from crewai.events import (
    BaseEventListener,
    MemoryQueryCompletedEvent,
    MemoryQueryFailedEvent,
    MemorySaveFailedEvent,
)
from crewai.llm import LLM
from crewai.memory.analyze import MemoryAnalysis
from crewai.memory.storage.backend import StorageBackend
from crewai.memory.types import (
    MemoryRecord,
    ScopeInfo,
)
from crewai.memory.unified_memory import Memory

from app.core.settings import Settings, get_settings

logger = logging.getLogger(__name__)


def _patch_bedrock_incompatible_schemas() -> None:
    """Remove minimum/maximum JSON schema constraints that Bedrock rejects.

    Bedrock does not support ``minimum``/``maximum`` on ``number`` type fields
    in structured output schemas. CrewAI's ``MemoryAnalysis.importance`` has
    ``ge=0.0, le=1.0`` which Pydantic converts to those keywords.  We
    monkey-patch ``model_json_schema`` on the affected models so the
    constraints are stripped before the schema reaches the LLM provider.
    """
    if getattr(MemoryAnalysis.model_json_schema, "_bedrock_patched", False):
        return

    _original = MemoryAnalysis.model_json_schema

    @classmethod  # type: ignore[misc]
    def _patched_schema(cls, *args: Any, **kwargs: Any) -> dict[str, Any]:
        schema = _original.__func__(cls, *args, **kwargs)  # type: ignore[attr-defined]
        _strip_numeric_constraints(schema)
        return schema

    _patched_schema._bedrock_patched = True  # type: ignore[attr-defined]
    MemoryAnalysis.model_json_schema = _patched_schema  # type: ignore[assignment]


def _strip_numeric_constraints(obj: Any) -> None:
    """Recursively remove minimum/maximum/exclusiveMinimum/exclusiveMaximum."""
    if isinstance(obj, dict):
        for key in (
            "minimum",
            "maximum",
            "exclusiveMinimum",
            "exclusiveMaximum",
        ):
            obj.pop(key, None)
        for value in obj.values():
            _strip_numeric_constraints(value)
    elif isinstance(obj, list):
        for item in obj:
            _strip_numeric_constraints(item)


KEY_PREFIX = "crewai:memory:"
SCOPE_PREFIX = "crewai:scope:"
CAT_PREFIX = "crewai:cat:"


def _record_to_dict(record: MemoryRecord) -> dict[str, Any]:
    data = record.model_dump()
    data["created_at"] = record.created_at.isoformat()
    data["last_accessed"] = record.last_accessed.isoformat()
    return data


def _dict_to_record(data: dict[str, Any]) -> MemoryRecord:
    data["created_at"] = datetime.fromisoformat(data["created_at"])
    data["last_accessed"] = datetime.fromisoformat(data["last_accessed"])
    return MemoryRecord(**data)


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    va = np.array(a, dtype=np.float32)
    vb = np.array(b, dtype=np.float32)
    denom = float(np.linalg.norm(va) * np.linalg.norm(vb))
    if denom == 0:
        return 0.0
    return float(np.dot(va, vb) / denom)


def _decode(value: bytes | str) -> str:
    """Decode a Redis return value to str."""
    return value.decode() if isinstance(value, bytes) else str(value)


class RedisStorageBackend(StorageBackend):
    """Redis-backed storage for CrewAI Memory."""

    def __init__(self, client: Any):
        self.client: Any = client
        self._write_lock = threading.RLock()

    @property
    def write_lock(self) -> threading.RLock:
        """Reentrant write lock expected by CrewAI's memory system."""
        return self._write_lock

    # ------------------------------------------------------------------
    # save
    # ------------------------------------------------------------------
    def save(self, records: list[MemoryRecord]) -> None:
        pipe = self.client.pipeline()
        for record in records:
            key = f"{KEY_PREFIX}{record.id}"
            data = _record_to_dict(record)
            pipe.set(key, json.dumps(data))

            ts = record.created_at.timestamp()
            pipe.zadd(f"{SCOPE_PREFIX}{record.scope}", {record.id: ts})

            for cat in record.categories:
                pipe.sadd(f"{CAT_PREFIX}{cat}", record.id)
        pipe.execute()

    # ------------------------------------------------------------------
    # search
    # ------------------------------------------------------------------
    def search(
        self,
        query_embedding: list[float],
        scope_prefix: str | None = None,
        categories: list[str] | None = None,
        metadata_filter: dict[str, Any] | None = None,
        limit: int = 10,
        min_score: float = 0.0,
    ) -> list[tuple[MemoryRecord, float]]:
        record_ids = self._candidate_ids(scope_prefix, categories)
        results: list[tuple[MemoryRecord, float]] = []

        for rid in record_ids:
            raw = self.client.get(f"{KEY_PREFIX}{rid}")
            if raw is None:
                continue
            record = _dict_to_record(json.loads(raw))

            if metadata_filter and not self._matches_metadata(
                record, metadata_filter
            ):
                continue

            if record.embedding is None:
                continue
            score = _cosine_similarity(query_embedding, record.embedding)
            if score >= min_score:
                results.append((record, score))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:limit]

    # ------------------------------------------------------------------
    # delete
    # ------------------------------------------------------------------
    def delete(
        self,
        scope_prefix: str | None = None,
        categories: list[str] | None = None,
        record_ids: list[str] | None = None,
        older_than: datetime | None = None,
        metadata_filter: dict[str, Any] | None = None,
    ) -> int:
        ids_to_delete: set[str]

        if record_ids is not None:
            ids_to_delete = set(record_ids)
        else:
            ids_to_delete = self._candidate_ids(scope_prefix, categories)

        deleted = 0
        for rid in ids_to_delete:
            raw = self.client.get(f"{KEY_PREFIX}{rid}")
            if raw is None:
                continue
            record = _dict_to_record(json.loads(raw))

            if older_than and record.created_at >= older_than:
                continue
            if metadata_filter and not self._matches_metadata(
                record, metadata_filter
            ):
                continue

            self._remove_record(record)
            deleted += 1

        return deleted

    # ------------------------------------------------------------------
    # update
    # ------------------------------------------------------------------
    def update(self, record: MemoryRecord) -> None:
        old_raw = self.client.get(f"{KEY_PREFIX}{record.id}")
        if old_raw is not None:
            old = _dict_to_record(json.loads(old_raw))
            if old.scope != record.scope:
                self.client.zrem(f"{SCOPE_PREFIX}{old.scope}", record.id)
            for cat in old.categories:
                if cat not in record.categories:
                    self.client.srem(f"{CAT_PREFIX}{cat}", record.id)

        data = _record_to_dict(record)
        self.client.set(f"{KEY_PREFIX}{record.id}", json.dumps(data))
        ts = record.created_at.timestamp()
        self.client.zadd(f"{SCOPE_PREFIX}{record.scope}", {record.id: ts})
        for cat in record.categories:
            self.client.sadd(f"{CAT_PREFIX}{cat}", record.id)

    # ------------------------------------------------------------------
    # get_record
    # ------------------------------------------------------------------
    def get_record(self, record_id: str) -> MemoryRecord | None:
        raw = self.client.get(f"{KEY_PREFIX}{record_id}")
        if raw is None:
            return None
        return _dict_to_record(json.loads(raw))

    # ------------------------------------------------------------------
    # list_records
    # ------------------------------------------------------------------
    def list_records(
        self,
        scope_prefix: str | None = None,
        limit: int = 200,
        offset: int = 0,
    ) -> list[MemoryRecord]:
        # Use zrevrange to preserve timestamp ordering (newest-first)
        all_ids: list[str] = []
        pattern = (
            f"{SCOPE_PREFIX}{scope_prefix}*"
            if scope_prefix is not None
            else f"{SCOPE_PREFIX}*"
        )
        for key in self.client.scan_iter(match=pattern):
            members = self.client.zrevrange(key, 0, -1)
            all_ids.extend(_decode(m) for m in members)
        page = all_ids[offset : offset + limit]
        records: list[MemoryRecord] = []
        for rid in page:
            raw = self.client.get(f"{KEY_PREFIX}{rid}")
            if raw is not None:
                records.append(_dict_to_record(json.loads(raw)))
        return records

    # ------------------------------------------------------------------
    # get_scope_info
    # ------------------------------------------------------------------
    def get_scope_info(self, scope: str) -> ScopeInfo:
        scope_key = f"{SCOPE_PREFIX}{scope}"
        count = int(self.client.zcard(scope_key))
        all_ids: list[str] = [
            _decode(m) for m in list(self.client.zrange(scope_key, 0, -1))
        ]

        oldest: datetime | None = None
        newest: datetime | None = None
        cats: set[str] = set()

        for rid in all_ids:
            raw = self.client.get(f"{KEY_PREFIX}{rid}")
            if raw is None:
                continue
            rec = _dict_to_record(json.loads(raw))
            cats.update(rec.categories)
            if oldest is None or rec.created_at < oldest:
                oldest = rec.created_at
            if newest is None or rec.created_at > newest:
                newest = rec.created_at

        child_scopes = self._child_scopes(scope)

        return ScopeInfo(
            path=scope,
            record_count=count,
            categories=sorted(cats),
            oldest_record=oldest,
            newest_record=newest,
            child_scopes=child_scopes,
        )

    # ------------------------------------------------------------------
    # list_scopes
    # ------------------------------------------------------------------
    def list_scopes(self, parent: str = "/") -> list[str]:
        pattern = f"{SCOPE_PREFIX}*"
        scopes: set[str] = set()
        for key in self.client.scan_iter(match=pattern):
            scope = _decode(key).removeprefix(SCOPE_PREFIX)
            if scope.startswith(parent):
                scopes.add(scope)
        return sorted(scopes)

    # ------------------------------------------------------------------
    # list_categories
    # ------------------------------------------------------------------
    def list_categories(
        self, scope_prefix: str | None = None
    ) -> dict[str, int]:
        if scope_prefix is not None:
            ids = self._candidate_ids(scope_prefix, categories=None)
            cats: dict[str, int] = {}
            for rid in ids:
                raw = self.client.get(f"{KEY_PREFIX}{rid}")
                if raw is None:
                    continue
                rec = _dict_to_record(json.loads(raw))
                for cat in rec.categories:
                    cats[cat] = cats.get(cat, 0) + 1
            return cats

        result: dict[str, int] = {}
        for key in self.client.scan_iter(match=f"{CAT_PREFIX}*"):
            cat = _decode(key).removeprefix(CAT_PREFIX)
            result[cat] = int(self.client.scard(f"{CAT_PREFIX}{cat}"))
        return result

    # ------------------------------------------------------------------
    # count
    # ------------------------------------------------------------------
    def count(self, scope_prefix: str | None = None) -> int:
        if scope_prefix is not None:
            return len(self._candidate_ids(scope_prefix, categories=None))
        total = 0
        for key in self.client.scan_iter(match=f"{SCOPE_PREFIX}*"):
            total += int(self.client.zcard(key))
        return total

    # ------------------------------------------------------------------
    # reset
    # ------------------------------------------------------------------
    def reset(self, scope_prefix: str | None = None) -> None:
        if scope_prefix is not None:
            ids = self._candidate_ids(scope_prefix, categories=None)
            for rid in ids:
                raw = self.client.get(f"{KEY_PREFIX}{rid}")
                if raw is not None:
                    record = _dict_to_record(json.loads(raw))
                    self._remove_record(record)
            return

        for pat in [f"{KEY_PREFIX}*", f"{SCOPE_PREFIX}*", f"{CAT_PREFIX}*"]:
            for key in self.client.scan_iter(match=pat):
                self.client.delete(key)

    # ------------------------------------------------------------------
    # async variants — delegate to sync
    # ------------------------------------------------------------------
    async def asave(self, records: list[MemoryRecord]) -> None:
        self.save(records)

    async def asearch(
        self,
        query_embedding: list[float],
        scope_prefix: str | None = None,
        categories: list[str] | None = None,
        metadata_filter: dict[str, Any] | None = None,
        limit: int = 10,
        min_score: float = 0.0,
    ) -> list[tuple[MemoryRecord, float]]:
        return self.search(
            query_embedding,
            scope_prefix,
            categories,
            metadata_filter,
            limit,
            min_score,
        )

    async def adelete(
        self,
        scope_prefix: str | None = None,
        categories: list[str] | None = None,
        record_ids: list[str] | None = None,
        older_than: datetime | None = None,
        metadata_filter: dict[str, Any] | None = None,
    ) -> int:
        return self.delete(
            scope_prefix, categories, record_ids, older_than, metadata_filter
        )

    # ------------------------------------------------------------------
    # internal helpers
    # ------------------------------------------------------------------
    def _candidate_ids(
        self,
        scope_prefix: str | None,
        categories: list[str] | None,
    ) -> set[str]:
        ids: set[str] | None = None

        if scope_prefix is not None:
            scope_ids: set[str] = set()
            for key in self.client.scan_iter(
                match=f"{SCOPE_PREFIX}{scope_prefix}*"
            ):
                members = list(self.client.zrange(key, 0, -1))
                scope_ids.update(_decode(m) for m in members)
            ids = scope_ids

        if categories:
            for cat in categories:
                members_set = self.client.smembers(f"{CAT_PREFIX}{cat}")
                cat_ids = {_decode(m) for m in list(members_set)}
                ids = cat_ids if ids is None else ids & cat_ids

        if ids is None:
            logger.debug(
                "_candidate_ids called without scope or category filter — "
                "performing full key scan; this may be slow for large datasets"
            )
            ids = set()
            for key in self.client.scan_iter(match=f"{SCOPE_PREFIX}*"):
                members = list(self.client.zrange(key, 0, -1))
                ids.update(_decode(m) for m in members)

        return ids

    def _matches_metadata(
        self,
        record: MemoryRecord,
        metadata_filter: dict[str, Any],
    ) -> bool:
        for key, value in metadata_filter.items():
            if record.metadata.get(key) != value:
                return False
        return True

    def _remove_record(self, record: MemoryRecord) -> None:
        self.client.delete(f"{KEY_PREFIX}{record.id}")
        self.client.zrem(f"{SCOPE_PREFIX}{record.scope}", record.id)
        for cat in record.categories:
            self.client.srem(f"{CAT_PREFIX}{cat}", record.id)

    def _child_scopes(self, parent: str) -> list[str]:
        children: list[str] = []
        prefix = parent if parent.endswith("/") else parent + "/"
        for key in self.client.scan_iter(match=f"{SCOPE_PREFIX}{prefix}*"):
            scope = _decode(key).removeprefix(SCOPE_PREFIX)
            if scope != parent:
                children.append(scope)
        return sorted(children)


class _MemoryEventListener(BaseEventListener):
    """Log memory failures and query timing for production observability."""

    def setup_listeners(self, crewai_event_bus: Any) -> None:
        @crewai_event_bus.on(MemorySaveFailedEvent)
        def on_save_failed(source: Any, event: Any) -> None:
            logger.error(
                "Memory save failed: %s — value: %.200s",
                event.error,
                getattr(event, "value", ""),
            )

        @crewai_event_bus.on(MemoryQueryFailedEvent)
        def on_query_failed(source: Any, event: Any) -> None:
            logger.error(
                "Memory query failed: %s — query: %s",
                event.error,
                getattr(event, "query", ""),
            )

        @crewai_event_bus.on(MemoryQueryCompletedEvent)
        def on_query_done(source: Any, event: Any) -> None:
            if getattr(event, "source_type", None) == "unified_memory":
                logger.debug(
                    "Memory query completed in %.0fms — query: %s",
                    getattr(event, "query_time_ms", 0),
                    getattr(event, "query", ""),
                )


class MemoryService:
    """Service to create CrewAI Memory backed by Redis."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self._memory: Memory | None = None
        self._redis_client: redis.Redis | None = None
        self._instance_lock = threading.Lock()

    def _build_redis_client(self) -> redis.Redis:
        return redis.Redis(
            host=self.settings.redis_host,
            port=self.settings.redis_port,
            password=self.settings.redis_password,
            db=self.settings.redis_db,
            decode_responses=False,
            socket_timeout=self.settings.redis_socket_timeout,
            socket_connect_timeout=self.settings.redis_connect_timeout,
            retry_on_timeout=True,
            max_connections=self.settings.redis_max_connections,
            health_check_interval=30,
        )

    def get_memory_instance(self) -> Memory:
        if self._memory is None:
            with self._instance_lock:
                if self._memory is None:
                    if "bedrock" in self.settings.litellm_model.lower():
                        _patch_bedrock_incompatible_schemas()

                    self._redis_client = self._build_redis_client()
                    backend = RedisStorageBackend(self._redis_client)

                    if self.settings.embedding_provider == "openai":
                        embedder_cfg: dict[str, Any] = {
                            "model": self.settings.embedding_model,
                            "api_key": self.settings.litellm_api_key,
                            "api_base": self.settings.litellm_api_base,
                        }
                        if self.settings.embedding_api_version:
                            embedder_cfg["api_version"] = (
                                self.settings.embedding_api_version
                            )
                        embedder_config: dict[str, Any] = {
                            "provider": "openai",
                            "config": embedder_cfg,
                        }
                    else:
                        embedder_config = {
                            "provider": "sentence-transformer",
                            "config": {
                                "model_name": self.settings.embedding_model,
                            },
                        }

                    llm = LLM(
                        model=self.settings.litellm_model,
                        api_key=self.settings.litellm_api_key,
                        base_url=self.settings.litellm_api_base,
                    )

                    self._memory = Memory(
                        storage=backend,
                        embedder=embedder_config,
                        llm=llm,
                        recency_weight=self.settings.memory_recency_weight,
                        semantic_weight=self.settings.memory_semantic_weight,
                        importance_weight=self.settings.memory_importance_weight,
                        recency_half_life_days=self.settings.memory_half_life_days,
                    )
                    _MemoryEventListener()
                    logger.info(
                        "CrewAI Memory initialized with Redis backend at %s:%s",
                        self.settings.redis_host,
                        self.settings.redis_port,
                    )
        assert self._memory is not None
        return self._memory

    def close(self) -> None:
        """Drain pending background saves and release the Memory instance."""
        with self._instance_lock:
            if self._memory is not None:
                self._memory.close()
                self._memory = None
                self._redis_client = None

    def health_check(self) -> bool:
        try:
            if self._redis_client is not None:
                return bool(self._redis_client.ping())
            # Not yet initialized — create a short-lived check client
            client = self._build_redis_client()
            return bool(client.ping())
        except redis.RedisError:
            logger.exception("Redis health check failed")
            return False


_state: dict[str, MemoryService | None] = {"service": None}
_state_lock = threading.Lock()


def get_memory_service(
    settings: Settings | None = None,
) -> MemoryService:
    """Get memory service singleton."""
    if _state["service"] is None:
        with _state_lock:
            if _state["service"] is None:
                if settings is None:
                    settings = get_settings()
                _state["service"] = MemoryService(settings)
    assert _state["service"] is not None
    return _state["service"]


def reset_memory_service() -> None:
    """Reset memory service singleton (useful for testing)."""
    with _state_lock:
        service = _state["service"]
        if service is not None:
            service.close()
        _state["service"] = None
