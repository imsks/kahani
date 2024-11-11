import traceback
from flask_sqlalchemy import SQLAlchemy
from utils.contants import CelebRoles
from utils.functions import is_real_value

db = SQLAlchemy()

class Celeb(db.Model):
    __tablename__ = 'celeb'

    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(200))

    def store_celeb(self, data):
        if data["type"] != "Celeb":
            return None

        try:
            celeb = Celeb.query.filter_by(id=data["id"]).first()
            if not celeb:
                celeb = Celeb(id=data["id"], name=data["name"], image=data["image"])
                db.session.add(celeb)
            else:
                if not celeb.name and is_real_value(data.get("name")):
                    celeb.name = data["name"]
                if not celeb.image and is_real_value(data.get("image")):
                    celeb.image = data["image"]
                
            db.session.commit()
            print(f"Stored celeb: {celeb}")
            return celeb
        except Exception:
            print(traceback.format_exc())
            return None

class Movie(db.Model):
    __tablename__ = 'movie' 

    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(600))
    year = db.Column(db.Integer)
    link = db.Column(db.String(80))
    poster = db.Column(db.String(600))
    type = db.Column(db.String(10))
    rating = db.Column(db.Float)
    runtime = db.Column(db.String(80))
    director = db.Column(db.String(80))
    writer = db.Column(db.String(80))

    celebs = db.relationship('Celeb', secondary='movie_celeb_role', back_populates='movies')
    genres = db.relationship('Genre', secondary='movie_genre', back_populates='movies')
    streaming_on = db.relationship('StreamingService', secondary='movie_streaming_service', back_populates='movies')
    
    def store_movie(self, data):
        try:
            movie = Movie.query.filter_by(id=data["id"]).first()
            if not movie:
                movie = Movie(id=data["id"], name=data["name"])
                db.session.add(movie)
                
            # Update fields if necessary
            for field in ["description", "year", "type", "rating", "link", "poster", "director", "writer", "runtime"]:
                if not getattr(movie, field) and is_real_value(data.get(field)):
                    setattr(movie, field, data.get(field))

            # Store related data
            for celeb_data in data.get("celebs", []):
                celeb = Celeb().store_celeb(celeb_data)
                if celeb:
                    movie.celebs.append(celeb)

            for genre_data in data.get("genres", []):
                genre = Genre().store_genre(genre_data)
                if genre:
                    movie.genres.append(genre)

            for streaming_service_data in data.get("streaming_on", []):
                streaming_service = StreamingService().store_streaming_service(streaming_service_data)
                if streaming_service:
                    movie.streaming_on.append(streaming_service)
            
            db.session.commit()
            print(f"Stored movie: {movie}")
            return movie
        except Exception:
            print(traceback.format_exc())
            return None
        
class Genre(db.Model):
    __tablename__ = 'genre' 
    
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(80), unique=True, nullable=False)
    
    def store_genre(self, genre):
        try:
            genre_obj = Genre.query.filter_by(genre=genre).first()
            if not genre_obj:
                genre_obj = Genre(genre=genre)
                db.session.add(genre_obj)
                db.session.commit()
                print(f"Stored genre: {genre_obj}")
            return genre_obj
        except Exception:
            print(f"Error storing genre: {traceback.format_exc()}")
            return None

class MovieGenre(db.Model):
    __tablename__ = 'movie_genre'

    movie_id = db.Column(db.String(10), db.ForeignKey('movie.id'), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), primary_key=True)

class StreamingService(db.Model):
    __tablename__ = 'streaming_service' 
    
    id = db.Column(db.Integer, primary_key=True)
    service = db.Column(db.String(80), unique=True, nullable=False)
    
    def store_streaming_service(self, service):
        try:
            service_obj = StreamingService.query.filter_by(service=service).first()
            if not service_obj:
                service_obj = StreamingService(service=service)
                db.session.add(service_obj)
                db.session.commit()
                print(f"Stored streaming service: {service_obj}")
            return service_obj
        except Exception:
            print(f"Error storing streaming service: {traceback.format_exc()}")
            return None

class MovieStreamingService(db.Model):
    __tablename__ = 'movie_streaming_service'

    movie_id = db.Column(db.String(10), db.ForeignKey('movie.id'), primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('streaming_service.id'), primary_key=True)

class CelebRole(db.Model):
    __tablename__ = 'celeb_role' 
    
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Enum(CelebRoles), unique=True, nullable=False)

class MovieCelebRole(db.Model):
    __tablename__ = 'movie_celeb_role'

    movie_id = db.Column(db.String(10), db.ForeignKey('movie.id'), primary_key=True)
    celeb_id = db.Column(db.String(10), db.ForeignKey('celeb.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('celeb_role.id'), primary_key=True)

    def store_movie_celeb_role(self, movie_id, celeb_id, role_id):
        try:
            role = MovieCelebRole.query.filter_by(movie_id=movie_id, celeb_id=celeb_id, role_id=role_id).first()
            if not role:
                role = MovieCelebRole(movie_id=movie_id, celeb_id=celeb_id, role_id=role_id)
                db.session.add(role)
                db.session.commit()
                print(f"Stored movie_celeb_role: {role}")
            return role
        except Exception:
            print(f"Error storing movie celeb role: {traceback.format_exc()}")
            return None

class Scrapped(db.Model):
    __tablename__ = 'scrapped' 

    id = db.Column(db.String(10), primary_key=True)
    type = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def store_scrapped(self, data):
        try:
            scrapped = Scrapped.query.filter_by(id=data["id"]).first()
            if not scrapped:
                scrapped = Scrapped(id=data["id"], type=data["type"])
                db.session.add(scrapped)
            else:
                scrapped.updated_at = db.func.now()
            db.session.commit()
            print(f"Stored/Updated scrapped: {scrapped}")
            return scrapped
        except Exception:
            print(f"Error storing scrapped: {traceback.format_exc()}")
            return None

    def get_scrapped(self, id):
        return Scrapped.query.filter_by(id=id).first()
