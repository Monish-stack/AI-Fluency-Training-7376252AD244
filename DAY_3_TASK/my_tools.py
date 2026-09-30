# my_tools.py

library_books = {
    "clean code": {
        "author": "Robert C. Martin",
        "available_copies": 2
    },
    "the pragmatic programmer": {
        "author": "Andrew Hunt and David Thomas",
        "available_copies": 0
    },
    "atomic habits": {
        "author": "James Clear",
        "available_copies": 4
    },
    "introduction to algorithms": {
        "author": "Thomas H. Cormen",
        "available_copies": 1
    },
    "python crash course": {
        "author": "Eric Matthes",
        "available_copies": 3
    }
}


def check_book_availability(book_name):
    """
    Check the current availability of a book in the college library.
    """

    book_name = book_name.lower().strip()

    if book_name not in library_books:
        return f"Book '{book_name}' was not found in the library records."

    book = library_books[book_name]

    if book["available_copies"] > 0:
        return (
            f"Book: {book_name.title()}\n"
            f"Author: {book['author']}\n"
            f"Available copies: {book['available_copies']}\n"
            f"Status: Available"
        )

    return (
        f"Book: {book_name.title()}\n"
        f"Author: {book['author']}\n"
        f"Available copies: 0\n"
        f"Status: Not available"
    )


# Test the tool directly
if __name__ == "__main__":
    result = check_book_availability("Clean Code")
    print(result)