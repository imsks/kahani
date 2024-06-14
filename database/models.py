from flask_sqlalchemy import SQLAlchemy
from utils.contants import CelebRoles, SearchItemType

db = SQLAlchemy()

class Celeb(db.Model):
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
            print(f"Error storing celeb: {e}")
            return None

class Movie(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    title = db.Column(db.String(80), nullable=False, unique=False)
    year = db.Column(db.Integer)
    type = db.Column(db.String(10))
    rating = db.Column(db.Float)

    def store_movie(self, data):
        if data["type"] != SearchItemType.MOVIE.value and data["type"] != SearchItemType.TV_SHOW.value:
            return None

        movie = Movie.query.filter_by(id=data["id"]).first()
        if not movie:
            movie = Movie(id=data["id"], title=data["name"], year=data["year"], type=data["type"])
            db.session.add(movie)
            db.session.commit()
            print(f"Stored movie: {movie}")

        try:
            db.session.commit()
            print(f"Stored movie: {movie}")
            return movie
        except Exception as e:
            print(f"Error storing movie: {e}")
            return None

class Scrapped(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    type = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now())

    def store_scrapped(self, data):
        scrapped = Scrapped.query.filter_by(id=data["id"]).first()

        try:
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
            print(f"Error storing scrapped: {e}")
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