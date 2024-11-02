from flask import Flask, request, render_template, redirect, url_for, send_file, after_this_request
import os
import subprocess
import shutil
from werkzeug.utils import secure_filename
import time
import threading

app = Flask(__name__)
app.secret_key = "your_secret_key"
UPLOAD_FOLDER = "./uploads"
RESULT_FOLDER = "./runs"
MODEL_PATH = "bigT7.pt"  # Path to your YOLO model file

# Ensure upload and result folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file:
            print('No file selected')
            return redirect(request.url)
        
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        print('File uploaded successfully')
        return redirect(url_for('home'))
    
    return render_template('upload.html')

@app.route('/run_model')
def run_model():
    # Run YOLO model on the uploaded file
    input_file = os.path.join(UPLOAD_FOLDER, os.listdir(UPLOAD_FOLDER)[0])  # Assuming only one file
    if not os.path.exists(input_file):
        print('No uploaded file found')
        return redirect(url_for('home'))
    
    # Run the YOLO model
    try:
        subprocess.run(
            ["yolo", "task=detect", "mode=predict", f"model={MODEL_PATH}", f"source={input_file}"],
            check=True
        )

        print('Model run successfully')
        
        # Clear the uploads folder after running the model
        shutil.rmtree(UPLOAD_FOLDER)
        os.makedirs(UPLOAD_FOLDER)
    except subprocess.CalledProcessError as e:
        print(f"Error running model: {e}")
    
    return redirect(url_for('home'))

@app.route('/download')
def download():
    result_zip = "result.zip"
    # Zip the results folder for downloading
    subprocess.run(["zip", "-r", result_zip, RESULT_FOLDER], check=True)

    @after_this_request
    def remove_file(response):
        def delayed_delete(zip_path, result_folder):
            time.sleep(1)  # Wait briefly to ensure the file is sent
            try:
                os.remove(zip_path)  # Remove the zip file
                print(f"{zip_path} deleted.")
                
                # Clear out and remove RESULT_FOLDER
                shutil.rmtree(result_folder)
                print(f"{result_folder} cleared.")
                
                # Recreate the empty RESULT_FOLDER for next use
                os.makedirs(result_folder)
                print(f"{result_folder} recreated.")
            except Exception as e:
                print(f"Error during cleanup: {e}")

        # Start the cleanup in a new thread
        threading.Thread(target=delayed_delete, args=(result_zip, RESULT_FOLDER)).start()
        return response
    
    return send_file(result_zip, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
