import re
import tldextract
from pathlib import Path
from typing import List
from googlesearch import search
from common_utils.utils import load_corpus


class GetSeedUrl:
    """
    The GetURL class checks each url if:
    (1) Its domain is not on the excluded domain list.
    (2) It is a new seed.
    (3) It is a new domain.
    
    After satifying the 1 and 2 conditions:
        * If the url's length is lower than 300, add it to the seed url file.
        * If the url contains a new domain, add it to the domain file.
    """

    def __init__(
        self,
        extension_to_exclude: List[str],
        domains_to_exclude: List[str],
        generate_seed_words: callable,
        google_search_num_result: int,
        max_seed_url_length: int,
        nutch_seed_url_file_path: Path,
        domain_file_path: Path,
    ) -> None:
        self.extension_to_exclude = extension_to_exclude
        self.domains_to_exclude = domains_to_exclude
        self.generate_seed_words = generate_seed_words
        self.google_search_num_result = google_search_num_result
        self.max_seed_url_length = max_seed_url_length
        self.nutch_seed_url_file_path = nutch_seed_url_file_path
        self.domain_file_path = domain_file_path

    def is_allowed_seed_url(self, seed: str) -> bool:
        """
        Checks if the given urls' domain is not part of the domain excluded list 
        and it still not exists on the seed url file.

        :param seed: a seed url.
        :return: True if the url is allowed, False otherwise.
        """

        is_allowed = not any(
            re.search(ext, seed.lower()) for ext in self.extension_to_exclude
        ) and not any(domain in seed for domain in self.domains_to_exclude)

        return is_allowed

    def is_new_seed_url(self, seed_url: str) -> bool:
        """
        Checks if it is a new url.

        :param seed_url: a seed url.
        :return: True if the url is new, False otherwise.
        """

        new_seed_url = seed_url not in load_corpus(self.nutch_seed_url_file_path)

        return new_seed_url

    def extract_domain(self, url: str) -> str:
        """
        Gets the domain name from an url.

        :param url: the input url.
        :return: the domain or domain with subdomain name.
        """

        exctracted = tldextract.extract(url)
        domain = exctracted.registered_domain
        subdomain = exctracted.subdomain
        if subdomain:
            domain = subdomain + "." + domain

        return domain

    def is_new_domain(self, seed_url: str) -> bool:
        """
        Checks if the input URL's domain contains any of the domains in the domain list.

        :param url: The URL to be checked.
        :return: True if the URL's domain contains any of the domains, False otherwise.
        """

        domain = self.extract_domain(seed_url)
        new_domain = domain not in load_corpus(self.domain_file_path)

        return new_domain

    def get_seed_urls(self) -> List[str]:
        """
        Gets new seeds having length < 300 and save them to the seed file 
        and return a list of seed URLs.
        """

        seeds = set()
        for url in search(self.generate_seed_words, num_results=self.google_search_num_result):
            if self.is_allowed_seed_url(url) and self.is_new_seed_url(url):
                seeds.add(url)
                if len(url) < self.max_seed_url_length:
                    with self.nutch_seed_url_file_path.open("a", encoding="utf-8") as seed_url_file:
                        seed_url_file.write(url + "\n")

        return list(seeds)

    def get_domains(self, seed_urls: List[str]) -> None:
        """
        Gets new domains from the seed URLs.

        :param seeds: a list of the seed URLs.
        :return: a list of domains.
        """

        domains = set()
        for seed_url in seed_urls:
            domain = self.extract_domain(seed_url)
            if self.is_new_domain(seed_url):
                domains.add(domain)
                with self.domain_file_path.open("a", encoding="utf-8") as domain_file:
                    domain_file.write(domain + "\n")

        return list(domains)

    def generate_seed_urls(self) -> None:
        """ Gets seed urls returned by the Google search and their respective domains. """

        seeds = self.get_seed_urls()
        domains = self.get_domains(seeds)

        print(f"\nNew url(s):\n" + "\n".join(list(seeds)))
        print(f"\nNew domain(s):\n" + "\n".join(list(domains)))
