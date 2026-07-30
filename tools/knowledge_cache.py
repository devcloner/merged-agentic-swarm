"""
Knowledge Cache Service
Persistent cache for validated learnings, obstacle resolution patterns, and AST symbol manifests.
"""
import os
import json
import time
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger("knowledge_cache")

class KnowledgeCache:
    def __init__(self, cache_file: str = "/home/ubuntu/.opencode/knowledge_cache.json"):
        self.cache_file = cache_file
        self.learnings: Dict[str, Dict[str, Any]] = {}
        self.symbol_cache: Dict[str, Any] = {}
        self.load_cache()

    def load_cache(self):
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.learnings = data.get("learnings", {})
                    self.symbol_cache = data.get("symbols", {})
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

    def add_learning(self, title: str, category: str, pattern_solution: str, tags: Optional[List[str]] = None) -> str:
        learning_id = f"LEARN-{len(self.learnings)+1:04d}"
        self.learnings[learning_id] = {
            "id": learning_id,
            "title": title,
            "category": category,
            "solution": pattern_solution,
            "tags": tags or [],
            "created_at": time.time()
        }
        self.save_cache()
        logger.info(f"Added validated learning {learning_id}: {title}")
        return learning_id

    def get_learning(self, learning_id: str) -> Optional[Dict[str, Any]]:
        return self.learnings.get(learning_id)

    def search_learnings(self, query: str) -> List[Dict[str, Any]]:
        results = []
        q = query.lower()
        for l in self.learnings.values():
            if q in l["title"].lower() or q in l["solution"].lower() or any(q in t.lower() for t in l["tags"]):
                results.append(l)
        return results

# Global Singleton
default_knowledge_cache = KnowledgeCache()
