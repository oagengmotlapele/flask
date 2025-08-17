import os

def create_project_structure(project_path):
    """
    Generates a standard project structure at the given path.
    """
    # Define folder structure
    folders = [
        "src",
        "templates",
        "static/css",
        "static/js",
        "static/images",
        "docs",
        "tests"
    ]

    # Define starter files with some content
    files = {
        "README.md": "# Project Title\n\nAuthor: Oageng Motlapele",
        "src/__init__.py": "",
        "src/main.py": "# Main Python file\n\nif __name__ == '__main__':\n    print('Hello, World!')",
        "templates/index.html": "<!DOCTYPE html>\n<html>\n<head>\n<title>Home</title>\n</head>\n<body>\n<h1>Welcome</h1>\n</body>\n</html>",
        "static/css/style.css": "/* Add your CSS here */",
        "tests/test_main.py": "import unittest\n\nclass TestMain(unittest.TestCase):\n    pass"
    }

    # Create folders
    for folder in folders:
        path = os.path.join(project_path, folder)
        os.makedirs(path, exist_ok=True)
        print(f"Created folder: {path}")

    # Create files
    for file_path, content in files.items():
        path = os.path.join(project_path, file_path)
        with open(path, "w") as f:
            f.write(content)
        print(f"Created file: {path}")

    print("\n✅ Project structure created successfully!")

# Example usage:
# create_project_structure("/home/oagengmtlapele/Projects/MyNewProject")
