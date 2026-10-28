import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = ROOT / "data" / "evaluation_cases.json"
JSON_OUTPUT = ROOT / "reports" / "recurring_error_patterns.json"
MD_OUTPUT = ROOT / "reports" / "recurring_error_patterns.md"


def analyze_patterns(cases):
    category_counts = Counter()
    severity_counts = Counter()
    language_categories = defaultdict(Counter)
    patterns = []

    for case in cases:
        language = case["source_language"].upper()

        for error in case["errors"]:
            category = error["category"]
            severity = error["severity"]

            category_counts[category] += 1
            severity_counts[severity] += 1
            language_categories[language][category] += 1

            patterns.append({
                "case_id": case["id"],
                "language": language,
                "category": category,
                "severity": severity,
                "span": error["span"],
                "description": error["description"],
                "data_origin": case.get(
                    "data_origin", "unspecified"
                ),
            })

    return {
        "dataset_origin": "synthetic_test_cases",
        "engine_level_claim": False,
        "interpretation": (
            "Candidate patterns from synthetic annotations only. "
            "Actual engine-level recurrence requires real engine "
            "outputs and engine identifiers."
        ),
        "total_annotated_errors": len(patterns),
        "counts_by_category": dict(category_counts),
        "counts_by_severity": dict(severity_counts),
        "counts_by_language_and_category": {
            language: dict(counts)
            for language, counts in sorted(
                language_categories.items()
            )
        },
        "annotated_patterns": patterns,
    }


def write_markdown(report):
    lines = [
        "# Recurring Error-Pattern Analysis",
        "",
        "**Dataset:** Synthetic test cases",
        "",
        "> These findings are illustrative. They do not establish "
        "real translation-engine performance or recurrence.",
        "",
        f"Total annotated errors: {report['total_annotated_errors']}",
        "",
        "## Counts by category",
        "",
    ]

    for category, count in sorted(
        report["counts_by_category"].items()
    ):
        lines.append(f"- {category}: {count}")

    lines.extend(["", "## Annotated error patterns", ""])

    for item in report["annotated_patterns"]:
        lines.extend([
            f"### {item['case_id']} — {item['category']} "
            f"({item['severity']})",
            f"- Language: {item['language']}",
            f"- Error span: `{item['span']}`",
            f"- Description: {item['description']}",
            "",
        ])

    lines.extend([
        "## Limitations",
        "",
        "- No real machine-translation engine output was supplied.",
        "- No engine identifiers or production corpus were supplied.",
        "- The annotations are synthetic and manually authored.",
        "- Repeated category counts alone do not prove a recurring "
        "engine-level failure.",
    ])

    return "\n".join(lines) + "\n"


def main():
    with INPUT_FILE.open("r", encoding="utf-8") as file:
        cases = json.load(file)

    report = analyze_patterns(cases)

    JSON_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with JSON_OUTPUT.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=2, ensure_ascii=False)

    MD_OUTPUT.write_text(
        write_markdown(report),
        encoding="utf-8",
    )

    print("Pattern analysis completed.")
    print(f"Annotated errors: {report['total_annotated_errors']}")
    print(f"Category counts: {report['counts_by_category']}")
    print(f"JSON report: {JSON_OUTPUT}")
    print(f"Markdown report: {MD_OUTPUT}")


if __name__ == "__main__":
    main()