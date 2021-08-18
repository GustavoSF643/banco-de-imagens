from werkzeug.utils import secure_filename
from flask import safe_join
import os

def create_files(files, directory: str) -> list:
    files_list = list(files)
    uploaded_list = []

    for f in files_list:
        received_file = files[f]

        filename = secure_filename(received_file.filename)
        file_path = safe_join(directory, filename)
        received_file.save(file_path)
        
        uploaded_list.append(filename)

    return uploaded_list