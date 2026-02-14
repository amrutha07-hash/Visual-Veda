from PIL import Image
import pytesseract

# If your tesseract executable is in a non-standard location (Windows), set the path here:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_path):
    # Open the image file
    image = Image.open(image_path)
    # Use pytesseract OCR to extract text with Sanskrit language model
    text = pytesseract.image_to_string(image, lang='san')
    return text

if __name__ == "__main__":
    # Path to your Sanskrit slokam image inside the images folder
    image_path = "images/s-1.jpg"
    extracted_text = extract_text_from_image(image_path)
    print("Extracted Sanskrit Text:")
    print(extracted_text)
