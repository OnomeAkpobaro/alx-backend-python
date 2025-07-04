#!/usr/bin/python3

import seed

def stream_user_ages():
    """
    Generator function that yields user ages one by one
    """
    connection = seed.connect_to_prodev()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT age FROM user_data")
            
            while True:
                row = cursor.fetchone()
                if row is None:
                    break
                yield row[0]  # Yield just the age value
                
        except Exception as e:
            print(f"Error streaming user ages: {e}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Could not connect to database")

def calculate_average_age():
    """
    Calculates the average age using the generator without loading
    the entire dataset into memory
    """
    total_age = 0
    count = 0
    
    # Loop through ages one by one
    for age in stream_user_ages():
        total_age += age
        count += 1
    
    if count > 0:
        average_age = total_age / count
        print(f"Average age of users: {average_age}")
    else:
        print("No users found")

if __name__ == "__main__":
    calculate_average_age()