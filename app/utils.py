from llama_index.core.bridge.pydantic import BaseModel
import qdrant_client
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core.schema import Document
from llama_index.core import VectorStoreIndex, Settings
from llama_index.core.node_parser import SentenceWindowNodeParser
from llama_index.core.query_engine import CitationQueryEngine
from dataclasses import dataclass
import os
from app.pdf_reader import PDFPlumberExtractor
from app.pdf_parser import CustomPDFParser
from dotenv import load_dotenv

load_dotenv()

key = os.environ["OPENAI_API_KEY"]
_PROJECT_ROOT = os.environ.get("PROJECT_ROOT")
DEFAULT_PDF_PATH = os.path.join(_PROJECT_ROOT, "docs", "laws.pdf")


@dataclass
class Input:
    query: str
    file_path: str


@dataclass
class Citation:
    source: str
    text: str


class Output(BaseModel):
    query: str
    response: str
    citations: list[Citation]


class DocumentService:
    def __init__(self, pdf_path: str = DEFAULT_PDF_PATH):
        self.pdf_reader = PDFPlumberExtractor(pdf_path)

    def nodes_to_documents(self, nodes, path=None) -> list[Document]:
        docs = []
        path = path or []

        for node in nodes:
            new_path = path + [node.title]

            section_text = node.title
            if node.content:
                section_text += "\n" + "\n".join(node.content)

            doc = Document(
                text=section_text,
                metadata={
                    "section": node.title,
                    "path": new_path,
                    "depth": node.depth,
                },
            )
            docs.append(doc)

            if node.children:
                docs.extend(self.nodes_to_documents(node.children, new_path))

        return docs

    def create_documents(self) -> list[Document]:
        raw_text = self.pdf_reader.extract_text()
        parser = CustomPDFParser(raw_text)
        nodes = parser.parse()
        return self.nodes_to_documents(nodes)


def clean_section_title(meta: dict) -> str:
    section = (meta.get("section") or "").strip().rstrip(".")

    # If it’s a decent label, use it
    if len(section) > 3:
        return section

    # Otherwise fall back to last item in path
    path = meta.get("path") or []
    if path:
        fallback = str(path[-1]).strip()
        if len(fallback) > 2:
            return fallback

    return "Unknown Section"


class QdrantService:
    def __init__(self, k: int = 5):
        self.index = None
        self.k = k

    def connect(self) -> None:
        # KEEP IN-MEMORY — as requested
        client = qdrant_client.QdrantClient(path=":memory:")
        vstore = QdrantVectorStore(client=client, collection_name="temp")

        Settings.embed_model = OpenAIEmbedding(api_key=key)
        Settings.llm = OpenAI(api_key=key, model="gpt-4")

        self.index = VectorStoreIndex.from_vector_store(vstore)

    def load(self, docs: list[Document]) -> None:
        if self.index is None:
            raise RuntimeError("Call connect() before load().")

        parser = SentenceWindowNodeParser.from_defaults(
            window_size=5,  # richer chunk context
        )

        nodes = parser.get_nodes_from_documents(docs)
        self.index.insert_nodes(nodes)

    def query(self, query_str: str) -> Output:
        if self.index is None:
            raise RuntimeError("Call connect() before query().")

        try:
            query_engine = CitationQueryEngine.from_args(
                self.index,
                similarity_top_k=self.k,
                citation_chunk_size=200,
            )

            response = query_engine.query(query_str)

            citations = []
            if hasattr(response, "source_nodes") and response.source_nodes:
                for node in response.source_nodes:
                    label = clean_section_title(node.metadata or {})

                    snippet = (
                        node.text[:200] + "..." if len(node.text) > 200 else node.text
                    )

                    citations.append(Citation(source=label, text=snippet))

            return Output(
                query=query_str,
                response=str(response.response),
                citations=citations,
            )

        except Exception as e:
            return Output(
                query=query_str,
                response=f"Error processing query: {str(e)}",
                citations=[],
            )


if __name__ == "__main__":
    doc_service = DocumentService()
    docs = doc_service.create_documents()
    print(f"Created {len(docs)} docs.")

    index = QdrantService()
    print("Connecting…")
    index.connect()
    print("Connected.")

    print("Loading documents…")
    index.load(docs)
    print("Loaded.")

    result = index.query("what happens if I steal?")
    print(result)
    input("wait")
