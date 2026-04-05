# Jobty

A simple command-line application to track your job applications.

This project helps you manage every job application in one place with commands for listing, adding, updating, and deleting job application entries. I originally created this project for myself to keep track of my job applications.

## What this project is

`jobty` is a Python CLI app built to track job applications you submit.
It stores application details locally and provides a quick interface to:

- add new job application entry
- view all saved application entries
- inspect a single job application entry
- update a single job application entry
- delete a single job application entry

## Requirements

- Python 3.13 or newer
- `pydantic`
- `questionary`
- `typer`

## How to clone and run it

> [!IMPORTANT]  
> You must already have [uv](https://docs.astral.sh/uv/) installed on your machine. If not, you can check out the documentation [here](https://docs.astral.sh/uv/getting-started/installation/).

1. Clone the repository:

```bash
git clone https://github.com/eljohn316/jobty.git
cd jobty
```

2. Create and activate a virtual environment with uv:

```bash
uv venv .venv
source .venv/bin/activate
```

3. Installation

```bash
uv sync
```

## Example commands

- List all job applications entries:

```bash
jobty list
```

- View a single application by ID:

```bash
jobty list-one <job_id>
```

- Add a new application:

```bash
jobty add
```

- Update an existing application:

```bash
jobty update <job_id>
```

- Delete an application:

```bash
jobty delete <job_id>
```

## Notes

When run, the CLI initializes the local job applications storage automatically, so you can start adding applications right away.
