from transformers import pipeline

#  init a zero-shot classification pipeline via huggin face transformers
classifier = pipeline("zero-shot-classification", model="valhalla/distilbart-mnli-12-1")

# a closed predefined of categories list based on Google Ads API verticals
categories = [
    "Arts & Entertainment",
    "Autos & Vehicles",
    "Beauty & Fitness",
    "Books & Literature",
    "Business & Industrial",
    "Computers & Electronics",
    "Finance",
    "Food & Drink",
    "Games",
    "Health",
    "Hobbies & Leisure",
    "Home & Garden",
    "Internet & Telecom",
    "Jobs & Education",
    "Law & Government",
    "News",
    "Online Communities",
    "People & Society",
    "Pets & Animals",
    "Real Estate",
    "Reference",
    "Science",
    "Shopping",
    "Sports",
    "Travel & Transportation",
    "World Localities",
]


def classify_website(content: str) -> str:
    max_length = 1024  # based on Bart hugginface documentation
    # if the content is too long, truncate it
    truncated_content = ' '.join(content.split()[:max_length])

    # Perform zero-shot classification
    result = classifier(truncated_content, categories)

    # retrun the 1st top predicted category
    return result['labels'][0]


# Example usage
if __name__ == "__main__":
    sample_content = "Welcome to our online store. Shop the latest trends in fashion, electronics, and home decor."
    category = classify_website(sample_content)
    print(f"Predicted category: {category}")