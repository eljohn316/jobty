# `jobty`

A simple CLI for tracking all your job applications.

## Motivation

While there are plenty of existing job application trackers out there, most of them require creating an account, signing up for yet another service, and navigating a heavy web interface. As a developer who uses the terminal a lot, I just want something I could use instantly with simple commands, no onboarding, no locked-in platforms, just my data under my control. This CLI tool lets me log, update, and see my applications with simple commands.

## Getting started

### Installing

```console
$ pip install jobty
```

### Documentation

**Usage**:

```console
$ jobty [OPTIONS] COMMAND [ARGS]...
```

**Options**:

- `--install-completion`: Install completion for the current shell.
- `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
- `--help`: Show this message and exit.

**Commands**:

- `list`: List all job application entries or a single job application entry if job id is provided.
- `add`: Add job application entry.
- `update`: Update an existing job application entry.
- `delete`: Delete an existing job application entry.

### `jobty list`

List all job application entries or a single job application entry if job id is provided.

**Usage**:

```console
$ jobty list [OPTIONS] [job_id]
```

**Arguments**:

- `[job_id]`: The ID of the Job to list

**Options**:

- `--status [Applied|Interview|Hired|Rejected]`: Filter by status
- `--work-arrangement [Onsite|Hybrid|Remote]`: Filter by work arrangement
- `--help`: Show this message and exit.

### `jobty add`

Add job application entry.

**Usage**:

```console
$ jobty add [OPTIONS]
```

**Options**:

- `--role TEXT`: Job role [required]
- `--company TEXT`: Company name [required]
- `--location TEXT`: Location [required]
- `--work-arrangement [Onsite|Hybrid|Remote]`: Work arrangement [required]
- `--status [Applied|Interview|Hired|Rejected]`: Application status [default: Applied]
- `--source-link TEXT`: Source link
- `--interview-date [%m-%d-%Y]`: Interview date
- `--interview-time [%I:%M %p]`: Interview time
- `--help`: Show this message and exit.

### `jobty update`

Update an existing job application entry.

**Usage**:

```console
$ jobty update [OPTIONS] job_id
```

**Arguments**:

- `job_id`: The ID of the Job to update [required]

**Options**:

- `--role TEXT`: Job role
- `--company TEXT`: Company name
- `--location TEXT`: Location
- `--work-arrangement [Onsite|Hybrid|Remote]`: Work arrangement
- `--status [Applied|Interview|Hired|Rejected]`: Application status
- `--source-link TEXT`: Source link
- `--interview-date [%m-%d-%Y]`: Interview date
- `--interview-time [%I:%M %p]`: Interview time
- `--help`: Show this message and exit.

### `jobty delete`

Delete an existing job application entry.

**Usage**:

```console
$ jobty delete [OPTIONS] job_id
```

**Arguments**:

- `job_id`: The ID of the Job to delete [required]

**Options**:

- `--help`: Show this message and exit.
