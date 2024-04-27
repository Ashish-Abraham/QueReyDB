from qdrant_client import QdrantClient, models


def push_to_qdrant(client, collection_name, query_vector, natural_language_query, sql_query):
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
        },
        vector=query_vector,
    )

    # Push the data point to the Qdrant collection
    client.upsert(collection_name=collection_name, points=[point])
