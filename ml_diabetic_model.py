import pickle
import numpy as np

# Load model and scaler once at module load
with open('models/svm_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('models/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

def predict_diabetes(input_data):
    """
    input_data: list or numpy array of 8 features
    Returns prediction: 0 (not diabetic) or 1 (diabetic)
    """
    
    data = np.array(input_data).reshape(1, -1)
    scaled_data = scaler.transform(data)
    prediction = model.predict(scaled_data)
    return prediction[0]

