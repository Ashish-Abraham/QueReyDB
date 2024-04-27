import streamlit as st
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from llm_loader import load_llm  # Import the LLM loader
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

            # ... rest of your code ...

if __name__ == "__main__":
    main()
