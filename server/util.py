import os
import pickle
import json
import numpy as np

__locations = None
__data_columns = None
__model = None

def get_location_names():
    return __locations

def get_estimated_price(location, sqft, bhk, bath):
    try:
        loc_index = __data_columns.index(location.lower())
    except ValueError:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1

    return round(__model.predict([x])[0], 2)

def load_saved_artifacts():
    print("Loading saved artifacts....start")
    global __data_columns
    global __locations
    global __model

    # Absolute path from current working directory
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    columns_path = os.path.join(project_root, "artifacts", "columns.json")
    model_path = os.path.join(project_root, "artifacts", "banglore_home_prices_model.pickle")

    # Check if files exist
    if not os.path.exists(columns_path):
        raise FileNotFoundError(f"columns.json not found at {columns_path}")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model pickle file not found at {model_path}")

    # Load artifacts
    with open(columns_path, 'r') as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]  # location names start from index 3

    with open(model_path, 'rb') as f:
        __model = pickle.load(f)

    print("Loading saved artifacts...done")
