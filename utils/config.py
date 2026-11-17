from pathlib import Path


def load_system_prompt():
    """Load the system prompt from the project-level prompt.txt file."""
    prompt_path = Path(__file__).resolve().parent.parent / "prompt.txt"
    try:
        return prompt_path.read_text(encoding="utf-8").strip()
    except FileNotFoundError as error:
        raise FileNotFoundError(
            "prompt.txt file not found. Please ensure it exists in the solution directory"
        ) from error
    except Exception as error:
        raise RuntimeError(f"Error loading prompt.txt: {error}") from error


def get_system_prompt():
    """Get the system prompt for the technical support assistant."""
    return load_system_prompt()


SYSTEM_PROMPT = get_system_prompt()
