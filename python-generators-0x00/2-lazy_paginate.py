#!/usr/bin/python3

import seed

def paginate_users(page_size, offset):
    """
    Fetches a page of users from the database with given page_size and offset
    Returns a list of user dictionaries
    """
    connection = seed.connect_to_prodev()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
            rows = cursor.fetchall()
            cursor.close()
            connection.close()
            return rows
        except Exception as e:
            print(f"Error paginating users: {e}")
            connection.close()
            return []
    else:
        print("Could not connect to database")
        return []

def lazy_pagination(page_size):
    """
    Generator function that lazily loads paginated data
    Yields each page only when needed
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:  # No more data
            break
        yield page
        offset += page_size