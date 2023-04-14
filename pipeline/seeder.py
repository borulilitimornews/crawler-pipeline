from common_utils import config
from src.get_seed_word import GetSeedWords
from src.get_seed_url import GetSeedUrl


class MainSeeder:
    """ This class generates seed words and seed URLs, 
    including domains from the seed URLs. """

    def __init__(self) -> None:
        get_seed_word = GetSeedWords(
            config.MAIN_CORPUS_FILE_PATH,
            config.LANGUAGE,
            config.CORPUS_SAMPLE_RATIO,
            config.LID_MODEL_FILE_PATH,
            config.LANG_PROBA_THRESHOLD,
            config.NUM_SEED_WORD_SAMPLE,
            config.SEED_WORDS_FILE_PATH,
        )
        self.get_url = GetSeedUrl(
            config.EXTENSION_TO_EXCLUDE,
            config.DOMAINS_TO_EXCLUDE,
            get_seed_word.generate_seed_words(),
            config.GOOGLE_SEARCH_NUM_RESULT,
            config.MAX_SEED_URL_LENGTH,
            config.NUTCH_SEED_URL_FILE_PATH,
            config.DOMAIN_FILE_PATH,
        )

    def run(self) -> None:
        try:
            self.get_url.generate_seed_urls()
            print(f"\nSeed URLs have been generated successfully.\n\n")

        except Exception as e:
            print(f"\nError while generating the seed URLs: {e}\n")


if __name__ == "__main__":
    seeder = MainSeeder()
    seeder.run()
