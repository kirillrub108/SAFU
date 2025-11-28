"""Initial migration

Revision ID: 001_initial
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Buildings
    op.create_table(
        'buildings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('code', sa.String(), nullable=True),
        sa.Column('address', sa.String(), nullable=False),
        sa.Column('lat', sa.Float(), nullable=True),
        sa.Column('lon', sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_buildings_id'), 'buildings', ['id'], unique=False)
    op.create_index(op.f('ix_buildings_name'), 'buildings', ['name'], unique=False)
    op.create_index(op.f('ix_buildings_code'), 'buildings', ['code'], unique=True)

    # Rooms
    op.create_table(
        'rooms',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('building_id', sa.Integer(), nullable=False),
        sa.Column('number', sa.String(), nullable=False),
        sa.Column('capacity', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('features', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['building_id'], ['buildings.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_rooms_id'), 'rooms', ['id'], unique=False)
    op.create_index(op.f('ix_rooms_building_id'), 'rooms', ['building_id'], unique=False)
    op.create_index(op.f('ix_rooms_number'), 'rooms', ['number'], unique=False)

    # Lecturers
    op.create_table(
        'lecturers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('fio', sa.String(), nullable=False),
        sa.Column('chair', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('phone', sa.String(), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_lecturers_id'), 'lecturers', ['id'], unique=False)
    op.create_index(op.f('ix_lecturers_fio'), 'lecturers', ['fio'], unique=False)

    # Groups
    op.create_table(
        'groups',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('year', sa.Integer(), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code')
    )
    op.create_index(op.f('ix_groups_id'), 'groups', ['id'], unique=False)
    op.create_index(op.f('ix_groups_code'), 'groups', ['code'], unique=True)

    # Subgroups
    op.create_table(
        'subgroups',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('group_id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_subgroups_id'), 'subgroups', ['id'], unique=False)
    op.create_index(op.f('ix_subgroups_group_id'), 'subgroups', ['group_id'], unique=False)
    op.create_index(op.f('ix_subgroups_code'), 'subgroups', ['code'], unique=False)

    # Streams
    op.create_table(
        'streams',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_streams_id'), 'streams', ['id'], unique=False)
    op.create_index(op.f('ix_streams_name'), 'streams', ['name'], unique=False)

    # Stream Members
    op.create_table(
        'stream_members',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('stream_id', sa.Integer(), nullable=False),
        sa.Column('group_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['stream_id'], ['streams.id'], ),
        sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('stream_id', 'group_id')
    )
    op.create_index(op.f('ix_stream_members_id'), 'stream_members', ['id'], unique=False)
    op.create_index(op.f('ix_stream_members_stream_id'), 'stream_members', ['stream_id'], unique=False)
    op.create_index(op.f('ix_stream_members_group_id'), 'stream_members', ['group_id'], unique=False)

    # Disciplines
    op.create_table(
        'disciplines',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('short_name', sa.String(), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_disciplines_id'), 'disciplines', ['id'], unique=False)
    op.create_index(op.f('ix_disciplines_name'), 'disciplines', ['name'], unique=False)

    # Work Kinds
    op.create_table(
        'work_kinds',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('color_hex', sa.String(), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_work_kinds_id'), 'work_kinds', ['id'], unique=False)
    op.create_index(op.f('ix_work_kinds_name'), 'work_kinds', ['name'], unique=True)

    # Time Slots
    op.create_table(
        'time_slots',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('pair_number', sa.Integer(), nullable=False),
        sa.Column('time_start', sa.Time(), nullable=False),
        sa.Column('time_end', sa.Time(), nullable=False),
        sa.Column('timezone', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_time_slots_id'), 'time_slots', ['id'], unique=False)
    op.create_index(op.f('ix_time_slots_date'), 'time_slots', ['date'], unique=False)

    # Events
    op.create_table(
        'events',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('discipline_id', sa.Integer(), nullable=False),
        sa.Column('work_kind_id', sa.Integer(), nullable=False),
        sa.Column('room_id', sa.Integer(), nullable=False),
        sa.Column('time_slot_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('note', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['discipline_id'], ['disciplines.id'], ),
        sa.ForeignKeyConstraint(['work_kind_id'], ['work_kinds.id'], ),
        sa.ForeignKeyConstraint(['room_id'], ['rooms.id'], ),
        sa.ForeignKeyConstraint(['time_slot_id'], ['time_slots.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_events_id'), 'events', ['id'], unique=False)
    op.create_index(op.f('ix_events_discipline_id'), 'events', ['discipline_id'], unique=False)
    op.create_index(op.f('ix_events_work_kind_id'), 'events', ['work_kind_id'], unique=False)
    op.create_index(op.f('ix_events_room_id'), 'events', ['room_id'], unique=False)
    op.create_index(op.f('ix_events_time_slot_id'), 'events', ['time_slot_id'], unique=False)

    # Event Lecturers
    op.create_table(
        'event_lecturers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('event_id', sa.Integer(), nullable=False),
        sa.Column('lecturer_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
        sa.ForeignKeyConstraint(['lecturer_id'], ['lecturers.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('event_id', 'lecturer_id')
    )
    op.create_index(op.f('ix_event_lecturers_id'), 'event_lecturers', ['id'], unique=False)
    op.create_index(op.f('ix_event_lecturers_event_id'), 'event_lecturers', ['event_id'], unique=False)
    op.create_index(op.f('ix_event_lecturers_lecturer_id'), 'event_lecturers', ['lecturer_id'], unique=False)

    # Event Groups
    op.create_table(
        'event_groups',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('event_id', sa.Integer(), nullable=False),
        sa.Column('group_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
        sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('event_id', 'group_id')
    )
    op.create_index(op.f('ix_event_groups_id'), 'event_groups', ['id'], unique=False)
    op.create_index(op.f('ix_event_groups_event_id'), 'event_groups', ['event_id'], unique=False)
    op.create_index(op.f('ix_event_groups_group_id'), 'event_groups', ['group_id'], unique=False)

    # Event Subgroups
    op.create_table(
        'event_subgroups',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('event_id', sa.Integer(), nullable=False),
        sa.Column('subgroup_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
        sa.ForeignKeyConstraint(['subgroup_id'], ['subgroups.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('event_id', 'subgroup_id')
    )
    op.create_index(op.f('ix_event_subgroups_id'), 'event_subgroups', ['id'], unique=False)
    op.create_index(op.f('ix_event_subgroups_event_id'), 'event_subgroups', ['event_id'], unique=False)
    op.create_index(op.f('ix_event_subgroups_subgroup_id'), 'event_subgroups', ['subgroup_id'], unique=False)

    # Event Streams
    op.create_table(
        'event_streams',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('event_id', sa.Integer(), nullable=False),
        sa.Column('stream_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
        sa.ForeignKeyConstraint(['stream_id'], ['streams.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('event_id', 'stream_id')
    )
    op.create_index(op.f('ix_event_streams_id'), 'event_streams', ['id'], unique=False)
    op.create_index(op.f('ix_event_streams_event_id'), 'event_streams', ['event_id'], unique=False)
    op.create_index(op.f('ix_event_streams_stream_id'), 'event_streams', ['stream_id'], unique=False)

    # Change Log
    op.create_table(
        'change_log',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('entity', sa.String(), nullable=False),
        sa.Column('entity_id', sa.Integer(), nullable=False),
        sa.Column('actor', sa.String(), nullable=True),
        sa.Column('change_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('reason', sa.String(), nullable=True),
        sa.Column('diff_before', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('diff_after', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('source', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_change_log_id'), 'change_log', ['id'], unique=False)
    op.create_index(op.f('ix_change_log_entity'), 'change_log', ['entity'], unique=False)
    op.create_index(op.f('ix_change_log_entity_id'), 'change_log', ['entity_id'], unique=False)
    op.create_index('idx_entity_id', 'change_log', ['entity', 'entity_id'], unique=False)

    # Attachments
    op.create_table(
        'attachments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('kind', sa.String(), nullable=False),
        sa.Column('url', sa.String(), nullable=False),
        sa.Column('uploaded_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_attachments_id'), 'attachments', ['id'], unique=False)

    # Calendar Subscriptions
    op.create_table(
        'calendar_subscriptions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(), nullable=False),
        sa.Column('filter_kind', sa.Enum('GROUP', 'LECTURER', 'STREAM', name='filterkind'), nullable=False),
        sa.Column('filter_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('token')
    )
    op.create_index(op.f('ix_calendar_subscriptions_id'), 'calendar_subscriptions', ['id'], unique=False)
    op.create_index(op.f('ix_calendar_subscriptions_token'), 'calendar_subscriptions', ['token'], unique=True)
    op.create_index(op.f('ix_calendar_subscriptions_filter_kind'), 'calendar_subscriptions', ['filter_kind'], unique=False)
    op.create_index(op.f('ix_calendar_subscriptions_filter_id'), 'calendar_subscriptions', ['filter_id'], unique=False)


def downgrade() -> None:
    op.drop_table('calendar_subscriptions')
    op.drop_table('attachments')
    op.drop_table('change_log')
    op.drop_table('event_streams')
    op.drop_table('event_subgroups')
    op.drop_table('event_groups')
    op.drop_table('event_lecturers')
    op.drop_table('events')
    op.drop_table('time_slots')
    op.drop_table('work_kinds')
    op.drop_table('disciplines')
    op.drop_table('stream_members')
    op.drop_table('streams')
    op.drop_table('subgroups')
    op.drop_table('groups')
    op.drop_table('rooms')
    op.drop_table('buildings')

