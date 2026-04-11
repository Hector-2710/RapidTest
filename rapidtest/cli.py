"""
RapidTest CLI - Command line interface for RapidTest

Usage:
    rapidtest [options]
"""

import argparse
import importlib.util
import os
import sys
from pathlib import Path

INIT_TEMPLATE = '''
from rapidtest import Test, StatusCode, Data

api = Test(url="http://localhost:8000")

def test_example():
    """Example test demonstrating RapidTest usage."""
    response = api.get(
        path="/health",
        status=StatusCode.OK_200,
        keys=["message"]
    )

def test_post_example():
    """Example POST request with JSON body."""
    response = api.post(
        path="/users",
        json={"name": "test", "email": Data.generate_email()},
        status=StatusCode.CREATED_201,
        keys=["id"]
    )

def test_with_auth():
    """Example request with authentication headers."""
    response = api.post(
        path="/token",
        data={"username": "user", "password": "pass"},
        status=StatusCode.OK_200,
        keys=["access_token"]
    )
'''


def init_command(args) -> int:

    project_name = (
        input("Name of project: (default my_api_tests): ").strip() or "my_tests"
    )

    tests_dir = Path("tests")
    tests_dir.mkdir(exist_ok=True)

    filename = tests_dir / f"{project_name}.py"

    if filename.exists():
        print(f"Error: {filename} already exists.")
        return 1

    content = INIT_TEMPLATE
    filename.write_text(content)

    print(f"Created: {filename}")

    return 0


def run_command(args) -> int:
    tests_dir = Path("tests")

    if not tests_dir.exists():
        print("No se encontró la carpeta 'tests'.")
        return 1

    test_files = sorted(tests_dir.glob("test*.py"))

    if not test_files:
        print(
            "No se encontró ningún archivo que empiece con 'test' en la carpeta 'tests'."
        )
        return 1

    sys.path.insert(0, str(Path.cwd()))

    for test_file in test_files:
        print(f"Ejecutando: {test_file.name}")
        spec = importlib.util.spec_from_file_location("test_module", test_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

    print("Ejecución completada.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="rapidtest")
    subparsers = parser.add_subparsers(dest="command")

    sc = subparsers.add_parser("init", help="Initialize a new RapidTest project")
    sc.set_defaults(func=init_command)

    sr = subparsers.add_parser("run", help="Run RapidTest files from tests directory")
    sr.set_defaults(func=run_command)

    parser.add_argument(
        "-v", "--version", action="version", version="RapidTest CLI 0.1.0"
    )

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 0

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
