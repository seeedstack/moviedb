from datetime import datetime, timezone
from app import db

movie_actor = db.Table(
    "movie_actor",
    db.Column("movie_id", db.Integer, db.Foreignkey("movie.id"), primary_key=True),
    db.Column("actor_id", db.Integer, db.Foreignkey("actor.id"), primary_key=True),
)


class Director(db.Model):
    __tablename__ = "director"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    bio = db.Column(db.Text)
    movies = db.relationship("Movie", back_populates="author", lazy="select")
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc),
                           nullable=False)
    deleted_at = db.Column(db.DateTime, default=None, nullable=True)


class Actor(db.Model):
    __tablename__ = "actor"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    bio = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc),
                           nullable=False)
    deleted_at = db.Column(db.DateTime, default=None, nullable=True)


class Movie(db.Model):
    __tablename__ = "movie"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    release_year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc),
                           nullable=False)
    deleted_at = db.Column(db.DateTime, default=None, nullable=True)

    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director", back_populates="movies", lazy="joined")

    actors = db.relationship(
        "Actor",
        secondary=movie_actor,
        backref=db.backref("movies", lazy="select"),
        lazy="select",
    )

