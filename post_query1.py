import psycopg2
from psycopg2 import sql

# Database connection parameters
DB_NAME = "user_system_db"
DB_USER = "postgres"
DB_PASSWORD = "1234" #your_password"
DB_HOST = "localhost"
DB_PORT = "5432"

# Function to connect to the database
def connect_to_db(dbname=DB_NAME):
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

# Function to create a new database
def create_database():
    conn = connect_to_db("postgres")  # Connect to default 'postgres' database
    conn.autocommit = True
    cursor = conn.cursor()
    try:
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
        print(f"Database '{DB_NAME}' created successfully.")
    except Exception as e:
        print(f"Error creating database: {e}")
    finally:
        cursor.close()
        conn.close()

# Function to create the USERS table
def create_table():
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                user_name VARCHAR(50) NOT NULL,
                user_password VARCHAR(50) NOT NULL CHECK (LENGTH(user_password) > 5)
            )
        """)
        conn.commit()
        print("Table 'users' created successfully.")
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        cursor.close()
        conn.close()

# Function to insert data into the USERS table
def insert_users():
    conn = connect_to_db()
    cursor = conn.cursor()
    users = [
        ("Alice", "alice123"),
        ("Bob", "bob456"),
        ("Charlie", "charlie789"),
        ("David", "david101"),
        ("Eve", "eve202"),
        ("Frank", "frank303"),
        ("Grace", "grace404"),
        ("Hank", "hank505"),
        ("Ivy", "ivy606"),
        ("Jack", "jack707")
    ]
    try:
        for user in users:
            cursor.execute("""
                INSERT INTO users (user_name, user_password)
                VALUES (%s, %s)
            """, user)
        conn.commit()
        print("10 users inserted successfully.")
    except Exception as e:
        print(f"Error inserting users: {e}")
    finally:
        cursor.close()
        conn.close()

# Function to read data from the USERS table
def read_users():
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except Exception as e:
        print(f"Error reading users: {e}")
    finally:
        cursor.close()
        conn.close()

# Function to update a user's password
def update_user_password(user_id, new_password):
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE users
            SET user_password = %s
            WHERE user_id = %s
        """, (new_password, user_id))
        conn.commit()
        print(f"Password for user_id {user_id} updated successfully.")
    except Exception as e:
        print(f"Error updating password: {e}")
    finally:
        cursor.close()
        conn.close()

# Function to delete a user by user_id
def delete_user(user_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        conn.commit()
        print(f"User with user_id {user_id} deleted successfully.")
    except Exception as e:
        print(f"Error deleting user: {e}")
    finally:
        cursor.close()
        conn.close()

# Function to handle user login
def login():
    conn = connect_to_db()
    cursor = conn.cursor()
    attempts = 3
    while attempts > 0:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        try:
            cursor.execute("""
                SELECT * FROM users
                WHERE user_name = %s AND user_password = %s
            """, (username, password))
            user = cursor.fetchone()
            if user:
                print(f"Login successful! Welcome, {username}.")
                return True
            else:
                attempts -= 1
                print(f"Invalid credentials. {attempts} attempts remaining.")
        except Exception as e:
            print(f"Error during login: {e}")
        if attempts == 0:
            print("No more attempts left. Exiting.")
            return False
    cursor.close()
    conn.close()

# Function to delete the database (for cleanup)
def delete_database():
    conn = connect_to_db("postgres")  # Connect to default 'postgres' database
    conn.autocommit = True
    cursor = conn.cursor()
    try:
        cursor.execute(sql.SQL("DROP DATABASE {}").format(sql.Identifier(DB_NAME)))
        print(f"Database '{DB_NAME}' deleted successfully.")
    except Exception as e:
        print(f"Error deleting database: {e}")
    finally:
        cursor.close()
        conn.close()

# Main function to execute all operations
def main():
    # Create database and table
    create_database()
    create_table()

    # Insert users
    insert_users()

    # Read users
    print("Users in the database:")
    read_users()

    # Update a user's password
    update_user_password(1, "newpassword123")

    # Delete a user
    delete_user(10)

    # Login system
    if login():
        print("You are now logged in.")
    else:
        print("Login failed.")

if __name__ == "__main__":
    main()