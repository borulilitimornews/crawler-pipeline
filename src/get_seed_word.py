import random
from collections import Counter
from tetuntokenizer.tokenizer import TetunWordTokenizer
from pathlib import Path
from typing import List, Dict
from utils import load_corpus, load_lid_model


class SeedWords:
    """ 
    The seeder class is composed of the following task:
    1. Get a random text sample with a ratio of 10% from the text corpus.
    2. Tokenize the text sample into tokens (or words) using TetunWordTokenizer.
    3. Applying LID model to get only tokens with the proba of being Tetun >= 0.95.
    4. Count the word frequency and calculate its probability of distribution.
    5. Sample three unique words and save in the seed file.
    """

    def get_sample_corpus(
        self, corpus_file_path: Path, sample_ratio: float = 0.1
    ) -> List[str]:
        """
        Generate a random text sample with a ratio of 10% from the text corpus.

        :param corpus_file_path: a path to the corpus file.
        :param sample_ration: the ratio of sample to get from the corpus text.
        :return: a list of corpus.
        """
        corpus = load_corpus(corpus_file_path)

        corpus_size = len(corpus)
        sample_size = int(sample_ratio * corpus_size)
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
        #print(f"Tokens: {words[:10]}")

        return words

    def get_tetun_words(
        self, corpus_file_path: Path,
        lid_model_file_path: Path,
        threshold: float = 0.95
    ) -> List[str]:
        """
        Get only the words with a probability of being Tetun >= 0.95

        :param lid_model_file_path: a path to the LID model file.
        :param words: a list of words.
        :return: a list of words
        """

        words = self.tokenize_sample_corpus(corpus_file_path)

        tetun_words = []
        lid_model = load_lid_model(lid_model_file_path)
        pred_probs = lid_model.predict_proba(words)
        for i, probs in enumerate(pred_probs):
            for j, lang in enumerate(lid_model.classes_):
                if lang == 'tet' and round(probs[j], 2) >= threshold:
                   #print(words[i], probs[j])
                    tetun_words.append(words[i])

        return tetun_words

    def calculate_proba_distribution(
        self, corpus_file_path: Path,
        lid_model_file_path: Path
    ) -> Dict:
        """
        Count the word frequency and calculate its probability of distribution.

        :param lid_model_file_path: a path to the LID model file.
        :param words: a list of words.
        :return: a dictionary contains words and their distribution probability.
        """

        words = self.get_tetun_words(corpus_file_path, lid_model_file_path)

        freq_dict = Counter(words)
        total_words = len(words)
        probs_dist = {word: count / total_words for word,
                      count in freq_dict.items()}

        return probs_dist

    def generate_seed_words(
        self, corpus_file_path: Path, lid_model_file_path: Path,
        seed_words_file_path: Path, num_samples: int = 3
    ) -> str:
        """
        Sample three unique words and save in the seed file.

        :param corpus_file_path: a path to the corpus file.
        :param seed_words_file_path: a path to the seed words file.
        :param lid_model_file_path: a path to the LID model file.
        :param num_samples: the number of words to sample.
        :return: a string of sampled words.
        """

        proba_dist = self.calculate_proba_distribution(
            corpus_file_path, lid_model_file_path)

        # Sample num_samples words (unique) from the distribution
        sequence_words = list(proba_dist.keys())
        weights = list(proba_dist.values())
        samples = set()
        while len(samples) < num_samples:
            sample = random.choices(sequence_words, weights)[0]
            samples.add(sample)
            sequence_words.remove(sample)
            weights.remove(proba_dist[sample])

        seeds = ' '.join(list(samples))
        print(f"Seed words: {seeds}")

        with seed_words_file_path.open('a', encoding='utf-8') as f:
            f.write(seeds + '\n')

        return seeds
