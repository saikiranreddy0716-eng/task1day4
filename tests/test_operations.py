
"""Tests for student record operations."""

import pytest

from record_manager.operations import (
    create_student,
    delete_student,
    list_students,
    search_student,
)


@pytest.fixture
def students():
    """Provide a fresh student list for each test."""
    return []


def test_create_student(students):
    result = create_student(students, "101", "Ravi")

    assert result == {"id": "101", "name": "Ravi"}
    assert len(students) == 1


def test_create_student_removes_outer_spaces(students):
    result = create_student(students, " 101 ", " Ravi ")

    assert result == {"id": "101", "name": "Ravi"}


@pytest.mark.parametrize(
    ("student_id", "name"),
    [
        ("", "Ravi"),
        ("101", ""),
        ("   ", "Ravi"),
        ("101", "   "),
    ],
)
def test_reject_empty_fields(students, student_id, name):
    with pytest.raises(ValueError):
        create_student(students, student_id, name)


def test_reject_duplicate_id(students):
    create_student(students, "101", "Ravi")

    with pytest.raises(ValueError, match="already exists"):
        create_student(students, "101", "Priya")

    assert len(students) == 1


def test_list_empty_records(students):
    assert list_students(students) == []


def test_search_existing_student(students):
    create_student(students, "101", "Ravi")

    assert search_student(students, "101") == {
        "id": "101",
        "name": "Ravi",
    }


def test_search_missing_student(students):
    assert search_student(students, "999") is None


def test_delete_student(students):
    create_student(students, "101", "Ravi")

    deleted = delete_student(students, "101")

    assert deleted == {"id": "101", "name": "Ravi"}
    assert students == []


def test_delete_missing_student(students):
    with pytest.raises(ValueError, match="was not found"):
        delete_student(students, "999")
