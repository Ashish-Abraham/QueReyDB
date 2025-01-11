<h1 align="center" style="font-family: 'Dancing Script', cursive; color: #9933FF;">QueReyDB  <img src="images\logo.png"  width=50 height=50/></h1>

<h4 align="center" >RAG (Retrieval Augmented Generation) and vector search to translate natural language into SQL queries for PostgreSQL databases.</h4><br>

<p align="center">
  <img src="images\cover.png" width=500>
</p>

QueReyDB is a solution that revolutionizes the way users interact with databases. By combining the power of natural language processing, large language models, and vector search algorithms, this project empowers users to analyze large databases using intuitive natural language queries.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)

## Overview

Are you struggling with SQL queries and syntax? QueReyDB got you covered!

In the era of big data, efficiently querying and analyzing large databases has become crucial for data professionals. QueReyDB simplifies this process by enabling users to interact with databases using natural language queries. Leveraging the power of Mistral LLM, LangChain framework, and Qdrant vector database, QueReyDB translates natural language queries into accurate SQL queries through Retrieval Augmented Generation (RAG) and vector search techniques.

By integrating vector search capabilities, QueReyDB can retrieve relevant query-SQL pairs from a search history, improving accuracy and efficiency. As more queries are processed, the vector database grows, enhancing overall performance. QueReyDB ensures scalability, low latency, and consistent query execution, empowering users to focus on their analytical problems while it handles the complexities of SQL query generation.

## Features

- **Natural Language Query Translation**: QueReyDB allows users to express their analytical problems using natural language, which is then translated into efficient SQL queries.
- **Vector Search Integration**: The project utilizes vector search techniques to retrieve relevant query-SQL pairs from a search history, improving query translation accuracy and efficiency.
- **Incremental Learning**: As more queries are processed, QueReyDB's vector database grows, increasing the likelihood of finding relevant historical data for future queries and enhancing overall performance.
- **Scalability and Low Latency**: By leveraging vector search and reducing the load on the LLM, QueReyDB can handle a high volume of queries concurrently with low latency.
- **Consistency**: QueReyDB ensures consistent query execution by retrieving SQL queries from the search history for similar queries, maintaining consistency in query translation.

## Workflow
<p align="center">
  <img src="images\Workflow.png" width=500>
</p>

## Installation

----------------
### Prerequisite
- Python3
- GPU support for Mistral-7B LLM
-----------------

1. Clone the repository:


   ```bash
   git clone https://github.com/your-username/QueReyDB.git
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up the PostgreSQL database connection by using a cloud-hosted service or PGAdmin locally.

## Usage

- Start the QueReyDB application:
   ```bash
   streamlit run app.py
   ```

- Open the web interface in your preferred browser.
<p align="center">
  <img src="images\Untitled.png" width=600>
</p>
<p align="center">
  <img src="images\Untitled-2.png" width=600>
</p>

Find the medium [article](https://medium.com/@ashishabraham02/exploring-vector-search-for-sql-databases-0f5be67aff57) also. 

## Contributing
- Create a branch for your changes.
- Open a pull request.

   
