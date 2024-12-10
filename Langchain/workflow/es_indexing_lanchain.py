
import json
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")
import os
from text_loader import loader_text
from search_engine import Search
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from injector import doc, ES_HOST, es_version


path = os.getcwd() + "/Data"


if __name__ == "__main__":
    
    try:
        bulk_json = {}

        ''' Loading json-format if create_json is True'''
        '''
        Loading extracted text via langchain_community.document_loaders and apache tika
        loader_text("test.txt", create_json=True)
        loader_text("asiabrief_3-26.pdf", create_json=True)
        loader_text("Sample.docx", create_json=True)
        loader_text("Sample.doc", create_json=True)
        loader_text("Sample.pptx", create_json=True)
        loader_text("test", create_json=True)
        loader_text("Sample.xls", create_json=True)
        '''
        
        # raw_json_list = loader_text("{}/{}".format(path, "Sample.hwp"), create_json=True)
        # raw_json_list = loader_text("{}/{}".format(path, "Sample.pptx"), create_json=True)
        raw_json_list = loader_text("{}/{}".format(path, "Sample.docx"), create_json=True)

        ''' Loading json-format if create_json is False'''
        # loader_text("{}/{}".format(path, "Sample.hwp"))

        es_obj = Search(host=ES_HOST)
        # es_client = es_obj.get_es_instance()

        if '5.' in es_version['version']['number']:
            es_obj.buffered_json_to_es(raw_json_list, "test_ngram_v1", "props")
        elif '8.' in es_version['version']['number']:
            es_obj.buffered_json_to_es(raw_json_list, "test_ngram_v1")

    except Exception as e:
        print(e)