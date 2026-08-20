import json

from app.database.database import SessionLocal
from app.services.matching_service import find_best_matching_post


DATASET_PATH = "evaluation/dataset.json"


def main():
    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        dataset = json.load(file)

    db = SessionLocal()

    correct = 0
    evaluated = 0
    results = []

    try:
        for case in dataset:
            description = case["image_description"]
            expected_post_id = case["expected_post_id"]

            try:
                result = find_best_matching_post(
                    image_description=description,
                    db=db,
                    image_metadata={
                        "subject": description,
                        "category": "unknown",
                        "attributes": [],
                        "caption": description,
                        "confidence": 1.0,
                    },
                )

                if isinstance(result, dict):
                    post = result.get("post")
                    predicted_post_id = post.id if post else None
                    status = result.get("status")
                    similarity = result.get("similarity")
                    reason = result.get("reason")
                else:
                    predicted_post_id = result.id if result else None
                    status = "matched" if result else "no_match"
                    similarity = None
                    reason = ""

            except TypeError:
                result = find_best_matching_post(
                    image_description=description,
                    db=db,
                )

                predicted_post_id = result.id if result else None
                status = "matched" if result else "no_match"
                similarity = None
                reason = ""

            is_correct = predicted_post_id == expected_post_id

            if is_correct:
                correct += 1

            evaluated += 1

            results.append(
                {
                    "case_id": case["id"],
                    "expected_post_id": expected_post_id,
                    "predicted_post_id": predicted_post_id,
                    "status": status,
                    "similarity": similarity,
                    "correct": is_correct,
                    "reason": reason,
                }
            )

        precision = correct / evaluated if evaluated else 0.0

        print("\n===== EVALUATION RESULTS =====")
        print(f"Total cases: {evaluated}")
        print(f"Correct top-1 predictions: {correct}")
        print(f"Top-1 precision: {precision:.2%}")

        print("\nCase results:")

        for result in results:
            print(
                f"Case {result['case_id']}: "
                f"expected={result['expected_post_id']} "
                f"predicted={result['predicted_post_id']} "
                f"correct={result['correct']}"
            )

        output = {
            "total_cases": evaluated,
            "correct_predictions": correct,
            "top_1_precision": precision,
            "results": results,
        }

        with open(
            "evaluation/results.json",
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                output,
                file,
                indent=2,
            )

    finally:
        db.close()


if __name__ == "__main__":
    main()