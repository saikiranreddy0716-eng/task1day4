
"""Tests for safe JSON loading and saving."""

import json

import pytest

from record_manager.storage import load_students, save_students


def test_missing_file_returns_empty_list(tmp_path):
    path = tmp_path / "students.json"

    assert load_students(path) == []
    assert not path.exists()


def test_save_and_load_students(tmp_path):
    path = tmp_path / "students.json"
    students = [
        {"id": "101", "name": "Ravi"},
        {"id": "102", "name": "Priya"},
    ]

    save_students(path, students)

    assert load_students(path) == students


def test_empty_file_is_not_silently_accepted(tmp_path):
    path = tmp_path / "students.json"
    path.write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid JSON"):
        load_students(path)

    assert path.read_text(encoding="utf-8") == ""


def test_malformed_json_is_not_overwritten(tmp_path):
    path = tmp_path / "students.json"
    original_content = '{"id": "101", broken JSON'

    path.write_text(original_content, encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid JSON"):
        load_students(path)

    assert path.read_text(encoding="utf-8") == original_content


def test_wrong_json_structure_is_rejected(tmp_path):
    path = tmp_path / "students.json"
    path.write_text('{"id": "101", "name": "Ravi"}', encoding="utf-8")

    with pytest.raises(ValueError, match="must contain a list"):
        load_students(path)


def test_duplicate_ids_in_json_are_rejected(tmp_path):
    path = tmp_path / "students.json"
    data = [
        {"id": "101", "name": "Ravi"},
        {"id": "101", "name": "Priya"},
    ]
    path.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ValueError, match="Duplicate student ID"):
        load_students(path)


def test_invalid_data_does_not_replace_existing_file(tmp_path):
    path = tmp_path / "students.json"
    original_content = '[{"id": "101", "name": "Ravi"}]'
    path.write_text(original_content, encoding="utf-8")

    with pytest.raises(ValueError):
        save_students(path, [{"id": "", "name": "Invalid"}])

    assert path.read_text(encoding="utf-8") == original_content


def test_saved_file_contains_readable_json(tmp_path):
    path = tmp_path / "students.json"
    save_students(path, [{"id": "101", "name": "Ravi"}])

    data = json.loads(path.read_text(encoding="utf-8"))

    assert data[0]["id"] == "101"
    assert data[0]["name"] == "Ravi"
