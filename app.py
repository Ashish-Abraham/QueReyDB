import streamlit as st
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from llm_loader import load_llm  
from qdrant_util import push_to_qdrant
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient, models


def main():
    # Center the title and subtitle with a blank line in between
    st.markdown("""
    <h1 style="text-align: center;">QueReyDB</h1>
    <h3 style="text-align: center;">powered by 🔸MistralAI🔸</h3>
    """, unsafe_allow_html=True)

    # Add some space between the subtitle and the columns
    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        username = st.text_input("Enter the database username")
        password = st.text_input("Enter the database password", type="password")
        host = st.text_input("Enter the database host")

    with col2:
        port = st.text_input("Enter the database port")
        mydatabase = st.text_input("Enter the database name")

    # Create the database URI and SQLDatabase instance
    if username and password and host and port and mydatabase:
        pg_uri = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{mydatabase}"
        db = SQLDatabase.from_uri(pg_uri)

        # Get the query from the user
        query = st.text_area("Enter your query")

        # Submit button
        if st.button("Submit"):
            model_name = "mistralai/Mistral-7B-v0.1"  # Or any desired model name

            # Load the LLM using the llm_loader
            llm = load_llm(model_name)

            # Create the SQL query chain
            db_chain = create_sql_query_chain(llm, db)

            # Load the sentence transformer model
            encoder = SentenceTransformer('BAAI/bge-small-en')

            # Create a Qdrant client
            client = QdrantClient(":memory:")

            # Search the vector database
            hits = client.search(
                collection_name="MovieDB",
                query_vector=encoder.encode(query).tolist(),
                limit=1,
            )

            if hits[0].score > 0.90:
                # Retrieve the result from the search history
                st.write(hits[0].payload)
            else:
                # Get the response from the LLM
                response = db_chain.invoke({"question": query})

                # Display the response
                st.write(response)

                # Convert the response to a vector and store in the database
                vector = encoder.encode(query).tolist()
                # Push data to Qdrant using the qdrant_util function
                push_to_qdrant(
                    client, "MovieDB", vector, query, response
                )

if __name__ == "__main__":
    main()
