"""
Utility functions for Quiz Bot
"""
from config import ADMIN_ID
from services import get_user_role


def is_admin(user_id: int) -> bool:
    """Check if user is super-admin or has admin role in DB"""
    if user_id == ADMIN_ID:
        return True
    role = get_user_role(user_id)
    return role == 'admin'
