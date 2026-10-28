import json
import tempfile
import unittest
from pathlib import Path

from src.evaluator import (
    QUALITY_THRESHOLD,
    calculate_score,
    evaluate_case,
    run_evaluation,
    validate_case,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = PROJECT_ROOT / "data" / "evaluation_cases.json"


class TestTranslationEvaluator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with DATA_FILE.open("r", encoding="utf-8") as file:
            cls.cases = json.load(file)

    def test_dataset_has_twelve_unique_cases(self):
        self.assertEqual(len(self.cases), 12)
        ids = [case["id"] for case in self.cases]
        self.assertEqual(len(ids), len(set(ids)))

    def test_all_supported_languages_are_present(self):
        languages = {case["source_language"] for case in self.cases}
        self.assertEqual(languages, {"ES", "FR", "DE"})

    def test_all_cases_pass_schema_validation(self):
        for case in self.cases:
            with self.subTest(case=case["id"]):
                self.assertTrue(validate_case(case))

    def test_critical_error_receives_expected_score(self):
        errors = [{"severity": "critical"}]
        self.assertEqual(calculate_score(errors), 70)

    def test_clean_case_scores_one_hundred(self):
        case = next(
            case for case in self.cases
            if case["id"] == "ES-001"
        )
        result = evaluate_case(case)
        self.assertEqual(result["score"], 100)
        self.assertFalse(result["below_threshold"])
        self.assertIsNone(result["corrected_translation"])

    def test_low_scoring_case_gets_reference_correction(self):
        case = next(
            case for case in self.cases
            if case["id"] == "ES-002"
        )
        result = evaluate_case(case)
        self.assertTrue(result["below_threshold"])
        self.assertEqual(
            result["corrected_translation"],
            case["reference_translation"],
        )

    def test_score_never_falls_below_zero(self):
        errors = [{"severity": "critical"} for _ in range(5)]
        self.assertEqual(calculate_score(errors), 0)

    def test_invalid_language_is_rejected(self):
        case = dict(self.cases[0])
        case["source_language"] = "IT"
        with self.assertRaises(ValueError):
            validate_case(case)

    def test_invalid_mqm_category_is_rejected(self):
        case = dict(self.cases[1])
        case["errors"] = [
            {
                "category": "made_up_category",
                "severity": "major",
                "span": "example",
                "description": "Invalid category test",
            }
        ]
        with self.assertRaises(ValueError):
            validate_case(case)

    def test_output_files_are_generated(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            results_path = temp / "results.json"
            summary_path = temp / "summary.json"

            summary = run_evaluation(
                DATA_FILE,
                results_path,
                summary_path,
            )

            self.assertTrue(results_path.exists())
            self.assertTrue(summary_path.exists())
            self.assertEqual(summary["cases_evaluated"], 12)

            with results_path.open(encoding="utf-8") as file:
                results = json.load(file)

            self.assertEqual(len(results), 12)


if __name__ == "__main__":
    unittest.main(verbosity=2)