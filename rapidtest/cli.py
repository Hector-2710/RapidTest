"""
RapidTest CLI - Command line interface for RapidTest

Usage:
    rapidtest [options]
"""

import argparse
import importlib
import importlib.util
import sys
from pathlib import Path

INIT_TEMPLATE = '''
from rapidtest import HTTPTest, ASGITest, StatusCode, Data

api = HTTPTest(url="http://localhost:8000")

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

# HTTP methods to include in generated tests (exclude HEAD, OPTIONS)
VALID_HTTP_METHODS = frozenset({"GET", "POST", "PUT", "PATCH", "DELETE"})

# Default status codes for each HTTP method
DEFAULT_STATUS_CODES = {
    "GET": "StatusCode.OK_200",
    "POST": "StatusCode.CREATED_201",
    "PUT": "StatusCode.OK_200",
    "PATCH": "StatusCode.OK_200",
    "DELETE": "StatusCode.NO_CONTENT_204",
}


def _get_status_code_str(method: str) -> str:
    """Get the status code string for a given HTTP method."""
    return DEFAULT_STATUS_CODES.get(method, "StatusCode.OK_200")


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

    cwd = Path.cwd()
    sys.path.insert(0, str(cwd))

    backend_dir = cwd / "backend"
    if backend_dir.exists():
        sys.path.insert(0, str(backend_dir))

    test_dir = cwd / "test"
    if test_dir.exists():
        sys.path.insert(0, str(test_dir))

    test_files = sorted(tests_dir.glob("test*.py"))

    if not test_files:
        print(
            "No se encontró ningún archivo que empiece con 'test' en la carpeta 'tests'."
        )
        return 1

    for test_file in test_files:
        print(f"📂 {test_file.name}", flush=True)
        try:
            spec = importlib.util.spec_from_file_location("test_module", test_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except Exception as e:
            print(f"❌ Error en {test_file.name}: {e}", flush=True)
            return 1

    return 0


def _parse_app_arg(app_arg: str) -> tuple[str, str] | None:
    """Parse the app argument in the format 'module:app_name'.

    Args:
        app_arg: The argument in format "module:app_name" (e.g., "main:app")

    Returns:
        A tuple of (module_name, app_name) or None if invalid format.
    """
    if ":" not in app_arg:
        return None
    parts = app_arg.split(":", 1)
    if len(parts) != 2 or not parts[0] or not parts[1]:
        return None
    return parts[0], parts[1]


def _inspect_routes(app) -> list[tuple[str, str, list[str]]]:
    """Inspect routes from a FastAPI/Starlette application.

    Args:
        app: The FastAPI or Starlette application instance.

    Returns:
        A list of tuples containing (path, method, methods_list) for each route.
    """
    routes = []

    if not hasattr(app, "routes"):
        return routes

    for route in app.routes:
        # Skip non-HTTP routes (WebSockets, Mounts, etc.)
        if not hasattr(route, "methods"):
            continue

        # Get the path
        path = getattr(route, "path", "")
        if not path:
            continue

        # Filter to only valid HTTP methods (exclude HEAD, OPTIONS)
        methods = getattr(route, "methods", set())
        valid_methods = [m for m in methods if m in VALID_HTTP_METHODS]

        if not valid_methods:
            continue

        for method in sorted(valid_methods):
            routes.append((path, method, list(methods)))

    return routes


def _generate_test_calls(
    module_name: str, app_name: str, routes: list[tuple[str, str, list[str]]]
) -> str:
    """Generate the test file content.

    Args:
        module_name: The name of the module containing the app.
        app_name: The name of the app variable.
        routes: List of route tuples (path, method, all_methods).

    Returns:
        The generated test file content as a string.
    """
    lines = [
        '"""Auto-generated ASGI tests from scan command."""',
        "",
        "from rapidtest import ASGITest, StatusCode",
        f"from {module_name} import {app_name}",
        "",
        f"api = ASGITest(app={app_name})",
        "",
    ]

    for path, method, _ in routes:
        comment = f"# Auto-generated test for {method} {path}"
        lines.append(comment)
        lines.append(
            "# TODO: Review and update expected response, headers, and body as needed"
        )
        status_str = _get_status_code_str(method)
        lines.append(f'api.{method.lower()}(path="{path}", status={status_str})')
        lines.append("")

    return "\n".join(lines)


def _get_unique_filename(base_name: Path) -> Path:
    """Get a unique filename by adding a numeric suffix if file exists.

    Args:
        base_name: The desired file path.

    Returns:
        A unique file path with numeric suffix if needed.
    """
    if not base_name.exists():
        return base_name

    stem = base_name.stem
    suffix = base_name.suffix
    parent = base_name.parent

    counter = 1
    while True:
        new_name = parent / f"{stem}_{counter}{suffix}"
        if not new_name.exists():
            return new_name
        counter += 1


def scan_command(args) -> int:
    """Scan a FastAPI/Starlette app and generate ASGI tests.

    Args:
        args: Command line arguments containing 'app' in format 'module:app_name'.

    Returns:
        Exit code (0 for success, 1 for error).
    """
    # Parse the app argument
    parsed = _parse_app_arg(args.app)
    if parsed is None:
        print(
            f"Error: Invalid format for app argument. Expected 'module:app_name', got '{args.app}'"
        )
        return 1

    module_name, app_name = parsed

    # Add current directory to sys.path for imports
    cwd = Path.cwd()
    sys.path.insert(0, str(cwd))

    # Also check for common project structures
    for subdir in ["backend", "app", "api"]:
        subdir_path = cwd / subdir
        if subdir_path.exists() and str(subdir_path) not in sys.path:
            sys.path.insert(0, str(subdir_path))

    # Import the module dynamically
    try:
        module = importlib.import_module(module_name)
        app = getattr(module, app_name)
    except ImportError as e:
        print(f"Error: Could not import module '{module_name}'.")
        print(f"  Make sure the module exists and any dependencies are installed.")
        print(f"  Original error: {e}")
        return 1
    except AttributeError:
        print(f"Error: Module '{module_name}' does not have an attribute '{app_name}'.")
        print(
            f"  Available attributes: {[a for a in dir(module) if not a.startswith('_')]}"
        )
        return 1

    # Inspect routes
    routes = _inspect_routes(app)

    if not routes:
        print("No HTTP routes found in the application.")
        return 1

    print(f"Found {len(routes)} route(s) in {module_name}:{app_name}")
    for path, method, _ in routes:
        print(f"  {method:7} {path}")

    # Generate test file
    test_content = _generate_test_calls(module_name, app_name, routes)

    # Create tests directory if it doesn't exist
    tests_dir = cwd / "tests"
    tests_dir.mkdir(exist_ok=True)

    # Get unique filename
    base_filename = tests_dir / "test_asgi_auto.py"
    filename = _get_unique_filename(base_filename)

    # Write the file
    filename.write_text(test_content)

    print(f"\nGenerated test file: {filename}")
    print("Review and customize the generated tests as needed.")

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="rapidtest")
    subparsers = parser.add_subparsers(dest="command")

    sc = subparsers.add_parser("init", help="Initialize a new RapidTest project")
    sc.set_defaults(func=init_command)

    sr = subparsers.add_parser("run", help="Run RapidTest files from tests directory")
    sr.set_defaults(func=run_command)

    ss = subparsers.add_parser(
        "scan", help="Scan a FastAPI/Starlette app and generate ASGI tests"
    )
    ss.add_argument("app", help="App to scan in the format module:app (e.g., main:app)")
    ss.set_defaults(func=scan_command)

    parser.add_argument(
        "-v", "--version", action="version", version="RapidTest CLI 0.7.0"
    )

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 0

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
