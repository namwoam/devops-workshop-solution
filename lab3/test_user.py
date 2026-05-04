import pytest
from lab3.user import User, insert_user, get_user_by_id, create_users_table, delete_all_users, DatabaseConnectionError


@pytest.fixture(scope="function")
def setup_db():
    """Setup database before each test"""
    create_users_table()
    delete_all_users()
    yield
    delete_all_users()


class TestUserInsertion:
    """Test suite for user insertion functionality"""
    
    def test_insert_user_successfully(self, setup_db):
        """Test inserting a user successfully"""
        user = User(username="john_doe", email="john@example.com", is_premium_user=False)
        user_id = insert_user(user)
        
        assert user_id > 0
        
        # Verify user was inserted
        retrieved_user = get_user_by_id(user_id)
        assert retrieved_user is not None
        assert retrieved_user["username"] == "john_doe"
        assert retrieved_user["email"] == "john@example.com"
        assert retrieved_user["is_premium_user"] is False
    
    def test_insert_premium_user(self, setup_db):
        """Test inserting a premium user"""
        user = User(username="premium_user", email="premium@example.com", is_premium_user=True)
        user_id = insert_user(user)
        
        retrieved_user = get_user_by_id(user_id)
        assert retrieved_user["is_premium_user"] is True
    
    def test_insert_user_duplicate_username(self, setup_db):
        """Test that duplicate usernames are rejected"""
        user1 = User(username="duplicate", email="user1@example.com")
        insert_user(user1)
        
        user2 = User(username="duplicate", email="user2@example.com")
        with pytest.raises(Exception):  # psycopg2.IntegrityError
            insert_user(user2)
    
    def test_insert_user_duplicate_email(self, setup_db):
        """Test that duplicate emails are rejected"""
        user1 = User(username="user1", email="duplicate@example.com")
        insert_user(user1)
        
        user2 = User(username="user2", email="duplicate@example.com")
        with pytest.raises(Exception):  # psycopg2.IntegrityError
            insert_user(user2)
    
    def test_get_user_not_found(self, setup_db):
        """Test retrieving a non-existent user"""
        user = get_user_by_id(9999)
        assert user is None
    
    def test_insert_multiple_users(self, setup_db):
        """Test inserting multiple users"""
        users = [
            User(username="alice", email="alice@example.com"),
            User(username="bob", email="bob@example.com"),
            User(username="charlie", email="charlie@example.com", is_premium_user=True),
        ]
        
        user_ids = [insert_user(user) for user in users]
        assert len(user_ids) == 3
        
        # Verify all users exist
        for i, user_id in enumerate(user_ids):
            retrieved = get_user_by_id(user_id)
            assert retrieved is not None
            assert retrieved["username"] == users[i].username
