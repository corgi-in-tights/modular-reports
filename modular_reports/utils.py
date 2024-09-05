from pathlib import Path

def get_file_content(path):
    with open(path, 'r') as fp:
        data = fp.read()
    return data

def get_component_template_path(subpath: str):
    return Path(__file__).parent / 'templates' / subpath.strip('/')