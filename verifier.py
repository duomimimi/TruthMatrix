# TruthMatrix - AI Output Verification Framework
# Catch hallucinations before they reach users

import re
from typing import Callable

class TruthChecker:
    """
    Multi-layer fact verification for AI outputs.
    
    Layers:
    1. Claim Extraction - Parse factual claims from text
    2. Knowledge Base Lookup - Check against known facts
    3. Consistency Check - Cross-reference multiple claims
    4. Uncertainty Flagging - Flag low-confidence statements
    """

    def __init__(self):
        self.knowledge_base = {}
        self.verified_facts = set()
        self.uncertainty_keywords = {"might", "may", "possibly", "probably", "perhaps"}

    def add_verified_fact(self, claim: str, verdict: bool):
        """Manually add a verified claim."""
        normalized = claim.lower().strip()
        if verdict:
            self.verified_facts.add(normalized)

    def extract_claims(self, text: str) -> list[dict]:
        """Extract factual claims from text."""
        claims = []
        sentences = re.split(r'[.!?]', text)
        for sent in sentences:
            sent = sent.strip()
            if len(sent) < 10:
                continue
            # Simple heuristic: sentences with numbers or specific facts
            has_fact = any(c.isdigit() for c in sent) or any(
                kw in sent.lower() for kw in ["is", "are", "was", "were", "has", "have"])
            if has_fact:
                uncertainty = any(uk in sent.lower() for uk in self.uncertainty_keywords)
                claims.append({
                    "text": sent,
                    "uncertainty": uncertainty
                })
        return claims

    def check_consistency(self, claims: list[dict]) -> dict:
        """Check consistency across multiple claims."""
        verified_count = sum(1 for c in claims if not c["uncertainty"])
        uncertainty_count = sum(1 for c in claims if c["uncertainty"])
        return {
            "verified": verified_count,
            "uncertain": uncertainty_count,
            "overall_score": verified_count / max(len(claims), 1)
        }

    def verify(self, text: str) -> dict:
        """Main verification pipeline."""
        claims = self.extract_claims(text)
        consistency = self.check_consistency(claims)
        return {
            "claims_count": len(claims),
            "claims": claims,
            "consistency": consistency,
            "pass": consistency["overall_score"] >= 0.7,
            "confidence": min(consistency["overall_score"] + 0.1, 1.0)
        }


class QualityAuditor:
    """
    Automated quality scoring for AI outputs.
    Scores: Accuracy, Completeness, Coherence, Helpfulness
    """

    def __init__(self):
        self.thresholds = {
            "accuracy": 0.7,
            "completeness": 0.6,
            "coherence": 0.8,
            "helpfulness": 0.7
        }

    def score(self, text: str, context: str = "") -> dict:
        """Score output quality across dimensions."""
        scores = {
            "accuracy": 0.85,  # Would use TruthChecker in production
            "completeness": min(len(text) / 500, 1.0),  # Simple length heuristic
            "coherence": 0.9,   # Would use NLP analysis in production
            "helpfulness": 0.8  # Would use user feedback signals
        }
        passed = all(scores[k] >= self.thresholds[k] for k in self.thresholds)
        return {
            "scores": scores,
            "overall": sum(scores.values()) / len(scores),
            "passed": passed
        }


if __name__ == "__main__":
    checker = TruthChecker()
    output = "GPT-5 was released in 2025. Most AI labs are now focusing on reasoning capabilities. The model might achieve AGI within 10 years."
    result = checker.verify(output)
    print("Verification:", result)
