from sqlmodel import SQLModel, Session, create_engine

database_file = 'sqlite3.db'
sqlite_url = f"sqlite:///{database_file}"

engine = create_engine(sqlite_url, echo=True)

def conn():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
