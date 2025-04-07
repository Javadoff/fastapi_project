"""Added users and transactions models

Revision ID: c0dd1aed416c
Revises: 
Create Date: 2025-04-07 02:15:41.377504

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'c0dd1aed416c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('password_hash', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('transactions',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('currency', sa.String(), nullable=False),
    sa.Column('transaction_type', sa.String(), nullable=False),
    sa.Column('recipient_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.CheckConstraint("(transaction_type = 'withdrawal' AND amount < 0) OR (transaction_type = 'deposit' AND amount > 0)", name='check_amount_matches_type'),
    sa.CheckConstraint("currency IN ('USD', 'EUR', 'GBP')", name='check_valid_currency'),
    sa.CheckConstraint("status IN ('pending', 'success', 'failed')", name='check_valid_status'),
    sa.CheckConstraint("transaction_type IN ('deposit', 'withdrawal')", name='check_valid_transaction_type'),
    sa.CheckConstraint('amount != 0', name='check_non_zero_amount'),
    sa.ForeignKeyConstraint(['recipient_id'], ['users.id'], name='fk_transactions_recipient_id', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transactions_id'), 'transactions', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_transactions_id'), table_name='transactions')
    op.drop_table('transactions')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
