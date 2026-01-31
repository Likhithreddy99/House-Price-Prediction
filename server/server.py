from flask import Flask, request, jsonify, send_from_directory
import util
import os

# Create Flask app, serving static files from client folder
app = Flask(__name__, static_folder='client')

# Serve the main frontend page
@app.route("/")
def serve_frontend():
    return send_from_directory(app.static_folder, 'app.html')

# Serve any other static files in the client folder
@app.route("/<path:path>")
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)

# API endpoint to get location names
@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# API endpoint to predict home price
@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    try:
        total_sqft = float(request.form['total_sqft'])
        location = request.form['location']
        bhk = int(request.form['bhk'])
        bath = int(request.form['bath'])
    except (KeyError, ValueError):
        return jsonify({'error': 'Invalid input parameters'}), 400

    estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)
    
    response = jsonify({
        'estimated_price': estimated_price
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Run the server
if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    util.load_saved_artifacts()  # Make sure util.py handles paths correctly
    app.run(debug=True)  # debug=True helps during development
