from pathlib import Path

# File Paths
INITIAL_CORPUS_FILE_PATH = Path("pipeline/data/timornews_corpus.txt")
SEED_WORDS_FILE_PATH = Path("pipeline/data/seed_words.txt")
NUTCH_SEED_URL_FILE_PATH = Path("./nutch/urls/seed.txt")
DOMAIN_FILE_PATH = Path("pipeline/data/domains.txt")
LID_MODEL_FILE_PATH = Path("pipeline/tetun_lid/model.pkl")
GET_SKIPPED_FILE_PATH = Path("pipeline/data/skipped_corpus.txt")
FINAL_CORPUS_FILE_PATH = Path("pipeline/data/final_corpus.txt")


# URLs
SOLR_API_URL = "http://localhost:8983/solr/nutch/select"


# Others
LANGUAGE = "tet"
LANG_PROBA_THRESHOLD = 0.95
CORPUS_SAMPLE_RATIO = 0.1
SEED_WORD_SAMPLE = 3

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

START_PATTERNS = [
    "home",
    "previous",
    "next",
    "comments on",
    "comment on",
    "labels",
    "etiquetas:",
    "address",
    "street",
    "from",
    "http",
    "»",
    "«",
    "←",
]

IN_PATTERNS = [
    "div>",
    "span>",
    "p>",
    "h1>",
    "h2>",
    "h3>",
    "h4>",
    "ul>",
    "ol>",
    "li>",
    "a>",
    "table>",
    "th>",
    "td>",
    " | ",
    "headline",
    "copyright",
    "+670",
    "670)",
]

END_PATTERNS = ["...", "…", "___", ",,,", "[…]", "download", "»", "«", "→"]