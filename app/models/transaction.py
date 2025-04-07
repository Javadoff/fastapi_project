import sqlalchemy
from app.models.base import metadata
from sqlalchemy import Column, Integer, String, Float, DateTime, func, Enum, CheckConstraint
from app.models.user import users


TRANSACTION_TYPES = ('deposit', 'withdrawal')
TRANSACTION_STATUSES = ('pending', 'success', 'failed')
VALID_CURRENCIES = ('USD', 'EUR', 'GBP')  # Add more as needed


transactions = sqlalchemy.Table(
    "transactions",
    metadata,
    sqlalchemy.Column("id", Integer, primary_key=True, autoincrement=True, index=True),
    sqlalchemy.Column("user_id", Integer, sqlalchemy.ForeignKey(users.c.id, ondelete="CASCADE"), nullable=False),
    sqlalchemy.Column("amount", Float, nullable=False),
    sqlalchemy.Column("currency", String, nullable=False),
    sqlalchemy.Column("transaction_type", String, nullable=False),
    sqlalchemy.Column("recipient_id", Integer, sqlalchemy.ForeignKey(users.c.id, ondelete="CASCADE", name="fk_transactions_recipient_id"), nullable=True),
    sqlalchemy.Column("status", String, nullable=False, default='pending'),
    sqlalchemy.Column("timestamp", DateTime, default=func.now(), nullable=False),
    
    # Add constraints
    CheckConstraint('amount != 0', name='check_non_zero_amount'),
    CheckConstraint(f"transaction_type IN {TRANSACTION_TYPES}", name='check_valid_transaction_type'),
    CheckConstraint(f"status IN {TRANSACTION_STATUSES}", name='check_valid_status'),
    CheckConstraint(f"currency IN {VALID_CURRENCIES}", name='check_valid_currency'),
    CheckConstraint('(transaction_type = \'withdrawal\' AND amount < 0) OR (transaction_type = \'deposit\' AND amount > 0)', name='check_amount_matches_type')
)
