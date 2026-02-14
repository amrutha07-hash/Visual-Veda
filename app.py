from flask import Flask, request, jsonify, send_file
from ocr import extract_text_from_image
from nlp import summarize_text, translate_text
from image_gen import create_story_card
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/process_image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    image = request.files['image']
    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(image_path)

    # Step 1: OCR
    extracted_text = extract_text_from_image(image_path)

    # Step 2: Summarize & Translate
    summary = summarize_text(extracted_text)
    translation = translate_text(summary)

    # Step 3: Create Story Card
    output_file = os.path.join(OUTPUT_FOLDER, f"story_card_{image.filename}.png")
    create_story_card(translation, output_file)

    return send_file(output_file, mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True)
