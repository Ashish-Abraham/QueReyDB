import os
import streamlit as st
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from qdrant_util import push_to_qdrant, initialize_qdrant
from langchain_community.vectorstores import Qdrant
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from qdrant_client import QdrantClient, models
from dotenv import load_dotenv
load_dotenv()

client = initialize_qdrant()  

def format_query_results(llm, query, sql_query, results):
    """Use the LLM to format the query results in a user-friendly way"""
    formatting_prompt = f"""You are a helpful SQL tool. Format the following query and results in a clear, professional way.
    Original question: {query}
    SQL Query used: {sql_query}
    Query results: {results}
    
    Present this information in a clear way that:
    1. Shows the SQL query used (formatted nicely)
    2. Results like the interface of an SQL query tool
    3move the function . If relevant, provides any additional insights about the data
    
    Keep the tone professional like a tool"""

    formatted_response = llm.invoke(formatting_prompt)
    return formatted_response.content

def main():
    st.markdown(
        """
        <h1 style="text-align: center;">QueReyDB</h1>
        <h3 style="text-align: center;">powered by 🔸MistralAI🔸</h3>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        username = st.text_input("Enter the database username")
        password = st.text_input("Enter the database password", type="password")
        host = st.text_input("Enter the database host")

    with col2:
        port = st.text_input("Enter the database port")
        mydatabase = st.text_input("Enter the database name")

    if username and password and host and port and mydatabase:
        try:
            pg_uri = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{mydatabase}"
            db = SQLDatabase.from_uri(pg_uri)
            context = db.get_context()
            st.success("Database connection successful!")

            query = st.text_area("Enter your query")
            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))
            encoder = OpenAIEmbeddings(model="text-embedding-3-small", api_key=os.getenv("OPENAI_API_KEY"))

            examples = [
                {"input": "List all movies with a rating higher than 8.5.", "query": "SELECT * FROM Movies WHERE Rating > 8.5;"},
                {"input": "List all genres available in the database.", "query": "SELECT * FROM Genres;"},
                {"input": "Find all movies released in the year 2020.", "query": "SELECT * FROM Movies WHERE ReleaseYear = 2020;"},
                {"input": "Find the total duration of all tracks.", "query": "SELECT SUM(Milliseconds) FROM Track;"},
                {"input": "List all customers from Canada.", "query": "SELECT * FROM Customer WHERE Country = 'Canada';"},
                {"input": "How many tracks are there in the album with ID 5?", "query": "SELECT COUNT(*) FROM Track WHERE AlbumId = 5;"},
                {"input": "Find the total number of invoices.", "query": "SELECT COUNT(*) FROM Invoice;"},
                {"input": "List all tracks that are longer than 5 minutes.", "query": "SELECT * FROM Track WHERE Milliseconds > 300000;"},
            ]

            example_prompt = PromptTemplate.from_template("User input: {input}\nSQL query: {query}")
            prompt = FewShotPromptTemplate(
                examples=examples,
                example_prompt=example_prompt,
                prefix="You are a {dialect} expert. Given an input question, create a syntactically correct {dialect} query to run. Unless otherwise specified, do not return more than {top_k} rows.\n\nHere is the relevant table info: {table_info}\n\nBelow are a number of examples of questions and their corresponding SQL queries.",
                suffix="User input: {input}\nSQL query: ",
                input_variables=["dialect", "input", "top_k", "table_info"],
            )

            if st.button("Submit"):
                if query.strip():
                    query_vector = encoder.embed_query(query)
                    hits = client.search(collection_name="MovieDB", query_vector=query_vector, limit=1)

                    if hits and hits[0].score > 0.90:
                        st.success("Result found in search history:")
                        st.write(hits[0].payload.response)
                    else:
                        db_chain = create_sql_query_chain(llm=llm, db=db, prompt=prompt, k=2)
                        response = db_chain.invoke({"question": query, "dialect": "PostgreSQL", "top_k": 3})

                        st.success("Result from the database:")
                        result = db.run(response.replace('```sql', '').replace('```', '').strip())
                        formatted_result = format_query_results(llm,query,response,result)
                        st.write(formatted_result)
                        push_to_qdrant(client, "MovieDB", query_vector, query, response, formatted_result)
                else:
                    st.warning("Please enter a valid query.")
        except Exception as e:
            st.error(f"Failed to connect to the database: {e}")

if __name__ == "__main__":
    st.set_page_config(page_title="QueReyDB", layout="wide")
    main()


# Model and vector settings
                # model_name = "meta-llama/Llama-3.2-1B"
                # llm = load_llm(model_name)  # Load the LLM
# encoder = SentenceTransformer('BAAI/bge-small-en')
# # Perform a vector search on the Qdrant client
                        # query_vector = encoder.encode(query).tolist()     
