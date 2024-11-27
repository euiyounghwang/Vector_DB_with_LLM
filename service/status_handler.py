
from fastapi.responses import JSONResponse
from fastapi import status, HTTPException

class StatusHanlder(object):
    HTTP_STATUS_200 = 200
    HTTP_STATUS_202 = 202
    HTTP_STATUS_404 = 404
    HTTP_STATUS_500 = 500
    
    def __init__(self):
        pass
   
   
class StatusException(object):
    
    @staticmethod
    def raise_exception(e):
        return JSONResponse(
            status_code=StatusHanlder.HTTP_STATUS_404,
            content={"message": str(e)}
        )
        # return {
        #     "status_code" : StatusHanlder.HTTP_STATUS_404,
        #     "message" : str(e)
        # }
        # return HTTPException(status_code=404, detail={"message" : str(e)})
