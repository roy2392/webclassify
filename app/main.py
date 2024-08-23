from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from app.scraper import scrape_website
from app.classifier import classify_website
from app.vector_db import store_vector, search_similar

import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="transformers.tokenization_utils_base")

app = FastAPI()


# Pydantic model to define the input for the scraping endpoint
class ScrapeRequest(BaseModel):
    urls: List[str]


# Pydantic model to define the input for the search endpoint
class SearchQuery(BaseModel):
    text: str
    limit: int = 5  # Optional: default limit to 5 results


# Endpoint to scrape, classify, and store websites
@app.post("/scrape")
async def scrape_and_classify(request: ScrapeRequest):
    results = []
    for url in request.urls:
        try:
            # Scrape website content
            content = await scrape_website(url)
            if not content:
                raise HTTPException(status_code=404, detail="Content not found")

            # Classify the content
            category = classify_website(content)

            # Store the vector in Qdrant
            vector_id = store_vector(content, url, category)

            # Append the result
            results.append({"url": url, "category": category, "vector_id": vector_id})
        except Exception as e:
            # Append error information if something goes wrong
            results.append({"url": url, "error": str(e)})

    return results


# Endpoint to search for similar websites
@app.post("/search")
async def get_similar_websites(query: SearchQuery):
    try:
        # Search for similar vectors in Qdrant
        search_results = search_similar(query.text, query.limit)
        return search_results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Example root endpoint
@app.get("/")
def read_root():
    return {"message": "Web Classification and Search API"}


# Entry point to run the application directly
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
