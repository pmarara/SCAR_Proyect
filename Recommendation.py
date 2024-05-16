
# Para iniciar: python -m streamlit run Recommendation.py

import streamlit as st
import pandas as pd
from streamlit_card import card
import numpy as np

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

class User_type:
    def __init__(self, type_id, min_age, max_age, gender, occupation, genres):
        self.type_id = type_id
        self.min_age = min_age
        self.max_age = max_age
        self.gender = gender
        self.occupation = occupation
        self.genres = genres

class Preference:
    def __init__(self, user_id, genres):
        self.user_id = user_id
        self.genres = genres

def selectMovies(genre_weights):
    # Retrieve list of movies already rated by the user
    rated_movies = [rating.movie_id for rating in ratings.values() if rating.user_id == uid]
        
    # Calcular ratios para cada película
    for movie_id, movie in movies.items():
        if movie_id not in rated_movies:  # Check if user hasn't watched the movie
            movie_genres = np.array(movie.genres)
                
            # normalization by sum of genre weights
            normalization_factor = np.sum(genre_weights)
                
            # # normalization by sum of genre weights and sum of movie genres (pro: normalization not only by genre weights but also by movie genres; con: very low ratios)
            # normalization_factor = np.sum(genre_weights) * np.sum(movie_genres)
                
            # # normalization by maximum scalar product (pro: normalization not only by genre weights but also by movie genres; con: a lot of movies with ratio 1)
            # num_genres = np.sum(movie_genres)
            # normalization_factor = np.sum(np.sort(genre_weights)[-num_genres:])

            ratio = np.dot(genre_weights, movie_genres) / normalization_factor # Normalización
            recommendations.append(Recommendation(movie, round(ratio, 4)))
    return recommendations


# Cargar datos de genre.txt
genre_data = pd.read_csv("data/genre.txt", sep='\t', names=['GenreID', 'GenreName'], encoding="utf-8")
genres = {row['GenreID']: Genre(row['GenreID'], row['GenreName']) for _, row in genre_data.iterrows()}

# Cargar datos de items.txt
items_data = pd.read_csv("data/items.txt", sep='\t', names=['MovieID'] + [f'Genre_{i}' for i in range(1, 20)] + ['TitleYear'], encoding="latin-1")
movies = {row['MovieID']: Movie(row['MovieID'], row.iloc[1:20], row['TitleYear']) for _, row in items_data.iterrows()}

# Cargar datos de users.txt
users_data = pd.read_csv("data/users.txt", sep='\t', names=['UserID', 'Age', 'Gender', 'Occupation'], encoding="utf-8")
users = {row['UserID']: User(row['UserID'], row['Age'], row['Gender'], row['Occupation']) for _, row in users_data.iterrows()}

# Cargar datos de u1_base.txt
ratings_data = pd.read_csv("data/u1_base.txt", sep='\t', names=['UserID', 'MovieID', 'Rating'], encoding="utf-8")
ratings = {(row['UserID'], row['MovieID']): Rating(row['UserID'], row['MovieID'], row['Rating']) for _, row in ratings_data.iterrows()}





st.title("Welcome to the Palu movie recommender!")  

highest_id = len(users)
uid = st.number_input("Please enter your User ID:", 1, highest_id, None)

rec_type = st.selectbox("Pick type of recommendation", ["Demographic", "Based on content", "Collaborative", "Hybrid"])
  
if uid is not None:

  recommendations = []

  class Recommendation:
        def __init__(self, movie, ratio):
            self.movie = movie
            self.ratio = ratio


  #Recomendación Demográfica
  if rec_type == "Demographic":

    recommendations = []

    # Cargar datos de users_types.txt
    user_types_data = pd.read_csv("data/user_types.txt", sep='\t', names=['TypeID', 'MinAge', 'MaxAge', 'Gender', 'Occupation'] + [f'Genre_{i}' for i in range(1, 20)], encoding="utf-8")
    user_types = {row['TypeID']: User_type(row['TypeID'], row['MinAge'], row['MaxAge'], row['Gender'], row['Occupation'], row.iloc[5:24]) for _, row in user_types_data.iterrows()}

    # Cargar datos de users_types_assigned.txt
    user_types_assigned_data = pd.read_csv("data/user_types_assigned.txt", sep='\t', names=['UserID', 'TypeID'], encoding="utf-8")
    user_types_assigned = {row['UserID']: row['TypeID'] for _, row in user_types_assigned_data.iterrows()}

    if uid in user_types_assigned:
        type_id = user_types_assigned[uid]
        user_type = user_types[type_id]
        genre_weights = np.array(user_type.genres)
        recommendations = selectMovies(genre_weights)
        
        
  #Recomendación Basado en contenido
  if rec_type == "Based on content":

    recommendations = []

    # Cargar datos de vectoresbasadosContenido.txt
    preferences_based_on_content_data = pd.read_csv("data/VectoresBasadosContenido.txt", sep='\t', names=['UserID'] + [f'Genre_{i}' for i in range(1, 20)], encoding="utf-8")
    preferences_based_on_content = {row['UserID']: Preference(row['UserID'], row.iloc[1:20] ) for _, row in preferences_based_on_content_data.iterrows()}

    if uid in preferences_based_on_content:

        genre_weights = np.array(preferences_based_on_content[uid].genres)
        recommendations = selectMovies( genre_weights)
        

  # Ordenar por ratio y obtener las 5 películas superiores
  recommendations.sort(key=lambda x: x.ratio, reverse=True)

        
    
    
    
  for i, r in enumerate(recommendations[:5]):
    card(
      key="Recommendation " + str(i),
      title=r.movie.title_year,
      text="Ratio: " + str(r.ratio),
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
