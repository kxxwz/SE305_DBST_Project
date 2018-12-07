#!/usr/bin/env python3

from bs4 import BeautifulSoup
import re
import numpy as np
from tqdm import tqdm
import os

MAX_BOOK_ID = 100

OUT_DIR = 'output'
B_OUT_DIR = '{}/book_info'.format(OUT_DIR)
P_OUT_DIR = '{}/pic_info'.format(OUT_DIR)
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(B_OUT_DIR, exist_ok=True)
os.makedirs(P_OUT_DIR, exist_ok=True)

def main():
    ###################
    ######
    ###### Extract Book Info
    ######
    ###################
    path = '../raw_data_sample/book_info'
    book_ids, book_names, languages, authors, b_urls = [], [], [], [], []
    missed = []
    decode_err = []

    for book_id in tqdm(range(1, MAX_BOOK_ID)):
        try:
            html = open('{}/{}.html'.format(path, book_id), 'r', encoding='ISO-8859-1')
            soup = BeautifulSoup(html, features='lxml')
        except FileNotFoundError:
            # print('{} missed!'.format(book_id))
            missed.append(book_id)
            continue
        except UnicodeDecodeError:
            # print('{} decoding error'.format(book_id))
            decode_err.append(book_id)
            continue

        # book_name
        try:
            book_name = soup.find(name='th', text='Title')
            book_name = book_name.parent.td.get_text().strip().replace('\n', ', ')
        except AttributeError:
            book_name = 'Unknown'
        
        # author
        try:
            language = soup.find(name='th', text='Language')
            language = language.parent.td.get_text().strip().replace('\n', ', ')
        except AttributeError:
            author = 'Unknown'
        
        # language
        try:
            author = soup.find(name='th', text='Author')
            author = author.parent.td.get_text().strip().replace('\n', ', ')
        except AttributeError:
            author = 'Unknown'
        
        # b_url
        try:
            # b_url = 'https:' + soup.find(text=re.compile('Read this book online')).parent['href']
            b_url = 'https:' + soup.find(text='Read this book online: HTML').parent['href']
        except AttributeError:
            b_url = 'Unknown'
            continue

        book_ids.append(book_id)
        book_names.append(book_name)
        languages.append(language)
        authors.append(author)
        b_urls.append(b_url)

        # intermediate save
        if len(book_ids) % 100 == 0:
            np.save('{}/book_ids'.format(B_OUT_DIR), book_ids)
            np.save('{}/book_names'.format(B_OUT_DIR), book_names)
            np.save('{}/languages'.format(B_OUT_DIR), languages)
            np.save('{}/authors'.format(B_OUT_DIR), authors)
            np.save('{}/b_urls'.format(B_OUT_DIR), b_urls)

    # final save
    np.save('{}/book_ids'.format(B_OUT_DIR), book_ids)
    np.save('{}/book_names'.format(B_OUT_DIR), book_names)
    np.save('{}/languages'.format(B_OUT_DIR), languages)
    np.save('{}/authors'.format(B_OUT_DIR), authors)
    np.save('{}/b_urls'.format(B_OUT_DIR), b_urls)   

    # write to txt file
    book_num = len(book_ids)
    print('{} books'.format(book_num))
    with open('{}/Books.txt'.format(OUT_DIR), 'w') as file:
        file.write('book_id \t book_name \t author \t b_url \t language \n')
        for i in range(book_num):
            try:
                file.write('{0} \t {1} \t {2} \t {3} \t {4} \n'.format(
                        book_ids[i], book_names[i], authors[i], b_urls[i], languages[i])
                    )
            except:
                pass 


    ###################
    ######
    ###### Extract Pic Info
    ######
    ###################
    path = '../raw_data_sample/book_content'
    p_book_ids, chap_nums, p_urls, dep_words = [], [], [], []
    missed = []
    decode_err = []
    valid_books = []

    idx = -1
    for book_id in tqdm(book_ids):
        idx += 1
        try:
            html = open('{}/{}.html'.format(path, book_id), 'r', encoding='ISO-8859-1')
            soup = BeautifulSoup(html, features='lxml')
        except FileNotFoundError:
            # print('{} missed!'.format(book_id))
            missed.append(book_id)
            continue
        except UnicodeDecodeError:
            # print('{} decoding error'.format(book_id))
            decode_err.append(book_id)
            continue
        
        chap_num = 0
        next_ele = soup.title
        # print(next_ele)
        # print(book_id)

        pic_save_flag = False
        while next_ele != None:
            if next_ele.name in ['h2', 'h3']:
                text = next_ele.get_text().strip().lower().split()
                if 'chapter' in text and 'chapter' == text[0]:
                    chap_num += 1
                    # print(text, chap_num)
            
            if (chap_num > 0) and (next_ele.name == 'img'):
                alt = next_ele['alt'].strip().replace('\n', ', ')
                pic_save_flag = (len(alt.split()) > 2)
                src = next_ele['src']
                backslash = b_urls[idx].rfind('/')
                p_url = b_urls[idx][:backslash] + '/' + src
                
                if pic_save_flag:
                    p_book_ids.append(book_id)
                    chap_nums.append(chap_num)
                    p_urls.append(p_url)
                    dep_words.append(alt)
                
            next_ele = next_ele.next_element
        
        if (chap_num > 0) and pic_save_flag:
            valid_books.append(book_id)

        # intermediate save
        if len(p_book_ids) % 100 == 0:
            np.save('{}/p_book_ids'.format(P_OUT_DIR), p_book_ids)
            np.save('{}/chap_nums'.format(P_OUT_DIR), chap_nums)
            np.save('{}/p_urls'.format(P_OUT_DIR), p_urls)
            np.save('{}/dep_words'.format(P_OUT_DIR), dep_words)

    # final save
    np.save('{}/p_book_ids'.format(P_OUT_DIR), p_book_ids)
    np.save('{}/chap_nums'.format(P_OUT_DIR), chap_nums)
    np.save('{}/p_urls'.format(P_OUT_DIR), p_urls)
    np.save('{}/dep_words'.format(P_OUT_DIR), dep_words)

    # write to txt file
    pic_num = len(p_book_ids)
    print('{} pictures in {} books'.format(pic_num, len(valid_books)))
    with open('{}/Pictures.txt'.format(OUT_DIR), 'w') as file:
        file.write('book_id \t chap_num \t p_url \t desp_words \n')
        for i in range(pic_num):
            file.write('{0} \t {1} \t {2} \t {3} \n'.format(
                        p_book_ids[i], chap_nums[i], p_urls[i], dep_words[i])
                    )

if __name__ == '__main__':
    main()