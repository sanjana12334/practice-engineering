from sqlalchemy import text
from url_database import engine

try:
    with engine.connect() as connection:

        result = connection.execute(
            text("SELECT DATABASE()")
        )

        print("MySQL connected successfully!")
        print("Database:", result.scalar())

except Exception as error:
    print("Connection failed:", error)