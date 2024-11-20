from typing import Any, Dict
from llama_index.core import SQLDatabase
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.llms.azure_openai import AzureOpenAI
from sqlalchemy import text

from database import StreamingDatabase


GPT_4O_MINI = AzureOpenAI(
    engine="gpt-4o-mini",
    model="gpt-4o-mini",
    api_version="2024-08-01-preview",
    system_prompt="You are a friendly chat assistant for a streaming service. You have access to a database and can use the provided information.",
)


class DatabaseRetriever:
    def __init__(self, db: StreamingDatabase):
        self.sql_database = SQLDatabase(db.engine)
        self.query_engine = NLSQLTableQueryEngine(
            sql_database=self.sql_database, llm=GPT_4O_MINI
        )

    def prompt_database(self, prompt: str) -> tuple[str, Dict[str, Any]]:
        response = self.query_engine.query(prompt)
        return str(response), response.metadata


if __name__ == "__main__":
    db = StreamingDatabase()
    db.populate_database()
    db_retriever = DatabaseRetriever(db)
    response, metadata = db_retriever.prompt_database("What has Diana Wilson watched?")
    with db.engine.connect() as session:
        rows = session.execute(
            text("""SELECT g.name AS genre_name
                FROM movie m
                JOIN movie_genre mg ON m.id = mg.movie_id
                JOIN genre g ON mg.genre_id = g.id
                WHERE m.name = 'Golden Shadow';""")
        )
        for row in rows:
            print(row)
    print(response)
