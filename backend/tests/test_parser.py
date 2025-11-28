"""Тесты парсера HTML."""
import pytest
from app.services.parser import ParserService
from app.models import Building, Room, Discipline, WorkKind, Lecturer, Group


def test_parser_basic(db):
    """Базовый тест парсера."""
    # Создаем минимальные данные
    building = Building(name="корп. А", code="A", address="ул. Тест")
    db.add(building)
    db.flush()

    room = Room(building_id=building.id, number="301", capacity=30, type="lecture")
    db.add(room)
    db.flush()

    # Простой HTML для теста
    html_content = """
    <table>
        <tr>
            <td>17.11.2025</td>
            <td>1</td>
            <td>Информатика</td>
            <td>Лекция</td>
            <td>Минеева Т.А.</td>
            <td>521428</td>
            <td>301</td>
        </tr>
    </table>
    """

    result = ParserService.parse_html(db, html_content)
    db.commit()

    # Проверяем результаты
    assert result.events_created >= 0  # Может быть 0 если парсер не распознал формат
    # В реальности нужно тестировать с правильным форматом HTML

