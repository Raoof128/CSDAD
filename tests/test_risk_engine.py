"""Unit tests for the risk fusion engine."""

from __future__ import annotations

from backend.engines.risk_engine import RiskEngine


def test_risk_classification_boundaries():
    engine = RiskEngine()
    assert engine.classify(10) == "LOW"
    assert engine.classify(45) == "MEDIUM"
    assert engine.classify(70) == "HIGH"
    assert engine.classify(90) == "CRITICAL"


def test_risk_compute_includes_deception_markers():
    engine = RiskEngine()
    result = engine.compute(
        manipulation_score=40,
        misinfo_score=30,
        influence_score=20,
        domain_credibility=80,
        emotional_intensity=10,
        deception_markers=2,
    )
    assert result.level in {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
    assert any("Deception markers" in note for note in result.explanation)
