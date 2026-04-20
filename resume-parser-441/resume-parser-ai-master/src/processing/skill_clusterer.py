from typing import List, Dict
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


class SkillClusterer:
    def __init__(self, num_clusters: int = 8):
        self._num_clusters = num_clusters
        self._algorithm = "K-Means"
        self._vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4))
        self._model: KMeans = None
        self._cluster_map: Dict[int, List[str]] = {}
        self._fitted = False

    def fit(self, skills: List[str]) -> None:
        if not skills:
            return
        unique = list(dict.fromkeys(skills))
        k = min(self._num_clusters, len(unique))
        if k < 2:
            self._cluster_map = {0: unique}
            self._fitted = False
            return
        self._num_clusters = k
        matrix = self._vectorizer.fit_transform(unique)
        self._model = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = self._model.fit_predict(matrix)
        self._cluster_map = {}
        for skill, label in zip(unique, labels):
            self._cluster_map.setdefault(int(label), []).append(skill)
        self._fitted = True

    def assign_cluster(self, skill: str) -> int:
        if not self._fitted:
            return 0
        vec = self._vectorizer.transform([skill])
        return int(self._model.predict(vec)[0])

    def get_clusters(self) -> Dict[int, List[str]]:
        return self._cluster_map

    @property
    def num_clusters(self) -> int:
        return self._num_clusters

    @property
    def algorithm(self) -> str:
        return self._algorithm
