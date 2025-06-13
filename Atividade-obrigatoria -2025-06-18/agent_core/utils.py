import os
import zipfile
import tempfile


def save_uploaded_zip(uploaded_file):
    """
    Salva o arquivo ZIP enviado e retorna uma tupla com o diretório temporário e o caminho do ZIP.
    """
    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, "uploaded.zip")
    with open(zip_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return temp_dir, zip_path

def extract_zip(zip_path):
    """
    Extrai o arquivo ZIP (no caminho zip_path) para seu diretório temporário.
    Retorna o diretório onde os arquivos foram extraídos.
    """
    extract_dir = os.path.dirname(zip_path)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    return extract_dir

def find_data_files(dir_path):
    """
    Busca recursivamente arquivos com extensões csv ou xlsx dentro de dir_path.
    """
    data_files = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith(('.csv', '.xlsx')):
                data_files.append(os.path.join(root, file))
    return data_files