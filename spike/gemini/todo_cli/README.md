# TODO CLI Application

A simple, robust command-line interface (CLI) for managing your TODO tasks. Built with Python, Typer, and Pydantic.

## Features

- **Add Tasks**: Create new tasks with title, priority, due date, and category.
- **List Tasks**: View your tasks, filtered by category or sorted by priority/due date.
- **Edit Tasks**: Update existing tasks.
- **Complete Tasks**: Mark tasks as done.
- **Delete Tasks**: Remove tasks you no longer need.
- **Search**: Find tasks by keyword.
- **Data Persistence**: Tasks are saved to a local JSON file (`tasks.json`).

## Installation

### Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/) (recommended for dependency management)

### Setup

1. Clone the repository (if applicable) or navigate to the project directory.

2. Install dependencies using Poetry:

   ```bash
   poetry install
   ```

## Usage

You can run the application using `poetry run todo`.

### Commands

#### Add a Task
Add a new task. Priority is 1 (high) to 5 (low). Default is 3.

```bash
poetry run todo add "Buy milk" --priority 1 --category shopping
poetry run todo add "Finish report" --due-date 2026-03-01
```

#### List Tasks
List all tasks. You can filter by category or sort.

```bash
# List all
poetry run todo list

# Filter by category
poetry run todo list --category shopping

# Sort by priority (High to Low)
poetry run todo list --sort-by priority

# Sort by due date (Soonest first)
poetry run todo list --sort-by due-date
```

#### Edit a Task
Edit an existing task by ID.

```bash
poetry run todo edit 1 --title "Buy almond milk" --priority 2
```

#### Complete a Task
Mark a task as completed.

```bash
poetry run todo complete 1
```

#### Delete a Task
Delete a task by ID.

```bash
poetry run todo delete 1
```

#### Search Tasks
Search for tasks containing a keyword in the title.

```bash
poetry run todo search "milk"
```

## Testing

Run the test suite to ensure everything is working correctly:

```bash
poetry run pytest
```