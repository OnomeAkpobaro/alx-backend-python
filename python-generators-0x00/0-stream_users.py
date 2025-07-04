#!/usr/bin/python3

import seed

def stream_users():
    """
    Generator function that streams rows from the user_data table one by one
    Yields each row as a dictionary
    """
    connection = seed.connect_to_prodev()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data")
            
            # Use fetchone() to get one row at a time
            while True:
                row = cursor.fetchone()
                if row is None:
                    break
                yield row
                
        except Exception as e:
            print(f"Error streaming users: {e}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Could not connect to database")