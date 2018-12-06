# SE305 DBST Project
Course Project for SE305 Database System Techniques

## Structure
```
project
│   README.md
│      
└───code
│   │   process_raw.ipynb
│   │   Books.txt
│   │   Pictures.txt
│   │
└───raw_data_sample
    │   book_content
    │   book_info
```

## Entity
- Book (**book\_id**, book\_name, author, b\_url, language)

| book\_id | book\_name | author | b\_url | language |
| :---: | :---: | :---: | :---: | :---: |
| * | * | * | * | * |

- Figure (book\_id, chap\_num, **p\_url**, desp_words)

| book\_id | chap\_num | p\_url | desp_words |
| :---: | :---: | :---: | :---: |
| * | * | * | * |


## Query

```
# Find the books according to the name, author.
def find_book(book_name, author):
	retun book_url

# Given a book and chapter number, you can return some relative pictures.
def find_pic_by_name_chapter(book_name, chapter_num):
	return [pic1_url, pic2_url]

# Given some words, you can find the relative pictures according to the words.
def find_pic_by_words(book_name, words):
	return [pic1_url, pic2_url]
```


