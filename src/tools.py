# Tools module defining custom tools for the LangChain assistant.
# Includes utility functions and document retrieval tools.

import datetime
import re
from pathlib import Path
from langchain_core.tools import tool


@tool
def obtain_current_date_and_time() -> str:
    """Return the current date and time of the system. Useful if the user asks what day or what time it is."""
    ahora = datetime.datetime.now()
    return f"The current date and time of the system is: {ahora.strftime('%Y-%m-%d %H:%M:%S')}"


@tool
def add_numbers(a: float, b: float) -> float:
    """Add two numbers. Useful for arithmetic questions or quick calculations."""
    return a + b


@tool
def multiply_numbers(a: float, b: float) -> float:
    """Multiply two numbers. Useful when the user asks for products or simple math operations."""
    return a * b


@tool
def read_project_file(file_path: str) -> str:
    """Read a text file from the project folder and return its content. Useful for inspecting code or configuration files."""
    project_root = Path(__file__).resolve().parent.parent
    requested_path = (project_root / file_path).resolve()

    if project_root not in requested_path.parents and requested_path != project_root:
        return "Access denied: the requested path is outside the project folder."

    if not requested_path.exists():
        return f"File not found: {file_path}"

    if not requested_path.is_file():
        return f"The path is not a file: {file_path}"

    try:
        return requested_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return f"The file '{file_path}' is not a UTF-8 text file."


def _get_study_docs_directory() -> Path:
    # Helper function to get the path to the docs directory
    return Path(__file__).resolve().parent.parent / "docs"


def _tokenize_text(text: str) -> set[str]:
    # Tokenize text into lowercase words for keyword matching
    return set(re.findall(r"[a-zA-Z0-9_]+", text.lower()))


@tool
def list_study_documents() -> str:
    """List the study documents available in the local docs folder."""
    docs_directory = _get_study_docs_directory()

    if not docs_directory.exists():
        return "No docs directory was found in the project."

    document_names = sorted(
        file_path.name for file_path in docs_directory.glob("*.md") if file_path.is_file()
    )

    if not document_names:
        return "No study documents are available."

    return "\n".join(document_names)


@tool
def retrieve_study_context(query: str) -> str:
    """Retrieve the most relevant study document snippets for a question using simple keyword matching."""
    docs_directory = _get_study_docs_directory()

    if not docs_directory.exists():
        return "No docs directory was found in the project."

    query_tokens = _tokenize_text(query)

    if not query_tokens:
        return "Please provide a more specific query."

    ranked_sections = []

    for file_path in sorted(docs_directory.glob("*.md")):
        if not file_path.is_file():
            continue

        content = file_path.read_text(encoding="utf-8")
        sections = [section.strip() for section in content.split("\n\n") if section.strip()]

        for section in sections:
            section_tokens = _tokenize_text(section)
            overlap_score = len(query_tokens & section_tokens)

            if overlap_score > 0:
                ranked_sections.append((overlap_score, file_path.name, section))

    if not ranked_sections:
        return "No relevant study context was found for that query."

    ranked_sections.sort(key=lambda item: item[0], reverse=True)
    top_sections = ranked_sections[:3]

    formatted_sections = [
        f"Source: {document_name}\n{section}"
        for _, document_name, section in top_sections
    ]

    return "\n\n---\n\n".join(formatted_sections)
