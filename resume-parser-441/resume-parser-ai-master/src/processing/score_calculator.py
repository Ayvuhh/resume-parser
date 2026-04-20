from typing import Dict, List


class ScoreCalculator:
    def __init__(self):
        self._min_score: int = 0
        self._max_score: int = 10

    def calculate(self, clusters: Dict[int, List[str]]) -> float:
        if not clusters:
            return 0.0
        total_skills = sum(len(v) for v in clusters.values())
        num_domains = len(clusters)

        # Breadth: how many distinct skill domains the candidate covers
        breadth = min(num_domains / 5.0, 1.0)
        # Depth: raw skill count, capped at 15 for full score
        depth = min(total_skills / 15.0, 1.0)

        raw = (breadth * 0.4 + depth * 0.6) * 10.0
        return self.normalize(raw)

    def normalize(self, raw: float) -> float:
        clamped = max(float(self._min_score), min(float(self._max_score), raw))
        return round(clamped, 2)

    @property
    def min_score(self) -> int:
        return self._min_score

    @property
    def max_score(self) -> int:
        return self._max_score
