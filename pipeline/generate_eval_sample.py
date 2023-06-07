from common_utils import config
from src.get_sample_corpus import GetSampleCorpus


class GenerateEvalSample:
    """ Main class for generating sample data. """

    def __init__(self) -> None:
        self.generate_eval_sample = GetSampleCorpus(
            config.FINAL_CORPUS_FILE_PATH,
            config.EVAL_SAMPLE_DIRECTORY_PATH,
            config.TOTAL_SAMPLES,
            config.TOTAL_TEXT_PAGES
        )

    def run(self):
        try:
            self.generate_eval_sample.generate_sample()
        except ValueError as e:
            print(f"Insuficient sample: {e}")


if __name__ == '__main__':
    eval_samples = GenerateEvalSample()
    eval_samples.run()
