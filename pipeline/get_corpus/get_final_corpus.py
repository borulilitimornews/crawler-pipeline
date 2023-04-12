from pathlib import Path


class GetFinalCorpus:
    """
    A class to filter the input text that meets the predefined filter conditions 
    and blank lines more than two times in consecutive order.
    """

    def __init__(self, start_patterns, end_patterns, in_patterns) -> None:
        self.start_patterns = start_patterns
        self.end_patterns = end_patterns
        self.in_patterns = in_patterns

    def is_text_to_filter(self, text_line: str) -> bool:
        """
        Check if the given text meets the predefined filter conditions.

        :param text_line: the input text.
        :return: True if the given text meets, False otherwise.
        """

        text_to_filter = any(
            text_line.lower().startswith(start_pattern)
            or text_line.lower().endswith(end_pattern)
            or in_pattern in text_line.lower()
            for start_pattern in self.start_patterns
            for end_pattern in self.end_patterns
            for in_pattern in self.in_patterns
        )

        return text_to_filter

    def filtered_text(
        self,
        initial_corpus_file_path: Path,
        final_corpus_file_path: Path,
        max_consecutive_newlines: int = 2,
    ) -> str:
        """
        Filtered the input text that meets the predefined filter conditions.

        :param initial_corpus_file_path: a path to the input file.
        :param final_corpus_file_path: a path to the output file.
        :param max_consecutive_newlines: the maximum newlines allowed after each document.
        :return: a conclusion message.
        """
        with initial_corpus_file_path.open("r", encoding="utf-8") as f:
            unique_sentences = []
            seen_sentences = set()
            consecutive_newlines = 0

            for line in f:
                line = line.strip()
                if self.is_text_to_filter(line):
                    print("Skipped: ", line)
                    continue

                if line not in seen_sentences:
                    if line == "":
                        consecutive_newlines += 1
                    else:
                        consecutive_newlines = 0
                    if (
                        line == ""
                        and consecutive_newlines >= max_consecutive_newlines
                    ):
                        continue
                    else:
                        unique_sentences.append(line)
                        if not line == "":
                            seen_sentences.add(line)
                        print("Added: ", line)

        with final_corpus_file_path.open("w", encoding="utf-8") as f:
            f.write("\n".join(unique_sentences))

        return f"Total unique sentences: {len(unique_sentences)}"
