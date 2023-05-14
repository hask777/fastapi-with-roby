from fastapi import FastAPI
from enum import Enum
from typing import Optional

app = FastAPI()

BOOKS = {
    'book_1': {'title': 'Title One', 'author': "Author One"},
    'book_2': {'title': 'Title Two', 'author': "Author Two"},
    'book_3': {'title': 'Title Three', 'author': "Author Three"},
    'book_4': {'title': 'Title Four', 'author': "Author Four"},
    'book_5': {'title': 'Title Five', 'author': "Author Five"}
}

class DirectionName(str, Enum):
    north = "North"
    east = "East"
    west = "West"
    south = "South"

@app.get("/deriction/{direction_name}")    
async def get_direction(direction_name: DirectionName):
    if direction_name == DirectionName.north:
        return {"Direction": direction_name, "sub": "Up"}  
    if direction_name == DirectionName.east:
        return {"Direction": direction_name, "sub": "Left"} 
    if direction_name == DirectionName.west:
        return {"Direction": direction_name, "sub": "Right"} 
    if direction_name == DirectionName.south:
        return {"Direction": direction_name, "sub": "Down"}

# get all books

@app.get("/")
async def read_all_books(skip_book: Optional[str] = None):
    if skip_book:
        new_books = BOOKS.copy()
        del new_books[skip_book] 
        return new_books
    return BOOKS

# get book

@app.get("/{book_name }")
async def read_book(book_name: str):
    return BOOKS[book_name]

# create book

@app.post('/')
async def create_book(book_title, book_author):
    current_book_id = 0

    if len(BOOKS) > 0:
        for book in BOOKS:
            x = int(book.split('_')[-1])
            if x > current_book_id:
                current_book_id = x
    
    BOOKS[f'book_{current_book_id + 1}'] = {'title': book_title, 'author': book_author}
    return BOOKS[f'book_{current_book_id + 1}']

# change book

@app.put("/{book_name}")
async def update(book_name: str, book_title: str, book_author: str):
    book_information = {"book_title": book_title, "book_author": book_author}
    BOOKS[book_name] = book_information
    return book_information


# delete book

@app.delete("/{book_name}")
async def delete_book(book_name):
    del BOOKS[book_name]
    return f'Book {book_name} is deleted'

# read book with query params

@app.get("/assignment/")
async def read_book_assignment(book_name: str):
    return BOOKS[book_name]

# delete book by query params

@app.delete("/assignment/")
async def delete_book_assignment(book_name):
    del BOOKS[book_name]
    return BOOKS