
# Day 4 - Student Record Manager

## Description

A menu-driven Python application that creates, lists, searches,
and deletes student records.

Records are persisted in a local JSON file.

## Concepts covered

- Functions, modules, and type hints
- JSON file handling
- Context managers
- Input validation and exception handling
- Automated testing with pytest
- Temporary files and safe file replacement

## Requirements

- Python 3.10 or newer
- Git

## Setup

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install pytest:

```powershell
python -m pip install pytest
```

## Run the application

```powershell
python -m record_manager.cli
```

## Run the tests

```powershell
python -m pytest -v
```

## Data file

The application stores records in `students.json` at the project
root. The file is created when a record is first saved.

Missing files start with an empty record list. Empty or invalid JSON
is reported as an error and is not silently replaced.

The JSON file is excluded from Git by `.gitignore`.
