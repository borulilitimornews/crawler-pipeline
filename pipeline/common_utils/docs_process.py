import logging
import requests
import json
import tldextract
from common_utils import config
from typing import List


class DocumentProcess:
    """ This class retrieves documents from Solr. """

    def __init__(self, solr_api_url: str, start_solr_docs: int, total_solr_docs: int) -> None:
        self.solr_api_url = solr_api_url
        self.start_solr_docs =  start_solr_docs
        self.total_solr_docs = total_solr_docs
        logging.basicConfig(
            filename=config.LOG_FILE,
            level=logging.DEBUG,
            format="%(asctime)s %(levelname)s: %(message)s"
        )

    def get_documents(self) -> List[str]:
        """ Gets documents from Solr and return them. """

        params = {
            "q": "*:*",
            "wt": "json",
            "start": self.start_solr_docs,
            "rows": self.total_solr_docs,
        }

        logging.info("Getting json data from Solr...")
        response = requests.get(self.solr_api_url, params=params)
        logging.info("Loading json data from Solr...")
        data = json.loads(response.text)
        docs = data["response"]["docs"]

        return docs
    

def extract_domain(seed_url) -> str:
    """
    Gets the domain name from an url.

    :param url: the input url.
    :return: the domain or domain with subdomain name.
    """
    exctracted = tldextract.extract(seed_url)
    domain = exctracted.registered_domain
    subdomain = exctracted.subdomain
    if subdomain:
        domain = subdomain + "." + domain

    return domain
