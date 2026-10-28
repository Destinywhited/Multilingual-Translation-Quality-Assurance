from pathlib import Path

from src.evaluator import run_evaluation


ROOT = Path(__file__).resolve().parents[1]

input_file = ROOT / "data" / "evaluation_cases.json"
output_file = ROOT / "output" / "evaluation_results.json"
summary_file = ROOT / "reports" / "evaluation_summary.json"

summary = run_evaluation(
    input_file,
    output_file,
    summary_file,
)

print("Evaluation completed.")
print(f"Cases evaluated: {summary['cases_evaluated']}")
print(f"Below threshold: {summary['cases_below_threshold']}")
print(f"Category counts: {summary['error_counts_by_category']}")
print(f"Severity counts: {summary['error_counts_by_severity']}")
print(f"Results: {output_file}")
print(f"Summary: {summary_file}")