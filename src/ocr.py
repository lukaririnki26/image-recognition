from flask import Blueprint, render_template, request, jsonify, current_app
import cv2
import numpy as np
import pytesseract
from PIL import Image
import re
import matplotlib.pyplot as plt

ocr = Blueprint('ocr', __name__)

def extract_capslock_text(input_text):
    capitalized_words = re.findall(r'\b[A-Z]+\b', input_text)
    result = ' '.join(capitalized_words)
    return result

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
        #Convert the uploaded file to a NumPy array
        img = np.array(Image.open(file))

        #Method 1
        # # Convert to grayscale
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # # Thresholding
        # _, threshed = cv2.threshold(gray, 127, 255, cv2.THRESH_TRUNC)
        # processed_image = cv2.GaussianBlur(threshed, (1, 1), 0)
        # # Detect text using Tesseract
        # result = pytesseract.image_to_string(threshed, config='--psm 4', lang='ind')

        #Method 2
        #Convert the image to grayscale
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Apply GaussianBlur to reduce noise and detail in the image
        blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
        # Apply Otsu's thresholding after Gaussian filtering
        _, binary_image = cv2.threshold(blurred_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # Use a larger kernel for the morphological operation to remove noise
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        processed_image = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel)

        # Display the processed image
        plt.imshow(processed_image, cmap='gray')
        plt.axis('off')
        plt.show()

        # Use Tesseract to extract text
        custom_config = r'--oem 3 --psm 6'
        result = pytesseract.image_to_string(processed_image, config=custom_config, lang='ind')




        
        # Define a dictionary to store extracted data
        ktp_data = {
            "nik": None,
            "nama": None,
            "tempat_tanggal_lahir": None,
            "jenis_kelamin": None,
            "gol_darah": None,
            "alamat": None,
            "rt_rw": None,
            "kel_desa": None,
            "kecamatan": None,
            "kabupaten_kota": None,
            "provinsi": None,
            "agama": None,
            "status_perkawinan": None,
            "pekerjaan": None,
            "kewarganegaraan": None,
            "berlaku_hingga": None
        }

        lines = result.split("\n")
        for line in lines:
            current_app.logger.info(line)
            if "N I K" in line or "NIK" in line:
                nik_line =  line.split(":")[-1].strip()
                ktp_data["nik"] = nik_line
            if "Nama" in line:
                nama_line =  line.split(":")[-1].strip()
                nama_line = extract_capslock_text(nama_line)
                ktp_data["nama"] = nama_line
            if "Alamat" in line:
                alamat_line =  line.split(":")[-1].strip()
                alamat_line = extract_capslock_text(alamat_line)
                ktp_data["alamat"] = alamat_line
            if "RT/RW" in line:
                rt_rw_line =  line.split(":")[-1].strip()
                ktp_data["rt_rw"] = rt_rw_line
            if "Kel/Desa" in line:
                kel_desa_line =  line.split(":")[-1].strip()
                kel_desa_line = extract_capslock_text(kel_desa_line)
                ktp_data["kel_desa"] = kel_desa_line
            if "Kecamatan" in line:
                kecamatan_line =  line.split(":")[-1].strip()
                kecamatan_line = extract_capslock_text(kecamatan_line)
                ktp_data["kecamatan"] = kecamatan_line
            if "KOTA" in line or "KABUPATEN" in line:
                kabupaten_kota_line =  line.split(":")[-1].strip()
                kabupaten_kota_line = extract_capslock_text(kabupaten_kota_line)
                ktp_data["kabupaten_kota"] = kabupaten_kota_line
            if "PROVINSI" in line:
                provinsi_line =  line.split(":")[-1].strip()
                provinsi_line = extract_capslock_text(provinsi_line)
                ktp_data["provinsi"] = provinsi_line
            if "Tempat/Tgl Lahir" in line or "Tempat/Tgi Lahir" in line:
                tempat_tanggal_lahir_line =  line.split(":")[-1].strip()
                tempat_tanggal_lahir_line = extract_capslock_text(tempat_tanggal_lahir_line)
                ktp_data["tempat_tanggal_lahir"] = tempat_tanggal_lahir_line
            if "Jenis Kelamin" in line:
                jenis_kelamin_line =  line.split(":")[-1].strip()
                jenis_kelamin_line = extract_capslock_text(jenis_kelamin_line)
                ktp_data["jenis_kelamin"] = jenis_kelamin_line
            if "Gol. Darah" in line:
                gol_darah_line =  line.split(":")[-1].strip()
                gol_darah_line = extract_capslock_text(gol_darah_line)
                ktp_data["gol_darah"] = gol_darah_line
            if "Agama" in line:
                agama_line =  line.split(":")[-1].strip()
                agama_line = extract_capslock_text(agama_line)
                ktp_data["agama"] = agama_line
            if "Status Perkawinan" in line:
                status_perkawinan_line =  line.split(":")[-1].strip()
                status_perkawinan_line = extract_capslock_text(status_perkawinan_line)
                ktp_data["status_perkawinan"] = status_perkawinan_line
            if "Pekerjaan" in line:
                pekerjaan_line =  line.split(":")[-1].strip()
                pekerjaan_line = extract_capslock_text(pekerjaan_line)
                ktp_data["pekerjaan"] = pekerjaan_line
            if "Kewarganegaraan" in line:
                kewarganegaraan_line =  line.split(":")[-1].strip()
                kewarganegaraan_line = extract_capslock_text(kewarganegaraan_line)
                ktp_data["kewarganegaraan"] = kewarganegaraan_line
            if "Berlaku Hingga" in line:
                berlaku_hingga_line =  line.split(":")[-1].strip()
                berlaku_hingga_line = extract_capslock_text(berlaku_hingga_line)
                ktp_data["berlaku_hingga"] = berlaku_hingga_line

        return jsonify(ktp_data)

    except Exception as e:
        error = f"Error: {str(e)}"
        return render_template('ocr.html', error=error)
