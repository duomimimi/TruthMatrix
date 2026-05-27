# TruthMatrix User Guide

> AI Output Validation Layer — Multi-layer Cross-Validation that Leaves Nowhere for Hallucinations to Hide

---

## Core Concept

TruthMatrix is an **AI output validation framework** whose core responsibility is to perform multi-layered fact-checking and quality verification on AI-generated content before it reaches users.

**Why does it matter?**

All current large language models produce "hallucinations" — content that looks reasonable but is actually incorrect. Sources of hallucinations include:
- Erroneous information in training data
- Logical deviations during reasoning
- Nonsense under edge conditions
- Confusion when synthesizing multiple information sources

TruthMatrix solves this through a three-layer validation mechanism:
1. **Fact Layer**: Verifies whether objective facts in the output are accurate
2. **Logic Layer**: Checks whether the reasoning chain is self-consistent
3. **Consistency Layer**: Ensures output doesn't contradict context or known knowledge

---

## How to Use

### Step 1: Initialize the Validator

```python
from truthmatrix import Validator, FactChecker, LogicChecker

# Create multi-layer validator
validator = Validator(
    layers=[
        FactChecker(provider="serp"),      # Fact layer: web verification
        LogicChecker(provider="local"),    # Logic layer: local rules
        ConsistencyChecker()               # Consistency layer: context comparison
    ],
    threshold=0.85  # Flag as suspicious if confidence below 85%
)
```

### Step 2: Validate AI Output

```python
async def process_with_verification(prompt: str, ai_output: str):
    # Use NexusCore to get AI output
    from nexuscore import Router
    router = Router(models)
    raw_output = await router.route(prompt)

    # Hand off to TruthMatrix for validation
    result = await validator.verify(raw_output, context=prompt)

    if result.is_healthy:
        return result.output  # Passed validation, return directly
    else:
        # Mark suspicious areas
        return result.output_with_annotations
```

### Step 3: Handle Validation Failure

```python
result = await validator.verify(output, context=prompt)

if not result.is_healthy:
    print(f"Found {len(result.issues)} issues:")
    for issue in result.issues:
        print(f"  [{issue.type}] {issue.description}")
        print(f"  Original text: {issue.text}")
        print(f"  Suggestion: {issue.suggestion}")

    # Can trigger regeneration
    if result.confidence < 0.5:
        await regenerate_with_feedback(prompt, result.issues)
```

---

## Code Example

```python
import asyncio
from truthmatrix import Validator, VerificationReport

async def agent_loop(prompt: str):
    validator = Validator(threshold=0.8)

    for attempt in range(3):
        # Get AI output
        output = await get_ai_response(prompt)

        # Validate output
        report = await validator.verify(output, context=prompt)

        if report.is_healthy:
            return output

        # Validation failed, regenerate with feedback
        prompt = f"{prompt}\n\nPlease avoid the following errors: {report.summary}"

    return "Unable to generate reliable output, human intervention required"
```

---

## Use Cases

### Case 1: News Content Moderation
Media AI automatically validates news through TruthMatrix before publishing, intercepting false information before release. For fact-intensive domains like finance and sports, error rates can be reduced by over 90%.

### Case 2: Medical AI-Assisted Diagnosis
After diagnostic recommendations are generated, TruthMatrix automatically verifies: Are drug interactions accurate? Do dosages comply with guidelines? Are there conflicts with patient history? Protecting patient safety.

### Case 3: Legal Document Generation
After contract clauses are generated, the validator automatically checks: Are cited legal provisions still valid? Are numerical amounts consistent? Are all parties' rights balanced?

### Case 4: Customer Service Bot Quality Control
Every automated response is validated through TruthMatrix, ensuring no erroneous information is given to users. Especially important when sensitive information like pricing, policies, or validity periods is involved.

---

## Relationship with Other Modules

| Module | Relationship | Description |
|:----:|:----:|:-----|
| NexusCore | Upstream Dependency | NexusCore provides AI output; TruthMatrix handles validation |
| QualityForge | Scoring Source | TruthMatrix validation results become QualityForge quality scores |
| SelfMend | Trigger Source | When TruthMatrix finds serious issues, it triggers SelfMend's repair flow |
| AgentHive | Validation Node | AgentHive can have a dedicated "validator agent" using TruthMatrix |

**Architecture Position**: TruthMatrix is the quality assurance layer, connecting NexusCore and all other output modules, ensuring the reliability of final content.

---

## Validation Report Interpretation

```python
report = await validator.verify(output, context=prompt)

print(f"""
Validation Result: {'✅ Passed' if report.is_healthy else '❌ Failed'}
Confidence: {report.confidence:.1%}
Issue Count: {len(report.issues)}

Layer Details:
  Fact Layer: {'✅' if report.fact_score > 0.8 else '⚠️'} {report.fact_score:.1%}
  Logic Layer: {'✅' if report.logic_score > 0.8 else '⚠️'} {report.logic_score:.1%}
  Consistency: {'✅' if report.consistency_score > 0.8 else '⚠️'} {report.consistency_score:.1%}
""")
```

---

## Next Steps

- See the [QualityForge Guide](./qualityforge-guide_en.md) — How to build self-improvement systems based on TruthMatrix
- See the [SelfMend Guide](./selfmend-guide_en.md) — How TruthMatrix triggers self-repair
- Get started: `pip install truthmatrix`

---

*TruthMatrix — Upgrade AI output from "do your best" to "trustworthy"*