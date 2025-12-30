"""
Create xiaohongshu_trends table
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.create_table(
        'xiaohongshu_trends',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('hashtag', sa.Text, nullable=False),
        sa.Column('post_count', sa.Integer, nullable=False),
        sa.Column('sample_posts', postgresql.JSONB, nullable=False),
        sa.Column('avg_sentiment', sa.Float, nullable=False),
        sa.Column('timestamp', sa.TIMESTAMP(timezone=True), nullable=False)
    )

def downgrade():
    op.drop_table('xiaohongshu_trends')
