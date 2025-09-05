import psycopg2
from urllib.parse import quote_plus

def create_schema():
    password = quote_plus("P@ssw0rd")
    conn = psycopg2.connect(
        dbname="nextdb",
        user="admin",
        password="P@ssw0rd",
        host="localhost",
        port="5432"
    )
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Create schema
    cursor.execute("CREATE SCHEMA IF NOT EXISTS sales;")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_schema()
