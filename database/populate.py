from sqlalchemy import inspect
from database.models import Celeb, CelebRole, Movie, MovieCelebRole, Scrapped
from utils.contants import CelebRoles

class PopulateDB:
    def __init__(self, db):
        self.db = db

    def init_populate(self):
        self.create_tables([Movie, Celeb, CelebRole, Scrapped, MovieCelebRole])
        self.populate_celeb_role()

    def populate_celeb_role(self):
        existing_roles = CelebRole.query.all()

        if existing_roles:
            print("CelebRole table already populated. Skipping...")
            return

        for role in CelebRoles:
            new_role = CelebRole(role=role)
            self.db.session.add(new_role)

        self.db.session.commit()
        print("CelebRole table populated successfully!")


    def create_tables(self, models):
        for model in models:
            if not inspect(self.db.engine).has_table(model.__tablename__):
                print(f"{model.__tablename__} table not found. Creating...")
                self.db.metadata.create_all(self.db.engine, [model])
                print(f"{model.__tablename__} table created successfully!")
            else:
                print(f"{model.__tablename__} table already exists. Skipping...")