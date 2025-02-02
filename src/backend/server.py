"""
Server file, runs using Flask
"""
from flask import Flask, request, jsonify, send_from_directory, send_file
from processing import process_image, ascii
from PIL import Image, ImageDraw, ImageFont
import io
import os
import traceback

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
    ascii_art = data.get('ascii', '')
    
    if not ascii_art.strip():
        return jsonify({"error": "No ASCII art to save"}), 400
    
    try:
        font_size = 12
        try:
            font = ImageFont.truetype("DejaVuSansMono.ttf", font_size)
        except IOError:
            try:
                font = ImageFont.truetype("cour.ttf", font_size)
            except IOError:
                font = ImageFont.load_default()

        lines = [line for line in ascii_art.split('\n') if line.strip()]
        if not lines:
            return jsonify({"error": "Empty ASCII art"}), 400
            
        max_line_length = max(len(line) for line in lines)
        
        # Get character dimensions using getbbox
        test_char = "A"
        left, top, right, bottom = font.getbbox(test_char)
        char_width = right - left
        char_height = bottom - top
        
        img_width = max_line_length * char_width
        img_height = len(lines) * char_height

        if img_width <= 0 or img_height <= 0:
            return jsonify({"error": "Invalid ASCII dimensions"}), 400

        img = Image.new('RGB', (img_width, img_height), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), ascii_art, font=font, fill=(0, 0, 0))
        
        img_io = io.BytesIO()
        img.save(img_io, format="PNG")
        img_io.seek(0)

        return send_file(img_io, mimetype="image/png", as_attachment=True, download_name="ascii_art.png")

    except Exception as e:
        print(f"CRITICAL ERROR: {traceback.format_exc()}")
        return jsonify({"error": f"Image generation failed: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)