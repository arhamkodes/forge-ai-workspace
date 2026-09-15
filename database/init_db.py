from database.connection import Base, engine
from database.models import Workspace


def init_database() -> None:
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")


if __name__ == "__main__":
    init_database()