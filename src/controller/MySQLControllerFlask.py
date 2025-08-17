import mysql.connector
import os
from dotenv import load_dotenv
from datetime import datetime as dt

load_dotenv()



class MySQLManager:
    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.port = int(os.getenv("DB_PORT"))
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_NAME")
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.conn.cursor()

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def get_column_type(self, value):
        if isinstance(value, int):
            return "INT"
        elif isinstance(value, float):
            return "DOUBLE"
        elif isinstance(value, bool):
            return "BOOLEAN"
        elif isinstance(value, str):
            return "VARCHAR(255)"
        else:
            return "TEXT"

    def manage_table(self, table_name, row_data=None, query=None, where=None, user=None, select_columns=None):
        self.connect()

        # Audit columns
        audit_columns = {
            'date_row_inserted': 'VARCHAR(255)',
            'date_row_deleted': 'VARCHAR(255)',
            'last_date_row_updated': 'VARCHAR(255)',
            'user_inserted_data': 'VARCHAR(255)',
            'user_deleted_rows': 'VARCHAR(255)',
            'last_user_updated_row': 'VARCHAR(255)',
            'deleted': "VARCHAR(3) DEFAULT 'no'"
        }

        # === 1. Check if table exists ===
        self.cursor.execute("SHOW TABLES LIKE %s", (table_name,))
        table_exists = self.cursor.fetchone()

        if not table_exists:
            if not row_data:
                raise Exception("Table does not exist and no row_data provided to create it.")

            data_columns_def = ", ".join([f"{col} {self.get_column_type(val)}" for col, val in row_data.items()])
            audit_columns_def = ", ".join([f"{col} {dtype}" for col, dtype in audit_columns.items()])
            create_query = f"""CREATE TABLE {table_name} (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                {data_columns_def},
                                {audit_columns_def}
                            )"""
            self.cursor.execute(create_query)
            existing_columns = set(row_data.keys()) | set(audit_columns.keys())
        else:
            self.cursor.execute(f"SHOW COLUMNS FROM {table_name}")
            existing_columns = {row[0] for row in self.cursor.fetchall()}

        # === 2. Add any new columns from row_data ===
        if row_data:
            for col, val in row_data.items():
                if col not in existing_columns:
                    col_type = self.get_column_type(val)
                    alter_query = f"ALTER TABLE {table_name} ADD COLUMN {col} {col_type}"
                    self.cursor.execute(alter_query)
                    existing_columns.add(col)

        # === 3. Add missing audit columns ===
        for col, col_type in audit_columns.items():
            if col not in existing_columns:
                alter_query = f"ALTER TABLE {table_name} ADD COLUMN {col} {col_type}"
                self.cursor.execute(alter_query)
                existing_columns.add(col)

        # === 4. Handle Queries ===
        now_str = dt.utcnow().isoformat()

        if query == "insert" and row_data:
            row_data.setdefault("date_row_inserted", now_str)
            row_data.setdefault("deleted", "no")
            if user:
                row_data.setdefault("user_inserted_data", user)

            columns = ", ".join(row_data.keys())
            values = ", ".join(["%s"] * len(row_data))
            insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
            self.cursor.execute(insert_query, tuple(row_data.values()))

        elif query == "update" and row_data and where:
            row_data["last_date_row_updated"] = now_str
            if user:
                row_data["last_user_updated_row"] = user

            set_clause = ", ".join([f"{key} = %s" for key in row_data])
            where_clause = " AND ".join([f"{key} = %s" for key in where])
            update_query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
            self.cursor.execute(update_query, tuple(row_data.values()) + tuple(where.values()))

        elif query == "delete" and where:
            soft_delete_fields = {
                "deleted": "yes",
                "date_row_deleted": now_str
            }
            if user:
                soft_delete_fields["user_deleted_rows"] = user

            set_clause = ", ".join([f"{key} = %s" for key in soft_delete_fields])
            where_clause = " AND ".join([f"{key} = %s" for key in where])
            delete_query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
            self.cursor.execute(delete_query, tuple(soft_delete_fields.values()) + tuple(where.values()))

        elif query == "select":
            select_cols = ", ".join(select_columns) if select_columns else "*"
            if where:
                if "deleted" not in where:
                    where["deleted"] = "no"
                where_clause = " AND ".join([f"{key} = %s" for key in where])
                select_query = f"SELECT {select_cols} FROM {table_name} WHERE {where_clause}"
                self.cursor.execute(select_query, tuple(where.values()))
            else:
                select_query = f"SELECT {select_cols} FROM {table_name} WHERE deleted = 'no'"
                self.cursor.execute(select_query)

            rows = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]
            self.disconnect()
            return [dict(zip(columns, row)) for row in rows]

        self.conn.commit()
        self.disconnect()

