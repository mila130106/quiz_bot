"""
Database initialization script
Run this to create database tables
"""
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services import init_db

if __name__ == "__main__":
    init_db()
    print("Database successfully initialized!")
