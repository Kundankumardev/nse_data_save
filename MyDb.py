import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
import pandas as pd

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
                print(f"Connected to MySQL database: {self.database}")
        except Error as e:
            print(f"Error: '{e}'")
    
    def change_database(self, new_database):
        """Change the database without closing the connection."""
        try:
            if self.connection.is_connected():
                cursor = self.connection.cursor()
                cursor.execute(f"USE {new_database};")
                self.database = new_database
                print(f"Switched to database: {new_database}")
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
    
    def create_table_from_df(self, table_name, df):
        """Create a table based on the structure of the DataFrame."""
        cursor = self.connection.cursor()
        columns_with_types = []
        for col_name, dtype in df.dtypes.items():
            # Mapping DataFrame types to MySQL types
            if dtype == 'int64':
                sql_type = 'INT'
            elif dtype == 'float64':
                sql_type = 'FLOAT'
            elif dtype == 'object':
                sql_type = 'VARCHAR(255)'  # You can adjust this size if needed
            elif dtype == 'datetime64[ns]':
                sql_type = 'DATETIME'
            else:
                sql_type = 'TEXT'
            columns_with_types.append(f"{col_name} {sql_type}")
        
        columns_sql = ", ".join(columns_with_types)
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql});"
        
        try:
            cursor.execute(create_table_query)
            self.connection.commit()
            print(f"Table `{table_name}` created successfully")
        except Error as e:
            print(f"Error: '{e}'")
    
    def insert_df(self, table_name, df):
        """Insert the DataFrame's data into a specified table."""
        cursor = self.connection.cursor()
        columns = ", ".join(df.columns)
        placeholders = ", ".join(["%s"] * len(df.columns))
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        # Convert the DataFrame to a list of tuples (row-wise)
        data = [tuple(row) for row in df.to_numpy()]
        
        try:
            cursor.executemany(insert_query, data)
            self.connection.commit()
            print(f"Data from DataFrame inserted successfully into `{table_name}`")
        except Error as e:
            print(f"Error: '{e}'")
    
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
    
    # Create a sample DataFrame
    data = {
        'name': ['John Doe', 'Jane Smith', 'Alice Johnson'],
        'age': [30, 25, 35],
        'position': ['Software Engineer', 'Data Scientist', 'Product Manager']
    }
    df = pd.DataFrame(data)
    
    # Create a table based on the DataFrame's structure
    db.create_table_from_df("employees", df)
    
    # Insert the DataFrame's data into the table
    db.insert_df("employees", df)
    
    # Close the connection
    db.close()
