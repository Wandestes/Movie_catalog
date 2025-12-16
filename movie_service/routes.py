from flask import Blueprint, jsonify, request
# Імпортуємо функції з нашого репозиторію
import movie_service.movies_repository as movie_repo 

movies_bp = Blueprint('movies', __name__, url_prefix='/api/v1')

@movies_bp.route('/movies', methods=['GET'])
def get_movies_list():
    """ 1. Отримати список усіх фільмів або виконати пошук """
    query = request.args.get('q') 
    
    if query:
        movies = movie_repo.search_movies(query)
    else:
        # Тут можна додати пагінацію, але для початку використовуємо all
        movies = movie_repo.get_all_movies()
        
    return jsonify(movies)

@movies_bp.route('/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    """ 2. Отримати деталі конкретного фільму """
    movie = movie_repo.get_movie_by_id(movie_id)
    if movie:
        return jsonify(movie)
    return jsonify({"message": "Movie not found"}), 404

@movies_bp.route('/movies', methods=['POST'])
def add_new_movie():
    """ 3. Додати новий фільм у каталог (потрібна авторизація адміна) """
    data = request.json
    
    # *Важливо*: У реальному проєкті тут має бути перевірка,
    # чи авторизований користувач є адміністратором!
    
    if not all(k in data for k in ("title", "year", "genre", "rating")):
        return jsonify({"message": "Missing required fields (title, year, genre, rating)"}), 400
        
    if movie_repo.add_movie(data):
        # 201 Created
        return jsonify({"message": "Movie added successfully", "movie": data}), 201
    return jsonify({"message": "Failed to add movie due to DB error"}), 500