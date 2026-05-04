import os
from typing import Optional
import psycopg2
from psycopg2 import sql


class DatabaseConnectionError(Exception):
    """Raised when database connection fails"""
    pass


class User:
    """Model for user data"""
    def __init__(self, username: str, email: str, is_premium_user: bool = False):
        self.username = username
        self.email = email
        self.is_premium_user = is_premium_user


def get_db_connection():
    """
    Get a connection to the PostgreSQL database.
    
    Environment variables:
        DB_HOST: Database host (default: localhost)
        DB_PORT: Database port (default: 5432)
        DB_NAME: Database name (default: testdb)
        DB_USER: Database user (default: postgres)
        DB_PASSWORD: Database password (default: postgres)
    
    Returns:
        psycopg2 connection object
    
    Raises:
        DatabaseConnectionError: If connection fails
    """
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", 5432),
            database=os.getenv("DB_NAME", "testdb"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "postgres")
        )
        return conn
    except psycopg2.Error as e:
        raise DatabaseConnectionError(f"Failed to connect to database: {e}")


def create_users_table():
    """
    Create the users table if it doesn't exist.
    
    Schema:
        id: Auto-incrementing primary key
        username: String, not null, unique
        email: String, not null, unique
        is_premium_user: Boolean, default false
        created_at: Timestamp, default current time
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) NOT NULL UNIQUE,
                email VARCHAR(255) NOT NULL UNIQUE,
                is_premium_user BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    finally:
        cur.close()
        conn.close()


def insert_user(user: User) -> int:
    """
    Insert a new user into the database.
    
    Args:
        user: User object with username, email, and is_premium_user
    
    Returns:
        The ID of the newly inserted user
    
    Raises:
        DatabaseConnectionError: If connection to database fails
        psycopg2.IntegrityError: If username or email already exists
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute(
            sql.SQL("""
                INSERT INTO users (username, email, is_premium_user)
                VALUES (%s, %s, %s)
                RETURNING id
            """),
            (user.username, user.email, user.is_premium_user)
        )
        user_id = cur.fetchone()[0]
        conn.commit()
        return user_id
    except psycopg2.IntegrityError as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()


def get_user_by_id(user_id: int) -> Optional[dict]:
    """
    Retrieve a user from the database by ID.
    
    Args:
        user_id: The ID of the user to retrieve
    
    Returns:
        Dictionary with user data or None if not found
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute(
            "SELECT id, username, email, is_premium_user FROM users WHERE id = %s",
            (user_id,)
        )
        row = cur.fetchone()
        if row:
            return {
                "id": row[0],
                "username": row[1],
                "email": row[2],
                "is_premium_user": row[3]
            }
        return None
    finally:
        cur.close()
        conn.close()


def modify_user(user_id: int, username: str, email: str, is_premium_user: bool) -> bool:
    """
    Modify an existing user in the database.

    Args:
        user_id: The ID of the user to update
        username: Updated username
        email: Updated email
        is_premium_user: Updated premium status

    Returns:
        True if a user was updated, False if user was not found

    Raises:
        DatabaseConnectionError: If connection to database fails
        psycopg2.IntegrityError: If username or email conflicts with existing users
    """
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            UPDATE users
            SET username = %s, email = %s, is_premium_user = %s
            WHERE id = %s
            """,
            (username, email, is_premium_user, user_id),
        )
        updated = cur.rowcount > 0
        conn.commit()
        return updated
    except psycopg2.IntegrityError as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()


def delete_user(user_id: int) -> bool:
    """
    Delete a user from the database by ID.

    Args:
        user_id: The ID of the user to delete

    Returns:
        True if a user was deleted, False if user was not found
    """
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        deleted = cur.rowcount > 0
        conn.commit()
        return deleted
    finally:
        cur.close()
        conn.close()


def delete_all_users():
    """Delete all users from the database (useful for testing)"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("DELETE FROM users")
        conn.commit()
    finally:
        cur.close()
        conn.close()
