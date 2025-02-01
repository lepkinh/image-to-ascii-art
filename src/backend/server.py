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


@app.route('/save', methods=['POST'])
def save_ascii():
    """
    Save ASCII art as an image file.

    Returns:
    file, the image file of the ascii art
    """
    data = request.json
    ascii_art = data.get('ascii')
    format = data.get('format', 'png')  # 'png' or 'jpeg'

    if not ascii_art:
        return jsonify({"error": "No ASCII art to save"}), 400
    
    try:
        # Calculate image dimensions
        lines = ascii_art.split('\n')
        font_size = 12  # Base font size
        font = ImageFont.truetype("Courier_New.ttf", font_size)
        
        # Estimate character dimensions
        char_width, char_height = font.getsize("A")
        img_width = max(len(line) for line in lines) * char_width
        img_height = len(lines) * char_height

        # Create image
        img = Image.new('RGB', (img_width, img_height), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), ascii_art, font=font, fill=(0, 0, 0))

        # Save to bytes buffer
        img_io = io.BytesIO()
        img.save(img_io, format=format.upper(), quality=95)
        img_io.seek(0)

        return send_file(img_io, mimetype=f'image/{format}', as_attachment=True, download_name=f'ascii_art.{format}')
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)