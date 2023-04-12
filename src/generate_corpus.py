from pathlib import Path
from get_initial_corpus import GetInitialCorpus
from get_final_corpus import GetFinalCorpus
from seeder import MainSeeder


class MainGetInitalCorpus:
    SOLR_API_URL = "http://localhost:8983/solr/nutch/select"

    def __init__(self) -> None:
        self.start_row = 0
        self.rows = 3  # 65687
        self.get_initial_corpus = GetInitialCorpus(
            self.SOLR_API_URL, self.start_row, self.rows)
        self.main_seeder = MainSeeder()
        self.lid_model_file_path = self.main_seeder.lid_model_file_path
        self.initial_corpus_file_path = Path('src/data/initial_corpus.txt')

    def run(self) -> None:
        try:
            self.get_initial_corpus.generate_corpus(
                self.lid_model_file_path,
                self.initial_corpus_file_path
            )
            print("\nThe final corpus has been generated sucessfully.\n\n")
        except Exception as e:
            print(f"\nError while generating initial corpus: {e}\n")


class MainGetFinalCorpus:
    START_PATTERNS = ["home", "previous", "next", "comments on", "comment on",
                      "labels", "etiquetas:", "address", "from", "http", "»", "«"]
    IN_PATTERNS = ["div>", "ul>", "ol>", "li>", "a>", "span>", "p>",
                   "+670", "670)", " | ",  "headline", "copyright", ]
    END_PATTERNS = ["...", "…", "download", "»", "«"]

    def __init__(self) -> None:
        self.main_initial_corpus = MainGetInitalCorpus()
        self.get_final_corpus = GetFinalCorpus(
            self.START_PATTERNS, self.END_PATTERNS, self.IN_PATTERNS)
        self.initial_corpus_file_path = self.main_initial_corpus.initial_corpus_file_path
        self.final_corpus_file_path = Path("src/data/final_corpus.txt")

    def run(self) -> None:
        try:
            self.get_final_corpus.filtered_text(
                self.initial_corpus_file_path,
                self.final_corpus_file_path
            )
            print(f"\nThe final corpus has been generated sucessfully.\n")
        except Exception as e:
            print(f"\nError while generating final corpus: {e}\n")


if __name__ == '__main__':
    gen_initial_corpus = MainGetInitalCorpus()
    gen_initial_corpus.run()

    gen_final_corpus = MainGetFinalCorpus()
    gen_final_corpus.run()
