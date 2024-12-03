import traceback
from sqlalchemy import inspect
from database.models import Celeb, CelebRole, Genre, Movie, MovieCelebRole, MovieGenre, MovieStreamingService, Scrapped, StreamingService
from utils.contants import CelebRoles
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class PopulateDB:
    def __init__(self, db, DATABASE_URL):
        self.db = db
        self.DATABASE_URL = DATABASE_URL

    def create_database(self):
        db_url_parts = self.DATABASE_URL.split('/')
        db_name = db_url_parts[-1]
        db_url_without_db = '/'.join(db_url_parts[:-1])

        conn = psycopg2.connect(db_url_without_db)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname='{db_name}'")
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(f'CREATE DATABASE {db_name}')
        cursor.close()
        conn.close()

    def init_populate(self):
        self.create_database()
        self.create_tables([
            Movie, 
            Celeb, 
            CelebRole, 
            MovieCelebRole, 
            Scrapped, 
            Genre, 
            MovieGenre,
            StreamingService,
            MovieStreamingService,
        ])
        self.populate_celeb_role()

    def populate_celeb_role(self):
        if not inspect(self.db.engine).has_table(CelebRole.__tablename__):
            print(f"{CelebRole.__tablename__} table not found. Creating...")
            self.db.metadata.create_all(self.db.engine, [CelebRole])
            print(f"{CelebRole.__tablename__} table created successfully!")

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
        try:
            for model in models:
                table_name = model.__tablename__
                if not inspect(self.db.engine).has_table(table_name):
                    print(f"{table_name} table not found. Creating...")
                    self.db.metadata.create_all(self.db.engine, [model.__table__])
                    print(f"{table_name} table created successfully!")
                else:
                    print(f"{table_name} table already exists. Skipping...")
        except Exception as e:
            print(f"Error creating tables: {traceback.print_exc(), e}")
            return None