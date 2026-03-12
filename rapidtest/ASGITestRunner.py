from contextlib import contextmanager
from .ASGITest import ASGITest, ASGIResponse
from .ASGIDatabase import db_interceptor, DatabaseOperation
from .Utils import print_report, show_connection_error
from typing import Annotated, Any

class ASGITestRunner(ASGITest):
    """
    Main class for testing ASGI applications with integrated API and database validation.

    This class extends ASGITest to provide enhanced functionality for validating both API
    responses and database operations in a cohesive manner. It includes:
    """

    def __init__(self, app: Annotated[Any, "Instance of ASGI application"], auto_patch_db: bool = True):
        """
        Initializes the ASGITestRunner with the given ASGI application and optional database patching.
        
        Args:
            app: An instance of the ASGI application to be tested (e.g., FastAPI app).
            auto_patch_db: If True, attempts to automatically patch database interceptors for capturing operations
            without requiring manual setup. Defaults to True.
        """
        super().__init__(app)
        
        if auto_patch_db:
            self._try_patch_database()
    
    def get(self, 
            path: str, 
            expected_status: int = 200, 
            expected_json: dict | None = None,
            contain_keys: list[str] | None = None,
            **kwargs) -> 'EnhancedASGIResponse':
        """
        Performs a GET request and validates status code and response body.
        
        Args:
            path (str): The path for the GET request.
            expected_status (int): The expected HTTP status code (default: 200).
            expected_json (dict | None): The expected JSON response body (default: None).
            contain_keys (list[str] | None): A list of keys that should be present in the response JSON (default: None).
            **kwargs: Additional keyword arguments to pass to the request method.

        Returns:
            EnhancedASGIResponse: An enhanced response object that includes database operation information.
        """
        try:
            response = super().get(path, **kwargs)
            enhanced = EnhancedASGIResponse(response, db_interceptor.captured_operations.copy())
            
            validation_passed = self._process_response_validation(
                response, path, expected_status, expected_json, contain_keys
            )
            
            return enhanced
            
        except Exception as e:
            simulated_url = f"asgi://testserver{path}"
            show_connection_error(simulated_url, e)
            raise
    
    def post(self,
             path: str, 
             json_data: dict | None = None, 
             expected_status: int = 201,
             expected_json: dict | None = None,
             contain_keys: list[str] | None = None,
             **kwargs) -> 'EnhancedASGIResponse':
        """
        Performs a POST request and validates status code and response body.
        
        Args:
            path (str): The path for the POST request.
            json_data (dict | None): The JSON data to send in the request body.
            expected_status (int): The expected HTTP status code (default: 201).
            expected_json (dict | None): The expected JSON response body (default: None).
            contain_keys (list[str] | None): A list of keys that should be present in the response JSON (default: None).
            **kwargs: Additional keyword arguments to pass to the request method.

        Returns:
            EnhancedASGIResponse: An enhanced response object that includes database operation information.
        """
        try:
            response = super().post(path, json_data, **kwargs)
            enhanced = EnhancedASGIResponse(response, db_interceptor.captured_operations.copy())
            
            validation_passed = self._process_response_validation(
                response, path, expected_status, expected_json, contain_keys
            )
            
            return enhanced
            
        except Exception as e:
            simulated_url = f"asgi://testserver{path}"
            show_connection_error(simulated_url, e)
            raise
    
    def put(self, 
            path: str, 
            json_data: dict | None = None,
            expected_status: int = 200,
            expected_json: dict | None = None,
            contain_keys: list[str] | None = None,
            **kwargs) -> 'EnhancedASGIResponse':
        """
        Performs a PUT request and validates status code and response body.
        
        Args:
            path (str): The path for the PUT request.
            json_data (dict | None): The JSON data to send in the request body.
            expected_status (int): The expected HTTP status code (default: 200).
            expected_json (dict | None): The expected JSON response body (default: None).
            contain_keys (list[str] | None): A list of keys that should be present in the response JSON (default: None).
            **kwargs: Additional keyword arguments to pass to the request method.

        Returns:
            EnhancedASGIResponse: An enhanced response object that includes database operation information.
        """
        try:
            response = super().put(path, json_data, **kwargs)
            enhanced = EnhancedASGIResponse(response, db_interceptor.captured_operations.copy())
            
            validation_passed = self._process_response_validation(
                response, path, expected_status, expected_json, contain_keys
            )
            
            return enhanced
            
        except Exception as e:
            simulated_url = f"asgi://testserver{path}"
            show_connection_error(simulated_url, e)
            raise
    
    def delete(self, 
               path: str, 
               expected_status: int = 204, 
               expected_json: dict | None = None,
               contain_keys: list[str] | None = None,
               **kwargs) -> 'EnhancedASGIResponse':
        """
        Performs a DELETE request and validates status code and response body.
        
        Args:
            path (str): The path for the DELETE request.
            expected_status (int): The expected HTTP status code (default: 204).
            expected_json (dict | None): The expected JSON response body (default: None).
            contain_keys (list[str] | None): A list of keys that should be present in the response JSON (default: None).
            **kwargs: Additional keyword arguments to pass to the request method.

        Returns:
            EnhancedASGIResponse: An enhanced response object that includes database operation information.
        """
        try:
            response = super().delete(path, **kwargs)
            enhanced = EnhancedASGIResponse(response, db_interceptor.captured_operations.copy())
            
            validation_passed = self._process_response_validation(
                response, path, expected_status, expected_json, contain_keys
            )
            
            return enhanced
            
        except Exception as e:
            simulated_url = f"asgi://testserver{path}"
            show_connection_error(simulated_url, e)
            raise
    
    def patch(self, path: str, 
              json_data: dict | None = None,
              expected_status: int = 200,
              expected_json: dict | None = None,
              contain_keys: list[str] | None = None,
              **kwargs) -> 'EnhancedASGIResponse':
        """
        Performs a PATCH request and validates status code and response body.
        
        Args:
            path (str): The path for the PATCH request.
            json_data (dict | None): The JSON data to send in the request body.
            expected_status (int): The expected HTTP status code (default: 200).
            expected_json (dict | None): The expected JSON response body (default: None).
            contain_keys (list[str] | None): A list of keys that should be present in the response JSON (default: None).
            **kwargs: Additional keyword arguments to pass to the request method.

        Returns:
            EnhancedASGIResponse: An enhanced response object that includes database operation information.
        """
        try:
            response = super().patch(path, json_data, **kwargs)
            enhanced = EnhancedASGIResponse(response, db_interceptor.captured_operations.copy())
            
            validation_passed = self._process_response_validation(
                response, path, expected_status, expected_json, contain_keys
            )
            
            return enhanced
            
        except Exception as e:
            simulated_url = f"asgi://testserver{path}"
            show_connection_error(simulated_url, e)
            raise
    
    def _try_patch_database(self):
        """Intent to patch database interceptors if available, but fail gracefully if not"""
        try:
            db_interceptor.patch_sqlalchemy_session()
        except Exception:
            pass
    
    @contextmanager
    def capture_api_and_database(self):
        """
        Context manager to capture both API responses and database operations together.
        This allows for cohesive validation of the entire request lifecycle, including
        the API response and the underlying database interactions that occurred during the request.
        """
        self._is_capturing = True
        
        with db_interceptor.capture_operations() as operations:
            yield operations
        
        self._is_capturing = False
    
    def _validate_contain_keys(self, response_json: dict, contain_keys: list) -> bool:
        """
        Validates that the response JSON contains the expected subset of keys.
        Copiado de Test.py para mantener consistencia.
        """
        if not response_json:
            return False
        for item in contain_keys:
            if item not in response_json:
                return False
        return True
    
    def _process_response_validation(self, response: ASGIResponse, path: str, 
                                   expected_status: int, expected_json: dict = None,
                                   contain_keys: list[str] | None = None):
        """
        Proccesses the response validation and prints the report in the same format as Test.py.
        """
        simulated_url = f"asgi://testserver{path}"
        
        keys = True
        if contain_keys is not None:
            try:
                response_json = response.json()
                keys = self._validate_contain_keys(response_json, contain_keys)
            except Exception:
                response_json = {"raw_content": response.text if hasattr(response, 'text') else str(response.content)}
                keys = False
        
        try:
            response_json = response.json()
        except Exception:
            response_json = {"raw_content": response.text if hasattr(response, 'text') else str(response.content)}
        
        status_ok = response.status_code == expected_status
        body_ok = True
        error_msg = None

        if expected_json is not None:
            if response_json != expected_json:
                body_ok = False
                if status_ok:
                    if keys:
                        error_msg = "The expected JSON is not the correct"
                    else:
                        error_msg = "The expected JSON is not the correct and keys are not correct"
                else:
                    if keys:
                        error_msg = f"Expected status {expected_status}, but got {response.status_code} and the expected JSON is not the correct"
                    else:
                        error_msg = f"Expected status {expected_status}, but got {response.status_code} and the expected JSON is not the correct and keys are not correct"

        if not status_ok and not error_msg:
            if keys:
                error_msg = f"Expected status {expected_status}, but got {response.status_code}"
            else:
                error_msg = f"Expected status {expected_status}, but got {response.status_code} and keys are not correct"

        if status_ok and body_ok:
            if keys:
                print_report("PASSED", simulated_url, response.status_code, response_json)
            else:
                error_msg = "Keys are not correct"
                print_report("PASSED", simulated_url, response.status_code, response_json, error_msg=error_msg)
        else:
            print_report("FAILED", simulated_url, response.status_code, response_json, error_msg=error_msg)
        
        return status_ok and body_ok and keys
    
    def assert_db_operation_occurred(self, operation: str, table: str):
        """ Verify that a specific database operation occurred during the test execution"""
        operations = [op for op in db_interceptor.captured_operations 
                     if op.operation_type == operation.upper() and op.table.lower() == table.lower()]
        
        if not operations:
            available_ops = [f'{op.operation_type} {op.table}' for op in db_interceptor.captured_operations]
            raise AssertionError(
                f"Expected {operation.upper()} operation on table '{table}', but none occurred. "
                f"Captured operations: {available_ops}"
            )
    
    def assert_no_db_operations(self, operation: str | None = None, table: str | None = None):
        """Verify that no database operations occurred (or a specific type)"""
        if operation and table:
            operations = [op for op in db_interceptor.captured_operations 
                         if op.operation_type == operation.upper() and op.table.lower() == table.lower()]
            if operations:
                raise AssertionError(
                    f"Expected no {operation.upper()} operations on table '{table}', but {len(operations)} occurred"
                )
        elif operation:
            operations = [op for op in db_interceptor.captured_operations 
                         if op.operation_type == operation.upper()]
            if operations:
                raise AssertionError(
                    f"Expected no {operation.upper()} operations, but {len(operations)} occurred"
                )
        else:
            if db_interceptor.captured_operations:
                ops_summary = [f'{op.operation_type} {op.table}' for op in db_interceptor.captured_operations]
                raise AssertionError(
                    f"Expected no DB operations, but {len(db_interceptor.captured_operations)} occurred: {ops_summary}"
                )
    
    def get_db_operations(self, operation_type: str | None = None, table: str | None = None) -> list[DatabaseOperation]:
        """Get captured database operations with optional filtering by type and table."""
        operations = db_interceptor.captured_operations.copy()
        
        if operation_type:
            operations = [op for op in operations if op.operation_type == operation_type.upper()]
        
        if table:
            operations = [op for op in operations if op.table.lower() == table.lower()]
        
        return operations
    
    def print_db_operations_summary(self):
        """Prints a summary of captured database operations for the last request, including counts and details."""
        operations = db_interceptor.captured_operations
        
        if not operations:
            print("📊 No database operations captured")
            return
        
        print(f"\n📊 Database Operations Summary ({len(operations)} total):")
        
        types_count = {}
        tables_count = {}
        
        for op in operations:
            types_count[op.operation_type] = types_count.get(op.operation_type, 0) + 1
            tables_count[op.table] = tables_count.get(op.table, 0) + 1
        
        print(f"   Operation types: {dict(types_count)}")
        print(f"   Tables affected: {dict(tables_count)}")
        
        for i, op in enumerate(operations, 1):
            query_preview = op.query[:60] + "..." if len(op.query) > 60 else op.query
            print(f"   {i}. {op.operation_type} on '{op.table}' - {query_preview}")
    
    def clear_db_operations(self):
        db_interceptor.clear_operations()


class EnhancedASGIResponse(ASGIResponse):
    """
    An enhanced ASGI response that includes database operation information.

    This class extends ASGIResponse to provide additional context about the database operations.
    """
    
    def __init__(self, response: ASGIResponse, db_operations: list[DatabaseOperation]):
        super().__init__({
            "status_code": response.status_code,
            "headers": response.headers,
            "content": response._content,
            "json": response._json
        })
        self.db_operations = db_operations
    
    def get_db_changes(self, operation_type: str | None = None, table: str | None = None) -> list[DatabaseOperation]:
        """Get captured database operations related to this response, with optional filtering by type and table."""
        operations = self.db_operations.copy()
        
        if operation_type:
            operations = [op for op in operations if op.operation_type == operation_type.upper()]
        
        if table:
            operations = [op for op in operations if op.table.lower() == table.lower()]
        
        return operations
    
    def assert_db_operation_in_response(self, operation_type: str, table: str):
        """Verify that this specific response caused a database operation of the given type on the given table."""
        matching_ops = self.get_db_changes(operation_type, table)
        if not matching_ops:
            available_ops = [f'{op.operation_type} {op.table}' for op in self.db_operations]
            raise AssertionError(
                f"Expected {operation_type.upper()} on '{table}' in this response, "
                f"but operations were: {available_ops}"
            )
