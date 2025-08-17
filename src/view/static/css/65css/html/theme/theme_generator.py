import os
from matplotlib.colors import CSS4_COLORS

# Static color tokens for all themes
theme_tokens = {
    "light": "#ffffff",
    "dark": "#000000",
    "error": "#ff0000",
    "pass": "#00cc66",
}

# Properties mapped to tokens
base_color_mapping = {
    "background-color": "default",
    "text-color": "dark",
    "border-color": "light",
    "border-top-color": "light",
    "border-bottom-color": "light",
    "border-left-color": "light",
    "border-right-color": "light",
    "outline-color": "default"
}

# HTML elements to theme
elements = [
    "body", "nav", "header", "main", "section", "footer",
    "p", "span", "a", "button", "aside", "article", "figure",
    "label", "form", "fieldset", "legend", "textarea", "input", "select",
    "glass-div", "sub-menu", "sub-menu1", "sub-menu2", "sub-menu3"
]

# Elements that should not have borders
no_border_elements = ["body", "nav", "header", "main", "section", "footer"]

# Elements that should not have background
text_only_elements = ["p", "span", "a", "label", "legend"]

# Output folder
output_folder = "themes"
os.makedirs(output_folder, exist_ok=True)

# Generate 1 CSS file per color
for color_name, hex_code in CSS4_COLORS.items():
    theme_name = color_name.lower()
    theme_colors = theme_tokens.copy()
    theme_colors["default"] = hex_code

    # Element-specific variable definitions
    element_styles = {}
    for el in elements:
        element_styles[el] = {}
        if el == "glass-div":
            continue  # Skip generating variables for glass-div
        for prop, token in base_color_mapping.items():
            if el in no_border_elements and prop.startswith("border-"):
                continue
            if el in text_only_elements and prop == "background-color":
                continue
            element_styles[el][prop] = f"var(--color-{token})"

    # Start building the CSS
    css = f".{theme_name}-theme {{\n"

    # Theme tokens
    for token, val in theme_colors.items():
        css += f"  --color-{token}: {val};\n"
    css += "\n"

    # Element-level variables
    for el, props in element_styles.items():
        for prop, val in props.items():
            var_name = f"  --{el}-{prop}: {val};\n"
            if  'form' in el and 'background-color' in prop:
                var_name = f"  --{el}-{prop}: var(--color-light);\n"
            if  'input' in el and 'background-color' in prop:
                var_name = f"  --{el}-{prop}: var(--color-light);\n"
            if  'input' in el and 'border-color' in prop:
                var_name = f"  --{el}-border: var(--color-dark);\n"
            print(var_name)
            css += var_name
    css += "}\n\n"

    # Actual rules per element
    for el in elements:
        selector = f".{theme_name}-theme {el}" if el != "glass-div" and not el.startswith("sub-") else f".{theme_name}-theme .{el}"
        css += f"{selector} {{\n"
        if el == "glass-div":
            css += "  color: var(--text-color);\n"
            css += "  font-weight: bold;\n"
            css += "  backdrop-filter: blur(12px);\n"
            css += "  -webkit-backdrop-filter: blur(12px);\n"
            css += "  background-color: rgba(255, 255, 255, 0.3);\n"
            css += "  border: 1px solid rgba(255, 255, 255, 0.3);\n"
            css += "  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);\n"
        else:
            for prop in element_styles[el]:
                var_name = f"--{el}-{prop}"
                css += f"  {prop}: var({var_name});\n"
            if el == "button":
                css += f"  outline: 2px solid var(--{el}-outline-color);\n"
            css += "  border-radius: 5px;\n"
        css += "}\n\n"

    # Save to file
    filepath = os.path.join(output_folder, f"{theme_name}.css")
    with open(filepath, "w") as f:
        f.write(css)

    print(f"✅ Generated: {filepath}")
