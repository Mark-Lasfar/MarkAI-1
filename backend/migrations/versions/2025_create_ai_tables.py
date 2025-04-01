# backend/migrations/versions/2025_create_ai_tables.py
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'ai_models',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('ai_models')