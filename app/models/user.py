import sqlalchemy
from app.models.base import metadata
from sqlalchemy import Column, Integer, String


users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", Integer, primary_key=True),
    sqlalchemy.Column("username", String, unique=True, index=True),
    sqlalchemy.Column("password_hash", String),
    sqlalchemy.Column("email", String, unique=True, index=True),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=sqlalchemy.func.now()),
)

