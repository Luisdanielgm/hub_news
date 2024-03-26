import argparse
import os
from typing import List

import google.generativeai as genai
import chromadb
from chromadb.utils import embedding_functions

model = genai.GenerativeModel("gemini-pro")


def build_prompt(query: str, context: List[str]) -> str:
    """
    Crea un mensaje para el LLM. #

    Esta función crea un mensaje para el LLM. Toma la consulta original,
    y el contexto devuelto, y le pide al modelo que responda la pregunta basándose únicamente
    en lo que está en el contexto, no en lo que está en sus pesos.

    Args:
    query (str): La consulta original.
    context (List[str]): El contexto de la consulta, devuelto mediante la búsqueda integrada.

    Returns:
    Ub prompt para el LLM (str).
    """

    base_prompt = {
        "content": "Te voy a hacer una pregunta que me gustaría que respondieras."
        " basado únicamente en el contexto proporcionado y no en ninguna otra información."
        " Si no hay suficiente información en el contexto para responder la pregunta,"
        ' Di "No estoy seguro", luego intenta hacer una suposición.'
        " Divide tu respuesta en párrafos agradables de leer.",
    }
    user_prompt = {
        "content": f" La pregunta es '{query}'. Aquí está todo el contexto que tienes.:"
        f'{(" ").join(context)}',
    }

    # combine the prompts to output a single prompt string
    system = f"{base_prompt['content']} {user_prompt['content']}"

    return system


def get_gemini_response(query: str, context: List[str]) -> str:
    """
    Consulta la API de Gemini para obtener una respuesta a la pregunta.

    Args:
    query (str): La consulta original.
    context (List[str]): El contexto de la consulta, devuelto mediante la búsqueda integrada.

    Returns:
    Una respuesta a la pregunta.
    """

    response = model.generate_content(build_prompt(query, context))

    return response.text


def main(
    collection_name: str = "documents_collection", persist_directory: str = "."
) -> None:
    # Check if the GOOGLE_API_KEY environment variable is set. Prompt the user to set it if not.
    google_api_key = None
    if "API_GEMINI" not in os.environ:
        gapikey = input("Please enter your Google API Key: ")
        genai.configure(api_key=gapikey)
        google_api_key = gapikey
    else:
        google_api_key = os.environ["API_GEMINI"]

    # Instantiate a persistent chroma client in the persist_directory.
    # This will automatically load any previously saved collections.
    # Learn more at docs.trychroma.com
    client = chromadb.PersistentClient(path=persist_directory)

    # create embedding function
    embedding_function = embedding_functions.GoogleGenerativeAiEmbeddingFunction(api_key=google_api_key, task_type="RETRIEVAL_QUERY")

    # Get the collection.
    collection = client.get_collection(
        name=collection_name, embedding_function=embedding_function
    )

    # We use a simple input loop.
    while True:
        # Get the user's query
        query = input("Query: ")
        if len(query) == 0:
            print("Please enter a question. Ctrl+C to Quit.\n")
            continue
        print("\nThinking...\n")

        # Query the collection to get the 5 most relevant results
        results = collection.query(
            query_texts=[query], n_results=5, include=["documents", "metadatas"]
        )

        sources = "\n".join(
            [
                f"{result['filename']}: line {result['line_number']}"
                for result in results["metadatas"][0]  # type: ignore
            ]
        )

        # Get the response from Gemini
        response = get_gemini_response(query, results["documents"][0])  # type: ignore

        # Output, with sources
        print(response)
        print("\n")
        print(f"Source documents:\n{sources}")
        print("\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Load documents from a directory into a Chroma collection"
    )

    parser.add_argument(
        "--persist_directory",
        type=str,
        default="chroma_storage",
        help="The directory where you want to store the Chroma collection",
    )
    parser.add_argument(
        "--collection_name",
        type=str,
        default="documents_collection",
        help="The name of the Chroma collection",
    )

    # Parse arguments
    args = parser.parse_args()

    main(
        collection_name=args.collection_name,
        persist_directory=args.persist_directory,
    )