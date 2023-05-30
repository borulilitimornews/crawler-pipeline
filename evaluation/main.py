import config
from generate_data import GenerateData


class Main:
    """ Main class for generating sample data. """

    def __init__(self) -> None:
        self.generate_data = GenerateData(config.MAIN_CORPUS_FILE_PATH, config.SAMPLE_DIRECTORY_PATH,
                                          config.TOTAL_DATA_SAMPLES, config.TOTAL_DOCS_SEGMENTS)

    def run(self):
        self.generate_data.generate_sample()


if __name__ == '__main__':
    main = Main()
    main.run()
