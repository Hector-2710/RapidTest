"""
RapidTest Scanner - Logic for scanning ASGI applications and generating test code.

This module contains the business logic for:
- Parsing application import strings
- Inspecting routes from FastAPI/Starlette applications
- Generating test file content
- Managing unique file paths
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path


class ScanError(Exception):
    """Custom exception for scan-related errors."""

    def __init__(self, message: str, details: str | None = None) -> None:
        super().__init__(message)
        self.details = details


# HTTP methods to include in generated tests (exclude HEAD, OPTIONS)
VALID_HTTP_METHODS = frozenset({"GET", "POST", "PUT", "PATCH", "DELETE"})

# Default status codes for each HTTP method
DEFAULT_STATUS_CODES: dict[str, str] = {
    "GET": "StatusCode.OK_200",
    "POST": "StatusCode.CREATED_201",
    "PUT": "StatusCode.OK_200",
    "PATCH": "StatusCode.OK_200",
    "DELETE": "StatusCode.NO_CONTENT_204",
}


def get_status_code_for_method(method: str) -> str:
    """Get the status code string for a given HTTP method.

    Args:
        method: The HTTP method (e.g., "GET", "POST").

    Returns:
        The status code string for the method.
    """
    return DEFAULT_STATUS_CODES.get(method, "StatusCode.OK_200")


def parse_app_import_string(app_str: str) -> tuple[str, str]:
    """Parse an app import string in the format 'module:app_name'.

    Args:
        app_str: The string in format "module:app_name" (e.g., "main:app").

    Returns:
        A tuple of (module_name, app_name).

    Raises:
        ScanError: If the format is invalid.
    """
    if ":" not in app_str:
        raise ScanError(
            f"Invalid format for app argument. Expected 'module:app_name', got '{app_str}'",
            details="The app string must contain a colon (:) separating the module and app name.",
        )

    parts = app_str.split(":", 1)
    if len(parts) != 2 or not parts[0] or not parts[1]:
        raise ScanError(
            f"Invalid format for app argument. Expected 'module:app_name', got '{app_str}'",
            details="Both module name and app name must be non-empty.",
        )

    return parts[0], parts[1]


def inspect_asgi_routes(app: object) -> list[tuple[str, str, list[str]]]:
    """Inspect routes from a FastAPI/Starlette application.

    Args:
        app: The FastAPI or Starlette application instance.

    Returns:
        A list of tuples containing (path, method, all_methods_list) for each route.

    Example:
        >>> routes = inspect_asgi_routes(my_app)
        >>> for path, method, all_methods in routes:
        ...     print(f"{method} {path}")
    """
    routes: list[tuple[str, str, list[str]]] = []

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


def generate_test_file_content(
    module_name: str,
    app_name: str,
    routes: list[tuple[str, str, list[str]]],
) -> str:
    """Generate the test file content from scanned routes.

    Args:
        module_name: The name of the module containing the app.
        app_name: The name of the app variable.
        routes: List of route tuples (path, method, all_methods).

    Returns:
        The generated test file content as a string.

    Example:
        >>> content = generate_test_file_content("main", "app", [("/health", "GET", ["GET"])])
        >>> print(content)
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
        status_str = get_status_code_for_method(method)
        lines.append(f'api.{method.lower()}(path="{path}", status={status_str})')
        lines.append("")

    return "\n".join(lines)


def get_unique_file_path(base_path: Path) -> Path:
    """Get a unique filename by adding a numeric suffix if file exists.

    Args:
        base_path: The desired file path.

    Returns:
        A unique file path with numeric suffix if needed.

    Example:
        >>> get_unique_file_path(Path("tests/test_auto.py"))
        Path("tests/test_auto.py")  # if doesn't exist
        Path("tests/test_auto_1.py")  # if test_auto.py exists
    """
    if not base_path.exists():
        return base_path

    stem = base_path.stem
    suffix = base_path.suffix
    parent = base_path.parent

    counter = 1
    while True:
        new_name = parent / f"{stem}_{counter}{suffix}"
        if not new_name.exists():
            return new_name
        counter += 1


def _load_app_from_string(app_string: str) -> object:
    """Load an ASGI app from a module:app_name string.

    Args:
        app_string: The string in format "module:app_name".

    Returns:
        The loaded application instance.

    Raises:
        ScanError: If the module cannot be imported or app attribute not found.
    """
    module_name, app_name = parse_app_import_string(app_string)

    # Add current directory to sys.path for imports
    cwd = Path.cwd()
    if str(cwd) not in sys.path:
        sys.path.insert(0, str(cwd))

    # Also check for common project structures
    for subdir in ["backend", "app", "api"]:
        subdir_path = cwd / subdir
        if subdir_path.exists() and str(subdir_path) not in sys.path:
            sys.path.insert(0, str(subdir_path))

    # Import the module dynamically
    try:
        module = importlib.import_module(module_name)
    except ImportError as e:
        raise ScanError(
            f"Could not import module '{module_name}'.",
            details="Make sure the module exists and any dependencies are installed.",
        ) from e

    try:
        app = getattr(module, app_name)
    except AttributeError:
        available = [a for a in dir(module) if not a.startswith("_")]
        raise ScanError(
            f"Module '{module_name}' does not have an attribute '{app_name}'.",
            details=f"Available attributes: {available}",
        ) from None

    return app


def scan_app(app_string: str, output_dir: Path | str | None = None) -> Path:
    """Scan an ASGI application and generate test file.

    This is the main orchestrator function that:
    1. Parses the app import string
    2. Loads the application
    3. Inspects routes
    4. Generates test file content
    5. Writes the test file

    Args:
        app_string: The string in format "module:app_name" (e.g., "main:app").
        output_dir: Directory to write the test file. Defaults to "tests" in cwd.

    Returns:
        Path to the generated test file.

    Raises:
        ScanError: If any step in the scanning process fails.

    Example:
        >>> from pathlib import Path
        >>> test_file = scan_app("main:app", Path("tests"))
        >>> print(f"Generated: {test_file}")
    """
    if output_dir is None:
        output_dir = Path.cwd() / "tests"
    elif isinstance(output_dir, str):
        output_dir = Path(output_dir)

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load the application
    app = _load_app_from_string(app_string)

    # Inspect routes
    routes = inspect_asgi_routes(app)

    if not routes:
        raise ScanError(
            "No HTTP routes found in the application.",
            details="Make sure the app is a FastAPI or Starlette application with defined routes.",
        )

    # Parse app_string to get module and app names for generation
    module_name, app_name = parse_app_import_string(app_string)

    # Generate test content
    test_content = generate_test_file_content(module_name, app_name, routes)

    # Generate unique filename
    base_filename = output_dir / "test_asgi_auto.py"
    filename = get_unique_file_path(base_filename)

    # Write the file
    filename.write_text(test_content)

    return filename
