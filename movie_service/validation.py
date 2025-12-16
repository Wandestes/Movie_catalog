from typing import Dict, Any

def validate_movie_data(data: Dict[str, Any]) -> tuple[bool, str]:

    
    required_fields = ['title', 'year', 'genre', 'rating', 'description']
    
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: '{field}'"
        
    
    if not isinstance(data['title'], str) or not data['title'].strip():
        return False, "Title must be a non-empty string."

    if not isinstance(data['year'], int) or data['year'] < 1888: 
        return False, "Year must be a valid integer (e.g., 2024)."

    if not isinstance(data['rating'], (int, float)) or not (0.0 <= data['rating'] <= 5.0):
        return False, "Rating must be a number between 0.0 and 5.0."

    if not isinstance(data['genre'], str):
        return False, "Genre must be a string."

    if not isinstance(data['description'], str):
        return False, "Description must be a string."
    
    return True, ""