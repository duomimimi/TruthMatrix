# TruthMatrix

**Multi-Layer AI Output Verification System**

TruthMatrix is a comprehensive verification framework that detects AI hallucinations, validates facts across independent sources, and ensures output reliability through adversarial checking. It acts as a guardian for AI-generated content.

## Key Features

- **Hallucination Detection**: Identifies confidently-stated false information before it reaches users
- **Cross-Source Validation**: Verifies claims against multiple independent sources using retrieval-augmented approaches
- **Adversarial Checking**: Runs AI outputs through a second model trained to spot errors and inconsistencies
- **Confidence Scoring**: Assigns reliability scores to each claim in the output
- **Source Attribution**: Traces every factual claim back to its source
- **Audit Trail**: Maintains a complete verification history for compliance and review

## Quick Start

```bash
# Install
pip install truthmatrix

# Basic usage
from truthmatrix import Verifier

verifier = Verifier(config={
    "adversarial_model": "gpt-4",
    "validation_sources": ["wikipedia", "arxiv", "custom-db"],
    "confidence_threshold": 0.8
})

result = verifier.verify("The capital of France is Paris")
# Returns: verified=True, confidence=0.99, sources=[...]
```

## Architecture

```
┌─────────────────────────────────────────────┐
│           AI Output (Unverified)             │
└─────────────────────┬───────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│          TruthMatrix Pipeline               │
│  ┌─────────────┐  ┌─────────────────────┐  │
│  │  Claim     │  │   Cross-Source       │  │
│  │  Extraction│  │   Validator          │  │
│  └─────────────┘  └─────────────────────┘  │
│  ┌─────────────┐  ┌─────────────────────┐  │
│  │ Adversarial│  │   Confidence        │  │
│  │  Checker   │  │   Scorer             │  │
│  └─────────────┘  └─────────────────────┘  │
└─────────────────────┬───────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│         Verified Output + Audit Trail        │
└─────────────────────────────────────────────┘
```

**Core Components:**

- **Claim Extractor**: Breaks output into discrete factual claims
- **Cross-Source Validator**:Retrieves and cross-checks information against external sources
- **Adversarial Checker**: Second-pass model trained to identify errors
- **Confidence Scorer**: Assigns reliability scores with explainability
- **Audit Logger**: Records full verification history

## License

MIT License