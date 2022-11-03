import pandas as pd
from matplotlib import pyplot as plt
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
        df_books = pd.read_csv(book, sep=';', encoding='iso-8859-1', on_bad_lines='warn',
                               low_memory=False)

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
# Convert str to ints and account for list index vs pandas index.

malformed_line_index = [int(i) - 1 for i in malformed_line_list]

malformed_book_lines = []


def get_lines(file, line_numbers):
    return (x for i, x in enumerate(file) if i in line_numbers)


with open(book, 'r') as g:
    lines = get_lines(g, malformed_line_index)

    for line in lines:
        malformed_book_lines.append(line)

# print(malformed_book_lines)

# Print shapes of datasets

print('Books dataset has {} entries with {} features each.'.format(*df_books.shape))
print('Ratings dataset has {} entries with {} features each.'.format(*df_rat.shape))
print('Users dataset has {} entries with {} features each.'.format(*df_users.shape))

print('Books.csv missing values: \n')
print(pd.DataFrame({'percent_missing': df_books.isnull().sum() * 100 / len(df_books)}))
print('\n')
print('Book-Ratings.csv missing values: \n')
print(pd.DataFrame({'percent_missing': df_rat.isnull().sum() * 100 / len(df_rat)}))
print('\n')
print('Users.csv missing values: \n')
print(pd.DataFrame({'percent_missing': df_users.isnull().sum() * 100 / len(df_users)}))
print('\n')

# df_books[df_books.columns] = df_books[df_books.columns].astype('category') # LUL can't believe it worked

print('Data types for Books.csv')
print(df_books.dtypes, end='\n')
df_books.drop(['Image-URL-S', 'Image-URL-M', 'Image-URL-L'], axis=1, inplace=True)

print('Datatypes for Users.csv', end='\n')
print(df_users.dtypes, end='\n')



df_books.loc[df_books.ISBN == '0789466953','Year-Of-Publication'] = 2000
df_books.loc[df_books.ISBN == '0789466953','Book-Author'] = "James Buckley"
df_books.loc[df_books.ISBN == '0789466953','Publisher'] = "DK Publishing Inc"
df_books.loc[df_books.ISBN == '0789466953','Book-Title'] = "DK Readers: Creating the X-Men, How Comic Books Come to Life (Level 4: Proficient Readers)"

df_books.loc[df_books.ISBN == '078946697X','Year-Of-Publication'] = 2000
df_books.loc[df_books.ISBN == '078946697X','Book-Author'] = "Michael Teitelbaum"
df_books.loc[df_books.ISBN == '078946697X','Publisher'] = "DK Publishing Inc"
df_books.loc[df_books.ISBN == '078946697X','Book-Title'] = "DK Readers: Creating the X-Men, How It All Began (Level 4: Proficient Readers)"

df_books.loc[df_books.ISBN == '2070426769','Year-Of-Publication'] = 2003
df_books.loc[df_books.ISBN == '2070426769','Book-Author'] = "Jean-Marie Gustave Le ClÃ?Â©zio"
df_books.loc[df_books.ISBN == '2070426769','Publisher'] = "Gallimard"
df_books.loc[df_books.ISBN == '2070426769','Book-Title'] = "Peuple du ciel, suivi de 'Les Bergers"

# Convert the column Year of publication to Datetime and drop the rows that have malformed year of publication.




df_books['Year-Of-Publication'] = pd.to_numeric(df_books['Year-Of-Publication'], errors='coerce')
# df_books.dropna(inplace=True)

######