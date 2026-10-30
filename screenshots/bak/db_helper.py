# ============================================================
# db_helper.py
# ------------------------------------------------------------
# Database connection and reusable input validation functions.
# NOTE: Change the MySQL password in the connect_db() function
#       below to YOUR OWN MySQL root password before running!
# ============================================================

import mysql.connector
from mysql.connector import Error


# ------------------------------------------------------------
# DATABASE CONNECTION FUNCTIONS
# ------------------------------------------------------------
def connect_db():
    """Creates and returns a connection to the fines_db database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",          # <--- CHANGE THIS to your MySQL password
            database="fines_db"
        )
        if connection.is_connected():
            print("[SUCCESS] Connected to the MySQL database 'fines_db'.")
            return connection
    except Error as e:
        print(f"[ERROR] Could not connect to MySQL: {e}")
        return None


def close_db(connection):
    """Safely closes the database connection."""
    if connection and connection.is_connected():
        connection.close()
        print("[SUCCESS] Connection closed. Goodbye!")


# ------------------------------------------------------------
# INPUT VALIDATION FUNCTIONS
# ------------------------------------------------------------
def prompt_non_empty(prompt_text):
    """Keeps asking until the user enters a non-empty value."""
    while True:
        value = input(prompt_text).strip()
        if value:
            return value
        print("[ERROR] Input cannot be empty. Please try again.")


def prompt_positive_amount(prompt_text):
    """Keeps asking until the user enters a valid positive number.
    Uses try...except ValueError as required."""
    while True:
        raw = prompt_non_empty(prompt_text)
        try:
            amount = float(raw)
            if amount <= 0:
                print("[ERROR] Amount must be a positive number.")
            else:
                return amount
        except ValueError:
            print("[ERROR] Invalid amount. Please enter a number, e.g. 150.50")


def prompt_int(prompt_text):
    """Keeps asking until the user enters a valid whole number (used for IDs)."""
    while True:
        raw = prompt_non_empty(prompt_text)
        try:
            return int(raw)
        except ValueError:
            print("[ERROR] Invalid ID. Please enter a whole number, e.g. 3")


def prompt_yes_no(prompt_text):
    """Returns True only if the user answers 'y' (case-insensitive)."""
    while True:
        answer = input(prompt_text).strip().lower()
        if answer in ("y", "n"):
            return answer == "y"
        print("[ERROR] Please enter 'y' or 'n' only.")
