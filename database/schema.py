from database.database import init_db


def create_tables():
    init_db()
    print("Database tables created successfully")


if __name__ == "__main__":
    create_tables()
