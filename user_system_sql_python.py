import psycopg2
from psycopg2 import sql
from psycopg2.extensions import connection  # Correct import

# Database connection parameters
DB_NAME = "user_system_db"
DB_USER = "postgres"
DB_PASSWORD = "1234"
DB_HOST = "localhost"
DB_PORT = "5432"

# Queries
CREATE_USERS_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY,
        user_name VARCHAR(50) NOT NULL UNIQUE,
        user_password VARCHAR(50) NOT NULL CHECK (LENGTH(user_password) > 5)
    )
"""

INSERT_QUERY = """
    INSERT INTO users (user_name, user_password) 
    VALUES 
    ('Alice', 'alice123'),
    ('Bob', 'bob456'),
    ('Charlie', 'charlie789'),
    ('David', 'david101'),
    ('Eve', 'eve202'),
    ('Frank', 'frank303'),
    ('Grace', 'grace404'),
    ('Hank', 'hank505'),
    ('Ivy', 'ivy606'),
    ('Jack', 'jack707')
    ON CONFLICT (user_name) DO NOTHING;
"""

UPDATE_QUERY = """
    UPDATE users SET user_password = 'newpassword123' WHERE user_name = 'Frank'
"""

DELETE_QUERY = """
    DELETE FROM users WHERE user_name = 'Grace'
"""

SELECT_QUERY = """
    SELECT * FROM users
    ORDER BY user_id ASC 
"""

# Function to make a connection with the database
def connect_to_db(_dbname: str = "postgres") -> connection | None:
    print(f"DB name -> {_dbname}")
    try:
        conn = psycopg2.connect(
            dbname=_dbname,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print(f"Connected to database '{_dbname}' successfully.")
        conn.autocommit = True  # Enable autocommit for database operations
        return conn
    except Exception as e:
        print(f"Error: Can't connect to database '{_dbname}': {e}")
        return None

# Function to check if a database exists
def database_exists(_conn: connection, _dbname: str) -> bool:
    if not _conn:
        print("Cannot check database existence: No connection.")
        return False

    cursor = _conn.cursor()
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (_dbname,))
    exists = cursor.fetchone() is not None  # Returns True if the database exists
    cursor.close()
    return exists

# Function to drop (delete) a database if it exists
def drop_database(_conn: connection, _dbname: str) -> None:
    if not _conn:
        print("Cannot drop database: No connection.")
        return

    cursor = _conn.cursor()
    try:
        print(f"Database '{_dbname}' existed, now deleting it...")
        cursor.execute(sql.SQL("DROP DATABASE {}").format(sql.Identifier(_dbname)))
        print(f"Database '{_dbname}' has been deleted successfully.")
    except Exception as e:
        print(f"Error deleting database '{_dbname}': {e}")
    finally:
        cursor.close()

# Function to create a new database

def create_database(conn: connection, _dbname: str) -> None:
    if not conn:
        print("Cannot create database: No connection.")
        return

    cursor = conn.cursor()
    try:
        # sql.Identifier(_dbname) sanitizes _dbname to prevent SQL injection.
        # Create DB
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(_dbname)))
        cursor.close()
        conn.commit()
        print(f"DB '{_dbname}' Create Successfully.")
    except Exception as e:
        print(f"Error in the process create DB '{_dbname}': {e}")
    finally:
        cursor.close()

# Universal function to execute any SQL query (CREATE, INSERT, UPDATE, DELETE, SELECT)
def execute_query(_conn: connection, _query: str) -> str:
    cursor = _conn.cursor()
    results = None
    try:
        # Execute the given query
        cursor.execute(_query)
        # Extract the first keyword (CREATE, INSERT, DELETE, SELECT)
        query_type = _query.strip().split()[0].upper()

        if query_type == "CREATE":
            print("Table or structure created successfully.")
        elif query_type == "INSERT":
            print(f"{cursor.rowcount} row(s) inserted successfully.")
        elif query_type == "UPDATE":
            print(f"{cursor.rowcount} row(s) updated successfully.")
        elif query_type == "DELETE":
            print(f"{cursor.rowcount} row(s) deleted successfully.")
        elif query_type == "SELECT":
            results = cursor.fetchall()
            # Results are returned as default a list of tuples, where each tuple represents a row.
            print(f"Query executed successfully. Retrieved {len(results)} row(s).")

        else:
            print("Query executed successfully.")

    except Exception as e:
        print(f"Error executing query: {e}")
    finally:
        cursor.close()
        return results

# Continue SELECT QUERY process
def continue_select_query_process(_results: list[tuple]) -> None:
    print(_results)
    for row in _results:
        # Print retrieved rows
        print(row)

# Login/Registration with max 3 attempts and exit option
def login_registration(_conn: connection) -> bool:
    login = False
    max_attempts = 3  # Maximum allowed login attempts
    attempts = 0

    while attempts < max_attempts:
        _user_name = input("Enter username (or type 'exit' to cancel): ").strip()
        if _user_name.lower() == "exit":
            print(" Exiting login/registration process.")
            return False  # Stop login process

        if len(_user_name) < 3:
            print(" Username must be at least 4 characters long.")
            continue  # Ask again

        _user_password = input("Enter password (or type 'exit' to cancel): ").strip()
        if _user_password.lower() == "exit":
            print("Exiting login/registration process.")
            return False  # Stop login process

        if len(_user_password) <= 5:
            print(" Password must be at least 6 characters long.")
            continue  # Ask again

        try:
            cursor = _conn.cursor()
            cursor.execute("SELECT user_password FROM users WHERE user_name = %s", (_user_name,))
            result = cursor.fetchone()  # Fetch password if user exists

            if result:
                #  User exists → Check password
                if result[0] == _user_password:
                    login = True
                    print(" Login successful!")
                    break  #  Exit the loop on success
                else:
                    print(f" Incorrect password. Attempts left: {max_attempts - (attempts + 1)}")
            else:
                # User does not exist → Register
                print(" User does not exist. Registering...")
                cursor.execute("INSERT INTO users (user_name, user_password) VALUES (%s, %s)",
                               (_user_name, _user_password))
                _conn.commit()
                print(" Registration successful!")
                login = True
                break  #  Exit the loop after registration

        except Exception as e:
            print(f"️ Error in Login/Registration process: {e}")

        attempts += 1  # Increment failed login attempts
        cursor.close()

    if not login:
        print(" Too many failed login attempts. Try again later.")

    return login

def main():
   # Create a single connection to 'postgres' for database management
    conn_postgres = connect_to_db("postgres")

    if conn_postgres:
        if database_exists(conn_postgres, DB_NAME):
            drop_database(conn_postgres, DB_NAME)

        create_database(conn_postgres, DB_NAME)
        conn_postgres.close()  # close connection postgres

        # create new connection to DB
        conn_user_db = connect_to_db(DB_NAME)

        if conn_user_db:
            execute_query(conn_user_db, CREATE_USERS_TABLE_QUERY)
            execute_query(conn_user_db, INSERT_QUERY)
            execute_query(conn_user_db, UPDATE_QUERY)
            execute_query(conn_user_db, DELETE_QUERY)
            # Capture SELECT results for continue process
            results = execute_query(conn_user_db, SELECT_QUERY)
            if results is not None:
                continue_select_query_process(results)
            login = login_registration(conn_user_db)
            if login:
                results = execute_query(conn_user_db, SELECT_QUERY)
                if results is not None:
                    continue_select_query_process(results)

            conn_user_db.close()
            print("Database connection closed successfully.")

        print("Main end runing")

if __name__ == "__main__":
    main()