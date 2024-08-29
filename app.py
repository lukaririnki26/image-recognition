# flask_app/app.py
from flask import Flask, render_template
from src.ocr import ocr

app = Flask(__name__)

app.register_blueprint(ocr, url_prefix='/ocr')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)