# ai-orchestrator/app/graph/nodes/auditor.py
# ai-orchestrator/app/graph/nodes/auditor.py
# ai-orchestrator/app/graph/nodes/auditor.py
"""
Auditor Agent using DeepEval with local Ollama judge.
"""
import logging
from deepeval.models import OllamaModel
from app.config import settings
from app.graph.state import AgentState

logger = logging.getLogger("orchestrator.auditor")

_judge: OllamaModel | None = None


def _get_judge() -> OllamaModel:
    global _judge
    if _judge is None:
        _judge = OllamaModel(
            model=settings.ollama_model,
            base_url=settings.ollama_base_url,
            temperature=0,
        )
    return _judge


def _extract_context(threat_intel: dict | None) -> list[str]:
    hits = (threat_intel or {}).get("matched_techniques", [])
    context = []
    for hit in hits:
        title = hit.get("title", "")
        text = hit.get("text", "")
        if text:
            context.append(f"{title}: {text}" if title else text)
    return context


async def auditor_agent(state: AgentState) -> AgentState:
    decision = state.get("decision") or {}
    recommendation = decision.get("recommendation")
    context = _extract_context(state.get("threat_intel"))

    if not recommendation or not context:
        state["audit"] = {
            "status": "skipped",
            "note": "No recommendation yet, or no retrieved context to evaluate faithfulness against",
            "passed": bool(recommendation),
            "faithfulness": None,
            "hallucination_rate": None,
        }
        state.setdefault("trace", []).append("auditor_agent")
        return state

    try:
        from deepeval.metrics import FaithfulnessMetric, HallucinationMetric
        from deepeval.test_case import LLMTestCase

        test_case = LLMTestCase(
            input=state.get("summary") or state.get("asset", ""),
            actual_output=recommendation,
            retrieval_context=context,
            context=context,
        )

        judge = _get_judge()
        faithfulness = FaithfulnessMetric(model=judge, async_mode=True, include_reason=True)
        hallucination = HallucinationMetric(model=judge, async_mode=True, include_reason=True)

        faithfulness_score = await faithfulness.a_measure(test_case)
        hallucination_score = await hallucination.a_measure(test_case)

        passed = (
            faithfulness_score >= faithfulness.threshold
            and hallucination_score >= hallucination.threshold
        )

        state["audit"] = {
            "status": "ok",
            "passed": passed,
            "faithfulness": faithfulness_score,
            "faithfulness_reason": faithfulness.reason,
            "hallucination_rate": hallucination_score,
            "hallucination_reason": hallucination.reason,
        }
    except Exception as exc:
        logger.warning("DeepEval evaluation failed (%s) -- falling back to stub", exc)
        state["audit"] = {
            "status": "stub",
            "note": "DeepEval evaluation failed -- check Ollama is running and orchestrator logs",
            "passed": bool(recommendation),
            "faithfulness": None,
            "hallucination_rate": None,
        }

    state.setdefault("trace", []).append("auditor_agent")
    return state