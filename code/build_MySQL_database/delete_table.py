import mysql.connector

mydb = mysql.connector.connect(
  host="192.168.1.115",
  user="hesson",
  passwd="hesson",
  database='ebook',
  port=3306
)

cursor = mydb.cursor()

sql = "DROP TABLE books"

cursor.execute(sql)

sql = "DROP TABLE picture_book"

cursor.execute(sql)

sql = "DROP TABLE picture_word"

cursor.execute(sql)

sql = "DROP TABLE book_id_name"

cursor.execute(sql)