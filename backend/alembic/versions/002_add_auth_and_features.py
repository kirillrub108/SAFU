"""Add auth and features

Revision ID: 002_add_auth_and_features
Revises: 001_initial
Create Date: 2025-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002_add_auth_and_features'
down_revision = '001_initial'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Faculties
    op.create_table(
        'faculties',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_faculties_id'), 'faculties', ['id'], unique=False)
    op.create_index(op.f('ix_faculties_name'), 'faculties', ['name'], unique=True)

    # Add faculty_id to groups
    op.add_column('groups', sa.Column('faculty_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_groups_faculty_id', 'groups', 'faculties', ['faculty_id'], ['id'])
    op.create_index(op.f('ix_groups_faculty_id'), 'groups', ['faculty_id'], unique=False)

    # Users
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password_hash', sa.String(), nullable=False),
        sa.Column('fio', sa.String(), nullable=False),
        sa.Column('role', sa.Enum('STUDENT', 'LECTURER', 'ADMIN', 'DEVELOPER', name='userrole'), nullable=False),
        sa.Column('group_id', sa.Integer(), nullable=True),
        sa.Column('lecturer_id', sa.Integer(), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['group_id'], ['groups.id']),
        sa.ForeignKeyConstraint(['lecturer_id'], ['lecturers.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_group_id'), 'users', ['group_id'], unique=False)
    op.create_index(op.f('ix_users_lecturer_id'), 'users', ['lecturer_id'], unique=False)

    # Favorites
    op.create_table(
        'favorites',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('filters', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_favorites_id'), 'favorites', ['id'], unique=False)
    op.create_index(op.f('ix_favorites_user_id'), 'favorites', ['user_id'], unique=False)

    # Notifications
    op.create_table(
        'notifications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('type', sa.Enum('SCHEDULE_CHANGE', 'EVENT_CANCELLED', 'EVENT_ADDED', 'EVENT_MODIFIED', 'ROOM_CHANGED', 'TIME_CHANGED', name='notificationtype'), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('read', sa.Boolean(), nullable=False),
        sa.Column('event_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['event_id'], ['events.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notifications_id'), 'notifications', ['id'], unique=False)
    op.create_index(op.f('ix_notifications_user_id'), 'notifications', ['user_id'], unique=False)

    # Notification Settings
    op.create_table(
        'notification_settings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('schedule_changes', sa.Boolean(), nullable=False),
        sa.Column('event_cancelled', sa.Boolean(), nullable=False),
        sa.Column('event_added', sa.Boolean(), nullable=False),
        sa.Column('event_modified', sa.Boolean(), nullable=False),
        sa.Column('room_changed', sa.Boolean(), nullable=False),
        sa.Column('time_changed', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_notification_settings_id'), 'notification_settings', ['id'], unique=False)
    op.create_index(op.f('ix_notification_settings_user_id'), 'notification_settings', ['user_id'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_notification_settings_user_id'), table_name='notification_settings')
    op.drop_index(op.f('ix_notification_settings_id'), table_name='notification_settings')
    op.drop_table('notification_settings')
    op.drop_index(op.f('ix_notifications_user_id'), table_name='notifications')
    op.drop_index(op.f('ix_notifications_id'), table_name='notifications')
    op.drop_table('notifications')
    op.drop_index(op.f('ix_favorites_user_id'), table_name='favorites')
    op.drop_index(op.f('ix_favorites_id'), table_name='favorites')
    op.drop_table('favorites')
    op.drop_index(op.f('ix_users_lecturer_id'), table_name='users')
    op.drop_index(op.f('ix_users_group_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_groups_faculty_id'), table_name='groups')
    op.drop_constraint('fk_groups_faculty_id', 'groups', type_='foreignkey')
    op.drop_column('groups', 'faculty_id')
    op.drop_index(op.f('ix_faculties_name'), table_name='faculties')
    op.drop_index(op.f('ix_faculties_id'), table_name='faculties')
    op.drop_table('faculties')
    op.execute("DROP TYPE IF EXISTS userrole")
    op.execute("DROP TYPE IF EXISTS notificationtype")

