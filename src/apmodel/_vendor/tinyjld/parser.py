# SPDX-License-Identifier: MIT
# Copyright (c) 2026 AmaseCocoa
# Smallest JSON-LD parser made for apmodel

from typing import Any, Callable, Dict, Optional


class TinyJLD:
    def __init__(self, loader: Callable[[str], Dict[str, Any]]):
        self.loader = loader
        self._context_cache = {}

    def fetch_remote_context(self, url: str) -> Dict[str, Any]:
        if url in self._context_cache:
            return self._context_cache[url]

        try:
            data = self.loader(url)
            ctx = data.get("@context", data) if isinstance(data, dict) else {}
            res = self.flatten_context(ctx)
            self._context_cache[url] = res
            return res
        except Exception:
            self._context_cache[url] = {}
            return {}

    def flatten_context(self, ctx_input: Any) -> Dict[str, Any]:
        if not ctx_input:
            return {}
        if isinstance(ctx_input, dict):
            return ctx_input

        merged = {}
        items = ctx_input if isinstance(ctx_input, list) else [ctx_input]
        for item in items:
            if isinstance(item, str):
                merged.update(self.fetch_remote_context(item))
            elif isinstance(item, dict):
                merged.update(item)
        return merged

    def expand_term(
        self, term: Any, context: Dict[str, Any], seen: Optional[set] = None
    ) -> Any:
        if not isinstance(term, str) or term.startswith("@"):
            return term

        if ":" in term:
            prefix, suffix = term.split(":", 1)
            if suffix.startswith("//"):
                return term
            if prefix in context:
                if seen is None:
                    seen = set()
                if term in seen:
                    return term
                seen.add(term)
                base = context[prefix]
                base_iri = base.get("@id") if isinstance(base, dict) else base
                if isinstance(base_iri, str):
                    return (
                        f"{self.expand_term(base_iri, context, seen)}{suffix}"
                    )

        if term in context:
            mapping = context[term]
            val = mapping.get("@id") if isinstance(mapping, dict) else mapping
            if isinstance(val, str) and val != term:
                if seen is None:
                    seen = set()
                if term in seen:
                    return term
                seen.add(term)
                return self.expand_term(val, context, seen)
            return val

        vocab = context.get("@vocab")
        return f"{vocab}{term}" if vocab and isinstance(vocab, str) else term

    def resolve(
        self,
        data: Dict[str, Any],
        parent_context: Optional[Dict[str, Any]] = None,
    ) -> Optional[str]:
        if not isinstance(data, dict):
            return None
        ctx = (parent_context or {}).copy()
        if "@context" in data:
            ctx.update(self.flatten_context(data["@context"]))

        raw_type = data.get("@type") or data.get("type")
        if not raw_type:
            return None

        target = (
            raw_type[0] if isinstance(raw_type, list) and raw_type else raw_type
        )
        res = self.expand_term(target, ctx)
        return str(res) if res else None
