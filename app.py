import streamlit as st
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain.llms import HuggingFacePipeline

def main():
    st.title("Database Query with Mistral-7B 👾")

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

        # Define the prompt
        PROMPT = """ 
                    Given an input question, do the following.
                    1. Create a syntactically correct postgresql query to find the answer to the question.
                    2. Look at the results of the query and return a descriptive answer.
                    == Question: {question}
                    Use the following format:
                    Question: "Question here"
                    SQLQuery: "SQL Query to run"
                    SQLResult: "Result of the SQLQuery"
                    Answer: "Final answer here"
                """

        # Get the query from the user
        query = st.text_area("Enter your query")

        # Submit button
        if st.button("Submit"):
            model_name = "mistralai/Mistral-7B-v0.1"

            # pipe = pipeline(
            #     "text-generation",
            #     model=model,
            #     tokenizer = tokenizer,
            #     torch_dtype=torch.bfloat16,
            #     device_map="auto",
            #     max_new_tokens= max_new_tokens,
            # )
            # llm = HuggingFacePipeline(pipeline=pipe )

            # # Create the SQL query chain
            # db_chain = create_sql_query_chain(llm, db)

            # # Get the response from the LLM
            # response = db_chain.invoke({"question" : query})

            response = """
            You are a PostgreSQL expert. Given an input question, first create a syntactically correct PostgreSQL query to run, then look at the results of the query and return the answer to the input question.
            Unless the user specifies in the question a specific number of examples to obtain, query for at most 5 results using the LIMIT clause as per PostgreSQL. You can order the results to return the most informative data in the database.
            Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in double quotes (") to denote them as delimited identifiers.
            Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
            Pay attention to use CURRENT_DATE function to get the current date, if the question involves "today".

            Use the following format:

            Question: Question here
            SQLQuery: SQL Query to run
            SQLResult: Result of the SQLQuery
            Answer: Final answer here

            Only use the following tables:

            CREATE TABLE movies (
                show_id INTEGER NOT NULL, 
                title VARCHAR(100), 
                director VARCHAR(100), 
                country VARCHAR(20), 
                release_year VARCHAR(20), 
                rating VARCHAR(10), 
                description VARCHAR(1000), 
                CONSTRAINT movies_pkey PRIMARY KEY (show_id)
            )

            /*
            3 rows from movies table:
            show_id	title	director	country	release_year	rating	description
            1	Dick Johnson Is Dead	Kirsten Johnson	United States	2020	PG-13	As her father nears the end of his life, filmmaker Kirsten Johnson stages his death in inventive and
            2	Blood & Water	Robert Cullen	South Africa	2021	TV-MA	After crossing paths at a party, a Cape Town teen sets out to prove whether a private-school swimmin
            3	My Little Pony: A New Generation	Josa Luis Ucha	United States	2021	PG	Equestrias divided. But a bright-eyed hero believes Earth Ponies, Pegasi and Unicorns should be pals
            */

            Question: Which are the movies released in 2021?
            SQLQuery: 
            SELECT title FROM movies WHERE release_year = '2021'
            SQLResult:
            title
            Blood & Water
            My Little Pony: A New Generation
            Answer: Blood & Water and My Little Pony: A New Generation

            Question: Which are the movies released in 2021 and rated PG-13?
            SQLQuery: 
            SELECT title FROM movies WHERE release_year = '2021' AND rating = 'PG-13'
            SQLResult:
            title
            Dick Johnson Is Dead
            Answer: Dick Johnson Is Dead

            Question: Which are the movies released in 2021 and rated PG-13 or TV-MA?
            SQLQuery: 
            SELECT title FROM movies WHERE release_year = '2021' AND (rating = 'PG-13' OR rating = 'TV-MA')
            SQLResult:
            title
            Blood & Water
            Dick Johnson Is Dead
            My Little Pony: A New Generation
            Answer: Blood & Water, Dick Johnson Is Dead and My Little Pony: A New Generation

            Question: Which are the movies released in 2021 and rated PG-1"
            """
            # Display the response
            st.write(response)          

if __name__ == "__main__":
    main()