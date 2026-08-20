from sqlalchemy.orm import Session

from app.models.ai_usage import AIUsage


# Estimated Gemini pricing configuration.
# These values are kept in one place so they can be updated
# without changing the processing code.
INPUT_COST_PER_MILLION = 0.30
OUTPUT_COST_PER_MILLION = 2.50


def calculate_ai_cost(
    input_tokens: int,
    output_tokens: int,
) -> float:
    input_cost = (
        input_tokens / 1_000_000
    ) * INPUT_COST_PER_MILLION

    output_cost = (
        output_tokens / 1_000_000
    ) * OUTPUT_COST_PER_MILLION

    return round(
        input_cost + output_cost,
        8,
    )


def record_ai_usage(
    db: Session,
    operation: str,
    model: str,
    input_tokens: int,
    output_tokens: int,
) -> AIUsage:
    estimated_cost = calculate_ai_cost(
        input_tokens=input_tokens,
        output_tokens=output_tokens,
    )

    usage = AIUsage(
        operation=operation,
        model=model,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        estimated_cost=estimated_cost,
    )

    db.add(usage)
    db.commit()
    db.refresh(usage)

    return usage