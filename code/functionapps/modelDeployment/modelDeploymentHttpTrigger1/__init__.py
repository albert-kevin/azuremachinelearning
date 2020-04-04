import logging
import azure.functions as func
import json
from .predict import predict_from_url

import logging
import os
import json
import joblib
import numpy as np
from azureml.core.model import Model

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    data = req.params.get('data')
    if not data:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            data = req_body.get('data')

    if data:
        result = predict_from_url(data)


        headers = {
            "Content/type": "application/json",
            "Access-Control-Allow-Origin": "*"
        }
        return func.HttpResponse(json.dumps({"result": result}), mimetype="application/json", charset='utf-8')
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
