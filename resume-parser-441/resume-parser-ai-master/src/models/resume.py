from datetime import datetime
from typing import Optional


class Resume:
    def __init__(self, id: int, raw_text: str, job_title: str, submitted_at: Optional[datetime] = None):
        self._id = id
        self._raw_text = raw_text
        self._job_title = job_title
        self._submitted_at = submitted_at or datetime.now()

    def get_raw_text(self) -> str:
        return self._raw_text

    @property
    def id(self) -> int:
        return self._id

    @property
    def job_title(self) -> str:
        return self._job_title

    @property
    def submitted_at(self) -> datetime:
        return self._submitted_at

    def __repr__(self) -> str:
        return f"Resume(id={self._id}, job_title='{self._job_title}')"
