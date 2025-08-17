import os

project_name = "contact_cards_app"

files_content = {
    "flask_app.py": '''from flask import Flask, render_template, request, redirect, url_for
from mysql import get_all_contacts, add_contact

app = Flask(__name__)

@app.route('/')
def index():
    contacts = get_all_contacts()
    return render_template('index.html', contacts=contacts)

@app.route('/add_contact', methods=['POST'])
def add_contact_route():
    contact_type = request.form.get('contactType')
    contact_value = request.form.get('contactUrl') or request.form.get('contactValue')
    if not contact_type or not contact_value:
        return "Missing required fields", 400
    add_contact(contact_type, contact_value)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
''',

    "mysql.py": '''import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'youruser',
    'password': 'yourpassword',
    'database': 'yourdatabase'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

def get_all_contacts():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM contacts ORDER BY id DESC")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def add_contact(contact_type, contact_value):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO contacts (contact_type, contact_value) VALUES (%s, %s)",
        (contact_type, contact_value)
    )
    conn.commit()
    cursor.close()
    conn.close()
''',

    "requirements.txt": '''flask
mysql-connector-python
''',

    os.path.join("templates", "index.html"): '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Contact Cards Manager</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}" />
  <script>
    // Pass contacts from Flask to JS
    const initialContacts = {{ contacts | tojson }};
  </script>
</head>
<body>

<div id="contactCards" class="contact-grid"></div>

<button id="addContactBtn" class="btn-primary">Add Contact</button>

<div id="modalOverlay" class="modal-overlay" style="display:none;">
  <div class="modal">
    <div class="modal-header">
      <h2 id="modalTitle">Add Contact</h2>
      <button id="closeModalBtn" class="close-btn" aria-label="Close">&times;</button>
    </div>
    <form id="contactForm" method="POST" action="/add_contact">
      <label for="contactType">Contact Type</label>
      <select id="contactType" name="contactType" required>
        <option value="" disabled selected>Select contact type</option>
        <option value="phone">Phone</option>
        <option value="whatsapp">WhatsApp</option>
        <option value="email">Email</option>
        <option value="facebook">Facebook</option>
        <option value="twitter">Twitter</option>
        <option value="instagram">Instagram</option>
        <option value="linkedin">LinkedIn</option>
        <option value="website">Website</option>
        <option value="location">Location</option>
        <option value="postal">Postal Address</option>
      </select>

      <label for="contactValue" id="contactValueLabel">Value</label>
      <input type="text" id="contactValue" name="contactValue" required />

      <label for="contactUrl" id="contactUrlLabel" style="display:none;">URL</label>
      <input type="url" id="contactUrl" name="contactUrl" style="display:none;" />

      <div class="modal-buttons">
        <button type="submit" class="btn-primary">Save</button>
        <button id="cancelBtn" type="button" class="btn-secondary">Cancel</button>
      </div>
    </form>
  </div>
</div>

<script src="{{ url_for('static', filename='js/script.js') }}"></script>
</body>
</html>
''',

    os.path.join("static", "css", "style.css"): '''/* Grid container for cards */
.contact-grid {
  display: grid;
  gap: 20px;
  padding: 20px;
  grid-template-columns: 1fr;
}

@media(min-width: 992px) {
  .contact-grid {
    grid-template-columns: 1fr 1fr;
  }
}

/* Card style */
.contact-card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgb(0 0 0 / 0.1);
  padding: 15px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  display: flex;
  align-items: center;
  gap: 15px;
}

.contact-card:hover {
  background-color: #f0f7ff;
  text-decoration: none;
}

/* Icon container */
.contact-icon {
  font-size: 28px;
  flex-shrink: 0;
}

/* Text container */
.contact-text {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-weight: 600;
  color: #333;
}

/* Button styles */
.btn-primary {
  background-color: #0073e6;
  border: none;
  color: white;
  padding: 10px 18px;
  font-size: 16px;
  border-radius: 6px;
  cursor: pointer;
  margin: 20px;
}

.btn-secondary {
  background-color: #ccc;
  border: none;
  color: #333;
  padding: 10px 18px;
  font-size: 16px;
  border-radius: 6px;
  cursor: pointer;
}

/* Modal styles */
.modal-overlay {
  position: fixed;
  top: 0; left: 0;
  width: 100vw; height: 100vh;
  background: rgba(0,0,0,0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 400px;
  padding: 20px;
  box-shadow: 0 8px 16px rgba(0,0,0,0.2);
  position: relative;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.close-btn {
  background: transparent;
  border: none;
  font-size: 28px;
  cursor: pointer;
  color: #555;
}

.modal label {
  display: block;
  margin-top: 15px;
  font-weight: 600;
}

.modal input, .modal select {
  width: 100%;
  padding: 10px;
  margin-top: 6px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
}

.modal-buttons {
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
}
''',

    os.path.join("static", "js", "script.js"): '''// Icon colors & classes for each contact type
const contactTypeIcons = {
  phone: { icon: "fas fa-phone", color: "#28a745", labelPrefix: "Call us at " },
  whatsapp: { icon: "fab fa-whatsapp", color: "#25D366", labelPrefix: "WhatsApp us at " },
  email: { icon: "fas fa-envelope", color: "#ea4335", labelPrefix: "Email us at " },
  facebook: { icon: "fab fa-facebook-f", color: "#1877F2", labelPrefix: "Facebook: " },
  twitter: { icon: "fab fa-twitter", color: "#1DA1F2", labelPrefix: "Twitter: " },
  instagram: { icon: "fab fa-instagram", color: "#C13584", labelPrefix: "Instagram: " },
  linkedin: { icon: "fab fa-linkedin-in", color: "#0A66C2", labelPrefix: "LinkedIn: " },
  website: { icon: "fas fa-globe", color: "#0073e6", labelPrefix: "Visit our website: " },
  location: { icon: "fas fa-map-marker-alt", color: "#d93025", labelPrefix: "Find us at: " },
  postal: { icon: "fas fa-envelope-open", color: "#6c757d", labelPrefix: "Postal address: " }
};

const contactCardsDiv = document.getElementById('contactCards');
const addContactBtn = document.getElementById('addContactBtn');
const modalOverlay = document.getElementById('modalOverlay');
const closeModalBtn = document.getElementById('closeModalBtn');
const cancelBtn = document.getElementById('cancelBtn');
const contactForm = document.getElementById('contactForm');
const contactTypeSelect = document.getElementById('contactType');
const contactValueInput = document.getElementById('contactValue');
const contactUrlInput = document.getElementById('contactUrl');
const contactUrlLabel = document.getElementById('contactUrlLabel');
const contactValueLabel = document.getElementById('contactValueLabel');

// Render cards from initialContacts (from Flask)
function renderCards(contacts) {
  contactCardsDiv.innerHTML = '';

  contacts.forEach(contact => {
    const typeInfo = contactTypeIcons[contact.contact_type] || {
      icon: "fas fa-info-circle",
      color: "#888",
      labelPrefix: ""
    };

    // For clickable types with URLs, show clickable link else text + copy number on click
    const isClickableLink = ['facebook','twitter','instagram','linkedin','website'].includes(contact.contact_type);
    const isPhoneLike = ['phone','whatsapp','email'].includes(contact.contact_type);

    const card = document.createElement('div');
    card.className = 'contact-card';

    const icon = document.createElement('i');
    icon.className = typeInfo.icon + ' contact-icon';
    icon.style.color = typeInfo.color;

    const text = document.createElement('span');
    text.className = 'contact-text';

    // Compose the label text
    const labelText = typeInfo.labelPrefix + contact.contact_value;

    if (isClickableLink) {
      const link = document.createElement('a');
      link.href = contact.contact_value;
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      link.style.color = "inherit";
      link.style.textDecoration = "none";
      link.textContent = labelText;

      // Hover effect on link
      link.addEventListener('mouseenter', () => {
        link.style.color = '#0073e6';
      });
      link.addEventListener('mouseleave', () => {
        link.style.color = 'inherit';
      });

      text.appendChild(link);
    } else if (isPhoneLike) {
      text.textContent = labelText;
      card.addEventListener('click', () => {
        copyToClipboard(contact.contact_value);
        showToast('Copied to clipboard: ' + contact.contact_value);
      });
    } else {
      // fallback text
      text.textContent = labelText;
    }

    card.appendChild(icon);
    card.appendChild(text);
    contactCardsDiv.appendChild(card);
  });
}

// Copy text to clipboard
function copyToClipboard(text) {
  navigator.clipboard.writeText(text).catch(() => {
    // fallback for older browsers
    const textarea = document.createElement('textarea');
    textarea.value = text;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    textarea.remove();
  });
}

// Toast popup for copy notification
function showToast(message) {
  const toast = document.createElement('div');
  toast.textContent = message;
  toast.style.position = 'fixed';
  toast.style.bottom = '20px';
  toast.style.left = '50%';
  toast.style.transform = 'translateX(-50%)';
  toast.style.backgroundColor = '#333';
  toast.style.color = '#fff';
  toast.style.padding = '10px 20px';
  toast.style.borderRadius = '5px';
  toast.style.opacity = '1';
  toast.style.transition = 'opacity 0.5s ease-out';
  toast.style.zIndex = '10000';

  document.body.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    setTimeout(() => toast.remove(), 500);
  }, 1500);
}

// Show/hide modal
addContactBtn.addEventListener('click', () => {
  modalOverlay.style.display = 'flex';
  contactForm.reset();
  contactUrlInput.style.display = 'none';
  contactUrlLabel.style.display = 'none';
  contactValueInput.required = true;
  contactUrlInput.required = false;
});

closeModalBtn.addEventListener('click', () => {
  modalOverlay.style.display = 'none';
});

cancelBtn.addEventListener('click', () => {
  modalOverlay.style.display = 'none';
});

// Adjust form inputs based on contact type
contactTypeSelect.addEventListener('change', () => {
  const val = contactTypeSelect.value;
  const needsUrl = ['facebook','twitter','instagram','linkedin','website'].includes(val);
  const needsValue = !needsUrl;

  if (needsUrl) {
    contactUrlInput.style.display = 'block';
    contactUrlLabel.style.display = 'block';
    contactUrlInput.required = true;

    contactValueInput.style.display = 'none';
    contactValueLabel.style.display = 'none';
    contactValueInput.required = false;
  } else {
    contactUrlInput.style.display = 'none';
    contactUrlLabel.style.display = 'none';
    contactUrlInput.required = false;

    contactValueInput.style.display = 'block';
    contactValueLabel.style.display = 'block';
    contactValueInput.required = true;
  }
});

// On page load render cards
document.addEventListener('DOMContentLoaded', () => {
  renderCards(initialContacts);
});
'''
}

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    print(f"Creating project folder '{project_name}' with all files...")
    for relative_path, content in files_content.items():
        file_path = os.path.join(project_name, relative_path)
        create_file(file_path, content)
        print(f"Created: {file_path}")
    print("Done! Your project files are ready.")

if __name__ == "__main__":
    main()
