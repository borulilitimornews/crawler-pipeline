from pathlib import Path
import joblib
from typing import List


class TetunLid:
    """
    Tetun LID class loads the LID model file, applies it to the input text, 
    and then extracts only texts that are predicted to Tetun with a certain 
    probability that meets the predefined threshold.
    """

    def __init__(self, tetun_lang: str, lang_proba_threshold) -> None:
        self.tetun_lang = tetun_lang
        self.lang_proba_threshold = lang_proba_threshold

    def load_lid_model(self, lid_model_file_path: Path) -> object:
        """ 
        Load language identification model.

        :param lid_model_file_path: a path to the Tetun LID model file.
        :return: Tetun LID model.
        """

        if not lid_model_file_path.exists():
            print(f"Model file not found at: {lid_model_file_path}")
            return []
        model = joblib.load(lid_model_file_path)

        return model

    def get_tetun_text(
        self, input_text: List[str], lid_model_file_path: Path
    ) -> List[str]:
        """
            Get Tetun words with a probability >= threshold. 

            :param input_text: a list of string.
            :param lid_model_file_path: a path to the LID model file.
            :return: a list of text
            """

        tetun_text = []
        tetun_lid_model = self.load_lid_model(lid_model_file_path)
        pred_probs = tetun_lid_model.predict_proba(input_text)
        for i, probs in enumerate(pred_probs):
            for j, lang in enumerate(tetun_lid_model.classes_):
                if (
                    lang == self.tetun_lang
                    and round(probs[j], 2) >= self.lang_proba_threshold
                ):
                    tetun_text.append(input_text[i])

        return tetun_text
