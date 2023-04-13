from common_utils import config
from seeder import MainSeeder
from src.process_corpus import GetInitialCorpus, GetFinalCorpus


class BuildCorpus:
    """ This class first extracts Tetun text from the mixed documents, 
    then preprocesses them to get the final clean corpus """

    def __init__(self) -> None:
        self.main_seeder = MainSeeder()
        self.get_initial_corpus = GetInitialCorpus(
            config.SOLR_API_URL,
            config.LANGUAGE,
            config.LANG_PROBA_THRESHOLD,
            config.LID_MODEL_FILE_PATH,
        )
        self.generate_initial_corpus = (
            self.get_initial_corpus.generate_initial_corpus()
        )
        self.get_final_corpus = GetFinalCorpus(
            self.generate_initial_corpus,
            config.GET_SKIPPED_FILE_PATH,
            config.START_PATTERNS,
            config.END_PATTERNS,
            config.IN_PATTERNS,
        )

    def run(self) -> None:
        try:
            self.get_final_corpus.get_final_text(
                config.FINAL_CORPUS_FILE_PATH, config.GET_SKIPPED_FILE_PATH
            )
            print("\nThe final corpus has been generated sucessfully.\n\n")
        except Exception as e:
            print(f"\nError while generating final corpus: {e}\n")


if __name__ == "__main__":
    build_corpus = BuildCorpus()
    build_corpus.run()
