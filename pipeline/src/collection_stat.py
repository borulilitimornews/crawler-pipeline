import os
import requests
import logging
from common_utils.docs_process import DocumentProcess, extract_domain
from common_utils.tetun_lid import TetunLid
from common_utils.utils import Utils
from common_utils import config
from pathlib import Path
from bs4 import BeautifulSoup
import numpy as np
import warnings

warnings.filterwarnings("ignore")

class CollectionStatistic:
    """ 
    This class generates the collection's statistics that consist of:
    (1) Total inlinks and outlinks per document (url).
    (2) Total documents.  
    (3) Total documents per domain.
    (4) Total documents per extension.
    """
    
    def __init__(
        self, solr_api_url: str, 
        start_solr_docs: int, 
        total_solr_docs: int,
        tetun_lang: str,
        lang_proba_threshold: float,
        lid_model_file_path: Path,
        url_in_out_links_file_path: Path,
        stats_in_out_links_file_path: Path
    ) -> None: 
        self.document_process = DocumentProcess(solr_api_url, start_solr_docs, total_solr_docs)
        self.tetun_lid = TetunLid(tetun_lang, lang_proba_threshold, lid_model_file_path)
        self.url_in_out_links = Utils(url_in_out_links_file_path)
        self.stats_in_out_links_file_path = Utils(stats_in_out_links_file_path)
        logging.basicConfig(
            filename=config.LOG_FILE,
            level=logging.DEBUG,
            format="%(asctime)s %(levelname)s: %(message)s"
        )

    def generate_stats(self) -> None:
        """ Extract domains and extensions frequency from the urls, including inlinks and outlinks. """

        logging.info("Generating statistics for the collection...")
        logging.info("Generating titles...")
        get_titles = [d.get("title") for d in self.document_process.get_documents() if d.get("title") is not None]
        logging.info("Validating titles...")
        temp_titles = self.tetun_lid.get_tetun_text(get_titles) # Apply Tetun LID
        valid_titles_unique = list(set(temp_titles))

        domain_counts = {}
        extension_counts = {}
        outlink_count_list = []
        inlink_count_list = []
        total_documents = 0
        for doc in self.document_process.get_documents():
            title = doc.get("title")
            url = doc.get("url")

            if title in valid_titles_unique and '/feed' not in url and '/tag' not in url: # Urls contain '/feed' and '/tag' are excluded.
                if "wikipedia" in url and not "tet.wikipedia.org" in url: # Ensure that only Tetun wikipedia data is executed.
                    continue
                if "wikidata" in url: # The wikipedia for Tetun does not exist.
                    continue
                       
                total_documents += 1 
                # Domains
                domain = extract_domain(url)
                if domain in domain_counts:
                    domain_counts[domain] += 1
                else:
                    domain_counts[domain] = 1

                # Extensions
                filename = os.path.basename(url) # Extract the last part of the URL
                extension = os.path.splitext(filename)[1].lower() if '.' in filename else ''
                # Uniformize the MS. Office extensions
                if extension == 'doc':
                    extension = 'docx'
                if extension == 'ppt':
                    extension == 'pptx'
                if extension == 'xls':
                    extension == 'xlsx'

                if extension in extension_counts:
                    extension_counts[extension] += 1
                else:
                    extension_counts[extension] = 1

                # Outlinks and Inlinks for each URL
                response = requests.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    links = soup.find_all('a')
                    
                    outlink_count = 0
                    inlink_count = 0
                    for link in links:
                        href = link.get('href')
                        if href and (href.startswith('http://') or href.startswith('https://')):
                            if domain not in href:
                                outlink_count += 1
                            else:
                                inlink_count += 1
                        elif href and not href.startswith('#'):
                            inlink_count += 1

                    outlink_count_list.append(outlink_count)
                    inlink_count_list.append(inlink_count)
                    self.url_in_out_links.save_corpus(f"Url: {url}, Outlink: {outlink_count}, Inlink: {inlink_count}")
                else:
                    continue

        # Save the inlinks and outlinks summary        
        stat_inlinks_outlinks = f""" The statistics of the collection:
        ========================================
        Total web pages (urls) processed: {total_documents}\n
        Max outlinks: {max(outlink_count_list)}, Min outlinks: {min(outlink_count_list)}, Average oulinks: {np.mean(outlink_count_list):.2f}
        Max inlinks: {max(inlink_count_list)}, Min inlinks: {min(inlink_count_list)}, Average inlinks: {np.mean(inlink_count_list):.2f}
        ========================================
        """
        self.stats_in_out_links_file_path.save_corpus(stat_inlinks_outlinks.strip())

        self.stats_in_out_links_file_path.save_corpus(f"\n========= Domain: total documents in the corresponding domain =========")
        sorted_domain_items = sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)
        for domain, count in sorted_domain_items:
            self.stats_in_out_links_file_path.save_corpus(f"Domain: {domain}, total_docs: {count}")
        
        self.stats_in_out_links_file_path.save_corpus(f"\n========= Extension: total documents with the corresponding extension =========")
        sorted_extension_items = sorted(extension_counts.items(), key=lambda x: x[1], reverse=True)
        for extension, count in sorted_extension_items:
            self.stats_in_out_links_file_path.save_corpus(f"Extension: {extension}, total_docs: {count}")
        
        logging.info("The statistics have been generated sucessfully.")