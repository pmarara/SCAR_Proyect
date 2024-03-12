import streamlit as st
import pandas as pd
from streamlit_card import card

class Genre:
    def __init__(self, genre_id, genre_name):
        self.genre_id = genre_id
        self.genre_name = genre_name

class Movie:
    def __init__(self, movie_id, genres, title_year):
        self.movie_id = movie_id
        self.genres = genres
        self.title_year = title_year

class User:
    def __init__(self, user_id, age, gender, occupation):
        self.user_id = user_id
        self.age = age
        self.gender = gender
        self.occupation = occupation

class Rating:
    def __init__(self, user_id, movie_id, rating):
        self.user_id = user_id
        self.movie_id = movie_id
        self.rating = rating

# Cargar datos de genre.txt
genre_data = pd.read_csv("genre.txt", sep='\t', names=['GenreID', 'GenreName'], encoding="utf-8")
genres = {row['GenreID']: Genre(row['GenreID'], row['GenreName']) for _, row in genre_data.iterrows()}

# Cargar datos de items.txt
items_data = pd.read_csv("items.txt", sep='\t', names=['MovieID'] + [f'Genre_{i}' for i in range(1, 20)] + ['TitleYear'], encoding="latin-1")
movies = {row['MovieID']: Movie(row['MovieID'], row.iloc[1:20], row['TitleYear']) for _, row in items_data.iterrows()}

# Cargar datos de users.txt
users_data = pd.read_csv("users.txt", sep='\t', names=['UserID', 'Age', 'Gender', 'Occupation'], encoding="utf-8")
users = {row['UserID']: User(row['UserID'], row['Age'], row['Gender'], row['Occupation']) for _, row in users_data.iterrows()}

# Cargar datos de u1_base.txt
ratings_data = pd.read_csv("u1_base.txt", sep='\t', names=['UserID', 'MovieID', 'Rating'], encoding="utf-8")
ratings = {(row['UserID'], row['MovieID']): Rating(row['UserID'], row['MovieID'], row['Rating']) for _, row in ratings_data.iterrows()}


st.title("Welcome to the Palu movie recommender!")  

highest_id = len(users)
uid = st.number_input("Please enter your User ID:", 1, highest_id, None)
  
if uid is not None:
  rec = st.selectbox("Pick type of recommendation", ["Demographic", "Based on content", "Collaborative", "Hybrid"])
  
  recommendations = []
  class Recommendation:
      def __init__(self, title, ratio):
          self.title = title
          self.ratio = ratio
  recommendations.append(Recommendation(movies[uid+0].title_year, 88))
  recommendations.append(Recommendation(movies[uid+1].title_year, 90))
  recommendations.append(Recommendation(movies[uid+2].title_year, 92))
  
  for i, e in enumerate(recommendations):
    card(
      key="card" + str(i),
      title=e.title,
      text="Ratio: " + str(e.ratio),
      styles={
        "card": {
          "width": "700px",
          "height": "150px",
          "margin": "0px",
          "box-shadow": "none",
        },
        "title": {
          "font-size": "1.75em",
        }
      }
    )