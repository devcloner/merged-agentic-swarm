"""
Knowledge Cache Service
Persistent cache for validated learnings, obstacle resolution patterns, and AST symbol manifests.
"""
import json
import logging
import os
import time
from typing import Any

logger = logging.getLogger("knowledge_cache")

class KnowledgeCache:
    def __init__(self, cache_file: str | None = None, max_learnings: int = 200):
        if cache_file is None:
            cache_file = os.path.expanduser("~/.opencode/knowledge_cache.json")
        self.cache_file = cache_file
        self.max_learnings = max_learnings
        self.learnings: dict[str, dict[str, Any]] = {}
        self.symbol_cache: dict[str, Any] = {}
        self.load_cache()

    def load_cache(self):
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    raw_learnings = data.get("learnings", {})
                    self.symbol_cache = data.get("symbols", {})

                # Compact pre-existing duplicates by content hash (title+category+solution).
                # Prevents LEARN-0001..0005 dupes from persisting across restarts.
                seen: dict[str, str] = {}  # content hash -> surviving learning ID
                deduped: dict[str, dict[str, Any]] = {}
                dupes_removed = 0
                for lid, entry in raw_learnings.items():
                    key = f"{entry.get('title','')}|{entry.get('category','')}|{entry.get('solution','')}"
                    if key in seen:
                        dupes_removed += 1
                    else:
                        seen[key] = lid
                        deduped[lid] = entry
                self.learnings = deduped
                if dupes_removed:
                    logger.info(f"Compacted {dupes_removed} duplicate learning(s) on load")
                    self.save_cache()  # persist the compaction
            except Exception as e:
                logger.error(f"Failed to load knowledge cache: {e}")

    def save_cache(self):
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
        data = {
            "learnings": self.learnings,
            "symbols": self.symbol_cache,
            "saved_at": time.time()
        }
        with open(self.cache_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def add_learning(self, title: str, category: str, pattern_solution: str, tags: list[str] | None = None, ttl_sec: float | None = None) -> str:
        # Dedup via content hash: title + category + solution (prevents semantic duplicates
        # like LEARN-0001 through LEARN-0005 that share identical content under different IDs)
        for existing in self.learnings.values():
            if existing.get("title") == title and existing.get("category") == category and existing.get("solution") == pattern_solution:
                logger.info(f"Skipped duplicate learning (content match): {existing['id']}")
                return existing["id"]

        # Evict expired learnings first
        now = time.time()
        expired_ids = [
            lid for lid, l in self.learnings.items()
            if l.get("ttl_sec") is not None and l.get("created_at", 0) + l["ttl_sec"] < now
        ]
        for lid in expired_ids:
            self.learnings.pop(lid, None)

        # Enforce max learnings — remove oldest if at capacity
        if len(self.learnings) >= self.max_learnings:
            oldest_id = min(self.learnings, key=lambda lid: self.learnings[lid].get("created_at", 0))
            self.learnings.pop(oldest_id, None)

        # Generate unique ID using a counter to avoid collisions after eviction
        # (len+1 would collide with existing IDs when items were evicted)
        max_idx = 0
        for lid in self.learnings:
            if lid.startswith("LEARN-"):
                try:
                    max_idx = max(max_idx, int(lid.split("-")[1]))
                except (ValueError, IndexError):
                    pass
        learning_id = f"LEARN-{max_idx + 1:04d}"
        self.learnings[learning_id] = {
            "id": learning_id,
            "title": title,
            "category": category,
            "solution": pattern_solution,
            "tags": tags or [],
            "created_at": time.time(),
            "ttl_sec": ttl_sec,
        }
        self.save_cache()
        logger.info(f"Added validated learning {learning_id}: {title}")
        return learning_id

    def get_learning(self, learning_id: str) -> dict[str, Any] | None:
        return self.learnings.get(learning_id)

    def search_learnings(self, query: str) -> list[dict[str, Any]]:
        results = []
        q = query.lower()
        for l in self.learnings.values():
            if q in l["title"].lower() or q in l["solution"].lower() or any(q in t.lower() for t in l["tags"]):
                results.append(l)
        return results

# Global Singleton
default_knowledge_cache = KnowledgeCache()
