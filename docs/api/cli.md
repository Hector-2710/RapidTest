# RapidTest CLI

RapidTest includes a command-line interface to bootstrap a test file quickly.

```bash
rapidtest --help
```

## Command: init

Creates a starter Python test file in your current directory.

```bash
rapidtest init
```

Then the CLI asks for a project name and writes <name>.py with starter tests.

## What gets generated

The generated file includes examples using:

- `Test` for functional API tests
- `StatusCode` enum values
- `data` helpers for fake test data

## Example workflow

```bash
mkdir my-api-tests
cd my-api-tests
rapidtest init
python my_tests.py
```

## Notes

- If the output file already exists, the command stops and prints an error.
- The generated template is a starting point; adjust URLs, paths, and payloads for your API.
