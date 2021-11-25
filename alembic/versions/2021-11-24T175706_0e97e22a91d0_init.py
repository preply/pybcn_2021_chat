"""init

Revision ID: 0e97e22a91d0
Revises: 
Create Date: 2021-11-24 17:57:06.331172

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0e97e22a91d0"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "rooms",
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column("name", sa.String(length=256), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_rooms_created_at"), "rooms", ["created_at"], unique=False)
    op.create_index(op.f("ix_rooms_id"), "rooms", ["id"], unique=False)
    op.create_index(op.f("ix_rooms_name"), "rooms", ["name"], unique=False)
    op.create_index(op.f("ix_rooms_updated_at"), "rooms", ["updated_at"], unique=False)
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column("name", sa.String(length=256), nullable=True),
        sa.Column("password", sa.String(length=256), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("role", sa.Enum("USER", "ADMIN", name="role"), nullable=True),
        sa.Column(
            "lang",
            sa.Enum(
                "EN",
                "ES",
                "UA",
                "RU",
                "PT",
                "CA",
                "FR",
                "DE",
                "ZH",
                "AR",
                "KO",
                "IW",
                "JA",
                name="lang",
            ),
            nullable=True,
        ),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_users_created_at"), "users", ["created_at"], unique=False)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(op.f("ix_users_is_active"), "users", ["is_active"], unique=False)
    op.create_index(op.f("ix_users_role"), "users", ["role"], unique=False)
    op.create_index(op.f("ix_users_updated_at"), "users", ["updated_at"], unique=False)
    op.create_table(
        "messages",
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column("room_id", postgresql.UUID(), nullable=True),
        sa.Column("user_id", postgresql.UUID(), nullable=True),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column(
            "lang",
            sa.Enum(
                "EN",
                "ES",
                "UA",
                "RU",
                "PT",
                "CA",
                "FR",
                "DE",
                "ZH",
                "AR",
                "KO",
                "IW",
                "JA",
                name="lang",
            ),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["room_id"], ["rooms.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_messages_created_at"), "messages", ["created_at"], unique=False
    )
    op.create_index(op.f("ix_messages_id"), "messages", ["id"], unique=False)
    op.create_index(
        op.f("ix_messages_updated_at"), "messages", ["updated_at"], unique=False
    )


def downgrade():
    op.drop_index(op.f("ix_messages_updated_at"), table_name="messages")
    op.drop_index(op.f("ix_messages_id"), table_name="messages")
    op.drop_index(op.f("ix_messages_created_at"), table_name="messages")
    op.drop_table("messages")
    op.drop_index(op.f("ix_users_updated_at"), table_name="users")
    op.drop_index(op.f("ix_users_role"), table_name="users")
    op.drop_index(op.f("ix_users_is_active"), table_name="users")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_index(op.f("ix_users_created_at"), table_name="users")
    op.drop_table("users")
    op.drop_index(op.f("ix_rooms_updated_at"), table_name="rooms")
    op.drop_index(op.f("ix_rooms_name"), table_name="rooms")
    op.drop_index(op.f("ix_rooms_id"), table_name="rooms")
    op.drop_index(op.f("ix_rooms_created_at"), table_name="rooms")
    op.drop_table("rooms")
