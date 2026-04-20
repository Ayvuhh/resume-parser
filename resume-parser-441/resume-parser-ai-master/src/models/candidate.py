from .resume import Resume


class Candidate:
    def __init__(self, name: str, email: str):
        self._name = name
        self._email = email

    def submit_resume(self, resume: Resume) -> Resume:
        return resume

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email

    def __repr__(self) -> str:
        return f"Candidate(name='{self._name}', email='{self._email}')"
