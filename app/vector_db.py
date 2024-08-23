from qdrant_client import QdrantClient, models
from qdrant_client.models import Distance, VectorParams, PointStruct
from qdrant_client.http.exceptions import UnexpectedResponse
from sentence_transformers import SentenceTransformer
import os
import uuid
from app.classifier import classify_website

# Initialize Qdrant client
client = QdrantClient(
    host=os.getenv("QDRANT_HOST", "qdrant"),
    port=int(os.getenv("QDRANT_PORT", 6333))
)

# Initialize transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Collection name
collection_name = "websites"


# Ensure the collection exists
def ensure_collection_exists():
    try:
        client.get_collection(collection_name)
    except UnexpectedResponse as e:
        if "not found" in str(e).lower():
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=model.get_sentence_embedding_dimension(),
                    distance=Distance.COSINE
                )
            )
        else:
            raise e


# Ensure the collection is created on module load
ensure_collection_exists()


# Function to store a vector
def store_vector(content: str, url: str, category: str):
    # Check if the URL is already stored
    existing_points = client.search(
        collection_name=collection_name,
        query_vector=model.encode(url).tolist(),  # Search using the URL vector
        limit=1  # We only need to know if it exists
    )

    # If the URL is already in the collection, return its ID
    if existing_points:
        for point in existing_points:
            if point.payload["url"] == url:
                return point.id

    # If the URL is not stored, generate the vector and store it
    vector = model.encode(content).tolist()
    point_id = str(uuid.uuid4())
    client.upsert(
        collection_name=collection_name,
        points=[
            PointStruct(
                id=point_id,
                vector=vector,
                payload={"url": url, "category": category}
            )
        ]
    )
    return point_id


# Function to search for similar vectors
def search_similar(query: str, limit: int = 5):
    # Generate query vector
    query_vector = model.encode(query).tolist()

    # Search for similar vectors
    search_result = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=limit  # limit the number of search results
    )

    # Extract the category from the query
    query_category = classify_website(query)

    # Filter results by the same category
    filtered_results = [
        {"url": hit.payload["url"], "category": hit.payload["category"], "score": hit.score}
        for hit in search_result
        if hit.payload["category"] == query_category
    ]

    return filtered_results[:limit]

# Example usage
if __name__ == "__main__":
    # Example to store a vector
    sample_content = "Welcome to our news website. Stay updated with the latest headlines and breaking news."
    vector_id = store_vector(sample_content, "https://example-news.com", "News")
    print(f"Stored vector with ID: {vector_id}")

    # Example to search for similar vectors
    search_results = search_similar("Latest news updates")
    print("Search results:", search_results)
