import unittest
from app import app


class BookAPITestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_store_openlib_books(self):
        # Test storing books from OpenLibrary:
        # 1984, Misery, The Shining, The Last Wish, Blood of elves,
        # Ai ai ai, Eragon, Don Quixote, Lotr, George R.R. Martin
        data = {
            "codes": [
                "OL24382006M",
                "OL20931016M",
                "OL22312685M",
                "OL10426195M",
                "OL24255147M",
                "OL47164721M",
                "OL3685343M",
                "OL6469521M",
                "OL5237526M",
                "OL27170045M",
            ]
        }
        response = self.app.post("/store_openlib_books", json=data)
        # print(response.data.decode("utf-8"))
        self.assertEqual(response.status_code, 200)
        # Add more assertions to validate the response data

    def test_get_all_books(self):
        # Test retrieving all books
        response = self.app.get("/books")
        self.assertEqual(response.status_code, 200)
        # Add more assertions to validate the response data

    def test_search_books(self):
        # Test searching books
        params = {"author": "Steph", "work": "Mis", "min_pages": 100}
        response = self.app.get("/books/search", query_string=params)
        self.assertEqual(response.status_code, 200)
        # Add more assertions to validate the response data

    def test_create_book(self):
        # Test creating a new book entry
        data = {
            "id": "BOOKTEST123M",
            "title": "The Example Book",
            "numbwer_of_pages": 250,
            "authors": [
                {"id": "AUTHOR1A", "name": "John Smith"},
                {"id": "AUTHOR2A", "name": "Jane Doe"},
            ],
            "works": [
                {"id": "WORK1W", "title": "Work A"},
                {"id": "WORK2W", "title": "Work B"},
            ],
        }
        response = self.app.post("/books", json=data)
        self.assertEqual(response.status_code, 200)
        # Add more assertions to validate the response data

    def test_delete_book(self):
        # Test deleting a book
        book_id = "OL10426195M"
        response = self.app.delete(f"/books/{book_id}")
        self.assertEqual(response.status_code, 200)
        # Add more assertions to validate the response data


if __name__ == "__main__":
    unittest.main()
