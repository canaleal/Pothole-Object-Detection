import os


def checkIfFolderExistsAndCreateIfNot(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def deleteFileIfItExists(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
