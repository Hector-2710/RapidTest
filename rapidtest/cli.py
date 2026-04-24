"""
RapidTest CLI - Command line interface for RapidTest.

Usage:
    rapidtest [options]
    rapidtest run [--dir DIR] [--pattern PATTERN] [--fail-fast] [--dry-run]
    rapidtest scan module:app [--output FILE] [--format {text,json}] [--dry-run]
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

from .scanner import ScanError, scan_app


def run_command(args) -> int:
    """Run RapidTest files from the tests directory.

    Args:
        args: Command line arguments.

    Returns:
        Exit code (0 for success, 1 for error).
    """
    # Determine test directory
    tests_dir = Path(args.dir) if args.dir else Path("tests")

    if not tests_dir.exists():
        print(f"No se encontró la carpeta '{tests_dir}'.")
        return 1

    cwd = Path.cwd()
    sys.path.insert(0, str(cwd))

    backend_dir = cwd / "backend"
    if backend_dir.exists():
        sys.path.insert(0, str(backend_dir))

    test_dir = cwd / "test"
    if test_dir.exists():
        sys.path.insert(0, str(test_dir))

    # Determine pattern
    pattern = args.pattern
    test_files = sorted(tests_dir.glob(pattern))

    if not test_files:
        print(
            f"No se encontró ningún archivo que coincida con el patrón '{pattern}' en la carpeta '{tests_dir}'."
        )
        return 1

    # If dry-run, just list files and exit
    if args.dry_run:
        for test_file in test_files:
            print(f"📂 {test_file.name}")
        return 0

    # Run tests
    error_occurred = False
    for test_file in test_files:
        print(f"📂 {test_file.name}", flush=True)
        try:
            spec = importlib.util.spec_from_file_location("test_module", test_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except Exception as e:
            print(f"❌ Error en {test_file.name}: {e}", flush=True)
            error_occurred = True
            if args.fail_fast:
                return 1

    return 1 if error_occurred else 0


def scan_command(args) -> int:
    """Scan a FastAPI/Starlette app and generate ASGI tests.

    Args:
        args: Command line arguments containing 'app' in format 'module:app_name'.

    Returns:
        Exit code (0 for success, 1 for error).
    """
    app_string = args.app
    # Determine output directory
    if args.output:
        output_path = Path(args.output)
        output_dir = output_path.parent
        # Ensure parent directory exists
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = Path.cwd() / "tests"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = None  # Will be determined by scan_app

    try:
        if args.dry_run:
            # In dry-run mode, we just show what would be done without writing
            # We need to inspect the app and generate content but not write file.
            # For simplicity, we can call scan_app with a dummy directory and then discard.
            # However, scan_app writes file; we could modify scan_app to support dry_run.
            # Since we cannot change scanner.py (out of scope?), we'll simulate by checking
            # if the app can be loaded and routes inspected, but not write.
            # For now, we'll just print the intended output path.
            if output_path is None:
                # We need to generate a default filename similar to scan_app logic
                # We'll reuse the logic from scanner.get_unique_file_path but we don't want to import.
                # Simpler: just indicate the directory and that a file would be generated.
                print(f"Dry run: Would scan {app_string} and generate a test file in {output_dir}/")
            else:
                print(f"Dry run: Would scan {app_string} and generate test file: {output_path}")
            return 0

        # Normal mode
        filename = scan_app(app_string, output_dir)

        # If user specified output path, we need to rename the generated file to that path
        if output_path is not None and output_path != filename:
            # Ensure the target directory exists (already done)
            filename.replace(output_path)
            filename = output_path

        # Print success message
        if args.format == "json":
            import json
            result = {
                "status": "success",
                "app": app_string,
                "test_file": str(filename),
                "message": "Review and customize the generated tests as needed."
            }
            print(json.dumps(result))
        else:
            print(f"Generated test file: {filename}")
            print("Review and customize the generated tests as needed.")

        return 0

    except ScanError as e:
        if args.format == "json":
            import json
            result = {
                "status": "error",
                "app": app_string,
                "error": str(e),
                "details": e.details if e.details else None
            }
            print(json.dumps(result))
        else:
            print(f"Error: {e}")
            if e.details:
                print(f"  {e.details}")
        return 1


def main() -> int:
    """Main entry point for the CLI.

    Returns:
        Exit code.
    """
    parser = argparse.ArgumentParser(prog="rapidtest")
    subparsers = parser.add_subparsers(dest="command")

    sr = subparsers.add_parser("run", help="Run RapidTest files from tests directory")
    sr.add_argument(
        "--dir",
        help="Directory to look for test files (default: tests)",
    )
    sr.add_argument(
        "--pattern",
        default="test*.py",
        help="Pattern to match test files (default: test*.py)",
    )
    sr.add_argument(
        "--fail-fast",
        action="store_true",
        help="Stop on first test error",
    )
    sr.add_argument(
        "--dry-run",
        action="store_true",
        help="List test files without running them",
    )
    sr.set_defaults(func=run_command)

    ss = subparsers.add_parser(
        "scan", help="Scan a FastAPI/Starlette app and generate ASGI tests"
    )
    ss.add_argument("app", help="App to scan in the format module:app (e.g., main:app)")
    ss.add_argument(
        "--output",
        help="Output file path for the generated test (default: tests/<generated_name>.py)",
    )
    ss.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )
    ss.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without writing files",
    )
    ss.set_defaults(func=scan_command)

    parser.add_argument(
        "-v", "--version", action="version", version="RapidTest CLI 0.9.0"
    )

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 0

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
