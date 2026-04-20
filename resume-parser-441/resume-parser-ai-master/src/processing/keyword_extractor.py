from typing import List

# Canonical skills matched after PorterStemmer is applied
_STEMMED_SKILLS = {
    # Languages
    "python", "java", "javascrip", "typescrip", "ruby", "swift", "kotlin", "scala",
    "php", "golang", "rust", "matlab", "perl", "bash",
    # Web / Frontend
    "react", "angular", "vuej", "html", "css", "bootstrap", "jquery", "webpack",
    # Backend / Frameworks
    "django", "flask", "fastapi", "express", "spring", "hibern", "laravel", "rail",
    # Data / ML
    "tensorflow", "pytorch", "keras", "sklearn", "panda", "numpy", "scipy", "spark",
    "hadoop", "hive", "kafka", "airflow", "tableau", "powerbi",
    # DevOps / Cloud
    "docker", "kubernet", "jenkins", "terraform", "ansible", "aws", "azur", "gcp",
    "linux", "nginx", "git",
    # Databases
    "mysql", "postgresql", "mongodb", "redis", "elasticsearch", "oracl", "sqlite",
    "cassandra", "dynamodb",
    # Concepts / Methodologies
    "machinlearn", "deeplearn", "nlp", "devop", "agil", "scrum", "kanban",
    "microservic", "restapi", "graphql", "blockchain", "cybersecur",
}

# Human-readable labels for display (best-effort reverse map)
_SKILL_LABELS = {
    "python": "Python", "java": "Java", "javascrip": "JavaScript",
    "typescrip": "TypeScript", "ruby": "Ruby", "swift": "Swift",
    "kotlin": "Kotlin", "scala": "Scala", "php": "PHP",
    "golang": "Go", "rust": "Rust", "matlab": "MATLAB",
    "perl": "Perl", "bash": "Bash", "react": "React",
    "angular": "Angular", "vuej": "Vue.js", "html": "HTML",
    "css": "CSS", "bootstrap": "Bootstrap", "jquery": "jQuery",
    "webpack": "Webpack", "django": "Django", "flask": "Flask",
    "fastapi": "FastAPI", "express": "Express.js", "spring": "Spring",
    "hibern": "Hibernate", "laravel": "Laravel", "rail": "Rails",
    "tensorflow": "TensorFlow", "pytorch": "PyTorch", "keras": "Keras",
    "sklearn": "scikit-learn", "panda": "pandas", "numpy": "NumPy",
    "scipy": "SciPy", "spark": "Apache Spark", "hadoop": "Hadoop",
    "hive": "Hive", "kafka": "Kafka", "airflow": "Airflow",
    "tableau": "Tableau", "powerbi": "Power BI", "docker": "Docker",
    "kubernet": "Kubernetes", "jenkins": "Jenkins", "terraform": "Terraform",
    "ansible": "Ansible", "aws": "AWS", "azur": "Azure",
    "gcp": "GCP", "linux": "Linux", "nginx": "Nginx",
    "git": "Git", "mysql": "MySQL", "postgresql": "PostgreSQL",
    "mongodb": "MongoDB", "redis": "Redis", "elasticsearch": "Elasticsearch",
    "oracl": "Oracle", "sqlite": "SQLite", "cassandra": "Cassandra",
    "dynamodb": "DynamoDB", "machinlearn": "Machine Learning",
    "deeplearn": "Deep Learning", "nlp": "NLP", "devop": "DevOps",
    "agil": "Agile", "scrum": "Scrum", "kanban": "Kanban",
    "microservic": "Microservices", "restapi": "REST API",
    "graphql": "GraphQL", "blockchain": "Blockchain",
    "cybersecur": "Cybersecurity",
}


class KeywordExtractor:
    def extract_keywords(self, tokens: List[str]) -> List[str]:
        freq: dict = {}
        for token in tokens:
            freq[token] = freq.get(token, 0) + 1
        return sorted(freq, key=freq.get, reverse=True)[:30]

    def extract_skills(self, tokens: List[str]) -> List[str]:
        seen = set()
        found = []
        for token in tokens:
            if token in _STEMMED_SKILLS and token not in seen:
                found.append(_SKILL_LABELS.get(token, token))
                seen.add(token)
        return found
