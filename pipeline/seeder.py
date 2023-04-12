from get_seeds.get_seed_word import GetSeedWords
from get_seeds.get_seed_url import GetSeedUrl
from pathlib import Path


class MainSeeder:
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

    def __init__(self) -> None:
        # Parameters
        self.tetun_language = "tet"
        self.corpus_sample_ratio = 0.1
        self.lang_proba_threshold = 0.95
        self.n_seed_word_sample = 3

        get_seed_word = GetSeedWords(
            self.tetun_language,
            self.corpus_sample_ratio,
            self.lang_proba_threshold,
            self.n_seed_word_sample,
        )
        # This is used in the 'run' as a param of the 'generate_seed_urls'
        self.generate_get_seed_words = get_seed_word.generate_seed_words

        self.get_url = GetSeedUrl(
            self.EXTENSION_TO_EXCLUDE, self.DOMAINS_TO_EXCLUDE
        )
        # Paths
        self.timornews_corpus_file_path = Path(
            "pipeline/data/timornews_corpus.txt"
        )
        self.seed_words_file_path = Path("pipeline/data/seed_words.txt")
        self.nutch_seed_url_file_path = Path("./nutch/urls/seed.txt")
        self.domain_file_path = Path("pipeline/data/domains.txt")
        self.lid_model_file_path = Path("pipeline/tetun_lid/model.pkl")

    def run(self) -> None:
        try:
            self.get_url.generate_seed_urls(
                self.timornews_corpus_file_path,
                self.seed_words_file_path,
                self.nutch_seed_url_file_path,
                self.lid_model_file_path,
                self.domain_file_path,
                self.generate_get_seed_words,
            )
            print(f"\nSeed URLs have been generated successfully.\n")
        except Exception as e:
            print(f"\nError while generating seed URLs: {e}\n")


if __name__ == "__main__":
    seeder = MainSeeder()
    seeder.run()
