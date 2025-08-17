import json
import matplotlib

themes = list(matplotlib.colors.CSS4_COLORS.keys())

data = {
    "icon": "fa fa-sign-in",
    "txt": "About us",
    "href": "#",
    "depth": 1,
    "sub": [
        {
            "icon": "fa fa-sign-in",
            "txt": i,
            "href": f"/themes/{i}",
            "depth": 0
        } for i in themes
    ]
}

# Convert to JSON string with indentation for readability
json_str = json.dumps(data, indent=2)

print(json_str)
