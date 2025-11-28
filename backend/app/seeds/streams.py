"""Seeds для потоков."""
from sqlalchemy.orm import Session
from app.models import Stream, StreamMember


def seed_streams(db: Session, groups: list) -> list[Stream]:
    """Заполнение потоков."""
    # Поток из групп 521423, 521424, 521425, 521427, 521428
    stream_name = "521423, 521424, 521425, 521427, 521428"
    stream = db.query(Stream).filter(Stream.name == stream_name).first()
    if not stream:
        stream = Stream(name=stream_name, active=True)
        db.add(stream)
        db.flush()

        # Добавляем группы в поток
        group_codes = ["521423", "521424", "521425", "521427", "521428"]
        for code in group_codes:
            group = next((g for g in groups if g.code == code), None)
            if group:
                member = (
                    db.query(StreamMember)
                    .filter(StreamMember.stream_id == stream.id, StreamMember.group_id == group.id)
                    .first()
                )
                if not member:
                    member = StreamMember(stream_id=stream.id, group_id=group.id)
                    db.add(member)

    db.flush()
    return [stream] if stream else []

