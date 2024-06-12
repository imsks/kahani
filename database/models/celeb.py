from app import db

class Celeb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    image = db.Column(db.String(200))

    def store_celeb(data):
        if data["type"] != "Celeb":
            return None  # Skip non-celeb entries

        celeb = Celeb.query.filter_by(id=data["id"]).first()
        if not celeb:
            celeb = Celeb(id=data["id"], name=data["name"], image=data["image"])
            db.session.add(celeb)

        try:
            db.session.commit()
            return celeb
        except Exception as e:
            print(f"Error storing celeb: {e}")
            return None