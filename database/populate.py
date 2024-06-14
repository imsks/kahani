from sqlalchemy import inspect
from database.models import CelebRole
from utils.contants import CelebRoles

class PopulateDB:
    def __init__(self, db):
        self.db = db

    def init_populate(self):
        self.populate_celebRole()

    def populate_celebRole(self):
        if not inspect(self.db.engine).has_table(CelebRole.__tablename__):
            print(f"CelebRole table not found. Skipping population...")
            return

        existing_roles = CelebRole.query.all()
        if existing_roles:
            print("CelebRole table already populated. Skipping...")
            return

        for role in CelebRoles:
            new_role = CelebRole(role=role)
            self.db.session.add(new_role)

        self.db.session.commit()
        print("CelebRole table populated successfully!")