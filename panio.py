# ============================================================
# main.py - FINES MANAGEMENT SYSTEM (run this file to start)
# ------------------------------------------------------------
# Contains the CRUD operations and the menu loop.
# Connection + validation helpers live in db_helper.py.
# ============================================================

from mysql.connector import Error
from db_helper import (
    connect_db,
    close_db,
    prompt_non_empty,
    prompt_positive_amount,
    prompt_int,
    prompt_yes_no,
)


# ------------------------------------------------------------
# Shared helper: fetch a single fine by ID (used by Update & Delete)
# ------------------------------------------------------------
def get_fine_by_id(cursor, fine_id):
    """Returns (fine_id, person_name, amount, status) or None if not found.
    Uses a parameterized query."""
    cursor.execute(
        "SELECT fine_id, person_name, amount, status FROM fines WHERE fine_id = %s",
        (fine_id,)
    )
    return cursor.fetchone()


# ------------------------------------------------------------
# CREATE - Add a new fine record
# ------------------------------------------------------------
def add_fine(connection):
    """Asks the user for a name and amount, then inserts a new fine."""
    print("\n--- ADD A NEW FINE ---")

    person_name = prompt_non_empty("Enter person's name: ")
    amount = prompt_positive_amount("Enter fine amount: ")

    cursor = None
    try:
        cursor = connection.cursor()
        # Parameterized query (%s) - prevents SQL injection
        query = "INSERT INTO fines (person_name, amount, status) VALUES (%s, %s, %s)"
        values = (person_name, amount, "Unpaid")
        cursor.execute(query, values)
        connection.commit()
        print(f"[SUCCESS] Fine added for '{person_name}' with ID {cursor.lastrowid}.")
    except Error as e:
        print(f"[ERROR] Database error while adding fine: {e}")
        connection.rollback()
    finally:
        if cursor:
            cursor.close()


# ------------------------------------------------------------
# READ - Display all fine records
# ------------------------------------------------------------
def view_fines(connection):
    """Fetches and displays all fines in a formatted table."""
    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM fines")
        records = cursor.fetchall()

        if not records:
            print("\n[INFO] No fines found in the database.")
            return

        # Neat formatted table
        print("\n" + "=" * 60)
        print(f"{'ID':<6}{'NAME':<25}{'AMOUNT':>10}  {'STATUS':<15}")
        print("-" * 60)
        for (fine_id, person_name, amount, status) in records:
            print(f"{fine_id:<6}{person_name:<25}{amount:>10.2f}  {status:<15}")
        print("=" * 60)
        print(f"[SUCCESS] {cursor.rowcount} record(s) displayed.")
    except Error as e:
        print(f"[ERROR] Database error while fetching fines: {e}")
    finally:
        if cursor:
            cursor.close()


# ------------------------------------------------------------
# UPDATE - Mark an existing fine as Paid
# ------------------------------------------------------------
def mark_as_paid(connection):
    """Marks a fine as 'Paid' after verifying the ID exists."""
    print("\n--- MARK FINE AS PAID ---")
    fine_id = prompt_int("Enter the Fine ID to mark as paid: ")

    cursor = None
    try:
        cursor = connection.cursor()

        # Step 1: Verify the record exists (parameterized query)
        record = get_fine_by_id(cursor, fine_id)
        if record is None:
            print(f"[ERROR] No fine found with ID {fine_id}. Operation cancelled.")
            return

        _, person_name, _, current_status = record
        if current_status == "Paid":
            print(f"[INFO] Fine #{fine_id} for '{person_name}' is already marked as Paid.")
            return

        # Step 2: Update the status (parameterized query)
        query = "UPDATE fines SET status = %s WHERE fine_id = %s"
        cursor.execute(query, ("Paid", fine_id))
        connection.commit()
        print(f"[SUCCESS] Fine #{fine_id} for '{person_name}' is now marked as 'Paid'.")
    except Error as e:
        print(f"[ERROR] Database error while updating fine: {e}")
        connection.rollback()
    finally:
        if cursor:
            cursor.close()


# ------------------------------------------------------------
# DELETE - Remove a fine record (with confirmation)
# ------------------------------------------------------------
def delete_fine(connection):
    """Deletes a fine after verifying the ID exists and asking y/n."""
    print("\n--- DELETE A FINE ---")
    fine_id = prompt_int("Enter the Fine ID to delete: ")

    cursor = None
    try:
        cursor = connection.cursor()

        # Step 1: Verify the record exists (parameterized query)
        record = get_fine_by_id(cursor, fine_id)
        if record is None:
            print(f"[ERROR] No fine found with ID {fine_id}. Operation cancelled.")
            return

        _, person_name, amount, _ = record
        print(f"Found fine: #{fine_id} | {person_name} | {amount:.2f}")

        # Step 2: Ask for y/n confirmation
        confirmed = prompt_yes_no(
            "Are you sure you want to DELETE this record? (y/n): "
        )
        if not confirmed:
            print("[INFO] Delete operation cancelled by user.")
            return

        # Step 3: Delete the record (parameterized query)
        query = "DELETE FROM fines WHERE fine_id = %s"
        cursor.execute(query, (fine_id,))
        connection.commit()
        print(f"[SUCCESS] Fine #{fine_id} for '{person_name}' has been deleted.")
    except Error as e:
        print(f"[ERROR] Database error while deleting fine: {e}")
        connection.rollback()
    finally:
        if cursor:
            cursor.close()


# ------------------------------------------------------------
# MAIN MENU - Menu-driven loop
# ------------------------------------------------------------
def main_menu():
    """Runs the main menu loop until the user chooses Exit."""
    connection = connect_db()
    if connection is None:
        print("[ERROR] Cannot start the application without a database connection.")
        return

    try:
        while True:
            print("\n" + "=" * 40)
            print("      FINES MANAGEMENT SYSTEM")
            print("=" * 40)
            print("1. Add Fine    (Create)")
            print("2. View Fines  (Read)")
            print("3. Mark as Paid (Update)")
            print("4. Delete Fine (Delete)")
            print("5. Exit")
            print("-" * 40)

            choice = input("Enter your choice (1-5): ").strip()

            if choice == "1":
                add_fine(connection)
            elif choice == "2":
                view_fines(connection)
            elif choice == "3":
                mark_as_paid(connection)
            elif choice == "4":
                delete_fine(connection)
            elif choice == "5":
                print("[INFO] Closing the database connection...")
                close_db(connection)
                break
            else:
                print("[ERROR] Invalid choice. Please enter a number from 1 to 5.")
    except KeyboardInterrupt:
        print("\n[INFO] Program interrupted. Closing connection...")
        close_db(connection)


# ------------------------------------------------------------
# PROGRAM ENTRY POINT
# ------------------------------------------------------------
if __name__ == "__main__":
    main_menu()
