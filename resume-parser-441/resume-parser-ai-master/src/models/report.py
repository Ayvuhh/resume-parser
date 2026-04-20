import json
import csv
from datetime import datetime
from typing import List
from .candidate_profile import CandidateProfile


class Report:
    def __init__(self, profiles: List[CandidateProfile] = None):
        self._generated_at = datetime.now()
        self._profiles: List[CandidateProfile] = profiles or []

    def filter_by_score(self, min: float) -> List[CandidateProfile]:
        return [p for p in self._profiles if p.get_score() >= min]

    def export(self, format: str = "json") -> str:
        if format.lower() == "json":
            return self._export_json()
        elif format.lower() == "csv":
            return self._export_csv()
        raise ValueError(f"Unsupported format: {format}")

    def _export_json(self) -> str:
        data = {
            "generated_at": self._generated_at.isoformat(),
            "total": len(self._profiles),
            "profiles": [
                {
                    "resume_id": p.resume.id,
                    "job_title": p.resume.job_title,
                    "score": p.get_score(),
                    "cluster": p.cluster,
                    "keywords": p.keywords[:10],
                    "skills": p.skills[:10],
                    "summary": p.get_summary(),
                }
                for p in self._profiles
            ],
        }
        path = f"report_{self._generated_at.strftime('%Y%m%d_%H%M%S')}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return path

    def _export_csv(self) -> str:
        path = f"report_{self._generated_at.strftime('%Y%m%d_%H%M%S')}.csv"
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["resume_id", "job_title", "score", "cluster", "keywords", "skills"])
            for p in self._profiles:
                writer.writerow([
                    p.resume.id,
                    p.resume.job_title,
                    round(p.get_score(), 2),
                    p.cluster,
                    "|".join(p.keywords[:10]),
                    "|".join(p.skills[:10]),
                ])
        return path

    @property
    def profiles(self) -> List[CandidateProfile]:
        return self._profiles

    @property
    def generated_at(self) -> datetime:
        return self._generated_at
