from src.collection_stat import CollectionStatistic
from common_utils import config


class ViewCollectionStatistic:
    """ This class shows some statistics extracted from the collection. """

    def __init__(self) -> None:
        self.collection_stat = CollectionStatistic(
            config.FINAL_CORPUS_FILE_PATH,
            config.URL_INL_OUT_LINKS_FILE_PATH,
            config.STATS_INL_OUT_LINKS_FILE_PATH
        )

    def run(self) -> None:
        self.collection_stat.generate_stats()


if __name__ == '__main__':
    generate_stat = ViewCollectionStatistic()
    generate_stat.run()
