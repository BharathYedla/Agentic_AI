"""
Initialize models package
"""
from models.database import (
    JobApplication,
    EmailLog,
    init_database,
    get_session,
    create_db_engine
)

__all__ = [
    'JobApplication',
    'EmailLog',
    'init_database',
    'get_session',
    'create_db_engine',
]
