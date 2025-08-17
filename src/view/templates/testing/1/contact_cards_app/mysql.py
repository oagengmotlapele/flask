import mysql.connector

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
