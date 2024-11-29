from fastapi import APIRouter, File, UploadFile # type: ignore
import json
import datetime
from injector import (logger,
                      SearchAPIHandlerInject,
                      SearchOmniHandlerInject
                      )
from service.status_handler import (StatusHanlder, StatusException)
from typing import Optional
import os
from Langchain.workflow.text_loader import loader_text


app = APIRouter(
    prefix="/vector",
)

current_path = os.path.dirname(os.path.abspath(__file__))

@app.post("/uploadfile",
          status_code=StatusHanlder.HTTP_STATUS_200,
          responses={
            200: {"description" : "OK"},
            404 :{"description" : "URl not found"}
          },
          description="Sample Payload : http://localhost:7000/vector/uploadfile", 
          summary="uploadfile",
          )
async def create_upload_file(file: UploadFile):
    '''  poetry add python-multipart '''
    logger.info(f"path : {current_path}")
    contents = await file.read()
    with open(os.getcwd() + "/Data/" + file.filename, "wb") as f:
        f.write(contents)
    # return {"filename": file.filename}
    logger.info(f"file name : {file.filename}")

    extracted_text = loader_text(file.filename)

    return {"filename": extracted_text} 
