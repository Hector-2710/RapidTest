"""
RapidTest CLI - Command line interface for RapidTest

Usage:
    rapidtest [options]
"""

import argparse
import sys
from pathlib import Path

INIT_TEMPLATE = '''
from rapidtest import Test, StatusCode, data

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
        json={"name": "test", "email": data.generate_email()},
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
    filename = f"{project_name}.py"

    output_path = Path(filename)

    if output_path.exists():
        print(f"Error: {output_path} already exists.")
        return 1

    content = INIT_TEMPLATE
    output_path.write_text(content)

    print(f"Created: {output_path}")

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="rapidtest")
    subparsers = parser.add_subparsers(dest="command")

    sc = subparsers.add_parser("init", help="Initialize a new RapidTest project")
    sc.set_defaults(func=init_command)

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
