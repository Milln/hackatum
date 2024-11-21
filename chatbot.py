from typing import Any, Dict
from llama_index.core import SQLDatabase
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.llms.azure_openai import AzureOpenAI

from database import CineStreamDatabase

DEFAULT_SYSTEM_PROMPT = """
You are a friendly chat assistant for a movie streaming service called CineStream.

You have access to a database, and can query it to help respond to the users queries.
"""


class CustomerChatbot:
    DEFAULT_SYSTEM_PROMPT = "You are a friendly chat assistant for a streaming service. You have access to a database and can use the provided information."

    def __init__(
        self, db: CineStreamDatabase, system_prompt: str = DEFAULT_SYSTEM_PROMPT
    ):
        self.sql_database = SQLDatabase(db.engine)
        self.initialize_retriever(system_prompt)

    def initialize_retriever(self, system_prompt: str):
        self.system_prompt = system_prompt
        self.llm = self.create_llm(system_prompt)
        self.query_engine = NLSQLTableQueryEngine(
            sql_database=self.sql_database, llm=self.llm
        )

    def chat(
        self, message: str, customer: str | None = None
    ) -> tuple[str, Dict[str, Any]]:
        query = message
        if customer:
            query = f"{message}. My name is {customer}."
        response = self.query_engine.query(query)
        return str(response), response.metadata

    def get_system_prompt(self):
        return self.system_prompt

    def reset_system_prompt(self):
        self.initialize_retriever(self.DEFAULT_SYSTEM_PROMPT)

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
    db = CineStreamDatabase()
    db.populate_database()
    db_retriever = CustomerChatbot(db)
    response, metadata = db_retriever.chat("Which users are there?")
    print(response)

    print(db.get_all_users())

    response, metadata = db_retriever.chat("What is Evelyn Wilson view history?")
    print(response, metadata)
