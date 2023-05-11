from src.collection_stat import CollectionStatistic
from common_utils import config

class ViewCollectionStatistic:
    """ This class shows some statistics extracted from the collection. """

    def __init__(self) -> None:
        self.collection_stat = CollectionStatistic(
            config.SOLR_API_URL,
            config.LANGUAGE,
            config.LANG_PROBA_THRESHOLD,
            config.LID_MODEL_FILE_PATH,
            config.URL_INL_OUT_LINKS_FILE_PATH,
            config.STATS_INL_OUT_LINKS_FILE_PATH
        )

    def run(self):
        self.collection_stat.generate_stats()

if __name__ == '__main__':
    generate_stat = ViewCollectionStatistic()
    generate_stat.run()