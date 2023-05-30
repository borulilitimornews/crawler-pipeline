import random
from pathlib import Path
from typing import List


class GenerateData:
    """ Load and generate ramdom samples for the corpus contents evaluation. """

    def __init__(self, corpus_file_path: Path, sample_directory_path: Path, total_sample: int, total_doc_segments: int) -> None:
        self.corpus_file_path = corpus_file_path
        self.sample_directory_path = sample_directory_path
        self.total_sample = total_sample
        self.total_doc_segments = total_doc_segments

    def load_corpus(self) -> List[str]:
        with self.corpus_file_path.open('r', encoding='utf-8') as f_corpus:
            contents = f_corpus.read().split('\n\n')
        return contents

    def generate_sample(self) -> List[str]:
        corpus = self.load_corpus()
        for i in range(1, self.total_sample+1, 1):
            ramdom_contents = "\n\n".join(
                random.sample(corpus, self.total_doc_segments))
            sample_path = f"{self.sample_directory_path}/sample_{i}.txt"
            with open(sample_path, 'w', encoding='utf-8') as f_sample:
                f_sample.write(ramdom_contents)
        print(
            f"A total of {self.total_sample} samples have been generated successfully.")
