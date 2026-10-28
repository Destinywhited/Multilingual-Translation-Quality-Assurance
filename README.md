Multilingual Translation Quality Assurance

Overview

A Python-based quality-assurance framework for structured evaluation cases covering translation from Spanish (ES), French (FR), and German (DE) into English.

The framework validates case data, applies a configurable penalty-based screening score, flags cases below a quality threshold, preserves error annotations, and generates JSON and Markdown reports.

Dataset limitation: The included cases are synthetic examples for testing the framework. They are not client-provided translations or evidence of real machine-translation engine performance.

Features

- Input validation and duplicate case-ID detection.
- Support for ES, FR, and DE source-language labels.
- MQM-inspired accuracy, fluency, and terminology categories.
- Minor, major, and critical severity levels.
- Configurable screening threshold.
- Corrected reference translations for below-threshold cases.
- JSON evaluation results and summary.
- Error-pattern reports in JSON and Markdown.
- Automated unit tests.

Project Structure

- "data/" — evaluation case dataset.
- "src/" — evaluator, entry point, and pattern analyzer.
- "tests/" — automated unit tests.
- "reports/" — summaries, findings, and pattern reports.
- "output/" — generated evaluation results.

Requirements

- Python 3.10 or later recommended.
- No third-party packages are required by the current implementation.

Run the Evaluation

From the repository root:

python -m src.run_evaluation

Run Error-Pattern Analysis

python -m src.pattern_analysis

Run Tests

python -m unittest discover -s tests -v

Scoring

The current project-defined screening score starts at 100 and subtracts 5 points per minor error, 15 per major error, and 30 per critical error, with a minimum of zero. Scores below 80 are flagged for review.

This is an illustrative scoring rule, not an official MQM scoring formula.

Current Demonstration Results

The synthetic dataset contains 12 cases and 6 annotated errors. Three cases fall below the configured threshold. The category totals are four accuracy errors, one fluency error, and one terminology error.

These figures describe only the included test dataset.

Limitations and Next Steps

The current dataset is synthetic. To evaluate a real translation engine, provide source passages, machine translations, relevant terminology or style guidance, and engine/version metadata where available.

Real engine-level recurring patterns must be established using actual outputs and traceable engine identifiers.