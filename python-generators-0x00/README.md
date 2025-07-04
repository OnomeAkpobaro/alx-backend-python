# MySQL CSV Import Script

This Python script connects to a MySQL server, creates a database and table if they do not exist, and imports data from a CSV file into the table.

## Features

- Connects to a MySQL database server
- Creates a database named `ALX_prodev` if it doesn't exist
- Connects specifically to the `ALX_prodev` database
- Creates a table `user_data` with fields:
  - `user_id` (UUID, primary key)
  - `name` (string)
  - `email` (string)
  - `age` (integer)
- Imports data from a CSV file into the `user_data` table
- Skips insertion if data already exists in the table

## Prerequisites

- Python 3
- MySQL server
- `mysql-connector-python` module

Install the MySQL connector with:

```bash
pip install mysql-connector-python
```

## Database Configuration

The script connects using the following credentials:

- **Host**: `localhost`
- **User**: `root`
- **Password**: `root`

Update these credentials in the script if your setup is different.

## CSV File Format

The script expects a CSV file with the following headers:

```csv
name,email,age
John Doe,john@example.com,30
Jane Smith,jane@example.com,25
```

The `user_id` is automatically generated as a UUID for each entry.

## How to Use

1. Place your CSV file in the same directory as the script.
2. Run the script:

```bash
python3 your_script_name.py
```

> Replace `your_script_name.py` with the actual file name.

3. Make sure to update the `insert_data` function call at the bottom of the script to specify your CSV file, for example:

```python
insert_data(connection, 'your_file.csv')
```

## Functions Overview

- `connect_db()`: Connects to MySQL server
- `create_database(connection)`: Creates the `ALX_prodev` database
- `connect_to_prodev()`: Connects to `ALX_prodev` database
- `create_table(connection)`: Creates `user_data` table
- `insert_data(connection, csv_file)`: Reads from CSV and inserts data if table is empty


