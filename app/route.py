from flask import Blueprint, jsonify, request, abort
from app import db
from app.models import Director, Actor, Movie

movie_bp = Blueprint("movie_bp", __name__)


@movie_bp.route("/list", methods=["GET"])
def list_movies():
    movies = Movie.query.all()
    return jsonify([movie.to_dict() for movie in movies])


@movie_bp.route("/add-movie", methods=["POST"])
def create_movie():
    data = request.get_json()
    title = data.get("title")
    if not title:
        abort(400, description="title is required")

    director_name = data.get("director")
    actor_name = data.get("actors", [])

    director = None
    if director_name:
        director = Director.query.filter_by(name=director_name).first()
        if not director:
            director = Director(name=director_name)
            db.session.add(director)

    movie = Movie(
        title=title,
        description=data.get("description"),
        release_year=data.get("release_year"),
        rating=data.get("rating"),
        director=director,
    )

    for name in actor_name:
        actor = Actor.query.filter_by(name=name).first()
        if not actor:
            actor = Actor(name=name)
            db.sesion.add(actor)
        movie.actor.append(actor)

    db.session.add(movie)
    db.session.commit()

    return jsonify({"id": movie.id, "title": movie.title}), 201
