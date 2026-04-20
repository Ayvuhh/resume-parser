import os
import sys

from src.models.recruiter import Recruiter
from src.models.resume_dataset import ResumeDataset
from pipeline import Pipeline

DATA_PATH = os.path.join("data", "resumes.csv")
SAMPLE_SIZE = 500  # number of resumes to process (set to None for all 42k)


def main():
    if not os.path.exists(DATA_PATH):
        print(f"Dataset not found at '{DATA_PATH}'.")
        sys.exit(1)

    recruiter = Recruiter(name="Admin", email="admin@example.com")
    dataset = ResumeDataset(source=DATA_PATH)

    print("Loading resumes...")
    all_resumes = recruiter.upload_dataset(dataset)
    resumes = all_resumes[:SAMPLE_SIZE] if SAMPLE_SIZE else all_resumes
    print(f"Loaded {len(resumes)} resumes ({dataset.total_records} total in dataset).")

    print("Running pipeline (pre-process → extract → cluster → score)...")
    pipeline = Pipeline(num_clusters=8)
    report = recruiter.view_candidates(pipeline.run(resumes))

    # Display top candidates by score
    top = sorted(report.profiles, key=lambda p: p.get_score(), reverse=True)[:10]
    print(f"\nTop 10 Candidates (scored 0–10):")
    print("─" * 70)
    for i, profile in enumerate(top, 1):
        print(f"  {i:2}. {profile.get_summary()}")

    # Score distribution by category
    print(f"\nAverage score by job category:")
    print("─" * 70)
    category_scores: dict = {}
    for p in report.profiles:
        cat = p.resume.job_title
        category_scores.setdefault(cat, []).append(p.get_score())
    for cat, scores in sorted(category_scores.items()):
        avg = sum(scores) / len(scores)
        print(f"  {cat:<30} avg score: {avg:.2f}  (n={len(scores)})")

    # Export
    path = recruiter.export_report(report, format="json")
    print(f"\nFull report exported → {path}")

    # Filter demo
    threshold = 5.0
    qualified = report.filter_by_score(threshold)
    print(f"Candidates scoring ≥ {threshold}: {len(qualified)} / {len(report.profiles)}")


if __name__ == "__main__":
    main()
