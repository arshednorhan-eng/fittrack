class AppError(Exception):
    """Base application error."""
    status_code = 400

    def __init__(self, message: str = "Application error"):
        super().__init__(message)


class NotFoundError(AppError):
    status_code = 404

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message)


class DuplicateError(AppError):
    status_code = 409

    def __init__(self, message: str = "Duplicate resource"):
        super().__init__(message)


class BusinessRuleError(AppError):
    status_code = 400

    def __init__(self, message: str = "Business rule violated"):
        super().__init__(message)
