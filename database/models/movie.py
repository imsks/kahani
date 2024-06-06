from app import db

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    year = db.Column(db.Integer)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=False)
    genre = db.relationship('Genre')

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'year': self.year,
            'genre': self.genre.name
        }
