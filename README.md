# Resume Parser

An NLP-based resume parsing system that extracts skills, clusters candidates by domain, and scores each resume on a 0–10 scale. Built for CMPSC 441.

---

## What it does

1. Loads a dataset of resumes (CSV)
2. Pre-processes the raw text using NLTK (tokenization, stopword removal, stemming)
3. Extracts keywords and matches against a skill taxonomy
4. Groups skills into domain clusters using K-Means
5. Scores each candidate based on skill breadth and depth
6. Generates a filterable report exportable as JSON or CSV

---

## Project Structure

```
resume-parser-ai/
├── data/
│   └── resumes.csv              # 42k real resumes across 25 job categories
├── src/
│   ├── models/
│   │   ├── resume.py            # Resume entity
│   │   ├── candidate.py         # Candidate actor
│   │   ├── recruiter.py         # Recruiter actor
│   │   ├── resume_dataset.py    # Dataset loader
│   │   ├── candidate_profile.py # Scored candidate output
│   │   └── report.py            # Filterable report with export
│   └── processing/
│       ├── text_preprocessor.py # NLTK tokenize / stopwords / stem
│       ├── keyword_extractor.py # TF-based keywords + skill matching
│       ├── skill_clusterer.py   # K-Means clustering over skill vectors
│       └── score_calculator.py  # 0–10 normalized scoring
├── pipeline.py                  # Ties all processing steps together
├── main.py                      # Entry point
└── requirements.txt
```

---

## Setup

```bash
pip install -r requirements.txt
python main.py
```

NLTK corpora (`punkt`, `stopwords`) are downloaded automatically on first run.

---

## Dataset

The included dataset (`data/resumes.csv`) contains 42,104 resumes across 25 categories:

> Advocate, Arts, Automation Testing, Blockchain, Business Analyst, Civil Engineer, Data Science, Database, DevOps Engineer, DotNet Developer, ETL Developer, Electrical Engineering, Finance, HR, Hadoop, Health and Fitness, Java Developer, Mechanical Engineer, Network Security Engineer, Operations Manager, PMO, Python Developer, SAP Developer, Sales, Testing, Web Designing

Source: [Kaggle — Resume Dataset](https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset)

---

## Sample Output

```
Top 10 Candidates (scored 0–10):
──────────────────────────────────────────────────────────────────────
   1. [Data Science] Score: 8.4/10 | Cluster: 3 | Skills: Python, TensorFlow, pandas, scikit-learn, SQL
   2. [DevOps Engineer] Score: 7.9/10 | Cluster: 1 | Skills: Docker, Kubernetes, AWS, Jenkins, Terraform
   3. [Java Developer] Score: 7.6/10 | Cluster: 2 | Skills: Java, Spring, Hibernate, MySQL, REST API
   ...
```

---

## Design

The class structure follows the UML diagrams defined in the project specification. The two main actors are `Recruiter` (uploads datasets, views and exports reports) and `Candidate` (submits individual resumes). All processing is handled by a four-stage pipeline: `TextPreprocessor → KeywordExtractor → SkillClusterer → ScoreCalculator`, with results wrapped into `CandidateProfile` objects and aggregated into a `Report`.
