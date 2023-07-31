function addBook() {
    const bookId = document.getElementById("book_id").value;
    const title = document.getElementById("title").value;
    const authorIds = document.getElementById("author_ids").value.split(',');

    fetch('/add_book', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            book_id: bookId,
            title: title,
            author_ids: authorIds
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("book-info").innerText = data.message;
    })
    .catch(error => {
        document.getElementById("book-info").innerText = error.error;
    });
}

function addAuthor() {
    const authorId = document.getElementById("author_id").value;
    const name = document.getElementById("name").value;
    const booksWritten = document.getElementById("books_written").value.split(',');

    fetch('/add_author', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            author_id: authorId,
            name: name,
            books_written: booksWritten
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("author-info").innerText = data.message;
    })
    .catch(error => {
        document.getElementById("author-info").innerText = error.error;
    });
}
