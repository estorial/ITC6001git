import pandas as pd
import numpy as np
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

with open('mal.txt', 'w',encoding='iso-8859-1') as h:
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

print(malformed_book_lines)

# Rename columns to be easier to work with.
# Insert some convoluted way to automate it instead of typing it.

df_books.drop(['Image-URL-S', 'Image-URL-M', 'Image-URL-L'], axis=1, inplace=True) # Not going to use these.

df_books.columns = ['ISBN', 'BookTitle', 'BookAuthor', 'YearOfPublication', 'Publisher']
df_users.columns = ['UserID', 'Location', 'Age']
df_rat.columns = ['UserID', 'ISBN', 'BookRating']

# Print shapes of datasets1

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

df_books.loc[df_books.ISBN == '0789466953', 'YearOfPublication'] = 2000
df_books.loc[df_books.ISBN == '0789466953', 'BookAuthor'] = 'James Buckley'
df_books.loc[df_books.ISBN == '0789466953', 'Publisher'] = 'DK Publishing Inc'
df_books.loc[df_books.ISBN == '0789466953', 'BookTitle'] = 'DK Readers: Creating the X-Men, How Comic Books Come to Life (Level 4: Proficient Readers)'

df_books.loc[df_books.ISBN == '078946697X', 'YearOfPublication'] = 2000
df_books.loc[df_books.ISBN == '078946697X', 'BookAuthor'] = 'Michael Teitelbaum'
df_books.loc[df_books.ISBN == '078946697X', 'Publisher'] = 'DK Publishing Inc'
df_books.loc[df_books.ISBN == '078946697X', 'BookTitle'] = 'DK Readers: Creating the X-Men, How It All Began (Level 4: Proficient Readers)'

df_books.loc[df_books.ISBN == '2070426769', 'YearOfPublication'] = 2003
df_books.loc[df_books.ISBN == '2070426769', 'BookAuthor'] = "Jean-Marie Gustave Le ClÃ?Â©zio"
df_books.loc[df_books.ISBN == '2070426769', 'Publisher'] = 'Gallimard'
df_books.loc[df_books.ISBN == '2070426769', 'BookTitle'] = 'Peuple du ciel, suivi de \'Les Bergers'

# Convert the column Year of publication to Numeric and drop the rows that have malformed year of publication.

df_books['YearOfPublication'] = pd.to_numeric(df_books['YearOfPublication'], errors='coerce')
# df_books.dropna(inplace=True)

######User Exploration########
print('Datatypes for Users.csv', end='\n')
print(df_users.dtypes, end='\n \n')

print(f'There are {df_users.UserID.nunique()} unique user ID\'s and {df_users.UserID.count()} unique entries.')
print(sorted(df_users.Age.unique()))

df_users.loc[(df_users.Age<5) | (df_users.Age>100), 'Age'] = np.nan

print(f'There are {df_users.Age.isnull().sum()} empty age values in the set of {df_users.UserID.count()} users (or {(df_users.Age.isnull().sum()/df_users.UserID.count())*100:.2f}%).')
'''
u = df_users.Age.value_counts().sort_index()
plt.figure(figsize=(20, 10))
plt.rcParams.update({'font.size': 15}) # Set larger plot font size
plt.bar(u.index, u.values)
plt.xlabel('Age')
plt.ylabel('counts')
plt.show()
'''
# Fill the missing user ages with the mean value. Probably not going to be used later due to 40% of the values are empty.
df_users.Age.fillna(df_users.Age.mean())
# Print the authors with the most amount of entries.
df_auth_group = df_books.groupby("BookAuthor")
print(f'The authors with the most amount of entries on the dataframe:\n\
        {df_books.groupby("BookAuthor").size().sort_values(ascending=False)}')
df_auth_group['BookAuthor'].nunique()

#df_rat_gb_isbn = df_rat.groupby('ISBN').size().sort_values(ascending=False)

df_rat_gb_isbn = df_rat.groupby('ISBN')


df_book_rat_isbn = df_books.merge(df_rat, how='left', on='ISBN')

print(f'The authors with the most amount of entries on the dataframe:\n\
        {df_book_rat_isbn.groupby("BookAuthor").size().sort_values(ascending=False)}')

print(pd.DataFrame({'percent_missing': df_book_rat_isbn.isnull().sum() * 100 / len(df_book_rat_isbn)}))