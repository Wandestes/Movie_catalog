import sys
import os

# Додаємо корінь проекту до шляхів пошуку модулів
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from movie_service.movies_repository import (
    get_all_movies,
    search_movies,
    get_movie_by_id,
    add_movie,
    delete_movie,
    update_movie
)
from user_service.users_repository import (
    create_user,
    get_user_by_id,
    delete_user
)

# --- MOVIE UI FUNCTIONS ---

def list_movies():
    movies = get_all_movies()
    print("\nAll movies:")
    if not movies:
        print("Catalog is empty.\n")
        return
    for m in movies:
        print(f"{m['id']}. {m['title']} ({m['year']}) - {m['genre']} - ⭐{m['rating']}")
    print()

def search_movie():
    query = input("Enter title to search: ").lower()
    results = search_movies(query)
    print("\nSearch results:")
    if results:
        for m in results:
            print(f"{m['id']}. {m['title']} - ⭐{m['rating']}")
    else:
        print("Nothing found.")
    print()

def filter_by_genre():
    genre = input("Enter genre: ").capitalize()
    movies = get_all_movies()
    results = [m for m in movies if m["genre"] == genre]
    print(f"\nMovies of genre {genre}:")
    if results:
        for m in results:
            print(f"{m['id']}. {m['title']} - ⭐{m['rating']}")
    else:
        print("Nothing found.\n")
    print()

def show_movie_details():
    try:
        movie_id = int(input("Enter movie ID: "))
        movie = get_movie_by_id(movie_id)
        if movie:
            print("\nMovie details:")
            print(f"Title: {movie['title']}")
            print(f"Year: {movie['year']}")
            print(f"Genre: {movie['genre']}")
            print(f"Rating: {movie['rating']}")
            print(f"Description: {movie['description']}\n")
        else:
            print("Movie not found.\n")
    except ValueError:
        print("Invalid ID format.\n")

def add_movie_ui():
    print("\nAdd movie")
    title = input("Title: ")
    year = int(input("Year: "))
    genre = input("Genre: ")
    rating = float(input("Rating: "))
    description = input("Description: ")
    movie = {"title": title, "year": year, "genre": genre, "rating": rating, "description": description}
    add_movie(movie)
    print("Movie successfully added!\n")

def delete_movie_ui():
    try:
        movie_id = int(input("Enter movie ID to delete: "))
        delete_movie(movie_id)
        print("Movie deleted (if existed).\n")
    except ValueError:
        print("Invalid ID format.\n")

def update_movie_ui():
    try:
        movie_id = int(input("Movie ID to update: "))
        movie = get_movie_by_id(movie_id)
        if not movie:
            print("Movie not found.\n")
            return

        print("\nLeave empty to keep the field unchanged.")
        new_title = input(f"New title ({movie['title']}): ") or movie['title']
        new_year = input(f"New year ({movie['year']}): ")
        new_year = int(new_year) if new_year else movie['year']
        new_genre = input(f"New genre ({movie['genre']}): ") or movie['genre']
        new_rating = input(f"New rating ({movie['rating']}): ")
        new_rating = float(new_rating) if new_rating else movie['rating']
        new_description = input(f"New description ({movie['description']}): ") or movie['description']

        updated_movie = {
            "title": new_title, "year": new_year, "genre": new_genre,
            "rating": new_rating, "description": new_description
        }
        update_movie(movie_id, updated_movie)
        print("Movie updated!\n")
    except ValueError:
        print("Invalid input format.\n")

# --- USER UI FUNCTIONS ---

def add_user_ui():
    print("\n--- Create New User ---")
    username = input("Enter username: ")
    email = input("Enter email: ")
    password = input("Enter password: ")
    user_id = create_user({"username": username, "email": email, "password": password})
    if user_id:
        print(f"User created successfully with ID: {user_id}\n")
    else:
        print("Error: Could not create user.\n")

def show_user_details_ui():
    try:
        user_id = int(input("Enter user ID: "))
        user = get_user_by_id(user_id)
        if user:
            print("\n--- User Details ---")
            print(f"ID: {user['id']} | Username: {user['username']} | Email: {user['email']}")
            print(f"Joined: {user['created_at']}\n")
        else:
            print("User not found.\n")
    except ValueError:
        print("Invalid ID format.\n")

def delete_user_ui():
    try:
        user_id = int(input("Enter user ID to delete: "))
        if delete_user(user_id):
            print("User successfully deleted.\n")
        else:
            print("User not found.\n")
    except ValueError:
        print("Invalid ID format.\n")

# --- MAIN MENU ---

def main():
    while True:
        print("========== MOVIE & USER SYSTEM ==========")
        print("1. Show all movies")
        print("2. Search movie")
        print("3. Filter by genre")
        print("4. Movie details")
        print("5. Add movie")
        print("6. Delete movie")
        print("7. Update movie")
        print("-" * 25)
        print("8. Create user")
        print("9. Show user details")
        print("10. Delete user")
        print("0. Exit")

        choice = input("\nChoose an action: ")

        if choice == "1": list_movies()
        elif choice == "2": search_movie()
        elif choice == "3": filter_by_genre()
        elif choice == "4": show_movie_details()
        elif choice == "5": add_movie_ui()
        elif choice == "6": delete_movie_ui()
        elif choice == "7": update_movie_ui()
        elif choice == "8": add_user_ui()
        elif choice == "9": show_user_details_ui()
        elif choice == "10": delete_user_ui()
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice!\n")

if __name__ == "__main__":
    main()