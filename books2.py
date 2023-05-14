from fastapi import FastAPI, HTTPException, Request, status, Form, Header
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from starlette.responses import JSONResponse


class NegativeNumberException(Exception):
    def __init__(self, books_to_return):
        self.book_to_return = books_to_return

app = FastAPI()

class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(title="Description of book", max_length=100, min_length=1)
    rating: int = Field(gt=-1, lt=101)

    class Config:
        schema_extra = {
            "example": {
                "id": "20e5a980-d785-4276-97b8-8872b9213e51",
                "title": "Computer science",
                "author": "Programmer",
                "description": "Description",
                "rating": 75
            }
        }

class BookNoRating(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str
    description: str = Field(
        None, title="description of the Book", max_length=100, min_length=1
    )

BOOKS = []

@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(request: Request, exception: NegativeNumberException):
    return JSONResponse(
        status_code=418,
        content=f"Hey why do you want {exception.book_to_return}, You need to read more books!"
    )

@app.post('/books/login')
async def book_login(username: str = Form(...), password: str = Form(...)):
    return {"username": username, "password": password}

@app.get('/header')
async def read_header(random_header: Optional[str] = Header(None)):
    return {'Random-Header': random_header}


@app.get('/')
async def read_all_books(books_to_return: Optional[int] = None):
    if books_to_return and books_to_return < 0:
        raise NegativeNumberException(books_to_return=books_to_return)

    if len(BOOKS) < 1:
        create_books_no_api()

    if books_to_return and len(BOOKS) >= books_to_return > 0:
        i = 1
        new_books = []
        while i <= books_to_return:
            new_books.append(BOOKS[i - 1])
            i += 1
        return new_books
    
    return BOOKS

@app.get("/book/{book_id}")
async def read_book(book_id: UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x
    raise raise_item_cannot_be_found_exception()

@app.get("/book/{book_id}", response_model=BookNoRating)
async def read_book_no_rating(book_id: UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x
    raise raise_item_cannot_be_found_exception()
        
@app.put("/{book_id}")
async def update_book(book_id: UUID, book: Book):
    counter = 0
    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            BOOKS[counter - 1] = book
            return BOOKS[counter - 1]
    raise raise_item_cannot_be_found_exception()
        
@app.delete("/{book_id}")
async def delete_book(book_id: UUID):
    counter = 0
    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            del BOOKS[counter - 1]
            return f'ID: {book_id} deleted'
    raise raise_item_cannot_be_found_exception()

@app.post('/', status_code=status.HTTP_201_CREATED)
async def create_book(book:Book):
    BOOKS.append(book)
    return BOOKS

def create_books_no_api():
    book_1 = Book(id='20e5a980-d785-4276-97b8-8872b9213e51',
                  title='title one',
                  author='author one',
                  description='description one',
                  rating=12
                  )
    book_2 = Book(id='20e5a940-d785-4276-97b8-8872b9213e51',
                  title='title two',
                  author='author two',
                  description='description two',
                  rating=13
                  )
    book_3 = Book(id='20e5a680-d785-4276-97b8-8872b9213e51',
                  title='title three',
                  author='author three',
                  description='description three',
                  rating=14
                  )
    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)


def raise_item_cannot_be_found_exception():
    return HTTPException(status_code=404, detail='book not found', headers={"X-Header-Error": "Nothing to be found in UUID"})