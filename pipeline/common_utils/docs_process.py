import logging
import requests
import json
import tldextract
from common_utils import config
from typing import List


class DocumentProcess:
    """ This class retrieves documents from Solr. """

    def __init__(self, solr_api_url: str) -> None:
        self.solr_api_url = solr_api_url
        logging.basicConfig(
            filename=config.LOG_FILE,
            level=logging.DEBUG,
            format="%(asctime)s %(levelname)s: %(message)s"
        )

    def get_total_documents(self) -> int:
        """ Gets total documents from the Solr and return it. """

        params = {"q": "*:*", "rows": 0}
        response = requests.get(self.solr_api_url, params=params)
        response_json = response.json()
        total_doc = response_json["response"]["numFound"]

        return total_doc

    def get_documents(self) -> List[str]:
        """ Gets documents from Solr and return them. """

        params = {
            "q": "*:*",
            "wt": "json",
            "start": 0,
            "rows": self.get_total_documents()
        }

        logging.info("Getting json data from Solr...")
        response = requests.get(self.solr_api_url, params=params)
        logging.info("Loading json data from Solr...")
        data = json.loads(response.text)
        docs = data["response"]["docs"]

        return docs
    

def extract_domain(seed_url: str) -> str:
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
