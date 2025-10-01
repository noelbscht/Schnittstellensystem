import string
import random


def file_content(path):
    """Read and return file content."""
    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "<p>Nicht verfügbar.</p>"


def sql(prompt, parameters=None, fetch_one=False, return_insert_id=False, database_name=None):
    """ if database_name not set then the prompt will be sent to the main database"""
    from main import app

    with app.app_context():
        mysql = app.extensions['mysqldb']
        if database_name:
            mysql.connection.select_db(database_name)

        cursor = mysql.connection.cursor()
        try:
            if parameters:
                cursor.execute(prompt, parameters)
            else:
                cursor.execute(prompt)

            if prompt.strip().upper().startswith(("INSERT", "UPDATE", "DELETE", "REPLACE", "CREATE", "DROP", "ALTER")):
                cursor.connection.commit()

            if fetch_one:
                res = cursor.fetchone()
            else:
                res = cursor.fetchall()

            if return_insert_id:
                insert_id = cursor.lastrowid
        finally:
            cursor.close()

        if return_insert_id:
            return insert_id
        return res


def generate_username(length=8):
    result = ""
    for i in range(length):
        result += string.printable[random.randint(0, len(string.printable))]
    return result
