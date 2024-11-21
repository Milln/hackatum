from typing import Any, Dict
from llama_index.core import SQLDatabase
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.llms.azure_openai import AzureOpenAI

from database import StreamingDatabase

DEFAULT_SYSTEM_PROMPT = "You are a friendly chat assistant for a streaming service. You have access to a database and can use the provided information."


class DatabaseRetriever:
    def __init__(
        self, db: StreamingDatabase, system_prompt: str = DEFAULT_SYSTEM_PROMPT
    ):
        self.sql_database = SQLDatabase(db.engine)
        self.initialize_retriever(system_prompt)

    def initialize_retriever(self, system_prompt: str):
        self.system_prompt = system_prompt
        self.llm = self.create_llm(system_prompt)
        self.query_engine = NLSQLTableQueryEngine(
            sql_database=self.sql_database, llm=self.llm
        )

    def prompt_database(
        self, prompt: str, user_name: str | None = None
    ) -> tuple[str, Dict[str, Any]]:
        query = prompt
        if user_name:
            query = f"{prompt}. My name is {user_name}."
        response = self.query_engine.query(query)
        return str(response), response.metadata

    def get_system_prompt(self):
        return self.system_prompt

    def set_system_prompt(self, system_prompt: str):
        self.initialize_retriever(system_prompt)

    def create_llm(self, system_prompt: str):
        return AzureOpenAI(
            engine="gpt-4o-mini",
            model="gpt-4o-mini",
            api_version="2024-08-01-preview",
            system_prompt=system_prompt,
        )


if __name__ == "__main__":
    db = StreamingDatabase()
    db.populate_database()
    db_retriever = DatabaseRetriever(db)
    response, metadata = db_retriever.prompt_database("Which users are there?")
    print(response)

    print(db.get_all_users())

    response, metadata = db_retriever.prompt_database(
        "What is Evelyn Wilson view history?"
    )
    print(response, metadata)
