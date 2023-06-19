# Book API

This Flask application provides endpoints for managing books, including storing books from OpenLibrary, retrieving books, searching books based on criteria, creating new book entries, and deleting books.

## Technologies Used

The application is built using the following technologies:

* **Flask**
* **PostgreSQL**
* **SQLAlchemy**

## Endpoints

### `POST /store_openlib_books`

Stores books from OpenLibrary.

* Method: `POST`
* Request Body: JSON object with a list of book codes from OpenLibrary.

* Response: JSON object with information about the added books (those inserted successfully into the database) and skipped books (those skipped because of errors or missing fields).

### `GET /books`

Retrieves all books from the database.

* Method: `GET`
* Response: JSON object with a list of all the books in the database.

### `GET /books/search`

Searches books based on specified criteria (author, work, number of pages). At least one of the three criteria must be specified.

* Method: `GET`
* Query Parameters:
  * `author`: Name of the author to filter the books by.
  * `work`: Title of the work to filter the books by.
  * `min_pages`: Minimum number of pages a book should have.
* Response: JSON object with a list of books that match the specified criteria.

### `POST /books`

Creates a new book entry.

Method: `POST`

* Request Body: JSON object containing the book data.
* Response: JSON object with the status of the book creation.

### `DELETE /books/<book_id>`

This endpoint handles the deletion of a book.

Method: `DELETE`

* Path Parameter: book_id - ID of the book to be deleted.
* Response: JSON object with the status of the book deletion.

## Dockerized Deployment

The application can be easily deployed using Docker and Docker Compose. The provided docker-compose.yml file sets up a Docker container for the Book API and a Docker container running PostgreSQL as the database.

## Running the application

1. To run the application, follow these steps:

2. Make sure you have Docker and Docker Compose installed on your machine.

3. Clone this repository.
4. Rename the provided `.env.example` file to `.env`. This file will be used to set the required environment variables for the application. Replace the given values with your desired ones.
5. Open a terminal or command prompt and navigate to the root directory of the application.
6. Run the following command to start the application:

    ```bash
    docker-compose up -d
    ```

7. Wait for the containers to start up.

8. Access the book API at `http://localhost:5000`.

9. To stop the application and remove the containers, run:

    ```bash
    docker-compose down
    ```

## Running Unit Tests

You can run unit tests for the API. Follow these steps:

1. Make sure you have the Docker containers up and running by following the instructions in the previous section.

2. Attach a shell to the Flask Book API container.
3. Once inside the container, navigate to the root directory of the application.
4. Run the tests.py file using the following command:

    ```bash
    python tests.py
    ```

This will execute the unit tests defined in the tests.py file.

## Usage Examples

Here are some examples demonstrating how to hit the API endpoints:

### Filling the Database with 10 Books

To fill the database with 10 books, including titles like "1984," "Misery," "The Shining," and others, make a `POST` request to the `/store_openlib_books` endpoint with the following request body:

```json
POST /store_openlib_books
Content-Type: application/json

{
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
        "OL27170045M"
    ]
}
```

The API will store the books in the database and return a 200 OK response if the operation is successful.

### Retrieving All Books

To retrieve all books from the database, make a `GET` request to the `/books` endpoint:

```json
GET /books
```

The API will respond with a 200 OK status code and return a JSON object containing a list of all books in the database.

### Searching Books

To search for books based on specific criteria (author, work, minimum number of pages), make a `GET` request to the /books/search endpoint with the desired query parameters.

For example, to search for books with an author containing "Steph," a work containing "Mis," and a minimum of 100 pages, make the following request:

```json
GET /books/search?author=Steph&work=Mis&min_pages=100
```

The API will respond with a 200 OK status code and return a JSON object containing a list of books that match the specified criteria.

### Creating a New Book Entry

To create a new book entry in the database, make a `POST` request to the `/books` endpoint with the following request body:

```json
POST /books
Content-Type: application/json
{
    "id": "BOOKTEST123M",
    "title": "The Example Book",
    "number_of_pages": 250,
    "authors": [
        {"id": "AUTHOR1A", "name": "John Smith"},
        {"id": "AUTHOR2A", "name": "Jane Doe"}
    ],
    "works": [
        {"id": "WORK1W", "title": "Work A"},
        {"id": "WORK2W", "title": "Work B"}
    ]
}
```

The API will create a new book entry with the provided details and return a 200 OK response if the operation is successful.

### Deleting a Book

To delete a book from the database, make a `DELETE` request to the `/books/<book_id>` endpoint, where `<book_id>` represents the unique identifier of the book you want to delete.

For example, to delete a book with the ID "OL10426195M," make the following request:

```json
DELETE /books/OL10426195M
```

The API will respond with a 200 OK status code if the book is successfully deleted.
