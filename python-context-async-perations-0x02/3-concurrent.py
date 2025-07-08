import asyncio
import aiosqlite
import sqlite3

async def async_fetch_users():
    """
    Asynchronously fetch all users from the database.
    
    Returns:
        list: All users from the users table
    """
    try:
        async with aiosqlite.connect("sample.db") as db:
            async with db.execute("SELECT * FROM users") as cursor:
                results = await cursor.fetchall()
                print(f"async_fetch_users: Retrieved {len(results)} users")
                return results
    except Exception as e:
        print(f"Error in async_fetch_users: {e}")
        return []

async def async_fetch_older_users():
    """
    Asynchronously fetch users older than 40 from the database.
    
    Returns:
        list: Users older than 40 from the users table
    """
    try:
        async with aiosqlite.connect("sample.db") as db:
            async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
                results = await cursor.fetchall()
                print(f"async_fetch_older_users: Retrieved {len(results)} users older than 40")
                return results
    except Exception as e:
        print(f"Error in async_fetch_older_users: {e}")
        return []

async def fetch_concurrently():
    """
    Execute both fetch functions concurrently using asyncio.gather.
    
    Returns:
        tuple: Results from both fetch functions
    """
    print("Starting concurrent database queries...")
    
    # Execute both queries concurrently
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    
    print("\nConcurrent queries completed!")
    
    # Display results
    print("\n" + "="*50)
    print("ALL USERS:")
    print("ID | Name           | Age | Email")
    print("-" * 45)
    for user in all_users:
        print(f"{user[0]:<2} | {user[1]:<14} | {user[2]:<3} | {user[3]}")
    
    print("\n" + "="*50)
    print("USERS OLDER THAN 40:")
    print("ID | Name           | Age | Email")
    print("-" * 45)
    for user in older_users:
        print(f"{user[0]:<2} | {user[1]:<14} | {user[2]:<3} | {user[3]}")
    
    return all_users, older_users

def setup_sample_database():
    """
    Create a sample database with users table and sample data.
    """
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
            ("Henry Ford", 55, "henry@email.com"),
            ("Ivy League", 43, "ivy@email.com"),
            ("Jack Sparrow", 39, "jack@email.com")
        ]
        
        cursor.executemany(
            "INSERT INTO users (name, age, email) VALUES (?, ?, ?)",
            sample_users
        )
        conn.commit()
        print("Sample database created successfully!")

# Main execution
if __name__ == "__main__":
    # Setup the sample database
    setup_sample_database()
    
    # Run the concurrent fetch using asyncio.run()
    asyncio.run(fetch_concurrently())