# Project Report: Resume Parser

**Name:** Ava Iranmanesh
**Course:** CMPSC 441  
**Project:** NLP-Based Resume Parsing and Candidate Ranking System

---

## Section 1: System Scenarios

The resume parser is a recruiter-facing tool that ingests a large dataset of resumes, processes them through a four-stage NLP pipeline, and produces ranked, filterable candidate reports. The system is capable of handling the following scenarios:

**Scenario 1: Bulk Resume Ingestion**  
A recruiter uploads a CSV dataset containing thousands of resumes across multiple job categories. The system reads each row, constructs structured `Resume` objects, and makes them available for downstream processing. In testing, the system successfully loaded 500 resumes from a 42,000-record dataset spanning 25 job categories.

**Scenario 2: Text Normalization and Preprocessing**  
Raw resume text is noisy, containing punctuation, numbers, boilerplate, and filler language. The system tokenizes each resume, strips stopwords, and applies Porter stemming to reduce words to their root forms. This produces a clean token list that downstream stages can process consistently regardless of how a candidate phrased their experience.

**Scenario 3: Skill and Keyword Extraction**  
The system identifies technical skills from resume text by matching stemmed tokens against a curated taxonomy of roughly 80 skills spanning programming languages, frameworks, databases, cloud tools, DevOps technologies, and methodological concepts. It also extracts the top 30 most frequent tokens as general keywords for each candidate.

**Scenario 4: Domain Clustering**  
Once skills are extracted across the entire corpus, the system groups them into clusters using K-Means. Each cluster represents a coherent skill domain (for example, one cluster may center on data science tools while another groups DevOps and cloud infrastructure skills). Each candidate is then assigned to the cluster that best matches their primary skill.

**Scenario 5: Candidate Scoring**  
Each candidate receives a normalized score between 0 and 10 based on two factors: skill breadth (how many distinct domains their skills span) and skill depth (total number of distinct skills identified). The formula weights depth at 60% and breadth at 40%, reflecting that recruiters value both specialization and versatility.

**Scenario 6: Score-Based Filtering**  
A recruiter can filter the candidate pool to only those who meet a minimum score threshold. For example, calling `report.filter_by_score(5.0)` returns only candidates who scored at or above 5.0, which supports shortlisting workflows without manually reviewing every profile.

**Scenario 7: Report Export**  
The system exports the full ranked candidate list to either JSON or CSV format. The JSON export includes metadata (generation timestamp, total count) alongside per-candidate fields: resume ID, job category, score, cluster assignment, top keywords, and top skills. The CSV export follows the same structure in a tabular format suited to spreadsheet tools.

**Scenario 8: Per-Category Score Analysis**  
After processing, the system groups candidates by job category and computes the average score within each category. This lets a recruiter see at a glance which categories in the dataset are strong (for example, Data Science and DevOps candidates may score higher on average than categories with less technical vocabulary).

---

## Section 2: Prompt Engineering and Model Parameter Choice

The resume parser uses classical NLP methods rather than a large language model as its core processing engine. The design decision behind this was deliberate: the skill extraction task is well-defined enough that a curated taxonomy with stemmed matching is both faster and more predictable than an LLM at inference time over 42,000 records.

That said, the system does make a series of structured decisions that are equivalent in intent to prompt engineering, in the sense that they control how the model interprets and responds to input.

**Text preprocessing choices as implicit prompting**  
The `TextPreprocessor` applies three sequential transformations before any skill matching occurs: lowercasing and punctuation removal, stopword filtering, and Porter stemming. These transformations function as a kind of pre-prompt, ensuring the downstream skill matcher sees normalized input. Without stemming, "Kubernetes" and "kubernetes" would be treated as distinct tokens and the matcher would miss the stemmed form `kubernet`. The choice of Porter stemming over Snowball or lemmatization was intentional: Porter is more aggressive, which is appropriate for a technical vocabulary where partial stem matches are desirable.

**Taxonomy construction as knowledge grounding**  
The `_STEMMED_SKILLS` set in `keyword_extractor.py` is the system's knowledge base. It was constructed by manually stemming a representative set of technical terms and verifying that the stemmer output was consistent. This is analogous to constructing a system prompt that tells a language model which concepts to recognize: the taxonomy tells the extractor which token patterns are meaningful. The human-readable label map (`_SKILL_LABELS`) then reverses the stemming for output, which mirrors how a prompted LLM would be asked to return clean, human-facing text rather than internal representations.

**Scoring formula as a decision rule**  
The `ScoreCalculator` encodes a deliberate weighting: depth is valued at 60% and breadth at 40%, with depth capping out at 15 skills and breadth capping at 5 distinct domains. These thresholds were chosen to reflect realistic recruiter expectations: a candidate with 15 or more identified skills is competitive regardless of domain spread, but a candidate with 5 or more distinct domains is likely a generalist. Adjusting these constants changes how the system ranks candidates, which is functionally equivalent to adjusting temperature or weighting parameters in a probabilistic model.

**Clustering configuration**  
The `SkillClusterer` is initialized with `num_clusters=8` and `random_state=42`. The cluster count was chosen to match the rough number of recognizable technical domains in the dataset (frontend, backend, data science, DevOps, databases, security, mobile, and general software engineering). Setting `random_state=42` ensures reproducible results across runs, which is equivalent to setting temperature to 0 in an LLM context: deterministic output for the same input.

---

## Section 3: Tools Usage

The system integrates several tools from the Python AI and NLP ecosystem.

**NLTK**  
The `TextPreprocessor` uses NLTK for tokenization (`word_tokenize`), stopword filtering (`stopwords.words`), and stemming (`PorterStemmer`). NLTK corpora are downloaded automatically on first run via `nltk.download`, which means the system self-configures without requiring manual setup.

**scikit-learn**  
The `SkillClusterer` uses scikit-learn's `KMeans` and `TfidfVectorizer`. The vectorizer converts skill names into character-level n-gram TF-IDF features (bigrams through 4-grams), which captures sub-word structure and makes the clustering robust to minor variations in skill naming. `KMeans` then groups skills by these feature vectors. This is the primary machine learning tool call in the system.

**NumPy**  
NumPy underpins the scikit-learn matrix operations in the clustering step. It is listed explicitly in `requirements.txt` to ensure version compatibility.

**pandas**  
The `ResumeDataset` loader reads the CSV using Python's built-in `csv` module for reliability on large files. Pandas is available in the environment and was used during development for exploratory analysis of the dataset structure and column naming conventions across different CSV formats.

**CSV and JSON standard library tools**  
The `Report` class uses Python's built-in `csv` and `json` modules to write structured exports. These act as the system's output interface, equivalent to a tool that formats and delivers results to an end user.

---

## Section 4: Planning and Reasoning

The system implements explicit multi-step reasoning through its pipeline architecture. Each stage builds on the output of the previous one, and no stage can run correctly without the stages before it completing successfully.

**Stage 1: Preprocessing**  
`TextPreprocessor.preprocess()` converts raw resume text into a normalized token list. This stage reasons about what is and is not a meaningful unit: it strips punctuation, filters stopwords, and stems, so that the downstream extractor operates on semantically consistent input rather than surface-level text.

**Stage 2: Corpus-level skill aggregation**  
Before building individual candidate profiles, `Pipeline.run()` collects all tokens across all resumes and runs skill extraction on the entire corpus. This is a deliberate planning decision: the clusterer needs to see the full range of skills present in the dataset before it can partition them into meaningful groups. Running extraction per-resume first and clustering later would produce cluster assignments that are not globally consistent.

**Stage 3: Cluster fitting**  
`SkillClusterer.fit()` reasons about the scale of the data before committing to a cluster count. If fewer unique skills exist than the requested number of clusters, it dynamically reduces `k` to avoid degenerate clustering. It also guards against the edge case of a single unique skill, for which K-Means cannot run at all.

**Stage 4: Per-candidate profile construction**  
With the clusterer fitted on the global skill distribution, each resume is processed individually. Keywords, skills, cluster assignment, and score are computed in sequence, and the results are wrapped into a `CandidateProfile`. This structure means that scoring a candidate requires all prior reasoning steps to have completed.

**Stage 5: Report generation and filtering**  
The `Report` class aggregates all profiles and exposes a `filter_by_score` method that applies a threshold-based decision rule. This final reasoning step converts a ranked list into a shortlist, which is the recruiters actionable output.

This chain-of-reasoning structure ensures that each decision is informed by prior context, which mirrors how chain-of-thought prompting works in LLM-based systems: no step is taken in isolation.

---

## Section 5: RAG Implementation

The system implements a form of retrieval-augmented generation in its skill extraction stage. Rather than relying on a general-purpose model to infer whether a token represents a technical skill, the `KeywordExtractor` retrieves matches from a structured skill taxonomy at inference time.

**Knowledge base**  
The taxonomy in `_STEMMED_SKILLS` serves as the retrieval corpus. It contains stemmed representations of roughly 80 canonical technical skills across six categories: programming languages, web and frontend technologies, backend frameworks, data and machine learning tools, DevOps and cloud platforms, and databases.

**Retrieval mechanism**  
For each resume, the extractor scans the preprocessed token list and retrieves any token that appears in the taxonomy. This is a direct lookup retrieval rather than a similarity search, which is appropriate given that the preprocessing pipeline has already normalized tokens to a form the taxonomy was built around.

**Augmented output**  
After retrieval, the extractor maps each stemmed token back to its human-readable label using `_SKILL_LABELS`, which acts as the generation step: the raw retrieved key is augmented with a clean display form before being included in the candidate profile and exported report.

**Data source integration**  
The Kaggle resume dataset (`data/resumes.csv`) provides 42,104 real resumes across 25 job categories. The taxonomy was informed by scanning this dataset to identify the most commonly occurring technical terms, which means the retrieval corpus was built from the same data distribution the system operates on. This is analogous to how RAG systems build their vector stores from domain-relevant documents.

---

## Section 6: Additional Tools and Innovation

**Score distribution analysis by job category**  
Beyond ranking individual candidates, `main.py` computes the average score per job category across the processed sample. This gives the recruiter a macro-level view of the talent pool: which categories have strong candidates on average, and which are sparse. This kind of aggregate analysis is not a standard feature of simple resume parsers and adds actionable insight beyond individual rankings.

**Dual export format support**  
The `Report` class supports both JSON and CSV export without requiring any configuration changes. JSON export is structured for programmatic consumption (for example, feeding results into a downstream system or API), while CSV export is oriented toward human review in spreadsheet tools. Supporting both formats from a single unified report object makes the system more useful across different recruiter workflows.

**Automatic NLTK corpus management**  
The `TextPreprocessor` module includes self-healing download logic that checks for required NLTK corpora at import time and downloads any that are missing. This eliminates a common setup failure point and makes the system runnable immediately after `pip install` without additional configuration steps.

**Dynamic cluster sizing**  
Rather than failing or producing degenerate clusters when the dataset is small, `SkillClusterer.fit()` dynamically reduces the number of clusters to match the number of unique skills present. This makes the system robust to edge cases (such as processing a very small sample) without requiring the user to manually tune the cluster count.

---

## Code Quality and Modular Design

The project is organized into two top-level layers: `src/models/` for data entities and actors, and `src/processing/` for the NLP pipeline stages. `pipeline.py` wires the processing stages together, and `main.py` serves as the entry point.

Each class has a single well-defined responsibility. `TextPreprocessor` only handles text normalization. `KeywordExtractor` only handles matching and retrieval. `SkillClusterer` only handles vectorization and clustering. `ScoreCalculator` only handles scoring. This separation means each component can be tested, swapped, or extended independently.

All public interfaces use Python type hints throughout, and private state is encapsulated behind properties. Version control and environment management follow standard practices: dependencies are pinned in `requirements.txt`, and the codebase is organized to be cloneable and runnable without additional configuration.
