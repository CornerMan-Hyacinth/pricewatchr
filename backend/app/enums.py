from enum import Enum

class ResponseStatus(str, Enum):
    """Allowed values for the `status` field."""
    SUCCESS = "success"
    ERROR = "error"
    
class UserRole(str, Enum):
    """Allowed values for the user `role` field."""
    USER = "user"
    ADMIN = "admin"