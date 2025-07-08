import time
import sqlite3 
import functools

query_cache = {}

def with_db_connection(func):
    """Decorator that automatically handles database connection opening and closing"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper

def cache_query(func):
    """Decorator that caches query results based on the SQL query string"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query from kwargs or args
        query = kwargs.get('query')
        if not query:
            # Try to find query in positional arguments (skip conn which is first arg)
            for arg in args[1:]:
                if isinstance(arg, str) and arg.strip().upper().startswith(('SELECT', 'SHOW', 'DESCRIBE')):
                    query = arg
                    break
        
        # Use query as cache key
        cache_key = query if query else str(args) + str(kwargs)
        
        # Check if result is in cache
        if cache_key in query_cache:
            print(f"Cache hit for query: {query}")
            return query_cache[cache_key]
        
        # Execute function and cache result
        print(f"Cache miss for query: {query}")
        result = func(*args, **kwargs)
        query_cache[cache_key] = result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")