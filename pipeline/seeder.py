from common_utils import config
from src.get_seed_word import GetSeedWords
from src.get_seed_url import GetSeedUrl


class MainSeeder:
    """ This class generates seed words and seed URLs, 
    including domains from the seed URLs. """

    def __init__(self) -> None:
        get_seed_word = GetSeedWords(
            config.LANGUAGE,
            config.CORPUS_SAMPLE_RATIO,
            config.LANG_PROBA_THRESHOLD,
            config.SEED_WORD_SAMPLE,
        )
        self.generate_get_seed_words = get_seed_word.generate_seed_words
        self.get_url = GetSeedUrl(
            config.EXTENSION_TO_EXCLUDE, config.DOMAINS_TO_EXCLUDE
        )

    def run(self) -> None:
        try:
            self.get_url.generate_seed_urls(
                config.INITIAL_CORPUS_FILE_PATH,
                config.SEED_WORDS_FILE_PATH,
                config.NUTCH_SEED_URL_FILE_PATH,
                config.LID_MODEL_FILE_PATH,
                config.DOMAIN_FILE_PATH,
                self.generate_get_seed_words,
            )
            print(f"\nSeed URLs have been generated successfully.\n\n")
        except Exception as e:
            print(f"\nError while generating the seed URLs: {e}\n")


if __name__ == "__main__":
    seeder = MainSeeder()
    seeder.run()
