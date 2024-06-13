def get_file_content(path):
    with open(path, 'r') as fp:
        data = fp.read()
    return data