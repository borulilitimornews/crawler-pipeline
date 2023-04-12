import re
import tldextract
from pathlib import Path
from typing import List, Optional
from googlesearch import search
from utils import load_corpus


class GetSeedUrl:
    """
    The GetURL class is composed of the following tasks:
    1. Check if the domain of the generated seed is not in the excluded domain list.
    2. Check if it is a new seed.
    3. Check if it is a new domain.
    4. After satifying the 1 and 2 criterias:
        * if the seed's length is lower than 300, add to the seed file.
        * if the seed contains a new domain, add it to the domain file.
    """

    def __init__(self, extension_to_exclude, domains_to_exclude) -> None:
        self.extension_to_exclude = extension_to_exclude
        self.domains_to_exclude = domains_to_exclude

    def is_allowed_seed_url(self, seed: str) -> bool:
        """
        Check if the link domain is not part of the domain excluded list and
        it is still not exist on the seed file.

        :param seed: a seed url.
        :param excluded_domains: a list of domain names to exclude.
        :return: True if the link is allowed, False otherwise.
        """
        is_allowed = not any(
            re.search(ext, seed.lower()) for ext in self.extension_to_exclude
        ) and not any(
            domain in seed for domain in self.domains_to_exclude
        )

        return is_allowed

    def is_new_seed_url(self, seed: str, nutch_seed_file_path: Path) -> bool:
        """
        Check if it is a new seed.

        :param seed: a seed url.
        :param nutch_seed_file_path: a path to the seed url file within the nutch folder.
        :return: True if the link is new, False otherwise.
        """
        new_seed_url = seed not in load_corpus(nutch_seed_file_path)

        return new_seed_url

    def extract_domain(self, url: str) -> str:
        """
        Get the domain name from an url.

        :param url: an url
        :return: the domain name.
        """
        exctracted = tldextract.extract(url)
        domain = exctracted.registered_domain
        subdomain = exctracted.subdomain
        if subdomain:
            domain = subdomain + '.' + domain

        return domain

    def is_new_domain(self, seed: str, domain_file_path: Path) -> bool:
        """
        Check if the given URL contains any of the domains in the domain list.

        :param url: The URL to be checked.
        :return: True if the URL contains any of the domains, False otherwise.
        """
        domain = self.extract_domain(seed)
        new_domain = domain not in load_corpus(domain_file_path)

        return new_domain

    def get_seed_urls(self, query: str, nutch_seed_file_path, num_results: int = 10) -> List[str]:
        """
        Get new seeds and save to the seed file.

        :param query: a search query or seed words.
        :param nutch_seed_file_path: a path to the seed url file within the nutch folder.
        :param num_result: a total of the result to be retrieved.
        :return: a list of seeds or urls
        """

        seeds = set()
        for url in search(query, num_results=num_results):
            if self.is_allowed_seed_url(url) and self.is_new_seed_url(url, nutch_seed_file_path):
                seeds.add(url)
                # add seed url to the seed file
                if len(url) < 300:
                    with nutch_seed_file_path.open('a', encoding='utf-8') as f:
                        f.write(url + '\n')

        return list(seeds)

    def get_domains(self, seeds: List[str], domain_file_path: Path) -> None:
        """
        Get new domains from the seeds.

        :param domain_file_path: a path to the domain file.
        :param seeds: a list of seeds or urls.
        :return: a list of domains.
        """

        domains = set()
        for seed in seeds:
            domain = self.extract_domain(seed)
            if self.is_new_domain(seed, domain_file_path):
                domains.add(domain)
                with domain_file_path.open('a', encoding='utf-8') as f:
                    f.write(domain + '\n')

        return list(domains)

    def generate_seed_urls(
        self, corpus_file_path: Path, seed_words_file_path: Path,
        nutch_seed_file_path: Path, lid_model_file_path: Path,
        domain_file_path: Path, gen_seed_words_func: callable
    ) -> None:
        """
        Get seed urls returned by the Google search for the input seed words.

        :param corpus_file_path: a path to the corpus file.
        :param seed_words_file_path: a path to the seed words file.
        :param seed_file_path: a path to the seed file.
        :param domain_file_path: a path to the domain file.
        :param nutch_seed_file_path: a path to the seed url file within the nutch folder.
        :param seed_words: a function to generate seed words.

        :returns: a list of seed urls and domains.
        """

        # gen_seed_word_func = generate_seed_words() of the SeedWords class
        query = gen_seed_words_func(
            corpus_file_path, lid_model_file_path, seed_words_file_path)

        seeds = self.get_seed_urls(query, nutch_seed_file_path)
        domains = self.get_domains(seeds, domain_file_path)

        print(f"\nNew url(s):\n" + '\n'.join(list(seeds)))
        print(f"\nNew domain(s):\n" + '\n'.join(list(domains)))
