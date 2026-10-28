import json
import re
from collections import Counter
from pathlib import Path

SUPPORTED_LANGUAGES = {"ES", "FR", "DE"}
MQM_CATEGORIES = {"accuracy", "fluency", "terminology"}
SEVERITIES = {"minor", "major", "critical"}
QUALITY_THRESHOLD = 80


def normalize_text(text):
    """Normalize whitespace for basic text comparisons."""
    return re.sub(r"\s+", " ", str(text)).strip()


def validate_case(case):
    """Validate the required fields in one evaluation case."""
    required = {
        "id",
        "source_language",
        "source_text",
        "machine_translation",
        "reference_translation",
    }
    missing = required - case.keys()

    if missing:
        raise ValueError(f"Missing fields: {sorted(missing)}")

    language = case["source_language"].upper()
    if language not in SUPPORTED_LANGUAGES:
        raise ValueError(f"Unsupported language: {language}")

    for field in (
        "source_text",
        "machine_translation",
        "reference_translation",
    ):
        if not isinstance(case[field], str) or not case[field].strip():
            raise ValueError(f"{field} must be a non-empty string")

    if not isinstance(case["errors"], list):
        raise ValueError("errors must be a list")

    for error in case["errors"]:
        if error.get("category") not in MQM_CATEGORIES:
            raise ValueError("Invalid MQM category")

        if error.get("severity") not in SEVERITIES:
            raise ValueError("Invalid error severity")

        if not error.get("span"):
            raise ValueError("Each error must identify an error span")

    return True


def calculate_score(errors):
    """
    Calculate an illustrative score out of 100.

    Penalties: minor=5, major=15, critical=30.
    This is a project-defined screening score, not an official
    MQM score or a universal translation-quality standard.
    """
    penalties = {"minor": 5, "major": 15, "critical": 30}
    score = 100 - sum(
        penalties[error["severity"]] for error in errors
    )
    return max(0, score)


def evaluate_case(case):
    """Validate and evaluate one annotated translation case."""
    validate_case(case)

    errors = case["errors"]
    score = calculate_score(errors)

    return {
        "id": case["id"],
        "source_language": case["source_language"].upper(),
        "score": score,
        "threshold": QUALITY_THRESHOLD,
        "below_threshold": score < QUALITY_THRESHOLD,
        "error_count": len(errors),
        "errors": errors,
        "corrected_translation": (
            case["reference_translation"]
            if score < QUALITY_THRESHOLD
            else None
        ),
        "data_origin": case.get("data_origin", "unspecified"),
    }


def summarize_results(results):
    """Summarize errors by category, language, and severity."""
    categories = Counter()
    languages = Counter()
    severities = Counter()

    for result in results:
        languages[result["source_language"]] += 1
        for error in result["errors"]:
            categories[error["category"]] += 1
            severities[error["severity"]] += 1

    return {
        "cases_evaluated": len(results),
        "cases_below_threshold": sum(
            result["below_threshold"] for result in results
        ),
        "error_counts_by_category": dict(categories),
        "error_counts_by_language": dict(languages),
        "error_counts_by_severity": dict(severities),
        "quality_threshold": QUALITY_THRESHOLD,
        "scoring_note": (
            "Illustrative penalty-based screening score; "
            "not an official MQM score."
        ),
    }


def run_evaluation(input_path, output_path, summary_path):
    """Load cases, evaluate them, and write JSON evidence."""
    with open(input_path, "r", encoding="utf-8") as file:
        cases = json.load(file)

    if not isinstance(cases, list):
        raise ValueError("Input JSON must contain a list of cases")

    ids = [case.get("id") for case in cases]
    if len(ids) != len(set(ids)):
        raise ValueError("Case IDs must be unique")

    results = [evaluate_case(case) for case in cases]
    summary = summarize_results(results)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(summary_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2, ensure_ascii=False)

    with open(summary_path, "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2, ensure_ascii=False)

    return summary