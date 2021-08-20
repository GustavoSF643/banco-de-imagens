import os
from flask import safe_join
import zipfile
from datetime import datetime

def create_zip_file(directory: str, directory_list: str,file_type: str=None, compression_rate: int=9) -> dict:
    """ function for create a zip folder from a folder with files

    Args:
        directory (str): directory for create a zip folder
        directory_list (str): directory for zip files
        file_type (str, optional): type of files for zip. Defaults to None.
        compression_rate (int, optional): compression rate for zip files. Defaults to 9.

    Returns:
        dict: dict with 'filename' and 'filepath' of zip folder
    """

    files = os.listdir(directory_list)

    zip_folder_name = f"zip_files_{str(datetime.now()).replace(' ', '_')}"
    zip_folder_path = safe_join(directory, zip_folder_name)
    zip_folder = zipfile.ZipFile(zip_folder_path, 'x')

    for file in files:
        if file_type == None:
            file_path = safe_join(directory_list, file)
            zip_folder.write(filename=file_path,arcname=file,compress_type=zipfile.ZIP_DEFLATED, compresslevel=compression_rate)
        else:
            if file.endswith(file_type):
                file_path = safe_join(directory_list, file)
                zip_folder.write(filename=file_path,arcname=file,compress_type=zipfile.ZIP_DEFLATED, compresslevel=compression_rate)
        
    zip_folder.close()

    return {'filename': zip_folder_name, 'filepath': zip_folder_path}