from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

books = {}
authors = {}


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/add_book', methods=['POST'])
def add_book():
    data = request.get_json()
    book_id = data.get('book_id')
    title = data.get('title')
    author_ids = data.get('author_ids', [])

    if book_id and title:
        for author_id in author_ids:
            if author_id not in authors:
                return jsonify({'error': f'Автор с идентификатором {author_id} не найден.'}), 404

        books[book_id] = {
            'title': title,
            'author_ids': author_ids
        }
        return jsonify({'message': 'Книга успешно добавлена!'})
    else:
        return jsonify({'error': 'Идентификатор книги и заголовок обязательны.'}), 400


@app.route('/get_book/<book_id>', methods=['GET'])
def get_book(book_id):
    if book_id in books:
        return jsonify(books[book_id])
    else:
        return jsonify({'error': 'Книга не найдена.'}), 404


@app.route('/add_author', methods=['POST'])
def add_author():
    data = request.get_json()
    author_id = data.get('author_id')
    name = data.get('name')
    books_written = data.get('books_written', [])

    if author_id and name:
        for book_id in books_written:
            if book_id not in books:
                return jsonify({'error': f'Книга с идентификатором {book_id} не найдена.'}), 404

        authors[author_id] = {
            'name': name,
            'books_written': books_written
        }
        return jsonify({'message': 'Автор успешно добавлен!'})
    else:
        return jsonify({'error': 'Идентификатор автора и имя обязательны.'}), 400


@app.route('/get_author/<author_id>', methods=['GET'])
def get_author(author_id):
    if author_id in authors:
        return jsonify(authors[author_id])
    else:
        return jsonify({'error': 'Автор не найден.'}), 404


@app.route('/get_all_books', methods=['GET'])
def get_all_books():
    return jsonify(books)


@app.route('/get_all_authors', methods=['GET'])
def get_all_authors():
    return jsonify(authors)


if __name__ == '__main__':
    app.run(debug=True)
