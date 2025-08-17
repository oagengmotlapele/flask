def generate_html_form(fields):
    html = """
  {% for i in form1 %}
"""
    for field in fields:
        # Start if statement for each field
        html += f"    {{% if i == '{field['name']}' %}}\n"
        if field['type'] in ('text', 'password', 'date', 'color','email','file'):
            icon_html = f'<i class="fas fa-{field["icon"]} input-left-icon"></i>' if field.get("icon") else ""
            html += f"""\
    <div class="{{{{ responsive }}}}">
      <div class="broken-line invalid" id="broken-{field['id']}">
        <span class="broken-line-label invalid">{field['name']}</span>
      </div>
      <div class="input-floating-container">
        <div class="input-input-group">
          {icon_html}
          <input
            name="{field['id']}" 
            type="{field['type']}"
            id="{field['id']}-input"
            class="floating-input"
            placeholder=" "
            autocomplete="off"
            required
          />
          <label for="{field['id']}-input" class="floating-label">{field['name']}</label>
          <i class="input-error-icon fas fa-times-circle" id="{field['id']}-error-icon" title="{field['name']} validation error"></i>
        </div>
        <div class="criteria-panel" id="{field['id']}-criteria-panel" aria-live="polite">
          <span class="input-title">{field['name']} Criteria</span>
"""
            # Add criteria points if any
            for crit in field.get('criteria', []):
                html += f"""\
          <div class="criteria-point">
            <div class="criteria-point-icon" id="{field['id']}-{crit['id']}-icon">
              <i class="fas fa-times invalid"></i>
            </div>
            <span>{crit['desc']}</span>
          </div>
"""
            html += """\
        </div>
      </div>
    </div>
"""
        elif field['type'] == 'radio':
            html += f"""\
    <div class="{{{{ responsive }}}}">
      <div class="broken-line" id="broken-{field['id']}">
        <span class="broken-line-label">{field['name']}</span>
      </div>
      <div class="input-floating-container">
        <div class="input-input-group" style="padding-left: 40px;">
          <div class="options-group" role="radiogroup" aria-labelledby="broken-{field['id']}">
"""
            # Add radio options
            for option in field.get('options', []):
                html += f'            <label><input type="radio" name="{field["id"]}" value="{option["value"]}" /> {option["label"]}</label>\n'

            html += f"""\
          </div>
          <i class="input-error-icon fas fa-exclamation-circle invalid" id="{field['id']}-error-icon" title="Select your {field['name'].lower()}"></i>
        </div>
        <div class="criteria-panel" id="{field['id']}-criteria-panel" aria-live="polite">
          <span class="input-title">{field['name']} Criteria</span>
          <div class="criteria-point">
            <div class="criteria-point-icon" id="{field['id']}-selected-icon">
              <i class="fas fa-times"></i>
            </div>
            <span>You must select a {field['name'].lower()}</span>
          </div>
        </div>
      </div>
    </div>
"""
        elif field['type'] == 'checkbox':
            html += f"""\
    <div class="{{{{ responsive }}}}">
      <div class="broken-line" id="broken-{field['id']}">
        <span class="broken-line-label">{field['name']}</span>
      </div>
      <div class="input-floating-container">
        <div class="input-input-group padding-left-4" >
          <div class="options-group" role="group" aria-labelledby="broken-{field['id']}">
"""
            # Add checkbox options
            for option in field.get('options', []):
                req_str = "required" if option.get("required", False) else ""
                html += f'            <label><input type="checkbox" name="{field["id"]}" value="{option["value"]}" {req_str}/> {option["label"]}</label>\n'

            html += f"""\
          </div>
          <i class="input-error-icon fas fa-times-circle" id="{field['id']}-error-icon" title="Select your {field['name'].lower()}"></i>
        </div>
        <div class="criteria-panel" id="{field['id']}-criteria-panel" aria-live="polite">
          <span class="input-title">{field['name']} Criteria</span>
          <div class="criteria-point">
            <div class="criteria-point-icon" id="{field['id']}-selected-icon">
              <i class="fas fa-times"></i>
            </div>
            <span>You must select at least one {field['name'].lower()}</span>
          </div>
        </div>
      </div>
    </div>
"""
        else:
            # default fallback
            html += f"""\
    <div class="{{{{ responsive }}}}">
      <div class="broken-line" id="broken-{field['id']}">
        <span class="broken-line-label">{field['name']}</span>
      </div>
      <div class="input-floating-container">
        <input type="{field['type']}" id="{field['id']}-input" class="floating-input" required />
      </div>
    </div>
"""
        # Close if statement
        html += f"    {{% endif %}}\n"
    html += "  {% endfor %}\n"
    return html
def generate_validation_js(fields):
    js = """// ======== AUTO-GENERATED VALIDATION SCRIPT ========

// Utility: toggle valid/invalid icon for each criteria point
function setCriteriaPointIcon(id, valid) {
    const iconContainer = document.getElementById(id + "-icon");
    if (!iconContainer) return;

    const icon = iconContainer.querySelector("i");
    if (!icon) return;

    icon.classList.remove("fa-check", "fa-times");
    iconContainer.classList.remove("valid", "invalid");

    if (valid) {
        icon.classList.add("fas", "fa-check");
        iconContainer.classList.add("valid");
    } else {
        icon.classList.add("fas", "fa-times");
        iconContainer.classList.add("invalid");
    }
}

// Utility: update broken line color
function updateBrokenLineColor(id, valid) {
    const el = document.getElementById("broken-" + id);
    if (!el) return;
    el.classList.remove("valid", "invalid");
    el.classList.add(valid ? "valid" : "invalid");
}

// Utility: update the main field error icon
function updateErrorIcon(id, valid) {
    const icon = document.getElementById(id + "-error-icon");
    if (!icon) return;
    icon.classList.remove("fa-check-circle", "fa-times-circle");
    icon.classList.remove("valid", "invalid");
    
    if (valid) {
        icon.classList.add("fas", "fa-check-circle");
        icon.classList.add("valid");
    } else {
        icon.classList.add("fas", "fa-times-circle");
        icon.classList.add("invalid");
    }
}

// Utility: show criteria panel on focus
function attachFocusHandler(id) {
    const input = document.getElementById(id + "-input");
    const panel = document.getElementById(id + "-criteria-panel");
    if (input && panel) {
        input.addEventListener("focus", () => {
            panel.style.display = "block";
        });
        input.addEventListener("blur", () => {
            panel.style.display = "none";
        });
    }
}

// Utility: test regex
function testRegex(pattern, value) {
    const re = new RegExp(pattern);
    return re.test(value);
}

// Utility: get input value
function getValue(id) {
    const el = document.getElementById(id + "-input");
    return el ? el.value : "";
}
"""

    for field in fields:
        fid = field["id"]
        ftype = field["type"]
        if ftype == "color":
            js += f'''
// === {field['name']} ===
try{{
document.addEventListener('DOMContentLoaded', function() {{
  console.log("cOLOR DOM  loaded");
  attachFocusHandler("{fid}");
  const colorInput = document.getElementById('{fid}-input');
    if (colorInput) {{
        colorInput.addEventListener('input', function() {{
        updateBrokenLineColor("{fid}", true);
        updateErrorIcon("{fid}", true);
'''
            for cid in field["criteria"]:
                print(cid)
                js += f'''
        setCriteriaPointIcon("{fid}-{cid['id']}", true);
        '''
            js+='''
        });
    }
});} catch (e) {
    console.error("Error attaching event listener:", e);
}            '''
        if ftype in ("text", "password"):
            js += f"""
// === {field['name']} ===
try{{
attachFocusHandler("{fid}");
document.getElementById("{fid}-input").addEventListener("input", function() {{
    
    const value = getValue("{fid}");
    let allValid = true;
"""
            for crit in field.get("criteria", []):
                cid = crit["id"]
                regex = crit.get("regex", "")
                if cid == "match" and fid == "confirm-password":
                    js += f"""
    let match = value === getValue("password");
    setCriteriaPointIcon("{fid}-{cid}", match);
    if (!match) allValid = false;
"""
                elif regex:
                    js += f"""
    let valid_{cid} = testRegex("{regex}", value);
    setCriteriaPointIcon("{fid}-{cid}", valid_{cid});
    if (!valid_{cid}) allValid = false;
"""
                else:
                    js += f"""
    // {cid} handled in custom logic
"""
            js += f"""
    updateBrokenLineColor("{fid}", allValid);
    updateErrorIcon("{fid}", allValid);
}});
}} catch (e) {{
    console.error("Error attaching event listener:", e);
}}
"""
        elif ftype == "radio":
            js += f"""
// === {field['name']} ===
const radios_{fid} = document.getElementsByName("{fid}");
radios_{fid}.forEach(r => r.addEventListener("change", () => {{
    let selected = Array.from(radios_{fid}).some(r => r.checked);
    setCriteriaPointIcon("{fid}-selected", selected);
    updateBrokenLineColor("{fid}", selected);
    updateErrorIcon("{fid}", selected);
}}));
"""
        elif ftype == "checkbox":
            fid = field["id"]
            js += f'''
try{{
attachFocusHandler("{fid}");
function {fid.replace('-', '_')}() {{
   let varValid = false;
   // Select all checkboxes with class '{fid}-input' AND type checkbox
   const checkboxes = document.querySelectorAll('input[name="{fid}"]');
   checkboxes.forEach(chk => {{
      chk.addEventListener('change', function() {{
      // Check if at least one checkbox is checked
      varValid = Array.from(checkboxes).some(box => box.checked);
      setCriteriaPointIcon('{fid}', varValid);
      updateBrokenLineColor('{fid}', varValid);
      updateErrorIcon('{fid}', varValid);
      console.log('varValid:', varValid, 'Any checked:', varValid);
      }});
   }});
}}
{fid.replace('-', '_')}();
}} catch (e) {{
    console.error("Error attaching event listener:", e);
}}
'''
    return js


def main():
    fields = [
        {
            "name": "Username",
            "id": "username",
            "type": "text",
            "icon": "user",
            "criteria": [
                {
                    "id": "length",
                    "desc": "3 to 15 characters",
                    "regex": "^.{3,15}$"
                },
                {
                    "id": "validchars",
                    "desc": "Only letters and numbers (a-z, A-Z, 0-9)",
                    "regex": "^[a-zA-Z0-9]+$"
                }
            ]
        },
        {
            "name": "First Name",
            "id": "first-name",
            "type": "text",
            "icon": "user",
            "criteria": [
                {
                    "id": "length",
                    "desc": "3 to 15 characters",
                    "regex": "^.{3,15}$"
                },
                {
                    "id": "validchars",
                    "desc": "Only letters and numbers (a-z, A-Z, 0-9)",
                    "regex": "^[a-zA-Z0-9]+$"
                }
            ]
        },
        {
            "name": "Password",
            "id": "password",
            "type": "password",
            "icon": "lock",
            "criteria": [
                {
                    "id": "length",
                    "desc": "At least 8 characters",
                    "regex": "^.{8,}$"
                },
                {
                    "id": "uppercase",
                    "desc": "At least 1 uppercase letter",
                    "regex": ".*[A-Z].*"
                },
                {
                    "id": "lowercase",
                    "desc": "At least 1 lowercase letter",
                    "regex": ".*[a-z].*"
                },
                {
                    "id": "special",
                    "desc": "At least 1 special character (!@#$%^&*)",
                    "regex": ".*[!@#$%^&*].*"
                },
                {
                    "id": "number",
                    "desc": "At least 1 digit",
                    "regex": ".*[0-9].*"
                }
            ]
        },
        {
            "name": "Confirm Password",
            "id": "confirm-password",
            "type": "password",
            "icon": "lock",
            "criteria": [
                {
                    "id": "match",
                    "desc": "Passwords must match",
                    "regex": ""  # Matching will be done in code logic, not regex
                }
            ]
        },
        {
            "name": "Date of Birth",
            "id": "date-of-birth",
            "type": "date",
            "icon": "calendar-alt",
            "criteria": [
                {
                    "id": "selected",
                    "desc": "Date must be selected",
                    "regex": ""
                }
            ]
        },
        {
            "name": "Gender",
            "id": "gender",
            "type": "radio",
            "options": [
                {"label": "Male", "value": "male"},
                {"label": "Female", "value": "female"},
                {"label": "Other", "value": "other"}
            ]
        },
        {
            "name": "Interest",
            "id": "interest",
            "type": "checkbox",
            "options": [
                {"label": "Sports", "value": "sports"},
                {"label": "Music", "value": "music"},
                {"label": "Movies", "value": "movies"},
                {"label": "Books", "value": "books"}
            ]
        },
        {
            "name": "Favorite Color",
            "id": "favorite-color",
            "type": "color",
            "icon": "palette",
            "criteria": [
                {
                    "id": "picked",
                    "desc": "You must pick a color",
                    "regex": ""  # Usually validated as non-empty or valid hex in code
                }
            ]
        },
        {
            "name": "Login Button",
            "id": "login-button",
            "type": "button"
        }
    ]
    html='/home/oagengmotlapele/PycharmProjects/flask/src/view/templates/include/form/2.html'
    js ='/home/oagengmotlapele/PycharmProjects/flask/src/view/static/js/65js/form/2.js'
    # Generate and save HTML form template
    html_content = generate_html_form(fields)
    with open(html, "w", encoding="utf-8") as f:
        f.write(html_content)
    print("2.html generated.")

    # Generate and save JS validation script
    js_content = generate_validation_js(fields)
    with open(js, "w", encoding="utf-8") as f:
        f.write(js_content)
    print("2.js generated.")


if __name__ == "__main__":
    main()
