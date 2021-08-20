from werkzeug.datastructures import FileStorage, ImmutableDict
from werkzeug.utils import secure_filename
from flask import safe_join

def create_files(files: ImmutableDict[str, FileStorage], directory: str) -> list:
    """function for create files in a directory

    Args:
        files (ImmutableDict[str, FileStorage]): ImmutableDict received from request.files of Flask
        directory (str): path of directory for create a file(s)

    Returns:
        list: list of names from created files
    """

    files_list = list(files)
    uploaded_list = []

    for f in files_list:
        received_file = files[f]

        filename = secure_filename(received_file.filename)
        file_path = safe_join(directory, filename)
        received_file.save(file_path)
        
        uploaded_list.append(filename)

    return uploaded_list