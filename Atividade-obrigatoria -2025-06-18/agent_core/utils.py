import os
import zipfile
import tempfile

def extract_zip(uploaded_file):
    temp_dir = tempfile.mkdtemp()
    with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    return temp_dir

def find_data_files(dir_path):
    return [f for f in os.listdir(dir_path) if f.endswith(('.csv', '.xlsx'))] 