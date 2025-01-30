"""
Server file, runs using Flask
"""

from flask import Flask, request, jsonify, send_from_directory
from processing import process_image, ascii
import os

app = Flask(__name__, static_folder="../frontend")

@app.route('/')
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)


@app.route('/upload', methods=['POST'])
def upload_image():
    """ 
    jsonify ascii art of the uploaded image file.

    Returns:
    json, ascii art of the uploaded image file
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']

    # arbitrarily chosen file size constraint at 15MB, can change during testing
    if file.content_length > 15 * 1024 * 1024:
        return jsonify({"error": "File too large"}), 400

    size = request.form.get("size", 2, type=int)
    data = process_image(file, size)

    if data is None:
        return jsonify({"error": "Invalid file or processing failed"}), 400

    ascii_art = ascii(data)
    return jsonify({"ascii": ascii_art})


if __name__ == '__main__':
    app.run(debug=True)