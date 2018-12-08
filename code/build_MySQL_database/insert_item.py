import mysql.connector
from datetime import date, datetime, timedelta

mydb = mysql.connector.connect(
  host="192.168.1.115",
  user="hesson",
  passwd="hesson",
  database='ebook',
  port=3306
)

def insert_data_into_books(cursor):
  with open ("Books.txt", 'r') as f:
    lines = f.readlines()
    for line in lines[1:]:
      try:
        items = line.split('\t')
        book_id, author, book_url = items[0], items[2], items[3]
        book_id = book_id.strip()
        author = author.strip().lower()
        book_url = book_url.strip()
        add_book = """
          INSERT INTO books
          (book_id, author, book_url)
          VALUES ('%s', '%s', '%s')
        """ % (book_id, author, book_url)
        cursor.execute(add_book)
      except:
        pass

def insert_data_into_picture_book(cursor):
  with open ("Pictures1.txt", 'r') as f:
    lines = f.readlines()
    for line in lines[1:]:
      try:
        items = line.split('\t')
        picture_url, book_id, chapter_num = items[2], items[0], items[1]
        picture_url = picture_url.strip()
        book_id = book_id.strip()
        chapter_num = chapter_num.strip()
        add_picture_book = """
          INSERT INTO picture_book
          (picture_url, book_id, chapter_num)
          VALUES ('%s', '%s', '%s')
        """ % (picture_url, book_id, chapter_num)
        cursor.execute(add_picture_book)
      except:
        pass

def insert_data_into_picture_word(cursor):
  with open ("Pictures2.txt", 'r') as f:
    lines = f.readlines()
    for line in lines[1:]:
      items = line.split('\t')
      picture_url, words = items[2], items[3]
      picture_url = picture_url.strip()
      words_list = words.replace('.', ' ').replace(',', ' ').strip().lower().split(' ')
      for word in set(words_list):
        try:
          add_picture_word = """
            INSERT INTO picture_word
            (picture_url, word)
            VALUES ('%s', '%s')
          """ % (picture_url, word)
          cursor.execute(add_picture_word)
        except:
          pass

def insert_data_into_book_id_name(cursor):
  with open ("Books.txt", 'r') as f:
    lines = f.readlines()
    for line in lines[1:]:
      try:
        items = line.split('\t')
        book_id, book_name = items[0], items[1]
        book_id = book_id.strip()
        book_name = book_name.strip().lower()
        add_id_name = """
          INSERT INTO book_id_name
          (book_id, book_name)
          VALUES ('%s', '%s')
        """ % (book_id, book_name)
        cursor.execute(add_id_name)
      except:
        pass


def main():
  cursor = mydb.cursor()
  insert_data_into_books(cursor)
  print("Finish 1")
  insert_data_into_picture_book(cursor)
  print("Finish 2")
  insert_data_into_picture_word(cursor)
  print("Finish 3")
  insert_data_into_book_id_name(cursor)
  print("Finish 4")
  mydb.commit()
  cursor.close()
  mydb.close()

if __name__ == '__main__':
    main()