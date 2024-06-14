import traceback
from flask_sqlalchemy import SQLAlchemy
from utils.contants import CelebRoles

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
            print(traceback.print_exc())
            return None

class Movie(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    title = db.Column(db.String(80), nullable=False, unique=False)
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
                              title=data["name"], 
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
                if movie.type == "" and data.get("type"):
                    movie.type = data["type"]
                elif movie.rating == "" and data.get("rating"):
                    movie.rating = data["rating"]
                elif movie.year == "" and data.get("year"):
                    movie.year = data["year"]
                elif movie.link == "" and data.get("link"):
                    movie.link = data["link"]
                elif movie.image == "" and data.get("image"):
                    movie.image = data["image"]
                db.session.commit()
                print(f"Updated movie: {movie}")
            return movie
        except Exception as e:
            print(traceback.print_exc())
            return None

class Scrapped(db.Model):
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