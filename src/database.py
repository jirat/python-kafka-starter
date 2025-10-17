# import psycopg2
# from psycopg2.extras import RealDictCursor
import pyodbc
from .config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME


def get_db_connection():
    """Create and return a database connection."""
    # conn = psycopg2.connect(
    #     host=DB_HOST,
    #     port=DB_PORT,
    #     user=DB_USER,
    #     password=DB_PASSWORD,
    #     database=DB_NAME
    # )
    # return conn
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={DB_HOST},{DB_PORT};"
        f"DATABASE={DB_NAME};"
        f"UID={DB_USER};"
        f"PWD={DB_PASSWORD}"
    )
    conn = pyodbc.connect(conn_str)
    return conn

def init_database():
    """Initialize the database table if it doesn't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            IF NOT EXISTS (
                SELECT * FROM sysobjects 
                WHERE name = 'kafka_messages' AND xtype = 'U'
            )
            BEGIN
                CREATE TABLE kafka_messages (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    customer_id NVARCHAR(255),
                    message NVARCHAR(MAX) NOT NULL,
                    created_at DATETIME2 DEFAULT SYSDATETIME()
                );
            END
        """)
        conn.commit()
        print("✅ Database table 'kafka_messages' is ready")
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def save_message_to_db(customer_id, message):
    """
    Save a Kafka message to the database.
    
    Args:
        customer_id: Customer ID from the message
        message: Message text to save
    
    Returns:
        bool: True if successful, False otherwise
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO kafka_messages (customer_id, message)
            VALUES (?, ?)
        """, (customer_id, message))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"❌ Error saving message to database: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()


def get_all_messages(limit=100):
    """
    Retrieve messages from the database.
    
    Args:
        limit: Maximum number of messages to retrieve
    
    Returns:
        list: List of message dictionaries
    """
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cursor.execute("""
            SELECT * FROM kafka_messages 
            ORDER BY created_at DESC 
            LIMIT ?
        """, (limit,))
        
        messages = cursor.fetchall()
        return messages
    except Exception as e:
        print(f"❌ Error retrieving messages: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

