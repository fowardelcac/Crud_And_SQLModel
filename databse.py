from sqlmodel import SQLModel, create_engine

ENGINE = create_engine("mysql+pymysql://root:123@localhost/crud", echo=False)


def create_db_and_tables():
    SQLModel.metadata.create_all(ENGINE)
