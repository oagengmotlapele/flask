import sqlite3
from datetime import datetime


def get_column_type(value):
    """Helper function to determine the SQL column type from the Python value type."""
    if isinstance(value, int):
        return "INTEGER"
    elif isinstance(value, float):
        return "REAL"
    elif isinstance(value, bool):
        return "BOOLEAN"
    elif isinstance(value, str):
        return "TEXT"
    else:
        return "TEXT"  # Default to TEXT for unknown types


def manage_table(conn, table_name, row_data=None, query=None, where=None, user=None, select_columns=None):
    cursor = conn.cursor()

    # Default columns (These will be present in every table)
    default_columns = {
        "is_deleted": "BOOLEAN DEFAULT 0",  # Renamed from 'delete' to 'is_deleted'
        "active": "BOOLEAN DEFAULT 1",
        "Code": "INTEGER",
        "CodeActive": "BOOLEAN DEFAULT 0",
        "CodeExpiryTimeAndDate": "TEXT",
        "DataAccessByUserType": "TEXT",
        "DataAccessByUsername": "TEXT",
        "DataAccessByGroups": "TEXT",
        "DataInsertionDate": "TEXT",
        "DataInsertionTime": "TEXT",
        "DataLastUpdate": "TEXT",
        "DataLastUpdateTime": "TEXT",
        "DataDeletionDate": "TEXT",
        "DataDeletionTime": "TEXT",
        "UserWhoAdded": "TEXT",
        "UserWhoLastUpdated": "TEXT",
        "UserWhoLastDeleted": "TEXT"
    }

    # Ensure table exists
    cursor.execute(f"PRAGMA table_info({table_name})")
    existing_columns = {row[1] for row in cursor.fetchall()}

    # Get columns from row_data
    if row_data:
        all_columns = {**row_data, **default_columns}
    else:
        all_columns = default_columns

    # Get the correct data types for each column
    columns_with_types = {col: get_column_type(value) for col, value in all_columns.items()}

    # Determine new columns to add (columns in row_data but not in existing_columns)
    new_columns = {col: dtype for col, dtype in columns_with_types.items() if col not in existing_columns}

    if not existing_columns:
        # Create table if it doesn't exist
        columns_def = ", ".join([f"{col} {dtype}" for col, dtype in columns_with_types.items()])
        create_query = f"CREATE TABLE {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, {columns_def})"
        cursor.execute(create_query)
    elif new_columns:
        # Add new columns dynamically
        for col, dtype in new_columns.items():
            alter_query = f"ALTER TABLE {table_name} ADD COLUMN {col} {dtype}"
            cursor.execute(alter_query)

    # Handle insert, update, delete, and select operations
    now_date = datetime.now().strftime("%Y-%m-%d")
    now_time = datetime.now().strftime("%H:%M")

    if query == "insert" and row_data:
        insert = True
        # Check if row already exists based on 'username' (or any unique field)
        if where:
            where_clause = " AND ".join([f"{key} = ?" for key in where.keys()])
            select_query = f"SELECT * FROM {table_name} WHERE {where_clause} LIMIT 1"
            cursor.execute(select_query, tuple(where.values()))
            existing_row = cursor.fetchall()

            print(existing_row)

            if existing_row:
                print(f"🔹 Row with {where} already exists. No insertion performed.")
                insert = False

        # Proceed with insertion if no existing row was found
        row_data.update({
            "DataInsertionDate": now_date,
            "DataInsertionTime": now_time,
            "UserWhoAdded": user
        })
        columns = ", ".join(row_data.keys())
        values = ", ".join(["?" for _ in row_data])
        if insert:
            insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
            cursor.execute(insert_query, tuple(row_data.values()))

    elif query == "update" and row_data and where:
        row_data.update({
            "DataLastUpdate": now_date,
            "DataLastUpdateTime": now_time,
            "UserWhoLastUpdated": user
        })
        update_data = ", ".join([f"{key} = ?" for key in row_data.keys()])
        where_clause = " AND ".join([f"{key} = ?" for key in where.keys()])
        update_query = f"UPDATE {table_name} SET {update_data} WHERE {where_clause}"
        cursor.execute(update_query, tuple(row_data.values()) + tuple(where.values()))

    elif query == "delete" and where:
        delete_query = f"""
        UPDATE {table_name} 
        SET is_deleted = 1, DataDeletionDate = ?, DataDeletionTime = ?, UserWhoLastDeleted = ? 
        WHERE {' AND '.join([f'{key} = ?' for key in where.keys()])}
        """
        cursor.execute(delete_query, (now_date, now_time, user) + tuple(where.values()))

    elif query == "select":
        # If user provides select_columns, use them, otherwise select all
        if select_columns:
            select_columns_str = ", ".join(select_columns)
        else:
            select_columns_str = "*"

        if where:
            where_clause = " AND ".join([f"{key} = ?" for key in where.keys()])
            select_query = f"SELECT {select_columns_str} FROM {table_name} WHERE {where_clause}"
            cursor.execute(select_query, tuple(where.values()))
        else:
            select_query = f"SELECT {select_columns_str} FROM {table_name}"
            cursor.execute(select_query)

        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]

        # Convert rows into a list of dictionaries with column names as keys
        result = [dict(zip(columns, row)) for row in rows]
        return result

    conn.commit()


# Test cases
def test_manage_table():
    conn = sqlite3.connect("test.db")

    print("\n🔹 Inserting data...")
    row_data_insert = {
        "username": "john_doe",
        "email": "john@testing.com",
        "age": 25,  # Integer
        "role": "admin"  # String
    }
    manage_table(conn, "users", row_data=row_data_insert, query="insert", user="admin")

    print("\n🔹 Trying to insert a duplicate user (should not insert):")
    row_data_insert_dup = {
        "username": "john_doe",  # Same as the previous one
        "email": "john@testing.com",
        "age": 25,
        "role": "admin"
    }
    manage_table(conn, "users", row_data=row_data_insert_dup, query="insert", where={"username": "john_doe"},
                 user="admin")

    print("\n🔹 Selecting all users:")
    all_users = manage_table(conn, "users", query="select")
    for user in all_users:
        print(user)

    print("\n🔹 Updating user's email...")
    row_data_update = {"email": "john.new@testing.com111"}
    where_conditions = {"username": "john_doe"}
    manage_table(conn, "users", row_data=row_data_update, query="update", where=where_conditions, user="admin")

    print("\n🔹 Selecting updated user:")
    updated_user = manage_table(conn, "users", query="select", where={"username": "john_doe"})
    for user in updated_user:
        print(user)

    print("\n🔹 Soft deleting user...")
    manage_table(conn, "users", query="delete", where={"username": "john_doe"}, user="admin")

    print("\n🔹 Selecting all users after delete:")
    users_after_delete = manage_table(conn, "users", query="select")
    for user in users_after_delete:
        print(user)
    conn.close()


# Run test
test_manage_table()
