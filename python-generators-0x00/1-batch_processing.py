#!/usr/bin/python3

import seed

def stream_users_in_batches(batch_size):
    """
    Generator function that fetches rows in batches from the user_data table
    Yields each batch as a list of dictionaries
    """
    connection = seed.connect_to_prodev()
    if not connection:
        print("Could not connect to database")
        return  # Exit the generator early if no connection
    
    try:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM user_data")
            while True:
                batch = cursor.fetchmany(batch_size)
                if not batch:
                    break
                yield batch

    except Exception as e:
        print(f"Error streaming users in batches: {e}")

    finally:
        connection.close()


def batch_processing(batch_size):
    """
    Processes each batch to filter users over the age of 25
    Prints filtered users from each batch
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)
