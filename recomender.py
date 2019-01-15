# Similar Movies example using movie lens data for example

import pandas as pd
import numpy as np

# Load data
rating_cols = ['user_id', 'movie_id', 'rating']
ratings = pd.read_csv('./data/u.data', sep='\t', names=rating_cols, usecols=range(3), encoding="ISO-8859-1")

movie_cols = ['movie_id', 'title']
movies = pd.read_csv('./data/u.item', sep='|', names=movie_cols, usecols=range(2), encoding="ISO-8859-1")

ratings = pd.merge(movies, ratings)

movie_ratings = ratings.pivot_table(index=['user_id'], columns=['title'], values='rating')

# Taking rating for star wars as an example
star_wars_ratings = movie_ratings['Star Wars (1977)']

similar_movies =  movie_ratings.corrwith(star_wars_ratings).dropna()
df = pd.DataFrame(similar_movies)
print('--- Similar Movies ---')
print(similar_movies.sort_values(ascending=False)[:10])

movie_stats = ratings.groupby('title').agg({ 'rating': [np.size, np.mean] })
# Movies with greater than 200 ratings
popular_movies = movie_stats['rating']['size'] >= 200
print('--- Popular Movies ---')
print(movie_stats[popular_movies].sort_values([('rating', 'mean')], ascending=False)[:10])

df = movie_stats[popular_movies].join(pd.DataFrame(similar_movies, columns=['similarity']))
print('--- Most popular and similar movies ---')
print(df.sort_values(['similarity'], ascending=False)[:20])