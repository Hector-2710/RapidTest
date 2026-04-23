"""
Unit tests for the RapidTest scanner module.

Tests cover:
- parse_app_import_string
- inspect_asgi_routes
- generate_test_file_content
- get_unique_file_path
- scan_app
- ScanError
"""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from rapidtest.scanner import (
    ScanError,
    generate_test_file_content,
    get_status_code_for_method,
    get_unique_file_path,
    inspect_asgi_routes,
    parse_app_import_string,
    scan_app,
    VALID_HTTP_METHODS,
    DEFAULT_STATUS_CODES,
)


class TestParseAppImportString(unittest.TestCase):
    """Tests for parse_app_import_string function."""

    def test_valid_simple_format(self):
        """Test parsing a simple module:app format."""
        module, app = parse_app_import_string("main:app")
        self.assertEqual(module, "main")
        self.assertEqual(app, "app")

    def test_valid_nested_module(self):
        """Test parsing with nested module path."""
        module, app = parse_app_import_string("api.routes:application")
        self.assertEqual(module, "api.routes")
        self.assertEqual(app, "application")

    def test_valid_dotted_app_name(self):
        """Test parsing with dotted app name."""
        module, app = parse_app_import_string("main:app.fastapi")
        self.assertEqual(module, "main")
        self.assertEqual(app, "app.fastapi")

    def test_missing_colon_raises_error(self):
        """Test that missing colon raises ScanError."""
        with self.assertRaises(ScanError) as ctx:
            parse_app_import_string("main_app")
        self.assertIn("Invalid format", str(ctx.exception))

    def test_empty_module_raises_error(self):
        """Test that empty module name raises ScanError."""
        with self.assertRaises(ScanError) as ctx:
            parse_app_import_string(":app")
        self.assertIn("Invalid format", str(ctx.exception))

    def test_empty_app_raises_error(self):
        """Test that empty app name raises ScanError."""
        with self.assertRaises(ScanError) as ctx:
            parse_app_import_string("main:")
        self.assertIn("Invalid format", str(ctx.exception))

    def test_both_empty_raises_error(self):
        """Test that both empty raises ScanError."""
        with self.assertRaises(ScanError) as ctx:
            parse_app_import_string(":")
        self.assertIn("Invalid format", str(ctx.exception))

    def test_error_has_details(self):
        """Test that error includes details."""
        with self.assertRaises(ScanError) as ctx:
            parse_app_import_string("invalid")
        self.assertIsNotNone(ctx.exception.details)


class TestGetStatusCodeForMethod(unittest.TestCase):
    """Tests for get_status_code_for_method function."""

    def test_get_status_code_for_get(self):
        """Test GET method returns OK_200."""
        result = get_status_code_for_method("GET")
        self.assertEqual(result, "StatusCode.OK_200")

    def test_get_status_code_for_post(self):
        """Test POST method returns CREATED_201."""
        result = get_status_code_for_method("POST")
        self.assertEqual(result, "StatusCode.CREATED_201")

    def test_get_status_code_for_put(self):
        """Test PUT method returns OK_200."""
        result = get_status_code_for_method("PUT")
        self.assertEqual(result, "StatusCode.OK_200")

    def test_get_status_code_for_patch(self):
        """Test PATCH method returns OK_200."""
        result = get_status_code_for_method("PATCH")
        self.assertEqual(result, "StatusCode.OK_200")

    def test_get_status_code_for_delete(self):
        """Test DELETE method returns NO_CONTENT_204."""
        result = get_status_code_for_method("DELETE")
        self.assertEqual(result, "StatusCode.NO_CONTENT_204")

    def test_unknown_method_defaults_to_ok_200(self):
        """Test unknown method defaults to OK_200."""
        result = get_status_code_for_method("UNKNOWN")
        self.assertEqual(result, "StatusCode.OK_200")


class TestInspectAsgiRoutes(unittest.TestCase):
    """Tests for inspect_asgi_routes function."""

    def test_app_without_routes_returns_empty(self):
        """Test that app without routes attribute returns empty list."""
        app = MagicMock()
        del app.routes
        result = inspect_asgi_routes(app)
        self.assertEqual(result, [])

    def test_app_with_empty_routes_returns_empty(self):
        """Test that app with empty routes returns empty list."""
        app = MagicMock()
        app.routes = []
        result = inspect_asgi_routes(app)
        self.assertEqual(result, [])

    def test_skips_routes_without_methods(self):
        """Test that routes without methods attribute are skipped."""
        route1 = MagicMock()
        del route1.methods  # Remove methods attribute

        app = MagicMock()
        app.routes = [route1]
        result = inspect_asgi_routes(app)
        self.assertEqual(result, [])

    def test_skips_routes_without_path(self):
        """Test that routes without path are skipped."""
        route = MagicMock()
        route.methods = {"GET"}
        route.path = ""

        app = MagicMock()
        app.routes = [route]
        result = inspect_asgi_routes(app)
        self.assertEqual(result, [])

    def test_filters_out_head_and_options(self):
        """Test that HEAD and OPTIONS methods are filtered out."""
        route = MagicMock()
        route.path = "/health"
        # Use a list to ensure consistent ordering
        route.methods = ["GET", "HEAD", "OPTIONS"]

        app = MagicMock()
        app.routes = [route]
        result = inspect_asgi_routes(app)
        self.assertEqual(len(result), 1)
        # Just verify the structure, order of all_methods may vary
        self.assertEqual(result[0][0], "/health")
        self.assertEqual(result[0][1], "GET")
        self.assertIn("GET", result[0][2])
        self.assertIn("HEAD", result[0][2])
        self.assertIn("OPTIONS", result[0][2])

    def test_returns_multiple_methods(self):
        """Test that multiple methods are returned."""
        route = MagicMock()
        route.path = "/users"
        # Use a list to ensure consistent ordering
        route.methods = ["GET", "POST"]

        app = MagicMock()
        app.routes = [route]
        result = inspect_asgi_routes(app)
        self.assertEqual(len(result), 2)
        # Check structure without depending on order
        methods_found = {r[1] for r in result}
        self.assertEqual(methods_found, {"GET", "POST"})

    def test_methods_are_sorted(self):
        """Test that methods are returned in sorted order."""
        route = MagicMock()
        route.path = "/items"
        route.methods = {"DELETE", "GET", "POST", "PUT"}

        app = MagicMock()
        app.routes = [route]
        result = inspect_asgi_routes(app)
        methods = [r[1] for r in result]
        self.assertEqual(methods, sorted(methods))


class TestGenerateTestFileContent(unittest.TestCase):
    """Tests for generate_test_file_content function."""

    def test_generates_valid_header(self):
        """Test that file starts with proper imports."""
        routes = [("/health", "GET", ["GET"])]
        content = generate_test_file_content("main", "app", routes)

        self.assertIn('"""Auto-generated ASGI tests from scan command."""', content)
        self.assertIn("from rapidtest import ASGITest, StatusCode", content)
        self.assertIn("from main import app", content)
        self.assertIn("api = ASGITest(app=app)", content)

    def test_generates_test_for_get_route(self):
        """Test that GET route generates proper test call."""
        routes = [("/health", "GET", ["GET"])]
        content = generate_test_file_content("main", "app", routes)

        self.assertIn("# Auto-generated test for GET /health", content)
        self.assertIn('api.get(path="/health", status=StatusCode.OK_200)', content)

    def test_generates_test_for_post_route(self):
        """Test that POST route generates proper test call with CREATED_201."""
        routes = [("/users", "POST", ["GET", "POST"])]
        content = generate_test_file_content("api", "router", routes)

        self.assertIn("# Auto-generated test for POST /users", content)
        self.assertIn('api.post(path="/users", status=StatusCode.CREATED_201)', content)

    def test_generates_test_for_delete_route(self):
        """Test that DELETE route generates proper test call with NO_CONTENT_204."""
        routes = [("/users/1", "DELETE", ["DELETE"])]
        content = generate_test_file_content("main", "app", routes)

        self.assertIn(
            'api.delete(path="/users/1", status=StatusCode.NO_CONTENT_204)', content
        )

    def test_includes_todo_comment(self):
        """Test that each test includes a TODO comment."""
        routes = [("/health", "GET", ["GET"])]
        content = generate_test_file_content("main", "app", routes)

        self.assertIn("# TODO: Review and update expected response", content)

    def test_handles_multiple_routes(self):
        """Test that multiple routes are all included."""
        routes = [
            ("/health", "GET", ["GET"]),
            ("/users", "GET", ["GET", "POST"]),
            ("/users", "POST", ["GET", "POST"]),
        ]
        content = generate_test_file_content("main", "app", routes)

        self.assertIn("/health", content)
        self.assertIn("/users", content)
        self.assertEqual(content.count("api."), 3)

    def test_handles_empty_routes(self):
        """Test that empty routes list generates valid file."""
        content = generate_test_file_content("main", "app", [])

        self.assertIn("from rapidtest import ASGITest, StatusCode", content)
        self.assertIn("api = ASGITest(app=app)", content)
        self.assertEqual(content.count("api."), 0)


class TestGetUniqueFilePath(unittest.TestCase):
    """Tests for get_unique_file_path function."""

    def setUp(self):
        """Create a temporary directory for tests."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)

    def tearDown(self):
        """Clean up temporary directory."""
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_returns_same_path_if_not_exists(self):
        """Test that non-existent file returns same path."""
        path = self.temp_path / "test_new.py"
        result = get_unique_file_path(path)
        self.assertEqual(result, path)

    def test_adds_suffix_if_exists(self):
        """Test that suffix is added if file exists."""
        path = self.temp_path / "test_existing.py"
        path.write_text("existing")

        result = get_unique_file_path(path)
        self.assertEqual(result.name, "test_existing_1.py")

    def test_increments_counter(self):
        """Test that counter increments correctly."""
        path = self.temp_path / "test.py"

        # Create files with suffixes
        (self.temp_path / "test.py").write_text("1")
        (self.temp_path / "test_1.py").write_text("2")

        result = get_unique_file_path(path)
        self.assertEqual(result.name, "test_2.py")

    def test_handles_multiple_existing_files(self):
        """Test with multiple existing files."""
        path = self.temp_path / "multi.py"

        # Create base file and files with suffix 1-4
        path.write_text("base")
        for i in range(1, 5):
            (self.temp_path / f"multi_{i}.py").write_text(str(i))

        result = get_unique_file_path(path)
        self.assertEqual(result.name, "multi_5.py")


class TestScanError(unittest.TestCase):
    """Tests for ScanError exception."""

    def test_creates_error_with_message(self):
        """Test that error can be created with message only."""
        error = ScanError("Something went wrong")
        self.assertEqual(str(error), "Something went wrong")
        self.assertIsNone(error.details)

    def test_creates_error_with_details(self):
        """Test that error can be created with message and details."""
        error = ScanError("Import failed", details="Module not found")
        self.assertEqual(str(error), "Import failed")
        self.assertEqual(error.details, "Module not found")

    def test_is_exception_subclass(self):
        """Test that ScanError is a subclass of Exception."""
        self.assertIsInstance(ScanError("test"), Exception)


class TestConstants(unittest.TestCase):
    """Tests for module constants."""

    def test_valid_http_methods_excludes_head_options(self):
        """Test that VALID_HTTP_METHODS excludes HEAD and OPTIONS."""
        self.assertIn("GET", VALID_HTTP_METHODS)
        self.assertIn("POST", VALID_HTTP_METHODS)
        self.assertIn("PUT", VALID_HTTP_METHODS)
        self.assertIn("PATCH", VALID_HTTP_METHODS)
        self.assertIn("DELETE", VALID_HTTP_METHODS)
        self.assertNotIn("HEAD", VALID_HTTP_METHODS)
        self.assertNotIn("OPTIONS", VALID_HTTP_METHODS)

    def test_default_status_codes_has_all_methods(self):
        """Test that DEFAULT_STATUS_CODES has entries for all valid methods."""
        for method in VALID_HTTP_METHODS:
            self.assertIn(method, DEFAULT_STATUS_CODES)


if __name__ == "__main__":
    unittest.main()
