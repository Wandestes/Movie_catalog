import re

def validate_user_data(data):
    """Checks if user input is valid: username, email, and password."""
    # Ensure all required fields are present
    if not all(k in data for k in ("username", "email", "password")):
        return False, "Missing fields"
    
    # Username length check
    if len(data['username']) < 3:
        return False, "Username too short"
    
    # Email format check using regex
    email_regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    if not re.match(email_regex, data['email']):
        return False, "Invalid email format"
        
    # Password complexity check
    if len(data['password']) < 6:
        return False, "Password must be at least 6 characters"
        
    return True, None