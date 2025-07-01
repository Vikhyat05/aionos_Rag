"""
List of OpenAI function-calling definitions used by the Canva assistant.

Currently includes:
- canva_doc_search: A semantic search function for answering questions related to using Canva.

Function Purpose:
- Enables the assistant to respond to Canva-related queries by retrieving relevant content
  from parsed instructional Markdown documents stored in a Supabase vector store.

Structure:
- name (str): The function identifier used by the assistant.
- description (str): When and why the assistant should call this function.
- parameters (dict):
    - type (str): Must be "object".
    - properties (dict): Defines accepted fields (currently only "query").
    - required (list): Specifies mandatory fields (["query"]).

Usage:
- This function is triggered by OpenAI's function-calling interface when the user asks
  a Canva usage question (e.g., editing a template, using tools, exporting designs).
- The result is handled by `function_calling_handler` and used to construct a grounded, step-by-step response.

Note:
- Each returned document chunk includes `content`, `metadata` (with source page), and a similarity score.
- The assistant should cite the source pages at the end of the response for traceability.
"""

functions = [
    {
        "name": "canva_doc_search",
        "description": (
            "Call this function whenever the user asks a question about how to use Canva "
            "(e.g., how to select a template, edit text, navigate the interface, export designs). "
            "It runs a semantic search against the Supabase vector store that contains parsed instructional "
            "Markdown content from Canva guides and returns the top-matching text chunks. "
            "The function accepts only the user’s query string and returns a list of dictionaries "
            "(each with content, metadata such as page number, and similarity score)."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The Canva-related question or action the user wants to perform.",
                }
            },
            "required": ["query"],
        },
    }
]
