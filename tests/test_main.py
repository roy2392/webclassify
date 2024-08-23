from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Test scraping and storing a valid URL
def test_scrape_and_store():
    response = client.post("/scrape", json={"urls": ["https://example.com"]})
    assert response.status_code == 200
    json_response = response.json()
    assert isinstance(json_response, list)
    assert "url" in json_response[0]
    assert "category" in json_response[0]
    assert "vector_id" in json_response[0]

# Test searching with a valid text query
def test_search():
    response = client.post("/search", json={"text": "sample text", "limit": 5})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Additional tests for edge cases and error handling

# Test scraping with an empty URL list
def test_scrape_empty_url_list():
    response = client.post("/scrape", json={"urls": []})
    assert response.status_code == 200
    assert response.json() == []

# Test scraping with an invalid URL format
def test_scrape_invalid_url():
    response = client.post("/scrape", json={"urls": ["invalid-url"]})
    assert response.status_code == 200
    json_response = response.json()
    assert "error" in json_response[0]
    assert json_response[0]["error"] is not None

# Test scraping a non-existent page
def test_scrape_non_existent_page():
    response = client.post("/scrape", json={"urls": ["https://example.com/non-existent-page"]})
    assert response.status_code == 200
    json_response = response.json()
    assert "error" in json_response[0]

# Test searching with no matching categories
def test_search_no_matching_category():
    response = client.post("/search", json={"text": "non-matching-category-text", "limit": 5})
    assert response.status_code == 200
    json_response = response.json()
    assert isinstance(json_response, list)
    assert len(json_response) == 0  # Expecting no results

# Test searching with a limit of 0
def test_search_limit_zero():
    response = client.post("/search", json={"text": "sample text", "limit": 0})
    assert response.status_code == 200
    json_response = response.json()
    assert isinstance(json_response, list)
    assert len(json_response) == 0  # Expecting no results due to limit 0

# Test scraping with duplicate URLs
def test_scrape_duplicate_urls():
    url = "https://example.com"
    response = client.post("/scrape", json={"urls": [url, url]})
    assert response.status_code == 200
    json_response = response.json()
    assert len(json_response) == 2
    assert json_response[0]["vector_id"] == json_response[1]["vector_id"]  # Should return the same vector ID

# Test scraping and searching with special characters in the URL
def test_scrape_and_search_special_characters():
    special_char_url = "https://example.com/special?chars=<>&#%"
    response = client.post("/scrape", json={"urls": [special_char_url]})
    assert response.status_code == 200
    json_response = response.json()
    assert "url" in json_response[0]
    assert "category" in json_response[0]
    assert "vector_id" in json_response[0]

    search_response = client.post("/search", json={"text": "special characters", "limit": 5})
    assert search_response.status_code == 200
    search_json_response = search_response.json()
    assert isinstance(search_json_response, list)

# Test search endpoint with invalid input
def test_search_invalid_input():
    response = client.post("/search", json={"text": 12345, "limit": "invalid-limit"})
    assert response.status_code == 422  # 422 Unprocessable Entity for invalid input

# Test scraping and searching with a large input text
def test_scrape_and_search_large_input():
    large_text = "A" * 10000  # Large input text
    response = client.post("/scrape", json={"urls": ["https://example.com/large-content"]})
    assert response.status_code == 200
    json_response = response.json()
    assert "url" in json_response[0]
    assert "category" in json_response[0]
    assert "vector_id" in json_response[0]

    search_response = client.post("/search", json={"text": large_text, "limit": 5})
    assert search_response.status_code == 200
    search_json_response = search_response.json()
    assert isinstance(search_json_response, list)

# Test root endpoint
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Web Classification and Search API"}

if __name__ == '__main__':
    test_scrape_and_store()
    test_search()
    test_scrape_empty_url_list()
    test_scrape_invalid_url()
    test_scrape_non_existent_page()
    test_search_no_matching_category()
    test_search_limit_zero()
    test_scrape_duplicate_urls()
    test_scrape_and_search_special_characters()
    test_search_invalid_input()
    test_scrape_and_search_large_input()
    test_root()