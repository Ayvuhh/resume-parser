from typing import List

from src.models.resume import Resume
from src.models.candidate_profile import CandidateProfile
from src.models.report import Report
from src.processing.text_preprocessor import TextPreprocessor
from src.processing.keyword_extractor import KeywordExtractor
from src.processing.skill_clusterer import SkillClusterer
from src.processing.score_calculator import ScoreCalculator


class Pipeline:
    def __init__(self, num_clusters: int = 8):
        self._preprocessor = TextPreprocessor()
        self._extractor = KeywordExtractor()
        self._clusterer = SkillClusterer(num_clusters=num_clusters)
        self._calculator = ScoreCalculator()

    def run(self, resumes: List[Resume]) -> Report:
        # Pre-process every resume and accumulate tokens
        all_tokens: List[str] = []
        per_resume_tokens: List[List[str]] = []

        for resume in resumes:
            tokens = self._preprocessor.preprocess(resume)
            per_resume_tokens.append(tokens)
            all_tokens.extend(tokens)

        # Fit the skill clusterer on all skills found in the corpus
        all_skills = self._extractor.extract_skills(all_tokens)
        if all_skills:
            self._clusterer.fit(all_skills)

        # Build a CandidateProfile for each resume
        profiles: List[CandidateProfile] = []
        for resume, tokens in zip(resumes, per_resume_tokens):
            keywords = self._extractor.extract_keywords(tokens)
            skills = self._extractor.extract_skills(tokens)

            if skills and self._clusterer._fitted:
                cluster = self._clusterer.assign_cluster(skills[0])
            else:
                cluster = 0

            skill_clusters = {cluster: skills} if skills else {}
            score = self._calculator.calculate(skill_clusters)

            profile = CandidateProfile(
                resume=resume,
                keywords=keywords,
                skills=skills,
                cluster=cluster,
                score=score,
            )
            profiles.append(profile)

        return Report(profiles=profiles)
