from flask import Blueprint, render_template, request, jsonify, send_file
import cv2
import numpy as np
import pytesseract
import matplotlib.pyplot as plt
from PIL import Image

ocr = Blueprint('ocr', __name__)

@ocr.route('/', methods=['GET'])
def index():
    return render_template('ocr.html')

@ocr.route('/', methods=['POST'])
def convert():
    if 'file' not in request.files:
        error = "Error: No File Part"
        return render_template('ocr.html', error=error)

    file = request.files['file']

    if file.filename == '':
        error = "Error: No Selected File"
        return render_template('ocr.html', error=error)

    try:
        # Convert the uploaded file to a NumPy array
        img = np.array(Image.open(file))

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # (2) Threshold
        th, threshed = cv2.threshold(gray, 127, 255, cv2.THRESH_TRUNC)

        # (3) Detect text using Tesseract
        result = pytesseract.image_to_string(threshed, lang="ind")

        # (5) Normalize text
        lines = []
        for word in result.split("\n"):
            # if "”—" in word:
            #     word = word.replace("”—", ":")
            if " 1 " in word:
                    word = word.replace(" 1 ", " : ")
            
            # # Normalize NIK
            # if "NIK" in word:
            #     if "D" in word:
            #         word = word.replace("D", "0")
            #     if "?" in word:
            #         word = word.replace("?", "7")
            lines.append(word)
        result = "\n".join(lines)
        return lines
        
        return render_template('ocr.html', result=result)

    except Exception as e:
        error = f"Error: {str(e)}"
        return render_template('ocr.html', error=error)
