import mysql.connector

mydb = mysql.connector.connect(
  host="192.168.1.115",
  user="hesson",
  passwd="hesson",
  database='ebook',
  port=3306
)

cursor = mydb.cursor()

TABLES = {}

TABLES['books'] = (
    """CREATE TABLE `books` (
      `book_id` varchar(10),
      `author` varchar(100),
      `book_url` varchar(100)
      `book_name` varchar(300)
    )""")

TABLES['picture_book'] = (
    """CREATE TABLE `picture_book` (
      `picture_url` varchar(100),
      `book_id` varchar(10),
      `chapter_num` int(10)
    )""")

TABLES['picture_word'] = (
    """CREATE TABLE `picture_word` (
      `picture_url` varchar(100),
      `word` varchar(30)
    )""")


for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        print("Oh no")
    else:
        print("OK")

cursor.close()
mydb.close()