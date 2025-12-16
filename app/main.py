from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

from contextlib import asynccontextmanager
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.utils import Output, DocumentService, QdrantService
import os

# Initialize services
doc_service = DocumentService()
qdrant_service = QdrantService(k=3)  # Return top 3 similar documents

# Global variable to track if services are initialized
services_initialized = False

_PROJECT_ROOT = os.environ.get("PROJECT_ROOT")
DEFAULT_PDF_PATH = os.path.join(_PROJECT_ROOT, "docs", "laws.pdf")


def initialize_services():
    """Initialize the document and vector services"""
    global services_initialized
    if not services_initialized:
        try:
            # Check if OpenAI API key is available
            if not os.environ.get("OPENAI_API_KEY"):
                raise ValueError("OPENAI_API_KEY environment variable is required")

            # Load documents from PDF
            docs = doc_service.create_documents()
            if not docs:
                raise ValueError("No documents could be loaded from the PDF")

            # Connect to Qdrant and load documents
            qdrant_service.connect()
            qdrant_service.load(docs)

            services_initialized = True
            print(f"Services initialized successfully with {len(docs)} documents")

        except Exception as e:
            print(f"Error initializing services: {e}")
            raise e


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up...")
    initialize_services()
    yield
    # Shutdown
    print("Shutting down...")


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ask", response_model=Output)
async def ask(q: str = Query(..., description="User query string about laws")):
    """
    Query the legal database using natural language.
    """
    try:
        # Process the query using QdrantService
        result = qdrant_service.query(q)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@app.get("/documents/laws")
def get_laws_pdf():
    return FileResponse(DEFAULT_PDF_PATH, media_type="application/pdf")
