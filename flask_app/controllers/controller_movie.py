from flask import render_template, redirect, request, session, flash
import requests
from flask_app import app
from flask_app.models.models_movie import Movie
from flask_app.models.models_popular_movies import PopMovie
from flask_app.models.models_user import User
import os
from flask import jsonify


@app.route('/popularmovies')
def popularMovies():
    print("this is the key : ")
    print( os.environ.get("FLASK_APP_API_KEY"))
    response = requests.get(f"https://api.themoviedb.org/3/movie/popular?api_key={os.environ.get('FLASK_APP_API_KEY')}&language=en-US&page=1")
    popularmovies = response.json()
    print(popularmovies)
    i=1
    while i <= 10:

        year = Movie.split_year(popularmovies['results'][i]['release_date'])

        data = {
        "movie_id" :  popularmovies['results'][i]['id'],
        'title' :  popularmovies['results'][i]['title'],
        'year' :  year,
        'release_date' :  popularmovies['results'][i]['release_date'],
        'overview' :  popularmovies['results'][i]['overview'],
        'poster_path' :  popularmovies['results'][i]['poster_path'],
        'original_language' :  popularmovies['results'][i]['original_language'],
        'rating' :  popularmovies['results'][i]['vote_average'],
        'id' : i
        }

        PopMovie.save(data)

        i += 1


        return render_template("popular.html", movies = PopMovie.get_all())


@app.route('/newmovie')
def addMovie():
    if session.get('user_id') != None:
        data = {
            "id" : session['user_id']
        }
        return render_template("addmovie.html", user=User.get_one(data))
    else: flash("You are not logged in!", 'notlog')
    return redirect('/')

@app.route('/createmovie', methods=['POST'])
def createmovie():

    title = request.form['title']
    year = request.form['year']

    response = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={os.environ.get('FLASK_APP_API_KEY')}&language=en-US&query={title}&page=1&include_adult=false&year={year}")
    
    if not(response):
        response = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={os.environ.get('FLASK_APP_API_KEY')}&language=en-US&query={title}&page=1&include_adult=false")

    print("first response status code")
    print(response.status_code)
    if response.status_code == 422:
        flash("No Movie Found!", "invalidMovie")
        return redirect('/newmovie')

    

    movieSearchjson = response.json()

    movie_id = movieSearchjson['results'][0]['id']

    responsefind = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={os.environ.get('FLASK_APP_API_KEY')}&language=en-US")

    print(response.status_code)
    movieFindjson = responsefind.json()
    print(movieFindjson)

    year = Movie.split_year(movieFindjson['release_date'])
    

    data = {
        "movie_id" :  movieFindjson['id'],
        'imdb_id' :  movieFindjson['imdb_id'],
        'title' :  movieFindjson['original_title'],
        'year' :  year,
        'release_date' :  movieFindjson['release_date'],
        'tagline' :  movieFindjson['tagline'],
        'overview' :  movieFindjson['overview'],
        'poster_path' :  movieFindjson['poster_path'],
        'original_language' :  movieFindjson['original_language'],
        'rating' :  request.form['rating'],
        'user_rating' :  movieFindjson['vote_average'],
        'genre' :  movieFindjson['genres'][0]['name'],
        'user_id' :  session['user_id']
        }

    Movie.save(data)

    return redirect('/dashboard')

@app.route('/edit/<int:movie_id>')
def edit_band(movie_id):
    movie_data = {
        'id':movie_id
    }
    if session.get('user_id') != None:
        data = {
            "id" : session['user_id']
        }
        return render_template("editmovie.html", user=User.get_one(data), movie = Movie.get_one(movie_data))
    else: flash("You are not logged in!", 'notlog')
    return redirect('/')

@app.route('/editmovie/<int:movie_database_id>', methods=['POST'])
def updateband(movie_database_id):

    imdb_id = request.form['imdb_id']

    response = requests.get(f"https://api.themoviedb.org/3/find/{imdb_id}?api_key={os.environ.get('FLASK_APP_API_KEY')}&language=en-US&external_source=imdb_id")

    movieSearchjson = response.json()

    print(movieSearchjson)

    movie_id = movieSearchjson['movie_results'][0]['id']

    responsefind = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={os.environ.get('FLASK_APP_API_KEY')}&language=en-US")

    print(response.status_code)
    movieFindjson = responsefind.json()
    print(movieFindjson)

    year = Movie.split_year(movieFindjson['release_date'])
    

    data = {
        "movie_id" :  movieFindjson['id'],
        'imdb_id' :  movieFindjson['imdb_id'],
        'title' :  movieFindjson['original_title'],
        'year' :  year,
        'release_date' :  movieFindjson['release_date'],
        'tagline' :  movieFindjson['tagline'],
        'overview' :  movieFindjson['overview'],
        'poster_path' :  movieFindjson['poster_path'],
        'original_language' :  movieFindjson['original_language'],
        'rating' :  request.form['rating'],
        'user_rating' :  movieFindjson['vote_average'],
        'genre' :  movieFindjson['genres'][0]['name'],
        'user_id' :  session['user_id'],
        'id' : movie_database_id
        }

    movie_id = Movie.update(data)

    return redirect('/dashboard')

@app.route('/delete/<int:movie_id>')
def delete_band(movie_id):
    data = {
        'id':movie_id
    }
    Movie.destroy(data)
    return redirect('/dashboard')

@app.route('/showmovie/<int:movie_id>')
def show_car(movie_id):
    data={
        'id':movie_id
    }
    return render_template("showmovie.html",movie = Movie.get_one_movie(data), poster = Movie.get_poster(data))

# @app.route('/searchmovie', methods=['POST'])
# def call_search_movie():

#     title = request.form['title']
#     year = request.form['year']

#     movie = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={os.environ.get('FLASK_API_KEY')}&language=en-US&query={movie}&page=1&include_adult=false&year={year}")
    
#     movie['user_id'] = session['user_id']

#     Movie.save(movie)
#     return redirect('dashboard')