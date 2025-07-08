import sqlite3

class ExecuteQuery:
    """
    A reusable class-based context manager for executing database queries.
    Manages both connection and query execution.
    """
    
    def __init__(self, db_name, query, parameters=None):
        """
        Initialize the ExecuteQuery context manager.
        
        Args:
            db_name (str): The name of the database file
            query (str): The SQL query to execute
            parameters (tuple): Parameters for the query (optional)
        """
        self.db_name = db_name
        self.query = query
        self.parameters = parameters or ()
        self.connection = None
        self.cursor = None
        self.results = None
    
    def __enter__(self):
        """
        Enter the context manager.
        Opens database connection, executes query, and returns results.
        
        Returns:
            list: Query results
        """
        try:
            # Open database connection
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            
            # Execute the query with parameters
            self.cursor.execute(self.query, self.parameters)
            self.results = self.cursor.fetchall()
            
            print(f"Query executed successfully: {self.query}")
            if self.parameters:
                print(f"Parameters: {self.parameters}")
            
            return self.results
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the context manager.
        Closes database connection and handles exceptions.
        
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
            print("Database connection closed successfully.")
        
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
                ("Edward Norton", 45, "edward@email.com"),
                ("Frank Castle", 38, "frank@email.com"),
                ("Grace Kelly", 29, "grace@email.com"),
                ("Henry Ford", 55, "henry@email.com")
            ]
            
            cursor.executemany(
                "INSERT INTO users (name, age, email) VALUES (?, ?, ?)",
                sample_users
            )
            conn.commit()
    
    # Setup the sample database
    setup_sample_database()
    
    # Use the ExecuteQuery context manager
    query = "SELECT * FROM users WHERE age > ?"
    parameter = 25
    
    with ExecuteQuery("sample.db", query, (parameter,)) as results:
        print(f"\nQuery Results for users older than {parameter}:")
        print("ID | Name           | Age | Email")
        print("-" * 45)
        for row in results:
            print(f"{row[0]:<2} | {row[1]:<14} | {row[2]:<3} | {row[3]}")
    
    # Example with a different query
    print("\n" + "="*50)
    print("Another example with different parameters:")
    
    with ExecuteQuery("sample.db", "SELECT name, age FROM users WHERE age BETWEEN ? AND ?", (30, 50)) as results:
        print("\nUsers between 30 and 50 years old:")
        print("Name           | Age")
        print("-" * 20)
        for row in results:
            print(f"{row[0]:<14} | {row[1]}")