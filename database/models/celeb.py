class CelebQuery:
    def __init__(self, db):
        self.db = db
        
    def store_celeb(self, data):
        if data["type"] != "Celeb":
            return None  # Skip non-celeb entries

        celeb = Celeb.query.filter_by(id=data["id"]).first()
        if not celeb:
            celeb = Celeb(id=data["id"], name=data["name"], image=data["image"])
            self.db.session.add(celeb)

        try:
            self.db.session.commit()
            print(f"Stored celeb: {celeb}")
            return celeb
        except Exception as e:
            print(f"Error storing celeb: {e}")
            return None

    def get_celeb(self, celeb_id):
        return self.db.celeb.find_one({"_id": celeb_id})

    def get_celebs(self, celeb_ids):
        return self.db.celeb.find({"_id": {"$in": celeb_ids}})