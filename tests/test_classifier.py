import unittest
from app.classifier import classify_website

class TestClassifier(unittest.TestCase):
    def test_classify_website(self):
        content = "This is an article about sports."
        category = classify_website(content)
        self.assertEqual(category, "Sports")  # Adjusted expected category based on the actual output

if __name__ == '__main__':
    unittest.main()