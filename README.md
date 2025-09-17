The Book Management App is a simple desktop application built with Python and PyQt5 that allows users to manage their personal library. Users can add, delete, search, and filter books while keeping track of useful statistics such as the total number of books and the average rating.

Features

Add Books – Add new books with title, author, genre, and rating (1–5).

Delete Books – Remove selected books from the list.

Search & Filter – Search books by genre or rating with error handling for invalid input.

Statistics – View total number of books and the average rating.

Custom Styles – Load a stylesheet (styles.css) to personalize the UI.

Error Handling – User-friendly error messages with auto-clear.

File Handling

The app uses Python’s file handling features to store book data in data/books.txt.

Read mode (r) – Loads books when the app starts.

Append mode (a) – Saves new books when added.

Write mode (w) – Updates the file when a book is deleted.

Requirements

Python 3.x

PyQt5

Install dependencies with:

pip install pyqt5

Usage

Run the application:

python book_app.py


Add books with title, author, genre, and rating.

Use the search bar and filter dropdown to narrow results.

View library statistics at the bottom of the app.

File Structure
project/
│-- data/books.txt     # Stores book records
│-- styles.css         # UI styling
│-- ui/book_ui.ui      # PyQt5 UI file
│-- book_app.py        # Main application
