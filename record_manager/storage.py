
"""Safe loading and saving of student records in JSON."""

import json
import os
from pathlib import Path
from typing import Any

from record_manager.operations import Student


def _validate_records(data: Any) -> list[Student]:
    """Validate the JSON structure and student records."""
    if not isinstance(data, list):
        raise ValueError("JSON must contain a list of student records.")

    records: list[Student] = []
    seen_ids: set[str] = set()

    for item in data:
        if not isinstance(item, dict):
            raise ValueError("Each student record must be a JSON object.")

        if set(item.keys()) != {"id", "name"}:
            raise ValueError(
                "Each record must contain only 'id' and 'name'."
            )

        student_id = item["id"]
        name = item["name"]

        if not isinstance(student_id, str) or not student_id.strip():
            raise ValueError("Every student must have a valid ID.")

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Every student must have a valid name.")

        if student_id != student_id.strip() or name != name.strip():
            raise ValueError(
                "Student IDs and names must not have outer spaces."
            )

        if student_id in seen_ids:
            raise ValueError(
                f"Duplicate student ID '{student_id}' in JSON."
            )

        seen_ids.add(student_id)
        records.append({"id": student_id, "name": name})

    return records


def load_students(file_path: str | Path) -> list[Student]:
    """Load student records without modifying the source file."""
    path = Path(file_path)

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON in '{path}'. The file was not changed."
        ) from error

    return _validate_records(data)


def save_students(
    file_path: str | Path, students: list[Student]
) -> None:
    """Validate and safely save records using a temporary file."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    validated = _validate_records(students)

    # Do not overwrite an existing file if its contents are invalid.
    if path.exists():
        load_students(path)

    temporary_path = path.with_name(path.name + ".tmp")

    try:
        with temporary_path.open("w", encoding="utf-8") as file:
            json.dump(validated, file, indent=2, ensure_ascii=False)
            file.write("\n")
            file.flush()
            os.fsync(file.fileno())

        os.replace(temporary_path, path)

    finally:
        if temporary_path.exists():
            temporary_path.unlink()
