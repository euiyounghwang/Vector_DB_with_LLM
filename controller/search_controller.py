from fastapi import APIRouter # type: ignore
import json
import datetime
from injector import (logger,
                      SearchAPIHandlerInject,
                      SearchOmniHandlerInject,
                      QueryBuilderInject
                      )
from service.status_handler import (StatusHanlder, StatusException)
from repository.schema import Search
from typing import Optional
import datetime


app = APIRouter(
    prefix="/es",
)


@app.post("/search", 
          status_code=StatusHanlder.HTTP_STATUS_200,
          responses={
            200: {"description" : "OK"},
            404 :{"description" : "URl not found"}
          },
          description="Return Search results", 
          summary="Return Search results")
async def build_search_api(request: Search):
    ''' Search to Elasticsearch '''
    try:
        # logger.info("api_controller doc: {}".format(json.dumps(doc, indent=2)))
        # request_json = {k : v for k, v in request}
        request_json = request.to_json()
        # print(request, type(request), request.size, request_json, request_json['query_string'])
        logger.info("build_search_api : {}".format(json.dumps(request_json, indent=2)))
    
        return await SearchOmniHandlerInject.search(QueryBuilderInject, oas_query=request_json)
       
    except Exception as e:
        logger.error(e)
