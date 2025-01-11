from qdrant_client import QdrantClient, models


def push_to_qdrant(client, collection_name, query_vector, natural_language_query, sql_query, response):
    """
    Pushes data to a Qdrant collection.

    Args:
        client (QdrantClient): The Qdrant client object.
        collection_name (str): The name of the Qdrant collection.
        query_vector (list): The vector representation of the natural language query.
        natural_language_query (str): The natural language query itself.
        sql_query (str): The generated SQL query.
    """

    # Create a Qdrant Point object with the data
    point = models.PointStruct(
        id=len(client.scroll(collection_name)) + 1,
        payload={
            "natural_lan_query": natural_language_query,
            "sql_query": sql_query,
            "response": response
        },
        vector=query_vector,
    )

    # Push the data point to the Qdrant collection
    client.upsert(collection_name=collection_name, points=[point])

def initialize_qdrant():
    """Initialize the Qdrant client with an in-memory database and create the collection if it doesn't exist."""
    client = QdrantClient(":memory:")
    if "MovieDB" not in client.get_collections():
        client.create_collection("MovieDB", vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE))
    return client    
