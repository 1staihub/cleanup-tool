class CleanupToolError(Exception):
    """Base exception for cleanup-tool."""


class ValidationError(CleanupToolError):
    """Raised when user input or config is invalid."""


class ScanError(CleanupToolError):
    """Raised when scanning fails."""


class ApplyError(CleanupToolError):
    """Raised when cleanup application fails."""


class ReportError(CleanupToolError):
    """Raised when report generation fails."""


class CleanupRuntimeError(CleanupToolError):
    """Raised when a runtime environment issue blocks execution."""
