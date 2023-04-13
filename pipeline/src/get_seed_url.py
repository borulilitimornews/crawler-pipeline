import re
import tldextract
from pathlib import Path
from typing import List
from googlesearch import search
from common_utils.utils import load_corpus


class GetSeedUrl:
    """
    The GetURL class checks each url if:
    (1) Its domain is not in the excluded domain list.
    (2) It is a new seed.
    (3) It is a new domain.
    
    After satifying the 1 and 2 conditions:
        * If the url's length is lower than 300, add it to the seed url file.
        * If the url contains a new domain, add it to the domain file.
    """

    def __init__(
        self, extension_to_exclude: List[str], domains_to_exclude: List[str]
    ) -> None:
        self.extension_to_exclude = extension_to_exclude
        self.domains_to_exclude = domains_to_exclude

    def is_allowed_seed_url(self, seed: str) -> bool:
        """
        Check if the given urls' domain is not part of the domain excluded list 
        and it still not exists on the seed url file.

        :param seed: a seed url.
        :return: True if the url is allowed, False otherwise.
        """

        is_allowed = not any(
            re.search(ext, seed.lower()) for ext in self.extension_to_exclude
        ) and not any(domain in seed for domain in self.domains_to_exclude)

        return is_allowed

    def is_new_seed_url(
        self, seed_url: str, nutch_seed_file_path: Path
    ) -> bool:
        """
        Check if it is a new url.

        :param seed_url: a seed url.
        :param nutch_seed_file_path: a path to the seed url file within the nutch folder.
        :return: True if the url is new, False otherwise.
        """

        new_seed_url = seed_url not in load_corpus(nutch_seed_file_path)

        return new_seed_url

    def extract_domain(self, url: str) -> str:
        """
        Get the domain name from an url.

        :param url: the input url.
        :return: the domain or domain with subdomain name.
        """

        exctracted = tldextract.extract(url)
        domain = exctracted.registered_domain
        subdomain = exctracted.subdomain
        if subdomain:
            domain = subdomain + "." + domain

        return domain

    def is_new_domain(self, seed_url: str, domain_file_path: Path) -> bool:
        """
        Check if the input URL contains any of the domains in the domain list.

        :param url: The URL to be checked.
        :return: True if the URL contains any of the domains, False otherwise.
        """

        domain = self.extract_domain(seed_url)
        new_domain = domain not in load_corpus(domain_file_path)

        return new_domain

    def get_seed_urls(
        self,
        query: str,
        nutch_seed_file_path: Path,
        num_results: int = 10,
        max_url_length: int = 300,
    ) -> List[str]:
        """
        Get new seeds having length < 300 and save them to the seed file.

        :param query: a search query or seed words.
        :param nutch_seed_file_path: a path to the seed url file within the nutch folder.
        :param num_result: a total of the result to be retrieved.
        :return: a list of seed urls
        """

        seeds = set()
        for url in search(query, num_results=num_results):
            if self.is_allowed_seed_url(url) and self.is_new_seed_url(
                url, nutch_seed_file_path
            ):
                seeds.add(url)
                if len(url) < max_url_length:
                    with nutch_seed_file_path.open("a", encoding="utf-8") as f:
                        f.write(url + "\n")

        return list(seeds)

    def get_domains(
        self, seed_urls: List[str], domain_file_path: Path
    ) -> None:
        """
        Get new domains from the seeds.

        :param seeds: a list of seed urls.
        :param domain_file_path: a path to the domain file.
        :return: a list of domains.
        """

        domains = set()
        for seed_url in seed_urls:
            domain = self.extract_domain(seed_url)
            if self.is_new_domain(seed_url, domain_file_path):
                domains.add(domain)
                with domain_file_path.open("a", encoding="utf-8") as f:
                    f.write(domain + "\n")

        return list(domains)

    def generate_seed_urls(
        self,
        corpus_file_path: Path,
        seed_words_file_path: Path,
        nutch_seed_file_path: Path,
        lid_model_file_path: Path,
        domain_file_path: Path,
        generate_seed_words_func: callable,
    ) -> None:
        """
        Get seed urls returned by the Google search for the input seed words.

        :param corpus_file_path: a path to the corpus file.
        :param seed_words_file_path: a path to the seed words file.
        :param nutch_seed_file_path: a path to the seed url file within the nutch folder.
        :param lid_model_file_path: a path to the LID model file.
        :param domain_file_path: a path to the domain file.
        :param generate_seed_words_func: a function to generate seed words.
        """

        # generate_seed_word_func = generate_seed_words() of the SeedWords class
        query = generate_seed_words_func(
            corpus_file_path, lid_model_file_path, seed_words_file_path
        )

        seeds = self.get_seed_urls(query, nutch_seed_file_path)
        domains = self.get_domains(seeds, domain_file_path)

        print(f"\nNew url(s):\n" + "\n".join(list(seeds)))
        print(f"\nNew domain(s):\n" + "\n".join(list(domains)))
