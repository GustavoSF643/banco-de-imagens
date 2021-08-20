import os

def files_list(directory: str) -> list:
    """function that returns a list of files in a directory

    Args:
        directory (str): path of directory for listing

    Returns:
        list: list with files of directory
    """
    files = os.listdir(directory)

    return files