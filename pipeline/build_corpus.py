from common_utils import config
from src.process_corpus import GetCorpus


class BuildCorpus:
    """ This class first extracts Tetun text from the mixed documents, 
    then preprocesses them to get the final clean corpus """

    def __init__(self) -> None:
        self.get_corpus = GetCorpus(
            config.SOLR_API_URL,
            config.LANGUAGE,
            config.LANG_PROBA_THRESHOLD,
            config.LID_MODEL_FILE_PATH,
            config.START_PATTERNS,
            config.END_PATTERNS,
            config.IN_PATTERNS,
            config.SKIPPED_CORPUS_FILE_PATH,
            config.FINAL_CORPUS_FILE_PATH,
        )

    def run(self) -> None:
        try:
            self.get_corpus.generate_corpus()
            print("\nThe final corpus has been generated sucessfully.\n\n")

        except Exception as e:
            print(f"\nError while generating the final corpus: {e}\n")


if __name__ == "__main__":
    build_corpus = BuildCorpus()
    build_corpus.run()
