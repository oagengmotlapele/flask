import json
from pathlib import Path
import os
class Files:
    def __init__(self):
        pass
    def get_all_files(self, directory):
        directory=directory+'/img'
        """Returns a dictionary with filenames (without extension) as keys and full paths as values."""
        files_dict = {}

        for file in Path(directory).rglob("*"):  # Recursively list all files
            if file.is_file():  # Ensure it's a file, not a directory
                file_name = file.stem  # Get filename without extension
                files_dict[file_name] = str(file.resolve())  # Store the full path
        return files_dict

    def get_css_links(self,dir_path:str):
        css_dir = dir_path+'/css'
        """Generates a list of paths to all CSS files in the static/css directory."""
        css_files = []
        for root, dirs, files in os.walk(css_dir):
            for file in files:
                if file.endswith(".css"):
                    # Construct the relative path for the file within the static folder
                    file_path = os.path.join(root, file).replace('\\', '/')
                    #file_path = file_path.replace('static/', '')  # Remove 'static/' from the path
                    f=file_path.split('static/')

                    css_files.append(f[1])
        return css_files

    def get_js_links(self, dir_path: str):
        """Generates a list of relative paths to all JS files inside static/js/"""
        js_files = []
        js_dir = os.path.join(dir_path, 'js')

        for root, _, files in os.walk(js_dir):
            for file in files:
                if file.endswith(".js"):
                    full_path = os.path.join(root, file).replace("\\", "/")
                    rel_path = full_path.split('static/', 1)[-1]
                    js_files.append(rel_path)
        return js_files

    def get_form_creator(self,package:str,filename:str,endpoint:str):
        with open(f"../controller/form_data/{package}/{filename}/{endpoint}.json", 'r') as file:
            data = json.load(file)
        return data