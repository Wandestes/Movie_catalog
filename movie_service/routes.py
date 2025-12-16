from flask import Blueprint, jsonify, request
import movie_service.movies_repository as movie_repo
from movie_service.validation import validate_movie_data

movies_bp = Blueprint('movies', __name__, url_prefix='/api/v1')

@movies_bp.route('/movies', methods=['GET'])
def get_movies_list():
    # Отримуємо параметр запиту 'query'
    query = request.args.get('query') 
    
    if query:
        # Якщо є параметр пошуку, викликаємо search_movies
        movies = movie_repo.search_movies(query)
    else:
        # Інакше повертаємо всі фільми
        movies = movie_repo.get_all_movies()
        
    if movies is None:
        # Обробка помилки підключення, якщо репозиторій повертає None (хоча у вашій реалізації повертається [])
        return jsonify({"message": "Database connection error"}), 500

    return jsonify(movies), 200

@movies_bp.route('/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    movie = movie_repo.get_movie_by_id(movie_id)
    if movie:
        return jsonify(movie)
    return jsonify({"message": "Movie not found"}), 404

@movies_bp.route('/movies', methods=['POST'])
def add_new_movie():
    data = request.json
    
    is_valid, error_msg = validate_movie_data(data)
    if not is_valid:
        return jsonify({"error": error_msg}), 400
    
    if movie_repo.add_movie(data):
        return jsonify({"message": "Movie added successfully", "movie": data}), 201
    return jsonify({"message": "Failed to add movie due to DB error"}), 500

@movies_bp.route('/movies/<int:movie_id>', methods=['PUT'])
def update_movie_route(movie_id):
    data = request.json

    if data is None:
        return jsonify({"error": "No JSON data provided"}), 400

    is_valid, error_msg = validate_movie_data(data)
    if not is_valid:
        return jsonify({"error": error_msg}), 400

    # ВИКОРИСТОВУЄМО movie_repo
    if movie_repo.update_movie(movie_id, data):
        return jsonify({"message": f"Movie with ID {movie_id} updated successfully"}), 200
    else:
        return jsonify({"error": f"Failed to update movie with ID {movie_id}. Movie not found or database error."}), 404

@movies_bp.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie_route(movie_id):

    # ВИКОРИСТОВУЄМО movie_repo
    if movie_repo.delete_movie(movie_id):
        return jsonify({"message": f"Movie with ID {movie_id} deleted successfully"}), 200
    else:
        return jsonify({"error": f"Failed to delete movie with ID {movie_id}. Movie not found or database error."}), 404