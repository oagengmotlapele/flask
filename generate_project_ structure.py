import os


def create_project_structure():
    """
    Generates a standard project structure in the current working directory
    and prints a visual tree, skipping 'venv' folder.
    """
    project_path = os.getcwd()

    # Folder structure
    folders = [
        "src",
        "templates",
        "static/css",
        "static/js",
        "static/images",
        "docs",
        "tests"
    ]

    # Starter files with content
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
        os.makedirs(os.path.join(project_path, folder), exist_ok=True)

    # Create files
    for file_path, content in files.items():
        with open(os.path.join(project_path, file_path), "w") as f:
            f.write(content)

    print("✅ Project structure created successfully!\n")

    # Function to print tree, skipping 'venv'
    def print_tree(start_path, prefix=""):
        contents = sorted(os.listdir(start_path))
        contents = [c for c in contents if c != "venv"]  # Skip venv
        for i, item in enumerate(contents):
            path = os.path.join(start_path, item)
            connector = "└── " if i == len(contents) - 1 else "├── "
            print(prefix + connector + item)
            if os.path.isdir(path):
                extension = "    " if i == len(contents) - 1 else "│   "
                print_tree(path, prefix + extension)

    # Print tree
    print(f"{os.path.basename(project_path)}/")
    print_tree(project_path, "")

# Example usage:
create_project_structure()
