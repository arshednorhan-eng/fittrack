import re

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"
PHONE_REGEX = r"^(05\d{8}|\+?9725\d{8})$"  # Israeli local or +972 format
ID_REGEX = r"^\d{9}$"
PASSWORD_REGEX = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$!]).{8,}$"

def regex_ok(value: str, pattern: str) -> bool:
    return re.match(pattern, value or "") is not None
