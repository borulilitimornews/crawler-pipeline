from pathlib import Path

""" This module contains configuration of the paths, urls, patterns, etc. """

# File paths
MAIN_CORPUS_FILE_PATH = Path("pipeline/data/timornews_corpus.txt")
SEED_WORDS_FILE_PATH = Path("pipeline/data/seed_words.txt")
NUTCH_SEED_URL_FILE_PATH = Path("./nutch/urls/seed.txt")
DOMAIN_FILE_PATH = Path("pipeline/data/domains.txt")
LID_MODEL_FILE_PATH = Path("pipeline/tetun_lid/model_9977.pkl")
FINAL_CORPUS_FILE_PATH = Path("pipeline/data/final_corpus.txt")
STATS_INL_OUT_LINKS_FILE_PATH = Path("pipeline/data/stats_inlinks_outlinks.txt")
URL_INL_OUT_LINKS_FILE_PATH = Path("pipeline/data/url_inlinks_outlinks.txt")
LOG_FILE = Path("pipeline/logs/execution.log")

# Solr
SOLR_API_URL = "http://localhost:8983/solr/nutch/select"
START_SOLR_DOCS = 0
#TOTAL_SOLR_DOCS = 355987

# Language, language model, and corpus.
LANGUAGE = "tet"
LANG_PROBA_THRESHOLD = 0.95
CORPUS_SAMPLE_RATIO = 0.1
NUM_SEED_WORD_SAMPLE = 3
GOOGLE_SEARCH_NUM_RESULT = 10
MAX_SEED_URL_LENGTH = 300

# Patterns to exclude the URLs retrieved for the seed URLs.
EXTENSION_TO_EXCLUDE = [
    "\.(rtf)$",
    "\.pptx?$",
    "\.docx?$",
    "\.(txt)$",
    "\.(pdf)$",
    "\.mp3",
    "\.mp4",
    "\.avi",
]

DOMAINS_TO_EXCLUDE = [
    "youtube.com",
    "instagram.com",
    "facebook.com",
    "linkedin.com",
]
