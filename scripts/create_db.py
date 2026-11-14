from sqlalchemy import inspect

import app.models  # noqa: F401
from app.database import Base, engine

Base.metadata.create_all(engine)

print("Tabellen in der Datenbank:", inspect(engine).get_table_names())