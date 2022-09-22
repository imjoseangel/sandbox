class Book:
    def __init__(self, title):
        self.title = title
        self.author = None

    def add_author(self, name):
        # add author property
        self.author = name

    def add_chapter(self, number, title):
        # add properties chapter_number and chapter_title
        self.chapter_number = number
        self.chapter_title = title


class BookInfo(Book):
    def __init__(self, title, price, info=False):
        Book.__init__(self, title)

        # add properties price and info
        self.info = info
        self.price = price
        self.stars = 0

    def rating(self, stars):
        try:
            # check if existing stars are less than new stars
            # and if new stars are greater than 4
            # adjust new price by a 20% increase
            if self.stars < stars and stars > 4:
                self.price = self.price * 1.2
            # update the stars property
            self.stars = stars
        except Exception as e:
            print(e, "Please try again")


# Create a book object titled 'Two Scoops of Django'
book = Book('Two Scoops of Django')
# Add the author 'Greenfeld'
book.add_author("Greenfeld")

# Add a chapter 3, with title 'Async Views'
book.add_chapter(3, "Async Views")

# Create a book_info object titled 'Two Scoops of Django'
# with a price of 10, and info set to True
book_info = BookInfo('Two Scoops of Django', 10, True)
# Give the book_info a rating of 5 stars
book_info.rating(5)

print("Book info: ", end=" ")
# Print book_info's title, stars and price
print(
    book_info.title, str(book_info.stars) + " stars",
    book_info.price, sep=", "
)
# Print all properties of book and book_info objects
print("Book properties: ", book.__dict__)
print("BookInfo properties: ", book_info.__dict__)
