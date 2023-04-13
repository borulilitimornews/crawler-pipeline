from pathlib import Path
from seeder import MainSeeder
from src.process_corpus import GetInitialCorpus, GetFinalCorpus


class BuildCorpus:
    SOLR_API_URL = "http://localhost:8983/solr/nutch/select"
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

    def __init__(self) -> None:
        # self.start_row = 1
        # self.rows = 3
        self.main_seeder = MainSeeder()
        self.lang_proba_threshold = self.main_seeder.lang_proba_threshold
        self.lid_model_file_path = self.main_seeder.lid_model_file_path
        self.tetun_lang = self.main_seeder.tetun_language
        self.get_initial_corpus = GetInitialCorpus(
            self.SOLR_API_URL,
            # self.start_row,
            # self.rows,
            self.tetun_lang,
            self.lang_proba_threshold,
            self.lid_model_file_path,
        )
        self.get_skipped_corpus_file_path = Path(
            "pipeline/data/skipped_corpus.txt"
        )
        self.final_corpus_file_path = Path("pipeline/data/final_corpus.txt")
        self.generate_initial_corpus = (
            self.get_initial_corpus.generate_initial_corpus()
        )
        self.get_final_corpus = GetFinalCorpus(
            self.generate_initial_corpus,
            self.get_skipped_corpus_file_path,
            self.START_PATTERNS,
            self.END_PATTERNS,
            self.IN_PATTERNS,
        )

    def run(self) -> None:
        try:
            self.get_final_corpus.get_final_text(
                self.final_corpus_file_path, self.get_skipped_corpus_file_path
            )
            print("\nThe final corpus has been generated sucessfully.\n\n")
        except Exception as e:
            print(f"\nError while generating final corpus: {e}\n")


if __name__ == "__main__":
    build_corpus = BuildCorpus()
    build_corpus.run()
