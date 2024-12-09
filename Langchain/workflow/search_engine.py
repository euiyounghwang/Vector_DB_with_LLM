
from xml.dom import NotFoundErr
from elasticsearch import Elasticsearch
import json
import os
from datetime import datetime
import pandas as pd
import re
import logging
from dotenv import load_dotenv

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

''' pip install python-dotenv'''
load_dotenv(dotenv_path="../.env") # will search for .env file in local folder and load variables 



class Search():
    ''' elasticsearch class '''
    
    def __init__(self, host):
        self.timeout = 600
        self.MAX_BYTES = 10485760
        self.max_len = 0
        self.total_count = 0
        self.total_buffer = 0
        self.response_total_time = 0
        self.response_request_cnt = 0
        self.actions = []
        
        # self.es_client = Elasticsearch(hosts=host, headers=self.get_headers(), timeout=self.timeout)
        # create a new instance of the Elasticsearch client class
        # Elasticseach < 8.x basic auth example:
        # self.es_client = Elasticsearch(hosts=host, headers=self.get_headers(), http_auth=('elastic','gsaadmin'), timeout=self.timeout)
        self.es_client = Elasticsearch(hosts=host, headers=self.get_headers(), timeout=self.timeout,  verify_certs=False)
        
        # Elasticsearch >= 8.x
        # self.es_client = Elasticsearch(hosts=_host, headers=self.get_headers(), basic_auth=('elastic','gsaadmin'), timeout=self.timeout)
    
    
    def get_es_instance(self):
        return self.es_client
    
    
    def close(self):
        self.es_client.close()
        
    
    def get_headers(self):
        ''' Elasticsearch Header '''
        return {
            'Content-type': 'application/json', 
            'Authorization' : '{}'.format(os.getenv('BASIC_AUTH')),
            # 'Connection': 'close'
        }
        
    
    def Get_Buffer_list_Length(self, docs):
        """
        :param docs:
        :return:
        """
        max_len = 0
        for doc in docs:
            max_len += len(str(doc))

        # logging.info(f"max_len : {max_len}")

        return max_len
    

    def Set_buffer_Lengh(self):
        self.max_len = 0


    def Get_Buffer_Length(self, actions):
        """
        :param docs:
        :return:
        """
        
        # self.max_len += len(json.dumps(actions))
        # logging.info(f"max_len : {self.max_len}")

        self.max_len += len(''.join(map(str, actions)))

        return self.max_len
    
        
    def create_index(self, _index):
        ''' sample index & mapping '''
        print(self.es_client)
        
        mapping = {
            "mappings": {
                "properties": {
                    # "title": {
                    #     "type": "text",
                    #     "analyzer": "standard",
                    #     "fields": {
                    #         "keyword": {
                    #             "type": "keyword"
                    #         }
                    #     }
                    # }
                }
            }
        }
        
        def try_delete_create_index(index):
            try:
                if self.es_client.indices.exists(index):
                    print('Successfully deleted: {}'.format(index))
                    self.es_client.indices.delete(index)
                    # now create a new index
                    self.es_client.indices.create(index=index, body=mapping)
                    # es_client.indices.put_alias(index, "omnisearch_search")
                    self.es_client.indices.refresh(index=index)
                    print("Successfully created: {}".format(index))
            
            except NotFoundErr:
                pass
            
        ''' delete and create index into ES '''
        try_delete_create_index(index=_index)
        
    
    def post_search(self, _index):
        ''' search after indexing as validate '''
        response = self.es_client.search(
            index=_index,
            body={
                    "query" : {
                       "match_all" : {
                       }
                    }
            }
        )
        print("Total counts for search - {}".format(json.dumps(response['hits']['total']['value'], indent=2)))
        # print("response for search - {}".format(json.dumps(response['hits']['hits'][0], indent=2)))
    
    
    def transform_df_to_clean_characters(self, df):
        ''' Clean dataframe '''
        df = df.fillna('')
        return df
    
    
    def transform_json_clean_characters(self, to_replace):
        ''' Clean dataframe '''
        if isinstance(to_replace, (str)):
            to_replace = to_replace.strip()
            to_replace = re.sub(r'\n|\\n', ' ', to_replace)
            to_replace = re.sub(r'\t|\\t', ' ', to_replace)
            to_replace = re.sub(r'\f|\\f', ' ', to_replace)
            to_replace = re.sub(r'\s+', ' ', to_replace)
            to_replace = re.sub(r'string', '', to_replace)
            to_replace = re.sub(r'_id', '', 'key')
        
        return to_replace
    
    

    def buffered_json_doc_to_es(self, raw_json, _index, _type):
        ''' https://coralogix.com/guides/elasticsearch/elasticsearch-python-index-search-optimize/ '''
        """
        doc = {
            "title": "Elasticsearch Python Demo",
            "content": "A demonstration of how to use Elasticsearch with Python."
        }
        index_name = "demo_index"
        doc_type = "_doc"
        doc_id = 1
        """
        # response = self.es_client.index(index=_index, _type=_type, id=doc_id, body=doc)
        response = self.es_client.index(index=_index, _type=_type, body=raw_json)
        print(response)


    def buffered_json_to_es(self, raw_json, _index, _type):
        ''' https://opster.com/guides/elasticsearch/how-tos/optimizing-elasticsearch-bulk-indexing-high-performance/ '''
        ''' To further improve bulk indexing performance, you can use multiple threads or processes to send bulk requests concurrently. This can help you utilize the full capacity of your Elasticsearch cluster and reduce the time it takes to index large datasets.'''
        ''' When using multiple threads or processes, make sure to monitor the performance and resource usage of your Elasticsearch cluster. '''
        ''' If you notice high CPU or memory usage, you may need to reduce the number of concurrent requests or adjust your Elasticsearch configuration.'''
        '''
        raw_json : 
        # [{'_index': 'recommendation_test', '_id': 'cLOXEosBDeViDjrDAL8Z', '_score': 1.0, '_source': {'intern': 'Richard', 'grade': 'bad', 'type': 'grade'}},
        ...]
        '''
        logging.info("buffered_json_to_es Loading.. {}".format(json.dumps(raw_json, indent=2, ensure_ascii=False)))
        
        try:
            
            for each_raw in raw_json:

                if "_source" not in each_raw:
                    continue

                # _id = each_raw['_id'] if "_id" in each_raw else "222"

                ''' ES v.5 header'''
                # _header = {'index': {'_index': _index, '_type' : _type, "_id" : each_raw['_id'], "op_type" : "create"}}
                _header = {'index': {'_index': _index, '_type' : _type, '_id' : each_raw['_id']}}
                
                ''' When indexing with ES v.8, _type is deleted and must be excluded. '''
                ''' So, when indexing with ES v.8, spark job also needs to remove the _type field.'''
                # _header = {'index': {'_index': _index, "_id" : each_raw['_id']}}
                # _header = {'index': {'_index': _index, "_id" : each_raw['_id'], "op_type" : "create"}}
                # self.actions.append({'index': {'_index': _index, "_id" : each_raw['_id'], "op_type" : "create"}})
                
                self.actions.append(_header)
                _body = each_raw['_source']
                self.actions.append(_body)
                '''
                actions += [
                    # {'index': {'_index': _index, '_type' : _type, "_id" : each_raw['_id'], "op_type" : "create"}},
                    {'index': {'_index': _index, "_id" : each_raw['_id'], "op_type" : "create"}},
                    each_raw['_source']
                ]
                '''

                self.total_count += 1
                # self.total_buffer += len(json.dumps(_header)) + len(json.dumps(_body))
                # self.total_buffer += len(str(_header)) + len(str(_body))

                # logging.info(f"size of buffer : {list(map(len,actions))}")
                
                # if self.Get_Buffer_Length(self.actions) > self.MAX_BYTES:
                # if self.total_buffer > self.MAX_BYTES:
                if self.total_count % 1000 == 0:
                    Bulk_StartTime = datetime.now()
                    
                    response = self.es_client.bulk(body=self.actions)
                    if str(response['errors']).lower() == 'true':
                        # logging.error(response)
                        pass
                    else:
                        logging.info("** indexing ** : {}".format(len(response['items'])))

                    Bulk_EndTime = datetime.now()
                    ''' accumulate response_total_time'''
                    self.response_total_time += float(str((Bulk_EndTime - Bulk_StartTime).seconds) + '.' + str((Bulk_EndTime - Bulk_StartTime).microseconds).zfill(6)[:2])
                    self.response_request_cnt += 1
                    logging.info(f"response_total_time :{self.response_total_time}, response_request_cnt = {self.response_request_cnt}")
                    
                    ''' initialize variables'''
                    ''' ----------------------'''
                    # self.Set_buffer_Lengh()
                    del self.actions[:]
                    self.total_count = 0
                    self.total_buffer = 0
                    ''' ----------------------'''
                
            # --
            # Index for the remain Dataset
            # --
            if len(self.actions) > 0:
                response = self.es_client.bulk(body=self.actions)
                
                if response['errors'] == 'true':
                    logging.error(response)
                else:
                    logging.info("** remain indexing ** : {}".format(len(response['items'])))
                    del self.actions[:]
            
            # --
            # refresh
            # self.es_client.indices.refresh(index=_index)
            
          
        except Exception as e:
            print('buffered_json_to_es exception : {}'.format(str(e)))
            pass
                

    def buffered_df_to_es(self, df, _index):
        ''' df : Dataframe format, _index: Elasticsearch index name that you want to save '''
        print("buffered_df_to_es Loading..")
        ''' Nan to black for each field value '''
        
        try:
            df = self.transform_df_to_clean_characters(df)
            actions = []
        
            # creating a list of dataframe columns 
            columns = list(df) 
            # print(columns)
            for row in list(df.values.tolist()):
                rows_dict = {}
                for i, colmun_name in enumerate(columns):
                    rows_dict.update({self.transform_json_clean_characters(colmun_name) : self.transform_json_clean_characters(row[i])})
                
                # print(rows_dict)
                actions.append({'index': {'_index': _index}})
                actions.append(rows_dict)
                # print(json.dumps(actions, indent=2))
                
                if self.Get_Buffer_Length(actions) > self.MAX_BYTES:
                    response = self.es_client.bulk(body=actions)
                    print("** indexing Error - True/False ** : {}".format(json.dumps(response['errors'], indent=2)))
                    del actions[:]
            
            # --
            # Index for the remain Dataset
            # --
            response = self.es_client.bulk(body=actions)
            # print(response)
            print("** Remain indexing Error - True/False ** : {}".format(json.dumps(response['errors'], indent=2)))
            
            # --
            # refresh
            self.es_client.indices.refresh(index=_index)
        
        except Exception as e:
            print('buffered_df_to_es exception : {}'.format(str(e)))