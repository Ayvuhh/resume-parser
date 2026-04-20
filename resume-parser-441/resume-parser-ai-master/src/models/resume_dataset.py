import csv
from datetime import datetime
from typing import List
from .resume import Resume


class ResumeDataset:
    def __init__(self, source: str):
        self._source = source
        self._total_records = 0

    def load(self) -> List[Resume]:
        resumes = []
        with open(self._source, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                raw_text = row.get("Resume", row.get("resume_text", "")).strip()
                job_title = row.get("Category", row.get("job_title", "Unknown")).strip()
                if not raw_text:
                    continue
                resume = Resume(
                    id=i + 1,
                    raw_text=raw_text,
                    job_title=job_title,
                    submitted_at=datetime.now(),
                )
                resumes.append(resume)
        self._total_records = len(resumes)
        return resumes

    @property
    def source(self) -> str:
        return self._source

    @property
    def total_records(self) -> int:
        return self._total_records

    def __repr__(self) -> str:
        return f"ResumeDataset(source='{self._source}', total_records={self._total_records})"
