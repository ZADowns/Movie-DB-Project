# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the friend table from our database
from flask_app import DATABASE
from flask_app.models import models_user

class PopMovie:
    def __init__( self , data ):
        self.id = data['id']
        self.movie_id = data['movie_id']
        self.title = data['title']
        self.year = data['year']
        self.release_date = data['release_date']
        self.overview = data['overview']
        self.poster_path = data['poster_path']
        self.original_language = data['original_language']
        self.rating = data['rating']
        self.updated_at = data['updated_at']
        self.created_at = data['created_at']
# Now we use class methods to query our database

    @classmethod
    def save(cls, data):
        print("movie save method")
        query = "INSERT INTO popular_movies ( movie_id, title, year, release_date, overview, poster_path, original_language, rating, created_at, updated_at, id ) VALUES (%(movie_id)s,  %(title)s, %(year)s, %(release_date)s,  %(overview)s, %(poster_path)s, %(original_language)s, %(rating)s, NOW(), NOW()), %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM popular_movies;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(DATABASE).query_db(query)
        # Create an empty list to append our instances of friends
        all_movies = []
        # Iterate over the db results and create instances of friends with cls.
        for dict in results:
            all_movies.append( cls(dict) )
        return all_movies
            

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM popular_movies WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)

        if not result:
            return False
        
        #return an instance
        return cls( result[0])

    @classmethod
    def update(cls,data):
        query = "UPDATE movies SET popular_movies=%(movie_id)s, imdb_id=%(imdb_id)s, title=%(title)s, year=%(year)s, release_date=%(release_date)s, tagline=%(tagline)s, overview=%(overview)s, poster_path=%(poster_path)s, original_language=%(original_language)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM popular_movies WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def get_all_movies(cls):

        query = "SELECT * FROM popular_movies JOIN users ON users.id = movies.user_id;"
        results = connectToMySQL(DATABASE).query_db(query)
        print(results)
        if not results:
            return False


        all_movies = []
        for row_from_db in results:
            movies = cls(row_from_db)
            user_data = {
                'id': row_from_db["users.id"],
                "created_at" : row_from_db["users.created_at"],
                "updated_at" : row_from_db["users.updated_at"],
                'first_name': row_from_db['first_name'],
                'last_name': row_from_db['last_name'],
                'email': row_from_db['email'],
                'password': row_from_db['password']
            }
            
            movies.user = models_user.User(user_data)
            all_movies.append(movies)
            
        return all_movies

    @classmethod
    def get_one_movie(cls,data):
        query = "SELECT * FROM popular_movies JOIN users ON users.id = movies.user_id  WHERE movies.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        print(results)
        if not results:
            return False


        all_movies = []
        for row_from_db in results:
            movies = cls(row_from_db)
            user_data = {
                'id': row_from_db["users.id"],
                "created_at" : row_from_db["users.created_at"],
                "updated_at" : row_from_db["users.updated_at"],
                'first_name': row_from_db['first_name'],
                'last_name': row_from_db['last_name'],
                'email': row_from_db['email'],
                'password': row_from_db['password']
            }
            
            movies.user = models_user.User(user_data)
            all_movies.append(movies)
            
        return all_movies[0]

    @classmethod
    def get_poster(cls, data):
        query = "SELECT poster_path FROM popular_movies WHERE movies.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        print(results[0]['poster_path'])
        url = f"https://image.tmdb.org/t/p/original/{results[0]['poster_path']}"
        print(url)
        return url

    @classmethod
    def append_poster_path(cls, data):
        url = f"https://image.tmdb.org/t/p/original/{data}"
        return url

    @classmethod
    def split_year(cls, data):
        year = data[0:4]
        return year