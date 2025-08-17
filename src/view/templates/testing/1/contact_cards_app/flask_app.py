from flask import Flask, render_template, request, redirect, url_for
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
