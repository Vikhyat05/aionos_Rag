from .prompt import prompt as SYSTEM_PROMPT


class Memory:
    """
    A simple in-memory session manager to track and manage chat history
    for multiple sessions using a dictionary-based store.
    """

    def __init__(self):
        """
        Initialize the memory store as an empty dictionary.
        Each session ID maps to a list of message dictionaries.
        """
        self.sessions = {}  # In-memory storage for chat histories

    def initialize_session(self, session_id: str):
        """
        Create a new session with a system prompt.

        Args:
            session_id (str): The unique identifier for the session.
        """
        print(f"Got the System Prompt-----------")
        self.sessions[session_id] = [{"role": "system", "content": SYSTEM_PROMPT}]

    def get_chat_history(self, session_id: str):
        """
        Retrieve the chat history for a given session.

        Args:
            session_id (str): The session ID to fetch history for.

        Returns:
            list: A list of message dictionaries for the session.
                  Returns an empty list if the session doesn't exist.
        """
        return self.sessions.get(session_id, [])

    def update_chat_history(self, session_id: str, message: dict):
        """
        Append a new message to the session's chat history.
        If the session does not exist, it will be initialized.

        Args:
            session_id (str): The session ID to update.
            message (dict): A dictionary representing the new message to add.
                            Example: {"role": "user", "content": "Hello!"}
        """
        if session_id in self.sessions:
            self.sessions[session_id].append(message)
        else:
            self.initialize_session(session_id)
            self.sessions[session_id].append(message)

    def clear_session(self, session_id: str):
        """
        Clear the chat history for a session.

        Args:
            session_id (str): The session ID to remove from memory.
        """
        if session_id in self.sessions:
            self.sessions.pop(session_id, None)


# Singleton instance for global use
memory = Memory()
