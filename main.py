import json
import logging
import uuid
import os

from typing import Dict, List, Any

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, utils

class ChemblElasticsearch:
    """
    Wrapper over an Elasticsearch instance.
    """
    HOST = os.getenv('ES_CH_URL', 'localhost')
    PORT = os.getenv('ES_CH_PORT', '9200')
    es = None

    def __init__(self):
        self.es = Elasticsearch([{'host': self.HOST, 'port': self.PORT}])

    def get_all_indices(self) -> List[str]:
        """
        :return: list of strings of index names starting with chembl
        """
        logging.debug("Querying Elasticsearch for list of indices")
        indices = self.es.indices.get_alias("*")
        filtered_indices = {key: value for key, value in indices.items() if key.startswith('chembl')}
        logging.debug(f"{len(filtered_indices)} indices found.")
        return list(filtered_indices.keys())

    def read_indexes_and_write(self, index_names: List[str]):
        """
        Converts index_dict into a json file named index_name with a simplified representation
        of the index as a json object.
        If a file '[index_name]_structure.json' already exists it will be overwritten
        :param index_names: name of indexes (will become file name).
        :return: void
        """
        index_query = ",".join(index_names)
        index = self.es.indices.get_mapping(index_query)
        logging.debug(f"{len(index)} indice mappings found.")
        master = {}

        for i in index:
            try:
                logging.debug(f"\tProcessing mappings for {i}")
                index_fields = index[i]['mappings']['properties']
                filename = f"{i}_structure.json"

                logging.debug(f"\t\tWriting mappings for {i} to {filename}")
                fields = get_fields(index_fields)
                master[i] = fields
                write_json(filename, fields)
            except(KeyError):
                logging.error(f"Key error encountered on {i}")
        logging.debug(f"Writing consolidated json record")
        write_json("indices_combined.json", master)


def get_fields(index_dict: Dict) -> Dict:
    """
    :param index_dict: Elasticsearch index mapping
    :return: simplified dictionary of structure with keys are field names and values as types
    """
    ret_dict = {}
    for key, value in index_dict.items():
        if "properties" in value:
            ret_dict[key] = get_fields(value["properties"])
        elif "type" in value:
            ret_dict[key] = value["type"]
        else:
            print(f"unrecognised key: {key}")
    return ret_dict


def write_json(filename: str, content: Dict):
    """
    :param filename: name of output file
    :param content: json contents of file
    :return: void
    """
    with open(filename, 'w') as outfile:
        json.dump(content, outfile)


if __name__ == '__main__':
 
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
 
    chembl_es = ChemblElasticsearch()

    # Get chembl index names
    index_names = chembl_es.get_all_indices()
    chembl_es.read_indexes_and_write(index_names)
