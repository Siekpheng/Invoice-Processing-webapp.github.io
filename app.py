from flask import Flask, request, send_file
import os
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    if file:
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Run main.py
        subprocess.run(['python', 'main.py', filepath], check=True)

        # Run final_combined.py
        subprocess.run(['python', 'final_combined.py'], check=True)

        # Send the processed file
        processed_file_path = os.path.join(app.config['PROCESSED_FOLDER'], 'output_combined.xlsx')
        return send_file(processed_file_path, as_attachment=True)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)
    app.run(host='0.0.0.0', port=5000)
