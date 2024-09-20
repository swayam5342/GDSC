import requests

def get_book_info(book_title):
    url = f"https://www.googleapis.com/books/v1/volumes?q={book_title}"
    response = requests.get(url)
    data = response.json()
    
    if 'items' in data:
        book = data['items'][0]['volumeInfo']
        title = book.get('title', 'N/A')
        authors = ', '.join(book.get('authors', ['N/A']))
        genre = ', '.join(book.get('categories', ['N/A']))
        return title, authors, genre
    else:
        return None, None, None

book_title = "To Kill a Mockingbird"
title, author, genre = get_book_info(book_title)
print(title, author, genre)