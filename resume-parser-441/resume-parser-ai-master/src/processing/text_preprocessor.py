import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from typing import List
from src.models.resume import Resume

for _pkg in ["punkt", "punkt_tab", "stopwords"]:
    try:
        nltk.data.find(f"tokenizers/{_pkg}" if "punkt" in _pkg else f"corpora/{_pkg}")
    except LookupError:
        nltk.download(_pkg, quiet=True)


class TextPreprocessor:
    def __init__(self):
        self._language = "english"
        self._stemmer = PorterStemmer()
        self._stop_words = set(stopwords.words(self._language))

    def tokenize(self, text: str) -> List[str]:
        cleaned = re.sub(r"[^a-zA-Z\s]", " ", text.lower())
        return word_tokenize(cleaned)

    def remove_stop_words(self, tokens: List[str]) -> List[str]:
        return [t for t in tokens if t.isalpha() and t not in self._stop_words and len(t) > 2]

    def stem(self, tokens: List[str]) -> List[str]:
        return [self._stemmer.stem(t) for t in tokens]

    def preprocess(self, resume: Resume) -> List[str]:
        tokens = self.tokenize(resume.get_raw_text())
        tokens = self.remove_stop_words(tokens)
        tokens = self.stem(tokens)
        return tokens

    @property
    def language(self) -> str:
        return self._language
