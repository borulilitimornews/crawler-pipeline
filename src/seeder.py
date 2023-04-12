from get_seed_url import GetUrl
from pathlib import Path


class MainSeeder:
    EXTENSION_TO_EXCLUDE = ['\.(rtf)$', '\.pptx?$', '\.docx?$', '\.(txt)$',
                            '\.(pdf)$', '\.mp3', '\.mp4', '\.avi']
    DOMAINS_TO_EXCLUDE = ['youtube.com', 'instagram.com',
                          'facebook.com', 'linkedin.com']

    def __init__(self) -> None:
        self.get_url = GetUrl(self.EXTENSION_TO_EXCLUDE,
                              self.DOMAINS_TO_EXCLUDE)
        self.timornews_corpus_file_path = Path("src/data/timornews_corpus.txt")
        self.seed_words_file_path = Path("src/data/seed_words.txt")
        self.nutch_seed_url_file_path = Path("./nutch/urls/seed.txt")
        self.domain_file_path = Path("src/data/domains.txt")
        self.lid_model_file_path = Path("src/lid_model/model.pkl")

    def run(self) -> None:
        try:
            self.get_url.generate_seed_urls(
                self.timornews_corpus_file_path,
                self.seed_words_file_path,
                self.nutch_seed_url_file_path,
                self.lid_model_file_path,
                self.domain_file_path
            )
            print(f"\nSeed URLs have been generated successfully.\n")
        except Exception as e:
            print(f"\nError while generating seed URLs: {e}\n")


if __name__ == '__main__':
    seeder = MainSeeder()
    seeder.run()
