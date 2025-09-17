import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic

class BookApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/book_ui.ui", self)

        self.books = []

        self.addBookBtn.clicked.connect(self.add_book)
        self.deleteBookBtn.clicked.connect(self.delete_book)
        self.filterButton.clicked.connect(self.filter_books)
        self.filterDropdown.currentTextChanged.connect(self.update_search_placeholder)

        self.load_books()

        self.load_stylesheet()

    def load_books(self):
        try:
            self.books = []
            with open("data/books.txt", "r") as file:
                line = file.readline()
                while line:
                    book = line.strip().split(',')
                    self.books.append(book)
                    line = file.readline()
        except FileNotFoundError:
            self.error_id.setText("Error: Books file not found.")
            self.books = []
        except Exception as e:
            self.error_id.setText(f"Error loading books: {str(e)}")
            self.books = []

        self.update_book_list(self.books)

        self.update_statistics()

    def update_book_list(self, books):
        self.bookList.clear()
        for book in books:
            self.bookList.addItem(f"Title: {book[0]}, Author: {book[1]}, Genre: {book[2]}, Rating: {book[3]}")

    def add_book(self):
        title = self.title_id.text()
        author = self.auhtor_id.text()
        genre = self.genre_id.text()
        rating = self.rating_id.text()

        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                raise ValueError("Rating must be between 1 and 5.")
        except ValueError as e:
            self.show_error_message(str(e))
            return

        if title and author and genre and rating:
            self.books.append([title, author, genre, rating])

            try:
                with open("data/books.txt", "a") as file:
                    file.write(f"{title},{author},{genre},{rating}\n")

                self.update_book_list(self.books)
                self.update_statistics()
                self.error_id.clear()

                self.title_id.clear()
                self.auhtor_id.clear()
                self.genre_id.clear()
                self.rating_id.clear()

            except Exception as e:
                self.show_error_message(f"Error saving book: {str(e)}")
        else:
            self.show_error_message("Error: Please fill all fields.")

    def delete_book(self):
        selected_item = self.bookList.currentItem()
        if selected_item:
            book_text = selected_item.text()

            selected_book = next((book for book in self.books if f"Title: {book[0]}" in book_text), None)

            if selected_book:
                self.books.remove(selected_book)

                try:
                    with open("data/books.txt", "w") as file:
                        for book in self.books:
                            file.write(f"{book[0]},{book[1]},{book[2]},{book[3]}\n")

                    self.update_book_list(self.books)
                    self.update_statistics()
                    self.error_id.clear()
                except Exception as e:
                    self.show_error_message(f"Error deleting book: {str(e)}")
            else:
                self.show_error_message("Error: Selected book not found.")
        else:
            self.show_error_message("Error: No book selected.")

    def filter_books(self):
        filter_option = self.filterDropdown.currentText()
        filter_value = self.search_button.text().strip().lower()

        if filter_option == "Genre":
            valid_genres = {book[2].lower() for book in self.books}

            if filter_value not in valid_genres:
                self.show_error_message("Error: Genre not found. Try again.")
                return
            else:
                self.error_id.setText("")

            filtered_books = [book for book in self.books if book[2].lower() == filter_value]

        elif filter_option == "Rating":
            try:
                filter_value = int(filter_value)

                if filter_value < 1 or filter_value > 5:
                    raise ValueError("Filter Rating must be between 1 and 5.")

                print("Books before filtering:", self.books)

                filtered_books = [book for book in self.books if int(book[3]) == filter_value]

                print("Filtered books:", filtered_books)

            except ValueError as e:
                self.show_error_message(f"Error: {str(e)}")
                return

        else:
            filtered_books = self.books

        self.update_book_list(filtered_books)
        self.update_statistics()

        self.search_button.clear()

    def update_statistics(self):
        total_books = len(self.books)
        avg_rating = sum(float(book[3]) for book in self.books) / total_books if total_books > 0 else 0

        stats_text = f"Total Books: {total_books} || Average Rating: {avg_rating:.2f}"

        self.statsid.setText(stats_text)

    def load_stylesheet(self):
        try:
            with open("styles.css", "r") as file:
                stylesheet = file.read()
                self.setStyleSheet(stylesheet)
        except FileNotFoundError:
            self.show_error_message("Error: Stylesheet file not found.")
        except Exception as e:
            self.show_error_message(f"Error loading stylesheet: {str(e)}")

    def update_search_placeholder(self):
        filter_option = self.filterDropdown.currentText()
        if filter_option == "Genre":
            self.search_button.setPlaceholderText("Search by Genre")
        elif filter_option == "Rating":
            self.search_button.setPlaceholderText("Search by Rating 1-5")
        else:
            self.search_button.setPlaceholderText("SEARCH")

    def show_error_message(self, message, duration=3000):
        self.error_id.setText(f"Error: {message}")
        QTimer.singleShot(duration, lambda: self.error_id.setText(""))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BookApp()
    window.show()
    sys.exit(app.exec_())
