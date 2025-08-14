import pickle
import numpy as np

# Load the heart model once
with open('models/heart_model.pkl', 'rb') as f:
    heart_model = pickle.load(f)

def predict_heart(input_data):
    """
    input_data: list or array of 13 features
    Returns: 0 (Healthy) or 1 (Heart Disease)
    """
    data = np.array(input_data).reshape(1, -1)
    prediction = heart_model.predict(data)
    return int(prediction[0])
