from typing import Optional
from utils.query import semantic_search


async def function_calling_handler(calling_data, session_id: Optional[str]):
    """
    Handles function calls returned by the assistant during the chat flow.

    Currently supports:
    - "canva_doc_search": Performs a semantic search on instructional Canva markdown pages
      using the query provided in the function arguments. Returns top-matching content chunks
      from the vector store along with their metadata.

    Args:
        calling_data (dict): A dictionary containing the function call data from the assistant.
            Expected structure:
            {
                "name": "<function_name>",
                "arguments": {
                    "query": "<search_query>"
                }
            }

        session_id (Optional[str]): Unique session identifier (reserved for future context tracking; not used currently).

    Returns:
        dict: A function message to be appended to the chat history in the format:
            {
                "role": "function",
                "name": "<function_name>",
                "content": "<search results from function>"
            }

        None: If the function name does not match a supported callable function.

    """

    func_name = calling_data["name"]

    if func_name == "canva_doc_search":
        func_response = semantic_search(calling_data["arguments"]["query"])
        print(func_response)
        return {"role": "function", "name": func_name, "content": func_response}

    return None
