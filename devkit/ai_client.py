import os


def get_api_key():
    api_key = os.environ.get("GROQ_API_KEY")

    if not api_key:
        return None
    return api_key