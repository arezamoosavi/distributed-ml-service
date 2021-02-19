import sqlalchemy

from sqlalchemy import inspect
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, BigInteger, DateTime, MetaData, Text
from sqlalchemy.sql import text, func

engine = create_engine(
    "mysql+mysqldb://{0}:{1}@{2}:{3}/{4}?charset=utf8mb4".format(
        "mainuser", "mainpass", "mysql", 3306, "maindb"
    )
)

metadata = MetaData()

dataset = Table(
    "dataset",
    metadata,
    Column("id", BigInteger, primary_key=True),
    Column("created_at", DateTime(timezone=True), nullable=True, default=func.now()),
    Column("dataset_id", Text, nullable=True, default=""),
    Column("hash_id", Text, nullable=True, default=""),
)


model_training = Table(
    "model_training",
    metadata,
    Column("id", BigInteger, primary_key=True),
    Column("model_id", BigInteger, nullable=True, default=""),
    Column("dataset_id", Text, nullable=True, default=""),
    Column("model_type", Text, nullable=True, default=""),
    Column("class_column", Text, nullable=True, default=""),
    Column("result", Text, nullable=True, default=""),
    Column("started", DateTime(timezone=True), nullable=True, default=""),
    Column("finished", DateTime(timezone=True), nullable=True, default=""),
)


metadata.create_all(engine)
inspector = inspect(engine)


def insert_json_data(data, table_name):
    with engine.connect() as con:

        statement = lambda x: text(
            """INSERT INTO {}({}) VALUES(:{})""".format(
                table_name, ",  ".join(x), ", :".join(x)
            )
        )

        con.execute(statement(data), **data)


def get_data_if_exists(field_val: dict, table_name: str):
    with engine.connect() as con:

        query = """SELECT * FROM {} WHERE {} = '{}'""".format(
            table_name, field_val["field"], field_val["val"]
        )
        result = con.execute(query).first()

        print("\n \n results: ", dict(result.items()), "\n \n")

        return dict(result.items()) if result else None
