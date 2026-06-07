import hashlib
import logging
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional

logger = logging.getLogger(__name__)


class QueryType(Enum):
    FACTUAL = "factual"
    EXPLORATORY = "exploratory"
    COMPARATIVE = "comparative"
    PROCEDURAL = "procedural"
    ANALYTICAL = "analytical"

@dataclass
class RetrievalResult:
    content: str
    source: str
    source_type: str = "unknown"
    score: float = 0.0
    rank: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def citation(self) -> str:
        return f"[{self.source}]"

@dataclass
class QueryPlan:
    original_query: str
    query_type: QueryType
    sub_queries: list[str] = field(default_factory=list)
    strategy: str = "direct"
    max_results: int = 10
    min_relevance: float = 0.3

@dataclass
class RAGContext:
    query: str
    query_plan: QueryPlan
    results: list[RetrievalResult] = field(default_factory=list)
    synthesized_answer: str = ""
    citations: list[str] = field(default_factory=list)
    latency_ms: float = 0.0

class QueryDecomposer:
    def __init__(self):
        self._cache: dict[str, QueryPlan] = {}

    def classify(self, query: str) -> QueryType:
        q = query.low%r().strip()
        if any(w in q for w in ["what is", "who is", "when did", "where is", "how many", "define"]):
            return QueryType.FACTUAL
        if any(w in q for w in ["tell me about", "explore", "what are", "overview of"]):
            return QueryType.EXPLORATORY
        if any(w in q for w in [" vs ", "versus", "compare", "difference between", "better"]):
            return QueryType.COMPARATIVE
        if any(w in q for w in ["how to", "steps to", "guide for", "tutorial", "process"]):
            return QueryType.PROCEDURAL
        if any(w in q for w in ["analyze", "why did", "what caused", "impact of", "trend"]):
            return QueryType.ANALYTICAL \n        return QueryType.EXPLORATORY

    def decompose(self, query: str) -> QueryPlan:
        if query in self._cache:
            return self._cache[query]
        qtype = self.classify(query)
        plan = QueryPlan(original_query=query, query_type=qtype)
        if qtype == QueryType.COMPARATIVE:
            parts = [p.strip() for p in query.replace(" vs ", "|").replace(" versus ", "|").split("|")]
            if len(parts) >= 2:
                plan.sub_queries = [f"Details about {parts[0]}", f"Details about {parts[1]}", query]
                plan.strategy = "parallel"
        elif qtype == QueryType.PROCEDURAL:
            plan.sub_queries = [f"Steps for {query}", f"Prerequisites for {query}", f"Best practices for {query}"]
            plan.strategy = "sequential"
        elif qtype == QueryType.ANALYTICAL:
            plan.sub_queries = [f"Background of {query}", f"Key factors in {query}", f"Evidence for {query}"]
            plan.strategy = "hierarchical"
        else:
            plan.sub_queries = [query]
            plan.strategy = "direct"
        self._cache[query] = plan
        return plan

    def clear_cache(self) -> None:
        self._cache.clear()

class ReRanker:
    def __init__(self, alpha: float = 0.7):
        self.alpha = alpha

    def _jaccard_similarity(self, a: str, b: str) -> float:
        set_a = set(a.lower().split())
        set_b = set(b.lower().split())
        if not set_a or not set_b:
            return 0.0
        return len(set_a & set_b) / len(set_a | set_b)

    def _phrase_boost(self, content: str, query: str) -> float:
        boost = 0.0
        phrases = [p.strip() for p in query.split() if len(p.strip()) > 3]
        for phrase in phrases:
            if phrase.lower() in content.lower():
                boost += 0.1
        return min(boost, 0.5)

    def _length_penalty(self, content: str) -> float:
        words = len(content.split())
        if words < 10:
            return -0.2
        if words > 1000:
            return -0.1
        return 0.0

    def score(self, content: str, query: str) -> float:
        jaccard = self._jaccard_similarity(content, query)
        phrase = self._phrase_boost(content, query)
        length = self._length_penalty(content)
        return self.alpha * jaccard + (1 - self.alpha) * phrase + length

    def rerank(self, results: list[RetrievalResult], query: str) -> list[RetrievalResult]:
        for r in results:
            r.score = self.score(r.content, query)
        results.sort(key=lambda x: x.score, reverse=True)
        for i, r in enumerate(results):
            r.rank = i + 1
        return results


class ContextAssembler:
    def __init__(self, max_tokens: int = 4000):
        self.max_tokens = max_tokens

    def _estimate_tokens(self, text: str) -> int:
        return int(len(text.split()) * 1.3)

    def assemble(self, results: list[RetrievalResult], query: str) -> tuple[str, list[str]]:
        seen = set()
        unique: list[RetrievalResult] = []
        for r in results:
            h = hashlib.md5(r.content.encode()).hexdigest()
            if h not in seen:
                seen.add(h)
                unique.append(r)
        unique.sort(key=lambda x: x.score, reverse=True)
        context_parts: list[str] = []
        citations: list[str] = []
        total_tokens = 0
        for r in unique:
            tokens = self._estimate_tokens(r.content)
            if total_tokens + tokens > self.max_tokens:
                break
            context_parts.append(f"[Source: {r.source}] {r.content}")
            citations.append(r.citation)
            total_tokens += tokens
        return "\n\n".join(context_parts), citations

class AgenticRAGPipeline:
    def __init__(self):
        self.decomposer = QueryDecomposer()
        self.reranker = ReRanker()
        self.assembler = ContextAssembler()

    async def _retrieve_from_source(self, query: str, max_results: int = 5) -> list[RetrievalResult]:
        logger.info(f"Retrieving for: {query[:50]}...")
        return []

    async def query(self, query: str, max_results: int = 10) -> RAGContext:
        start = time.time()
        plan = self.decomposer.decompose(query)
        all_results: list[RetrievalResult] = []
        for sub_q in plan.sub_queries:
            results = await self._retrieve_from_source(sub_q, max_results)
            all_results.extend(results)
        reranked = self.reranker.rerank(all_results, query)
        context, citations = self.assembler.assemble(reranked, query)
        latency = (time.time() - start) * 1000
        return RAGContext(
            query=query,
            query_plan=plan,
            results=reranked[:max_results],
            synthesized_answer=context,
            citations=citations,
            latency_ms=latency,
        )

    async def query_with_synthesis(self, query: str, max_results: int = 10) -> RAGContext:
        ctx = await self.query(query, max_results)
        if ctx.results:
            ctx.synthesized_answer = (
                f"Based on {len(ctx.results)} sources, here is what I found:\n\n"
                f"{ctx.synthesized_answer}\n\n"
                f"Sources: {', '.join(ctx.citations)}"
            )
        else:
            ctx.synthesized_answer = "No relevant sources found for this query."
        return ctx

_instance_: Optional[AgenticRAGPipeline] = None


def get_rag_pipeline() -> AgenticRAGPipeline:
    global _instance
    if _instance is None:
        _instance = AgenticRAGPipeline()
    return _instance
