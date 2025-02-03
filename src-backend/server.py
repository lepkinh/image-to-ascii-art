"""
Server file, runs using Flask
"""
from flask import Flask, request, jsonify, send_from_directory, send_file
import sys
import os
from PIL import Image, ImageDraw, ImageFont
import io
import traceback
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))
from processing import process_image, ascii

app = Flask(__name__, static_folder=".")

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
    save ascii art as an image file.

    Returns:
    image/png, ascii art as an image file
    """
    data = request.json
    ascii_art = data.get('ascii', '')
    
    if not ascii_art.strip():
        return jsonify({"error": "No ASCII art to save"}), 400
    
    try:
        # font setup
        font_size = 12
        try:
            font = ImageFont.truetype("DejaVuSansMono.ttf", font_size)
        except IOError:
            try:
                font = ImageFont.truetype("cour.ttf", font_size)  # windows
            except IOError:
                return jsonify({"error": "Monospace font not found"}), 500

        # trimmed lines and dimensions
        lines = [line.rstrip() for line in ascii_art.split('\n')]
        if not lines:
            return jsonify({"error": "Empty ASCII art"}), 400
        
        max_line_length = max(len(line) for line in lines)
        
        left, top, right, bottom = font.getbbox("A")
        char_width = right - left
        ascent, descent = font.getmetrics()
        line_height = ascent + descent

        img_width = max_line_length * char_width
        img_height = len(lines) * line_height

        # draw
        img = Image.new('RGB', (img_width, img_height), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        y = 0
        for line in lines:
            draw.text((0, y), line, font=font, fill=(0, 0, 0))
            y += line_height

        img_io = io.BytesIO()
        img.save(img_io, format="PNG")
        img_io.seek(0)

        return send_file(img_io, mimetype="image/png", as_attachment=True, download_name="ascii_art.png")

    except Exception as e:
        print(f"CRITICAL ERROR: {traceback.format_exc()}")
        return jsonify({"error": f"Image generation failed: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)