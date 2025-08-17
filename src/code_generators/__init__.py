import re

def extract_fas_icons(css_path):
    with open(css_path, 'r', encoding='utf-8') as f:
        css_content = f.read()

    # This regex finds all class selectors like `.fa-home`, `.fas.fa-home`, etc.
    matches = re.findall(r'\.fa-([a-z0-9-]+)', css_content)

    # Remove duplicates and sort
    unique_icons = sorted(set(matches))
    return [f"fa-{icon}" for icon in unique_icons]

# 👇 Path to your all.min.css file
css_file_path = "/home/oagengmotlapele/PycharmProjects/flask/src/view/static/css/fontawesome/css/all.min.css"

# 🔥 Get icons
icons = extract_fas_icons(css_file_path)

# 💥 Print or use as needed
for icon in icons:
    print(icon)

# Optional: return as JSON or array in app
