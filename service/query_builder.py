
import json


class QueryBuilder:
    # @inject(
    #     es_client=ElasticsearchConnection,
    # )
    def __init__(self, logger):
        self.logger = logger
        self.es_query = {}
        self.must_clauses = []
        self.should_clauses = []
        self.filter_clauses = []
        self.query_string = ""  # ES query string
        self.highlight_clauses = {}
        

    def build_sort(self, oas_query=None):
        '''  Builds the sort field format for elasticsearch '''
        order = oas_query.get("sort_order", "DESC")
        sort_field = oas_query.get("sort_field")

        ordered_date_sorts = [
            {
                # "start_date": {
                #     "order": oas_query.get("sort_order"),
                #     "missing": "_last"
                # },
                # "title.keyword": {
                #     "order": oas_query.get("sort_order"),
                #     "missing": "_last"
                # }
            }
        ]

        if not sort_field:
            return [{"_score": {"order": order}}] + ordered_date_sorts
        else:
            return [
                {sort_field: {"order": order, "missing": "_last"}},
                ordered_date_sorts[0]
            ]


    def transform_query_string(self, oas_query=None):
        # Base case for search, empty query string
        if not oas_query.get("query_string", ""):
            self.query_string = {"match_all": {}}
        else:
            self.query_string = {
                "query_string": {
                    # "fields": ['title^3', 'field2'],
                    "fields": ['*'],
                    "default_operator": "AND",
                    "analyzer": "standard",
                    "query": oas_query.get('query_string'),
                    "lenient" : True,
                }
            }


    def add_highlighting(self):
        self.highlight_clauses = {
            "highlight": {
                "order": "score",
                "pre_tags": [
                    "<b>"
                ],
                "post_tags": [
                    "</b>"
                ],
                "fields": {
                    "*": {
                        "number_of_fragments": 1,
                        "type": "plain",
                        "fragment_size": 150
                    }
                }
            }
        }

        self.es_query.update(self.highlight_clauses)


  
    def build_terms_filters_batch(self, _terms, max_terms_count=65000):
        '''The logic to separate terms clauses based on max_terms_count '''
        if len(_terms) < 2 and "*" in _terms:
            return []
        
        terms_filters = []
        terms_chunks = [_terms[i: i + max_terms_count] for i in range(0, len(_terms), max_terms_count)]
        print(terms_chunks)
        for _chunks in terms_chunks:
            terms_filters.append({"terms": {"_id": _chunks}})

        return terms_filters


    def build_query(self, oas_query=None):
        if not oas_query:
            return {}

        # self.logger.info('QueryBuilder:oas_query_params - {}'.format(oas_query))

        self.transform_query_string(oas_query)
        self.must_clauses = [self.query_string]
        self.filter_clauses = [{
            "bool": {
                "must": [
                    {
                        "bool": {
                            "should": self.build_terms_filters_batch(_terms=oas_query.get("ids_filters",[]), max_terms_count=5)
                        }
                    }
                ]
            }
        }]
        self.es_query = {
            # "track_total_hits": True,
            "sort": self.build_sort(oas_query),
            "query" : {
                "bool" : {
                    "must": self.must_clauses,
                    "should" : self.should_clauses,
                    "filter": self.filter_clauses
                }
            },
            "size" : oas_query.get("size", 1)
        }

        self.add_highlighting()
        
        # self.logger.info('QueryBuilder:oas_query_build - {}'.format(json.dumps(self.es_query, indent=2)))

        return self.es_query
