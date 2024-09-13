import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

class MySQLDatabase:
    def __init__(self):
        """Load environment variables and initialize the connection."""
        load_dotenv()  # Load environment variables from the .env file
        self.host = os.getenv("DB_HOST")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_NAME")
        self.connection = None
    
    def connect(self):
        """Establish connection to the MySQL database."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            print(f"Error: '{e}'")
    
    def execute_query(self, query, params=None):
        """Execute a SQL query (INSERT, UPDATE, DELETE)."""
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            self.connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"Error: '{e}'")
    
    def fetch_query(self, query, params=None):
        """Execute a SELECT query and return the results."""
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"Error: '{e}'")
            return None
    
    def close(self):
        """Close the database connection."""
        if self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")

# Example usage:
if __name__ == "__main__":
    db = MySQLDatabase()
    
    # Connect to the database
    db.connect()
    
    # Create a new table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS employees (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        age INT,
        position VARCHAR(100)
    );
    """
    db.execute_query(create_table_query)
    
    # Insert data into the table
    insert_query = "INSERT INTO employees (name, age, position) VALUES (%s, %s, %s)"
    db.execute_query(insert_query, ("John Doe", 30, "Software Engineer"))
    
    # Fetch data
    select_query = "SELECT * FROM employees"
    results = db.fetch_query(select_query)
    for row in results:
        print(row)
    
    # Close the connection
    db.close()
