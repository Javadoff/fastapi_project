import sqlalchemy
from app.models.base import metadata
from sqlalchemy import Column, Integer, String, Float, DateTime, func, Enum, CheckConstraint, Numeric
from app.models.user import users


transactions = sqlalchemy.Table(
    "transactions",
    metadata,
    sqlalchemy.Column("id", Integer, primary_key=True, autoincrement=True, index=True),
    sqlalchemy.Column("user_id", Integer, sqlalchemy.ForeignKey(users.c.id, ondelete="CASCADE"), nullable=False),
    sqlalchemy.Column("amount", Numeric(9, 2), nullable=False),
    sqlalchemy.Column("currency", String, nullable=False),
    sqlalchemy.Column("transaction_type", String, nullable=False),
    sqlalchemy.Column("recipient_id", Integer, sqlalchemy.ForeignKey(users.c.id, ondelete="CASCADE", name="fk_transactions_recipient_id"), nullable=True),
    sqlalchemy.Column("status", String, nullable=False, default='pending'),
    sqlalchemy.Column("timestamp", DateTime, default=func.now(), nullable=False),
)
