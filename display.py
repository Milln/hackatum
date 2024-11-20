from IPython.display import Markdown


INTERACTION_TEMPLATE = """
## User query

{user_message}

## Chatbot Reponse

{response}

## Query

This was generated using the following query

```sql
{sql_query}
```
"""

def print_markdown(markdown: str) -> None:
    display(Markdown(markdown))

def print_interaction(user_message: str, response: str, metadata: dict) -> None:
    print_markdown(
        INTERACTION_TEMPLATE.format(
            user_message=user_message,
            response=response,
            sql_query=metadata.get("sql_query"),
        )
    )
