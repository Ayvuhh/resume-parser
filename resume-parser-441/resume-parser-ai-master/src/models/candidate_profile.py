from typing import List
from .resume import Resume


class CandidateProfile:
    def __init__(self, resume: Resume, keywords: List[str], skills: List[str], cluster: int, score: float):
        self._resume = resume
        self._keywords = keywords
        self._skills = skills
        self._cluster = cluster
        self._score = score

    def get_score(self) -> float:
        return self._score

    def get_summary(self) -> str:
        top_skills = ", ".join(self._skills[:5]) if self._skills else "none identified"
        top_keywords = ", ".join(self._keywords[:5]) if self._keywords else "none identified"
        return (
            f"[{self._resume.job_title}] "
            f"Score: {self._score:.1f}/10 | "
            f"Cluster: {self._cluster} | "
            f"Skills: {top_skills} | "
            f"Keywords: {top_keywords}"
        )

    @property
    def resume(self) -> Resume:
        return self._resume

    @property
    def keywords(self) -> List[str]:
        return self._keywords

    @property
    def skills(self) -> List[str]:
        return self._skills

    @property
    def cluster(self) -> int:
        return self._cluster

    def __repr__(self) -> str:
        return f"CandidateProfile(job='{self._resume.job_title}', score={self._score:.1f})"
