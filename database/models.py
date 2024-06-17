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
    name = db.Column(db.String(80), nullable=False, unique=False)
    year = db.Column(db.Integer)
    link = db.Column(db.String(80))
    image = db.Column(db.String(600))
    type = db.Column(db.String(10))
    rating = db.Column(db.Float)

    def store_movie(self, data):
        try:
            movie = Movie.query.filter_by(id=data["id"]).first()
            if not movie:
                movie = Movie(id=data["id"], 
                              name=data["name"], 
                            )
                movie.year = data.get("year")
                movie.type = data.get("type")
                movie.rating = data.get("rating")
                movie.link = data.get("link")
                movie.image = data.get("image")
                db.session.add(movie)
                db.session.commit()
                db.session.commit()
                print(f"Stored movie: {movie}")
                
            else:
                if movie.type == "" and is_real_value(data.get("type")):
                    movie.type = data["type"]
                elif movie.rating == "" and is_real_value(data.get("rating")):
                    movie.rating = data["rating"]
                elif movie.year == "" and is_real_value(data.get("year")):
                    movie.year = data["year"]
                elif movie.link == "" and is_real_value(data.get("link")):
                    movie.link = data["link"]
                elif movie.image == "" and is_real_value(data.get("image")):
                    movie.image = data["image"]
                db.session.commit()
                print(f"Updated movie: {movie}")
            return movie
        except Exception as e:
            print(traceback.print_exc())
            return None
    
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