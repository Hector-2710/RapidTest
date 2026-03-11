from contextlib import contextmanager
from typing import Any
from dataclasses import dataclass
import inspect
import time
from collections.abc import Generator

@dataclass
class DatabaseOperation:
    """ Structure for storing details of a database operation """
    operation_type: str  
    table: str
    query: str
    params: dict | None = None
    execution_time: float = 0.0
    scope_info: dict | None = None


class ASGIDBInterceptor:
    """ 
    Interceptor for capturing database operations in ASGI test contexts.
    
    This class is designed to work with SQLAlchemy and can be extended to support other ORMs.
    """

    def __init__(self):
        self.captured_operations:list[DatabaseOperation] = []
        self.is_intercepting = False
        self._original_execute = None
        self._is_patched = False
        
    def detect_asgi_test_context(self, scope: dict | None = None) -> bool:
        """ The function attempts to detect if the current execution context is an ASGI """
        if not scope:
            frame = inspect.currentframe()
            while frame:
                if 'scope' in frame.f_locals:
                    scope = frame.f_locals['scope']
                    break
                frame = frame.f_back
        
        if not scope:
            return False
            
        test_indicators = [
            scope.get("server", ("", 0))[0] == "testserver",
            scope.get("client", ("", 0))[0] == "testclient", 
            scope.get("rapidtest_capturing", False),
            "test" in scope.get("path", "").lower()
        ]
        
        return any(test_indicators)
    
    def patch_sqlalchemy_session(self):
        """Patches SQLAlchemy Session to intercept execute calls"""
        if self._is_patched:
            return  
            
        try:
            from sqlalchemy.orm import Session
            self._original_execute = Session.execute
            
            def intercepted_execute(session_self, statement, parameters=None, **kwargs):
                start_time = time.time()
                
                if self.is_intercepting or self.detect_asgi_test_context():
                    operation = self._parse_sql_operation(str(statement), parameters)
                    operation.execution_time = time.time() - start_time
                    self.captured_operations.append(operation)
                
                result = self._original_execute(session_self, statement, parameters, **kwargs)
                
                return result
            
            Session.execute = intercepted_execute
            self._is_patched = True
            
        except ImportError:
            pass
    
    def _parse_sql_operation(self, sql: str, params: Any) -> DatabaseOperation:
        """Parses SQL statement to extract operation type and table name."""
        sql_upper = sql.upper().strip()
        
        operation_type = "UNKNOWN"
        table = "unknown"
        
        if sql_upper.startswith("INSERT"):
            operation_type = "INSERT"
            table = self._extract_table_from_insert(sql)
        elif sql_upper.startswith("UPDATE"):
            operation_type = "UPDATE"
            table = self._extract_table_from_update(sql)
        elif sql_upper.startswith("DELETE"):
            operation_type = "DELETE" 
            table = self._extract_table_from_delete(sql)
        elif sql_upper.startswith("SELECT"):
            operation_type = "SELECT"
            table = self._extract_table_from_select(sql)
            
        return DatabaseOperation(
            operation_type=operation_type,
            table=table,
            query=sql,
            params=params
        )
    
    def _extract_table_from_insert(self, sql: str) -> str:
        """Extracts table name from INSERT statement"""
        try:
            parts = sql.upper().split()
            into_index = parts.index("INTO")
            return parts[into_index + 1].strip("(").split("(")[0]
        except (ValueError, IndexError):
            return "unknown"
    
    def _extract_table_from_update(self, sql: str) -> str:
        """Extracts table name from UPDATE statement"""
        try:
            parts = sql.upper().split()
            update_index = parts.index("UPDATE")
            return parts[update_index + 1]
        except (ValueError, IndexError):
            return "unknown"
    
    def _extract_table_from_delete(self, sql: str) -> str:
        """Extracts table name from DELETE statement"""
        try:
            parts = sql.upper().split()
            from_index = parts.index("FROM")
            return parts[from_index + 1]
        except (ValueError, IndexError):
            return "unknown"
    
    def _extract_table_from_select(self, sql: str) -> str:
        """Extracts table name from SELECT statement"""
        try:
            parts = sql.upper().split()
            from_index = parts.index("FROM")
            return parts[from_index + 1].split()[0]
        except (ValueError, IndexError):
            return "unknown"
    
    @contextmanager
    def capture_operations(self) -> Generator[list[DatabaseOperation], None, None]:
        """Context manager for capturing database operations within its scope"""
        previous_operations = self.captured_operations.copy()
        self.captured_operations = []
        self.is_intercepting = True
        
        try:
            yield self.captured_operations
        finally:
            self.is_intercepting = False
            self.captured_operations.extend(previous_operations)
    
    def clear_operations(self):
        """Clears captured operations"""
        self.captured_operations = []
    
    def get_operations_by_type(self, operation_type: str) -> list[DatabaseOperation]:
        """Gets operations by type (INSERT, UPDATE, DELETE, SELECT)"""
        return [op for op in self.captured_operations 
                if op.operation_type == operation_type.upper()]
    
    def get_operations_by_table(self, table: str) -> list[DatabaseOperation]:
        """Gets operations by table"""
        return [op for op in self.captured_operations 
                if op.table.lower() == table.lower()]
    
    def restore_original_methods(self):
        """Restores original SQLAlchemy methods"""
        if self._original_execute and self._is_patched:
            try:
                from sqlalchemy.orm import Session
                Session.execute = self._original_execute
                self._original_execute = None
                self._is_patched = False
            except ImportError:
                pass

db_interceptor = ASGIDBInterceptor()