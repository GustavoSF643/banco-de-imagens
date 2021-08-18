import os

def create_directory(directory):
    if not os.path.exists(directory):
        return os.makedirs(directory)