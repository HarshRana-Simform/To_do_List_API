from .connection import engine, Base

# Run the file using : python -m To_do_app.database.create_db_table


def create_db_tables():
    from To_do_app.models.todo_models import Todos, test_table

    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    print("Creating Database Tables >>>")
    create_db_tables()
