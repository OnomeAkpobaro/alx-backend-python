import sqlite3

class DatabaseConnection:
    """
    A class-based context manager for handling database connections.
    Automatically opens and closes database connections.
    """
    
    def __init__(self, db_name):
        """
        Initialize the DatabaseConnection with a database name.
        
        Args:
            db_name (str): The name of the database file
        """
        self.db_name = db_name
        self.connection = None
        self.cursor = None
    
    def __enter__(self):
        """
        Enter the context manager.
        Opens the database connection and returns the cursor.
        
        Returns:
            sqlite3.Cursor: The database cursor for executing queries
        """
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            print(f"Database connection to '{self.db_name}' opened successfully.")
            return self.cursor
        except sqlite3.Error as e:
            print(f"Error opening database connection: {e}")
            raise
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the context manager.
        Closes the database connection and handles any exceptions.
        
        Args:
            exc_type: Exception type
            exc_val: Exception value
            exc_tb: Exception traceback
        """
        if self.cursor:
            self.cursor.close()
        
        if self.connection:
            if exc_type is None:
                # No exception occurred, commit any pending transactions
                self.connection.commit()
            else:
                # An exception occurred, rollback any pending transactions
                self.connection.rollback()
            
            self.connection.close()
            print(f"Database connection to '{self.db_name}' closed successfully.")
        
        # Return False to propagate any exceptions
        return False


# Example usage
if __name__ == "__main__":
    # Create a sample database and table for demonstration
    def setup_sample_database():
        with sqlite3.connect("sample.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    email TEXT UNIQUE NOT NULL
                )
            """)
            
            # Insert sample data
            cursor.execute("DELETE FROM users")  # Clear existing data
            sample_users = [
                ("Alice Johnson", 28, "alice@email.com"),
                ("Bob Smith", 35, "bob@email.com"),
                ("Charlie Brown", 42, "charlie@email.com"),
                ("Diana Prince", 31, "diana@email.com"),
                ("Edward Norton", 45, "edward@email.com")
            ]
            
            cursor.executemany(
                "INSERT INTO users (name, age, email) VALUES (?, ?, ?)",
                sample_users
            )
            conn.commit()
    
    # Setup the sample database
    setup_sample_database()
    
    # Use the DatabaseConnection context manager
    with DatabaseConnection("sample.db") as cursor:
        # Execute the query
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        
        # Print the results
        print("\nQuery Results:")
        print("ID | Name           | Age | Email")
        print("-" * 40)
        for row in results:
            print(f"{row[0]:<2} | {row[1]:<14} | {row[2]:<3} | {row[3]}")