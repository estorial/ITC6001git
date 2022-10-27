import pandas as pd
from customs import CheckEntries

file_ratings = 'Data/BX-Book-Ratings.csv'
book = 'Data/BX-Books.csv'
users = 'Data/BX-Users.csv'

# Load the files into dataframes.
df_rat = pd.read_csv(file_ratings, sep=';', encoding='unicode_escape')
df_books = pd.read_csv(book, sep=';', encoding='unicode_escape', on_bad_lines='warn',low_memory=False,)  # Some entries are malformed.
df_users = pd.read_csv(users, sep=';', encoding='unicode_escape')

df_books.describe()

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
