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
                if celeb.name == "" and is_real_value(data.get("name")):
                    celeb.name = data["name"]
                elif celeb.image == "" and is_real_value(data.get("image")):
                    celeb.image = data["image"]
                
            db.session.commit()
            print(f"Stored celeb: {celeb}")
            return celeb
        except Exception as e:
            print(traceback.print_exc())
            return None

class Movie(db.Model):
    __tablename__ = 'movie' 

    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=False)
    description = db.Column(db.String(600))
    year = db.Column(db.Integer)
    link = db.Column(db.String(80))
    poster = db.Column(db.String(600))
    type = db.Column(db.String(10))
    rating = db.Column(db.Float)
    runtime = db.Column(db.String(80))
    director = db.Column(db.String(80))
    writer = db.Column(db.String(80))
    celebs = db.relationship('Celeb', secondary='movie_celeb_role', backref=db.backref('movies', lazy='dynamic'))
    genres = db.relationship('MovieGenre', back_populates='movie')
    streaming_on = db.relationship('StreamingService', secondary='movie_streaming_service', backref=db.backref('movies', lazy='dynamic'))

    def store_movie(self, data):
        try:
            movie = Movie.query.filter_by(id=data["id"]).first()
            if not movie:
                movie = Movie(id=data["id"], 
                              name=data["name"], 
                            )
                movie.description = data.get("description")
                movie.year = data.get("year")
                movie.type = data.get("type")
                movie.rating = data.get("rating")
                movie.link = data.get("link")
                movie.poster = data.get("poster")
                movie.director = data.get("director")
                movie.writer = data.get("writer")
                movie.runtime = data.get("runtime")
                db.session.add(movie)
                
            else:
                if movie.type == "" and is_real_value(data.get("type")):
                    movie.type = data["type"]
                elif movie.rating == "" and is_real_value(data.get("rating")):
                    movie.rating = data["rating"]
                elif movie.year == "" and is_real_value(data.get("year")):
                    movie.year = data["year"]
                elif movie.link == "" and is_real_value(data.get("link")):
                    movie.link = data["link"]
                elif movie.poster == "" and is_real_value(data.get("poster")):
                    movie.poster = data["poster"]
                elif movie.description == "" and is_real_value(data.get("description")):
                    movie.description = data["description"]
                elif movie.director == "" and is_real_value(data.get("director")):
                    movie.director = data["director"]
                elif movie.writer == "" and is_real_value(data.get("writer")):
                    movie.writer = data["writer"]
                elif movie.runtime == "" and is_real_value(data.get("runtime")):
                    movie.runtime = data["runtime"]
            
            # Store celeb data
            celeb_data_list = data.get("celebs", [])
            for celeb_data in celeb_data_list:
                celeb = Celeb().store_celeb(celeb_data)
                if celeb:
                    movie.celebs.append(celeb)

            # Store genre data
            genre_data_list = data.get("genres", [])
            for genre_data in genre_data_list:
                genre = Genre().store_genre(genre_data)
                if genre:
                    movie.genres.append(genre)

            # Store streaming service data
            streaming_service_data_list = data.get("streaming_on", [])
            for streaming_service_data in streaming_service_data_list:
                streaming_service = StreamingService().store_streaming_service(streaming_service_data)
                if streaming_service:
                    movie.streaming_on.append(streaming_service)
            
            db.session.commit()
            print(f"Stored movie: {movie}")
            return movie
        except Exception as e:
            print(traceback.print_exc())
            return None
        
class Genre(db.Model):
    __tablename__ = 'genre' 
    
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(80), unique=True, nullable=False)
    
    def store_genre(self, genre):
        try:
            genre = Genre.query.filter_by(genre=genre).first()
            if not genre:
                genre = Genre(genre=genre)
                db.session.add(genre)
                db.session.commit()
                print(f"Stored genre: {genre}")
                return genre
            else:
                print(f"Genre already exists")
                return genre
        except Exception as e:
            print(f"Error storing genre: {traceback.print_exc()}")
            return None
        
class MovieGenre(db.Model):
    __tablename__ = 'movie_genre'

    movie_id = db.Column(db.String(10), db.ForeignKey('movie.id'), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), primary_key=True)

    # Relationships with Movie and Genre
    movie = db.relationship('Movie', backref=db.backref('movie_genres', cascade='all, delete-orphan', overlaps="genres"))
    genre = db.relationship('Genre', backref=db.backref('movie_genres', cascade='all, delete-orphan', overlaps="genres"))
        
# Create a Streaming Service table
class StreamingService(db.Model):
    __tablename__ = 'streaming_service' 
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    logo = db.Column(db.String(200))
    
    def store_streaming_service(self, service):
        try:
            service = StreamingService.query.filter_by(service=service).first()
            if not service:
                service = StreamingService(service=service)
                db.session.add(service)
                db.session.commit()
                print(f"Stored streaming service: {service}")
                return service
            else:
                print(f"Streaming Service already exists")
                return service
        except Exception as e:
            print(f"Error storing streaming service: {traceback.print_exc()}")
            return None
        
class MovieStreamingService(db.Model):
    __tablename__ = 'movie_streaming_service'

    movie_id = db.Column(db.String(10), db.ForeignKey('movie.id'), primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('streaming_service.id'), primary_key=True)
    link = db.Column(db.String(200))
    
class CelebRole(db.Model):
    __tablename__ = 'celeb_role' 
    
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Enum(CelebRoles), unique=True, nullable=False)

class MovieCelebRole(db.Model):
    __tablename__ = 'movie_celeb_role'

    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), primary_key=True)
    celeb_id = db.Column(db.Integer, db.ForeignKey('celeb.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('celeb_role.id'), primary_key=True)

    def store_movie_celeb_role(self, movie_id, celeb_id, role_id):
        try:
            movie_celeb_role = MovieCelebRole.query.filter_by(movie_id=movie_id, celeb_id=celeb_id, role_id=role_id).first()

            if not movie_celeb_role:
                movie_celeb_role = MovieCelebRole(movie_id=movie_id, celeb_id=celeb_id
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