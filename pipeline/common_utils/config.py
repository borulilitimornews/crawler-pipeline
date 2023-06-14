from pathlib import Path

""" This module contains main configuration of the pipeline. """

# File paths
MAIN_CORPUS_FILE_PATH = Path("pipeline/data/initial_corpus.txt")
SEED_WORDS_FILE_PATH = Path("pipeline/data/seed_words.txt")
NUTCH_SEED_URL_FILE_PATH = Path("./nutch/urls/seed.txt")
DOMAIN_FILE_PATH = Path("pipeline/data/domains.txt")
LID_MODEL_FILE_PATH = Path("pipeline/lid/lid_model.pkl")
FINAL_CORPUS_FILE_PATH = Path("pipeline/data/final_corpus.txt")
STATS_IN_OUT_LINKS_FILE_PATH = Path(
    "pipeline/data/stats_inlinks_outlinks.txt")
URL_INL_OUT_LINKS_FILE_PATH = Path("pipeline/data/url_inlinks_outlinks.txt")
LOG_FILE = Path("pipeline/log/execution.log")
EVAL_SAMPLE_DIRECTORY_PATH = Path("pipeline/data/evaluation_sample/")

# Solr
SOLR_API_URL = "http://localhost:8983/solr/nutch/select"
SOLR_START = 0
SOLR_ROWS = 1


# Language, LID model and corpus.
LANGUAGE = "tet"
LANG_PROBA_THRESHOLD = 0.95
CORPUS_SAMPLE_RATIO = 0.1
NUM_SEED_WORD_SAMPLE = 3
GOOGLE_SEARCH_NUM_RESULT = 10
MAX_SEED_URL_LENGTH = 300
MAX_CONSECUTIVE_NEW_LINE = 2

# Patterns to exclude from the URLs retrieved for the seed URLs.
EXTENSIONS_TO_EXCLUDE = [
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

# Total of samples for doc. quality evaluation and total text pages
TOTAL_SAMPLES = 6
TOTAL_TEXT_PAGES = 50
