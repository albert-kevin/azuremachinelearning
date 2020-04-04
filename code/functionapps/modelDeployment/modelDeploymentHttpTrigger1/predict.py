import logging
import os
import json
import joblib
import numpy as np
from azureml.core.model import Model

scriptpath = os.path.abspath(__file__)
scriptdir = os.path.dirname(scriptpath)
filename = os.path.join(scriptdir, "model.pkl")
labels_filename = os.path.join(scriptdir, "labels.txt")

# loading the model
model = joblib.load(filename)

def predict_from_url(raw_data):
    #raw_data = 
    # Get the input data as a numpy array
    data = np.array(raw_data)
    #data = np.array(json.loads(raw_data)['data'])
    # Get a prediction from the model
    predictions = model.predict(data)
    # Get the corresponding classname for each prediction (0 or 1)
    classnames = ['not-diabetic', 'diabetic']
    predicted_classes = []
    for prediction in predictions:
        predicted_classes.append(classnames[prediction])
    # Return the predictions as JSON
    #return json.dumps(predicted_classes)
    return predicted_classes