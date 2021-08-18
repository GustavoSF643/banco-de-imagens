import os

def files_list(directory) -> list:
    files = os.listdir(directory)

    return files