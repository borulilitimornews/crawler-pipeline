import os
import requests
from common_utils.docs_process import DocumentProcess, extract_domain
from common_utils.tetun_lid import TetunLid
from pathlib import Path
from bs4 import BeautifulSoup
import numpy as np
import warnings

warnings.filterwarnings("ignore")

class CollectionStatistic:
    """ 
    This class generates the collection's statistics consist of:
    (1) Total links per domain.
    (2) Total documents per extension.
    (3) Total inlinks and outlinks per document. 
    """
    def __init__(
        self, solr_api_url: str, 
        start_solr_docs: int, 
        total_solr_docs: int,
        tetun_lang: str,
        lang_proba_threshold: float,
        lid_model_file_path: Path
    ) -> None: 
        self.document_process = DocumentProcess(solr_api_url, start_solr_docs, total_solr_docs)
        self.tetun_lid = TetunLid(tetun_lang, lang_proba_threshold, lid_model_file_path)

    def generate_stats(self):
        """ Extract domains and extensions frequency from the urls, including inlinks and outlinks. """

        get_titles = [d.get("title") for d in self.document_process.get_documents() if d.get("title") is not None]
        valid_titles = self.tetun_lid.get_tetun_text(get_titles) # Apply Tetun LID
        valid_titles_unique = list(set(valid_titles))

        domain_counts = {}
        extension_counts = {}
        outlink_count_list = []
        inlink_count_list = []
        for doc in self.document_process.get_documents():
            title = doc.get("title")
            url = doc.get("url")

            if title in valid_titles_unique:
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
                #print(f"Url: {url}, Outlink: {outlink_count}, Inlink: {inlink_count}")

        print(f"Max outlinks: {max(outlink_count_list)}, Min outlinks: {min(outlink_count_list)}, Average oulinks: {np.mean(outlink_count_list)}")
        print(f"Max inlinks: {max(inlink_count_list)}, Min inlinks: {min(inlink_count_list)}, Average inlinks: {np.mean(inlink_count_list)}")

        sorted_domain_items = sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)
        for domain, count in sorted_domain_items[:5]:
            print(f"Domain: {domain}, total_docs: {count}")
        
        sorted_extension_items = sorted(extension_counts.items(), key=lambda x: x[1], reverse=True)
        for extension, count in sorted_extension_items[:5]:
            print(f"Extension: {extension}, total_docs: {count}")