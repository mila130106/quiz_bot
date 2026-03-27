"""
Database initialization script
Run this to create database tables
"""
from services import init_db

if __name__ == "__main__":
    init_db()
    print("Database successfully initialized!")
