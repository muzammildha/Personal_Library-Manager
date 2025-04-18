import streamlit as st
import sqlite3

def init_db():
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS books 
                 (id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER)''')
    conn.commit()
    conn.close()

def add_book(title, author, year):
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute("INSERT INTO books (title, author, year) VALUES (?, ?, ?)", (title, author, year))
    conn.commit()
    conn.close()

def get_books():
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute("SELECT * FROM books")
    books = c.fetchall()
    conn.close()
    return books

def delete_book(book_id):
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()

st.set_page_config(page_title="Personal Library Manager")
st.title("Personal Library Manager")

init_db()

menu = ["Add Book", "View Library", "Delete Book"]
choice = st.sidebar.selectbox("Select Action", menu)

if choice == "Add Book":
    st.subheader("Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=1000, max_value=2100, step=1)
    
    if st.button("Add Book "):
        if title and author and year:
            add_book(title, author, year)
            st.success(f"'{title}' by {author} added to library!")
        else:
            st.warning("Please enter details!")

elif choice == "View Library":
    st.subheader("Your Library")
    books = get_books()
    if books:
        for book in books:
            st.write(f" **{book[1]}** by *{book[2]}* ({book[3]})")
    else:
        st.info("No books found!")

elif choice == "Delete Book":
    st.subheader("Remove Book")
    books = get_books()
    if books:
        book_dict = {f"{book[1]} by {book[2]} ({book[3]})": book[0] for book in books}
        selected_book = st.selectbox("Select a book to delete", list(book_dict.keys()))
        if st.button(" Delete Book"):
            delete_book(book_dict[selected_book])
            st.success(" Book successfully deleted!")
    else:
        st.info("i.No books to delete!")
