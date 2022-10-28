import pandas as pd
# from matplotlib import pyplot as plt
from contextlib import redirect_stderr
import re

file_ratings = 'Data/BX-Book-Ratings.csv'
book = 'Data/BX-Books.csv'
users = 'Data/BX-Users.csv'

# Load the files into dataframes.
df_rat = pd.read_csv(file_ratings, sep=';', encoding='iso-8859-1')
# Some entries are malformed.
# df_books = pd.read_csv(book, sep=';', encoding='unicode_escape', on_bad_lines='warn', low_memory=False)
df_users = pd.read_csv(users, sep=';', encoding='iso-8859-1')

# The next code block will attempt to find the ISBNs of the books that are malformed.
# First redirect the error log to a file.

with open('mal.txt', 'w') as h:
    with redirect_stderr(h):
        df_books = pd.read_csv(book, sep=';', encoding='iso-8859-1', on_bad_lines='warn', low_memory=False)

malformed_line_list = []

# Next read the file and identify the lines using regex.
# Temp_list contains the lines in the BX-Books.csv that are malformed.

with open('mal.txt', 'r') as f:
    for line in f:
        # The following if-else statements goes around the index error created from the "empty" last line.
        if re.findall('\d+:', line):
            line_num = re.findall('\d+:', line)[0]
        else:
            continue
        malformed_line_list.append(line_num[:-1])
# Attempt to read specific lines from the Books.csv file.

malformed_line_index = [int(i)-1 for i in malformed_line_list]  # convert str to ints and account for list index.

malformed_book_lines = []


def get_lines(file, line_numbers):

    return (x for i, x in enumerate(file) if i in line_numbers)


with open(book, 'r') as g:

    lines = get_lines(g, malformed_line_index)

    for line in lines:
        malformed_book_lines.append(line)


print(malformed_book_lines)

# Drop the last columns with the image URLs from book data frame.
df_books.drop(['Image-URL-S', 'Image-URL-M', 'Image-URL-L'], axis=1, inplace=True)  # or assign it to new DF
a = df_books.shape

# Convert the column Year of publication to Datetime and drop the rows that have malformed year of publication.

df_books['Year-Of-Publication'] = pd.to_numeric(df_books['Year-Of-Publication'], downcast='signed', errors='coerce')
df_books.dropna(inplace=True)

b = df_books.shape
c = int((a[0] - b[0]))

print("Removed %s entries" % c)
# df_books['Year-Of-Publication'] = df_books['Year-Of-Publication'].astype("int32")
'''
df_rat.describe()
df_books.describe()
df_users.describe()
print("memory:", df_rat.info(memory_usage='deep'))
print("memory:", df_books.info(memory_usage='deep'))
print("memory:", df_users.info(memory_usage='deep'))
'''
