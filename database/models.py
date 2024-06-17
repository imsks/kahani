from sqlite3 import IntegrityError
import traceback
from flask_sqlalchemy import SQLAlchemy
from utils.contants import CelebRoles

db = SQLAlchemy()

class Celeb(db.Model):
    __tablename__ = 'celeb'

    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(200))

    def store_celeb(self, data):
        if data["type"] != "Celeb":
            return None

        celeb = Celeb.query.filter_by(id=data["id"]).first()
        if not celeb:
            celeb = Celeb(id=data["id"], name=data["name"], image=data["image"])
            db.session.add(celeb)

        try:
            db.session.commit()
            print(f"Stored celeb: {celeb}")
            return celeb
        except Exception as e:
            print(traceback.print_exc())
            return None

class Movie(db.Model):
    __tablename__ = 'movie' 

    id = db.Column(db.String(10), primary_key=True)
    title = db.Column(db.String(80), nullable=False, unique=False)
    year = db.Column(db.Integer)
    link = db.Column(db.String(80))
    image = db.Column(db.String(600))
    type = db.Column(db.String(10))
    rating = db.Column(db.Float)

    def store_movie(data):
        try:
            # Ensure all required fields have values (even if empty strings)
            data = {
                "id": data.get("id", ""),
                "name": data.get("name", ""),
                "year": int(data.get("year", "") or 0),
                "type": data.get("type", ""),
                "link": data.get("link", ""),
                "image": data.get("image", ""),
                "rating": float(data.get("rating", 0.0)) if data.get("rating") else None,
            }

            # Check for existing movie
            movie = Movie.query.filter_by(id=data["id"]).first()

            if movie is None:
                # Create a new movie
                movie = Movie(**data)
                db.session.add(movie)
                db.session.commit()
                print(f"Stored movie: {movie}")
            else:
                # Update existing movie with data (excluding empty strings)
                for field, value in data.items():
                    if value:  # Update only if data has a value (not empty string)
                        setattr(movie, field, value)
                db.session.commit()
                print(f"Updated movie: {movie}")

            return movie

        except IntegrityError as e:
            # Handle potential duplicate key errors (e.g., unique constraint violation)
            print(f"Error storing/updating movie: {e}")
            return None  # Or raise a more specific exception

        except Exception as e:
            # Catch other unexpected errors
            print(traceback.print_exc())
            return None  # Or raise a more specific exception

class Scrapped(db.Model):
    __tablename__ = 'scrapped' 

    id = db.Column(db.String(10), primary_key=True)
    type = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now())

    def store_scrapped(self, data):
        try:
            scrapped = Scrapped.query.filter_by(id=data["id"]).first()

            if not scrapped:
                scrapped = Scrapped(id=data["id"], type=data["type"])
                db.session.add(scrapped)
                db.session.commit()
                print(f"Stored scrapped: {scrapped}")
                return scrapped
            else:
                scrapped.updated_at = db.func.now()
                db.session.commit()
                print(f"Updated scrapped: {scrapped}")
                return scrapped
        except Exception as e:
            print(f"Error storing scrapped: {traceback.print_exc()}")
            return None
        
    def get_scrapped(self, id):
        scrapped = Scrapped.query.filter_by(id=id).first()
        return scrapped
    
class CelebRole(db.Model):
    __tablename__ = 'celeb_role' 
    
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Enum(CelebRoles), unique=True, nullable=False)

class MovieCelebRole(db.Model):
    __tablename__ = 'movie_celeb_role' 

    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), primary_key=True)
    celeb_id = db.Column(db.Integer, db.ForeignKey('celeb.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('celeb_role.id'), primary_key=True)
    movie = db.relationship('Movie', backref=db.backref('movie_celeb_role', cascade='all, delete-orphan'))
    celeb = db.relationship('Celeb', backref=db.backref('movie_celeb_role', cascade='all, delete-orphan'))
    role = db.relationship('CelebRole', backref=db.backref('movie_celeb_role', cascade='all, delete-orphan'))

    def store_movie_celeb_role(self, movie, celeb, role_id):
        try:
            movie_celeb_role = MovieCelebRole.query.filter_by(movie_id=movie.id, celeb_id=celeb.id, role_id=role_id).first()
            if not movie_celeb_role:
                movie_celeb_role = MovieCelebRole(movie_id=movie.id, celeb_id=celeb.id
                                                    , role_id=role_id)
                db.session.add(movie_celeb_role)
                db.session.commit()
                print(f"Stored movie_celeb_role: {movie_celeb_role}")
                return movie_celeb_role
            else:
                print(f"Movie Celeb Role already exists")
                return movie_celeb_role
        except Exception as e:
            print(f"Error storing movie celeb role: {traceback.print_exc()}")
            return None
        