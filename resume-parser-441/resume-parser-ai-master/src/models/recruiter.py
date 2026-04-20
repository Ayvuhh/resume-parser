from .resume_dataset import ResumeDataset
from .report import Report


class Recruiter:
    def __init__(self, name: str, email: str):
        self._name = name
        self._email = email

    def upload_dataset(self, dataset: ResumeDataset) -> list:
        return dataset.load()

    def view_candidates(self, report: Report) -> Report:
        return report

    def export_report(self, report: Report, format: str = "json") -> str:
        return report.export(format)

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email

    def __repr__(self) -> str:
        return f"Recruiter(name='{self._name}', email='{self._email}')"
