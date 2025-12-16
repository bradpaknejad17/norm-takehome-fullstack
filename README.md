This repository contains a client and server codebase. 

## Server Repository:

# Legal Document Semantic Search Backend

This repository contains the backend service for a semantic search application designed to index and query legal documents. Built with **FastAPI**, it leverages **Qdrant** for vector similarity search to provide relevant answers and citations from a source PDF.

## Overview

The application functions as a Retrieval-Augmented Generation (RAG) system (or Semantic Search engine) with the following workflow:
1.  **Ingestion**: On startup, the system reads a designated PDF file (e.g., `docs/laws.pdf`).
2.  **Indexing**: The document is processed into chunks, converted into vector embeddings, and stored in a Qdrant vector database.
3.  **Querying**: Users can submit natural language queries via the API. The system retrieves the most relevant document sections based on semantic similarity.

## Prerequisites

-   Python 3.12+
-   An OpenAI API Key (required for generating embeddings).
-   A running instance of Qdrant (or local configuration).

## Setup & Configuration

1.  **Environment Variables**
    Create a `.env` file in the root directory and add your OpenAI API key:
    ```bash
    OPENAI_API_KEY=your_api_key_here
    ```

2.  **Installation**
    Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

Start the FastAPI server using uvicorn:

## API Documentation

To interact with the API and execute requests against the `/ask` endpoint, please visit the interactive Swagger UI documentation at:
http://localhost:8000/docs

## Client Repository 

In the `frontend` folder you'll find a light NextJS app with it's own README including instructions to run. Your task here is to build a minimal client experience that utilizes the service build in part 1.

