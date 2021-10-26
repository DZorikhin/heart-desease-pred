# Load the model

import pickle
import numpy as np

from flask import Flask
from flask import request
from flask import jsonify

model_file = 'model_C=0.1.bin'

with open(model_file, 'rb') as f_in:
    model = pickle.load(f_in)

app = Flask('heart-disease')

@app.route('/predict', methods=['POST'])
def predict():
    parameters = request.get_json()
    
    X = np.fromiter(parameters.values(), dtype=float).reshape(1, -1)
    y_pred = model.predict_proba(X)[0, 1]
    risk = y_pred >= 0.5
    
    result = {
        'disease_probability': round(float(y_pred), 2),
        'risk': bool(risk)
    }

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696)