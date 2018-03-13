import os


def list_all_files(root, filenames):
    if os.path.isdir(root):
        for d in os.listdir(root):
            list_all_files(os.path.join(root, d), filenames)
    else:
        filenames.append(root)
