import random
from collections import Counter
from tetuntokenizer.tokenizer import TetunWordTokenizer
from pathlib import Path
from typing import List, Dict
from common_utils.tetun_lid import TetunLid
from common_utils.utils import load_corpus


class GetSeedWords:
    """ 
    This class:
    (1) Get a random text sample as per the predefined ratio.
    (2) Tokenize the text sample into tokens (words).
    (3) Applying LID model to get tokens with the probability >= threshold.
    (4) Count the word frequency and calculate its probability of distribution.
    (5) Sample three unique words from (4) and save them in the seed file.
    """

    def __init__(
        self,
        tetun_lang: str,
        corpus_sample_ratio: float,
        lang_proba_threshold: float,
        num_seed_words_sample: int,
    ) -> None:
        self.corpus_sample_ratio = corpus_sample_ratio
        self.lang_proba_threshold = lang_proba_threshold
        self.num_seed_words_sample = num_seed_words_sample
        self.tetun_lang = tetun_lang
        self.tetun_lid = TetunLid(self.tetun_lang, self.lang_proba_threshold)

    def get_sample_corpus(self, corpus_file_path: Path) -> List[str]:
        """
        Generate a random text sample from the corpus as per the ratio.

        :param corpus_file_path: a path to the corpus file.
        :return: a list of text lines.
        """

        corpus = load_corpus(corpus_file_path)

        corpus_size = len(corpus)
        sample_size = int(self.corpus_sample_ratio * corpus_size)
        sample_corpus = random.sample(corpus, sample_size)

        return sample_corpus

    def tokenize_sample_corpus(self, corpus_file_path: Path) -> List[str]:
        """
        Tokenize the sample corpus into tokens.

        :param corpus_file_path: a path to the corpus file.
        :return: a list of words.
        """

        doc = self.get_sample_corpus(corpus_file_path)
        print(f"\nCorpus amount in sample: {len(doc)} sentences.")

        tokenizer = TetunWordTokenizer()
        doc_lower = str(doc).lower()
        words = tokenizer.tokenize(doc_lower)

        return words

    def calculate_proba_distribution(
        self, corpus_file_path: Path, lid_model_file_path: Path
    ) -> Dict:
        """
        Count the word frequency and calculate its probability of distribution.

        :param corpus_file_path: a path to the corpus file.
        :param lid_model_file_path: a path to the LID model file.
        :return: a dictionary contains words and their distribution probability.
        """

        # Apply Tetun LID model to the tokenized words
        words = self.tetun_lid.get_tetun_text(
            self.tokenize_sample_corpus(corpus_file_path), lid_model_file_path
        )

        freq_dict = Counter(words)
        total_words = len(words)
        probs_dist = {
            word: count / total_words for word, count in freq_dict.items()
        }

        return probs_dist

    def generate_seed_words(
        self,
        corpus_file_path: Path,
        lid_model_file_path: Path,
        seed_words_file_path: Path,
    ) -> str:
        """
        Sample three unique words and save in the seed file.

        :param corpus_file_path: a path to the corpus file.
        :param lid_model_file_path: a path to the LID model file.
        :param seed_words_file_path: a path to the seed words file.
        :return: a string of sampled words.
        """

        proba_dist = self.calculate_proba_distribution(
            corpus_file_path, lid_model_file_path
        )

        sequence_words = list(proba_dist.keys())
        weights = list(proba_dist.values())
        samples = set()
        while len(samples) < self.num_seed_words_sample:
            sample = random.choices(sequence_words, weights)[0]
            samples.add(sample)
            sequence_words.remove(sample)
            weights.remove(proba_dist[sample])

        seeds = " ".join(list(samples))
        print(f"Seed words: {seeds}")

        with seed_words_file_path.open("a", encoding="utf-8") as f:
            f.write(seeds + "\n")

        return seeds
