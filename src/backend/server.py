"""
Server file, flask or django
"""

from flask import Flask, request, jsonify
from processing import process_image, ascii

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_image():
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


# run server
if __name__ == '__main__':
    app.run(debug=True)